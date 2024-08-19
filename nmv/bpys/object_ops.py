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

# Internal imports
import nmv.utilities


####################################################################################################
# @select_object
####################################################################################################
def select_object(scene_object):
    """Selects a given object in the scene.

    :param scene_object:
        A given scene object to be selected.
    """

    if nmv.utilities.is_blender_280():
        scene_object.select_set(True)
    else:
        scene_object.select = True


####################################################################################################
# @get_active_object
####################################################################################################
def get_active_object():
    """Returns a reference to the active object in the scene.

    :return:
        A reference to the active object in the scene.
    """

    if nmv.utilities.is_blender_280():
        return bpy.context.active_object
    else:
        return bpy.context.scene.objects.active

####################################################################################################
# @delete_selected_object
####################################################################################################
def delete_selected_object():
    """Deletes the selected object in the scene.
    """

    bpy.ops.object.delete(use_global=True)

####################################################################################################
# @
####################################################################################################
def set_edit_mode():
    """Sets the edit mode for the object.
    """

    bpy.ops.object.mode_set(mode='EDIT')


####################################################################################################
# @set_object_mode
####################################################################################################
def set_object_mode():
    """Sets the object mode for the object.
    """

    bpy.ops.object.mode_set(mode='OBJECT')


####################################################################################################
# @toggle_object_mode
####################################################################################################
def toggle_object_mode():
    """Toggles the object mode for the object.
    """

    bpy.ops.object.editmode_toggle()