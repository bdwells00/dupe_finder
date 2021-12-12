"""bytenote v0.0.3"""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def byte_notation(size: int, acc=2, ntn=0):
    """Decimal Notation: take an integer, converts it to a string with the
    requested decimal accuracy, and appends either single (default), double,
    or full word character notation.

    - Args:
        - size (int): the size to convert
        - acc (int, optional): number of decimal places to keep. Defaults to 2.
        - ntn (int, optional): notation name length. Defaults to 0.

    - Returns:
        - [tuple]: 0 = original size int unmodified; 1 = string for printing
    """
    size_dict = {
        1: ['B', 'B', 'bytes'],
        1000: ['k', 'kB', 'kilobytes'],
        1000000: ['M', 'MB', 'megabytes'],
        1000000000: ['G', 'GB', 'gigabytes'],
        1000000000000: ['T', 'TB', 'terabytes']
    }
    return_size_str = ''
    for key, value in size_dict.items():
        if (size / key) < 1000:
            return_size_str = f'{size / key:,.{acc}f} {value[ntn]}'
            return size, return_size_str
