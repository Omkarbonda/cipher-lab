"""
Rail Fence cipher — classical transposition cipher.

The plaintext is written in a zigzag pattern across a specified number of
rails (rows), then read off row by row.  Only alphabetic characters are
transposed; non-alphabetic characters are preserved in their original
positions.

The cipher is defined for rails >= 2.  rails = 1 is treated as the identity
transformation.
"""

_ALPHA_SIZE = 26


def _rail_pattern(n: int, rails: int) -> list[int]:
    """Return the rail assignment (0-indexed) for each of *n* characters.

    The pattern cycles through 0, 1, …, rails-1, rails-2, …, 1, 0, …
    """
    cycle = 2 * (rails - 1)
    pattern: list[int] = []
    for i in range(n):
        pos = i % cycle
        if pos < rails:
            pattern.append(pos)
        else:
            pattern.append(cycle - pos)
    return pattern


def encode(plaintext: str, rails: int) -> str:
    """Return the Rail Fence encoding of *plaintext* using *rails* rows.

    Args:
        plaintext: Input text.  Non-alpha characters pass through unchanged.
        rails: Number of rails (rows).  Must be >= 2 (1 is identity).

    Returns:
        Ciphertext string of the same length as *plaintext*.

    Raises:
        ValueError: If *rails* is less than 2 (and not 1).

    Examples:
        >>> encode("HELLO", 3)
        'HOELL'
        >>> encode("HELLO, WORLD!", 3)
        'HOLEL, WRDLO!'
    """
    if rails < 2:
        if rails == 1:
            return plaintext
        raise ValueError("rails must be >= 2")

    alpha_chars = [ch for ch in plaintext if ch.isalpha()]
    if not alpha_chars:
        return plaintext

    pattern = _rail_pattern(len(alpha_chars), rails)
    rails_content: list[list[str]] = [[] for _ in range(rails)]
    for ch, r in zip(alpha_chars, pattern):
        rails_content[r].append(ch)

    encoded_alpha = list(''.join(''.join(r) for r in rails_content))

    # Reconstruct output — replace alpha chars with permuted versions,
    # non-alpha chars stay in their original positions.
    result = list(plaintext)
    alpha_iter = iter(encoded_alpha)
    for i, ch in enumerate(plaintext):
        if ch.isalpha():
            result[i] = next(alpha_iter)
    return ''.join(result)


def decode(ciphertext: str, rails: int) -> str:
    """Return the Rail Fence decoding of *ciphertext* using *rails* rows.

    Non-alphabetic characters are stripped before decoding and re-inserted
    at the positions they occupied in *ciphertext*.

    Args:
        ciphertext: Encoded text.
        rails: Number of rails used during encoding.

    Returns:
        Plaintext string.

    Raises:
        ValueError: If *rails* is less than 2 (and not 1).

    Examples:
        >>> decode("HOELL", 3)
        'HELLO'
        >>> decode("HOLEL, WRDLO!", 3)
        'HELLO, WORLD!'
    """
    if rails < 2:
        if rails == 1:
            return ciphertext
        raise ValueError("rails must be >= 2")

    alpha_chars = [ch for ch in ciphertext if ch.isalpha()]
    if not alpha_chars:
        return ciphertext

    n = len(alpha_chars)
    pattern = _rail_pattern(n, rails)

    # Count characters per rail
    rail_counts = [0] * rails
    for r in pattern:
        rail_counts[r] += 1

    # Split alpha_chars into rails (they were concatenated row by row)
    rails_content: list[list[str]] = [[] for _ in range(rails)]
    idx = 0
    for rail in range(rails):
        rails_content[rail] = alpha_chars[idx: idx + rail_counts[rail]]
        idx += rail_counts[rail]

    # Read in zigzag order
    rail_pointers = [0] * rails
    decoded_alpha: list[str] = []
    for r in pattern:
        decoded_alpha.append(rails_content[r][rail_pointers[r]])
        rail_pointers[r] += 1

    # Re-insert non-alpha characters at their original positions
    result = list(ciphertext)
    alpha_iter = iter(decoded_alpha)
    for i, ch in enumerate(ciphertext):
        if ch.isalpha():
            result[i] = next(alpha_iter)
    return ''.join(result)
