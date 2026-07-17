"""
Secure Vault — AES-256-GCM encryption with PBKDF2 key derivation.

Non-negotiable rules (matching Cipher Lab's educational but correct ethos):
- Never roll custom crypto. All primitives come from the `cryptography` library.
- Use AES-256-GCM for authenticated encryption (confidentiality + integrity).
- Derive encryption keys via PBKDF2 with HMAC-SHA256 and a random salt.
- Each encryption generates a fresh random salt and IV — no key/IV reuse.
- Output format: base64-encoded concatenation of salt | iv | tag | ciphertext.
"""

import os
import math
import string
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# ── Constants ──────────────────────────────────────────────────────────

SALT_LENGTH = 16          # bytes, recommended for PBKDF2
IV_LENGTH = 12             # bytes, recommended for AES-GCM (96 bits)
TAG_LENGTH = 16            # bytes, GCM appends this to ciphertext automatically
KEY_LENGTH = 32            # bytes = 256 bits for AES-256
PBKDF2_ITERATIONS = 600_000  # OWASP 2023 recommendation for PBKDF2-HMAC-SHA256

# ── Public API ─────────────────────────────────────────────────────────

def encrypt(plaintext: str, passphrase: str) -> str:
    """
    Encrypt plaintext with a passphrase using AES-256-GCM + PBKDF2.

    Returns a base64-encoded string: base64(salt || iv || ciphertext_with_tag).
    """
    salt = os.urandom(SALT_LENGTH)
    iv = os.urandom(IV_LENGTH)
    key = _derive_key(passphrase, salt)

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, plaintext.encode("utf-8"), None)

    # bundle: salt + iv + ciphertext (which includes the GCM tag)
    bundle = salt + iv + ciphertext
    return base64.b64encode(bundle).decode("ascii")


def decrypt(payload: str, passphrase: str) -> str:
    """
    Decrypt a base64-encoded payload produced by `encrypt()`.

    Raises ValueError if the passphrase is wrong or the ciphertext is
    tampered with (AES-GCM authentication check).
    """
    bundle = base64.b64decode(payload)

    salt = bundle[:SALT_LENGTH]
    iv = bundle[SALT_LENGTH:SALT_LENGTH + IV_LENGTH]
    ciphertext = bundle[SALT_LENGTH + IV_LENGTH:]

    key = _derive_key(passphrase, salt)

    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(iv, ciphertext, None)
    except Exception as exc:
        raise ValueError("Decryption failed — wrong passphrase or corrupted data.") from exc

    return plaintext.decode("utf-8")


def estimate_entropy(passphrase: str) -> dict:
    """
    Estimate the entropy of a passphrase in bits.

    Returns a dict with:
      - length:         character count
      - charset_size:   size of the character set detected
      - entropy_bits:   log2(charset_size ** length)
      - strength:       label (very weak / weak / reasonable / strong / very strong)
    """
    length = len(passphrase)
    charset_size = _detect_charset_size(passphrase)

    if length == 0:
        return {"length": 0, "charset_size": 0, "entropy_bits": 0.0, "strength": "empty"}

    bits = length * math.log2(charset_size)

    strength = _classify_strength(bits)
    return {
        "length": length,
        "charset_size": charset_size,
        "entropy_bits": round(bits, 2),
        "strength": strength,
    }


# ── Internal helpers ───────────────────────────────────────────────────

def _derive_key(passphrase: str, salt: bytes) -> bytes:
    """Derive a 256-bit AES key from a passphrase using PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return kdf.derive(passphrase.encode("utf-8"))


def _detect_charset_size(passphrase: str) -> int:
    """Count the number of distinct character categories used."""
    size = 0
    if any(c in string.ascii_lowercase for c in passphrase):
        size += 26
    if any(c in string.ascii_uppercase for c in passphrase):
        size += 26
    if any(c in string.digits for c in passphrase):
        size += 10
    if any(c in string.punctuation for c in passphrase):
        size += 32
    # Fallback: if nothing matched (e.g., only spaces or unicode), use 128
    return size if size > 0 else 128


def _classify_strength(bits: float) -> str:
    """Classify entropy bits into human-readable strength labels."""
    if bits < 30:
        return "very weak"
    elif bits < 40:
        return "weak"
    elif bits < 60:
        return "reasonable"
    elif bits < 80:
        return "strong"
    else:
        return "very strong"
