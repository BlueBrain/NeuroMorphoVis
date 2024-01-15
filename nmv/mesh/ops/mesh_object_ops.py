####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################

# System imports
import random

# Blender imports
import bpy
import bmesh
import mathutils
from mathutils import Matrix

# Internal imports
import nmv.scene
import nmv.mesh
import nmv.bmeshi
import nmv.utilities


####################################################################################################
# @convert_to_bmesh_object
####################################################################################################
def convert_to_bmesh_object(mesh_object):
    """Convert the mesh object to a bmesh object and returns a reference to it.

    :param mesh_object:
        A given mesh object.
    :return:
        A reference to the created bmesh object.
    """

    # Create a new bmesh object
    bmesh_object = bmesh.new()

    # Convert the mesh object to a bmesh object
    bmesh_object.from_mesh(mesh_object.data)

    # Return a reference to the bmesh object
    return bmesh_object


####################################################################################################
# @smooth_object
####################################################################################################
def smooth_object(mesh_object,
                  level=1):
    """Smooth a mesh object.

    :param mesh_object:
        A given mesh object.
    :param level:
        Smoothing or subdivision level, by default 1.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(mesh_object)

    # Add a smoothing modifier
    bpy.ops.object.modifier_add(type='SUBSURF')

    if nmv.utilities.is_blender_280():

        # Set the smoothing level
        bpy.context.object.modifiers["Subdivision"].levels = level
        # bpy.context.object.modifiers["Subdivision"].use_subsurf_uv = False

        # Apply the smoothing modifier
        if nmv.utilities.is_blender_290():
            bpy.ops.object.modifier_apply(modifier="Subdivision")
        else:
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
    else:

        # Set the smoothing level
        bpy.context.object.modifiers["Subsurf"].levels = level

        # Apply the smoothing modifier
        if nmv.utilities.is_blender_290():
            bpy.ops.object.modifier_apply(modifier="Subsurf")
        else:
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")


####################################################################################################
# @randomize_surface
####################################################################################################
def randomize_surface(mesh_object,
                      offset=0.1,
                      iterations=1):
    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(mesh_object)

    # Toggle from the object mode to edit mode
    bpy.ops.object.editmode_toggle()

    # Select all the vertices of the mesh
    bpy.ops.mesh.select_all(action='SELECT')

    # Randomize the vertex
    for i in range(iterations):
        bpy.ops.transform.vertex_random(offset=offset)

    # Toggle from the edit mode to the object mode
    bpy.ops.object.editmode_toggle()


####################################################################################################
# @triangulate_mesh
####################################################################################################
def triangulate_mesh(mesh_object):
    """Convert the faces of a given mesh into triangles.

    :param mesh_object:
        A given mesh object.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(mesh_object)

    # Add the modifier
    bpy.ops.object.modifier_add(type='TRIANGULATE')

    # Apply the modifier
    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Triangulate")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Triangulate")


####################################################################################################
# @shade_smooth_object
####################################################################################################
def shade_smooth_object(mesh_object):
    """Smooth a given mesh object using the 'faces_shade_smooth' operator.

    :param mesh_object: A given mesh object.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(mesh_object)

    # Switch to geometry or edit mode from the object mode
    bpy.ops.object.editmode_toggle()

    # Select all the vertices of the mesh object
    bpy.ops.mesh.select_all(action='SELECT')

    # Apply a smoothing operator
    bpy.ops.mesh.faces_shade_smooth()

    # Switch back to the object mode from the edit mode
    bpy.ops.object.editmode_toggle()


####################################################################################################
# @smooth_object_vertices
####################################################################################################
def smooth_object_vertices(mesh_object,
                           level=1):
    """Smooth the vertices of the mesh object.

    :param mesh_object:
        A given mesh object.
    :param level:
        Smoothing or subdivision level or number of iterations, by default 1.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(mesh_object)

    # Select the SMOOTH modifier
    bpy.ops.object.modifier_add(type='SMOOTH')

    # Update the number of iterations
    bpy.context.object.modifiers["Smooth"].iterations = level

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier="Smooth")


####################################################################################################
# @adjust_normals
####################################################################################################
def adjust_normals(mesh_object):
    """Adjust the normals of a given mesh object.

    :param mesh_object:
        A given mesh in the scene.
    """
    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(mesh_object)

    # Toggle from the object mode to edit mode
    bpy.ops.object.editmode_toggle()

    # Select all the vertices of the mesh
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.normals_make_consistent(inside=False)

    # Toggle from the edit mode to the object mode
    bpy.ops.object.editmode_toggle()


####################################################################################################
# @decimate_mesh_object
####################################################################################################
def decimate_mesh_object(mesh_object,
                         decimation_ratio=1.0):
    """Decimate a mesh object.

    :param mesh_object:
        A given mesh object.
    :param decimation_ratio:
        Decimation ratio.
    """

    # If the decimation ration is not within range, skip this operation
    if decimation_ratio < 0.00001:

        # Return
        return

    # select mesh_object1 and set it to be the active object
    nmv.scene.ops.set_active_object(mesh_object)

    # add a decimation modifier
    bpy.ops.object.modifier_add(type='DECIMATE')

    # set the decimation ratio
    bpy.context.object.modifiers["Decimate"].ratio = decimation_ratio

    # Apply the modifier
    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Decimate")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")


####################################################################################################
# @smooth_object
####################################################################################################
def joint_meshes(soma_mesh=None,
                 branches_meshes=[],
                 spines_meshes=[]):

    """Join all the meshes of a neuron into a single mesh.

    NOTE: This function takes a distinct mesh for the soma, and a list of meshes for the arbors
    or the branches and another list for the spines.
    TODO: Rename the function to specify it to neurons.

    :param soma_mesh:
        The mesh of the soma.
    :param branches_meshes:
        A list of the meshes of all the bracnes.
    :param spines_meshes:
        A list of the meshes of the spines.
    :return:
        A single mesh object.
    """

    # Create a very small sphere to be used as the base object
    base_object = nmv.mesh.objects.create_uv_sphere(radius=0.01, subdivisions=4, name='mesh')

    # Set this base sphere as the active object
    nmv.scene.ops.set_active_object(base_object)

    # Select the soma mesh if not None
    if soma_mesh is not None:
        nmv.scene.select_object(soma_mesh)

    # Select all the branches meshes
    if len(branches_meshes) > 0:
        for branch_mesh in branches_meshes:
            nmv.scene.select_object(branch_mesh)

    # Select all the spines meshes
    if len(spines_meshes) > 0:
        for spine_mesh in spines_meshes:
            nmv.scene.select_object(spine_mesh)

    # Join the meshes together
    bpy.ops.object.join()

    # Return a reference to the final object.
    return base_object


####################################################################################################
# @union
####################################################################################################
def clip_mesh_object(primary_object,
                     secondary_object):
    """Apply a boolean union operator on the two meshes to make them only one mesh object.


    NOTE: This functions assumes that mesh_object1 to be the base and the other object will be
    deleted after the application of the union operator.

    :param primary_object:
        The primary object of the union operation.
    :param secondary_object:
        The secondary object of the union operation.
    :return:
        A reference to the primary object.
    """

    # Select mesh_object1 and set it to be the active object
    nmv.scene.ops.set_active_object(primary_object)

    # Add a boolean modifier
    bpy.ops.object.modifier_add(type='BOOLEAN')

    # Select the other mesh object (mesh_object2)
    bpy.context.object.modifiers["Boolean"].object = secondary_object

    # Set the difference operator
    bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'

    # Apply the union operator
    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Boolean")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

    # Return the final mesh object, 'a reference to mesh_object1'
    return primary_object


####################################################################################################
# @transform_mesh
####################################################################################################
def transform_mesh(mesh_object,
                   transformation_matrix):
    """Transform a mesh object by a given transformation.

    :param mesh_object:
        A given mesh object.
    :param transformation_matrix:
        Transformation matrix.
    """

    # Get all the vertices of the mesh object
    vertices = mesh_object.data.vertices[:]

    # Apply the transformation vertex by vertex
    for vertex in vertices:
        vertex.co = transformation_matrix * vertex.co


####################################################################################################
# @bridge_mesh_objects
####################################################################################################
def bridge_mesh_objects(mesh_object_1,
                        mesh_object_2,
                        connecting_point):
    """Bridge two mesh objects at a given point.

    :param mesh_object_1:
        A reference to the first mesh object.
    :param mesh_object_2:
        A reference to the second mesh object.
    :param connecting_point:
        A reference to the connecting point where the bringing should happen.
    :return:
        A reference to the resulting mesh after the bridging operation.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Select mesh_object_1 and set it to be the active object
    nmv.scene.set_active_object(mesh_object_1)

    # Get the nearest face to the starting point
    indices = nmv.mesh.ops.get_indices_of_nearest_faces_to_point_within_delta(
        mesh_object_1, connecting_point[0])
    nearest_face_index_on_mesh_1 = nmv.mesh.ops.get_index_of_nearest_face_to_point_in_faces(
        mesh_object_1, indices, connecting_point[1])

    # Select this face
    nmv.mesh.ops.select_face_vertices(mesh_object_1, nearest_face_index_on_mesh_1)

    # Deselect mesh_object_1
    nmv.scene.deselect_object(mesh_object_1)

    # Select mesh_object_2 and set it to be the active object
    nmv.scene.select_object(mesh_object_2)

    # Close all the open faces (including the caps) to ensure that there are no holes in the mesh
    nmv.mesh.ops.close_open_faces(mesh_object_2)

    # Get the nearest face to the bridging point
    nearest_face_index_on_mesh_2 = nmv.mesh.ops.get_index_of_nearest_face_to_point(
        mesh_object_2, connecting_point[1])

    # Select this face
    nmv.mesh.ops.select_face_vertices(mesh_object_2, nearest_face_index_on_mesh_2)

    # Select mesh_object_1 and mesh_object_2
    nmv.scene.select_object(mesh_object_1)
    nmv.scene.select_object(mesh_object_2)

    # Set the mesh_object_1 to be active
    nmv.scene.set_active_object(mesh_object_1)

    # Set tha parenting order, the parent mesh is becoming an actual parent
    bpy.ops.object.parent_set()

    # Join the two meshes in one mesh
    bpy.ops.object.join()

    # Switch to edit mode to be able to implement the bridging operator
    bpy.ops.object.editmode_toggle()

    # Apply the bridging operator
    bpy.ops.mesh.bridge_edge_loops()

    # Switch back to object mode
    bpy.ops.object.editmode_toggle()

    # Deselect all the vertices of the parent mesh, mesh_object_1
    nmv.mesh.ops.deselect_all_vertices(mesh_object_1)


####################################################################################################
# @bridge_mesh_objects_in_list
####################################################################################################
def bridge_mesh_objects_in_list(mesh_objects_list,
                                connecting_points_list):
    """Bridge a list of meshes and construct a single object out of them.

    :param mesh_objects_list:
        A list of mesh objects to be bridged.
    :param connecting_points_list:
        A list of the corresponding connection points.
    :return:
        A reference to the final mesh.
    """

    # Select the primary mesh object to be the first in the list
    mesh_object_1 = mesh_objects_list[0]

    # Close the faces of this primary object s
    nmv.mesh.ops.close_open_faces(mesh_object_1)

    # Iterate over all the secondary meshes and bridge them to the primary mesh
    for i in range(len(mesh_objects_list) - 1):

        # Get a reference to mesh_object_2
        mesh_object_2 = mesh_objects_list[i + 1]

        # Get the connecting point
        connecting_point = connecting_points_list[i + 1]

        # Bridge the meshes
        bridge_mesh_objects(mesh_object_1, mesh_object_2, connecting_point)

    # The resulting mesh is simply the first one in the mesh_objects_list
    return mesh_object_1


####################################################################################################
# @union_mesh_objects
####################################################################################################
def union_mesh_objects(mesh_object_1,
                       mesh_object_2):
    """Apply a boolean union operator on the two meshes to make them only one mesh object.

    NOTE: This functions assumes that mesh_object1 to be the base and the other object will be
    deleted after the application of the union operator.

    :param mesh_object_1:
        A reference to the first mesh object.
    :param mesh_object_2:
        A reference to the second mesh object.
    :return:
    The union of the two mesh objects.
    """

    # select mesh_object1 and set it to be the active object
    nmv.scene.ops.set_active_object(mesh_object_1)

    # add a boolean modifier
    bpy.ops.object.modifier_add(type='BOOLEAN')

    # select the other mesh object (mesh_object2)
    bpy.context.object.modifiers["Boolean"].object = mesh_object_2

    # set the union operator
    bpy.context.object.modifiers["Boolean"].operation = 'UNION'

    # apply the union operator
    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Boolean")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

    # return the final mesh object, 'a reference to mesh_object1'
    return mesh_object_1


####################################################################################################
# @union_mesh_objects_in_list
####################################################################################################
def union_mesh_objects_in_list(mesh_objects_list):
    """Union a list of mesh objects into a single mesh.
    :param mesh_objects_list:
        A list of mesh objects to be merged into a single mesh relying on the union operator.
    :return:
        The final mesh resulting from the union operator.
    """

    # Use the first mesh in the list to be the primary one
    mesh_object_1 = mesh_objects_list[0]

    # Ensure that the list has more than a single mesh to proceed.
    if len(mesh_objects_list) == 1:
        return mesh_object_1

    # Apply the union operator on all the other meshes in the list
    for i in range(1, len(mesh_objects_list)):

        # Show progress
        nmv.utilities.time_line.show_iteration_progress('Union', i, len(mesh_objects_list))

        # Union the ith mesh object
        mesh_object_1 = union_mesh_objects(mesh_object_1, mesh_objects_list[i])

        # Switch to edit mode to REMOVE THE DOUBLES
        # TODO: Use the remove doubles function
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()

        # Delete the other mesh
        nmv.scene.ops.delete_list_objects([mesh_objects_list[i]])

    # Report the progress
    nmv.utilities.time_line.show_iteration_progress(
        'Union', len(mesh_objects_list), len(mesh_objects_list), done=True)

    # TODO: handle the case when this operation fails.

    # Return a reference to the final mesh
    return mesh_object_1


################################################################################
# @intersect_mesh_objects
################################################################################
def intersect_mesh_objects(mesh_object1,
                           mesh_object2):
    """Apply a boolean union operator on the two meshes to make them only one mesh object.

    NOTE: This functions assumes that mesh_object1 to be the base and the other object will be
    delete after the application of the union operator.

    :param mesh_object1:
        The first mesh object.
    :param mesh_object2:
        The second mesh object.
    :return:
        The final mesh object after the intersection operation.
    """

    # Select mesh_object1 and set it to be the active object
    nmv.scene.ops.set_active_object(mesh_object1)

    # Add a boolean modifier
    bpy.ops.object.modifier_add(type='BOOLEAN')

    # Select the other mesh object (mesh_object2)
    bpy.context.object.modifiers["Boolean"].object = mesh_object2

    # Set the union operator
    bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'

    # Apply the intersection operator
    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Boolean")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

    # Return the final mesh object, 'a reference to mesh_object1'
    return mesh_object1


####################################################################################################
# @join_mesh_objects
####################################################################################################
def join_mesh_objects(mesh_list,
                      name='joint'):
    """Join all the meshes into one only and rename it.

    :param mesh_list:
        An input list of meshes to be joint.
    :param name:
        The name of the outcome.
    :return:
        A joint mesh.
    """

    # If the input list does not contain any meshes, return None
    if len(mesh_list) == 0:
        return None

    # If the input list contains only one mesh, return a reference to it
    if len(mesh_list) == 1:
        return mesh_list[0]

    # Switch to the object mode
    # bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect everything in the scene
    nmv.scene.ops.deselect_all()

    # Set the 0th mesh to be active
    nmv.scene.set_active_object(mesh_list[0])

    # Select all the sections in the sections list
    for mesh_object in mesh_list:

        # Ensure that this mesh object is not None
        if mesh_object is not None:

            # Must be only mesh
            if mesh_object.type == 'MESH':

                # Select the mesh object
                nmv.scene.select_object(mesh_object)

    # Set tha parenting order, the parent mesh is becoming an actual parent
    # bpy.ops.object.parent_set()

    # Join the selected meshes in one mesh
    bpy.ops.object.join()

    # Get a reference to the resulting mesh
    result_mesh = nmv.scene.get_active_object()

    # Rename it
    result_mesh.name = name

    # Update the parent mesh to the resulting one
    mesh_list[0] = result_mesh

    # Return a reference to the resulting mesh
    return result_mesh


####################################################################################################
# @subdivide_mesh
####################################################################################################
def subdivide_mesh(mesh_object,
                   level):
    """Subdivide the mesh.

    :param mesh_object:
        A given mesh object to subdivide.
    :param level:
        Subdivision level.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(mesh_object)

    # Toggle from the object mode to edit mode
    bpy.ops.object.editmode_toggle()

    # Select all the vertices of the mesh
    bpy.ops.mesh.select_all(action='SELECT')

    # Smooth
    for i in range(level):
        if nmv.utilities.is_blender_280():
            bpy.ops.mesh.subdivide(quadcorner='INNERVERT')
        else:
            bpy.ops.mesh.subdivide(smoothness=1)

    # Toggle from the edit mode to the object mode
    bpy.ops.object.editmode_toggle()


####################################################################################################
# @add_surface_noise_to_mesh_using_displacement_modifier
####################################################################################################
def add_surface_noise_to_mesh_using_displacement_modifier(mesh_object,
                                                          strength=1.0,
                                                          noise_scale=2.0,
                                                          noise_depth=2):

    # Deselect everything in the scene
    nmv.scene.ops.deselect_all()

    # Set the 0th mesh to be active
    nmv.scene.set_active_object(mesh_object)

    # Create a displacement modifier
    displacement_modifier = mesh_object.modifiers.new(name="Displace", type='DISPLACE')

    # Add a new texture for the modifier
    displacement_modifier.texture = bpy.data.textures.new(
        name='Surface Noise [%s]' % mesh_object.name, type='CLOUDS')

    # Select a PERLIN noise
    displacement_modifier.texture.noise_basis = 'ORIGINAL_PERLIN'

    # Update the noise parameters
    displacement_modifier.strength = strength
    displacement_modifier.texture.noise_scale = noise_scale
    displacement_modifier.texture.noise_depth = int(noise_depth)

    # Apply the modifiers
    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Displace")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")


####################################################################################################
# @add_surface_noise_to_mesh_using_displacement_modifier
####################################################################################################
def enlarge_mesh_using_displacement_modifier(mesh_object,
                                             enlargement_factor=0.1):
    # Deselect everything in the scene
    nmv.scene.ops.deselect_all()

    # Set the 0th mesh to be active
    nmv.scene.set_active_object(mesh_object)

    # Create a displacement modifier
    displacement_modifier = mesh_object.modifiers.new(name="Displace", type='DISPLACE')

    # Update the enlargement factor
    displacement_modifier.mid_level = 0.9

    # Apply the modifiers
    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Displace")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")


####################################################################################################
# @add_light_surface_noise
####################################################################################################
def add_light_surface_noise(mesh_object):

    # Deselect everything in the scene
    nmv.scene.ops.deselect_all()

    # Set the 0th mesh to be active
    nmv.scene.set_active_object(mesh_object)

    # Create a displacement modifier
    displacement_modifier = mesh_object.modifiers.new(name="Displace", type='DISPLACE')

    # Add a new texture for the modifier
    displacement_modifier.texture = bpy.data.textures.new(
        name='LightSurfaceNoise%s' % mesh_object.name, type='CLOUDS')

    # Noise strength
    displacement_modifier.strength = 1.0

    # Texture details
    displacement_modifier.texture.noise_scale = 1.5
    displacement_modifier.texture.noise_scale = 2
    displacement_modifier.texture.noise_depth = 30
    displacement_modifier.texture.nabla = 0.1
    displacement_modifier.texture.noise_basis = 'IMPROVED_PERLIN'

    # Apply the modifiers
    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Displace")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")


####################################################################################################
# @add_surface_noise_to_mesh
####################################################################################################
def add_surface_noise_to_mesh(mesh_object,
                              noise_strength=1.0,
                              subdivision_level=1):

    # Subdivide the surface
    #if subdivision_level > 0:
    #    subdivide_mesh(mesh_object=mesh_object, level=subdivision_level)

    # Adding the noise
    add_surface_noise_to_mesh_using_displacement_modifier(mesh_object=mesh_object,
                                                          strength=noise_strength)


####################################################################################################
# @apply_default_remesh_modifier
####################################################################################################
def apply_default_remesh_modifier(mesh_object,
                                  octree_depth=4,
                                  smooth=True):
    """Applies the default mesh modifier in Blender to a given mesh.

    :param mesh_object:
        Input mesh to be remeshed.
    :param octree_depth:
        The depth of the octree, default 4.
    :param smooth:
        Do you want a smooth surface or not.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(mesh_object)

    # Construct the modifier
    bpy.ops.object.modifier_add(type='REMESH')

    # Set the octree depth
    bpy.context.object.modifiers["Remesh"].octree_depth = octree_depth

    # Smooth the surface
    if smooth:
        bpy.context.object.modifiers["Remesh"].mode = 'SMOOTH'
        bpy.context.object.modifiers["Remesh"].use_smooth_shade = True

    # Apply the operator
    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Remesh")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")


####################################################################################################
# @apply_quadriflow_remesh_modifier
####################################################################################################
def apply_quadriflow_remesh_modifier(mesh_object,
                                     target_ratio=1.0):
    """Applies the default mesh modifier in Blender to a given mesh.
    NOTE: This function works only with Blender 2.8 onwards.

    :param mesh_object:
        Input mesh to be re-meshed.
    :param target_ratio:
        The ration of the number of triangles in the resulting mesh compared to the input one.
    """

    # Verify the Blender version
    if nmv.utilities.is_blender_280() or nmv.utilities.is_blender_290():

        # Deselect all the objects in the scene
        nmv.scene.ops.deselect_all()

        # Activate the selected object
        nmv.scene.ops.set_active_object(mesh_object)

        bpy.ops.object.quadriflow_remesh(
            use_paint_symmetry=False, mode='RATIO', target_ratio=target_ratio,
            seed=random.randint(1, 100))


####################################################################################################
# @remove_small_partitions
####################################################################################################
def remove_small_partitions(mesh_object):
    """Detects the number of partitions (or islands) in the mesh object and removes the small ones.

    :param mesh_object:
        A given mesh object to process.
    """

    # Get the paths along the edges of the mesh
    paths = {v.index: set() for v in mesh_object.data.vertices}
    for e in mesh_object.data.edges:
        paths[e.vertices[0]].add(e.vertices[1])
        paths[e.vertices[1]].add(e.vertices[0])

    # A list that will contain the different partitions in the mesh. Each partition will be
    # represented by a list of indices of the vertices of that partition.
    partitions_vertices_indices = list()

    # Search
    while True:

        # Get the next path
        try:
            iterator = next(iter(paths.keys()))
        except StopIteration:
            break
        partition = {iterator}
        current = {iterator}
        while True:
            eligible = {sc for sc in current if sc in paths}
            if not eligible:
                break
            current = {ve for sc in eligible for ve in paths[sc]}
            partition.update(current)
            for key in eligible:
                paths.pop(key)

        # Add
        partitions_vertices_indices.append(partition)

    # Convert the set to a list
    partitions_vertices_indices = list(partitions_vertices_indices)

    # Sort it
    partitions_vertices_indices.sort()

    # Select all the vertices of the small partitions
    for i in range(1, len(partitions_vertices_indices)):

        # Remove the vertices of the small partitions
        nmv.mesh.remove_vertices(
            mesh_object=mesh_object, vertices_indices=partitions_vertices_indices[i])


####################################################################################################
# @create_wire_frame
####################################################################################################
def create_wire_frame(mesh_object,
                      wireframe_thickness=0.02):
    """Creates a wireframe model for a given mesh

    :param mesh_object:
        A give mesh object.
    :param wireframe_thickness:
        Wireframe thickness.
    :return:
        A reference to the created wireframe mesh.
    """

    # Duplicate the mesh
    duplicated_mesh = nmv.scene.duplicate_object(
        original_object=mesh_object, duplicated_object_name='%s-wireframe' % mesh_object.name)

    # Make sure to deselect all the objects
    nmv.scene.deselect_all()

    # Select the duplicate mesh
    nmv.scene.select_object(scene_object=duplicated_mesh)

    # Activate the duplicate mesh
    nmv.scene.set_active_object(scene_object=duplicated_mesh)

    # Apply the wireframe operator
    bpy.ops.object.modifier_add(type='WIREFRAME')

    # Adjust the thickness
    bpy.context.object.modifiers["Wireframe"].thickness = wireframe_thickness

    # Set the even-offset to False
    # NOTE THis is important to avoid any artifacts in the resulting wireframe mesh
    bpy.context.object.modifiers["Wireframe"].use_even_offset = False

    # Apply the modifier
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Wireframe")

    # Return a reference to the wireframe object
    return duplicated_mesh


####################################################################################################
# @set_mesh_origin
####################################################################################################
def set_mesh_origin(mesh_object,
                    coordinate):
    """Sets the origin of the given mesh object to a specific coordinate.

    :param mesh_object:
        The given mesh object.
    :param coordinate:
        The coordinates of the new origin in mathutils::Vector format
    """

    # Compute the transform that accounts for the difference
    transform = Matrix.Translation(coordinate - mesh_object.location)

    # Update the location to the given coordinate
    mesh_object.location = coordinate

    # Apply the transform
    mesh_object.data.transform(transform.inverted())

    # Update the mesh object
    mesh_object.data.update()


####################################################################################################
# @apply_voxelization_remeshing_modifier
####################################################################################################
def apply_voxelization_remeshing_modifier(mesh_object,
                                          voxel_size=0.1):
    """Apply the voxelization-based remeshing algorithm to the given mesh object to create a
    connected mesh.

    :param mesh_object:
        A given mesh object to remesh.
    :param voxel_size:
        The size of the voxel represents the resolution of the grid. It should be set to the
        radius of the smallest element - or edge - in the mesh object
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(mesh_object)

    # Add the REMESH modifier to the scene
    bpy.ops.object.modifier_add(type='REMESH')

    # Ensure that it is the voxelization-based one
    bpy.context.object.modifiers["Remesh"].mode = 'VOXEL'

    # Update the voxel size
    bpy.context.object.modifiers["Remesh"].voxel_size = voxel_size

    # Use smooth shading 
    bpy.context.object.modifiers["Remesh"].use_smooth_shade = True

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier="Remesh")


####################################################################################################
# @check_self_intersections_of_mesh_object
####################################################################################################
def check_self_intersections_of_mesh_object(mesh_object):
    """Checks if the given mesh object has self-intersecting faces or not.

    :param mesh_object:
        AN input mesh object.
    :return:
        A list containing the indices of the self-intersecting faces. If this list is empty, then
        the mesh has no self-intersections.
    """

    # If the input object does not contain any polygons, return an empty list
    if not mesh_object.data.polygons:
        return []

    # Create the bmesh object
    bmesh_object = nmv.bmeshi.create_bmesh_copy_from_mesh_object(
        mesh_object=mesh_object, transform=False, triangulate=False)

    # Construct the BVHTree from the bmesh object
    tree = mathutils.bvhtree.BVHTree.FromBMesh(bmesh_object, epsilon=0.00001)

    # Check if any overlaps exist
    overlap = tree.overlap(tree)

    # Obtain a list of self-intersecting faces
    faces_error = {i for i_pair in overlap for i in i_pair}
    faces_error = list(faces_error)

    # Delete the bmesh object
    nmv.bmeshi.delete_bmesh(bmesh_object=bmesh_object)

    # Return a list of the indices of the self intersecting faces
    return faces_error


####################################################################################################
# @remove_loose
####################################################################################################
def remove_loose(mesh_object):
    """Remove the loose objects from a given mesh object.

    :param mesh_object:
        An input mesh object.
    """

    # Deselect all the objects in the scene
    nmv.scene.deselect_all()

    # Select the object
    nmv.scene.select_object(mesh_object)
    nmv.scene.set_active_object(mesh_object)

    # Switch to edit mode to be able to implement the bridging operator
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all vertices
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='SELECT')

    # Delete the loose objects in the mesh
    bpy.ops.mesh.delete_loose()

    # Deselect
    bpy.ops.mesh.select_all(action='DESELECT')

    # Switch to edit mode to be able to implement the bridging operator
    bpy.ops.object.mode_set(mode='OBJECT')


####################################################################################################
# @detect_non_manifold_vertices_of_mesh_object
####################################################################################################
def detect_non_manifold_vertices_of_mesh_object(mesh_object):
    """Detects non-manifold vertices of a mesh object.

    :param mesh_object:
        An input mesh object.
    """

    # Create a bmesh object from the given mesh object
    bmesh_object = nmv.bmeshi.create_bmesh_copy_from_mesh_object(
        mesh_object, transform=False, triangulate=False)

    # Create a list of the non-manifold vertices in the mesh
    vertices_non_manifold = [ele for i, ele in enumerate(bmesh_object.verts) if not ele.is_manifold]

    # Return the resulting list
    return vertices_non_manifold


####################################################################################################
# @get_partitions
####################################################################################################
def get_partitions(mesh_object):
    """Detects the number of partitions (or islands) in the mesh object.

    :param mesh_object:
        A given mesh object to process.
    """

    # Get the paths along the edges of the mesh
    paths = {v.index: set() for v in mesh_object.data.vertices}
    for e in mesh_object.data.edges:
        paths[e.vertices[0]].add(e.vertices[1])
        paths[e.vertices[1]].add(e.vertices[0])

    # A list that will contain the different partitions in the mesh. Each partition will be
    # represented by a list of indices of the vertices of that partition.
    partitions_vertices_indices = list()

    # Search
    while True:

        # Get the next path
        try:
            iterator = next(iter(paths.keys()))
        except StopIteration:
            break
        partition = {iterator}
        current = {iterator}
        while True:
            eligible = {sc for sc in current if sc in paths}
            if not eligible:
                break
            current = {ve for sc in eligible for ve in paths[sc]}
            partition.update(current)
            for key in eligible:
                paths.pop(key)

        # Add
        partitions_vertices_indices.append(partition)

    # Convert the set to a list
    return list(partitions_vertices_indices)