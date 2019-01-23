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
from bpy.props import BoolProperty

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.analysis


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
                            description):
    """For each arbor or neurite in the morphology, there will be a checkbox to show and hide the
    analysis data group.

    This feature is added to reduce any clutter if the number of analysis entries are huge.
    Note that the morphology group will be check by default, in contrast to the arbors.

    :param prefix:
        The prefix 'in string format' that is used to tag or identify the arbor.
    :param description:
        The tooltip description of the checkbox.
    """

    # By default show the morphology analysis group (set its checkbox)
    if 'Morphology' in prefix:
        setattr(bpy.types.Scene, '%s' % prefix,
                BoolProperty(name='Morphology', description=description, default=True))

    # By default hide the arbors analysis groups (unset their checkboxes)
    else:
        setattr(bpy.types.Scene, '%s' % prefix,
                BoolProperty(name=get_label_from_prefix(prefix), description=description,
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

    # Apical dendrite
    if morphology.apical_dendrite is not None:

        # Register the group checkbox of the 'Apical Dendrite'
        register_group_checkbox(prefix=morphology.apical_dendrite.get_type_prefix(),
                                description='Show the analysis data of %s' %
                                            morphology.apical_dendrite.get_type_label())
    # Basal dendrites
    if morphology.dendrites is not None:

        # For each basal dendrite
        for i, basal_dendrite in enumerate(morphology.dendrites):

            # Register the group checkbox of the 'Basal Dendrite i'
            register_group_checkbox(prefix='%s%i' % (basal_dendrite.get_type_prefix(), i),
                                    description='Show the analysis data of %s %d' %
                                                (basal_dendrite.get_type_label(), i))
    # Axon
    if morphology.axon is not None:

        # Register the group checkbox of the 'Axon'
        register_group_checkbox(prefix=morphology.axon.get_type_prefix(),
                                description='Show the analysis data of %s' %
                                            morphology.axon.get_type_label())


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

        # Update the analysis area with all the filters
        for item in nmv.analysis.ui_analysis_items:

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

    # Morphology
    add_analysis_group_to_panel(prefix='Morphology', layout=layout, context=context)

    # Apical dendrite
    if morphology.apical_dendrite is not None:

        # Add the analysis results to the panel
        add_analysis_group_to_panel(
            prefix=morphology.apical_dendrite.get_type_prefix(), layout=layout, context=context)

    # Basal dendrites
    if morphology.dendrites is not None:

        # For each basal dendrite
        for i, basal_dendrite in enumerate(morphology.dendrites):

            # Add the analysis results to the panel
            add_analysis_group_to_panel(
                prefix='%s%i' % (basal_dendrite.get_type_prefix(), i), layout=layout,
                context=context)

    # Axon
    if morphology.axon is not None:

        # Add the analysis results to the panel
        add_analysis_group_to_panel(
            prefix=morphology.axon.get_type_prefix(), layout=layout, context=context)


####################################################################################################
# @update_bounding_box_panel
####################################################################################################
def update_bounding_box_panel(current_scene,
                              bbox):
    """Update the bounding box panel

    :param current_scene:
        Current scene.
    :param bbox:
        Bounding box.
    """

    # PMin
    current_scene.BBoxPMinX = bbox.p_min[0]
    current_scene.BBoxPMinY = bbox.p_min[1]
    current_scene.BBoxPMinZ = bbox.p_min[2]

    # PMax
    current_scene.BBoxPMaxX = bbox.p_max[0]
    current_scene.BBoxPMaxY = bbox.p_max[1]
    current_scene.BBoxPMaxZ = bbox.p_max[2]

    # Center
    current_scene.BBoxCenterX = bbox.center[0]
    current_scene.BBoxCenterY = bbox.center[1]
    current_scene.BBoxCenterZ = bbox.center[2]

    # Bounds
    current_scene.BoundsX = bbox.bounds[0]
    current_scene.BoundsY = bbox.bounds[1]
    current_scene.BoundsZ = bbox.bounds[2]


####################################################################################################
# set_bounding_box_options
####################################################################################################
def set_bounding_box_options(layout,
                             scene,
                             options):
    """Morphology bounding box information.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Bounding box options
    bounding_box_row = layout.row()
    bounding_box_row.label(text='Morphology Bounding Box:', icon='BORDER_RECT')

    # Display bounding box option
    bounding_box_p_row = layout.row()
    bounding_box_p_min_row = bounding_box_p_row.column(align=True)
    bounding_box_p_min_row.label(text='PMin:')
    bounding_box_p_min_row.prop(scene, 'BBoxPMinX')
    bounding_box_p_min_row.prop(scene, 'BBoxPMinY')
    bounding_box_p_min_row.prop(scene, 'BBoxPMinZ')
    bounding_box_p_min_row.enabled = False

    bounding_box_p_max_row = bounding_box_p_row.column(align=True)
    bounding_box_p_max_row.label(text='PMax:')
    bounding_box_p_max_row.prop(scene, 'BBoxPMaxX')
    bounding_box_p_max_row.prop(scene, 'BBoxPMaxY')
    bounding_box_p_max_row.prop(scene, 'BBoxPMaxZ')
    bounding_box_p_max_row.enabled = False

    bounding_box_data_row = layout.row()
    bounding_box_center_row = bounding_box_data_row.column(align=True)
    bounding_box_center_row.label(text='Center:')
    bounding_box_center_row.prop(scene, 'BBoxCenterX')
    bounding_box_center_row.prop(scene, 'BBoxCenterY')
    bounding_box_center_row.prop(scene, 'BBoxCenterZ')
    bounding_box_center_row.enabled = False

    bounding_box_bounds_row = bounding_box_data_row.column(align=True)
    bounding_box_bounds_row.label(text='Bounds:')
    bounding_box_bounds_row.prop(scene, 'BoundsX')
    bounding_box_bounds_row.prop(scene, 'BoundsY')
    bounding_box_bounds_row.prop(scene, 'BoundsZ')
    bounding_box_bounds_row.enabled = False


####################################################################################################
# @analyze_morphology
####################################################################################################
def analyze_morphology(morphology,
                       context):
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

        # Register the morphology variables to be able to show and update them on the UI
        for item in nmv.analysis.ui_analysis_items:
            item.register_analysis_variables(morphology=morphology)

        # Apply the analysis filters and update the results
        for item in nmv.analysis.ui_analysis_items:
            item.apply_analysis_kernel(morphology=morphology, context=context)

        # Morphology is analyzed
        return True

    except ValueError:

        # Morphology could not be analyzed
        return False
