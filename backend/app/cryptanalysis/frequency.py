"""
Letter frequency analysis for cryptanalysis.

Provides:
  - ENGLISH_FREQ: reference relative frequencies for A-Z in standard English text
  - count(text)         : raw letter counts dict
  - relative(text)      : relative (0-1) frequencies dict
  - chi_squared(text)   : chi-squared goodness-of-fit score against English
                          (lower = more English-like)
  - score(text)         : 0-1 fitness score (higher = more English-like),
                          convenient inverse of chi-squared for ranking
  - top_letters(text, n): list of (letter, relative_freq) sorted by frequency

Chi-squared is the standard metric for measuring how well a frequency
distribution fits a reference distribution.  It is used by the brute-force
Caesar cracker to rank candidate decryptions without human inspection.
"""

from __future__ import annotations
from collections import Counter
import string

# ---------------------------------------------------------------------------
# Reference English letter frequencies (relative, sum ≈ 1.0)
# Source: Lewand (2000), widely used in cryptanalysis literature.
# ---------------------------------------------------------------------------
ENGLISH_FREQ: dict[str, float] = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253,
    'E': 0.12702, 'F': 0.02228, 'G': 0.02015, 'H': 0.06094,
    'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
    'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929,
    'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
    'Y': 0.01974, 'Z': 0.00074,
}

_LETTERS = string.ascii_uppercase


def count(text: str) -> dict[str, int]:
    """Return raw counts of each A-Z letter in *text* (case-insensitive).

    Non-alphabetic characters are ignored.

    Args:
        text: Input string of any length.

    Returns:
        Dict mapping each uppercase letter to its count (0 if absent).

    Examples:
        >>> count("Hello")
        {'A': 0, 'B': 0, ..., 'E': 1, ..., 'H': 1, ..., 'L': 2, ..., 'O': 1, ...}
    """
    upper = text.upper()
    c = Counter(ch for ch in upper if ch.isalpha())
    return {letter: c.get(letter, 0) for letter in _LETTERS}


def relative(text: str) -> dict[str, float]:
    """Return relative (0–1) frequencies for each A-Z letter in *text*.

    Args:
        text: Input string; non-alpha chars are ignored.

    Returns:
        Dict mapping uppercase letters to their relative frequencies.
        Returns all-zeros if *text* has no alphabetic characters.
    """
    counts = count(text)
    total = sum(counts.values())
    if total == 0:
        return {letter: 0.0 for letter in _LETTERS}
    return {letter: counts[letter] / total for letter in _LETTERS}


def chi_squared(text: str) -> float:
    """Compute the chi-squared statistic of *text* against English frequencies.

    A lower score means the letter distribution is closer to English.
    This is the primary scoring metric for ranking candidate decryptions.

    Chi-squared formula (per letter):
        Σ  (observed_count - expected_count)² / expected_count

    Args:
        text: Input string; only alpha characters count.

    Returns:
        Float chi-squared value.  Returns float('inf') for empty/non-alpha text.
    """
    counts = count(text)
    total = sum(counts.values())
    if total == 0:
        return float('inf')

    chi2 = 0.0
    for letter in _LETTERS:
        expected = ENGLISH_FREQ[letter] * total
        observed = counts[letter]
        chi2 += (observed - expected) ** 2 / expected
    return chi2


def score(text: str) -> float:
    """Return a 0–1 English-fitness score (higher = more English-like).

    Computed as  1 / (1 + chi_squared(text))  so it is bounded and monotone.

    Args:
        text: Candidate plaintext string.

    Returns:
        Float in (0, 1].  Returns 0.0 for empty/non-alpha input.
    """
    chi2 = chi_squared(text)
    if chi2 == float('inf'):
        return 0.0
    return 1.0 / (1.0 + chi2)


def top_letters(text: str, n: int = 5) -> list[tuple[str, float]]:
    """Return the *n* most-frequent letters in *text* with their relative frequencies.

    Args:
        text: Input string.
        n:    Number of top letters to return (default 5).

    Returns:
        List of (letter, relative_freq) tuples, sorted descending by frequency.
    """
    rel = relative(text)
    return sorted(rel.items(), key=lambda kv: kv[1], reverse=True)[:n]
