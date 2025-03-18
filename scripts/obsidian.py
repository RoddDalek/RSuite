"""
    obsidian.py
    Author: Rodolfo Canet
    Purpose: To hold functions that quickly alter one or many markdown files for Obsidian.
"""

import os

from scripts.files_util import ask_for_directory


class Vault:

    def __init__(self):

        def locate_vault():
            return ask_for_directory()

        def index_files(path):

            md_list = []
            png_list = []
            for subdir, dirs, files in os.walk(path):
                for file in files:
                    if os.path.split(file)[-1].endswith('.md'):
                        md_list.append((os.path.join(subdir, file)))
                    if os.path.split(file)[-1].endswith('.png'):
                        png_list.append((os.path.join(subdir, file)))
            return [md_list, png_list]

        self.path = locate_vault()
        self.vault = index_files(self.path)
        print(self.vault)