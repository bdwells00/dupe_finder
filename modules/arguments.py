

import argparse
from betterprint.colortext import Ct
import modules.version as version


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def get_args():
    """Get CLI arguments from argparse.

    Returns:
        - class 'argparse.ArgumentParser': Command Line Arguments
    """
    # Use argparse to capture cli parameters
    parser = argparse.ArgumentParser(
        prog=version.__prog__,
        description=f'{Ct.BBLUE}{version.ver}: {version.__purpose__}{Ct.A}',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=f'{Ct.RED}This program has no warranty. Please use with '
               f'caution.{Ct.A}',
        add_help=True)
    parser.add_argument('-f',
                        '--folder',
                        help='folder to scan for duplicates',
                        metavar=f'{Ct.RED}<path>{Ct.A}',
                        type=str)
    parser.add_argument('--auto',
                        help='automatically add the duplicated files to the'
                             'log file specified with "--log-file <filename>"',
                        action='store_true')
    parser.add_argument('--enable-delete-files',
                        help='interactive file deletion mode. DELETIONS ARE '
                             'EXPIRAMENTAL!!',
                        action='store_true')
    parser.add_argument('--exdir',
                        help='comma separated directories to exclude (no '
                             'spaces between directories)',
                        metavar=f'{Ct.GREEN}<dir>,<dir>{Ct.A}',
                        type=str)
    parser.add_argument('--exfile',
                        help='comma separated files to exclude (no spaces '
                             'between files)',
                        metavar=f'{Ct.GREEN}<file>,<file>{Ct.A}',
                        type=str)
    parser.add_argument('--json-output',
                        help='json file to save duplicates into',
                        metavar=f'{Ct.GREEN}<filename>{Ct.A}',
                        type=str)
    parser.add_argument('--json-input',
                        help='json file to process for deletions. DELETIONS '
                             'ARE EXPIRAMENTAL!!',
                        metavar=f'{Ct.GREEN}<filename>{Ct.A}',
                        type=str)
    parser.add_argument('--log-file',
                        help='file to save output',
                        metavar=f'{Ct.GREEN}<filename>{Ct.A}',
                        type=str)
    parser.add_argument('--no-color',
                        help='don\'t colorize output',
                        action='store_true')
    parser.add_argument('--two-hash',
                        help='also hash with blake2b for increased accuracy',
                        action='store_true')
    parser.add_argument('--version',
                        help='print program version and exit',
                        action='version',
                        version=f'{version.ver}')

    return parser.parse_args()
