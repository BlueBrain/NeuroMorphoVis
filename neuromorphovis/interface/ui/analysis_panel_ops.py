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
def get_arbor_label_with_spaces_from_prefix(arbor_prefix):

    if 'ApicalDendrite' in arbor_prefix:
        return 'Apical Dendrite'
    elif 'BasalDendrite' in arbor_prefix:
        i = arbor_prefix.split('BasalDendrite')[1]
        return 'Basal Dendrite %s' % i
    elif 'Axon' in arbor_prefix:
        return 'Axon'
    else:
        return 'ERROR'


####################################################################################################
# @register_arbor_checkbox
####################################################################################################
def register_arbor_checkbox(arbor_prefix,
                            description):
    """Register each arbor checkbox.

    :param arbor_prefix:
        The prefix 'in string format' that is used to tag or identify the arbor.
    :param description:
        The tooltip description of the checkbox.
    """
    setattr(bpy.types.Scene, '%s' % arbor_prefix,
            BoolProperty(name=get_arbor_label_with_spaces_from_prefix(arbor_prefix),
                         description=description, default=True))


####################################################################################################
# @register_morphology_ui_entries
####################################################################################################
def register_morphology_ui_entries(morphology):
    """Registers the analysis entries that correspond to the available morphology neurites.

    :param morphology:
        Loaded morphology.
    """

    # Apical dendrite
    if morphology.apical_dendrite is not None:

        # Register the checkbox
        register_arbor_checkbox(arbor_prefix=morphology.apical_dendrite.get_type_prefix(),
                                description='Show the analysis data of %s' %
                                            morphology.apical_dendrite.get_type_label())
        # Register each entry
        for item in nmv.analysis.items:
            item.register_ui_entry(arbor_prefix=morphology.apical_dendrite.get_type_prefix())

    # Basal dendrites
    if morphology.dendrites is not None:

        # For each basal dendrite
        for i, basal_dendrite in enumerate(morphology.dendrites):

            # Register the checkbox
            register_arbor_checkbox(arbor_prefix='%s%i' % (basal_dendrite.get_type_prefix(), i),
                                    description='Show the analysis data of %s %d' %
                                                (basal_dendrite.get_type_label(), i))

            # Register each entry
            for entry in nmv.analysis.per_arbor:
                entry.register_ui_entry(arbor_prefix='%s%i' % (basal_dendrite.get_type_prefix(), i))

    # Axon
    if morphology.axon is not None:

        # Register the checkbox
        register_arbor_checkbox(arbor_prefix=morphology.axon.get_type_prefix(),
                                description='Show the analysis data of %s' %
                                            morphology.axon.get_type_label())

        # Register each entry
        for entry in nmv.analysis.per_arbor:
            entry.register_ui_entry(arbor_prefix=morphology.axon.get_type_prefix())


####################################################################################################
# @add_analysis_group_to_panel
####################################################################################################
def add_analysis_group_to_panel(arbor,
                                layout,
                                context):
    """Adds the results of analysis of each arbor to the UI.

    :param arbor_prefix:
        The prefix 'in string format' that is used to tag or identify the arbor.
    :param layout:
        UI panel layout.
    :param context:
        Blender context.
    """

    # Create a column outline in the panel
    outline = layout.column()

    arbor_prefix = arbor.get_type_prefix()
    # Add a label that identifies the arbor
    # outline.label(text='%s:' % get_arbor_label_with_spaces_from_prefix(arbor_prefix))

    # outline.prop(context.scene, arbor_prefix)

    if True: # getattr(context.scene, arbor_prefix):

        # Create a sub-column that aligns the analysis data from the original outline
        analysis_area = outline.column(align=True)

        # Update the analysis area with all the filters
        for item in nmv.analysis.items:

            # Update the UI entry s
            # item.update_ui_entry(arbor_prefix, analysis_area, context)

            layout.prop(context.scene, '%s%s' % (arbor.get_type_prefix(), item.variable))

        # Disable editing the analysis area
        analysis_area.enabled = False


####################################################################################################
# @add_analysis_output_to_panel
####################################################################################################
def add_analysis_output_to_panel(morphology,
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

    # Apical dendrite
    if morphology.apical_dendrite is not None:

        # Add the analysis results to the panel
        add_analysis_group_to_panel(
            arbor=morphology.apical_dendrite, layout=layout,context=context)

    """
    # Basal dendrites
    if morphology.dendrites is not None:

        # For each basal dendrite
        for i, basal_dendrite in enumerate(morphology.dendrites):

            # Add the analysis results to the panel
            add_analysis_group_to_panel(
                arbor_prefix='%s%i' % (basal_dendrite.get_type_prefix(), i), layout=layout,
                context=context)
    """
    # Axon
    if morphology.axon is not None:

        # Add the analysis results to the panel
        add_analysis_group_to_panel(
            arbor=morphology.axon, layout=layout, context=context)






def add_analysis_result_to_panel(layout,
                                 context):

    # morphology


    # apical dendrite

    # Create a column outline in the panel
    outline = layout.column()

    # Add a label that identifies the arbor
    # outline.label(text='%s:' % get_arbor_label_with_spaces_from_prefix(arbor_prefix))

    # Create a sub-column that aligns the analysis data from the original outline
    analysis_area = outline.column(align=True)

    # Update the analysis area with all the filters
    for item in nmv.analysis.items:

        # Get the result

        # update the ui entry


        # Update the UI entry s
        item.update_ui_entry('ApicalDendrite', analysis_area, context)

    # basal dendrites

    # axon



    return