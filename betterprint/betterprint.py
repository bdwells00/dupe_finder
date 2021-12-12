#!/usr/bin/env python3
'''better print (bp) version 0.3.1'''


from datetime import datetime
import sys
from betterprint.colortext import Ct
import betterprint.version as version


# ~~~ #                 -global variable-
# global dict used to control bp functionality
bp_dict = {
    'bp_tracker_all': 0,        # tracks all bp function calls
    'bp_tracker_con': 0,        # tracks only bp cli calls
    'bp_tracker_log': 0,        # tracks only bp log_file calls
    'bp_tracker_elog': 0,       # tracks only bp elog_file calls
    'color': 1,                 # override cli color
    'date_log': 0,              # prepend date to each output
    'log_file': None,           # the log file name for all output
    'error_log_file': None,     # the error log file name for only errors
    'quiet': 0,                 # allows surpressing cli errors
    'verbose': 0,               # match this verbose to bp veb; skip if lower
    'con': 1,                   # permanently override the default con setting
    'err': 0,                   # permanently override the default err setting
    'fil': 1,                   # permanently override the default fil setting
    'fls': 0,                   # permanently override the default fls setting
    'inl': 0,                   # permanently override the default inl setting
    'log': 1,                   # permanently override the default log setting
    'num': 1,                   # permanently override the default num setting
    'veb': 0                    # permanently override the default veb setting
}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def bp(txt: list, con=bp_dict['con'], err=bp_dict['err'], fil=bp_dict['fil'],
       fls=bp_dict['fls'], inl=bp_dict['inl'], log=bp_dict['log'],
       num=bp_dict['num'], veb=bp_dict['veb']):
    """Better Print: send output commands here instead of using print command.
    Txt must be sent in the form of pairs of strings in a list. The even
    strings ("0", "2", "4", etc.) contain the output text while the odd strings
    ("1", "3", "5", etc.) contain the color companion that defines the color
    to be applied to the preceding string. There are pre-defined defaults that
    can be overwritten but not required.

    Example:
        - bp(['Hello', Ct.RED, 'world', Ct.A, '!', Ct.GREEN], veb=2)
            - This prints "Hello world!" with the Hello in red, world in
            terminal default color, and the bang in green. This will also only
            print if args.verbose is set to "2" via "-vv".

    Args:
        - txt (list): (required) must be pairs with the even entries a string
                      and odd sections the Ct.color to apply to that string.
        - con  (int): (optional) 0 = no console output, 1 = console output.
                      (default)
        - err  (int): (optional) 0 = none (default), 1 = WARNING, 2 = ERROR:
                      auto pre-pends ERROR: or WARNING:, colors line Red, and
                      allows routing of only these to error log if requested.
        - fil  (int): (optional) 0 = off, 1 (default)= on: setting zero skips
                      file output even if args requested.
        - fls  (int): (optional) 0 = off (default), 1 = on: flush the text
                      instead of holding on to it. Usually required for in-
                      line text (inl=1) to force output without an end-of-line.
        - inl  (int): (optional) 0 = off (default); 1 = on: text written in-
                      line with no end-of-line character. Make sure to invoke
                      eol with a final bp before moving on.
        - log  (int): (optional) 0 = off; 1 = on (default): allow pre-pend of
                      each print statement with the date. Can be turned off for
                      things like progress bars and % updates.
        - num  (int): (optional) 0 = off; 1 = on (default): print blue numbers
        - veb  (int): (optional) 0-3: value is used to print only as much as
                      requested.

    Return:
        - None
    """
    # ~~~ #             -variables-
    global bp_dict
    bp_local_dict = {
        'con_out': '',
        'file_out': ''
    }

    # ~~~ #             -all print tracking-
    # track function call even if no output
    bp_dict['bp_tracker_all'] += 1

    # ~~~ #             -validate verbosity-
    if err == 0 or bp_dict['quiet'] == 1:
        if bp_dict['verbose'] < veb:
            return      # skip higher veb as long as no errors or in quiet mode

    # ~~~ #             -validate txt list-
    # ensure each string has a color compliment within the list
    txt_l = len(txt)
    if txt_l % 2 != 0:
        raise Exception(f'{Ct.RED}"Better Print" (bp) function -> "txt: (list)'
                        f'": must be in pairs (txt length = {txt_l}){Ct.A}')

    # ~~~ #             -veb-
    # prepend INFO-L(x) to output
    if veb > 0 and err == 0 and log > 0:
        bp_local_dict['con_out'] = f'INFO-L{veb}: '
        bp_local_dict['file_out'] = f'INFO-L{veb}: '

    # ~~~ #             -err-
    # pre-pend Error or Warning, overwriting -veb- section
    if err == 1:
        bp_local_dict['con_out'] = f'{Ct.YELLOW}WARNING: {Ct.A}'
        bp_local_dict['file_out'] = 'WARNING: '
    elif err == 2:
        bp_local_dict['con_out'] = f'{Ct.RED}ERROR: {Ct.A}'
        bp_local_dict['file_out'] = 'ERROR: '

    # ~~~ #             -colorize and assemble-
    # need enumerate to identify even entries that contain strings
    for idx, val in enumerate(txt):
        if idx % 2 == 0:
            if type(val) != str:
                raise Exception(f'{Ct.RED}"Better Print" (bp) function -> "txt'
                                f' list even entries must be str. txt type = '
                                f'{type(val)}{Ct.A}')
            ttxt = ''               # even text val to be joined
            ctxt = txt[idx + 1]     # odd color val to color ttxt
            # colorize numbers and reset to default
            if num == 1 and ctxt == Ct.A:
                for idx in val[:]:
                    ttxt += f'{Ct.BBLUE}{idx}{Ct.A}' if idx.isdigit() else idx
            # colorize numbers and reset to requested color for that part
            elif num == 1:
                for idx in val[:]:
                    ttxt += f'{Ct.BBLUE}{idx}{ctxt}' if idx.isdigit() else idx
            # don't colorize numbers (equivalent to num=0)
            else:
                ttxt = val
            # now wrap the color numbered string with the requested color
            bp_local_dict['con_out'] += f'{ctxt}{ttxt}{Ct.A}'
            # file output is the original value with no console coloration
            bp_local_dict['file_out'] += val[:]

    # ~~~ #             -log-
    # allow log=0 to bypass this
    if bp_dict['date_log'] == 1 and log == 1:
        dt_now = datetime.now().strftime('[%H:%M:%S]')
        bp_local_dict['con_out'] = (
            f'{dt_now}-{bp_dict["bp_tracker_con"] + 1}'
            f'-{bp_local_dict["con_out"]}')
        bp_local_dict['file_out'] = (
            f'{dt_now}-{bp_dict["bp_tracker_log"] + 1}'
            f'-{bp_local_dict["file_out"]}')

    # ~~~ #             -color-
    # after all colorization sections, set cli to file if no color desired
    if bp_dict['color'] == 0:
        bp_local_dict['con_out'] = bp_local_dict['file_out'][:]

    # ~~~ #             -con-
    # skips con output if con=0
    if inl == 0 and con == 1:                   # default with new line
        sys.stdout.write(f'{bp_local_dict["con_out"]}\n')
        bp_dict['bp_tracker_con'] += 1
    elif inl == 1 and fls == 0 and con == 1:    # in-line with no flush
        sys.stdout.write(bp_local_dict['con_out'])
        bp_dict['bp_tracker_con'] += 1
    elif inl == 1 and fls == 1 and con == 1:    # in-line with flush
        bp_dict['bp_tracker_con'] += 1
        sys.stdout.write(bp_local_dict['con_out'])
        sys.stdout.flush()

    # ~~~ #             -file-
    try:
        # skip if file loging not requested or fil=0
        if bp_dict['log_file'] and fil == 1:
            with open(bp_dict['log_file'], 'a') as f:
                f.write(bp_local_dict['file_out'] + '\n')
        # separate errors into dedicated error log
        if bp_dict['error_log_file'] and err > 0 and fil == 1:
            with open(bp_dict['error_log_file'], 'a') as f:
                f.write(bp_local_dict['file_out'] + '\n')
    except OSError as e:
        bp([f'exception caught trying to write to {bp_dict["log_file"]} '
            f'or {bp_dict["error_log_file"]}\n\t{e}', Ct.RED], err=1, fil=0)

    return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

    # ~~~ #             -title-
    bp([f'{version.ver} - {version.__purpose__}\n', Ct.BBLUE])

    # ~~~ #             -exit-
    bp(['This module has no executable output. See the included examples.py '
        'for examples on how to use this module.'])
