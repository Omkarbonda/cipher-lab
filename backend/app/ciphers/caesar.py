"""
Caesar cipher — classical shift cipher.

Only alphabetic characters are shifted; punctuation, digits, and spaces are
preserved unchanged.  Case is preserved: shifting 'a' by 3 gives 'd'.

Key: an integer in the range [0, 25].  Values outside this range are reduced
modulo 26 so the function is always well-defined.
"""

_ALPHA_SIZE = 26


def _shift_char(ch: str, shift: int) -> str:
    """Shift a single alphabetic character by *shift* positions."""
    base = ord('A') if ch.isupper() else ord('a')
    return chr((ord(ch) - base + shift) % _ALPHA_SIZE + base)


def encode(plaintext: str, shift: int) -> str:
    """Return the Caesar-cipher encoding of *plaintext* with the given *shift*.

    Args:
        plaintext: Input text.  Non-alpha characters pass through unchanged.
        shift: Number of positions to shift (any integer; reduced mod 26).

    Returns:
        Ciphertext string of the same length as *plaintext*.

    Examples:
        >>> encode("Hello, World!", 3)
        'Khoor, Zruog!'
        >>> encode("abc", 0)
        'abc'
        >>> encode("xyz", 3)
        'abc'
    """
    shift = shift % _ALPHA_SIZE
    return ''.join(_shift_char(ch, shift) if ch.isalpha() else ch
                   for ch in plaintext)


def decode(ciphertext: str, shift: int) -> str:
    """Return the Caesar-cipher decoding of *ciphertext* with the given *shift*.

    Args:
        ciphertext: Encoded text.
        shift: The shift that was used during encoding.

    Returns:
        Plaintext string.

    Examples:
        >>> decode("Khoor, Zruog!", 3)
        'Hello, World!'
    """
    return encode(ciphertext, -shift)
