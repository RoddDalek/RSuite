"""
    debug.py
    Author: Rodolfo Canet
    Purpose: An alternative script to run to test particular functions without
    altering main.py.
"""

from scripts.files_util import ask_for_files, import_data, export_data
from scripts.obsidian import Vault

from scripts.gdstk_library import gdstk_library


def test():
    gdstk_library()


if __name__ == '__main__':
    print('Starting debug.')
    test()
    print('Ending debug.')
