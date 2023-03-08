####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# The code in this file is based on the Tesselator add-on, version 1.28, that is provided by
# Jean Da Costa Machado. The code is available at https://github.com/jeacom25b/Tesselator-1-28
# which has a GPL license similar to NeuroMorphoVis.
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

# System
import numpy

# Blender
import bmesh
from itertools import product
from mathutils import Vector, Matrix, Color


####################################################################################################
# @random_tangent_vector
####################################################################################################
def random_tangent_vector(normal):
    """Returns a random tangent vector of a given normal vector.

    :param normal:
        A given normal.
    :return:
        Random tangent vector.
    """
    return normal.cross(numpy.random.sample(3) - 0.5).normalized()


####################################################################################################
# @random_tangent_vector
####################################################################################################
def vert_normal(vert):
    return vert.normal


def normalize_vectors_array(arr):
    magnitudes = numpy.sqrt((arr ** 2).sum(axis=1))
    return arr / magnitudes[:, numpy.newaxis]


def best_matching_vector(tests, reference):
    return max(tests, key=lambda v: v.dot(reference))


def best_matching_vector_unsigned(tests, reference):
    return max(tests, key=lambda v: abs(v.dot(reference)))


def best_vector_combination(vecs_a, vecs_b):
    a, b = max(product(vecs_a, vecs_b), key=lambda a: a[0].dot(a[1]))
    return a, b


def symmetry_space(vec, normal):
    vec1 = Vector(vec).cross(normal)
    vec = Vector(vec)
    return vec, vec1, -vec, -vec1


def hex_symmetry_space(vec, normal):
    x = Vector(vec)
    y = Vector(vec).cross(normal)
    e = x * 0.5 + y * 0.866025
    f = x * -0.5 + y * 0.866025
    return x, e, f, -x, -e, -f


####################################################################################################
# @get_grease_pencil_frame
####################################################################################################
def get_grease_pencil_frame(context):
    """Gets a grease pencil frame for drawing in the three-dimensional view.
    The Grease Pencil is a particular type of Blender object that allow you to draw in the 3D space.
    It Can be use to make traditional 2D animation, cut-out animation, motion graphics or use it as
    storyboard tool among other things.

    :param context:
        Blender context.
    :return:
        The frame
    """

    # Initialize the frame to None, in case no valid ones are available
    frame = None

    # Get a reference to the pencil
    grease_pencil = context.scene.grease_pencil

    # Check the validity
    if grease_pencil:
        if grease_pencil.layers:
            if grease_pencil.layers.active:
                if grease_pencil.layers.active.active_frame:
                    frame = grease_pencil.layers.active.active_frame
                    print('grease_pencil', frame)

    # Return a reference to the frame
    return frame


####################################################################################################
# @average_curvature
####################################################################################################
def average_curvature(vertex):
    """Gets the average curvature on a vertex of a given mesh.

    :param vertex:
        A given vertex in a mesh.
    :return:
        Average curvature values.
    """

    # Curvature value
    curvature = 0

    # The total
    total = 0

    # For every edge connected to the vertex
    for edge in vertex.link_edges:

        # Get the other vertex
        other_vertex = edge.other_vert(vertex)

        # Compute the direction
        direction = other_vertex.co - vertex.co

        # Compute the normal
        normal = other_vertex.normal - vertex.normal

        # Compute the curvature values
        curvature += normal.dot(direction) / direction.length_squared

        # Increment the counter
        total += 1

    # Avoid division-by-zero and return the average curvature value
    if total > 0:
        return curvature / total
    return 0


####################################################################################################
# @average_curvature
####################################################################################################
def curvature_direction(vertex):
    """Computes the direction of the curvature on a given vertex in a mesh.

    :param vertex:
        The vertex object.
    :return:
        The direction of the curvature.
    """

    # Ensure that the vertex is not located on a boundary edge.
    if vertex.is_boundary:

        # For every edge alon the vertex
        for edge in vertex.link_edges:

            # Ensure that the edge is not a boundary one
            if edge.is_boundary:

                # Get the other vertex
                other_vertex = edge.other_vert(vertex)

                # Compute the direction
                direction = vertex.co - other_vertex.co

                # Return the normal vector of the direction
                return direction.normalized()

    # Otherwise, if the vertex is on a boundary edge, try another solution
    try:

        # Get the the vertex
        other_vertex = min((edge.other_vert(vertex) for edge in vertex.link_edges),
                           key=lambda v: v.normal.dot(vertex.normal))

        # Normal vector
        normal_vector = other_vertex.normal.cross(vertex.normal).normalized()
        if normal_vector.length_squared == 0:
            raise ValueError()
        return normal_vector
    except ValueError:

        # Random selection
        return random_tangent_vector(vertex.normal)


####################################################################################################
# @average_curvature
####################################################################################################
def average_curvature(vertex):
    """Computes the direction of the curvature on a given vertex in a mesh.

    :param vertex:
        The vertex object.
    :return:
        The direction of the curvature.
    """

    # Another approach that is faster
    return sum((abs(edge.other_vert(vertex).normal.dot(vertex.normal))
                for edge in vertex.link_edges)) / len(vertex.link_edges)


####################################################################################################
# @subdivide_split_triangles
####################################################################################################
def subdivide_split_triangles(bmesh_object):
    """
    NOTE: This implementation is based on the code of https://github.com/jeacom25b/Tesselator-1-28.

    :param bmesh_object:
        A given bmesh object to subdivide and split its triangles
    """

    # Subdivide the edges of a bmesh with a single cut
    bmesh.ops.subdivide_edges(
        bmesh_object, edges=bmesh_object.edges, cuts=1, use_grid_fill=True, smooth=True)

    # Lists to collect the data
    collapse = list()
    triangulate = set()
    visited_vertices = set()

    # For each vertex in the bmesh object
    for vertex in bmesh_object.verts:

        # If the vertex is shared within five edges to five vertices
        if len(vertex.link_faces) == 5:

            # Get the face signature
            face_signature = tuple(sorted(len(face.verts) for face in vertex.link_faces))

            # Signature must be a tuple of (3, 4, 4, 4, 4)
            if face_signature == (3, 4, 4, 4, 4):

                # For every face in the faces containing the vertex
                for face in vertex.link_faces:

                    # If the face is a triangle, i.e. must have three vertices
                    if len(face.verts) == 3:

                        # For each edge in the face
                        for edge in face.edges:

                            # Construct a set of vertices for searching
                            vertices = set(edge.verts)

                            # If this vertex has not been processed
                            if vertex not in vertices and not vertices & visited_vertices:
                                # Operate
                                visited_vertices |= vertices

                                # Add to the collapse list
                                collapse.append(edge)

                            # Add to the triangulate set
                            triangulate |= set(face for v in vertices for face in v.link_faces)

    # Triangulate the bmesh object from the built list of triangles with the SORT_EDGE method
    bmesh.ops.triangulate(bmesh_object, faces=list(triangulate), quad_method="SHORT_EDGE")

    # Collapse
    bmesh.ops.collapse(bmesh_object, edges=collapse)

    # Build the mesh by joining the triangles together
    bmesh.ops.join_triangles(bmesh_object, faces=bmesh_object.faces,
                             angle_face_threshold=3.16, angle_shape_threshold=3.16,
                             cmp_seam=True)


####################################################################################################
# @relax_topology
####################################################################################################
def relax_topology(bmesh_object):
    """
    NOTE: This code is based on the code of https://github.com/jeacom25b/Tesselator-1-28.

    :param bmesh_object:
    :return:
    """

    # For every vertex in the bmesh object
    for vertex in bmesh_object.verts:

        # Make sure that this vertex is not a boundary vertex
        if vertex.is_boundary:
            continue

        # Construct an average vector
        avg = Vector()

        # Get the number of edges connected to this vertex
        number_edges_connected_to_vertex = len(vertex.link_edges)
        for edge in vertex.link_edges:

            # If the edge is seam, then ignore it
            if edge.seam:
                number_edges_connected_to_vertex = 0
                break

            # Get the other edge
            other = edge.other_vert(vertex)

            # Extend the average vector
            avg += other.co

        # If the vertex is connected to 3, 5 or 0 edges, continue
        if number_edges_connected_to_vertex in (3, 5, 0):
            continue

        # Otherwise, compute the final result of the average vector
        avg /= number_edges_connected_to_vertex
        avg -= vertex.co
        avg -= vertex.normal * vertex.normal.dot(avg)

        # Update the vertex position
        vertex.co += avg * 0.5


####################################################################################################
# @straigthen_quad_topology
####################################################################################################
def straigthen_quad_topology(bmesh_object):
    """
    NOTE: This implementation is based on the code of https://github.com/jeacom25b/Tesselator-1-28.

    :param bmesh_object:
        The given bmesh object.
    """

    # For each vertex in the bmesh object
    for vertex in bmesh_object.verts:

        # Ignore boundary vertices
        if vertex.is_boundary:
            continue

        # If the vertex is connected to three edges
        if len(vertex.link_edges) == 3:

            # It is a valida candidate
            valid = True

            # For each edge connected to the vertex
            for edge in vertex.link_edges:

                # If it is a seam edge, then ignore it
                if edge.seam:
                    # It is not a valid edge, next
                    valid = False
                    break

            # If it is a valid vertex
            if valid:
                # Make new pairs
                pairs = [(e_a.other_vert(vertex).co, e_b.other_vert(vertex).co)
                         for e_a in vertex.link_edges
                         for e_b in vertex.link_edges
                         if e_a is not e_b]

                # Pick the best pair
                best_pair = min(pairs, key=lambda pair: (pair[0] - pair[1]).length_squared)

                # Update the vertex position
                vertex.co = sum(best_pair, vertex.co * 0.2) / 2.2


####################################################################################################
# @bvh_snap
####################################################################################################
def bvh_snap(bvh, vertices):
    """Snaps a given list of vertices to a given BVH.
    NOTE: This implementation is based on the code of https://github.com/jeacom25b/Tesselator-1-28.

    :param bvh:
        A given BVH to snap the vertices to.
    :param vertices:
        A list of vertices to be snapped to the given BVH.
    """

    # For every vertex in the given list
    for vertex in vertices:

        # If this vertex is a boundary one, ignore it
        if vertex.is_boundary:
            continue

        # Initially, set the proceed flag to False
        proceed = False

        # For every edge connected to the vertex
        for edge in vertex.link_edges:

            # If the edge is seam, break and go for the next vertex
            if edge.seam:
                proceed = True
                break

        # Next vertex please, no valid conditions were found
        if proceed:
            continue

        # Final vertex position, initially set to None to check if is valid or not
        final_position = None

        # Get the initial position
        start = vertex.co

        # Build a normal ray
        ray = vertex.normal

        # Get the candidate locations by casting the ray along the normal directions
        location1, normal, index, distance1 = bvh.ray_cast(start, ray)
        location2, normal, index, distance2 = bvh.ray_cast(start, -ray)

        # Get a candidate position based on the nearest vertex
        location3, normal, index, distance3 = bvh.find_nearest(vertex.co)

        # Compute the final position based on the output
        if location1 and location2:
            final_position = location2 if distance2 < distance1 else location1
        elif location1:
            final_position = location1
            if location3:
                if distance3 * 3 < distance1:
                    final_position = location3
        elif location2:
            final_position = location2
            if location3:
                if distance3 * 3 < distance2:
                    final_position = location3
        else:
            if location3:
                final_position = location3

        # Finally, if the final position is computed, then update the vertex position
        if final_position:
            vertex.co = final_position


####################################################################################################
# @lerp
####################################################################################################
def lerp(v,
         a,
         b):
    """Linear interpolation

    :param v:
        Vector
    :param a:
        Minimum value.
    :param b:
        Maximum value.
    :return:
        Interpolated value.
    """
    return (1 - v) * a + v * b

