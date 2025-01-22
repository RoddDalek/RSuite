"""
    debug.py
    Author: Rodolfo Canet
    Purpose: An alternative script to run to test particular functions without
    altering main.py.
"""

from scripts.files_util import ask_for_files

if __name__ == '__main__':
    print(ask_for_files())
