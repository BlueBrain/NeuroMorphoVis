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

# Internal imports
import nmv
import nmv.scene
import nmv.mesh


####################################################################################################
# @add_hook_to_vertices
####################################################################################################
def add_hook_to_vertices(mesh_object,
                         vertices_indices,
                         name='hook'):
    """Create and assign a hook to a a list of selected vertices given by their indices.
    For single vertex, just pass the index in a list, for e.g. add_hook_to_vertices(,[vertex_idx],)

    :param mesh_object:
        An input mesh where the hook will be added to.
    :param vertices_indices:
        A list of indices of the vertices where the hook will be attached to.
    :param name:
        Hook name, by default 'hook'.
    :return:
        A reference to the hook.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Set this object to be only the active object
    nmv.scene.ops.set_active_object(mesh_object)

    # Deselect all the vertices in the mesh object
    nmv.mesh.ops.deselect_all_vertices(mesh_object)

    # Select only the vertices of interest
    nmv.mesh.ops.select_vertices(mesh_object, vertices_indices)

    # Switch to the edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Add the hook
    bpy.ops.object.hook_add_newob()

    # Switch to the object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Rename the hook and return a reference to it
    hook = None
    for scene_object in bpy.context.scene.objects:
        if scene_object.name == 'Empty':
            hook = scene_object
            break
    hook.name = name

    # Deselect all again
    nmv.scene.ops.deselect_all()

    # Return a reference to the hook
    return hook


####################################################################################################
# @locate_hook_at_keyframe
####################################################################################################
def locate_hook_at_keyframe(hook,
                            location,
                            keyframe):
    """Manipulate the hook's position at certain keyframe.

    :param hook:
        A given hook.
    :param location:
        The specified hook position, where the hook will be located.
    :param keyframe:
        Time keyframe.
    """

    # Set the keyframe
    bpy.context.scene.frame_set(keyframe)

    # Deselect all the objects in the scene and activate the hook.
    nmv.scene.ops.set_active_object(hook)

    # Select the hook
    hook.select = True

    # Change its location
    hook.location=location

    # Insert the keyframe at this location
    hook.keyframe_insert(data_path="location")


####################################################################################################
# @scale_hook_at_keyframe
####################################################################################################
def scale_hook_at_keyframe(hook,
                           scale,
                           keyframe):
    """Scale the hook at certain keyframe.

    :param hook:
        A given hook.
    :param scale:
        The specified hook 'uniform' scale value.
    :param keyframe:
        Time keyframe.
    """

    # Set the keyframe
    bpy.context.scene.frame_set(keyframe)

    # Deselect all the objects in the scene
    nmv.scene.ops.set_active_object(hook)

    # Select the hook
    hook.select = True

    # Scale the hook
    hook.scale = (scale, scale, scale)

    # Insert the keyframe at this scale
    hook.keyframe_insert(data_path="scale")
