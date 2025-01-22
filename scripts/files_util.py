"""
    files_util.py
    Author: Rodolfo Canet
    Purpose: To hold the relevant scripts to import files easier.
"""

import tkinter as tk
import os

from tkinter.filedialog import askopenfilenames


def ask_for_files():
    return [os.path.normpath(x) for x in askopenfilenames()]
