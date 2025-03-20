"""
    files_util.py
    Author: Rodolfo Canet
    Purpose: To hold the relevant scripts to import and export files easier.
"""

import os

from tkinter.filedialog import askopenfilenames, askdirectory


def ask_for_files():
    """
    Opens a tkinter Dialog to select some files.
    :return: List with all the paths already normalized for all selected files.
    """
    return [os.path.normpath(x) for x in askopenfilenames()]


def ask_for_directory():
    """
        Opens a tkinter Dialog to select a folder.
        :return: List with all the paths already normalized for all selected files.
    """
    return os.path.normpath(askdirectory())


def import_data(filepath, separator='\t'):
    """
    It opens a .txt file and extracts the data.
    :param filepath:
    :param separator: Used separator in the file.
    :return: A list with all data tuples extracted on the file.
    """
    aux = []
    try:
        with open(filepath, 'r') as f:
            data = f.read()
        data = data.split('\n')
        for item in data:
            aux.append(item.split(separator))
    except FileNotFoundError:
        print('The selected file was not found.')
    return aux


def export_data(filepath, data, separator='\t'):
    """
    It creates a new .txt file with the exported data from the RSuite.
    :param filepath:
    :param data:
    :param separator:
    """
    with open(filepath, 'w') as f:
        for item in data:
            f.write(item[0] + separator + item[1] + '\n')
