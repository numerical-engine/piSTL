import numpy as np
from piSTL.core import Geometry
import sys

def split_lines(lines:list[list[str]])->list[list[str]]:
    """split lines into chunks based on 'solid' and 'endsolid' keywords

    Args:
        lines (list[list[str]]): The input lines to split.
    Returns:
        list[list[str]]: The split lines.
    """
    split_lines = []
    current_chunk = []
    for line in lines:
        if line[0] == 'solid':
            if current_chunk:
                split_lines.append(current_chunk)
            current_chunk = [line]
        elif line[0] == 'endsolid':
            current_chunk.append(line)
            split_lines.append(current_chunk)
            current_chunk = []
        else:
            current_chunk.append(line)
    if current_chunk:
        split_lines.append(current_chunk)
    return split_lines


def read_stl(file_path: str)->list[Geometry]:
    """Reads an STL file and extracts geometric information.

    Args:
        file_path (str): The path to the STL file.
    Returns:
        list[Geometry]: A list of Geometry objects representing the 3D shapes in the STL file.
    """
    geometries = []
    with open(file_path, 'r') as file:
        lines = [line.strip().split() for line in file.readlines()]
    blocks = split_lines(lines)

    for block in blocks:
        vertices = []
        facet_normals = []
        for i, line in enumerate(block):
            if line[0] == 'facet' and line[1] == 'normal':
                normal = list(map(float, line[2:5]))
                facet_normals.append(normal)
            elif line[0] == 'vertex':
                vertex = list(map(float, line[1:4]))
                vertices.append(vertex)
        vertices = np.array(vertices).reshape(-1, 3, 3)
        facet_normals = np.array(facet_normals)
        geometries.append(Geometry(vertices, facet_normals))
    
    return geometries