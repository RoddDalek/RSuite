"""
    C003_Scorpio.py
    Author: Rodolfo Canet
    Purpose: Cell representation of the contact pattern C003_Scorpio.
"""

from scripts.utils.gdstk_utils import create_pad, calc_rect_polygon

from scripts.gds_cells.C000_markers_5mm import Markers5mm

import numpy as np
import gdstk


# noinspection PyTypeChecker
class Scorpio:

    def __init__(self, channel_width=15, line_height=75, pad_size=500):

        self.markers = Markers5mm()
        self.center = [0, 0]
        self.cell_base = None
        self.cell = None

        self.h1 = 100
        self.w1 = 250

        self.channel_width = channel_width
        self.line_height = line_height
        self.line_width = 20
        self.pad_size = pad_size

        self.line = gdstk.Cell("Contact Line")
        self.pad = gdstk.Cell("Wire Pad")
        self.pad.add(create_pad(self.pad_size))

        self.unit = gdstk.Cell("Scorpio_Unit")

        for item in self.generate_shape():
            self.unit.add(item)

        self.scorpio = gdstk.Cell("Scorpio")
        self.scorpio.add(gdstk.Reference(self.unit, origin=(1.175 * self.pad_size, -4 * self.pad_size)
                                         , rotation=np.pi/4))
        self.scorpio.add(gdstk.Reference(self.unit, origin=(-1.175 * self.pad_size, 4 * self.pad_size)
                                         , rotation=5*np.pi / 4))

        for item in self.markers.lib.cells:
            self.scorpio.add(gdstk.Reference(item, origin=(0, 0)))

        self.cells = [self.scorpio, self.unit]

    def generate_shape(self):

        def generate_x(n, j):
            aux_x = 1.5 * self.pad_size + self.w1
            return aux_x + n * self.line_width / 2 + j * self.channel_width

        def deposit_pads():

            def define_parameters():

                y_15 = self.pad_size * 2.5 + 2 * self.h1
                y_24 = self.pad_size * 1.5 + self.h1
                y_3 = self.pad_size

                x_12 = self.pad_size / 2
                x_3 = self.pad_size * 1.5 + self.w1
                x_45 = self.pad_size * 2.5 + 2 * self.w1

                return x_12, x_3, x_45, y_15, y_24, y_3

            x_12, x_3, x_45, y_15, y_24, y_3 = define_parameters()

            p1 = gdstk.Reference(self.pad, (x_12, y_15))
            p2 = gdstk.Reference(self.pad, (x_12, y_24))
            p3 = gdstk.Reference(self.pad, (x_3, y_3))
            p4 = gdstk.Reference(self.pad, (x_45, y_24))
            p5 = gdstk.Reference(self.pad, (x_45, y_15))

            return [p1, p2, p3, p4, p5]

        def deposit_lines():

            def define_parameters():

                x_2 = generate_x(-2, -2)
                x_1 = generate_x(-1, -1)
                x_3 = generate_x(0, 0)
                x_5 = generate_x(1, 1)
                x_4 = generate_x(2, 2)

                y_all = 2.5 * self.pad_size + self.line_height / 2

                return x_1, x_2, x_3, x_4, x_5, y_all

            x_1, x_2, x_3, x_4, x_5, y_all = define_parameters()
            line_1 = gdstk.Polygon(calc_rect_polygon((x_1, y_all), 0.8 * self.line_width, self.line_height))
            line_2 = gdstk.Polygon(calc_rect_polygon((x_2, y_all), 0.6 * self.line_width, self.line_height))
            line_3 = gdstk.Polygon(calc_rect_polygon((x_3, y_all), self.line_width, self.line_height))
            line_4 = gdstk.Polygon(calc_rect_polygon((x_4, y_all), 0.6 * self.line_width, self.line_height))
            line_5 = gdstk.Polygon(calc_rect_polygon((x_5, y_all), 0.8 * self.line_width, self.line_height))
            lines = [line_1, line_2, line_3, line_4, line_5]

            return lines

        def deposit_paths():

            def pad1_to_line1():
                x0, y0 = self.pad_size, 2.5 * self.pad_size + 2 * self.h1
                x1, y1 = generate_x(-1, -1), 2.5 * self.pad_size + 2 * self.line_height
                x2, y2 = generate_x(-1, -1), 2.5 * self.pad_size + self.line_height
                return gdstk.FlexPath(((x0, y0), (x1, y1), (x2, y2)), ends='smooth', width = self.channel_width / 2)

            def pad2_to_line2():
                x0, y0 = self.pad_size, 1.5 * self.pad_size + 1 * self.h1
                x1, y1 = generate_x(-2, -2), 2.5 * self.pad_size - self.line_height / 2
                x2, y2 = generate_x(-2, -2), 2.5 * self.pad_size
                return gdstk.FlexPath(((x0, y0), (x1, y1), (x2, y2)), ends='smooth', width = self.channel_width / 2)

            def pad3_to_line3():

                x0, y0 = 1.5 * self.pad_size + self.w1, 1.5 * self.pad_size
                x1, y1 = 1.5 * self.pad_size + self.w1, 2.5 * self.pad_size
                return gdstk.FlexPath(((x0, y0), (x1, y1)), ends='smooth', width = self.channel_width / 2)

            def pad4_to_line4():
                x0, y0 = 2 * self.pad_size + 2 * self.w1, 1.5 * self.pad_size + 1 * self.h1
                x1, y1 = generate_x(2, 2), 2.5 * self.pad_size - self.line_height / 2
                x2, y2 = generate_x(2, 2), 2.5 * self.pad_size
                return gdstk.FlexPath(((x0, y0), (x1, y1), (x2, y2)), ends='smooth', width = self.channel_width / 2)

            def pad5_to_line5():
                x0, y0 = 2 * self.pad_size + 2 * self.w1, 2.5 * self.pad_size + 2 * self.h1
                x1, y1 = generate_x(1, 1), 2.5 * self.pad_size + 2 * self.line_height
                x2, y2 = generate_x(1, 1), 2.5 * self.pad_size + 1.0 * self.line_height
                return gdstk.FlexPath(((x0, y0), (x1, y1), (x2, y2)), ends='smooth', width = self.channel_width / 2)

            path_1 = pad1_to_line1()
            path_2 = pad2_to_line2()
            path_3 = pad3_to_line3()
            path_4 = pad4_to_line4()
            path_5 = pad5_to_line5()

            return path_1, path_2, path_3, path_4, path_5

        def cleanup_operation(list1, list2):

            clean = []
            for item1, item2 in zip(list1, list2):
                clean.append(gdstk.boolean(item1, item2, operation='or')[0])
            return clean

        pads = deposit_pads()
        lines = deposit_lines()
        paths = deposit_paths()

        clean = cleanup_operation(pads, paths)
        clean = cleanup_operation(clean, lines)

        return clean
