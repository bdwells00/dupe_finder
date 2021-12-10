'''
- dupeff.py             duplicate file finder
- modules               folder to hold dupeff modules
    - __init__.py       this file
    - argsval.py        validate arguments
    - arguments.py      argparse cli arguments
    - filechecks.py     size and hash logic to find duplicates
    - notations.py      simple B/kB/MB/GB/TB converter for raw byte input
    - options.py        global options that can be imported by other modules
    - timer.py          timing decorator using time.perf_counter
    - treewalk.py       walks folder structure to find all files and folders
    - version.py        program version
'''
