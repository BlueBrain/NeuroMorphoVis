####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import time

# Blender imports
import bpy

# Internal imports
import nmv.analysis
import nmv.consts
import nmv.enums
import nmv.interface
import nmv.utilities


####################################################################################################
# @NMV_ExportAnalysisResults
####################################################################################################
class NMV_ExportAnalysisResults(bpy.types.Operator):
    """Export the analysis results into a file"""

    # Operator parameters
    bl_idname = "nmv.export_analysis_results"
    bl_label = "Export Results"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

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
# @NMV_CreateNeuronCard
####################################################################################################
class NMV_CreateNeuronCard(bpy.types.Operator):
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
        #nmv.interface.ui.export_analysis_results(
        #    morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Analysis plots
        nmv.analysis.plot_analysis_results(
            morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Morphology analyzed
        analysis_time = time.time()

        nmv.interface.ui_morphology_analyzed = True
        context.scene.NMV_MorphologyAnalysisTime = analysis_time - start_time
        nmv.logger.info('Morphology skeleton analyzed in [%f] seconds' %
                        context.scene.NMV_MorphologyAnalysisTime)

        return {'FINISHED'}