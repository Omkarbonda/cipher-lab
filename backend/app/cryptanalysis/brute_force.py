"""
Brute-force cryptanalysis attacks.

Provides:
  - crack_caesar(ciphertext)
      Try all 25 non-zero Caesar shifts, rank by chi-squared fitness,
      return results sorted best-first with the top candidate highlighted.

  - crack_vigenere(ciphertext, max_key_len)
      Full Vigenère cracker:
        1. Use IC to estimate the key length (top 3 candidates tested).
        2. For each candidate key length, split into columns.
        3. Crack each column independently with crack_caesar.
        4. Reconstruct the key and the full plaintext.
        5. Score the full plaintext and return the best result.

Both functions are pure (no side effects) and deterministic.
They return structured dicts that the FastAPI layer can serialise directly.
"""

from __future__ import annotations
import math
from app.cryptanalysis import frequency as freq_module
from app.cryptanalysis.frequency import chi_squared, score as freq_score
from app.cryptanalysis.index_of_coincidence import (
    estimate_key_length,
    index_of_coincidence,
    split_into_columns,
)
from app.ciphers import caesar, vigenere, substitution, playfair, rail_fence, beaufort, affine

_ALPHA_SIZE = 26
_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_ENGLISH_FREQ_ORDER = "ETAOINSHRDLUCMWFGYPBVKJXQZ"


# ──────────────────────────── Caesar cracker ────────────────────────────────

def crack_caesar(ciphertext: str) -> dict:
    """Try all 25 Caesar shifts and rank by English-fitness score.

    Args:
        ciphertext: The text to crack (any case; non-alpha preserved).

    Returns:
        {
          "best": {
              "shift":     int,    # most likely shift
              "plaintext": str,    # decoded text
              "score":     float,  # 0-1 fitness (higher = more English-like)
              "chi2":      float,  # chi-squared (lower = more English-like)
          },
          "all_shifts": [          # all 26 candidates sorted best-first
              {"shift": int, "plaintext": str, "score": float, "chi2": float},
              ...
          ]
        }

    Examples:
        >>> result = crack_caesar("Khoor, Zruog!")
        >>> result["best"]["shift"]
        3
        >>> result["best"]["plaintext"]
        'Hello, World!'
    """
    candidates = []
    for shift in range(_ALPHA_SIZE):
        plaintext = caesar.decode(ciphertext, shift)
        chi2 = chi_squared(plaintext)
        sc = freq_score(plaintext)
        candidates.append({
            "shift":     shift,
            "plaintext": plaintext,
            "score":     round(sc, 6),
            "chi2":      round(chi2, 4),
        })

    # Sort: lowest chi-squared first (= closest to English distribution)
    candidates.sort(key=lambda c: c["chi2"])
    return {
        "best":       candidates[0],
        "all_shifts": candidates,
    }


# ──────────────────────────── Vigenère cracker ──────────────────────────────

def _crack_column(column_text: str) -> tuple[str, int]:
    """Find the best Caesar shift for a single column. Returns (key_letter, shift)."""
    result = crack_caesar(column_text)
    best_shift = result["best"]["shift"]
    # shift for decoding == the Caesar shift applied to that column
    # The key letter is chr(shift + ord('A'))
    key_letter = chr(best_shift + ord('A'))
    return key_letter, best_shift


def crack_vigenere(ciphertext: str, max_key_len: int = 20) -> dict:
    """Crack a Vigenère-encrypted ciphertext using IC + per-column Caesar attack.

    Algorithm:
      1. Estimate key length using the Index of Coincidence (top 5 candidates).
      2. For each candidate key length k:
         a. Split ciphertext into k interleaved columns.
         b. Crack each column independently with crack_caesar.
         c. Assemble the recovered key string.
         d. Decode the full ciphertext with that key.
         e. Score the decoded text.
      3. Return the candidate with the highest overall fitness score.

    Args:
        ciphertext:  Vigenère-encrypted text.
        max_key_len: Maximum key length to try (default 20).

    Returns:
        {
          "best": {
              "key":       str,   # recovered key
              "key_length": int,
              "plaintext": str,
              "score":     float,
          },
          "candidates": [         # all tried key lengths, best-first
              {"key": str, "key_length": int, "plaintext": str, "score": float},
              ...
          ]
        }
    """
    # Step 1 — estimate key lengths, take top 5 candidates
    kl_results = estimate_key_length(ciphertext, max_key_len)[:5]

    letters_only = ''.join(ch.upper() for ch in ciphertext if ch.isalpha())

    candidates = []
    for kl_result in kl_results:
        k = kl_result["key_length"]
        if k < 1 or len(letters_only) < k * 2:
            continue

        # Step 2 — split into k columns, crack each
        columns = split_into_columns(letters_only, k)
        key_letters = []
        for col in columns:
            kl, _ = _crack_column(col)
            key_letters.append(kl)
        recovered_key = ''.join(key_letters)

        # Step 3 — decode with recovered key
        try:
            plaintext = vigenere.decode(ciphertext, recovered_key)
        except Exception:
            continue

        sc = freq_score(plaintext)
        candidates.append({
            "key":        recovered_key,
            "key_length": k,
            "plaintext":  plaintext,
            "score":      round(sc, 6),
        })

    if not candidates:
        return {"best": None, "candidates": []}

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return {
        "best":       candidates[0],
        "candidates": candidates,
    }


# ────────────────────────── Substitution cracker ──────────────────────────────

def _build_key_from_mapping(
    mapping: list[tuple[str, str]],
) -> str:
    """Build a 26-letter substitution key from a list of (cipher_letter, plain_letter) pairs.

    The key is constructed so that ``decode(ciphertext, key)`` maps each
    *cipher_letter* to its paired *plain_letter*.  Any unassigned positions
    are filled with the remaining unused letters in alphabetical order.

    Args:
        mapping: List of (cipher_char, plain_char) pairs, e.g.
                 ``[('K', 'E'), ('X', 'T'), ...]``.

    Returns:
        A 26-character uppercase permutation of the alphabet.
    """
    key_arr: list[str] = [''] * _ALPHA_SIZE
    used_cipher: set[str] = set()
    for cl, pl in mapping:
        pl_idx = ord(pl) - ord('A')
        key_arr[pl_idx] = cl
        used_cipher.add(cl)

    # Fill remaining key positions with unused letters
    unused = sorted(ch for ch in _ALPHA if ch not in used_cipher)
    for i in range(_ALPHA_SIZE):
        if not key_arr[i]:
            key_arr[i] = unused.pop(0)

    return ''.join(key_arr)


def crack_substitution(ciphertext: str, top_n: int = 5) -> dict:
    """Crack a simple substitution cipher using letter-frequency analysis.

    Strategy:
      1. Compute the letter frequencies of the ciphertext.
      2. Sort ciphertext letters by frequency descending.
      3. Map most-frequent → ``E``, 2nd → ``T``, … (standard English order).
      4. Build a candidate substitution key from this mapping.
      5. Generate *top_n* variants by swapping adjacent frequency-rank pairs.
      6. Score each candidate with ``frequency.score()``.

    Args:
        ciphertext: The encoded text (any case; non-alpha preserved).
        top_n:      Number of candidate decryptions to return (default 5).

    Returns:
        {
          "candidates": [
            {"key": str, "plaintext": str, "score": float},
            ...
          ]
        }
        Candidates are sorted best-first by score.  Returns an empty list
        for ciphertext with no alphabetic characters.
    """
    letters_only = ''.join(ch.upper() for ch in ciphertext if ch.isalpha())
    if not letters_only:
        return {"candidates": []}

    # 1. Get ciphertext letters sorted by frequency, descending
    rel_freqs = freq_module.relative(letters_only)
    cipher_order = sorted(rel_freqs.keys(), key=lambda k: rel_freqs[k], reverse=True)

    # 2. Determine how many top positions we can permute
    n_perm = min(top_n + 2, len(cipher_order), _ALPHA_SIZE)

    # 3. Base mapping: most frequent ciphertext letter → 'E', 2nd → 'T', …
    base_mapping = list(zip(
        cipher_order[:n_perm],
        _ENGLISH_FREQ_ORDER[:n_perm],
    ))

    # 4. Generate variants: base + adjacent swaps
    mappings: list[list[tuple[str, str]]] = [list(base_mapping)]
    for i in range(min(top_n - 1, n_perm - 1)):
        variant = list(base_mapping)
        variant[i], variant[i + 1] = variant[i + 1], variant[i]
        mappings.append(variant)

    # 5. Build key → decode → score for each variant
    candidates: list[dict] = []
    for mapping in mappings:
        key = _build_key_from_mapping(mapping)
        plaintext = substitution.decode(ciphertext, key)
        sc = freq_score(plaintext)
        candidates.append({
            "key":        key,
            "plaintext":  plaintext,
            "score":      round(sc, 6),
        })

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return {"candidates": candidates[:top_n]}


# ──────────────────────────── Playfair cracker ────────────────────────────────

# Keywords tried when brute-forcing a Playfair key (ordered roughly by
# likelihood — common/short words first).
_PLAYFAIR_KEYWORDS: list[str] = [
    "KEY", "TEST", "CODE", "CIPHER", "PLAYFAIR",
    "SECRET", "CRYPTO", "ALGORITHM", "ENCRYPT", "DECODE",
    "JULIUS", "CAESAR", "VIGENERE", "HILL", "AFFINE",
    "CLASSIC", "MODERN", "SECURITY", "PRIVACY", "DEFAULT",
    "PRACTICE", "STUDY", "ANALYSIS", "FREQUENCY", "BRUTE",
    "ATTACK", "DEFENSE", "MESSAGE", "LETTER", "DIGRAPH",
]

_ENGLISH_IC_REF: float = 0.0667


def _score_playfair_plaintext(text: str) -> float:
    """Score a candidate Playfair plaintext using IC + frequency analysis.

    Returns a weighted combination (0–1) where higher is more English-like.
    """
    ic_val = index_of_coincidence(text)
    freq_sc = freq_score(text)

    # How close is the IC to the English reference?  1.0 = perfect match.
    ic_similarity = max(0.0, 1.0 - abs(ic_val - _ENGLISH_IC_REF) / _ENGLISH_IC_REF)

    # Weighted: frequency is more reliable than IC for short texts.
    return 0.6 * freq_sc + 0.4 * ic_similarity


def crack_playfair(ciphertext: str, max_key_len: int = 10) -> dict:
    """Crack a Playfair cipher by trying common keywords.

    Playfair is a digraph substitution cipher that resists straightforward
    frequency analysis.  This function implements a best-effort attack:

      1. Decode *ciphertext* with each keyword in a built-in list.
      2. Score every candidate with ``_score_playfair_plaintext()``.
      3. Return candidates sorted best-first.

    Args:
        ciphertext:  Playfair-encoded text (any case; non-alpha stripped).
        max_key_len: Maximum keyword character length to try (default 10).

    Returns:
        {
          "candidates": [
            {"key": str, "plaintext": str, "score": float},
            ...
          ],
          "note": "Playfair cracking is best-effort"
        }
        Returns an empty candidate list for non-alphabetic or odd-length input.
    """
    letters_only = ''.join(ch.upper() for ch in ciphertext if ch.isalpha())
    if not letters_only:
        return {"candidates": [], "note": "Playfair cracking is best-effort"}

    if len(letters_only) % 2 != 0:
        return {"candidates": [], "note": "Playfair ciphertext must have an even number of letters"}

    candidates: list[dict] = []
    for kw in _PLAYFAIR_KEYWORDS:
        if len(kw) > max_key_len:
            continue
        try:
            plaintext = playfair.decode(ciphertext, kw)
            sc = _score_playfair_plaintext(plaintext)
            candidates.append({
                "key":        kw,
                "plaintext":  plaintext,
                "score":      round(sc, 6),
            })
        except Exception:
            continue

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return {
        "candidates": candidates,
        "note":       "Playfair cracking is best-effort",
    }


# ─────────────────────────── Rail Fence cracker ──────────────────────────────


def crack_railfence(ciphertext: str, max_rails: int = 10) -> dict:
    """Crack a Rail Fence cipher by brute-forcing all plausible rail counts.

    Tries *rails* from 2 to *max_rails* inclusive, scores each candidate
    using English frequency analysis, and returns the results sorted by
    score descending.

    Args:
        ciphertext: Rail-Fence-encoded text (any case; non-alpha preserved).
        max_rails:  Maximum number of rails to try (default 10).

    Returns:
        {
          "best":       {"rails": int, "plaintext": str, "score": float},
          "candidates": [
              {"rails": int, "plaintext": str, "score": float},
              ...
          ]
        }
        Candidates are sorted best-first.  Returns empty candidates for
        ciphertext with no alphabetic characters.
    """
    letters_only = ''.join(ch.upper() for ch in ciphertext if ch.isalpha())
    if not letters_only:
        return {"best": None, "candidates": []}

    candidates: list[dict] = []
    for rails in range(2, max_rails + 1):
        try:
            plaintext = rail_fence.decode(ciphertext, rails)
        except Exception:
            continue
        sc = freq_score(plaintext)
        candidates.append({
            "rails":      rails,
            "plaintext":  plaintext,
            "score":      round(sc, 6),
        })

    if not candidates:
        return {"best": None, "candidates": []}

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return {
        "best":       candidates[0],
        "candidates": candidates,
    }


# ──────────────────────────── Beaufort cracker ────────────────────────────────


def _crack_beaufort_column(column_text: str) -> tuple[str, int]:
    """Find the best single-letter Beaufort key for a column.

    Tries all 26 possible key letters, decodes the column with
    ``beaufort.decode()``, and selects the one with the lowest
    chi-squared statistic (most English-like).

    Returns:
        (key_letter, key_value) where key_value is the 0-25 numeric value.
    """
    best_key = 0
    best_chi2 = float('inf')
    for key_val in range(_ALPHA_SIZE):
        key_char = chr(key_val + ord('A'))
        decoded = beaufort.decode(column_text, key_char)
        chi2 = chi_squared(decoded)
        if chi2 < best_chi2:
            best_chi2 = chi2
            best_key = key_val
    return chr(best_key + ord('A')), best_key


def crack_beaufort(ciphertext: str, max_key_len: int = 20) -> dict:
    """Crack a Beaufort-encrypted ciphertext using IC + per-column key search.

    Algorithm (mirrors ``crack_vigenere``):
      1. Estimate key length using the Index of Coincidence (top 5 candidates).
      2. For each candidate key length *k*:
         a. Split ciphertext into *k* interleaved columns.
         b. Crack each column independently with ``_crack_beaufort_column``.
         c. Assemble the recovered key string.
         d. Decode the full ciphertext with that key using ``beaufort.decode()``.
         e. Score the decoded text.
      3. Return the candidate with the highest overall fitness score.

    Args:
        ciphertext:  Beaufort-encrypted text.
        max_key_len: Maximum key length to try (default 20).

    Returns:
        {
          "best":       {"key": str, "key_length": int, "plaintext": str, "score": float},
          "candidates": [
              {"key": str, "key_length": int, "plaintext": str, "score": float},
              ...
          ]
        }
        Returns ``{"best": None, "candidates": []}`` for ciphertext with no
        alphabetic characters.
    """
    kl_results = estimate_key_length(ciphertext, max_key_len)[:5]

    letters_only = ''.join(ch.upper() for ch in ciphertext if ch.isalpha())

    candidates: list[dict] = []
    for kl_result in kl_results:
        k = kl_result["key_length"]
        if k < 1 or len(letters_only) < k * 2:
            continue

        columns = split_into_columns(letters_only, k)
        key_letters: list[str] = []
        for col in columns:
            kl, _ = _crack_beaufort_column(col)
            key_letters.append(kl)
        recovered_key = ''.join(key_letters)

        try:
            plaintext = beaufort.decode(ciphertext, recovered_key)
        except Exception:
            continue

        sc = freq_score(plaintext)
        candidates.append({
            "key":        recovered_key,
            "key_length": k,
            "plaintext":  plaintext,
            "score":      round(sc, 6),
        })

    if not candidates:
        return {"best": None, "candidates": []}

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return {
        "best":       candidates[0],
        "candidates": candidates,
    }


# ──────────────────────────── Affine cracker ──────────────────────────────────


def crack_affine(ciphertext: str) -> dict:
    """Brute-force an Affine cipher by trying all 312 valid (a, b) pairs.

    An Affine cipher has the form ``E(x) = (a·x + b) mod 26`` where
    ``gcd(a, 26) = 1`` and ``b ∈ [0, 25]``.  There are exactly 12 values of
    *a* coprime with 26 and 26 values of *b*, yielding 312 valid key pairs.

    Each pair is decoded with ``affine.decode()`` and scored with English
    frequency analysis.  The top 10 candidates are returned.

    Args:
        ciphertext: Affine-encrypted text (any case; non-alpha preserved).

    Returns:
        {
          "best":       {"a": int, "b": int, "plaintext": str, "score": float},
          "candidates": [
              {"a": int, "b": int, "plaintext": str, "score": float},
              ...
          ],
          "total_tried": int,
        }
        Candidates are sorted best-first (max 10).  Returns empty candidates
        and total_tried = 0 for ciphertext with no alphabetic characters.
    """
    letters_only = ''.join(ch.upper() for ch in ciphertext if ch.isalpha())
    if not letters_only:
        return {"best": None, "candidates": [], "total_tried": 0}

    candidates: list[dict] = []
    total_tried = 0
    for a in range(_ALPHA_SIZE):
        if math.gcd(a, _ALPHA_SIZE) != 1:
            continue
        for b in range(_ALPHA_SIZE):
            total_tried += 1
            try:
                plaintext = affine.decode(ciphertext, a, b)
            except Exception:
                continue
            sc = freq_score(plaintext)
            candidates.append({
                "a":          a,
                "b":          b,
                "plaintext":  plaintext,
                "score":      round(sc, 6),
            })

    if not candidates:
        return {"best": None, "candidates": [], "total_tried": total_tried}

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return {
        "best":         candidates[0],
        "candidates":   candidates[:10],
        "total_tried":  total_tried,
    }
