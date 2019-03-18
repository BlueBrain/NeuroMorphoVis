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

# System imports
import math

# Blender imports
import bmesh
from mathutils import Vector, Matrix

# Internal imports
import nmv
import nmv.consts
import nmv.geometry


####################################################################################################
# @get_face_from_index
####################################################################################################
def get_face_from_index(bmesh_object,
                        face_index):
    """Gets a face using its index.

    :param bmesh_object:
        A given bmesh object.
    :param face_index:
        The index of a given face in the bmesh object.
    :return:
        The selected face for the given index.
    """

    # Update the bmesh faces
    bmesh_object.faces.ensure_lookup_table()

    # Return the face
    return bmesh_object.faces[face_index]


####################################################################################################
# @get_nearest_face_index
####################################################################################################
def get_nearest_face_index(bmesh_object,
                           point):
    """Gets the index of the nearest face to a given point in the three-dimensional space.

    :param bmesh_object:
        A given bmesh object.
    :param point:
        The position of a given point.
    :return:
        The index of the nearest face in the bmesh object to the point.
    """

    # Compute the shortest distance between the point and the centroid of all the faces of the
    # bmesh object, and return the index of the nearest face.
    nearest_face_index = -1
    shortest_distance = nmv.consts.Math.INFINITY

    # Iterate over all the faces in the bmesh object
    for face in bmesh_object.faces[:]:

        # Compute the distance between the face center and the point
        distance = (point - face.calc_center_median()).length

        # Update the shortest distance
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_face_index = face.index

    # Return the index of the nearest face to the point
    return nearest_face_index


####################################################################################################
# @get_nearest_vertex_index_to_point
####################################################################################################
def get_nearest_vertex_index_to_point(bmesh_object,
                                      point):
    """Gets the index of the nearest vertex in a given bmesh object to a given point in space.

    :param bmesh_object:
        A given bmesh object.
    :param point:
        A given point in the three-dimensional space.
    :return:
        The nearest vertex to a point.
    """

    # Get the index of the nearest face
    nearest_face_index = get_nearest_face_index(bmesh_object, point)

    # Get the nearest vertex in that selected face
    bmesh_object.faces.ensure_lookup_table()
    face = bmesh_object.faces[nearest_face_index]

    nearest_vertex_index = -1
    shortest_distance = nmv.consts.Math.INFINITY

    # Iterate over all the vertices in the bmesh object
    for vertex in face.verts[:]:
        # Compute the distance between the face center and the point
        distance = (point - vertex.co).length

        # Update the shortest distance
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_vertex_index = vertex.index

    # Return the index of the selected vertex
    return nearest_vertex_index


####################################################################################################
# @get_nearest_face_index_from_list
####################################################################################################
def get_nearest_face_index_from_list(bmesh_object,
                                     point,
                                     faces_indices):
    """Gets the index of the nearest face to a given point in the space from a given list of faces
    defined by their indices.

    :param bmesh_object:
        A given bmesh object.
    :param point:
        A given point in the three-dimensional space.
    :param faces_indices:
        A given list of indices that defines some faces in the bmesh object.
    :return:
        The index of the nearest face to the given point.
    """

    # Compute the shortest distance between the point and the centroid of all the given face of
    # the bmesh object, and return the index of the nearest face.
    nearest_face_index = -1
    shortest_distance = nmv.consts.Math.INFINITY

    # Iterate over all the indices in the list and retrieve the faces
    for face_index in faces_indices:

        # Retrieve the face from its index
        face = get_face_from_index(bmesh_object, face_index)

        # Compute the distance between the face center and the point
        distance = (point - face.calc_center_median()).length

        # Update the shortest distance
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_face_index = face.index

    # Return the index of the nearest face to the point
    return nearest_face_index


####################################################################################################
# @merge_faces_into_one_face
####################################################################################################
def merge_faces_into_one_face(bmesh_object,
                              faces_indices):
    """Merges a group of faces into a single face.
    This operation returns the index of the resulting face.

    :param bmesh_object:
        A given bmesh object.
    :param faces_indices:
        A list of indices of the faces that should be merged into one face.
    :return:
        The index of the new face created after the merge operation.
    """

    # Retrieve the faces that will be merged together from their indices
    faces_to_be_merged = []

    # Update the bmesh
    bmesh_object.faces.ensure_lookup_table()

    # Append all the faces to the list based on their indices
    for face_index in faces_indices:
        faces_to_be_merged.append(bmesh_object.faces[face_index])

    # Apply the merge operator
    final_face_dict = bmesh.ops.contextual_create(
        bmesh_object, geom=faces_to_be_merged)

    # Return the index of the resulting face from the merge operation
    return final_face_dict['faces'][0].index


####################################################################################################
# @rotate_face_in_object_towards_point
####################################################################################################
def rotate_face_in_object_towards_point(bmesh_object,
                                        face_index,
                                        to_point):
    """Rotate a face in a given object towards a certain point.

    :param bmesh_object:
        A given bmesh object.
    :param face_index:
        The index of the face that should be rotated.
    :param to_point:
        A point in space where the face should be oriented towards.
    :return:
    """
    # Get the face from its index
    face = nmv.bmeshi.ops.get_face_from_index(bmesh_object, face_index)

    # Compute the rotation angle and axis and then the rotation matrix
    face_center = face.calc_center_median()

    # Compute the rotation difference and the rotation quaternion
    track = to_point - face_center
    quaternion = face.normal.rotation_difference(track)

    # Compute the rotation matrix
    rotation_matrix = Matrix.Translation(
        face_center) * quaternion.to_matrix().to_4x4() * Matrix.Translation(-face_center)

    # Rotate the object
    matrix_object = rotation_matrix

    # Iterate over all the vertices in the bmesh object
    for vertex in face.verts[:]:

        # Transform
        vertex.co = matrix_object * vertex.co

####################################################################################################
# @rotate_face_from_center_to_point
####################################################################################################
def rotate_face_from_center_to_point(bmesh_object,
                                     face_index,
                                     target_point):
    """Rotates the face towards a point, using a vector that is connected between the center of the
    face and the given target point.

    :param bmesh_object:
        A given bmesh object.
    :param face_index:
        The index of the face that should be rotated.
    :param target_point:
        A point in space where the face should be oriented towards.
    """

    # Get the face from its index
    face = get_face_from_index(bmesh_object, face_index)

    # Compute the rotation angle and axis and then the rotation matrix
    face_center = face.calc_center_median()

    # Compute the direction between the face center and the target point
    delta = target_point - face_center
    direction = delta.normalized()

    # Compute the rotation angle
    rotation_angle = math.acos(face.normal.dot(direction) * 3.14 / 180)

    # Compute the rotation axis
    rotation_axis = face.normal.cross(direction).normalized()

    # Compute the rotation matrix
    rotation_matrix = Matrix.Rotation(rotation_angle, 4, rotation_axis)

    # Rotate the face
    bmesh.ops.rotate(bmesh_object, cent=face_center, matrix=rotation_matrix, verts=face.verts[:])


####################################################################################################
# @rotate_face_from_point_to_point
####################################################################################################
def rotate_face_from_point_to_point(bmesh_object,
                                    face_index,
                                    from_point,
                                    to_point):
    """Rotates a face towards a point and from another point 'from_point' and not from its center.

    :param bmesh_object:
        A given bmesh object.
    :param face_index:
        The index of the face that should be rotated.
    :param from_point:
        The initial point of the rotation vector.
    :param to_point:
        The final point of the rotation vector.
    """

    # Get the face from its index
    face = get_face_from_index(bmesh_object, face_index)

    # Compute the rotation difference
    track = to_point - from_point
    rotation_difference = face.normal.rotation_difference(track)

    # Compute the rotation matrix
    rotation_matrix = Matrix.Translation(from_point) * \
                      rotation_difference.to_matrix().to_4x4() * \
                      Matrix.Translation(-from_point)

    # Rotate the face
    bmesh.ops.rotate(bmesh_object, verts=face.verts[:], cent=Vector((0, 0, 0)),
                     matrix=rotation_matrix)


####################################################################################################
# @extrude_face_to_face
####################################################################################################
def extrude_face_to_face(bmesh_object,
                         face):
    """Extrudes a face by duplication at the same point.

    :param bmesh_object:
        A given bmesh object.
    :param face:
        A reference to the face that should be extruded.
    :return:
        The index of the extruded face.
    """

    # Return a reference to the extruded face
    extruded_face_dict = bmesh.ops.extrude_discrete_faces(bmesh_object, faces=[face])
    return extruded_face_dict['faces'][0]


###################################################################################################
# @extrude_face_to_point
####################################################################################################
def extrude_face_to_point(bmesh_object,
                          face_index,
                          point):
    """Extrude a face in a bmesh to a given point.

    :param bmesh_object:
        A given bmesh object.
    :param face_index:
        Face index.
    :param point:
        Target point.
    :return:
    """

    # Retrieve the face from its index
    face = nmv.bmeshi.ops.get_face_from_index(bmesh_object, face_index)

    # Rotate the face
    rotate_face_in_object_towards_point(bmesh_object, face_index, point)

    # Compute the face center
    face_center = face.calc_center_median()

    # Get delta
    delta = point - face_center

    # Get orientation
    orientation = delta.normalized()

    # Compute the extrusion delta vector
    extrusion_delta = orientation * delta.length

    # Extrude the face
    face = nmv.bmeshi.extrude_face_to_face(bmesh_object, face)

    # Translate the extruded face by the extrusion delta vector
    bmesh.ops.translate(bmesh_object, vec=extrusion_delta, verts=face.verts)

    # Return the index of the extruded face
    return face.index


####################################################################################################
# @extrude_face_with_delta_along_its_normal
####################################################################################################
def extrude_face_with_delta_along_its_normal(bmesh_object,
                                             face_index,
                                             delta):
    """Extrudes a face with a given delta (distance not vector) along its normal.

    :param bmesh_object:
        A given bmesh object.
    :param face_index:
        An index to the face that should be extruded.
    :param delta:
        The distance where the face will get extruded along its normal.
    :return:
        The index of the extruded face.
    """

    # Retrieve the face from its index
    face = get_face_from_index(bmesh_object, face_index)

    # Get the normal direction on the face to be the extrusion direction
    direction = face.normal

    # Compute the extrusion delta vector
    extrusion_delta = direction * delta

    # Extrude the face
    face = extrude_face_to_face(bmesh_object, face)

    # Translate the extruded face by the extrusion delta vector
    bmesh.ops.translate(bmesh_object, vec=extrusion_delta, verts=face.verts)

    # Return the index of the extruded face
    return face.index


####################################################################################################
# @get_face_shortest_edge
####################################################################################################
def get_face_shortest_edge(bmesh_object,
                           face_index):
    """Returns the length of the shortest edge of a given face defined by its index.

    :param bmesh_object:
        A given bmesh object.
    :param face_index:
        The index of the face.
    :return:
        The length of the shortest edge.
    """

    # Get the face from its index
    face = get_face_from_index(bmesh_object, face_index)

    # Find the length of the shortest edge in the face
    shortest_edge_length = nmv.consts.Math.INFINITY

    # Iterate over all the edges in the face, edge by edge
    for edge in face.edges[:]:
        # Compute the edge length
        edge_length = edge.calc_length()

        # Update the shortest edge
        if edge_length < shortest_edge_length:
            shortest_edge_length = edge_length

    # Return the length of the shortest edge
    return shortest_edge_length


####################################################################################################
# @get_face_longest_edge
####################################################################################################
def get_face_longest_edge(bmesh_object,
                          face_index):
    """Returns the length of longest edge of a given face defined by its index.

    :param bmesh_object:
        A given bmesh object.
    :param face_index:
        The index of the face.
    :return:
        The length of the longest edge.
    """

    # Get the face from its index
    face = get_face_from_index(bmesh_object, face_index)

    # Find the length of the longest edge in the face
    longest_edge_length = -1 * nmv.consts.Math.INFINITY

    # Iterate over all the edges in the face, edge by edge
    for edge in face.edges[:]:
        # Compute the edge length
        edge_length = edge.calc_length()

        # Update the longest edge
        if edge_length > longest_edge_length:
            longest_edge_length = edge_length

    # Return the length of the longest edge
    return longest_edge_length


####################################################################################################
# @subdivide_face
####################################################################################################
def subdivide_face(bmesh_object,
                   face_index,
                   cuts=1):
    """Subdivides a faces defined by its index into multiple cuts.

    :param bmesh_object:
        A given bmesh object.
    :param face_index:
        The index of the face.
    :param cuts:
        Number of subdivision level, 1 i.e. two faces from a single face.
    :return:
        A list of the indices of the subdivided faces.
    """

    # Get the face from its index
    face = get_face_from_index(bmesh_object, face_index)

    # Compile a list of all the edges in the face, becuase the subdivision operation is only
    # applied on edges.
    edges = []
    for edge in face.edges[:]:
        edges.append(edge)

    # Execute the subdivision operation and return a dictionary of the resulting faces from the
    # subdivision operation
    subdivided_faces = bmesh.ops.subdivide_edges(bmesh_object, edges=edges, cuts=cuts,
                                                 use_grid_fill=True)

    # Filter the faces from the dictionary and get their indices
    subdivided_faces_indices = []
    for i in subdivided_faces['geom']:
        if 'BMFace' in str(i):
            subdivided_faces_indices.append(i.index)

    # Return a list of the indices of the resulting faces from the subdivision operation
    return subdivided_faces_indices


####################################################################################################
# @subdivide_faces
####################################################################################################
def subdivide_faces(bmesh_object,
                    faces_indices,
                    cuts=1):
    """This operation subdivides a set of faces defined by their indices into multiple cuts.

    :param bmesh_object:
        A given bmesh object.
    :param faces_indices:
        A list of the indices of all the faces that will be subdivided.
    :param cuts:
        Number of subdivision level, 1 i.e. two faces from a single face.
    :return:
        A list of the indices of the subdivided faces.
    """

    # Compile a list of all the edges of the given faces and remove the duplicate edges.
    edges = list()

    # Update the mbesh
    bmesh_object.faces.ensure_lookup_table()

    # Face by face, from the given list
    for face_index in faces_indices:

        # Get the face from its index
        face = bmesh_object.faces[face_index]

        # Edge by edge
        for edge in face.edges[:]:
            edges.append(edge)

    # Remove the duplicated elements
    edges = list(set(edges))

    # Execute the subdivision operation and return a dictionary of the resulting faces from the
    # subdivision operation
    subdivided_faces = bmesh.ops.subdivide_edges(bmesh_object, edges=edges, cuts=cuts,
                                                 use_grid_fill=True)

    # Filter the faces from the dictionary and get their indices
    subdivided_faces_indices = []
    for i in subdivided_faces['geom']:
        if 'BMFace' in str(i):
            subdivided_faces_indices.append(i.index)

    # Return a list of the indices of the resulting faces from the subdivision operation
    return subdivided_faces_indices


####################################################################################################
# @extrude_face_from_joint
####################################################################################################
def extrude_face_from_joint(bmesh_object,
                            joint_faces_indices,
                            p0, p1,
                            radius):
    """Extrudes a face from a joint and returns the index of the extruded face.

    :param bmesh_object:
        An input bmesh object.
    :param joint_faces_indices:
        The indices of the joint face.
    :param p0:
        The starting point of the extrusion.
    :param p1:
        The destination point of the extrusion.
    :param radius:
        The extrusion radius.
    :return:
        The index of the extruded face.
    """

    # Select the nearest face to p1 from the joint
    face_index = get_nearest_face_index_from_list(bmesh_object, p1, joint_faces_indices)

    # Remove that face from the list to avoid intersection
    joint_faces_indices.remove(face_index)

    # Get the face from its index
    face = get_face_from_index(bmesh_object, face_index)

    # Compute extrusion delta
    extrusion_delta = p1 - p0

    # Extrude the face
    face = extrude_face_to_face(bmesh_object, face)

    # Rotate the extruded face
    rotate_face(bmesh_object, face.index, p0, p1)

    # Translate the extruded face
    bmesh.ops.translate(bmesh_object, vec=extrusion_delta, verts=face.verts)

    # Set the radius of the face
    set_face_radius(bmesh_object, face.index, radius)

    # Return the extruded face index
    return face.index


####################################################################################################
# @extrude_face_to_joint
####################################################################################################
def extrude_face_to_joint(bmesh_object,
                          face_index,
                          p0, p1,
                          radius):
    """Extrudes a face to a joint and returns a list of the indices of all the faces covering it in
    addition to the index of the top face.

    :param bmesh_object:
        An input bmesh object.
    :param face_index:
        The index of the face.
    :param p0:
        The starting point of extrusion.
    :param p1:
        The destination point of extrusion.
    :param radius:
        The extrusion radius.
    :return:
        A list of all the indices making the joint.
    """

    # Get the face from its index
    face = get_face_from_index(bmesh_object, face_index)

    # Compute the extrusion delta
    extrusion_delta = p1 - p0

    # Keep a reference for the number of faces before the extrusion
    number_faces_before_extrusion = len(bmesh_object.faces[:])

    # Extrude the segment
    face = extrude_face_to_face(bmesh_object, face)

    # Rotate the extruded face
    rotate_face_from_point_to_point(bmesh_object, face.index, p0, p1)

    # Translate the extruded face
    bmesh.ops.translate(bmesh_object, vec=extrusion_delta, verts=face.verts)

    # Set the radius of the face
    set_face_radius(bmesh_object, face.index, radius)

    # Keep a reference for the number of faces after the extrusion
    number_faces_after_extrusion = len(bmesh_object.faces[:])

    # Compile a list of all the covering faces of the extrusion joint
    joint_faces_indices = []

    # Update the bmesh, and get the faces indices
    bmesh_object.faces.ensure_lookup_table()
    for i in range(number_faces_before_extrusion,
            number_faces_after_extrusion):
        joint_faces_indices.append(bmesh_object.faces[i].index)

    # Get he index of the top face
    top_face_index = face.index

    # Return a list of the indices of the covering faces of the joint
    return joint_faces_indices, top_face_index


####################################################################################################
# @set_face_radius
####################################################################################################
def set_face_radius(bmesh_object,
                    face_index,
                    radius):
    """Changes the radius of a given face to a new value.
    This method works well ONLY with almost square faces, if the face is very rectangular, the
    resulting shape from this operation is not good.

    :param bmesh_object:
        An input bmesh object.
    :param face_index:
        The index of the face.
    :param radius:
        The requested radius.
    """

    # Get the face from its index
    face = get_face_from_index(bmesh_object, face_index)

    # Compute the center of the face
    face_center = face.calc_center_median()

    p_0 = face.verts[0].co
    p_1 = face.verts[1].co
    p_2 = face.verts[2].co
    p_3 = face.verts[3].co

    p_01 = (p_0 + p_1) * 0.5
    p_12 = (p_1 + p_2) * 0.5
    p_23 = (p_2 + p_3) * 0.5
    p_30 = (p_3 + p_0) * 0.5

    dir_p_01 = (p_01 - face_center).normalized()
    dir_p_12 = (p_12 - face_center).normalized()
    dir_p_23 = (p_23 - face_center).normalized()
    dir_p_30 = (p_30 - face_center).normalized()

    new_p_01 = face_center + dir_p_01 * radius
    new_p_12 = face_center + dir_p_12 * radius
    new_p_23 = face_center + dir_p_23 * radius
    new_p_30 = face_center + dir_p_30 * radius

    center_p_01_p12 = (new_p_01 + new_p_12) * 0.5
    center_p_12_p23 = (new_p_12 + new_p_23) * 0.5
    center_p_23_p30 = (new_p_23 + new_p_30) * 0.5
    center_p_30_p01 = (new_p_30 + new_p_01) * 0.5

    new_p_0_direction = (center_p_30_p01 - face_center).normalized()
    new_p_1_direction = (center_p_01_p12 - face_center).normalized()
    new_p_2_direction = (center_p_12_p23 - face_center).normalized()
    new_p_3_direction = (center_p_23_p30 - face_center).normalized()

    new_p_0 = face_center + new_p_0_direction * radius
    new_p_1 = face_center + new_p_1_direction * radius
    new_p_2 = face_center + new_p_2_direction * radius
    new_p_3 = face_center + new_p_3_direction * radius

    face.verts[0].co = new_p_0
    face.verts[1].co = new_p_1
    face.verts[2].co = new_p_2
    face.verts[3].co = new_p_3

    return


####################################################################################################
# @get_indices_of_faces_fully_intersecting_sphere
####################################################################################################
def get_indices_of_faces_fully_intersecting_sphere(bmesh_object,
                                                   sphere_center,
                                                   sphere_radius):
    """Returns a list of all the faces of a bmesh object that intersects another sphere defined
    by its radius and center. The intersection is true if any vertex from the faces is
    located inside the sphere.

    :param bmesh_object:
        An input bmesh object.
    :param sphere_center:
        The center of the sphere.
    :param sphere_radius:
        The radius of the sphere.
    :return:
        A list of indices of the faces that 'definitely' intersect the given sphere.
    """

    # Compile a list with all the faces that intersect the sphere center
    faces_indices = []

    for face in bmesh_object.faces[:]:
        face_intersects = True # until further notice
        for vertex in face.verts[:]:
            distance = (vertex.co - sphere_center).length
            if distance > sphere_radius:
                face_intersects = False
                break

        if face_intersects is True:
            faces_indices.append(face.index)

    # Remove duplicated objects
    faces_indices = list(set(faces_indices))

    # Return the list
    return faces_indices


####################################################################################################
# @get_indices_of_faces_intersecting_sphere
####################################################################################################
def get_indices_of_faces_intersecting_sphere(bmesh_object,
                                             sphere_center,
                                             sphere_radius):
    """Returns a list of all the faces of a bmesh object that intersects another sphere
    defined by its radius and center. The intersection is true if any vertex from the faces
    is located inside the sphere.

    :param bmesh_object:
        An input bmesh object.
    :param sphere_center:
        The center of the sphere.
    :param sphere_radius:
        The radius of the sphere.
    :return:
        A list of indices of the faces that intersect the given sphere.
    """

    # Compile a list with all the faces that intersect the sphere center
    faces_indices = []

    # Iterate over all the faces in the object and check if any vertex of the face is located inside
    # the sphere or not. if yes, add the index of this face to the list and break afterwards check
    # if any of the edges of the face intersect the sphere or not
    for face in bmesh_object.faces[:]:
        vertex_intersection_exists = False
        for vertex in face.verts[:]:

            # Compute the distance between the vertex and the sphere center
            distance = (vertex.co - sphere_center).length
            if distance < sphere_radius:
                faces_indices.append(face.index)
                vertex_intersection_exists = True
                break

        if vertex_intersection_exists is False:
            for edge in face.edges[:]:
                if nmv.geometry.ops.sphere_line(sphere_center, sphere_radius,
                        edge.verts[0].co, edge.verts[1].co):
                    faces_indices.append(face.index)
                    break

    # Remove duplicated objects
    faces_indices = list(set(faces_indices))

    # Return the list
    return faces_indices


####################################################################################################
# @get_indices_of_faces_intersecting_sphere
####################################################################################################
def map_face_to_circle(bmesh_object,
                       face_index,
                       circle):
    """Maps a given face with the specified face index to the circumference of a circle.

    :param bmesh_object:
        An input bmesh object.
    :param face_index:
        The index of the face that should be converted.
    :param circle:
        A bmesh circle to map the selected face.
    """

    # Get a reference to the face and start processing each vertex in the face
    face = get_face_from_index(bmesh_object, face_index)

    # Vertex by vertex
    for face_vertex in face.verts[:]:
        shortest_distance = 10000000000
        nearest_vertex = 0

        # Map the face
        for mapping_vertex in circle.verts[:]:
            distance = (face_vertex.co - mapping_vertex.co).length
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_vertex = mapping_vertex
        face_vertex.co = nearest_vertex.co


####################################################################################################
# @convert_face_to_circle
####################################################################################################
def convert_face_to_circle(bmesh_object,
                           face_index,
                           face_center,
                           face_radius):
    """Converts the face from irregular shape to a circle-like pattern to make it clean for the
    extrusion.
    NOTE: This function should perform better than the mapping function @map_face_to_circle.

    :param bmesh_object:
        An input bmesh object.
    :param face_index:
        The index of the face being mapped to a circle.
    :param face_center:
        A given point that reflects the actual center of the circle, but not the actual center
        of the face.
    :param face_radius:
        The given radius of the circle.
    """

    # Get a reference to the face and its centroid
    face = get_face_from_index(bmesh_object, face_index)

    # Start processing each vertex in the face
    for vertex in face.verts[:]:

        # Compute the direction from the centro to the vertex
        direction = (vertex.co - face_center).normalized()

        # Compute the mapping point along that direction and set the vertex coordinates to it
        vertex.co = face_center + direction * face_radius


####################################################################################################
# @retrieve_face_vertices_as_list
####################################################################################################
def retrieve_face_vertices_as_list(bmesh_object,
                                   face_index):
    """Returns a list of the vertices composing a face in a given bmesh using the face index.

    :param bmesh_object:
        An input bmesh object.
    :param face_index:
        The index of the corresponding face in the bmesh object.
    :return:
        A list of vertices of the selected face via its index.
    """

    # A list of all the vertices of the selected face
    vertices_list = []

    # Compile the list
    bmesh_object.faces.ensure_lookup_table()
    face = bmesh_object.faces[face_index]

    # Append the vertices to the list
    for vertex in face.verts[:]:
        vertices_list.append(vertex.co)

    # Return the list
    return vertices_list


####################################################################################################
# @scale_face
####################################################################################################
def scale_face(bmesh_object,
               face_index,
               scale_factor):
    """Scale a given face.

    :param bmesh_object:
        An input bmesh object.
    :param face_index:
        The index of the corresponding face in the bmesh object.
    :param scale_factor:
        A given scale factor.
    """

    # Get a reference to the face and its centroid
    face = get_face_from_index(bmesh_object, face_index)

    # Get face center
    face_center = face.calc_center_median()

    # A list of all the vertices of the selected face
    vertices_list = []

    # Compile the list
    bmesh_object.faces.ensure_lookup_table()
    face = bmesh_object.faces[face_index]

    # Append the vertices to the list
    for vertex in face.verts[:]:

        # Compute the direction from the centro to the vertex
        direction = (vertex.co - face_center).normalized()

        factor = (vertex.co - face_center).length

        # Compute the mapping point along that direction and set the vertex coordinates to it
        vertex.co = face_center + direction * scale_factor
