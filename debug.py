"""
    debug.py
    Author: Rodolfo Canet
    Purpose: An alternative script to run to test particular functions without
    altering main.py.
"""

from scripts.files_util import ask_for_files, import_data, export_data


def test():
    aux = ask_for_files()
    aux = import_data(aux[0])
    print(aux)
    export_data('Debugged.txt', aux)


if __name__ == '__main__':
    test()
