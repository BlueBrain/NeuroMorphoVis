####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Internal imports
import nmv.bbox
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.shading
import nmv.scene
import nmv.skeleton
import nmv.rendering
import nmv.utilities


####################################################################################################
# @plot_analysis_results
####################################################################################################
def plot_analysis_results(morphology,
                          options):
    """Plots the analysis results of the morphology.

    :param morphology:
        The morphology skeleton.
    :param options:
        NeuroMorphoVis options
    """

    # Create the color palette
    morphology.create_morphology_color_palette()

    # Ensure to set the branching order to maximum to draw the entire skeleton and dendrogram
    options_clone = copy.deepcopy(options)
    options_clone.morphology.adjust_to_analysis_mode()

    # Render a simplified dendrogram
    builder = nmv.builders.DendrogramBuilder(morphology=morphology, options=options_clone)
    nmv.scene.clear_scene()
    builder.render_highlighted_arbors(dendrogram_type=nmv.enums.Dendrogram.Type.SIMPLIFIED,
                                      resolution=3000)

    # Render a detailed dendrogram
    nmv.scene.clear_scene()
    builder = nmv.builders.DendrogramBuilder(morphology=morphology, options=options_clone)
    builder.render_highlighted_arbors(dendrogram_type=nmv.enums.Dendrogram.Type.DETAILED,
                                      resolution=5000)

    # Render the arbors
    nmv.scene.clear_scene()
    builder = nmv.builders.DisconnectedSectionsBuilder(morphology=morphology,
                                                       options=options_clone)
    builder.render_highlighted_arbors()

    # Apply the analysis kernels and compile the analysis distributions
    for distribution in nmv.analysis.distributions:
        distribution.apply_kernel(morphology=morphology, options=options)


####################################################################################################
# @export_analysis_results
####################################################################################################
def export_analysis_results(morphology,
                            options):
    """Export the analysis results into a file.

    :param morphology:
        The morphology that is analysed.
    :param options:
        NMV options.
    """

    # Create a specific directory per morphology
    morphology_analysis_directory = '%s/%s' % (options.io.analysis_directory, morphology.label)
    if not nmv.file.ops.path_exists(morphology_analysis_directory):
        nmv.file.ops.clean_and_create_directory(morphology_analysis_directory)

    # Analysis results
    analysis_results_string = '*' * 80 + '\n'
    analysis_results_string += 'WARNING: AUTO-GENERATED FILE FROM NEUROMORPHOVIS \n'
    analysis_results_string += '*' * 80 + '\n'
    analysis_results_string += '* Analysis results for the morphology [%s] \n\n' % morphology.label

    analysis_results_string += '- Contents \n'
    analysis_results_string += '\t* Soma: ' + 'Found \n' \
        if morphology.soma is not None else 'Not Found \n'

    if morphology.has_apical_dendrites():
        analysis_results_string += '\t* Apical Dendrites: %d \n' % len(morphology.apical_dendrites)
    else:
        analysis_results_string += '\t* Apical Dendrites: 0 \n'

    if morphology.has_basal_dendrites():
        analysis_results_string += '\t* Basal Dendrites: %d \n' % len(morphology.basal_dendrites)
    else:
        analysis_results_string += '\t* Basal Dendrites: 0 \n'

    if morphology.has_axons():
        analysis_results_string += '\t* Axons: %d \n\n' % len(morphology.axons)
    else:
        analysis_results_string += '\t* Axons: 0 \n\n'

    # Register the morphology variables to be able to show and update them on the UI
    for item in nmv.analysis.ui_per_arbor_analysis_items:
        analysis_results_string += item.write_analysis_results_to_string(morphology=morphology)

    # Write the text to file
    analysis_results_file = open('%s/%s.txt' % (morphology_analysis_directory,
                                                nmv.consts.Analysis.ANALYSIS_FILE_NAME), 'w')
    analysis_results_file.write(analysis_results_string)
    analysis_results_file.close()
