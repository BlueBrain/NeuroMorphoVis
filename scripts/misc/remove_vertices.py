import bpy 
import bmesh 

import nmv.mesh
import nmv.bmeshi


####################################################################################################
# @create_bmesh_copy_from_mesh_object
####################################################################################################
def create_bmesh_copy_from_mesh_object(mesh_object,
                                       transform=True,
                                       triangulate=False):
                                           
    # If the given object is not mesh, assert
    assert mesh_object.type == 'MESH'

    # Get access to the mesh data
    mesh_data = mesh_object.data

    # If the mesh is in the edit mode
    if mesh_object.mode == 'EDIT':
        bm_orig = bmesh.from_edit_mesh(mesh_data)
        bmesh_object = bm_orig.copy()
    else:
        bmesh_object = bmesh.new()
        bmesh_object.from_mesh(mesh_data)

    # If we need to consider the transformation
    if transform:
        matrix = mesh_object.matrix_world.copy()
        if not matrix.is_identity:
            bmesh_object.transform(matrix)

            # Update normals if the matrix has no rotation.
            matrix.translation.zero()
            if not matrix.is_identity:
                bmesh_object.normal_update()

    # If we need to triangulate the bmesh
    if triangulate:
        bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)

    # Return a reference to the bmesh object
    return bmesh_object


####################################################################################################
# @create_bmesh_copy_from_mesh_object
####################################################################################################
def create_mesh_copy_from_bmesh_object(bmesh_object, 
                                       name):
                                           

    # Create a new mesh object and convert the bmesh object to it
    mesh = bpy.data.meshes.new(name)
    bmesh_object.to_mesh(mesh)

    # Create a blender object, link it to the scene
    mesh_object = bpy.data.objects.new(name, mesh)
    nmv.scene.link_object_to_scene(mesh_object)
    
    return mesh_object
    

# New scene 
nmv.scene.clear_scene()

# Create an object 
mesh_object_1 = nmv.mesh.create_ico_sphere(radius=1, subdivisions=3, name='mesh_object_1')

# Create a bmesh object copy 
bmesh_object_1 = create_bmesh_copy_from_mesh_object(mesh_object_1)

# Delete the first 10 vertices in mesh_object_1
vertices_indices_to_be_deleted = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
nmv.mesh.remove_vertices(mesh_object_1, vertices_indices_to_be_deleted)

# Delete the same list of vertices from the bmesh_object_1
nmv.bmeshi.remove_vertices(bmesh_object_1, vertices_indices_to_be_deleted)

# Create another mesh object from the bmesh obejct 
mesh_object_2 = create_mesh_copy_from_bmesh_object(bmesh_object_1, name='mesh_object_2')



