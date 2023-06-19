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

# Blender imports
import bpy


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

    # By default, show the morphology analysis group (set its checkbox)
    if 'Morphology' in prefix:
        setattr(bpy.types.Scene, '%s' % prefix,
                bpy.props.BoolProperty(name='Morphology', description=description, default=True))

    # Soma analysis
    elif 'Soma' in prefix:
        setattr(bpy.types.Scene, '%s' % prefix,
                bpy.props.BoolProperty(name='Soma', description=description, default=False))

    # By default, hide the arbors analysis groups (unset their checkboxes)
    else:
        setattr(bpy.types.Scene, '%s' % prefix,
                bpy.props.BoolProperty(name=label, description=description, default=False))


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
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    from .panel import NMV_AnalysisPanel
    from .ops_export import NMV_ExportAnalysisResults
    from .ops_export import NMV_CreateNeuronCard

    # Morphology analysis panel
    bpy.utils.register_class(NMV_AnalysisPanel)

    # Export analysis button
    bpy.utils.register_class(NMV_CreateNeuronCard)
    bpy.utils.register_class(NMV_ExportAnalysisResults)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    from .panel import NMV_AnalysisPanel
    from .ops_export import NMV_ExportAnalysisResults
    from .ops_export import NMV_CreateNeuronCard

    # Morphology analysis panel
    bpy.utils.unregister_class(NMV_AnalysisPanel)

    # Export analysis button
    bpy.utils.unregister_class(NMV_CreateNeuronCard)
    bpy.utils.unregister_class(NMV_ExportAnalysisResults)
