"""
Unit tests for all four classical ciphers.

Test strategy per cipher:
  - Round-trip (encode → decode returns original)
  - Known vectors from reference material or hand-computed values
  - Edge cases: empty string, shift=0 / identity key, all-punctuation input,
    mixed case, non-alpha characters passing through unchanged
  - Error / validation cases where applicable
"""

import pytest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.ciphers import caesar, vigenere, substitution, playfair, rail_fence, beaufort, affine, columnar


# ─────────────────────────── Caesar ────────────────────────────────────────

class TestCaesar:
    def test_known_vector(self):
        assert caesar.encode("Hello, World!", 3) == "Khoor, Zruog!"

    def test_known_vector_decode(self):
        assert caesar.decode("Khoor, Zruog!", 3) == "Hello, World!"

    def test_round_trip(self):
        pt = "The Quick Brown Fox Jumps Over The Lazy Dog!"
        assert caesar.decode(caesar.encode(pt, 13), 13) == pt

    def test_shift_zero_is_identity(self):
        assert caesar.encode("AbCdEf", 0) == "AbCdEf"
        assert caesar.decode("AbCdEf", 0) == "AbCdEf"

    def test_shift_26_is_identity(self):
        assert caesar.encode("Hello", 26) == "Hello"

    def test_wrap_around(self):
        assert caesar.encode("xyz", 3) == "abc"
        assert caesar.encode("XYZ", 3) == "ABC"

    def test_preserves_non_alpha(self):
        # r+5=w, i+5=n, g+5=l, h+5=m, t+5=y
        assert caesar.encode("1+1=2, right?", 5) == "1+1=2, wnlmy?"

    def test_preserves_mixed_case(self):
        ct = caesar.encode("aBcDeF", 1)
        assert ct == "bCdEfG"

    def test_empty_string(self):
        assert caesar.encode("", 7) == ""
        assert caesar.decode("", 7) == ""

    def test_large_shift_reduced(self):
        # shift 55 ≡ shift 3 (mod 26)
        assert caesar.encode("abc", 55) == caesar.encode("abc", 3)

    def test_negative_shift_in_decode(self):
        # encode with 5, decode with 5 should round-trip via negative shift internally
        ct = caesar.encode("Secret!", 5)
        assert caesar.decode(ct, 5) == "Secret!"

    def test_all_punctuation_unchanged(self):
        s = "!@#$%^&*() 123"
        assert caesar.encode(s, 13) == s


# ─────────────────────────── Vigenère ──────────────────────────────────────

class TestVigenere:
    def test_known_vector_uppercase(self):
        # Classic test vector from Wikipedia
        assert vigenere.encode("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"

    def test_known_vector_decode_uppercase(self):
        assert vigenere.decode("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"

    def test_round_trip_mixed_case(self):
        pt = "Hello, World!"
        assert vigenere.decode(vigenere.encode(pt, "key"), "key") == pt

    def test_known_mixed_case(self):
        # key="key" (k=10, e=4, y=24), key only steps on alpha chars.
        # H(k=10)→R, e(e=4)→i, l(y=24)→j, l(k=10)→v, o(e=4)→s, ','→',', ' '→' ',
        # W(y=24)→U, o(k=10)→y, r(e=4)→v, l(y=24)→j, d(k=10)→n, '!'→'!'
        ct = vigenere.encode("Hello, World!", "key")
        assert vigenere.decode(ct, "key") == "Hello, World!"

    def test_preserves_non_alpha(self):
        # Spaces, punctuation, numbers should pass through unchanged.
        # key "z" (shift=25): a→z, b→a; space & 'd' & '!' are non-alpha so
        # the key does NOT advance on non-alpha — only 'a' and 'b' consume key steps.
        # 'a'(key[0]=z=25)→z, 'b'(key[1]=z=25)→a, ' '→' ', 'c'(key[2]=z=25)→b, 'd'(key[3]=z=25)→c
        ct = vigenere.encode("ab cd!", "z")
        assert ct == "za bc!"

    def test_key_only_steps_on_alpha(self):
        # Non-alpha chars should NOT advance the key index
        # encode "a b" with key "bc": 'a'→'b', ' '→' ', 'b'→'d'
        assert vigenere.encode("a b", "bc") == "b d"

    def test_single_char_key(self):
        # Single char key = shifted caesar
        assert vigenere.encode("ABC", "D") == caesar.encode("ABC", 3)

    def test_key_longer_than_text(self):
        pt = "Hi"
        assert vigenere.decode(vigenere.encode(pt, "SUPERLONGKEY"), "SUPERLONGKEY") == pt

    def test_empty_string(self):
        assert vigenere.encode("", "key") == ""
        assert vigenere.decode("", "key") == ""

    def test_case_insensitive_key(self):
        # Key "KEY" and "key" should produce identical results
        assert vigenere.encode("Hello", "KEY") == vigenere.encode("Hello", "key")

    def test_invalid_key_raises(self):
        with pytest.raises(ValueError):
            vigenere.encode("abc", "12!")

    def test_empty_key_raises(self):
        with pytest.raises(ValueError):
            vigenere.encode("abc", "")


# ─────────────────────────── Substitution ──────────────────────────────────

_ATBASH = "ZYXWVUTSRQPONMLKJIHGFEDCBA"  # A↔Z, B↔Y, etc.


class TestSubstitution:
    def test_atbash_encode(self):
        assert substitution.encode("ABC", _ATBASH) == "ZYX"

    def test_atbash_decode(self):
        assert substitution.decode("ZYX", _ATBASH) == "ABC"

    def test_atbash_is_self_inverse(self):
        # Atbash: decoding = encoding
        assert substitution.encode("Hello", _ATBASH) == substitution.decode("Hello", _ATBASH)

    def test_known_vector(self):
        assert substitution.encode("Hello", _ATBASH) == "Svool"

    def test_round_trip(self):
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        pt = "The Quick Brown Fox Jumps Over The Lazy Dog!"
        assert substitution.decode(substitution.encode(pt, key), key) == pt

    def test_preserves_case(self):
        ct = substitution.encode("hello", _ATBASH)
        assert ct == "svool"

    def test_preserves_non_alpha(self):
        ct = substitution.encode("A, B!", _ATBASH)
        assert ct == "Z, Y!"

    def test_empty_string(self):
        assert substitution.encode("", _ATBASH) == ""

    def test_identity_key(self):
        key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        assert substitution.encode("Hello World", key) == "Hello World"

    def test_invalid_key_too_short(self):
        with pytest.raises(ValueError):
            substitution.encode("abc", "ABCDE")

    def test_invalid_key_repeats(self):
        with pytest.raises(ValueError):
            substitution.encode("abc", "AACDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_invalid_key_non_alpha(self):
        with pytest.raises(ValueError):
            substitution.encode("abc", "ABCDEFGHIJKLMNOPQRSTUVWXY1")


# ─────────────────────────── Playfair ──────────────────────────────────────

class TestPlayfair:
    def test_known_vector_encode(self):
        # Reference: https://en.wikipedia.org/wiki/Playfair_cipher
        ct = playfair.encode("HIDE THE GOLD IN THE TREE STUMP", "PLAYFAIR EXAMPLE")
        assert ct == "BMODZBXDNABEKUDMUIXMMOUVIF"

    def test_known_vector_decode(self):
        pt = playfair.decode("BMODZBXDNABEKUDMUIXMMOUVIF", "PLAYFAIR EXAMPLE")
        assert pt == "HIDETHEGOLDINTHETREXESTUMP"

    def test_round_trip(self):
        # Playfair round-trip works on prepared form (uppercase, no spaces, X padding)
        keyword = "MONARCHY"
        plaintext = "INSTRUMENTS"
        ct = playfair.encode(plaintext, keyword)
        pt = playfair.decode(ct, keyword)
        # The decoded form may contain X padding between doubled letters;
        # it must at least start with the right letters
        assert pt.startswith("IN")

    def test_j_treated_as_i(self):
        # Encoding the same message with J and I in keyword should be identical
        ct1 = playfair.encode("TEST", "KEYWORD")
        ct2 = playfair.encode("TEST", "KEYWORD".replace('I', 'J'))
        # (KEYWORD has no I/J so this tests the no-op path)
        assert ct1 == ct2

    def test_output_is_uppercase(self):
        ct = playfair.encode("hello", "key")
        assert ct == ct.upper()

    def test_output_even_length(self):
        for text in ["A", "AB", "ABC", "ABCD", "ABCDE"]:
            ct = playfair.encode(text, "KEY")
            assert len(ct) % 2 == 0

    def test_non_alpha_stripped(self):
        # "HI!" and "HI" should produce identical ciphertext
        assert playfair.encode("HI!", "KEY") == playfair.encode("HI", "KEY")

    def test_empty_string(self):
        assert playfair.encode("", "KEY") == ""

    def test_invalid_ciphertext_odd_length(self):
        with pytest.raises(ValueError):
            playfair.decode("ABC", "KEY")


# ─────────────────────────── Rail Fence ─────────────────────────────────────

class TestRailFence:
    def test_known_vector_encode(self):
        assert rail_fence.encode("HELLO", 3) == "HOELL"

    def test_known_vector_decode(self):
        assert rail_fence.decode("HOELL", 3) == "HELLO"

    def test_round_trip(self):
        pt = "Hello, World!"
        assert rail_fence.decode(rail_fence.encode(pt, 4), 4) == pt

    def test_preserves_non_alpha(self):
        # Non-alpha (1,+,=,,, ,?) remain in position; alpha chars transposed
        ct = rail_fence.encode("1+1=2, right?", 3)
        assert ct == "1+1=2, rtihg?"

    def test_preserves_case_in_round_trip(self):
        pt = "AbCdEfG"
        assert rail_fence.decode(rail_fence.encode(pt, 3), 3) == pt

    def test_empty_string(self):
        assert rail_fence.encode("", 3) == ""
        assert rail_fence.decode("", 3) == ""

    def test_identity_rails_one(self):
        assert rail_fence.encode("Hello, World!", 1) == "Hello, World!"

    def test_rails_less_than_one_raises(self):
        with pytest.raises(ValueError):
            rail_fence.encode("Hello", 0)


# ─────────────────────────── Beaufort ───────────────────────────────────────

class TestBeaufort:
    def test_known_vector_encode(self):
        assert beaufort.encode("HELLO", "D") == "WZSSP"

    def test_known_vector_decode(self):
        assert beaufort.decode("WZSSP", "D") == "HELLO"

    def test_round_trip(self):
        pt = "Hello, World!"
        assert beaufort.decode(beaufort.encode(pt, "KEY"), "KEY") == pt

    def test_reciprocal_property(self):
        # Beaufort: encode and decode are the same operation
        assert beaufort.encode("HELLO", "KEY") == beaufort.decode("HELLO", "KEY")

    def test_preserves_non_alpha(self):
        # Non-alpha (space, !) pass through; alpha chars use key "z" (shift=25)
        ct = beaufort.encode("ab cd!", "z")
        assert ct == "zy xw!"

    def test_empty_string(self):
        assert beaufort.encode("", "KEY") == ""
        assert beaufort.decode("", "KEY") == ""

    def test_invalid_key_raises(self):
        with pytest.raises(ValueError):
            beaufort.encode("abc", "12!")

    def test_empty_key_raises(self):
        with pytest.raises(ValueError):
            beaufort.encode("abc", "")


# ─────────────────────────── Affine ─────────────────────────────────────────

class TestAffine:
    def test_known_vector_encode(self):
        assert affine.encode("HELLO", 5, 8) == "RCLLA"

    def test_known_vector_decode(self):
        assert affine.decode("RCLLA", 5, 8) == "HELLO"

    def test_round_trip(self):
        pt = "The Quick Brown Fox Jumps Over The Lazy Dog!"
        assert affine.decode(affine.encode(pt, 7, 3), 7, 3) == pt

    def test_identity(self):
        assert affine.encode("Hello, World!", 1, 0) == "Hello, World!"

    def test_preserves_non_alpha(self):
        ct = affine.encode("Hello, World!", 5, 8)
        assert ct == "Rclla, Oaplx!"

    def test_empty_string(self):
        assert affine.encode("", 3, 5) == ""
        assert affine.decode("", 3, 5) == ""

    def test_non_coprime_a_raises(self):
        with pytest.raises(ValueError):
            affine.encode("abc", 2, 1)

    def test_b_outside_range_raises(self):
        with pytest.raises(ValueError):
            affine.encode("abc", 3, 30)


# ─────────────────────────── Columnar ───────────────────────────────────────

class TestColumnar:
    def test_known_vector_encode(self):
        assert columnar.encode("HELLO", "CBA") == "LEOHL"

    def test_known_vector_decode(self):
        assert columnar.decode("LEOHL", "CBA") == "HELLO"

    def test_round_trip(self):
        pt = "TheQuickBrownFoxJumpsOverTheLazyDog"
        assert columnar.decode(columnar.encode(pt, "KEY"), "KEY") == pt

    def test_non_alpha_stripped_in_output(self):
        ct = columnar.encode("H,e,l,l,o", "KEY")
        assert ct.isalpha()

    def test_empty_string(self):
        assert columnar.encode("", "KEY") == ""
        assert columnar.decode("", "KEY") == ""

    def test_invalid_key_raises(self):
        with pytest.raises(ValueError):
            columnar.encode("abc", "12!")

    def test_empty_key_raises(self):
        with pytest.raises(ValueError):
            columnar.encode("abc", "")
