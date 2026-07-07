"""
Simple Substitution cipher — maps each letter to a unique replacement letter.

The key is a 26-character permutation of the alphabet that defines the
substitution table.  For example, key[0] is the cipher letter for 'A',
key[1] for 'B', etc.  Case is preserved; non-alphabetic characters pass
through unchanged.

Key validation: the key must contain exactly 26 distinct ASCII letters.
"""

_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_ALPHA_SIZE = 26


def _validate_key(key: str) -> str:
    """Return the upper-cased key after validating it is a legal substitution."""
    key = key.upper()
    if len(key) != _ALPHA_SIZE or not key.isalpha() or len(set(key)) != _ALPHA_SIZE:
        raise ValueError(
            "Substitution key must be exactly 26 distinct alphabetic characters."
        )
    return key


def encode(plaintext: str, key: str) -> str:
    """Return the substitution-cipher encoding of *plaintext* using *key*.

    Args:
        plaintext: Input text; non-alpha characters are preserved unchanged.
        key: A 26-character permutation of the alphabet (case-insensitive).

    Returns:
        Ciphertext string of the same length as *plaintext*.

    Examples:
        >>> encode("Hello", "ZYXWVUTSRQPONMLKJIHGFEDCBA")
        'Svool'
        >>> encode("ABC", "ZYXWVUTSRQPONMLKJIHGFEDCBA")
        'ZYX'
    """
    key = _validate_key(key)
    table = str.maketrans(_ALPHA, key)
    # Build a lowercase version of the table for lower-case input
    table.update(str.maketrans(_ALPHA.lower(), key.lower()))
    return plaintext.translate(table)


def decode(ciphertext: str, key: str) -> str:
    """Return the substitution-cipher decoding of *ciphertext* using *key*.

    Args:
        ciphertext: Encoded text.
        key: The 26-character permutation used during encoding.

    Returns:
        Plaintext string.

    Examples:
        >>> decode("Svool", "ZYXWVUTSRQPONMLKJIHGFEDCBA")
        'Hello'
    """
    key = _validate_key(key)
    # Invert the mapping: cipher letter -> plain letter
    inverse_key = [''] * _ALPHA_SIZE
    for i, ch in enumerate(key):
        inverse_key[ord(ch) - ord('A')] = _ALPHA[i]
    inverse_str = ''.join(inverse_key)
    table = str.maketrans(key, _ALPHA)
    table.update(str.maketrans(key.lower(), _ALPHA.lower()))
    return ciphertext.translate(table)
