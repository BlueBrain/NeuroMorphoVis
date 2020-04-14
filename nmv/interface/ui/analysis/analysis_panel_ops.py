####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
import nmv.analysis
import nmv.builders
import nmv.scene
import nmv.enums
import nmv.consts


####################################################################################################
# @get_arbor_label_with_spaces_from_prefix
####################################################################################################
def get_label_from_prefix(prefix):
    """Gets a nice label for the UI of a component from a given prefix.

    Examples:
    * Prefix: 'ApicalDendrite' -> Label: 'Apical Dendrite'
    * Prefix: 'BasalDendrite0' -> Label: 'Basal Dendrite 0'

    :param prefix:
        Component prefix.
    :return:
        Component label that can be used to tag a UI element.
    """

    if 'ApicalDendrite' in prefix:
        return 'Apical Dendrite'
    elif 'BasalDendrite' in prefix:
        i = prefix.split('BasalDendrite')[1]
        return 'Basal Dendrite %s' % i
    elif 'Axon' in prefix:
        return 'Axon'
    elif 'Morphology' in prefix:
        return 'Morphology'
    else:
        return 'ERROR'


####################################################################################################
# @register_group_checkbox
####################################################################################################
def register_group_checkbox(prefix,
                            description,
                            label=''):
    """For each arbor in the morphology, there will be a checkbox to show and hide the analysis
    data group.

    This feature is added to reduce any clutter if the number of analysis entries are huge.
    Note that the morphology group will be checked by default, in contrast to the arbors.

    :param prefix:
        The prefix 'in string format' that is used to tag or identify the arbor.
    :param label:
        The label of the arbor.
    :param description:
        The tooltip description of the checkbox.
    """

    # By default show the morphology analysis group (set its checkbox)
    if 'Morphology' in prefix:
        setattr(bpy.types.Scene, '%s' % prefix,
                BoolProperty(name='Morphology', description=description, default=True))

    # This one is for the soma
    elif 'Soma' in prefix:
        setattr(bpy.types.Scene, '%s' % prefix,
                BoolProperty(name='Soma', description=description, default=False))

    # By default hide the arbors analysis groups (unset their checkboxes)
    else:
        setattr(bpy.types.Scene, '%s' % prefix,
                BoolProperty(name=label, description=description,
                             default=False))


####################################################################################################
# @register_analysis_groups
####################################################################################################
def register_analysis_groups(morphology):
    """Registers the analysis groups of the morphology.

    :param morphology:
        Loaded morphology.
    """

    # Register the checkbox of the 'Morphology' group
    register_group_checkbox(prefix='Morphology',
                            description='Show the analysis data of the entire morphology')

    # Register the checkbox of the 'Soma' group
    register_group_checkbox(prefix='Soma', description='Show the analysis data of the soma')

    # Register the group checkbox of the 'Apical Dendrites', if exist
    if morphology.has_apical_dendrites():
        for arbor in morphology.apical_dendrites:
            register_group_checkbox(
                prefix=arbor.tag,
                description='Show the analysis data of %s' % arbor.label,
                label=arbor.label)

    # Register the group checkboxes of the Basal Dendrites, if exist
    if morphology.has_basal_dendrites():
        for arbor in morphology.basal_dendrites:
            register_group_checkbox(
                prefix=arbor.tag,
                description='Show the analysis data of %s' % arbor.label,
                label=arbor.label)

    # Register the group checkboxes of the Axons, if exist
    if morphology.has_axons():
        for arbor in morphology.axons:
            register_group_checkbox(
                prefix=arbor.tag,
                description='Show the analysis data of %s' % arbor.label,
                label=arbor.label)


####################################################################################################
# @add_analysis_group_to_panel
####################################################################################################
def add_analysis_group_to_panel(prefix,
                                layout,
                                context):
    """Adds the results of analysis of each arbor to the UI.

    :param prefix:
        The prefix 'in string format' that is used to tag or identify the arbor.
    :param layout:
        UI panel layout.
    :param context:
        Blender context.
    """

    # Create a column outline in the panel
    outline = layout.column()

    # Add the checkbox that was registered before to show/hide the group @register_group_checkbox
    outline.prop(context.scene, prefix)

    # If the checkbox is checked
    if getattr(context.scene, prefix):

        # Create a sub-column that aligns the analysis data from the original outline
        analysis_area = outline.column(align=True)

        # In case of showing the analysis results of the entire morphology, add the
        # results of the global analysis before the common ones
        if 'Morphology' in prefix:
            for item in nmv.analysis.ui_global_analysis_items:
                analysis_area.prop(context.scene, '%s' % item.variable)

        # Update the analysis area with all the filters, that are common
        for item in nmv.analysis.ui_per_arbor_analysis_items:
            analysis_area.prop(context.scene, '%s%s' % (prefix, item.variable))

        # Disable editing the analysis area
        analysis_area.enabled = False


####################################################################################################
# @add_analysis_groups_to_panel
####################################################################################################
def add_analysis_groups_to_panel(morphology,
                                 layout,
                                 context):
    """Adds the results of the morphology analysis to the UI.

    :param morphology:
        Loaded morphology.
    :param layout:
        UI panel layout.
    :param context:
        Blender context.
    """

    # Bounding box information
    add_bounding_box_information_to_panel(morphology=morphology, layout=layout, scene=context.scene)

    # Morphology
    add_analysis_group_to_panel(prefix='Morphology', layout=layout, context=context)

    # Add the analysis results of the Apical Dendrites to the panel
    if morphology.has_apical_dendrites():
        for arbor in morphology.apical_dendrites:
            add_analysis_group_to_panel(prefix=arbor.tag, layout=layout, context=context)

    # Add the analysis results of the Basal Dendrites to the panel
    if morphology.basal_dendrites is not None:
        for arbor in morphology.basal_dendrites:
            add_analysis_group_to_panel(prefix=arbor.tag, layout=layout, context=context)

    # Add the analysis results of the Axons to the panel
    if morphology.has_axons():
        for arbor in morphology.axons:
            add_analysis_group_to_panel(prefix=arbor.tag, layout=layout, context=context)


####################################################################################################
# @add_bounding_box_information_to_panel
####################################################################################################
def add_bounding_box_information_to_panel(morphology,
                                          layout,
                                          scene):
    """Computes the bounding box information of the morphology and adds them to the analysis panel.

    :param morphology:
        The input morphology being analyzed.
    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    """

    # Draw the bounding box
    bounding_box_p_row = layout.row()
    bounding_box_p_min_row = bounding_box_p_row.column(align=True)
    bounding_box_p_min_row.label(text='BBox PMin:')
    bounding_box_p_min_row.prop(scene, 'NMV_BBoxPMinX')
    bounding_box_p_min_row.prop(scene, 'NMV_BBoxPMinY')
    bounding_box_p_min_row.prop(scene, 'NMV_BBoxPMinZ')
    bounding_box_p_min_row.enabled = False

    bounding_box_p_max_row = bounding_box_p_row.column(align=True)
    bounding_box_p_max_row.label(text='BBox PMax:')
    bounding_box_p_max_row.prop(scene, 'NMV_BBoxPMaxX')
    bounding_box_p_max_row.prop(scene, 'NMV_BBoxPMaxY')
    bounding_box_p_max_row.prop(scene, 'NMV_BBoxPMaxZ')
    bounding_box_p_max_row.enabled = False

    bounding_box_data_row = layout.row()
    bounding_box_center_row = bounding_box_data_row.column(align=True)
    bounding_box_center_row.label(text='BBox Center:')
    bounding_box_center_row.prop(scene, 'NMV_BBoxCenterX')
    bounding_box_center_row.prop(scene, 'NMV_BBoxCenterY')
    bounding_box_center_row.prop(scene, 'NMV_BBoxCenterZ')
    bounding_box_center_row.enabled = False

    bounding_box_bounds_row = bounding_box_data_row.column(align=True)
    bounding_box_bounds_row.label(text='BBox Bounds:')
    bounding_box_bounds_row.prop(scene, 'NMV_BoundsX')
    bounding_box_bounds_row.prop(scene, 'NMV_BoundsY')
    bounding_box_bounds_row.prop(scene, 'NMV_BoundsZ')
    bounding_box_bounds_row.enabled = False


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

    try:
        # Register the different analysis groups
        register_analysis_groups(morphology=morphology)

        # Register the global morphology variables to be able to show and update them on the UI
        for item in nmv.analysis.ui_global_analysis_items:
            item.register_global_analysis_variables(morphology=morphology)

        # Register the per-arbor variables to be able to show and update them on the UI
        for item in nmv.analysis.ui_per_arbor_analysis_items:
            item.register_per_arbor_analysis_variables(morphology=morphology)

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
