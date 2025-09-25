"""
    C005_RoundCoupler.py
    Author: Rodolfo Canet
    Purpose: Cell representation of RoundCoupler.
"""

from scripts.utils.gdstk_utils import calc_rect_polygon, calc_octa_polygon, calc_arrow_polygon

import numpy as np
import gdstk
import math


class RoundCoupler:

    def __init__(self):

        def generate_center_text(center, text, text_size):

            text_cell = gdstk.Cell("Chip name")
            position = (center[0] - len(text) * text_size / 3.6, center[1] - text_size / 2)
            text = gdstk.text(text, text_size, position, layer=3)
            for item in text:
                text_cell.add(item)
            bbox = text_cell.bounding_box()

            return text_cell, bbox

        def generate_octo_areas(center, size, b_width):

            def reorder_areas(areas):
                areas = [areas[3], areas[0], areas[1], areas[2], areas[4], areas[6], areas[7], areas[5]]
                return areas

            # Create the cell, and the basic polygon for the buffer between areas.
            buffer_cell = gdstk.Cell("Buffer")
            base_buffer = gdstk.Polygon(calc_rect_polygon(center, size, b_width))
            buffer_cell.add(base_buffer)

            # Generate the rotated and replicated references to the first buffer.
            full_buffer = []
            for i in range(0, 4, 1):
                full_buffer.append(gdstk.Reference(buffer_cell, rotation=i * (np.pi / 4)))

            # Creating auxiliary polygons for area and array creation
            ext_circle = gdstk.ellipse(center, 0.475 * size, tolerance=0.005)
            int_circle = gdstk.ellipse(center, 0.175 * size, tolerance=0.005)

            # Creation of the final polygonal areas
            center_area = gdstk.boolean(ext_circle, int_circle, "not")
            areas = gdstk.boolean(center_area, full_buffer, "not", layer=2, datatype=0)

            return reorder_areas(areas)

        def calculate_param_position(center):
            pass

        def construct_area(area, pattern, a, b, phi, shape, radius, inverse=False):

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
                        points.append((x0 + i * a1[0] + j * a2[0], y0 + i * a1[1] + j * a2[1]))
                return points

            def populate_area(area, points, shape, radius):

                def generate_element(shape, radius):

                    element = None
                    if shape == "pillar":
                        element = gdstk.ellipse(self.center, radius=radius, tolerance=0.005, layer=1)
                    if shape == "arrow":
                        element = gdstk.Polygon(calc_arrow_polygon(self.center, radius, radius / 3))

                    return element

                aux_name = shape + "_" + str(len(self.base_elements))
                aux_element = generate_element("pillar", radius)
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
                    aux_element = gdstk.Reference(self.base_elements[-1], point)
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
            points = generate_lattice(x0, y0, n_x, n_y, a1, a2)
            array = populate_area(area, points, shape, radius)
            if inverse:
                array = [gdstk.boolean(area, element, operation='not') for element in array]

            return array

        def construct_debug_areas():
            pass

        # Designate basic properties
        self.center = (0, 0)
        self.size = 200
        self.buffer_size = 1
        self.base_radius = 0.5
        self.radius_limit = 1.0
        self.cell = gdstk.Cell("RoundCoupler")
        self.base_elements = []

        # Generates and adds the center text
        text_cell, aux_bbox = generate_center_text(self.center, f"RoundCoupler v1", 5)
        text_position = (self.center[0] - (aux_bbox[0][0] + aux_bbox[1][0])/2,
                         self.center[1] - (aux_bbox[0][1] + aux_bbox[1][1])/2)
        self.cell.add(gdstk.Reference(text_cell, text_position))

        areas = generate_octo_areas(self.center, self.size, self.buffer_size)
        for area in areas:
            self.cell.add(area)

        areas = [construct_area(areas[0], "square", 2, 1, 0, "pillar", 0.250),
                 construct_area(areas[1], "hexagonal", 2, 1, 0, "pillar", 0.250),
                 construct_area(areas[2], "square", 1, 1, 0, "pillar", 0.250),
                 construct_area(areas[3], "hexagonal", 1, 1, 0, "pillar", 0.250),
                 construct_area(areas[4], "square", 0.75, 1, 0, "pillar", 0.250),
                 construct_area(areas[5], "hexagonal", 0.75, 1, 0, "pillar", 0.250),
                 construct_area(areas[6], "square", 0.5, 1, 0, "pillar", 0.250),
                 construct_area(areas[7], "hexagonal", 0.5, 1, 0, "pillar", 0.250)]

        for area in areas:
            for element in area:
                try:
                    self.cell.add(element)
                except TypeError:
                    self.cell.add(element[0])
        self.base_elements.append(text_cell)
