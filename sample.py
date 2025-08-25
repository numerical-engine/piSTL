import piSTL
import numpy as np
import pivtk

a = piSTL.read_stl('sample.stl')[0]

voxel = piSTL.algorithm.voxelization(a, 0.05).astype("float")
vtk = pivtk.geom.structured_points(voxel.shape, a.bounds[0] + 0.025, spacing = (0.05, 0.05, 0.05), point_data = [{"name": "voxel", "type": "scalar", "values": voxel}])
vtk.write("sample.vtk")