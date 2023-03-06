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
# @draw_input_options
####################################################################################################
def draw_input_options(panel,
                       scene,
                       options):

    # Input data options
    input_data_options_row = panel.layout.row()
    input_data_options_row.label(text='Input Data Options:', icon='LIBRARY_DATA_DIRECT')

    # Input source
    input_source_row = panel.layout.row()
    input_source_row.prop(scene, 'NMV_InputSource')

    # Read the data either from a given morphology file or from a circuit
    if bpy.context.scene.NMV_InputSource == nmv.enums.Input.MORPHOLOGY_FILE:
        morphology_file_row = panel.layout.row()
        morphology_file_row.prop(scene, 'NMV_MorphologyFile')
        options.morphology.morphology_file_path = scene.NMV_MorphologyFile
    elif bpy.context.scene.NMV_InputSource == nmv.enums.Input.CIRCUIT_GID:
        circuit_file_row = panel.layout.row()
        circuit_file_row.prop(scene, 'NMV_CircuitFile')
        gid_row = panel.layout.row()
        gid_row.prop(scene, 'NMV_Gid')
    else:
        # Otherwise, report an invalid input source errors
        panel.report({'ERROR'}, 'Invalid Input Source')

    # Center the morphology at the origin
    centering_check_box = panel.layout.row()
    centering_check_box.prop(scene, 'NMV_CenterMorphologyAtOrigin')
    options.morphology.center_at_origin = scene.NMV_CenterMorphologyAtOrigin


####################################################################################################
# @draw_morphology_loading_button
####################################################################################################
def draw_morphology_loading_button(panel):

    load_morphology_button = panel.layout.column()
    load_morphology_button.operator('nmv.load_morphology', icon='ANIM_DATA')
    load_morphology_button.separator()


####################################################################################################
# @draw_morphology_loading_statistics
####################################################################################################
def draw_morphology_loading_statistics(panel,
                                       scene,
                                       morphology_object):

    # Display the loading statistics after loading the morphology
    if morphology_object is not None:
        morphology_stats_row = panel.layout.row()
        morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')

        # Loading time
        loading_time_row = panel.layout.row()
        loading_time_row.prop(scene, 'NMV_MorphologyLoadingTime')
        loading_time_row.enabled = False

        # Drawing time
        drawing_time_row = panel.layout.row()
        drawing_time_row.prop(scene, 'NMV_MorphologyDrawingTime')
        drawing_time_row.enabled = False


####################################################################################################
# @draw_output_options
####################################################################################################
def draw_output_options(panel,
                        scene,
                        options):
    # Output options
    output_data_options_row = panel.layout.row()
    output_data_options_row.label(text='Output Options:', icon='SCRIPT')

    # Output directory
    output_directory_row = panel.layout.row()
    output_directory_row.prop(scene, 'NMV_OutputDirectory')

    # Default paths
    default_paths_row = panel.layout.row()
    default_paths_row.prop(scene, 'NMV_DefaultArtifactsRelativePath')

    # Images path
    images_path_row = panel.layout.row()
    images_path_row.prop(scene, 'NMV_ImagesPath')

    # Sequences path
    sequences_path_row = panel.layout.row()
    sequences_path_row.prop(scene, 'NMV_SequencesPath')

    # Meshes path
    meshes_path_row = panel.layout.row()
    meshes_path_row.prop(scene, 'NMV_MeshesPath')

    # Morphologies path
    morphologies_path_row = panel.layout.row()
    morphologies_path_row.prop(scene, 'NMV_MorphologiesPath')

    # Analysis path
    analysis_path_row = panel.layout.row()
    analysis_path_row.prop(scene, 'NMV_AnalysisPath')

    # Stats. path
    stats_path_row = panel.layout.row()
    stats_path_row.prop(scene, 'NMV_StatisticsPath')

    # Disable the default paths selection if the use default paths flag is set
    if scene.NMV_DefaultArtifactsRelativePath:
        images_path_row.enabled = False
        sequences_path_row.enabled = False
        meshes_path_row.enabled = False
        morphologies_path_row.enabled = False
        analysis_path_row.enabled = False
        stats_path_row.enabled = False

    # Pass options from UI to system
    if 'Select Directory' in scene.NMV_OutputDirectory:
        options.io.output_directory = None
    else:
        output_dir = scene.NMV_OutputDirectory
        options.io.output_directory = output_dir
        options.io.images_directory = '%s/%s' % (output_dir, scene.NMV_ImagesPath)
        options.io.sequences_directory = '%s/%s' % (output_dir, scene.NMV_SequencesPath)
        options.io.morphologies_directory = '%s/%s' % (output_dir, scene.NMV_MorphologiesPath)
        options.io.meshes_directory = '%s/%s' % (output_dir, scene.NMV_MeshesPath)
        options.io.analysis_directory = '%s/%s' % (output_dir, scene.NMV_AnalysisPath)
        options.io.statistics_directory = '%s/%s' % (output_dir, scene.NMV_StatisticsPath)


