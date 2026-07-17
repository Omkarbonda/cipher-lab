"""
Index of Coincidence (IC) — tool for breaking polyalphabetic ciphers.

The Index of Coincidence measures the probability that two randomly chosen
letters from a text are the same.

  IC = Σ  nᵢ(nᵢ - 1) / (N(N-1))

where nᵢ is the count of the i-th letter and N is the total letter count.

Reference values:
  - English text:   IC ≈ 0.0667  (non-uniform — letters not equally likely)
  - Random text:    IC ≈ 0.0385  (uniform distribution over 26 letters = 1/26)
  - Vigenère text:  IC < 0.0667, closer to 0.0385 as key length grows

Key insight for Vigenère cracking:
  If we split ciphertext into every-k-th-character columns (period = k),
  each column is a simple Caesar cipher.  We look for the k where each
  column's IC is close to 0.0667 (English-like).  That k is our key length.

This module provides:
  - index_of_coincidence(text)   : compute IC for a string
  - estimate_key_length(ciphertext, max_key_len)
      : return ranked list of likely key lengths (best first)
  - split_into_columns(text, period)
      : helper — split text into *period* interleaved columns
"""

from __future__ import annotations
from collections import Counter
import string

_ENGLISH_IC = 0.0667
_RANDOM_IC  = 0.0385


def index_of_coincidence(text: str) -> float:
    """Compute the Index of Coincidence for *text*.

    Args:
        text: Input string; non-alpha characters are ignored.

    Returns:
        IC value as a float, or 0.0 if text has fewer than 2 letters.

    Examples:
        >>> round(index_of_coincidence("AAAA"), 4)
        1.0
        >>> index_of_coincidence("A")
        0.0
    """
    letters = [ch.upper() for ch in text if ch.isalpha()]
    n = len(letters)
    if n < 2:
        return 0.0
    counts = Counter(letters)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator


def split_into_columns(text: str, period: int) -> list[str]:
    """Split *text* (letters only) into *period* interleaved columns.

    Column i contains characters at positions i, i+period, i+2*period, …

    This is the key step in the IC-based Vigenère attack: each column
    is encrypted by a single Caesar shift (one key character).

    Args:
        text:   Input string; non-alpha characters are stripped.
        period: Number of columns (= guessed key length).

    Returns:
        List of *period* strings, one per column.

    Examples:
        >>> split_into_columns("ABCDEF", 3)
        ['AD', 'BE', 'CF']
    """
    letters = [ch.upper() for ch in text if ch.isalpha()]
    return [''.join(letters[i::period]) for i in range(period)]


def _average_ic(text: str, period: int) -> float:
    """Return the mean IC of all *period* columns for *text*."""
    columns = split_into_columns(text, period)
    ics = [index_of_coincidence(col) for col in columns if len(col) >= 2]
    if not ics:
        return 0.0
    return sum(ics) / len(ics)


def estimate_key_length(
    ciphertext: str,
    max_key_len: int = 20,
) -> list[dict]:
    """Estimate the Vigenère key length using the Index of Coincidence.

    For each candidate period k from 1 to *max_key_len*, we split the
    ciphertext into k columns and compute the average IC.  The k whose
    average IC is closest to the English IC (≈ 0.0667) is the best guess.

    Args:
        ciphertext:  Vigenère-encrypted text.
        max_key_len: Maximum key length to test (default 20).

    Returns:
        List of dicts sorted by closeness to English IC (best first):
          [
            {"key_length": int, "average_ic": float, "delta": float},
            ...
          ]
        where *delta* = |average_ic - ENGLISH_IC| (lower = better fit).
    """
    results = []
    for k in range(1, max_key_len + 1):
        avg_ic = _average_ic(ciphertext, k)
        delta = abs(avg_ic - _ENGLISH_IC)
        results.append({
            "key_length": k,
            "average_ic": round(avg_ic, 6),
            "delta": round(delta, 6),
        })
    return sorted(results, key=lambda r: r["delta"])
