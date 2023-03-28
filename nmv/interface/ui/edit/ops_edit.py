####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import copy

# Blender imports
import bpy

# Internal imports
import nmv.edit
import nmv.interface
import nmv.scene
import nmv.enums


####################################################################################################
# @NMV_SketchSkeleton
####################################################################################################
class NMV_SketchSkeleton(bpy.types.Operator):
    """Repair the morphology skeleton, detect the artifacts and fix them"""

    # Operator parameters
    bl_idname = "sketch.skeleton"
    bl_label = "Sketch Skeleton"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Clone the options to avoid messing the other panels
        options_clone = copy.deepcopy(nmv.interface.ui_options)
        options_clone.shading.set_default()

        # Plot the morphology (whatever issues it contains)
        nmv.interface.ui.sketch_morphology_skeleton_guide(
            morphology=nmv.interface.ui_morphology,
            options=options_clone)

        return {'FINISHED'}


####################################################################################################
# @NMV_EditMorphologyCoordinates
####################################################################################################
class NMV_EditMorphologyCoordinates(bpy.types.Operator):
    """Update the morphology coordinates following to the repair process"""

    # Operator parameters
    bl_idname = "edit.morphology_coordinates"
    bl_label = "Edit Coordinates"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        if nmv.interface.ui_morphology is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Sketch the guide to make sure users can see something
        options_clone = copy.deepcopy(nmv.interface.ui_options)
        options_clone.morphology.soma_representation = nmv.enums.Soma.Representation.META_BALLS
        nmv.interface.ui.sketch_morphology_skeleton_guide(
            morphology=nmv.interface.ui_morphology, options=options_clone)

        # Sketch the morphological skeleton for repair
        nmv.interface.ui_morphology_editor = nmv.edit.MorphologyEditor(
            morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
        nmv.interface.ui_morphology_editor.sketch_morphology_skeleton()

        # Switch to the wire-frame mode
        nmv.scene.switch_interface_to_edit_mode()

        # Switch to edit mode, to be able to export the mesh
        bpy.ops.object.mode_set(mode='EDIT')

        # The morphology is edited
        nmv.interface.ui_is_skeleton_edited = True

        # Update the edit mode
        nmv.interface.ui_in_edit_mode = True

        return {'FINISHED'}


####################################################################################################
# @NMV_UpdateMorphologyCoordinates
####################################################################################################
class NMV_UpdateMorphologyCoordinates(bpy.types.Operator):
    """Update the morphology coordinates following to the repair process"""

    # Operator parameters
    bl_idname = "update.morphology_coordinates"
    bl_label = "Update Coordinates"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Switch back to the solid mode
        nmv.scene.switch_interface_to_visualization_mode()

        # Create the morphological skeleton
        if nmv.interface.ui_morphology_editor is not None:

            # Switch back to object mode, to be able to export the mesh
            bpy.ops.object.mode_set(mode='OBJECT')

            # Update the morphology skeleton
            nmv.interface.ui_morphology_editor.update_skeleton_coordinates()

            # Update the state
            nmv.interface.ui_is_skeleton_edited = False

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Plot the morphology (whatever issues it contains)
        nmv.interface.ui.sketch_morphology_skeleton_guide(
            morphology=nmv.interface.ui_morphology,
            options=copy.deepcopy(nmv.interface.ui_options))

        # Update the edit mode
        nmv.interface.ui_in_edit_mode = False

        # Switch back from the analysis mode to the visualization mode
        nmv.scene.switch_interface_to_visualization_mode()

        return {'FINISHED'}
