"""
    files_util.py
    Author: Rodolfo Canet
    Purpose: To hold the relevant scripts to import files easier.
"""

import tkinter as tk
import os

from tkinter.filedialog import askopenfilenames


def ask_for_files():
    """
    Opens a tkinter Dialog to select some files.
    :return: List with all the paths already normalized for all selected files.
    """
    return [os.path.normpath(x) for x in askopenfilenames()]


def import_data(filepath, separator='\t'):
    """
    In principle, it opens a .txt file and extracts the data.
    :param filepath:
    :param separator: Used separator in the file.
    :return: A list with all data tuples extracted on the file.
    """
    aux = []
    with open(filepath, 'r') as f:
        data = f.readlines()
    for item in data:
        aux.append(item.split(separator))
    return aux

