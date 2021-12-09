'''colortext.py v0.1.0'''


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Ct:
    """A class of constants used to color strings for console printing. Using
    the full Unicode escape sequence to allow both 8 and 24 bit color here."""
    # ~~~ #     all 3-bit/4-bit 8 bit (256) unicode, plus some grey 256
    A = '\u001b[0m'                         # reset (all attributes off)
    BLACK = '\u001b[38;5;0m'                # black
    RED = '\u001b[38;5;1m'                  # red
    GREEN = '\u001b[38;5;2m'                # green
    YELLOW = '\u001b[38;5;3m'               # yellow
    BLUE = '\u001b[38;5;4m'                 # blue
    MAGENTA = '\u001b[38;5;5m'              # magenta
    CYAN = '\u001b[38;5;6m'                 # cyan
    WHITE = '\u001b[38;5;7m'                # white
    BBLACK = '\u001b[38;5;8m'               # bright black (grey)
    BRED = '\u001b[38;5;9m'                 # bright red
    BGREEN = '\u001b[38;5;10m'              # bright green
    BYELLOW = '\u001b[38;5;11m'             # bright yellow
    BBLUE = '\u001b[38;5;12m'               # bright blue
    BMAGENTA = '\u001b[38;5;13m'            # bright magenta
    BCYAN = '\u001b[38;5;14m'               # bright cyan
    BWHITE = '\u001b[38;5;15m'              # bright white
    GREY1 = '\u001b[38;5;255m'              # grey level 255 (most white)
    GREY2 = '\u001b[38;5;253m'              # grey level 253
    GREY3 = '\u001b[38;5;251m'              # grey level 251
    GREY4 = '\u001b[38;5;249m'              # grey level 249
    GREY5 = '\u001b[38;5;247m'              # grey level 247
    GREY6 = '\u001b[38;5;245m'              # grey level 245
    GREY7 = '\u001b[38;5;243m'              # grey level 243
    GREY8 = '\u001b[38;5;241m'              # grey level 241
    GREY9 = '\u001b[38;5;239m'              # grey level 239
    GREY10 = '\u001b[38;5;237m'             # grey level 237
    GREY11 = '\u001b[38;5;235m'             # grey level 235
    GREY12 = '\u001b[38;5;233m'             # grey level 233 (most black)
    # ~~~ #     some 24-bit unicode colors
    ORANGE = '\u001b[38;2;233;133;33m'      # orange
    BROWN = '\u001b[38;2;118;65;12m'        # brown
