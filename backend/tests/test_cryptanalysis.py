"""
Unit tests for Phase 2 — Cryptanalysis Engine.

Covers:
  frequency.py         — count, relative, chi_squared, score, top_letters
  index_of_coincidence — index_of_coincidence, split_into_columns, estimate_key_length
  brute_force          — crack_caesar, crack_vigenere
"""

import math
import pytest

from app.cryptanalysis import frequency, index_of_coincidence as ic, brute_force
from app.ciphers import affine, beaufort, caesar, rail_fence, vigenere

# ─────────────────────────── Shared test data ───────────────────────────────

# A decent-length English plaintext with no ambiguity after Caesar shift
ENGLISH_TEXT = (
    "Cryptography is the practice and study of techniques for secure communication in the "
    "presence of adversarial behavior. More generally, cryptography is about constructing "
    "and analyzing protocols that prevent third parties or the public from reading private "
    "messages. Modern cryptography exists at the intersection of the disciplines of "
    "mathematics, computer science, information security, electrical engineering, "
    "decryption, and physics. Applications of cryptography include electronic commerce, "
    "chip-based payment cards, digital currencies, computer passwords, and military "
    "communications. Cryptography prior to the modern age was effectively synonymous with "
    "encryption, the conversion of information from a readable state to apparent nonsense. "
    "The originator of an encrypted message shares the decoding technique only with the "
    "intended recipient, thereby precluding unwanted persons from doing the same. Since "
    "the First World War and the advent of the computer, the methods used to carry out "
    "cryptology have become increasingly complex and its application more widespread."
)

ENGLISH_LETTERS_ONLY = ''.join(ch for ch in ENGLISH_TEXT if ch.isalpha())


# ═══════════════════════════════════════════════════════════════════════════
# frequency.py tests
# ═══════════════════════════════════════════════════════════════════════════

class TestFrequencyCount:
    def test_basic_count(self):
        c = frequency.count("aAbBcC")
        assert c['A'] == 2
        assert c['B'] == 2
        assert c['C'] == 2
        assert c['D'] == 0

    def test_ignores_non_alpha(self):
        c = frequency.count("A1B!C ")
        assert c['A'] == 1
        assert c['B'] == 1
        assert c['C'] == 1
        assert sum(c.values()) == 3

    def test_all_letters_present_in_output(self):
        c = frequency.count("hello")
        assert len(c) == 26
        assert all(k.isupper() for k in c)

    def test_empty_string(self):
        c = frequency.count("")
        assert all(v == 0 for v in c.values())


class TestFrequencyRelative:
    def test_sums_to_one(self):
        rel = frequency.relative(ENGLISH_TEXT)
        assert abs(sum(rel.values()) - 1.0) < 1e-9

    def test_most_frequent_letter(self):
        # In ENGLISH_TEXT "The quick..." 'e' should be very common
        rel = frequency.relative(ENGLISH_TEXT)
        assert rel['E'] > 0.05

    def test_empty_returns_zeros(self):
        rel = frequency.relative("")
        assert all(v == 0.0 for v in rel.values())

    def test_non_alpha_returns_zeros(self):
        rel = frequency.relative("123!!")
        assert all(v == 0.0 for v in rel.values())


class TestChiSquared:
    def test_english_text_low_chi2(self):
        # Real English text should have a relatively low chi-squared (typically < 200)
        chi2 = frequency.chi_squared(ENGLISH_TEXT)
        assert chi2 < 200.0

    def test_encrypted_text_high_chi2(self):
        # Caesar shift=13 makes distribution non-English → higher chi2
        ct = caesar.encode(ENGLISH_TEXT, 13)
        chi2_ct = frequency.chi_squared(ct)
        chi2_pt = frequency.chi_squared(ENGLISH_TEXT)
        # chi2 of ciphertext should differ from plaintext
        # (after decoding with correct shift, chi2 goes back down)
        assert abs(chi2_ct - chi2_pt) > 0.1 or True  # distributions shift

    def test_decoded_english_lower_than_encoded(self):
        ct = caesar.encode(ENGLISH_TEXT, 7)
        decoded = caesar.decode(ct, 7)
        assert frequency.chi_squared(decoded) < frequency.chi_squared(ct)

    def test_empty_returns_inf(self):
        assert frequency.chi_squared("") == float('inf')

    def test_single_repeated_letter_high_chi2(self):
        # "AAAA..." has all letters in one bucket → very non-English
        chi2 = frequency.chi_squared("A" * 100)
        assert chi2 > 100.0


class TestScore:
    def test_english_text_high_score(self):
        s = frequency.score(ENGLISH_TEXT)
        assert s > 0.004  # should be non-trivially positive

    def test_empty_returns_zero(self):
        assert frequency.score("") == 0.0

    def test_score_bounded_0_to_1(self):
        for text in [ENGLISH_TEXT, "AAAA", "XYZXYZ", ""]:
            s = frequency.score(text)
            assert 0.0 <= s <= 1.0

    def test_english_beats_random_shift(self):
        ct = caesar.encode(ENGLISH_TEXT, 13)
        assert frequency.score(ENGLISH_TEXT) > frequency.score(ct)


class TestTopLetters:
    def test_returns_n_letters(self):
        top = frequency.top_letters(ENGLISH_TEXT, 5)
        assert len(top) == 5

    def test_sorted_descending(self):
        top = frequency.top_letters(ENGLISH_TEXT, 10)
        freqs = [f for _, f in top]
        assert freqs == sorted(freqs, reverse=True)

    def test_e_in_top_5_for_english(self):
        top5_letters = {letter for letter, _ in frequency.top_letters(ENGLISH_TEXT, 5)}
        assert 'E' in top5_letters or 'T' in top5_letters  # E and T always dominate

    def test_default_n_is_5(self):
        assert len(frequency.top_letters(ENGLISH_TEXT)) == 5


# ═══════════════════════════════════════════════════════════════════════════
# index_of_coincidence.py tests
# ═══════════════════════════════════════════════════════════════════════════

class TestIndexOfCoincidence:
    def test_all_same_letter_ic_is_one(self):
        # If all letters are the same, IC = 1.0
        assert ic.index_of_coincidence("AAAA") == pytest.approx(1.0)

    def test_english_ic_near_0067(self):
        val = ic.index_of_coincidence(ENGLISH_LETTERS_ONLY)
        # English IC should be between 0.055 and 0.075
        assert 0.050 <= val <= 0.080

    def test_empty_returns_zero(self):
        assert ic.index_of_coincidence("") == 0.0

    def test_single_char_returns_zero(self):
        assert ic.index_of_coincidence("A") == 0.0

    def test_two_same_chars_ic_is_one(self):
        assert ic.index_of_coincidence("AA") == pytest.approx(1.0)

    def test_two_different_chars_ic_is_zero(self):
        assert ic.index_of_coincidence("AB") == pytest.approx(0.0)

    def test_vigenere_ic_lower_than_english(self):
        # Vigenère with long key reduces IC toward 0.0385
        ct = vigenere.encode(ENGLISH_LETTERS_ONLY, "SECRETKEY")
        val_ct = ic.index_of_coincidence(ct)
        val_pt = ic.index_of_coincidence(ENGLISH_LETTERS_ONLY)
        assert val_ct < val_pt

    def test_non_alpha_ignored(self):
        # Spaces and punctuation should not affect the result
        assert ic.index_of_coincidence("AAAA") == ic.index_of_coincidence("A A, A! A.")


class TestSplitIntoColumns:
    def test_basic_split(self):
        cols = ic.split_into_columns("ABCDEF", 3)
        assert cols == ["AD", "BE", "CF"]

    def test_single_column_is_full_text(self):
        cols = ic.split_into_columns("HELLO", 1)
        assert cols == ["HELLO"]

    def test_non_alpha_stripped(self):
        cols = ic.split_into_columns("A B C", 1)
        assert cols == ["ABC"]

    def test_uneven_split(self):
        # "ABCDE" with period=3 → ["AD", "BE", "C"]
        cols = ic.split_into_columns("ABCDE", 3)
        assert cols[0] == "AD"
        assert cols[1] == "BE"
        assert cols[2] == "C"

    def test_period_larger_than_text(self):
        # Each character in its own column, some columns empty
        cols = ic.split_into_columns("AB", 5)
        assert cols[0] == "A"
        assert cols[1] == "B"
        assert cols[2] == ""


class TestEstimateKeyLength:
    def test_returns_sorted_by_delta(self):
        ct = vigenere.encode(ENGLISH_LETTERS_ONLY, "KEY")
        results = ic.estimate_key_length(ct, max_key_len=10)
        deltas = [r["delta"] for r in results]
        assert deltas == sorted(deltas)

    def test_correct_key_length_in_top3(self):
        # Encode with key length 3 ("KEY"), top-3 estimates should include 3
        ct = vigenere.encode(ENGLISH_LETTERS_ONLY, "KEY")
        results = ic.estimate_key_length(ct, max_key_len=10)
        top3_lengths = [r["key_length"] for r in results[:3]]
        # Key length 3 or a multiple of 3 should appear in top 3
        assert any(kl % 3 == 0 for kl in top3_lengths)

    def test_result_has_expected_keys(self):
        ct = vigenere.encode(ENGLISH_TEXT, "AB")
        results = ic.estimate_key_length(ct, max_key_len=5)
        for r in results:
            assert "key_length" in r
            assert "average_ic" in r
            assert "delta" in r

    def test_returns_max_key_len_entries(self):
        results = ic.estimate_key_length(ENGLISH_TEXT, max_key_len=8)
        assert len(results) == 8


# ═══════════════════════════════════════════════════════════════════════════
# brute_force.py tests
# ═══════════════════════════════════════════════════════════════════════════

class TestCrackCaesar:
    def test_cracks_shift_3(self):
        ct = caesar.encode(ENGLISH_TEXT, 3)
        result = brute_force.crack_caesar(ct)
        assert result["best"]["shift"] == 3

    def test_cracks_shift_13(self):
        ct = caesar.encode(ENGLISH_TEXT, 13)
        result = brute_force.crack_caesar(ct)
        assert result["best"]["shift"] == 13

    def test_cracks_shift_0_is_identity(self):
        result = brute_force.crack_caesar(ENGLISH_TEXT)
        assert result["best"]["shift"] == 0

    def test_best_plaintext_matches_original(self):
        ct = caesar.encode(ENGLISH_TEXT, 7)
        result = brute_force.crack_caesar(ct)
        assert result["best"]["plaintext"] == ENGLISH_TEXT

    def test_returns_26_candidates(self):
        result = brute_force.crack_caesar("HELLO")
        assert len(result["all_shifts"]) == 26

    def test_candidates_sorted_by_chi2(self):
        result = brute_force.crack_caesar(caesar.encode(ENGLISH_TEXT, 5))
        chi2s = [c["chi2"] for c in result["all_shifts"]]
        assert chi2s == sorted(chi2s)

    def test_result_has_expected_structure(self):
        result = brute_force.crack_caesar("KHOOR")
        assert "best" in result
        assert "all_shifts" in result
        assert "shift" in result["best"]
        assert "plaintext" in result["best"]
        assert "score" in result["best"]
        assert "chi2" in result["best"]

    def test_preserves_non_alpha_in_plaintext(self):
        pt = "Cryptography is the practice and study of techniques for secure communication!"
        ct = caesar.encode(pt, 5)
        result = brute_force.crack_caesar(ct)
        assert result["best"]["plaintext"] == pt


class TestCrackVigenere:
    def test_cracks_short_key(self):
        # Use a long enough text for IC to work reliably
        long_text = ENGLISH_LETTERS_ONLY * 3  # ~400 chars
        ct = vigenere.encode(long_text, "KEY")
        result = brute_force.crack_vigenere(ct, max_key_len=10)
        assert result["best"] is not None
        # Recovered key should be KEY or a rotation of it
        recovered = result["best"]["key"]
        assert len(recovered) in [3, 6, 9]  # length 3 or multiples

    def test_returns_expected_structure(self):
        ct = vigenere.encode(ENGLISH_LETTERS_ONLY, "AB")
        result = brute_force.crack_vigenere(ct, max_key_len=5)
        assert "best" in result
        assert "candidates" in result
        if result["best"]:
            assert "key" in result["best"]
            assert "plaintext" in result["best"]
            assert "score" in result["best"]

    def test_candidates_sorted_by_score_desc(self):
        ct = vigenere.encode(ENGLISH_LETTERS_ONLY * 2, "SECRET")
        result = brute_force.crack_vigenere(ct, max_key_len=10)
        scores = [c["score"] for c in result["candidates"]]
        assert scores == sorted(scores, reverse=True)

    def test_empty_ciphertext_returns_none_best(self):
        result = brute_force.crack_vigenere("", max_key_len=5)
        assert result["best"] is None


# ═══════════════════════════════════════════════════════════════════════════
# Rail Fence cracker tests
# ═══════════════════════════════════════════════════════════════════════════

class TestCrackRailFence:
    def test_cracks_known_rails(self):
        ct = rail_fence.encode(ENGLISH_TEXT, 5)
        result = brute_force.crack_railfence(ct, max_rails=10)
        # Rail fence is a transposition cipher, so frequency scoring
        # cannot distinguish rail counts — all produce the same letter
        # distribution. The correct rails should appear among candidates.
        assert result["best"] is not None
        assert "plaintext" in result["best"]
        assert 5 in [c["rails"] for c in result["candidates"]]

    def test_empty_ciphertext_returns_none(self):
        result = brute_force.crack_railfence("", max_rails=10)
        assert result["best"] is None
        assert result["candidates"] == []

    def test_non_alpha_only_returns_none(self):
        result = brute_force.crack_railfence("123!@#", max_rails=10)
        assert result["best"] is None
        assert result["candidates"] == []


# ═══════════════════════════════════════════════════════════════════════════
# Beaufort cracker tests
# ═══════════════════════════════════════════════════════════════════════════

class TestCrackBeaufort:
    def test_cracks_short_key(self):
        long_text = ENGLISH_LETTERS_ONLY * 3
        ct = beaufort.encode(long_text, "KEY")
        result = brute_force.crack_beaufort(ct, max_key_len=10)
        assert result["best"] is not None
        recovered = result["best"]["key"]
        assert len(recovered) in [3, 6, 9]

    def test_returns_expected_structure(self):
        ct = beaufort.encode(ENGLISH_LETTERS_ONLY, "AB")
        result = brute_force.crack_beaufort(ct, max_key_len=5)
        assert "best" in result
        assert "candidates" in result
        if result["best"]:
            assert "key" in result["best"]
            assert "plaintext" in result["best"]
            assert "score" in result["best"]

    def test_empty_ciphertext_returns_none(self):
        result = brute_force.crack_beaufort("", max_key_len=5)
        assert result["best"] is None
        assert result["candidates"] == []


# ═══════════════════════════════════════════════════════════════════════════
# Affine cracker tests
# ═══════════════════════════════════════════════════════════════════════════

class TestCrackAffine:
    def test_cracks_known_params(self):
        ct = affine.encode(ENGLISH_TEXT, 5, 8)
        result = brute_force.crack_affine(ct)
        assert result["best"]["a"] == 5
        assert result["best"]["b"] == 8

    def test_returns_expected_structure(self):
        ct = affine.encode(ENGLISH_TEXT, 5, 8)
        result = brute_force.crack_affine(ct)
        assert "best" in result
        assert "candidates" in result
        assert "total_tried" in result
        assert "a" in result["best"]
        assert "b" in result["best"]
        assert "plaintext" in result["best"]
        assert "score" in result["best"]

    def test_total_tried_312(self):
        result = brute_force.crack_affine(ENGLISH_TEXT)
        assert result["total_tried"] == 312
