import numpy as np
from piSTL.core import Geometry
import sys

def voxelization(geometry:Geometry, size:float, bounds:np.ndarray = None, occupied:bool = True)->np.ndarray:
    """Performs voxelization of the 3D geometry.

    Args:
        geometry (Geometry): The 3D geometry to voxelize.
        size (float): The size of the voxels.
        bounds (np.ndarray, optional): The bounding box of the geometry. Defaults to None.
    Returns:
        np.ndarray: A 3D binary array representing the voxelized geometry.
        If occupied is True, the array will contain 1s for occupied voxels and 0s for unoccupied voxels.
        Otherwise, the array will contain 0s for occupied voxels and 1s for unoccupied voxels.
    """
    bounds = geometry.bounds if bounds is None else bounds
    grid_size = np.ceil((bounds[1] - bounds[0]) / size).astype(int)

    x = np.arange(bounds[0, 0], bounds[1, 0], size) + size / 2
    y = np.arange(bounds[0, 1], bounds[1, 1], size) + size / 2
    z = np.arange(bounds[0, 2], bounds[1, 2], size) + size / 2

    voxel_coords = (np.stack(np.meshgrid(x, y, z, indexing='ij'), axis = -1)).reshape(-1, 3)
    
    vertices1 = geometry.vertices[:,0]
    signed = np.stack([np.dot(vertex1 - voxel_coords, facet_normal) for vertex1, facet_normal in zip(vertices1, geometry.facet_normals)], axis = -1)
    signed = np.all(signed > 0, axis = -1) if occupied else np.all(signed < 0, axis = -1)
    signed = signed.reshape(grid_size)

    return signed