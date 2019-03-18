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
from mathutils import Vector

# Internal modules
import nmv
import nmv.mesh


####################################################################################################
# @create_line_object_from_data
####################################################################################################
def create_vertex_mesh(location=Vector((0.0, 0.0, 0.0)),
                       name='vertex'):
    """Creates a vertex at the specified location. This vertex is represented as a single
    point mesh that can be extruded.

    :param location:
        Vertex location in the scene.
    :param name:
        Vertex name.
    :return:
        A reference to the created vertex mesh.
    """

    # Initially, create a plane mesh
    vertex_mesh = nmv.mesh.create_plane(name=name)

    # Switch to the edit mode
    bpy.ops.object.editmode_toggle()

    # Merge the plan into a point at the center
    bpy.ops.mesh.merge(type='CENTER')

    # Switch back to the object mode
    bpy.ops.object.editmode_toggle()

    # Update the location
    vertex_mesh.location = location

    # Return a reference to the vertex mesh
    return vertex_mesh
