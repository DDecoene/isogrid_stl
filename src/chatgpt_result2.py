# I gave it the design document from nasa and let it read and update the code.
# Hint: It's still garbage

import os
import numpy as np
from stl import mesh

def create_isogrid_lattice(length, width, depth, rib_width, triangle_base):
    # Calculate the number of nodes in x and y directions
    nx = int(length / triangle_base) + 1
    ny = int(width / (triangle_base * np.sqrt(3) / 2)) + 1

    # Array to hold vertices and faces
    vertices = []
    faces = []

    # Generate vertices and faces for the isogrid
    for i in range(nx):
        for j in range(ny):
            # Compute the x, y coordinates of the nodes
            x = i * triangle_base
            y = j * (triangle_base * np.sqrt(3) / 2)

            # Create the main vertices for each triangle
            if j % 2 == 0:  # Shift every other row
                v1 = [x, y, 0]
                v2 = [x + triangle_base / 2, y + (triangle_base * np.sqrt(3) / 2), 0]
                v3 = [x + triangle_base, y, 0]
            else:
                v1 = [x + triangle_base / 2, y - (triangle_base * np.sqrt(3) / 2), 0]
                v2 = [x + triangle_base, y, 0]
                v3 = [x + triangle_base / 2, y + (triangle_base * np.sqrt(3) / 2), 0]

            # Add vertices for thickness (top layer)
            v1_thick = [v1[0], v1[1], depth]
            v2_thick = [v2[0], v2[1], depth]
            v3_thick = [v3[0], v3[1], depth]

            # Append vertices
            base_index = len(vertices)
            vertices.extend([v1, v2, v3, v1_thick, v2_thick, v3_thick])

            # Create faces (two triangular faces per side of the triangular prism)
            faces.extend([
                [base_index, base_index + 1, base_index + 2],  # Bottom face
                [base_index + 3, base_index + 4, base_index + 5],  # Top face
                [base_index, base_index + 1, base_index + 4],  # Side face 1
                [base_index, base_index + 4, base_index + 3],  # Side face 1 (continued)
                [base_index + 1, base_index + 2, base_index + 5],  # Side face 2
                [base_index + 1, base_index + 5, base_index + 4],  # Side face 2 (continued)
                [base_index + 2, base_index + 0, base_index + 3],  # Side face 3
                [base_index + 2, base_index + 3, base_index + 5]   # Side face 3 (continued)
            ])

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
length = 100  # Length of the isogrid panel
width = 100  # Width of the isogrid panel
depth = 5  # Depth of the panel
rib_width = 2  # Width of the ribs
triangle_base = 10  # Base length of the triangles

create_isogrid_lattice(length, width, depth, rib_width, triangle_base)
