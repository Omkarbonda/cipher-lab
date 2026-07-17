"""
Columnar Transposition cipher — transposition using a keyword.

The plaintext (with non-alphabetic characters removed) is written row-wise
into a grid whose number of columns equals the length of the key.  Columns
are then read out in the alphabetical order of the key letters to produce
the ciphertext.

Decryption reverses the process: the ciphertext is written into columns in
key order, then read row-wise.

Key: a non-empty string of ASCII letters (case-insensitive).
"""

_ALPHA_SIZE = 26


def _column_order(key: str) -> list[int]:
    """Return the column-reading order based on the sorted key."""
    # Sort column indices by the character at that position, using index as
    # tiebreaker so that equal key characters preserve their original order.
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def encode(plaintext: str, key: str) -> str:
    """Return the Columnar Transposition encoding of *plaintext* using *key*.

    Non-alphabetic characters in the plaintext are stripped before encoding.

    Args:
        plaintext: Input text.  Non-alpha characters are stripped.
        key: Keyword determining column order (case-insensitive, alphabetic).

    Returns:
        Ciphertext string containing only alphabetic characters.

    Raises:
        ValueError: If *key* is empty or contains non-alpha characters.

    Examples:
        >>> encode("HELLO", "CBA")
        'LEOHL'
        >>> encode("HELLO", "ABC")
        'HLEOL'
    """
    if not key or not key.isalpha():
        raise ValueError(
            "Columnar key must be a non-empty alphabetic string."
        )
    key = key.upper()

    letters = [ch for ch in plaintext if ch.isalpha()]
    if not letters:
        return ""

    num_cols = len(key)
    num_rows = (len(letters) + num_cols - 1) // num_cols  # ceil division
    num_full = len(letters) % num_cols
    if num_full == 0:
        num_full = num_cols  # all columns have num_rows items

    # Build grid: first num_full columns have num_rows rows,
    # remaining columns have num_rows - 1 rows.
    col_sizes = [num_rows if i < num_full else num_rows - 1 for i in range(num_cols)]

    # Write letters row-wise
    grid: list[list[str]] = [[''] * size for size in col_sizes]
    idx = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if row < len(grid[col]):  # column has this row
                grid[col][row] = letters[idx]
                idx += 1

    # Read columns in key order
    order = _column_order(key)
    result: list[str] = []
    for col_idx in order:
        result.extend(grid[col_idx])

    return ''.join(result)


def decode(ciphertext: str, key: str) -> str:
    """Return the Columnar Transposition decoding of *ciphertext* using *key*.

    Non-alphabetic characters in the ciphertext are stripped before decoding,
    then re-inserted at the same positions in the output.

    Args:
        ciphertext: Encoded text.
        key: Keyword used during encoding (case-insensitive, alphabetic).

    Returns:
        Plaintext string.

    Raises:
        ValueError: If *key* is empty or contains non-alpha characters.

    Examples:
        >>> decode("LEOHL", "CBA")
        'HELLO'
        >>> decode("HLEOL", "ABC")
        'HELLO'
    """
    if not key or not key.isalpha():
        raise ValueError(
            "Columnar key must be a non-empty alphabetic string."
        )
    key = key.upper()

    # Strip non-alpha from ciphertext, remembering positions
    non_alpha_positions = [(i, ch) for i, ch in enumerate(ciphertext) if not ch.isalpha()]
    letters = [ch for ch in ciphertext if ch.isalpha()]
    if not letters:
        return ""

    num_cols = len(key)
    n = len(letters)
    num_rows = (n + num_cols - 1) // num_cols
    num_full = n % num_cols
    if num_full == 0:
        num_full = num_cols  # all columns have num_rows items

    col_sizes = [num_rows if i < num_full else num_rows - 1 for i in range(num_cols)]

    # Determine column order and how many chars each physical column gets
    order = _column_order(key)

    # Slice ciphertext letters into columns based on their sorted-order sizes
    sorted_col_indices = order
    col_data: dict[int, list[str]] = {}
    idx = 0
    for col_idx in sorted_col_indices:
        size = col_sizes[col_idx]
        col_data[col_idx] = letters[idx: idx + size]
        idx += size

    # Read row-wise
    decoded_alpha: list[str] = []
    for row in range(num_rows):
        for col in range(num_cols):
            if row < len(col_data[col]):
                decoded_alpha.append(col_data[col][row])

    # Re-insert non-alpha characters at their original positions
    result = list(''.join(decoded_alpha))
    for pos, ch in non_alpha_positions:
        result.insert(pos, ch)

    return ''.join(result)
