"""Tests for the Secure Vault — AES-256-GCM + PBKDF2 + entropy estimator."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.vault import crypto

client = TestClient(app)


class TestEncryptDecrypt:
    """Round-trip encryption and decryption."""

    def test_round_trip_simple(self):
        ct = crypto.encrypt("Hello, World!", "hunter2")
        pt = crypto.decrypt(ct, "hunter2")
        assert pt == "Hello, World!"

    def test_round_trip_long_text(self):
        plaintext = "The quick brown fox jumps over the lazy dog. " * 10
        ct = crypto.encrypt(plaintext, "correct horse battery staple")
        pt = crypto.decrypt(ct, "correct horse battery staple")
        assert pt == plaintext

    def test_round_trip_unicode(self):
        ct = crypto.encrypt("café résumé 日本語 🚀", "p@ssw0rd!")
        pt = crypto.decrypt(ct, "p@ssw0rd!")
        assert pt == "café résumé 日本語 🚀"

    def test_round_trip_empty_passphrase(self):
        """Passphrase can technically be empty (though not recommended)."""
        ct = crypto.encrypt("test", "")
        pt = crypto.decrypt(ct, "")
        assert pt == "test"

    def test_wrong_passphrase_raises(self):
        ct = crypto.encrypt("secret", "correct passphrase")
        with pytest.raises(ValueError, match="Decryption failed"):
            crypto.decrypt(ct, "wrong passphrase")

    def test_tampered_ciphertext_raises(self):
        ct = crypto.encrypt("secret", "passphrase")
        # Corrupt a byte in the middle
        corrupted = ct[:10] + ("X" if ct[10] != "X" else "Y") + ct[11:]
        with pytest.raises((ValueError, Exception)):
            crypto.decrypt(corrupted, "passphrase")

    def test_different_keys_produce_different_ciphertexts(self):
        """Same plaintext + different passphrases → different ciphertexts (due to random salt/iv)."""
        ct1 = crypto.encrypt("hello", "key1")
        ct2 = crypto.encrypt("hello", "key2")
        assert ct1 != ct2

    def test_same_key_produces_different_ciphertexts(self):
        """Same plaintext + same passphrase → different ciphertexts (random salt/iv)."""
        ct1 = crypto.encrypt("hello", "key")
        ct2 = crypto.encrypt("hello", "key")
        assert ct1 != ct2


class TestEntropyEstimator:
    """Passphrase entropy estimation."""

    def test_empty(self):
        result = crypto.estimate_entropy("")
        assert result["strength"] == "empty"
        assert result["entropy_bits"] == 0.0

    def test_lowercase_only(self):
        result = crypto.estimate_entropy("abcdef")
        assert result["charset_size"] == 26
        expected = 6 * (26).bit_length()  # log2(26) ≈ 4.7 → 6*4.7 ≈ 28.2
        assert result["entropy_bits"] > 20
        assert result["strength"] in ("very weak", "weak")

    def test_mixed_case_digits_symbols(self):
        result = crypto.estimate_entropy("Tr0ub4dor&3")
        assert result["charset_size"] >= 26 + 26 + 10 + 32  # all categories
        assert result["entropy_bits"] > 50
        assert result["strength"] in ("reasonable", "strong")

    def test_long_passphrase(self):
        result = crypto.estimate_entropy("correct horse battery staple")
        assert result["length"] >= 20
        assert result["charset_size"] >= 26  # lowercase + spaces (not in standard charset groups)
        assert result["entropy_bits"] > 80
        assert result["strength"] == "very strong"

    def test_strength_scale(self):
        """Verify strength classification across the range."""
        assert crypto.estimate_entropy("a")["strength"] == "very weak"
        # "aB3$" — 4 chars, charset 94 → 26 bits, still very weak
        assert crypto.estimate_entropy("aB3$")["strength"] == "very weak"
        assert crypto.estimate_entropy("aB3$xyz1")["strength"] == "reasonable"
        assert crypto.estimate_entropy("Tr0ub4dor&3")["strength"] in ("reasonable", "strong")
        assert crypto.estimate_entropy("correct horse battery staple")["strength"] == "very strong"


class TestVaultAPI:
    """Integration tests for the vault API endpoints via TestClient."""

    def test_encrypt_decrypt_round_trip(self):
        resp = client.post("/api/vault/encrypt", json={
            "plaintext": "Hello API!",
            "passphrase": "api-test-key"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "ciphertext" in data
        assert data["algorithm"] == "AES-256-GCM + PBKDF2-HMAC-SHA256"

        # Decrypt back
        resp2 = client.post("/api/vault/decrypt", json={
            "ciphertext": data["ciphertext"],
            "passphrase": "api-test-key"
        })
        assert resp2.status_code == 200
        assert resp2.json()["plaintext"] == "Hello API!"

    def test_decrypt_wrong_passphrase(self):
        resp = client.post("/api/vault/encrypt", json={
            "plaintext": "secret",
            "passphrase": "correct"
        })
        ct = resp.json()["ciphertext"]

        resp2 = client.post("/api/vault/decrypt", json={
            "ciphertext": ct,
            "passphrase": "wrong"
        })
        assert resp2.status_code == 400

    def test_entropy_endpoint(self):
        resp = client.post("/api/vault/entropy", json={
            "passphrase": "Tr0ub4dor&3"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "entropy_bits" in data
        assert "strength" in data
        assert data["length"] > 0
