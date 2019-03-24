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
import bpy
from mathutils import Vector, Matrix

# Internal imports
import nmv
import nmv.scene
import nmv.mesh


####################################################################################################
# @rotate_face_in_object_towards_point
####################################################################################################
def rotate_face_in_object_towards_point(mesh_object,
                                        face,
                                        to_point):
    """Rotate a selected face in a mesh object towards certain target point.

    :param mesh_object:
        A given mesh object.
    :param face:
        The selected face in the mesh.
    :param to_point:
        The target point the face should be rotated towards.
    """

    # Get the world matrix of the object, and update the vertices of the object
    matrix_world = mesh_object.matrix_world
    for index in face.vertices:
        vertex = mesh_object.data.vertices[index]
        vertex.co = matrix_world * vertex.co

    # Compute the rotation difference and the rotation quaternion
    face_center = Vector((face.center[0], face.center[1], face.center[2]))
    track = to_point - face_center
    quaternion = face.normal.rotation_difference(track)

    # Compute the rotation matrix
    rotation_matrix = Matrix.Translation(face_center) * \
                      quaternion.to_matrix().to_4x4() * \
                      Matrix.Translation(-face_center)

    # Rotate the object
    matrix_object = matrix_world.inverted() * rotation_matrix

    # Apply the matrix to the vertices of the face
    for index in face.vertices:
        vertex = mesh_object.data.vertices[index]
        vertex.co = matrix_object * vertex.co


####################################################################################################
# @rotate_face_towards_point
####################################################################################################
def rotate_face_towards_point(mesh_object,
                              target_point):
    """Rotate a single-faced mesh object towards a target point.

    NOTE: This function will generate wrong results if the given object contains more than a single
    face, since it's always assumed to select the first face and apply the rotation operation on it.

    :param mesh_object:
        A given mesh object that has only a single face.
    :param target_point:
        The target point the mesh 'or the face' should be rotated towards.
    :return
        True or False.
    """

    # Make sure that the mesh has a single face, otherwise the results will be wrong
    if len(mesh_object.data.polygons) > 1:
        return False # Failure

    # Get the face (the only face in the mesh object)
    face = mesh_object.data.polygons[0]

    # Rotate the face
    rotate_face_in_object_towards_point(mesh_object, face, target_point)

    # Successful operation
    return True


####################################################################################################
# @convert_face_to_circle
####################################################################################################
def convert_face_to_circle(mesh_object,
                           face_index,
                           face_radius):
    """Convert the face of a mesh object from irregular shape to a circle-like pattern to make it
    clean for the extrusion.

    :param mesh_object:
        A given mesh object.
    :param face_index:
        The index of the face being mapped to a circle.
    :param face_radius:
        The given radius of the circle.
    """

    # Get a reference to the face and its centroid from the mesh data
    face = mesh_object.data.polygons[face_index]

    # Get all the vertices indices of the selected face
    vertices_indices = nmv.mesh.ops.get_faces_vertices_indices(
        mesh_object, face_index)

    # Start processing each vertex in the face
    for vertex_index in vertices_indices:

        # Get the vertex from its index
        vertex = mesh_object.data.vertices[vertex_index]

        # Compute the direction from the center to the vertex
        direction = (vertex.co - face.center).normalized()

        # Compute the mapping point along that direction and set the vertex coordinates to it
        vertex.co = face.center + direction * face_radius


####################################################################################################
# @map_face_to_circle
####################################################################################################
def map_face_to_circle(mesh_object,
                       vertices_indices,
                       mapping_circle):
    """Maps a given face in a given mesh object with the specified vertices to a circle.

    :param mesh_object:
        A given mesh object.
    :param vertices_indices:
        The indices of the vertices of the face that should be mapped.
    :param mapping_circle:
        A given circle that will be used to do the mapping operation.
    """

    # Get references to the face vertices and the circle ones
    vertices = mesh_object.data.vertices
    mapping_vertices = mapping_circle.data.vertices

    # Find the nearest vertex from the mapping circle and move the vertex to it
    for vertex_index in vertices_indices:
        shortest_distance = 10000000000
        nearest_vertex = 0
        for vertex in mapping_vertices:
            distance = (vertices[vertex_index].co - vertex.co).length
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_vertex = vertex
        vertices[vertex_index].co = nearest_vertex.co


####################################################################################################
# @extrude_face_to_face
####################################################################################################
def extrude_face_to_face(mesh_object,
                         face_index,
                         target_point):
    """Extrude a face in a mesh object specified by its face index to a given point.

    NOTE: This operation returns the index of the final extruded face.

    :param mesh_object:
        A given mesh object.
    :param face_index:
        The index of the face that will get extruded.
    :param target_point:
        A destination point where the face will be extruded to.
    :return:
        The index of the final extruded face.
    """

    # Set the selected object to be only the active one
    nmv.scene.ops.set_active_object(mesh_object)

    # Deselect all of its vertices
    nmv.mesh.ops.deselect_all_vertices(mesh_object)

    # Get the center of the face
    face_center = mesh_object.data.polygons[face_index].center

    # Compute the extrusion delta
    extrusion_delta = target_point - face_center

    # Select all the vertices of the face being extruded
    nmv.mesh.ops.select_face_vertices(mesh_object, face_index)

    # NOTE: To be able to compute the index of the extruded face, we have to count the number of
    # faces before and after the extrusion and later get the active face.
    face_count_before_extrusion = len(mesh_object.data.polygons[:])
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region={"mirror": False},
        TRANSFORM_OT_translate={"value": extrusion_delta})
    bpy.ops.object.editmode_toggle()

    # Face increase after extrusion +5
    face_count_after_extrusion = len(mesh_object.data.polygons[:])
    cap_face_index = -1
    for i in range(face_count_before_extrusion, face_count_after_extrusion):
        face = mesh_object.data.polygons[i]
        if face.select is True:
            cap_face_index = face.index
            break
    return cap_face_index


####################################################################################################
# @extrude_face_to_joint
####################################################################################################
def extrude_face_to_joint(mesh_object,
                          face_index,
                          target_point,
                          delta_ratio=0.1):
    """Extrude a face specified by its face index to a given point on a joint.

    NOTE: This operation returns a list of the indices of the extruded joint.

    :param mesh_object:
        A given mesh object.
    :param face_index:
        The index of the face that should be extruded.
    :param target_point:
        A destination point where the face will be extruded to.
    :param delta_ratio:
        Joint side length.
    :return:
        A list of the indices of the extruded joint.
    """

    # Set the selected object to be only the active one
    nmv.scene.ops.set_active_object(mesh_object)

    # Deselect all of its vertices
    nmv.mesh.ops.deselect_all_vertices(mesh_object)

    # Get the center of the face
    face_center = mesh_object.data.polygons[face_index].center

    # Compute the direction from the center of the face to the target point
    direction = (face_center - target_point).normalized()

    # Compute the cube length, and its base and cap points
    delta_distance = (face_center - target_point).length
    delta = delta_distance * delta_ratio
    base_point = target_point - direction * delta
    cap_point = target_point + direction * delta

    # First extrusion to base
    base_face_index = extrude_face_to_face(mesh_object, face_index, base_point)

    # Second extrusion to cap
    cap_face_index = extrude_face_to_face(mesh_object, base_face_index, cap_point)

    # Return a list of the indices of the joint faces
    joint_faces_indices_list = []
    for i in range(base_face_index + 1, cap_face_index + 1):
        joint_faces_indices_list.append(i)
    return joint_faces_indices_list


####################################################################################################
# @get_index_of_nearest_face_to_point_in_faces
####################################################################################################
def get_index_of_nearest_face_to_point_in_faces(mesh_object,
                                                faces_indices,
                                                point):
    """Get the index of the nearest face of an object to a given point in the space.

    :param mesh_object:
        A given mesh object.
    :param faces_indices:
        A list of indices of all the faces we need to check for.
    :param point:
        A point in the three-dimensional space.
    :return:
        The index of the nearest face in the list.
    """

    nearest_face_index = -1
    shortest_distance = 10000000000
    for face_index in faces_indices:
        face = mesh_object.data.polygons[face_index]
        face_center = Vector((face.center[0], face.center[1], face.center[2]))
        distance = (face_center - point).length
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_face_index = face.index
    return nearest_face_index


####################################################################################################
# @get_index_of_nearest_face_to_point
####################################################################################################
def get_index_of_nearest_face_to_point(mesh_object,
                                       point):
    """Get the index of the nearest face of an object to a given point in the space.

    :param mesh_object:
        A given mesh object.
    :param point:
        A point in the three-dimensional space.
    :return:
        The index of the nearest face in the given mesh object to the point.
    """

    nearest_face_index = -1
    shortest_distance = 10000000000
    for face in mesh_object.data.polygons:
        face_center = Vector((face.center[0], face.center[1], face.center[2]))
        distance = (face_center - point).length
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_face_index = face.index
    return nearest_face_index


####################################################################################################
# @get_index_of_nearest_face_to_point
####################################################################################################
def get_indices_of_nearest_faces_to_point_within_delta(mesh_object,
                                                       point,
                                                       delta=0.2):
    """Get the indices of the nearest faces to point within a given range.

    :param mesh_object:
        A given mesh object.
    :param point:
        A point in the three-dimensional space.
    :param delta:
        Delta value.
    :return:
        A list of indices of faces.
    """

    nearest_face_index = get_index_of_nearest_face_to_point(mesh_object, point)

    indices = list()

    # Compute the distance between the nearest face and the given point
    x_distance = (mesh_object.data.polygons[nearest_face_index].center - point).length + delta

    # Get the faces
    for face in mesh_object.data.polygons:
        face_center = Vector((face.center[0], face.center[1], face.center[2]))
        distance = (face_center - point).length

        if distance < x_distance:
            indices.append(face.index)

    return indices


####################################################################################################
# @smooth_faces
####################################################################################################
def subdivide_faces(mesh_object,
                    faces_indices,
                    cuts=1):
    """Subdivide a set of faces defined by their indices into multiple cuts.

    :param mesh_object:
        A given mesh object.
    :param faces_indices:
        A list of the indices of the faces.
    :param cuts:
        Number of cuts, by default set to 1.
    """

    # Set the selected object to be only the active one
    nmv.scene.ops.set_active_object(mesh_object)

    # Deselect all of its vertices
    nmv.mesh.ops.deselect_all_vertices(mesh_object)

    # For each face in the input faces list, select all of its vertices
    for face_index in faces_indices:
        nmv.mesh.ops.select_face_vertices(mesh_object, face_index)

    # Switch to edit mode
    bpy.ops.object.editmode_toggle()

    # Subdivide the selected vertices
    bpy.ops.mesh.subdivide(number_cuts=cuts, smoothness=0)

    # Switch back to the object mode
    bpy.ops.object.editmode_toggle()


####################################################################################################
# @close_open_faces
####################################################################################################
def close_open_faces(mesh_object):
    """Close all the open faces of a mesh object.

    :param mesh_object:
        A given mesh object.
    """

    # Select all the vertices of a mesh object
    nmv.mesh.ops.select_all_vertices(mesh_object)

    # Toggle the mesh object to the edit/object mode
    bpy.ops.object.editmode_toggle()

    # Add new faces for the selected vertices if there are any open faces
    bpy.ops.mesh.edge_face_add()

    # Switch back to the edit more
    bpy.ops.object.editmode_toggle()

    # Deselect all the vertices again for the other side
    nmv.mesh.ops.deselect_all_vertices(mesh_object)


####################################################################################################
# @close_open_faces
####################################################################################################
def try_to_close_open_faces(mesh_object):
    """Tries to close all the open faces of a mesh object. This function was to give a try with
    functions that we don't care about the certainty of the application of the operation.

    :param mesh_object:
        A given mesh object.
    """

    # Select all the vertices of a mesh object
    nmv.mesh.ops.select_all_vertices(mesh_object)

    # Toggle the mesh object to the edit/object mode
    bpy.ops.object.editmode_toggle()

    # Add new faces for the selected vertices if there are any open faces
    try:
        bpy.ops.mesh.edge_face_add()
    except:
        pass

    # Switch back to the edit more
    bpy.ops.object.editmode_toggle()

    # Deselect all the vertices again for the other side
    nmv.mesh.ops.deselect_all_vertices(mesh_object)


####################################################################################################
# @close_caps_for_4_vertices_mesh
####################################################################################################
def close_caps_for_4_vertices_mesh(mesh_object):
    """Close all the open faces of a mesh object.

    :param mesh_object:
        A given mesh object.
    """

    # Deselect all the vertices of the mesh object
    nmv.mesh.ops.deselect_all_vertices(mesh_object)

    # Select the first and last four vertices
    vertices_indices = [0, 1, 2, 3, -1, -2, -3, -4]
    nmv.mesh.ops.select_vertices(mesh_object, vertices_indices)

    # Switch to edit mode
    bpy.ops.object.editmode_toggle()

    # Add a new face for the selected vertices
    bpy.ops.mesh.edge_face_add()

    # Smooth, to avoid crappy endings after the wholistic smoothing operation
    # bpy.ops.mesh.subdivide(number_cuts=1)

    # Switch back to the edit more
    bpy.ops.object.editmode_toggle()

    # Deselect all the vertices again for the other side
    # mesh_vertex_ops.deselect_all_vertices(mesh_object)


####################################################################################################
# @close_caps_for_4_vertices_mesh
####################################################################################################
def close_caps_for_n_vertices(mesh_object,
                              n):
    """Close the caps for a mesh based on n-vertex polygon.

    :param mesh_object:
        A given mesh object.
    :param n:
        The number of vertices of the base polygon of the mesh.
    """

    # Deselect all the vertices of the mesh object
    nmv.mesh.ops.deselect_all_vertices(mesh_object)

    # Select the first and last four vertices
    vertices_indices = []
    for i in range(n):
        vertices_indices.append(i)

    number_vertices = len(mesh_object.data.vertices)
    for i in range(n):
        vertices_indices.append(number_vertices - i - 1)

    # Select the vertices
    nmv.mesh.ops.select_vertices(mesh_object, vertices_indices)

    # Switch to edit mode
    bpy.ops.object.editmode_toggle()

    # Add a new face for the selected vertices
    bpy.ops.mesh.edge_face_add()

    # Switch back to the edit more
    bpy.ops.object.editmode_toggle()


####################################################################################################
# @remove_first_face_of_quad_mesh_object
####################################################################################################
def remove_first_face_of_quad_mesh_object(mesh_object):
    """Close the first face of the given mesh object.

    :param mesh_object:
        A quad mesh object.
    """

    # Deselect all the vertices of the mesh object
    nmv.mesh.ops.deselect_all_vertices(mesh_object)

    # Select the first and last four vertices
    vertices_indices = [0, 1, 2, 3]

    # Select the vertices
    nmv.mesh.ops.select_vertices(mesh_object, vertices_indices)

    # Switch to edit mode
    bpy.ops.object.editmode_toggle()

    # Delete the face
    bpy.ops.mesh.delete(type='FACE')

    # Switch back to the edit more
    bpy.ops.object.editmode_toggle()
