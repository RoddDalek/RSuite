"""
    gdstk_utils.py
    Author: Rodolfo Canet
    Purpose: To hold interesting, repeatable functions that can be used with the gdstk library.
"""

import gdstk

from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath


def calc_rect_polygon(center, w, h):

    x, y = center[0], center[1]
    x1, y1 = x - w / 2, y + h / 2
    x2, y2 = x - w / 2, y - h / 2
    x3, y3 = x + w / 2, y - h / 2
    x4, y4 = x + w / 2, y + h / 2

    return [x1, y1], [x2, y2], [x3, y3], [x4, y4]


def calc_hex_polygon(center, w, h):

    x, y = center[0], center[1]
    x1, y1 = x + w / 6, y + h / 2
    x2, y2 = x + w / 2, y + h / 6
    x3, y3 = x + w / 2, y - h / 6
    x4, y4 = x + w / 6, y - h / 2
    x5, y5 = x - w / 6, y - h / 2
    x6, y6 = x - w / 2, y - h / 6
    x7, y7 = x - w / 2, y + h / 6
    x8, y8 = x - w / 6, y + h / 2

    return [x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6], [x7, y7], [x8, y8]


def render_text(text, size=None, position=(0, 0), font_prop=None, tolerance=0.1):

    precision = 0.1 * tolerance
    path = TextPath(position, text, size=size, prop=font_prop)
    polys = []
    xmax = position[0]

    for points, code in path.iter_segments():

        if code == path.MOVETO:
            c = gdstk.Curve(points, tolerance=tolerance)
        elif code == path.LINETO:
            c.segment(points.reshape(points.size // 2, 2))
        elif code == path.CURVE3:
            c.quadratic(points.reshape(points.size // 2, 2))
        elif code == path.CURVE4:
            c.cubic(points.reshape(points.size // 2, 2))
        elif code == path.CLOSEPOLY:
            pts = c.points()
            if pts.size > 0:
                poly = gdstk.Polygon(pts)
                if pts[:, 0].min() < xmax:
                    i = len(polys) - 1
                    while i >= 0:
                        if polys[i].contain_any(*poly.points):
                            p = polys.pop(i)
                            poly = gdstk.boolean(p, poly, "xor", precision)[0]
                            break
                        elif poly.contain_any(*polys[i].points):
                            p = polys.pop(i)
                            poly = gdstk.boolean(p, poly, "xor", precision)[0]
                        i -= 1
                xmax = max(xmax, poly.points[:, 0].max())
                polys.append(poly)

    return polys


"""
if __name__ == "__main__":
    cell = gdstk.Cell("fonts")
    fp = FontProperties(family="serif", style="italic")
    polygons = render_text("Text rendering", 10, font_prop=fp)
    cell.add(*polygons)
"""
