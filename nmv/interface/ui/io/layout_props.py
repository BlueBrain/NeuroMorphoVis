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

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @draw_io_documentation_button
####################################################################################################
def draw_io_documentation_button(panel):

    row = panel.layout.column()
    row.operator('nmv.documentation_io', icon='URL')
    row.separator()


####################################################################################################
# @draw_morphology_loading_button
####################################################################################################
def draw_morphology_loading_button(panel):

    row = panel.layout.column()
    row.operator('nmv.load_morphology', icon='ANIM_DATA')


####################################################################################################
# @draw_input_data_header
####################################################################################################
def draw_input_data_header(panel):

    row = panel.layout.row()
    row.label(text='Input Data Options', icon='LIBRARY_DATA_DIRECT')


####################################################################################################
# @draw_input_source
####################################################################################################
def draw_input_source(panel, scene, options):

    row = panel.layout.row()
    row.prop(scene, 'NMV_InputSource')
    options.io.input_source = scene.NMV_InputSource


####################################################################################################
# @draw_morphology_file_path_option
####################################################################################################
def draw_morphology_file_path_option(panel, scene, options):

    row = panel.layout.row()
    row.prop(scene, 'NMV_MorphologyFile')
    options.morphology.morphology_file_path = scene.NMV_MorphologyFile


####################################################################################################
# @draw_circuit_file_path_option
####################################################################################################
def draw_circuit_file_path_option(panel, scene, options):

    row = panel.layout.row()
    row.prop(scene, 'NMV_CircuitFile')
    options.morphology.blue_config = scene.NMV_CircuitFile


####################################################################################################
# @draw_morphology_gid_option
####################################################################################################
def draw_morphology_gid_option(panel, scene, options):

    row = panel.layout.row()
    row.prop(scene, 'NMV_Gid')
    options.morphology.gid = scene.NMV_Gid


####################################################################################################
# @draw_morphology_centering_option
####################################################################################################
def draw_morphology_centering_option(panel, scene, options):

    row = panel.layout.row()
    row.prop(scene, 'NMV_CenterMorphologyAtOrigin')
    options.morphology.center_at_origin = scene.NMV_CenterMorphologyAtOrigin


####################################################################################################
# @draw_input_data_options
####################################################################################################
def draw_input_data_options(panel, scene, options):

    draw_input_data_header(panel=panel)
    draw_input_source(panel=panel, scene=scene, options=options)

    if options.io.input_source == nmv.enums.Input.MORPHOLOGY_FILE:
        draw_morphology_file_path_option(panel=panel, scene=scene, options=options)

    elif options.io.input_source == nmv.enums.Input.CIRCUIT_GID:
        draw_circuit_file_path_option(panel=panel, scene=scene, options=options)
        draw_morphology_gid_option(panel=panel, scene=scene, options=options)

    else:
        panel.report({'ERROR'}, 'Invalid Input Source')
        nmv.logger.log('UI_ERROR: draw_input_output_panel_options')

    draw_morphology_centering_option(panel=panel, scene=scene, options=options)


####################################################################################################
# @draw_morphology_loading_statistics
####################################################################################################
def draw_morphology_loading_statistics(panel, scene, morphology):

    # Display the loading statistics after loading the morphology
    if morphology is not None:

        # Loading time
        row = panel.layout.row()
        row.prop(scene, 'NMV_MorphologyLoadingTime')
        row.enabled = False

        # Drawing time
        row = panel.layout.row()
        row.prop(scene, 'NMV_MorphologyDrawingTime')
        row.enabled = False


####################################################################################################
# @draw_output_data_header
####################################################################################################
def draw_output_data_header(panel):

    row = panel.layout.row()
    row.label(text='Output Options', icon='SCRIPT')


####################################################################################################
# @draw_output_directory_option
####################################################################################################
def draw_output_directory_option(panel, scene, options):

    row = panel.layout.row()
    row.prop(scene, 'NMV_OutputDirectory')
    options.io.output_directory = scene.NMV_OutputDirectory


####################################################################################################
# @draw_default_paths_option
####################################################################################################
def draw_default_paths_option(panel, scene, options):

    row = panel.layout.row()
    row.prop(scene, 'NMV_DefaultArtifactsRelativePath')
    options.io.use_default_path_for_artifacts = scene.NMV_DefaultArtifactsRelativePath


####################################################################################################
# @draw_images_path_option
####################################################################################################
def draw_images_path_option(panel, scene, enabled):
    row = panel.layout.row()
    row.prop(scene, 'NMV_ImagesPath')
    row.enabled = enabled


####################################################################################################
# @draw_sequences_path_option
####################################################################################################
def draw_sequences_path_option(panel, scene, enabled):

    row = panel.layout.row()
    row.prop(scene, 'NMV_SequencesPath')
    row.enabled = enabled


####################################################################################################
# @draw_meshes_path_option
####################################################################################################
def draw_meshes_path_option(panel, scene, enabled):

    row = panel.layout.row()
    row.prop(scene, 'NMV_MeshesPath')
    row.enabled = enabled


####################################################################################################
# @draw_morphologies_path_option
####################################################################################################
def draw_morphologies_path_option(panel, scene, enabled):

    row = panel.layout.row()
    row.prop(scene, 'NMV_MorphologiesPath')
    row.enabled = enabled


####################################################################################################
# @draw_analysis_path_option
####################################################################################################
def draw_analysis_path_option(panel, scene, enabled):

    row = panel.layout.row()
    row.prop(scene, 'NMV_AnalysisPath')
    row.enabled = enabled


####################################################################################################
# @draw_stats_path_option
####################################################################################################
def draw_stats_path_option(panel, scene, enabled):

    row = panel.layout.row()
    row.prop(scene, 'NMV_StatisticsPath')
    row.enabled = enabled


####################################################################################################
# @draw_output_options
####################################################################################################
def draw_output_data_options(panel, scene, options):

    draw_output_data_header(panel=panel)
    draw_output_directory_option(panel=panel, scene=scene, options=options)
    draw_default_paths_option(panel=panel,  scene=scene, options=options)

    enabled = not options.io.use_default_path_for_artifacts
    draw_images_path_option(panel=panel, scene=scene, enabled=enabled)
    draw_sequences_path_option(panel=panel, scene=scene, enabled=enabled)
    draw_meshes_path_option(panel=panel, scene=scene, enabled=enabled)
    draw_morphologies_path_option(panel=panel, scene=scene, enabled=enabled)
    draw_analysis_path_option(panel=panel, scene=scene, enabled=enabled)
    draw_stats_path_option(panel=panel, scene=scene, enabled=enabled)

    # Pass options from UI to system
    if 'Select Directory' in scene.NMV_OutputDirectory:
        options.io.output_directory = None
    else:
        output_dir = options.io.output_directory
        options.io.output_directory = output_dir
        options.io.images_directory = '%s/%s' % (output_dir, scene.NMV_ImagesPath)
        options.io.sequences_directory = '%s/%s' % (output_dir, scene.NMV_SequencesPath)
        options.io.morphologies_directory = '%s/%s' % (output_dir, scene.NMV_MorphologiesPath)
        options.io.meshes_directory = '%s/%s' % (output_dir, scene.NMV_MeshesPath)
        options.io.analysis_directory = '%s/%s' % (output_dir, scene.NMV_AnalysisPath)
        options.io.statistics_directory = '%s/%s' % (output_dir, scene.NMV_StatisticsPath)