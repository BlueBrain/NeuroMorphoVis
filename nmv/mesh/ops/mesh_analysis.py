####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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
import math

# Blender imports
from mathutils import Vector


####################################################################################################
# @compute_number_of_vertices_of_mesh
####################################################################################################
def compute_number_of_vertices_of_mesh(mesh_object):
    """Computes the number of vertices of a given mesh object.

    :param mesh_object:
        A given mesh object.
    :return:
        The number of vertices of the given mesh object. If the given object is not mesh, it will
        issue a warning and return zero.
    """

    # Ensure that it is a mesh
    if mesh_object.type == 'MESH':
        return len(mesh_object.data.vertices)
    else:
        print('The object [%s] is NOT a mesh object!' % mesh_object.name)
        return 0.0


####################################################################################################
# @compute_surface_area_of_mesh
####################################################################################################
def compute_surface_area_of_mesh(mesh_object):
    """Computes the surface area of a given mesh object.

    :param mesh_object:
        A given mesh object.
    :return:
        The surface area of the given mesh object. If the given object is not mesh, it will
        issue a warning and return zero.
    """

    # Ensure that it is a mesh
    if mesh_object.type == 'MESH':

        # Compute the sum of the areas of every face in the mesh
        total_surface_area = 0.0
        for face in mesh_object.data.polygons:

            # Calculate the area of the face
            face_vertices = [mesh_object.matrix_world @ mesh_object.data.vertices[vertex_index].co
                             for vertex_index in face.vertices]
            edge1 = face_vertices[1] - face_vertices[0]
            edge2 = face_vertices[2] - face_vertices[0]
            face_area = (edge1.cross(edge2)).length * 0.5

            # Add the face area to the total surface area
            total_surface_area += face_area
        return total_surface_area
    else:
        print('The object [%s] is NOT a mesh object!' % mesh_object.name)
        return 0.0


####################################################################################################
# @compute_bounding_box_diagonal_of_mesh
####################################################################################################
def compute_bounding_box_diagonal_of_mesh(mesh_object):
    """Computes the size (or thd diagonal bounding box length) of a given mesh object.

    :param mesh_object:
        A given mesh object.
    :return:
        The length of the diagonal of the mesh bounding box. If the given object is not mesh, it will
        issue a warning and return zero.
    """

    # Ensure that it is a mesh
    if mesh_object.type == 'MESH':

        # Get the bounding box dimensions
        # Get object's bounding box dimensions
        bbox = [mesh_object.matrix_world @ Vector(corner) for corner in mesh_object.bound_box]
        min_x = min(bbox, key=lambda x: x[0])[0]
        max_x = max(bbox, key=lambda x: x[0])[0]
        min_y = min(bbox, key=lambda x: x[1])[1]
        max_y = max(bbox, key=lambda x: x[1])[1]
        min_z = min(bbox, key=lambda x: x[2])[2]
        max_z = max(bbox, key=lambda x: x[2])[2]

        # Calculate the diagonal distance
        return math.sqrt((max_x - min_x) ** 2 + (max_y - min_y) ** 2 + (max_z - min_z) ** 2)
    else:
        print('The object [%s] is NOT a mesh object!' % mesh_object.name)
        return 0.0
