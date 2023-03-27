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
import nmv.bbp
import nmv.scene

from .layout_synapses_props import *
from .layout_neuron_props import *


####################################################################################################
# @draw_synaptics_reconstruction_button
####################################################################################################
def draw_synaptics_reconstruction_button(layout, scene):

    row = layout.row()
    row.operator('nmv.reconstruct_synaptics')

    if nmv.interface.ui_synaptics_reconstructed:
        row = layout.row()
        row.prop(scene, 'NMV_SynapticReconstructionTime')
        row.enabled = False


####################################################################################################
# @draw_synapses_options_header
####################################################################################################
def draw_synapses_options_header(layout):

    # Reconstruction options
    row = layout.row()
    row.label(text='Synapses Options', icon='OUTLINER_OB_EMPTY')


####################################################################################################
# @draw_synaptics_reconstruction_options
####################################################################################################
def draw_synaptics_reconstruction_options(layout, scene, options):

    # Header
    draw_synapses_options_header(layout=layout)

    # Use case
    use_case = options.synaptics.use_case
    if use_case == nmv.enums.Synaptics.UseCase.AFFERENT:
        draw_afferent_options(layout=layout, scene=scene, options=options)
        draw_common_options(layout=layout, scene=scene, options=options)
        layout.separator()

        draw_single_neuron_options(layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.EFFERENT:
        draw_efferent_options(layout=layout, scene=scene, options=options)
        draw_common_options(layout=layout, scene=scene, options=options)
        layout.separator()

        draw_single_neuron_options(layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.AFFERENT_AND_EFFERENT:
        draw_afferent_and_efferent_options(layout=layout, scene=scene, options=options)
        draw_common_options(layout=layout, scene=scene, options=options)
        layout.separator()

        draw_single_neuron_options(layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.EXCITATORY:
        draw_excitatory_options(layout=layout, scene=scene, options=options)
        draw_common_options(layout=layout, scene=scene, options=options)
        layout.separator()

        draw_single_neuron_options(layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.INHIBITORY:
        draw_inhibitory_options(layout=layout, scene=scene, options=options)
        draw_common_options(layout=layout, scene=scene, options=options)
        layout.separator()

        draw_single_neuron_options(layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.EXCITATORY_AND_INHIBITORY:
        draw_excitatory_and_inhibitory_options(layout=layout, scene=scene, options=options)
        draw_common_options(layout=layout, scene=scene, options=options)
        layout.separator()

        draw_single_neuron_options(layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.SPECIFIC_COLOR_CODED_SET:
        draw_specific_color_coded_set_options(layout=layout, scene=scene, options=options)
        draw_common_options(layout=layout, scene=scene, options=options)
        layout.separator()

        draw_single_neuron_options(layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.PATHWAY_PRE_SYNAPTIC:
        draw_pre_synaptic_pathway_options(layout=layout, scene=scene, options=options)
        draw_synapse_radius_options(layout=layout, scene=scene, options=options)
        layout.separator()

        draw_neuron_pair_options(layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.PATHWAY_POST_SYNAPTIC:
        draw_post_synaptic_pathway_options(layout=layout, scene=scene, options=options)
        draw_synapse_radius_options(layout=layout, scene=scene, options=options)
        layout.separator()

        draw_neuron_pair_options(layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.TARGETS:
        draw_synaptic_targets(layout=layout, scene=scene, options=options)
        layout.separator()

        draw_single_neuron_options(layout=layout, scene=scene, options=options)

    else:
        nmv.logger.log('UI_ERROR: draw_synaptics_reconstruction_options')
    layout.separator()

    # Common shading options
    draw_shading_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_out_of_context_message
####################################################################################################
def draw_out_of_context_message(layout, scene, options):

    message_row = layout.row()
    message_row.label(text='The Synaptics panel can ONLY be used with a circuit!')

