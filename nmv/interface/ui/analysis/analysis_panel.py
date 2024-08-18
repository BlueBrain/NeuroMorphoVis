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
import copy
import time

# Blender imports
import bpy

import nmv.consts
import nmv.analysis
import nmv.builders
import nmv.enums
import nmv.file
import nmv.interface
import nmv.skeleton
import nmv.scene
import nmv.utilities

from .analysis_panel_options import *

# Is the morphology analyzed or not
is_morphology_analyzed = False


####################################################################################################
# @AnalysisPanel
####################################################################################################
class AnalysisPanel(bpy.types.Panel):
    """Analysis panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if nmv.utilities.is_blender_280() else 'TOOLS'
    bl_idname = "OBJECT_PT_NMV_Analysis"
    bl_label = 'Morphology Analysis'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

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

        # The morphology must be loaded to the UI and analyzed to be able to draw the analysis
        # components based on its arbors count
        if nmv.interface.ui_morphology is not None:

            morphology_name_row = layout.row()
            morphology_name_row.label(text='Name: %s' % nmv.interface.ui_morphology.label)

            morphology_format_row = layout.row()
            morphology_format_row.label(text='Format: %s' % nmv.interface.ui_morphology.file_format)

            # If the morphology is analyzed, then add the results to the analysis panel
            nmv.interface.add_analysis_groups_to_panel(
                morphology=nmv.interface.ui_morphology, layout=layout, context=context)

            # Export analysis button
            export_row = layout.row()
            export_row.label(text='Export Analysis Results:', icon='MESH_UVSPHERE')

            export_analysis_row = layout.row()
            export_analysis_row.operator('nmv.export_analysis_results', icon='MESH_DATA')

            create_plots_row = layout.row()
            create_plots_row.operator('nmv.create_neuron_card', icon='MESH_DATA')

            global is_morphology_analyzed
            if is_morphology_analyzed:
                morphology_stats_row = layout.row()
                morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')
                analysis_time_row = layout.row()
                analysis_time_row.prop(context.scene, 'NMV_MorphologyAnalysisTime')
                analysis_time_row.enabled = False

        # Load a morphology file to get analyzed !
        else:
            simple_message_row = layout.row()
            simple_message_row.label(text='Load Morphology to Get Analyzed!',)

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(layout)


####################################################################################################
# @cExportAnalysisResults
####################################################################################################
class ExportAnalysisResults(bpy.types.Operator):
    """Export the analysis results into a file"""

    # Operator parameters
    bl_idname = "nmv.export_analysis_results"
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

        if not nmv.file.ops.path_exists(context.scene.NMV_OutputDirectory):
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
            morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        return {'FINISHED'}


####################################################################################################
# @cExportAnalysisResults
####################################################################################################
class CreateNeuronCard(bpy.types.Operator):
    """Export the analysis results into a file"""

    # Operator parameters
    bl_idname = "nmv.create_neuron_card"
    bl_label = "Create Plots"

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

        if not nmv.file.ops.path_exists(context.scene.NMV_OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Verify the output directory
        nmv.interface.validate_output_directory(self, context.scene)

        # Create the analysis directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.analysis_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.analysis_directory)

        # Create a specific directory per morphology
        morphology_analysis_directory = '%s/%s' % (nmv.interface.ui_options.io.analysis_directory,
                                                   nmv.interface.ui_morphology.label)
        if not nmv.file.ops.path_exists(morphology_analysis_directory):
            nmv.file.ops.clean_and_create_directory(morphology_analysis_directory)

        # Starting time
        start_time = time.time()

        # Export the analysis results
        nmv.interface.ui.export_analysis_results(
            morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Analysis plots
        nmv.analysis.plot_analysis_results(
            morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Morphology analyzed
        analysis_time = time.time()
        global is_morphology_analyzed
        is_morphology_analyzed = True
        context.scene.NMV_MorphologyAnalysisTime = analysis_time - start_time
        nmv.logger.info('Morphology skeleton analyzed in [%f] seconds' %
                        context.scene.NMV_MorphologyAnalysisTime)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.register_class(AnalysisPanel)

    # Export analysis button
    bpy.utils.register_class(CreateNeuronCard)
    bpy.utils.register_class(ExportAnalysisResults)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.unregister_class(AnalysisPanel)

    # Export analysis button
    bpy.utils.unregister_class(CreateNeuronCard)
    bpy.utils.unregister_class(ExportAnalysisResults)
