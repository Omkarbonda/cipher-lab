"""
Affine cipher — monoalphabetic substitution using linear transformation.

Each letter is transformed as E(x) = (a * x + b) mod 26, where x is the
numeric value (0-25) of the letter.  Decryption uses the modular inverse
of a: D(y) = a⁻¹ * (y - b) mod 26.

Only alphabetic characters are enciphered; non-alphabetic characters pass
through unchanged.  Case is preserved.

Requirements:
    * gcd(a, 26) = 1  (so that a has a modular inverse modulo 26)
    * 0 <= b <= 25
"""

import math

_ALPHA_SIZE = 26


def encode(plaintext: str, a: int, b: int) -> str:
    """Return the Affine cipher encoding of *plaintext* with parameters (a, b).

    Args:
        plaintext: Input text.  Non-alpha characters pass through unchanged.
        a: Multiplier.  Must be coprime with 26.
        b: Shift.  Must be in the range [0, 25].

    Returns:
        Ciphertext string of the same length as *plaintext*.

    Raises:
        ValueError: If gcd(a, 26) != 1 or b is outside [0, 25].

    Examples:
        >>> encode("HELLO", 5, 8)
        'RCLLA'
        >>> encode("Hello, World!", 5, 8)
        'Rclla, Oaplx!'
    """
    if math.gcd(a, _ALPHA_SIZE) != 1:
        raise ValueError(
            f"a={a} is not invertible modulo {_ALPHA_SIZE}. "
            "gcd(a, 26) must be 1."
        )
    if not 0 <= b < _ALPHA_SIZE:
        raise ValueError(f"b must be in [0, 25], got {b}.")

    result: list[str] = []
    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            x = ord(ch) - base
            result.append(chr((a * x + b) % _ALPHA_SIZE + base))
        else:
            result.append(ch)
    return ''.join(result)


def decode(ciphertext: str, a: int, b: int) -> str:
    """Return the Affine cipher decoding of *ciphertext* with parameters (a, b).

    Args:
        ciphertext: Encoded text.
        a: Multiplier used during encoding (must be coprime with 26).
        b: Shift used during encoding (must be in [0, 25]).

    Returns:
        Plaintext string.

    Raises:
        ValueError: If gcd(a, 26) != 1 or b is outside [0, 25].

    Examples:
        >>> decode("RCLLA", 5, 8)
        'HELLO'
        >>> decode("Rclla, Oaplx!", 5, 8)
        'Hello, World!'
    """
    if math.gcd(a, _ALPHA_SIZE) != 1:
        raise ValueError(
            f"a={a} is not invertible modulo {_ALPHA_SIZE}. "
            "gcd(a, 26) must be 1."
        )
    if not 0 <= b < _ALPHA_SIZE:
        raise ValueError(f"b must be in [0, 25], got {b}.")

    a_inv = pow(a, -1, _ALPHA_SIZE)
    result: list[str] = []
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            y = ord(ch) - base
            result.append(chr((a_inv * (y - b)) % _ALPHA_SIZE + base))
        else:
            result.append(ch)
    return ''.join(result)
