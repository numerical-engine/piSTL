import numpy as np

class Geometry:
    """Represents the geometry of a STL.

    Attributes:
        vertices (np.ndarray): The vertices of the STL. The shape is (n, 3, 3) where n is the number of facets. vertices[i] contains the 3D coordinates of the three vertices of the i-th facet.
        facet_normals (np.ndarray): The normals of the facets in the STL. The shape is (n, 3) where n is the number of facets. facet_normals[i] contains the normal vector of the i-th facet.
    """
    def __init__(self, vertices:np.ndarray, facet_normals:np.ndarray):
        self.vertices = vertices
        self.facet_normals = facet_normals
    
    @property
    def bounds(self)->np.ndarray:
        """Calculates the axis-aligned bounding box of the geometry.

        Returns:
            np.ndarray: A 2x3 array where the first row contains the minimum x, y, z coordinates and the second row contains the maximum x, y, z coordinates.
        """
        min_bounds = np.min(self.vertices.reshape(-1, 3), axis=0)
        max_bounds = np.max(self.vertices.reshape(-1, 3), axis=0)
        return np.array([min_bounds, max_bounds])