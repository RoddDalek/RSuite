"""
    C004_Snowflake_III.py
    Author: Rodolfo Canet
    Purpose: Cell representation of the contact pattern C004_Snowflake_III.
"""

from scripts.utils.gdstk_utils import calc_rect_polygon, calc_octo_polygon

import numpy as np
import gdstk
import math


class SnowflakeIII:

    def __init__(self):

        def generate_center_text(center, text, text_size):
            position = (center[0] - len(text) * text_size / 3.6, center[1] - text_size / 2)
            text = gdstk.text(text, 30, position)

            return text

        # Designate basic properties
        self.center = (0, 0)
        self.base_radius = 0.5
        self.radius_limit = 1.0
        self.cell = gdstk.Cell("Snowflake III")

        # Generates and adds the center text
        for item in generate_center_text(self.center, f"Snowflake III", 30):
            self.cell.add(item)



