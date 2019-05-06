####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Blender imports
import bpy, bmesh

# Internal imports
import nmv
import nmv.scene
import nmv.mesh
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

    # Set the smoothing level
    bpy.context.object.modifiers["Subsurf"].levels = level
    bpy.context.object.modifiers["Subsurf"].use_subsurf_uv = False

    # Apply the smoothing modifier
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")


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

    # Switch to geometry or edit mode from the object mode
    bpy.ops.object.editmode_toggle()

    # Convert the face to triangles
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

    # Switch back to the object mode from the edit mode
    bpy.ops.object.editmode_toggle()


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
        Smoothing or subdivision level, by default 1.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(mesh_object)

    # Toggle from the object mode to edit mode
    bpy.ops.object.editmode_toggle()

    # Select all the vertices of the mesh
    bpy.ops.mesh.select_all(action='TOGGLE')

    # Smooth
    for i in range(level):
        bpy.ops.mesh.subdivide(smoothness=1)

    # Close all the holes in the mesh, if any
    bpy.ops.mesh.edge_face_add()

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
        Decimation ratio between 0.01 and 1.0
    """

    # If the decimation ration is not within range, skip this operation
    if 1.0 < decimation_ratio < 0.01:

        # Return
        return

    # select mesh_object1 and set it to be the active object
    nmv.scene.ops.set_active_object(mesh_object)

    # add a decimation modifier
    bpy.ops.object.modifier_add(type='DECIMATE')

    # set the decimation ratio
    bpy.context.object.modifiers["Decimate"].ratio = decimation_ratio

    # apply the modifier
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
        soma_mesh.select = True

    # Select all the branches meshes
    if len(branches_meshes) > 0:
        for branch_mesh in branches_meshes:
            branch_mesh.select = True

    # Select all the spines meshes
    if len(spines_meshes) > 0:
        for spine_mesh in spines_meshes:
            spine_mesh.select = True

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
    bpy.context.scene.objects.active = mesh_object_1

    # Get the nearest face to the starting point
    indices = nmv.mesh.ops.get_indices_of_nearest_faces_to_point_within_delta(
        mesh_object_1, connecting_point[0])
    nearest_face_index_on_mesh_1 = nmv.mesh.ops.get_index_of_nearest_face_to_point_in_faces(
        mesh_object_1, indices, connecting_point[1])

    # Select this face
    nmv.mesh.ops.select_face_vertices(mesh_object_1, nearest_face_index_on_mesh_1)

    # Deselect mesh_object_1
    mesh_object_1.select = False

    # Select mesh_object_2 and set it to be the active object
    mesh_object_2.select = True

    # Close all the open faces (including the caps) to ensure that there are no holes in the mesh
    nmv.mesh.ops.close_open_faces(mesh_object_2)

    # Get the nearest face to the bridging point
    nearest_face_index_on_mesh_2 = nmv.mesh.ops.get_index_of_nearest_face_to_point(
        mesh_object_2, connecting_point[1])

    # Select this face
    nmv.mesh.ops.select_face_vertices(mesh_object_2, nearest_face_index_on_mesh_2)

    # Select mesh_object_1 and mesh_object_2
    mesh_object_1.select = True
    mesh_object_2.select = True

    # Set the mesh_object_1 to be active
    bpy.context.scene.objects.active = mesh_object_1

    # Set tha parenting order, the parent mesh is becoming an actual parent
    bpy.ops.object.parent_set()

    # Join the two meshes in one mesh
    bpy.ops.object.join()

    # Switch to edit mode to be able to implement the bridging operator
    bpy.ops.object.editmode_toggle()

    # apply the bridging operator
    bpy.ops.mesh.bridge_edge_loops()

    # switch back to object mode
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

    # Deselect everything in the scene
    nmv.scene.ops.deselect_all()

    # Select all the sections in the sections list
    for mesh_object in mesh_list:

        if mesh_object.type == 'MESH':
            
            # Select the mesh object
            mesh_object.select = True

    # Set the 0th mesh to be active
    bpy.context.scene.objects.active = mesh_list[0]

    # Set tha parenting order, the parent mesh is becoming an actual parent
    # bpy.ops.object.parent_set()

    # Join the two meshes in one mesh
    bpy.ops.object.join()

    # Get a reference to the resulting mesh
    result_mesh = bpy.context.scene.objects.active

    # Rename it
    result_mesh.name = name

    # Return a reference to the resulting mesh
    return result_mesh
