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
from app.cryptanalysis.frequency import chi_squared, score as freq_score
from app.cryptanalysis.index_of_coincidence import (
    estimate_key_length,
    split_into_columns,
)
from app.ciphers import caesar, vigenere

_ALPHA_SIZE = 26


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
