"""
Beaufort cipher — reciprocal polyalphabetic substitution.

The Beaufort cipher is the reciprocal of the Vigenère cipher.  Encryption
and decryption are the same operation: E(x) = (K - x) mod 26, D(y) = (K - y)
mod 26, where K is the numeric value (0-25) of the keyword letter and x/y
are the numeric values of the plaintext/ciphertext letter.

Only alphabetic characters are enciphered.  Non-alphabetic characters are
passed through unchanged and do *not* advance the keyword position.

Key: any non-empty string of ASCII letters (case-insensitive).
"""

_ALPHA_SIZE = 26


def _beaufort_transform(text: str, key: str) -> str:
    """Apply the Beaufort transform (used for both encode and decode)."""
    key = key.upper()
    if not key or not key.isalpha():
        raise ValueError("Beaufort key must be a non-empty alphabetic string.")

    result: list[str] = []
    key_idx = 0
    for ch in text:
        if ch.isalpha():
            k = ord(key[key_idx % len(key)]) - ord('A')
            base = ord('A') if ch.isupper() else ord('a')
            p = ord(ch) - base
            result.append(chr((k - p) % _ALPHA_SIZE + base))
            key_idx += 1
        else:
            result.append(ch)
    return ''.join(result)


def encode(plaintext: str, key: str) -> str:
    """Return the Beaufort cipher encoding of *plaintext* using *key*.

    Since Beaufort is reciprocal, *encode* and *decode* are identical.

    Args:
        plaintext: Input text.  Non-alpha characters pass through unchanged.
        key: Alphabetic keyword (case-insensitive).

    Returns:
        Ciphertext string of the same length as *plaintext*.

    Raises:
        ValueError: If *key* is empty or contains non-alpha characters.

    Examples:
        >>> encode("HELLO", "D")
        'WZSSP'
        >>> encode("Hello, World!", "B")
        'Uxqqn, Fnkqy!'
    """
    return _beaufort_transform(plaintext, key)


def decode(ciphertext: str, key: str) -> str:
    """Return the Beaufort cipher decoding of *ciphertext* using *key*.

    Since Beaufort is reciprocal, *decode* is identical to *encode*.

    Args:
        ciphertext: Encoded text.
        key: Alphabetic keyword used during encoding.

    Returns:
        Plaintext string.

    Raises:
        ValueError: If *key* is empty or contains non-alpha characters.

    Examples:
        >>> decode("WZSSP", "D")
        'HELLO'
        >>> decode("Uxqqn, Fnkqy!", "B")
        'Hello, World!'
    """
    return _beaufort_transform(ciphertext, key)
