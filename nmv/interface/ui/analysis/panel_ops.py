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
import copy

# Internal imports
import nmv.analysis
import nmv.builders
import nmv.scene
import nmv.enums
import nmv.consts
import nmv.interface


####################################################################################################
# @analyze_bounding_box
####################################################################################################
def analyze_bounding_box(morphology,
                         scene):
    """Analyzes the bounding nox of the morphology and copies the results to the context variables.

    :param morphology:
        Given morphology to be analyzed.
    :param scene:
        Context scene.
    """

    # Computes the bounding box to double confirm the results
    morphology.compute_bounding_box()

    # Copy the values to the context variables
    scene.NMV_BBoxPMinX = morphology.bounding_box.p_min[0]
    scene.NMV_BBoxPMinY = morphology.bounding_box.p_min[1]
    scene.NMV_BBoxPMinZ = morphology.bounding_box.p_min[2]
    scene.NMV_BBoxPMaxX = morphology.bounding_box.p_max[0]
    scene.NMV_BBoxPMaxY = morphology.bounding_box.p_max[1]
    scene.NMV_BBoxPMaxZ = morphology.bounding_box.p_max[2]
    scene.NMV_BBoxCenterX = morphology.bounding_box.center[0]
    scene.NMV_BBoxCenterY = morphology.bounding_box.center[1]
    scene.NMV_BBoxCenterZ = morphology.bounding_box.center[2]
    scene.NMV_BoundsX = morphology.bounding_box.bounds[0]
    scene.NMV_BoundsY = morphology.bounding_box.bounds[1]
    scene.NMV_BoundsZ = morphology.bounding_box.bounds[2]


####################################################################################################
# @analyze_morphology
####################################################################################################
def analyze_morphology(morphology,
                       context=None):
    """Registers the different analysis components and then analyze the morphology.

    :param morphology:
        A given morphology to analyse.
    :param context:
        A bpy.context.
    :return:
        True if the morphology is analyzed, and False if not.
    """

    from .registration import register_analysis_groups

    try:
        # Register the different analysis groups
        register_analysis_groups(morphology=morphology)

        # Register the global morphology variables to be able to show and update them on the UI
        for item in nmv.analysis.ui_soma_analysis_items:
            item.register_global_analysis_variables(morphology=morphology)

        # Register the global morphology variables to be able to show and update them on the UI
        for item in nmv.analysis.ui_global_analysis_items:
            item.register_global_analysis_variables(morphology=morphology)

        # Register the per-arbor variables to be able to show and update them on the UI
        for item in nmv.analysis.ui_per_arbor_analysis_items:
            item.register_per_arbor_analysis_variables(morphology=morphology)

        # Apply the global analysis filters and update the results
        for item in nmv.analysis.ui_soma_analysis_items:
            item.apply_global_analysis_kernel(morphology=morphology, context=context)

        # Apply the global analysis filters and update the results
        for item in nmv.analysis.ui_global_analysis_items:
            item.apply_global_analysis_kernel(morphology=morphology, context=context)

        # Apply the per-arbor analysis filters and update the results
        for item in nmv.analysis.ui_per_arbor_analysis_items:
            item.apply_per_arbor_analysis_kernel(morphology=morphology, context=context)

        # Analyze the bounding box information
        if context is not None:
            analyze_bounding_box(morphology=morphology, scene=context.scene)

        # Morphology is analyzed
        return True

    except ValueError:

        # Morphology could not be analyzed
        return False


####################################################################################################
# @sketch_morphology_skeleton_guide
####################################################################################################
def sketch_morphology_skeleton_guide(morphology,
                                     options):
    """Sketches the morphology skeleton in a very raw or basic format to correlate the analysis
    results with it.

    :param morphology:
        Morphology skeleton.
    :param options:
        Instance of NMV options, but it will be modified here to account for the changes we must do.
    """

    # Set the morphology options to the default after they have been already initialized
    options.morphology.set_default()

    # Clear the scene
    nmv.scene.clear_scene()

    # Create a skeletonizer object to build the morphology skeleton
    options_clone = copy.deepcopy(options)
    options_clone.morphology.branching = nmv.enums.Skeleton.Branching.RADII
    builder = nmv.builders.ConnectedSectionsBuilder(morphology, options_clone)

    # Draw the morphology skeleton and return a list of all the reconstructed objects
    nmv.interface.ui_reconstructed_skeleton = builder.draw_morphology_skeleton()


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
