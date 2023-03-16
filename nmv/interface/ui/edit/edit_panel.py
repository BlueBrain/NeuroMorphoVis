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
from bpy.props import BoolProperty

# Internal imports
import nmv.edit
import nmv.interface
import nmv.scene
import nmv.consts
import nmv.utilities
import nmv.enums

# Globals
# Morphology editor
morphology_editor = None

# A flag to indicate that the morphology has been edited and ready for update
is_skeleton_edited = False
in_edit_mode = False


####################################################################################################
# @NMV_EditPanel
####################################################################################################
class NMV_EditPanel(bpy.types.Panel):
    """Edit panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_idname = "OBJECT_PT_NMV_MorphologyEditing"
    bl_label = 'Morphology Editing'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    # Register a variable that indicates that the morphology is sketched to be able to update the UI
    bpy.types.Scene.NMV_MorphologySketched = BoolProperty(default=False)
    bpy.types.Scene.NMV_MorphologyCoordinatesEdited = BoolProperty(default=False)

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel

        :param context:
            Rendering context
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Documentation button
        documentation_button = layout.column()
        documentation_button.operator('nmv.documentation_editing', icon='URL')
        documentation_button.separator()

        # Morphology sketching button
        if not in_edit_mode:
            sketching_morphology_column = layout.column(align=True)
            sketching_morphology_column.operator('sketch.skeleton', icon='PARTICLE_POINT')

        # Reconstruction options
        edit_coordinates_row = layout.row()
        edit_coordinates_row.label(text='Editing Samples Coordinates:',
                                   icon='OUTLINER_OB_EMPTY')

        global is_skeleton_edited
        if not is_skeleton_edited:

            # Morphology edit button
            edit_morphology_column = layout.column(align=True)
            edit_morphology_column.operator('edit.morphology_coordinates', icon='MESH_DATA')

        else:

            # Morphology update buttons
            update_morphology_column = layout.column(align=True)
            update_morphology_column.operator('update.morphology_coordinates', icon='MESH_DATA')

        # Saving morphology buttons
        if not in_edit_mode:

            # Saving morphology options
            save_morphology_row = layout.row()
            save_morphology_row.label(text='Save Morphology As:', icon='MESH_UVSPHERE')

            save_morphology_buttons_column = layout.column(align=True)
            save_morphology_buttons_column.operator('export_morphology.swc', icon='GROUP_VERTEX')

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(layout)


####################################################################################################
# @NMV_SketchSkeleton
####################################################################################################
class NMV_SketchSkeleton(bpy.types.Operator):
    """Repair the morphology skeleton, detect the artifacts and fix them
    """

    # Operator parameters
    bl_idname = "sketch.skeleton"
    bl_label = "Sketch Skeleton"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Rendering context
        :return:
            'FINISHED'
        """

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
    """Update the morphology coordinates following to the repair process
    """

    # Operator parameters
    bl_idname = "edit.morphology_coordinates"
    bl_label = "Edit Coordinates"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Rendering context
        :return:
            'FINISHED        """

        if nmv.interface.ui_morphology is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Create an object of the repairer
        global morphology_editor

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Sketch the guide to make sure users can see something
        options_clone = copy.deepcopy(nmv.interface.ui_options)
        options_clone.morphology.soma_representation = nmv.enums.Soma.Representation.META_BALLS
        nmv.interface.ui.sketch_morphology_skeleton_guide(
            morphology=nmv.interface.ui_morphology, options=options_clone)

        # Sketch the morphological skeleton for repair
        morphology_editor = nmv.edit.MorphologyEditor(
            morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
        morphology_editor.sketch_morphology_skeleton()

        # Switch to the wire-frame mode
        nmv.scene.switch_interface_to_edit_mode()

        # Switch to edit mode, to be able to export the mesh
        bpy.ops.object.mode_set(mode='EDIT')

        # The morphology is edited
        global is_skeleton_edited
        is_skeleton_edited = True

        # Update the edit mode
        global in_edit_mode
        in_edit_mode = True

        return {'FINISHED'}


####################################################################################################
# @NMV_UpdateMorphologyCoordinates
####################################################################################################
class NMV_UpdateMorphologyCoordinates(bpy.types.Operator):
    """Update the morphology coordinates following to the repair process.
    """

    # Operator parameters
    bl_idname = "update.morphology_coordinates"
    bl_label = "Update Coordinates"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Rendering context
        :return:
            'FINISHED'
        """

        # Switch back to the solid mode
        nmv.scene.switch_interface_to_visualization_mode()

        # Create an object of the repairer
        global morphology_editor

        # Create the morphological skeleton
        if morphology_editor is not None:

            # Switch back to object mode, to be able to export the mesh
            bpy.ops.object.mode_set(mode='OBJECT')

            # Update the morphology skeleton
            morphology_editor.update_skeleton_coordinates()

            global is_skeleton_edited
            is_skeleton_edited = False

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Plot the morphology (whatever issues it contains)
        nmv.interface.ui.sketch_morphology_skeleton_guide(
            morphology=nmv.interface.ui_morphology,
            options=copy.deepcopy(nmv.interface.ui_options))

        # Update the edit mode
        global in_edit_mode
        in_edit_mode = False

        # Switch back from the analysis mode to the visualization mode
        nmv.scene.switch_interface_to_visualization_mode()

        return {'FINISHED'}


####################################################################################################
# @NMV_ExportMorphologySWC
####################################################################################################
class NMV_ExportMorphologySWC(bpy.types.Operator):
    """Export the reconstructed morphology in an SWC file"""

    # Operator parameters
    bl_idname = "export_morphology.swc"
    bl_label = "SWC (.swc)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """
        Executes the operator.

        :param context: Operator context.
        :return: {'FINISHED'}
        """

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.file_ops.path_exists(context.scene.NMV_OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.morphologies_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.morphologies_directory)

        # Export the reconstructed morphology as an .swc file
        nmv.file.write_morphology_to_swc_file(
            nmv.interface.ui_morphology, nmv.interface.ui_options.io.morphologies_directory)

        return {'FINISHED'}


####################################################################################################
# @NMV_MorphologyEditingDocumentation
####################################################################################################
class NMV_MorphologyEditingDocumentation(bpy.types.Operator):
    """Open the online documentation page of the Morphology Editing panel."""

    # Operator parameters
    bl_idname = "nmv.documentation_editing"
    bl_label = "Online User Guide"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis/wiki/Morphology-Editing')
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.register_class(NMV_EditPanel)

    # Buttons
    bpy.utils.register_class(NMV_MorphologyEditingDocumentation)
    bpy.utils.register_class(NMV_SketchSkeleton)
    bpy.utils.register_class(NMV_EditMorphologyCoordinates)
    bpy.utils.register_class(NMV_UpdateMorphologyCoordinates)
    bpy.utils.register_class(NMV_ExportMorphologySWC)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.unregister_class(NMV_EditPanel)

    # Buttons
    bpy.utils.unregister_class(NMV_MorphologyEditingDocumentation)
    bpy.utils.unregister_class(NMV_SketchSkeleton)
    bpy.utils.unregister_class(NMV_EditMorphologyCoordinates)
    bpy.utils.unregister_class(NMV_UpdateMorphologyCoordinates)
    bpy.utils.unregister_class(NMV_ExportMorphologySWC)
