"""
Vigenère cipher — polyalphabetic substitution using a repeating keyword.

Each letter of the plaintext is shifted by the corresponding letter of the
keyword (A=0, B=1, … Z=25).  Non-alphabetic characters in the plaintext are
passed through unchanged and do *not* advance the keyword index — i.e. the
keyword only "steps" on alphabetic characters.

Key: any non-empty string of ASCII letters (case-insensitive).
"""

_ALPHA_SIZE = 26


def _key_stream(key: str):
    """Infinite generator that cycles through the alphabetic shifts of *key*."""
    key = key.upper()
    if not key or not key.isalpha():
        raise ValueError("Vigenère key must be a non-empty alphabetic string.")
    i = 0
    while True:
        yield ord(key[i % len(key)]) - ord('A')
        i += 1


def encode(plaintext: str, key: str) -> str:
    """Return the Vigenère-cipher encoding of *plaintext* using *key*.

    Args:
        plaintext: Input text; non-alpha characters are preserved unchanged.
        key: Alphabetic keyword (case-insensitive).

    Returns:
        Ciphertext string of the same length as *plaintext*.

    Examples:
        >>> encode("ATTACKATDAWN", "LEMON")
        'LXFOPVEFRNHR'
        >>> encode("Hello, World!", "key")
        'Rijvs, Ambpb!'
    """
    gen = _key_stream(key)
    result = []
    for ch in plaintext:
        if ch.isalpha():
            shift = next(gen)
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % _ALPHA_SIZE + base))
        else:
            result.append(ch)
    return ''.join(result)


def decode(ciphertext: str, key: str) -> str:
    """Return the Vigenère-cipher decoding of *ciphertext* using *key*.

    Args:
        ciphertext: Encoded text.
        key: Alphabetic keyword used during encoding.

    Returns:
        Plaintext string.

    Examples:
        >>> decode("LXFOPVEFRNHR", "LEMON")
        'ATTACKATDAWN'
        >>> decode("Rijvs, Ambpb!", "key")
        'Hello, World!'
    """
    gen = _key_stream(key)
    result = []
    for ch in ciphertext:
        if ch.isalpha():
            shift = next(gen)
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base - shift) % _ALPHA_SIZE + base))
        else:
            result.append(ch)
    return ''.join(result)
