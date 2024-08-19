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

# Blender imports
import bpy


####################################################################################################
# @remove_mesh_data
####################################################################################################
def remove_mesh_data(mesh_object, 
                     do_unlink=True):
    """Remove the mesh data from the scene.
    :param mesh_object:
        The mesh object to remove its data.
    :param do_unlink:
        Whether to unlink the mesh object from the scene or not, by default it is True.
    """

    bpy.data.meshes.remove(mesh_object, do_unlink=do_unlink)