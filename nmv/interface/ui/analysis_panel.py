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


# System imports
import copy

# Blender imports
import bpy
from mathutils import Vector
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import FloatVectorProperty

import nmv
import nmv.consts
import nmv.analysis
import nmv.enums
import nmv.file
import nmv.interface
import nmv.skeleton
import nmv.scene


####################################################################################################
# @AnalysisPanel
####################################################################################################
class AnalysisPanel(bpy.types.Panel):
    """Analysis panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Morphology Analysis'
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
            Blender context
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Morphology analysis button
        analyze_morphology_column = layout.column(align=True)
        analyze_morphology_column.operator('analyze.morphology', icon='MESH_DATA')

        # The morphology must be loaded to the UI and analyzed to be able to draw the analysis
        # components based on its neurites count
        if context.scene.MorphologyAnalyzed:

            # If the morphology is analyzed, then add the results to the analysis panel
            nmv.interface.add_analysis_groups_to_panel(
                morphology=nmv.interface.ui_morphology, layout=layout, context=context)

            # Export analysis button
            export_analysis_row = layout.row()
            export_analysis_row.operator('export.analysis_results', icon='MESH_DATA')

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(layout)


####################################################################################################
# @SaveSomaMeshBlend
####################################################################################################
class AnalyzeMorphology(bpy.types.Operator):
    """Analyze the morphology skeleton, detect the artifacts and report them"""

    # Operator parameters
    bl_idname = "analyze.morphology"
    bl_label = "Analyze Morphology"

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

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Plot the morphology (whatever issues it contains)
        nmv.interface.ui.sketch_morphology_skeleton_guide(
            morphology=nmv.interface.ui_morphology,
            options=copy.deepcopy(nmv.interface.ui_options))

        # Register the analysis components, apply the kernel functions and update the UI
        context.scene.MorphologyAnalyzed = nmv.interface.analyze_morphology(
            morphology=nmv.interface.ui_morphology, context=context)

        # View all the objects in the scene
        nmv.scene.ops.view_all_scene()

        return {'FINISHED'}


####################################################################################################
# @SaveSomaMeshBlend
####################################################################################################
class ExportAnalysisResults(bpy.types.Operator):
    """Export the analysis results into a file"""

    # Operator parameters
    bl_idname = "export.analysis_results"
    bl_label = "Export Results"

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

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Verify the output directory
        nmv.interface.validate_output_directory(self, context.scene)

        # Create the analysis directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.analysis_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.analysis_directory)

        # Export the analysis results
        nmv.interface.ui.export_analysis_results(
            morphology=nmv.interface.ui_morphology,
            directory=nmv.interface.ui_options.io.analysis_directory)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.register_class(AnalysisPanel)

    # Morphology analysis button
    bpy.utils.register_class(AnalyzeMorphology)

    # Export analysis button
    bpy.utils.register_class(ExportAnalysisResults)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.unregister_class(AnalysisPanel)

    # Morphology analysis button
    bpy.utils.unregister_class(AnalyzeMorphology)

    # Export analysis button
    bpy.utils.unregister_class(ExportAnalysisResults)
