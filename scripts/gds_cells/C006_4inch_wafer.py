"""
    C006_4inch_wafer.py
    Author: Rodolfo Canet
    Purpose: Cell representation of a basic 4-inch wafer.
"""

from scripts.utils.gdstk_utils import calc_rect_polygon

import numpy as np
import gdstk
import math


class FourInchWafer:

    def __init__(self):

        def generate_outline(center, radius):

            cell = gdstk.Cell("Outline")
            ext_circle = gdstk.ellipse(center, radius, tolerance=0.3, layer=5)
            int_circle = gdstk.ellipse(center, radius - 1500, tolerance=0.3, layer=6)
            cell.add(ext_circle)
            cell.add(int_circle)

            return cell

        # Designate basic properties
        self.center = (0, 0)
        self.size = 100000
        self.flat_length = 32500
        self.sec_flat_length = 18000
        self.cell = gdstk.Cell("FourInchWafer")
        self.base_elements = []

        self.markers = gdstk.read_gds(
            r"C:\Users\canetr1\OneDrive - Aalto University\GDS Files\Markers-5mm - Recenter.gds")

        self.base_elements.append(generate_outline(self.center, self.size))
        self.cell.add(gdstk.Reference(self.base_elements[-1], (0, 0)))


