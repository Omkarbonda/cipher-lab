"""
Playfair cipher — digraph substitution cipher using a 5×5 key square.

The key square is built from a keyword: fill the grid left-to-right,
top-to-bottom with unique letters from the keyword (uppercased) then the
remaining letters of the alphabet.  I and J are merged into a single cell
(J is treated as I).

Encoding rules (pairs of letters):
  1. Same row   → each letter replaced by the one to its right (wrapping).
  2. Same column→ each letter replaced by the one below (wrapping).
  3. Rectangle  → each letter replaced by the letter in the same row but
                  the other letter's column.

Pre-processing:
  - Strip non-alpha, uppercase, replace J → I.
  - Insert an 'X' between repeated letters in a pair.
  - If the final digraph count is odd, append 'X'.

Post-processing (decode):
  - Remove trailing 'X' padding if present.
  - Reverse-X removal between repeated pairs is left to the caller (standard
    Playfair ambiguity — we faithfully round-trip on the processed form).

Output is always uppercase with no spaces.
"""

_SIZE = 5


def _build_square(keyword: str) -> list[list[str]]:
    """Build the 5×5 Playfair square from *keyword*."""
    keyword = keyword.upper().replace('J', 'I')
    seen: set[str] = set()
    order: list[str] = []
    for ch in keyword + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch.isalpha() and ch not in seen:
            seen.add(ch)
            order.append(ch)
    return [order[i * _SIZE:(i + 1) * _SIZE] for i in range(_SIZE)]


def _make_index(square: list[list[str]]) -> dict[str, tuple[int, int]]:
    return {square[r][c]: (r, c) for r in range(_SIZE) for c in range(_SIZE)}


def _prepare(text: str) -> list[str]:
    """Clean text and split into digraphs, inserting padding where needed."""
    text = text.upper().replace('J', 'I')
    letters = [ch for ch in text if ch.isalpha()]
    digraphs: list[str] = []
    i = 0
    while i < len(letters):
        a = letters[i]
        if i + 1 < len(letters):
            b = letters[i + 1]
            if a == b:
                digraphs.append(a)
                digraphs.append('X')
                i += 1
            else:
                digraphs.append(a)
                digraphs.append(b)
                i += 2
        else:
            digraphs.append(a)
            digraphs.append('X')
            i += 1
    return digraphs


def _encipher_pair(a: str, b: str, square: list[list[str]],
                   idx: dict[str, tuple[int, int]], direction: int) -> tuple[str, str]:
    """Encode or decode a single digraph.  direction=+1 for encode, -1 for decode."""
    ra, ca = idx[a]
    rb, cb = idx[b]
    if ra == rb:  # same row
        return (square[ra][(ca + direction) % _SIZE],
                square[rb][(cb + direction) % _SIZE])
    elif ca == cb:  # same column
        return (square[(ra + direction) % _SIZE][ca],
                square[(rb + direction) % _SIZE][cb])
    else:  # rectangle
        return square[ra][cb], square[rb][ca]


def encode(plaintext: str, keyword: str) -> str:
    """Return the Playfair encoding of *plaintext* using *keyword*.

    Args:
        plaintext: Input text; non-alpha chars are stripped for processing.
        keyword: Word used to build the Playfair key square.

    Returns:
        Uppercase ciphertext (no spaces).

    Examples:
        >>> encode("HIDE THE GOLD IN THE TREE STUMP", "PLAYFAIR EXAMPLE")
        'BMODZBXDNABEKUDMUIXMMOUVIF'
    """
    square = _build_square(keyword)
    idx = _make_index(square)
    digraphs = _prepare(plaintext)
    result = []
    for i in range(0, len(digraphs), 2):
        ca, cb = _encipher_pair(digraphs[i], digraphs[i + 1], square, idx, +1)
        result.append(ca)
        result.append(cb)
    return ''.join(result)


def decode(ciphertext: str, keyword: str) -> str:
    """Return the Playfair decoding of *ciphertext* using *keyword*.

    Args:
        ciphertext: Encoded text (should be uppercase, even length, no spaces).
        keyword: Word used to build the Playfair key square.

    Returns:
        Decoded uppercase string (may contain X padding — inherent to Playfair).

    Examples:
        >>> decode("BMODZBXDNABEKUDMUIXMMOUVIF", "PLAYFAIR EXAMPLE")
        'HIDETHEGOLDINTHETREXESTUMP'
    """
    square = _build_square(keyword)
    idx = _make_index(square)
    ciphertext = ciphertext.upper().replace('J', 'I')
    letters = [ch for ch in ciphertext if ch.isalpha()]
    if len(letters) % 2 != 0:
        raise ValueError("Playfair ciphertext must have an even number of letters.")
    result = []
    for i in range(0, len(letters), 2):
        pa, pb = _encipher_pair(letters[i], letters[i + 1], square, idx, -1)
        result.append(pa)
        result.append(pb)
    return ''.join(result)
