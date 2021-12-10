"""bytenote v0.0.2"""


from math import ceil, floor


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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def time_notation(time_var: float, ntn='short'):
    """Convert seconds and fractions of a second into human friendly notation.

    - Args:
        - time_var (float): the seconds to convert
        - ntn (str, optional): 'short' returns 00:00:00, while 'long' returns
                               0 hours, 0 minutes, and 0 seconds.
                               Defaults to 'short'.

    - Returns:
        - [type]: [description]
    """
    s = time_var % 60 if time_var > 1 else 1
    m, h, d, y = 0, 0, 0, 0
    if time_var < 3600:
        m = floor(time_var / 60)
    elif time_var < 86400:
        h = floor(time_var / 3600)
        m = floor((time_var % 3600) / 60)
    elif time_var < 31557600:
        d = floor(time_var / 86400)
        h = floor((time_var % 86400) / 3600)
        m = floor(((time_var % 86400) % 3600) / 60)
    else:
        y = floor(time_var / 31557600)
        d = floor((time_var % 31557600) / 86400)
        h = floor(((time_var % 31557600) % 86400) / 3600)
        m = floor((((time_var % 31557600) % 86400) % 3600) / 60)

    if y > 0:
        if ntn == 'short':
            return f'{y:02d}:{d:02d}:{h:02d}:{m:02d}:{ceil(s)}'
        elif ntn == 'long':
            return (f'{y} years, {d} days,{h} hours, {m} months, and {s}'
                    ' seconds')
    elif d > 0:
        if ntn == 'short':
            return f'{d:02d}:{h:02d}:{m:02d}:{ceil(s):02d}'
        elif ntn == 'long':
            return f'{d} days, {h} hours, {m} months, and {s} seconds'
    else:
        if ntn == 'short':
            return f'{h:02d}:{m:02d}:{ceil(s):02d}'
        elif ntn == 'long':
            return f'{h} hours, {m} minutes, and {s} seconds'
