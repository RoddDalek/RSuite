"""
    C000_markers_5mm.py
    Author: Rodolfo Canet
    Purpose: Integration of Nianze's markers for 5mm chips.
"""

from scripts.utils.gdstk_utils import calc_rect_polygon

import numpy as np
import gdstk


class Markers5mm:

    def __init__(self):

        self.lib = gdstk.read_gds(r"C:\Users\canetr1\OneDrive - Aalto University\GDS Files\Markers-5mm - Recenter.gds")

