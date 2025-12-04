"""
    C008_SnowflakeArray.py
    Author: Rodolfo Canet
    Purpose: Array version of Snowflake, working with mini-versions of it to save space and time.
"""

from scripts.utils.gdstk_utils import calc_rect_polygon, calc_octa_polygon, calc_arrow_polygon

import numpy as np
import gdstk
import math


class SnowflakeMini:

    def __init__(self, center=(0, 0), size=500, buffer_size=5, pattern="square",
                 base_distance=(1.08, 1), phi=0, shape="pillar", base_radius=0.395, inverse=False, chiral=False):

        def generate_center_text(text, text_size):

            text_cell = gdstk.Cell("Text - " + self.name)
            position = (self.center[0] - len(text) * text_size / 3.6, self.center[1] - text_size / 2)
            text = gdstk.text(text, text_size, position)
            for item in text:
                text_cell.add(item)
            bbox = text_cell.bounding_box()

            return text_cell, bbox

        def generate_octo_areas(size, b_width):

            def reorder_areas(areas):
                areas = [areas[3], areas[0], areas[1], areas[2], areas[4], areas[6], areas[7], areas[5]]
                return areas

            # Create the cell, and the basic polygon for the buffer between areas.
            buffer_cell = gdstk.Cell(self.name + "_buffer")
            base_buffer = gdstk.Polygon(calc_rect_polygon(self.center, size, b_width))
            buffer_cell.add(base_buffer)

            # Generate the rotated and replicated references to the first buffer.
            full_buffer = []
            for i in range(0, 4):
                full_buffer.append(gdstk.Reference(buffer_cell, origin=self.center, rotation=i * (np.pi / 4)))

            # Creating auxiliary polygons for area and array creation
            ext_octagon = gdstk.Polygon(calc_octa_polygon(self.center, 0.975 * size, 0.975 * size))
            int_octagon = gdstk.Polygon(calc_octa_polygon(self.center, 0.400 * size, 0.400 * size))

            # Creation of the final polygonal areas
            center_area = gdstk.boolean(ext_octagon, int_octagon, "not")
            areas = gdstk.boolean(center_area, full_buffer, "not", layer=2, datatype=0)
            print(len(areas))

            return reorder_areas(areas)

        def construct_param_matrix(pattern, a, b, phi, shape, radius, delta_d=0.0434, delta_r=0):

            if delta_d != 0:
                aux_a = np.linspace((1 - delta_d) * a, (1 + delta_d) * a, 8)
                aux_b = np.linspace((1 - delta_d) * b, (1 + delta_d) * b, 8)
                for i in range(0, 8):
                    aux_a[i] = round(aux_a[i], 4)
                    aux_b[i] = round(aux_b[i], 4)
            else:
                aux_a = a * np.ones(8)
                aux_b = b * np.ones(8)
            if delta_r != 0:
                aux_r = np.linspace((1 - delta_r) * radius, (1 + delta_r) * radius, 8)
                for i in range(0, 8):
                    aux_r[i] = round(aux_r[i], 4)
            else:
                aux_r = radius * np.ones(8)

            par_matrix = []
            for i in range(0, 8):
                aux_par = [pattern, aux_a[i], aux_b[i], phi, shape, aux_r[i]]
                par_matrix.append(aux_par)

            par_matrix = np.array(par_matrix)
            return par_matrix

        def construct_area(area, pattern, a, b, phi, shape, radius, chiral=False, inverse=False):

            def get_lattice_vector(pattern="rectangular", a=1, b=1, phi=0):

                a1, a2 = [], []
                if pattern == "oblique":
                    a1 = (a, 0)
                    a2 = (b * math.cos(phi), b * math.sin(phi))
                if pattern == "square":
                    a1 = (a, 0)
                    a2 = (0, a)
                if pattern == "rectangular":
                    a1 = (a, 0)
                    a2 = (0, b)
                if pattern == "hexagonal":
                    a1 = (a, 0)
                    a2 = (a / 2, a * math.sqrt(3) / 2)
                return np.array(a1), np.array(a2)

            def calculate_limits(area, a1, a2):

                bbox = area.bounding_box()
                bbox_dx, bbox_dy = bbox[1][0] - bbox[0][0], bbox[1][1] - bbox[0][1]
                n_x, n_y = int(bbox_dx / a1[0]), int(bbox_dy / a2[1])

                return bbox[0][0], bbox[0][1], n_x, n_y

            def generate_lattice(x0, y0, n_x, n_y, a1, a2):

                points = []
                for i in range(-n_x, n_x, 1):
                    for j in range(0, n_y, 1):
                        x1 = x0 + i * a1[0] + j * a2[0]
                        y1 = y0 + i * a1[1] + j * a2[1]
                        points.append([(x1, y1), 0])
                return points

            def generate_chiral_lattice(x0, y0, n_x, n_y, a1, a2):

                points = []
                for i in range(-n_x, n_x, 1):
                    for j in range(0, n_y, 1):
                        x1 = x0 + i * a1[0] + j * a2[0]
                        y1 = y0 + i * a1[1] + j * a2[1]
                        aux_alpha = math.atan(y1 / x1)
                        points.append([(x1, y1), aux_alpha])
                return points

            def populate_area(area, points, shape, radius):

                def generate_element(shape, radius):

                    element = None
                    if shape == "pillar":
                        element = gdstk.ellipse(self.center, radius=radius, tolerance=0.005, layer=1)
                    if shape == "arrow":
                        element = gdstk.Polygon(calc_arrow_polygon(self.center, radius, radius / 3))

                    return element

                aux_name = self.name + " - " + shape + "_" + str(len(self.base_elements))
                aux_element = generate_element(shape, radius)
                aux_cell = gdstk.Cell(aux_name)

                aux_cell.add(aux_element)
                self.base_elements.append(aux_cell)

                array = []
                """
                    This version of the point_check is the slowest, but works 100%.
                    If too slow, change to just one point and allow some to go through.
                """
                for point in points:
                    aux_check = True
                    aux_element = gdstk.Reference(self.base_elements[-1], point[0], rotation=point[1])
                    for aux_point in aux_element.get_polygons()[0].points:
                        if not area.contain_all(aux_point):
                            aux_check = False
                    if aux_check:
                        array.append(aux_element)

                return array

            def generate_param_text(area, shape, a, b, phi, inverse):
                pass

            a1, a2 = get_lattice_vector(pattern, a, b, phi)
            x0, y0, n_x, n_y = calculate_limits(area, a1, a2)
            if chiral:
                points = generate_chiral_lattice(x0, y0, n_x, n_y, a1, a2)
            else:
                points = generate_lattice(x0, y0, n_x, n_y, a1, a2)
            array = populate_area(area, points, shape, radius)
            if inverse:
                array = [gdstk.boolean(area, element, operation='not') for element in array]

            return array

        self.center = center
        self.size = size
        self.buffer_size = buffer_size
        self.base_radius = base_radius
        self.base_distance = base_distance
        self.name = "Snowflake (" + str(self.center[0]) + ", " + str(self.center[1]) + ")"
        self.cell = gdstk.Cell(self.name)
        self.base_elements = []

        # Generates and adds the center text
        text_cell, aux_bbox = generate_center_text(self.name, int(self.size / 40))
        text_position = (self.center[0] - (aux_bbox[0][0] + aux_bbox[1][0]) / 2,
                         self.center[1] - (aux_bbox[0][1] + aux_bbox[1][1]) / 2)
        self.cell.add(gdstk.Reference(text_cell, text_position))

        areas = generate_octo_areas(self.size, self.buffer_size)
        for area in areas:
            self.cell.add(area)

        pars = construct_param_matrix(pattern, self.base_distance[0], self.base_distance[1], phi,
                                      shape, self.base_radius)

        built_areas = []
        for i in range(0, len(areas)):
            built_areas.append(construct_area(areas[i], pars[i, 0], float(pars[i, 1]), float(pars[i, 2]),
                                              float(pars[i, 3]), pars[i, 4], float(pars[i, 5]), chiral, inverse))

        for area in built_areas:
            for element in area:
                try:
                    self.cell.add(element)
                except TypeError:
                    self.cell.add(element[0])
        self.base_elements.append(text_cell)


class SnowflakeArray:

    def __init__(self):
        self.center = (0, 0)
        self.snowflake_list = []

        d = (750, 0)

        self.snowflake_list.append(SnowflakeMini(self.center, pattern="hexagonal"))
        #self.snowflake_list.append(SnowflakeMini((self.center[0] + d[0], self.center[1] + d[1]), pattern="square"))
