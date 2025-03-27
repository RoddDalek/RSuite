"""
    C001_basic1.py
    Author: Rodolfo Canet
    Purpose: Cell representation of the contact pattern C001_Basic1.
"""

from scripts.utils.gdstk_utils import calc_rect_polygon

import numpy as np
import gdstk


class Basic1:

    def __init__(self, c_w=10, w1=15, h1=150, w2=100, h2=15, w3=500, h3=500):
        self.center = [0, 0]
        self.channel_w = c_w
        self.s1 = [w1, h1]
        self.s2 = [w2, h2]
        self.s3 = [w3, h3]
        self.cell_base = None
        self.cell = None
        self.generate_shape()

    def generate_shape(self):
        def generate_centers(center, channel_w, s1, s2, s3):
            center_1_x, center_1_y = center[0] + s1[0] / 2 + channel_w / 2, center[1]
            center_2_x, center_2_y = center_1_x + s1[0] / 2 + s2[0] / 2, center[1]
            center_3_x, center_3_y = center_2_x + s2[0] / 2 + s3[0] / 2, center[1]

            return [center_1_x, center_1_y], [center_2_x, center_2_y], [center_3_x, center_3_y]

        # Calculate centers
        c1, c2, c3 = generate_centers(self.center, self.channel_w, self.s1, self.s2, self.s3)

        # Calculate corner points for the different rectangles.
        c_s1 = calc_rect_polygon(c1, self.s1[0], self.s1[1])
        c_s2 = calc_rect_polygon(c2, self.s2[0], self.s2[1])
        c_s3 = calc_rect_polygon(c3, self.s3[0], self.s3[1])

        # Build up the shapes
        c_s1 = gdstk.Polygon(c_s1)
        c_s2 = gdstk.Polygon(c_s2)
        c_s3 = gdstk.Polygon(c_s3)

        # Build up the basic contact
        self.cell_base = gdstk.Cell("Contact")
        self.cell_base.add(c_s1, c_s2, c_s3)

        # Build the contact and its mirror
        right_contact = gdstk.Reference(self.cell_base, origin=(0, 0))
        left_contact = gdstk.Reference(self.cell_base, origin=(0, 0), rotation=np.pi)

        # Return the complete cell.
        self.cell = gdstk.Cell("Basic001")
        self.cell.add(right_contact, left_contact)
