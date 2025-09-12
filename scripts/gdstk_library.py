"""
    gdstk_library.py
    Author: Rodolfo Canet
    Purpose: To serve as the main script from where to run compilation of the gdstk library.
"""


from scripts.gds_cells.C000_markers_5mm import Markers5mm
from scripts.gds_cells.C001_basic1 import Basic1
from scripts.gds_cells.C002_Snowflake_II import SnowflakeII
from scripts.gds_cells.C003_Scorpio import Scorpio


import gdstk


def gdstk_library():
    # Library definition, which translates into the final gds file.
    lib = gdstk.Library()

    """
        Definition of the cell, which corresponds to the final "item" that will be created
        into the library.
    """
    # basic_markers = Markers5mm()
    # basic = Basic1()
    snowflake_2 = SnowflakeII()
    # scorpio = Scorpio()

    # Add each cell from one library into the final one.
    """    
    for cell in basic_markers.lib.cells:
        lib.add(cell)
    lib.add(basic.cell_base)
    lib.add(basic.cell)
    """

    for item in snowflake_2.base_pillars:
        lib.add(item)
    lib.add(snowflake_2.cell)

    """for cell in basic_markers.lib.cells:
        lib.add(cell)"""

    """for cell in scorpio.cells:
        lib.add(cell)"""

    # Saving the library in a GDSII file.
    lib.write_gds(r"C:\Users\canetr1\OneDrive - Aalto University\GDS Files\test.gds")
    print(gdstk.gds_info(r"C:\Users\canetr1\OneDrive - Aalto University\GDS Files\test.gds"))
