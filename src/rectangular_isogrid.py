import os
import struct
import math


def create_isogrid_stl(
    filename, width, height, line_thickness, depth, triangle_side_length
):
    half_thickness = line_thickness / 2.0
    num_triangles = 0
    facets = []

    def add_facet(v1, v2, v3):
        nonlocal num_triangles
        normal = (0.0, 0.0, 0.0)
        facets.append((normal, v1, v2, v3))
        num_triangles += 1

    def add_rect(p1, p2, p3, p4):
        add_facet(p1, p2, p3)
        add_facet(p1, p3, p4)

    def add_triangle(p1, p2, p3):
        # Bottom face
        add_facet((p1[0], p1[1], 0), (p2[0], p2[1], 0), (p3[0], p3[1], 0))
        # Top face
        add_facet((p1[0], p1[1], depth), (p2[0], p2[1], depth), (p3[0], p3[1], depth))
        # Side faces
        add_rect(
            (p1[0], p1[1], 0),
            (p1[0], p1[1], depth),
            (p2[0], p2[1], depth),
            (p2[0], p2[1], 0),
        )
        add_rect(
            (p2[0], p2[1], 0),
            (p2[0], p2[1], depth),
            (p3[0], p3[1], depth),
            (p3[0], p3[1], 0),
        )
        add_rect(
            (p3[0], p3[1], 0),
            (p3[0], p3[1], depth),
            (p1[0], p1[1], depth),
            (p1[0], p1[1], 0),
        )

    # Define an equilateral triangle with a base of 100mm
    base = triangle_side_length
    height_triangle = math.sqrt(base**2 - (base / 2) ** 2)

    # _______
    # |\/|\/|
    # -------
    # |/\|/\|
    # _______
    #

    # Fill the width
    y_offset = 0
    while y_offset < height:
        x_offset = 0
        while x_offset < width:
            # Left triangle
            p1 = (x_offset, y_offset)
            p2 = (x_offset, y_offset + base)
            p3 = (x_offset + base, y_offset + base)
            add_triangle(p1, p2, p3)

            # Right triangle
            p1 = (x_offset + base, y_offset + base)
            p2 = (x_offset + base * 2, y_offset + base)
            p3 = (x_offset + base * 2, y_offset)
            add_triangle(p1, p2, p3)

            # top triangle
            p1 = (x_offset, y_offset)
            p2 = (x_offset + base * 2, y_offset)
            p3 = (x_offset + base, y_offset + base)
            add_triangle(p1, p2, p3)

            x_offset += base * 2
        y_offset += base

    # Write the binary STL file
    with open(filename, "wb") as f:
        f.write(b"\0" * 80)  # 80-byte header
        f.write(struct.pack("<I", num_triangles))  # Number of triangles

        for facet in facets:
            normal, v1, v2, v3 = facet
            f.write(struct.pack("<3f", *normal))
            f.write(struct.pack("<3f", *v1))
            f.write(struct.pack("<3f", *v2))
            f.write(struct.pack("<3f", *v3))
            f.write(b"\0\0")  # Attribute byte count


filename = os.path.join("output", "isogrid.stl")
create_isogrid_stl(
    filename,
    width=1000.0,
    height=1000.0,
    line_thickness=10.0,
    depth=50.0,
    triangle_side_length=100.0,
)
