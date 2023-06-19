####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import bmesh
from mathutils import Vector


####################################################################################################
# @get_vertex_from_index
####################################################################################################
def get_vertex_from_index(bmesh_object,
                          vertex_index):
    """Gets a vertex of a bmesh object from its index.
    :param bmesh_object:
        A given bmesh object.
    :param vertex_index:
        The index of the vertex we need to get.
    :return:
        A reference to the vertex.
    """

    # Update the bmesh vertices
    bmesh_object.verts.ensure_lookup_table()

    # Get the vertex from its index
    vertex = bmesh_object.verts[vertex_index]

    # Return a reference to the vertex
    return vertex


####################################################################################################
# @extrude_vertex_towards_point
####################################################################################################
def extrude_vertex_towards_point(bmesh_object,
                                 index,
                                 point):
    """Extrude a vertex of a bmesh object to a given point in space.
    :param bmesh_object:
        A given bmesh object.
    :param index:
        The index of the vertex that will be extruded.
    :param point:
        A point in three-dimensional space.
    :return:
    """

    # Get a reference to the vertex
    vertex = get_vertex_from_index(bmesh_object, index)

    # Extrude the vertex (sort of via duplication)
    extruded_vertex = bmesh.ops.extrude_vert_indiv(bmesh_object, verts=[vertex])
    extruded_vertex = extruded_vertex['verts'][0]

    # Note that the extruded vertex is located at the same position of the original one
    # So we should update the coordinate of the extruded vertex to the given point
    extruded_vertex.co = point

    # Return a reference to the extruded vertex
    return extruded_vertex


####################################################################################################
# @relax_topology
####################################################################################################
def relax_topology(bmesh_object):
    """
    NOTE: This implementation is based on the code of https://github.com/jeacom25b/Tesselator-1-28.

    :param bmesh_object:
    :return:
    """

    # For every vertex in the bmesh object
    for vertex in bmesh_object.verts:

        # Make sure that this vertex is not a boundary vertex
        if vertex.is_boundary:
            continue

        # Construct an average vector
        avg = Vector((0.0, 0.0, 0.0))

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
