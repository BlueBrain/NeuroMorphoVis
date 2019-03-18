####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
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
import bmesh


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
