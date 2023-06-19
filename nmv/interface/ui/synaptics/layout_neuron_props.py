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


####################################################################################################
# @draw_neuron_options_header
####################################################################################################
def draw_neuron_options_header(layout):

    row = layout.row()
    row.label(text='Neuron Options', icon='OUTLINER_OB_EMPTY')


####################################################################################################
# @draw_neuron_radius_option
####################################################################################################
def draw_neuron_radius_option(layout, scene, options):

    neuron_radius_row = layout.row()
    unify_radius_column = neuron_radius_row.column()
    unify_radius_column.prop(scene, 'NMV_SynapticsUnifyRadius')
    options.synaptics.unify_branch_radii = scene.NMV_SynapticsUnifyRadius

    unified_radius_column = neuron_radius_row.column()
    unified_radius_column.prop(scene, 'NMV_SynapticsUnifiedNeuronRadius')
    options.synaptics.unified_radius = scene.NMV_SynapticsUnifiedNeuronRadius

    # Disable the options if all arbors are not selected for display
    if not options.synaptics.display_axons and not options.synaptics.display_dendrites:
        unify_radius_column.enabled = False
        unified_radius_column.enabled = False

    # Disable the column
    unified_radius_column.enabled = False if not scene.NMV_SynapticsUnifyRadius else True


####################################################################################################
# @draw_dendrites_options
####################################################################################################
def draw_dendrites_options(layout, scene, options):

    dendrites_row = layout.row()
    add_dendrites_column = dendrites_row.column()
    add_dendrites_column.prop(scene, 'NMV_DisplayDendrites')
    options.synaptics.display_dendrites = scene.NMV_DisplayDendrites

    dendrites_options_column = dendrites_row.column()
    dendrites_options_column.prop(scene, 'NMV_SynapticsDendritesColor')
    options.synaptics.dendrites_color = scene.NMV_SynapticsDendritesColor

    dendrites_options_column.enabled = True if scene.NMV_DisplayDendrites else False


####################################################################################################
# @draw_axons_options
####################################################################################################
def draw_axons_options(layout, scene, options):

    axons_row = layout.row()
    add_axons_column = axons_row.column()
    add_axons_column.prop(scene, 'NMV_DisplayAxons')
    options.synaptics.display_axons = scene.NMV_DisplayAxons

    axons_options_column = axons_row.column()
    axons_options_column.prop(scene, 'NMV_SynapticsAxonsColor')
    options.synaptics.axons_color = scene.NMV_SynapticsAxonsColor

    axons_options_column.enabled = True if scene.NMV_DisplayAxons else False


####################################################################################################
# @draw_single_neuron_options
####################################################################################################
def draw_single_neuron_options(layout, scene, options):

    draw_neuron_options_header(layout=layout)
    draw_dendrites_options(layout=layout, scene=scene, options=options)
    draw_axons_options(layout=layout, scene=scene, options=options)
    draw_neuron_radius_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_pre_synaptic_dendrites_options
####################################################################################################
def draw_pre_synaptic_dendrites_options(layout, scene, options):

    pre_dendrites_row = layout.row()
    add_dendrites_column = pre_dendrites_row.column()
    add_dendrites_column.prop(scene, 'NMV_DisplayPreSynapticDendrites')
    options.synaptics.display_pre_synaptic_dendrites = scene.NMV_DisplayPreSynapticDendrites

    dendrites_options_column = pre_dendrites_row.column()
    dendrites_options_column.prop(scene, 'NMV_PreSynapticDendritesColor')
    options.synaptics.pre_synaptic_dendrites_color = scene.NMV_PreSynapticDendritesColor

    dendrites_options_column.enabled = True if scene.NMV_DisplayPreSynapticDendrites else False


####################################################################################################
# @draw_pre_synaptic_axons_options
####################################################################################################
def draw_pre_synaptic_axons_options(layout, scene, options):

    pre_axons_row = layout.row()
    add_axons_column = pre_axons_row.column()
    add_axons_column.prop(scene, 'NMV_DisplayPreSynapticAxons')
    options.synaptics.display_pre_synaptic_axons = scene.NMV_DisplayPreSynapticAxons

    axons_options_column = pre_axons_row.column()
    axons_options_column.prop(scene, 'NMV_PreSynapticAxonsColor')
    options.synaptics.pre_synaptic_axons_color = scene.NMV_PreSynapticAxonsColor

    axons_options_column.enabled = True if scene.NMV_DisplayPreSynapticAxons else False


####################################################################################################
# @draw_post_synaptic_dendrites_options
####################################################################################################
def draw_post_synaptic_dendrites_options(layout, scene, options):

    post_dendrites_row = layout.row()
    add_dendrites_column = post_dendrites_row.column()
    add_dendrites_column.prop(scene, 'NMV_DisplayPostSynapticDendrites')
    options.synaptics.display_post_synaptic_dendrites = scene.NMV_DisplayPostSynapticDendrites

    dendrites_options_column = post_dendrites_row.column()
    dendrites_options_column.prop(scene, 'NMV_PostSynapticDendritesColor')
    options.synaptics.post_synaptic_dendrites_color = scene.NMV_PostSynapticDendritesColor
    dendrites_options_column.enabled = True if scene.NMV_DisplayPostSynapticDendrites else False


####################################################################################################
# @draw_post_synaptic_axons_options
####################################################################################################
def draw_post_synaptic_axons_options(layout, scene, options):
    axons_row = layout.row()
    add_axons_column = axons_row.column()
    add_axons_column.prop(scene, 'NMV_DisplayPostSynapticAxons')
    options.synaptics.display_post_synaptic_axons = scene.NMV_DisplayPostSynapticAxons

    axons_options_column = axons_row.column()
    axons_options_column.prop(scene, 'NMV_PostSynapticAxonsColor')
    options.synaptics.post_synaptic_axons_color = scene.NMV_PostSynapticAxonsColor

    axons_options_column.enabled = True if scene.NMV_DisplayPostSynapticAxons else False


####################################################################################################
# @draw_neuron_pair_options
####################################################################################################
def draw_neuron_pair_options(layout, scene, options):

    draw_neuron_options_header(layout=layout)

    draw_pre_synaptic_dendrites_options(layout=layout, scene=scene, options=options)
    draw_pre_synaptic_axons_options(layout=layout, scene=scene, options=options)
    draw_post_synaptic_dendrites_options(layout=layout, scene=scene, options=options)
    draw_post_synaptic_axons_options(layout=layout, scene=scene, options=options)

    draw_neuron_radius_option(layout, scene, options)
