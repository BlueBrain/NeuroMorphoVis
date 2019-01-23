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
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import FloatVectorProperty

import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.analysis
import neuromorphovis.edit
import neuromorphovis.enums
import neuromorphovis.file
import neuromorphovis.interface
import neuromorphovis.skeleton


# Morphology editor
morphology_editor = None

# A flag to indicate that the morphology has been edited and ready for update
is_skeleton_edited = False


####################################################################################################
# @EditPanel
####################################################################################################
class EditPanel(bpy.types.Panel):
    """Edit panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Morphology Editing'
    bl_context = 'objectmode'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    # Register a variable that indicates that the morphology is analyzed to be able to update the UI
    bpy.types.Scene.MorphologyAnalyzed = BoolProperty(default=False)

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

        # Morphology analysis button
        repair_morphology_column = layout.column(align=True)
        repair_morphology_column.operator('sketch.skeleton', icon='MESH_DATA')

        # Morphology update button
        update_morphology_column = layout.column(align=True)
        update_morphology_column.operator('update.morphology_coordinates', icon='MESH_DATA')
        if is_skeleton_edited:
            update_morphology_column.enabled = True
        else:
            update_morphology_column.enabled = False



        ####################################################################################################
# @SketchSkeleton
####################################################################################################
class SketchSkeleton(bpy.types.Operator):
    """Repair the morphology skeleton, detect the artifacts and fix them"""

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

        """
        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        nmv.logger.log(context.scene.OutputDirectory)
        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the analysis directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.analysis_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.analysis_directory)
        """

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology file
        nmv.interface.ui.load_morphology(self, context.scene)

        # Create an object of the repairer
        global morphology_editor
        morphology_editor = nmv.edit.MorphologyEditor(
            morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Create the morphological skeleton
        morphology_editor.create_morphological_skeleton()

        # Update the editing flag
        global is_skeleton_edited
        is_skeleton_edited = True

        return {'FINISHED'}


####################################################################################################
# @UpdateMorphologyCoordinates
####################################################################################################
class UpdateMorphologyCoordinates(bpy.types.Operator):
    """Update the morphology corrdinates following to the repair process.
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

        # Create an object of the repairer
        global morphology_editor

        # Create the morphological skeleton
        if morphology_editor is not None:
            morphology_editor.update_skeleton_coordinates()

            # Update the editing flag
            global is_skeleton_edited
            is_skeleton_edited = False

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.register_class(EditPanel)

    # Morphology analysis button
    bpy.utils.register_class(SketchSkeleton)

    # Morphology analysis button
    bpy.utils.register_class(UpdateMorphologyCoordinates)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.unregister_class(EditPanel)

    # Morphology analysis button
    bpy.utils.unregister_class(SketchSkeleton)

    bpy.utils.unregister_class(UpdateMorphologyCoordinates)
