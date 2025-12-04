import gdstk


def calc_rect_polygon(center=None, w: float = 500, h: float = 500):

    if center is None:
        center = [0, 0]

    x, y = center[0], center[1]
    x1, y1 = x - w / 2, y + h / 2
    x2, y2 = x - w / 2, y - h / 2
    x3, y3 = x + w / 2, y - h / 2
    x4, y4 = x + w / 2, y + h / 2

    return [x1, y1], [x2, y2], [x3, y3], [x4, y4]


class CapacitorArray:

    def __init__(self):
        self.center = [0, 0]
        self.cell = gdstk.Cell("CapacitorArray")

        test = self.generate_unit()

        lib = gdstk.Library()
        for item in test:
            lib.add(item)

        lib.write_gds(r"C:\Users\canetr1\OneDrive - Aalto University\GDS Files\test.gds")
        print(gdstk.gds_info(r"C:\Users\canetr1\OneDrive - Aalto University\GDS Files\test.gds"))

    def generate_unit(self):
        def generate_capacitor():
            basic_cell = gdstk.Cell("Capacitor array cell")
            basic_square = gdstk.Polygon(calc_rect_polygon((0, 0), 500, 500), layer=1)
            hole_cell = gdstk.Cell("Basic hole")
            basic_hole = gdstk.Polygon(calc_rect_polygon((0, 0), 50, 50), layer=0)
            hole_cell.add(basic_hole)

            basic_cell.add(basic_square)
            aux_hole = gdstk.Reference(hole_cell, (-150, 150), columns=4, rows=4, spacing=(100, -100))

            aux_bool = gdstk.boolean(basic_square, aux_hole, 'not')
            for item in aux_bool:
                basic_cell.add(item)

            return basic_cell, hole_cell

        test = generate_capacitor()

        return test


if __name__ == "__main__":
    test = CapacitorArray()
