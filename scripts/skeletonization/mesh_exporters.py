####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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

# Internal imports
import mesh_rendering


####################################################################################################
# @save_blend_file
####################################################################################################
def save_blend_file(output_directory,
                    file_name):
    """Saves the current scene to a Blender file.

    :param output_directory:
        The path where the file will be saved.
    :param file_name:
        The file name of the .blend file.
    """

    # Center the scene
    mesh_rendering.center_scene()

    # Save the file
    absolute_path = "%s/%s.blend" % (output_directory, file_name)
    bpy.ops.wm.save_mainfile(filepath=absolute_path)
    print("Blender file saved successfully to:", absolute_path)
