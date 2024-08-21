# Garbage
import os
import numpy as np
from stl import mesh

def create_isogrid_lattice(length, width, triangle_base):
    # Calculate number of triangles in x and y direction
    nx = int(length / triangle_base) + 1
    ny = int(width / triangle_base) + 1

    # Arrays to hold vertices and faces
    vertices = []
    faces = []

    # Generate vertices for the isogrid
    for i in range(nx):
        for j in range(ny):
            x = i * triangle_base
            y = j * triangle_base * np.sqrt(3) / 2

            # Add vertices, avoiding duplicates
            if j % 2 == 0:
                vertices.append([x, y, 0])  # Bottom vertex of triangle
                if i < nx - 1:
                    vertices.append([x + triangle_base / 2, y + triangle_base * np.sqrt(3) / 2, 0])  # Top vertex of triangle
            else:
                vertices.append([x + triangle_base / 2, y + triangle_base * np.sqrt(3) / 2, 0])  # Top vertex of triangle
                if i < nx - 1:
                    vertices.append([x + triangle_base, y, 0])  # Bottom vertex of next triangle

    # Create faces
    for i in range(0, len(vertices) - 2, 2):
        faces.append([i, i + 1, i + 2])

    # Convert vertices and faces to numpy arrays
    vertices = np.array(vertices)
    faces = np.array(faces)

    # Print debug information
    print(f"Number of vertices: {len(vertices)}")
    print(f"Number of faces: {len(faces)}")

    # Create the mesh
    isogrid_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            isogrid_mesh.vectors[i][j] = vertices[face[j], :]

    # Ensure output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the mesh to file
    try:
        isogrid_mesh.save(os.path.join(output_dir, "isogrid_lattice.stl"))
        print("STL file successfully saved.")
    except Exception as e:
        print(f"An error occurred while saving the STL file: {e}")

# Example usage
length = 100
width = 100
triangle_base = 10

create_isogrid_lattice(length, width, triangle_base)
