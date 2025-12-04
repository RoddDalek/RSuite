"""
    gdstk_example.py
    Author: Rodolfo Canet
    Purpose: To serve as the main script from where to run testing of the gdstk library.
"""

from scripts.gds_cells.C001_basic1 import Basic1

import gdstk


def gdstk_test():
    # Library definition, which translates into the final gds file.
    lib = gdstk.Library()

    """
        Definition of the cell, which corresponds to the final "item" that will be created
        into the library.
    """
    cell = lib.new_cell("Basic")

    # Create a geometry that will be added to the cell.
    rect = gdstk.rectangle((0, 0), (2, 1))
    cell.add(rect)

    # Saving the library in a GDSII file.
    lib.write_gds("test.gds")

    # Optionally, obtain a .svg with
    cell.write_svg("test.svg")
