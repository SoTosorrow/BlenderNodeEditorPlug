#import numpy as np
#import open3d as o3d

# https://towardsdatascience.com/5-step-guide-to-generate-3d-meshes-from-point-clouds-with-python-36bad397d8ba

'''
input_path="testin/"
output_path="testout/"
dataname="sample_w_normals.xyz"
point_cloud= np.loadtxt(input_path+dataname,skiprows=1)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud[:,:3])
pcd.normals = o3d.utility.Vector3dVector(point_cloud[:,6:9])
pcd.colors = o3d.utility.Vector3dVector(point_cloud[:,3:6]/255)

# o3d.visualization.draw_geometries([pcd])
'''


# BPA
'''
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 3 * avg_dist
bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2]))
dec_mesh = bpa_mesh.simplify_quadric_decimation(100000)
dec_mesh.remove_degenerate_triangles()
dec_mesh.remove_duplicated_triangles()
dec_mesh.remove_duplicated_vertices()
dec_mesh.remove_non_manifold_edges()

o3d.io.write_triangle_mesh(output_path+"bpa_mesh.ply", dec_mesh)
'''

# Poisson’ reconstruction
'''
poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]
bbox = pcd.get_axis_aligned_bounding_box()
p_mesh_crop = poisson_mesh.crop(bbox)

o3d.io.write_triangle_mesh(output_path+"p_mesh_c.ply", p_mesh_crop)
'''


# open3d 可视化
'''
def lod_mesh_export(mesh, lods, extension, path):
    mesh_lods={}
    for i in lods:
        mesh_lod = mesh.simplify_quadric_decimation(i)
        o3d.io.write_triangle_mesh(path+"lod_"+str(i)+extension, mesh_lod)
        mesh_lods[i]=mesh_lod
    print("generation of "+str(i)+" LoD successful")
    return mesh_lods

my_lods = lod_mesh_export(poisson_mesh, [100000], ".ply", output_path)
my_lods = lod_mesh_export(bpa_mesh, [100000,1000], ".ply", output_path)
o3d.visualization.draw_geometries([my_lods[1000]])
'''