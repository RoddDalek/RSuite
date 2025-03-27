"""
    C002_Snowflake_II.py
    Author: Rodolfo Canet
    Purpose: Cell representation of the contact pattern C002_SnowflakeII.
"""

from scripts.utils.gdstk_utils import calc_rect_polygon, calc_hex_polygon

import numpy as np
import gdstk


# noinspection PyTypeChecker
class SnowflakeII:

    def __init__(self, c_w=10, limit_x=1750):

        # Designate basic properties
        self.center = (0, 0)
        self.base_radius = 0.15
        self.radius_limit = 0.5
        self.cell = gdstk.Cell("Snowflake II")
        self.base_pillars = []

        # Generate the basic shapes that the chip will need.
        self.areas = self.generate_areas(c_w, limit_x)
        # Re-order areas, check if results become weird.
        self.areas = self.reorder_areas()

        for item in self.areas:
            self.cell.add(item)

        self.generate_sqa_arrays()
        self.generate_hex_arrays()

        # Generate and add to the cell the center text of the chip
        for item in self.generate_center_text(f"Snowflake II", 30):
            self.cell.add(item)

    def reorder_areas(self):
        areas = [self.areas[3], self.areas[0], self.areas[1], self.areas[2], self.areas[4], self.areas[6],
                 self.areas[7], self.areas[5]]
        return areas

    def generate_center_text(self, text, text_size):

        position = (self.center[0] - len(text) * text_size / 3.6, self.center[0] - text_size / 2)
        text = gdstk.text(text, 30, position)

        return text

    def generate_areas(self, c_w, limit_x):

        # Create the first polygon which will be rotated and replicated for the channels between.
        barrier_cell = gdstk.Cell("Barrier")
        base_barrier = gdstk.Polygon(calc_rect_polygon(self.center, 2 * limit_x, c_w))
        barrier_cell.add(base_barrier)

        # Generate the rotated and replicated references to the first polygon.
        full_barrier = []
        for i in range(0, 4, 1):
            full_barrier.append(gdstk.Reference(barrier_cell, rotation=i * (np.pi / 4)))

        # Creating now auxiliary polygons for area and array creation
        int_hexagon = gdstk.Polygon(calc_hex_polygon(self.center, 0.4 * limit_x, 0.4 * limit_x))
        ext_hexagon = gdstk.Polygon(calc_hex_polygon(self.center, 0.975 * 2 * limit_x, 0.975 * 2 * limit_x))

        # Creation of the polygons for each area
        center_area = gdstk.boolean(ext_hexagon, int_hexagon, "not")
        areas = gdstk.boolean(center_area, full_barrier, "not", layer=2, datatype=2)

        return areas

    def generate_sqa_arrays(self):

        # noinspection PyTypeChecker
        def generate_sqa_array(area, m=0):
            def calculate_limits(bbox):
                return bbox[1][0] - bbox[0][0], bbox[1][1] - bbox[0][1]

            bbox = area.bounding_box()
            bbox_dx, bbox_dy = calculate_limits(bbox)

            aux_r = self.base_radius + m * (self.radius_limit - self.base_radius) / 3
            aux_d = 3 * aux_r

            self.base_pillars.append(gdstk.Cell("Pillar_" + str(m)).add(gdstk.ellipse(self.center, radius=aux_r
                                                                                      , tolerance=0.005)))

            n_x, n_y = int(bbox_dx / aux_d - 2 * aux_r), int(bbox_dy / aux_d - 2 * aux_r)

            array = []
            for i in range(0, n_x, 1):
                aux_x = bbox[0][0] + aux_r + i * aux_d
                for j in range(0, n_y, 1):
                    aux_y = bbox[0][1] + aux_r + j * aux_d
                    aux_element = gdstk.Reference(self.base_pillars[m], (aux_x, aux_y))
                    if area.contain_all(aux_element.get_polygons()[0].points[0]):
                        array.append(aux_element)

            return array

        array_list = []
        for area, m in zip(self.areas[0:4], range(0, 4, 1)):
            array_list.append(generate_sqa_array(area, m))

        for array in array_list:
            for element in array:
                self.cell.add(element)

    def generate_hex_arrays(self):

        # noinspection PyTypeChecker
        def generate_hex_array(area, m=0):
            def calculate_limits(bbox):
                return bbox[1][0] - bbox[0][0], bbox[1][1] - bbox[0][1]

            bbox = area.bounding_box()
            bbox_dx, bbox_dy = calculate_limits(bbox)

            aux_r = self.base_radius + m * (self.radius_limit - self.base_radius) / 3
            aux_d = 3 * aux_r

            n_x, n_y = int(bbox_dx / aux_d - 2 * aux_r), int(bbox_dy / aux_d - 2 * aux_r)

            array = []
            for i in range(0, n_x, 2):
                aux_x = bbox[0][0] + aux_r + i * aux_d
                for j in range(0, n_y, 1):
                    aux_y = bbox[0][1] + aux_r + j * aux_d
                    aux_element = gdstk.Reference(self.base_pillars[m], (aux_x, aux_y))
                    if area.contain_all(aux_element.get_polygons()[0].points[0]):
                        array.append(aux_element)
                aux_x = bbox[0][0] + aux_r + (i + 1) * aux_d
                for j in range(0, n_y, 1):
                    aux_y = bbox[0][1] + aux_r + (j + 1/3) * aux_d
                    aux_element = gdstk.Reference(self.base_pillars[m], (aux_x, aux_y))
                    if area.contain_all(aux_element.get_polygons()[0].points[0]):
                        array.append(aux_element)

            return array

        array_list = []
        for area, m in zip(self.areas[4:8], range(0, 4, 1)):
            array_list.append(generate_hex_array(area, m))

        for array in array_list:
            for element in array:
                self.cell.add(element)
