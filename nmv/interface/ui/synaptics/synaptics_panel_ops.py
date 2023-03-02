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
from mathutils import Vector

# Internal imports
import nmv.consts
import nmv.enums
import nmv.bbp


####################################################################################################
# @draw_excitatory_synapses_color
####################################################################################################
def draw_excitatory_synapses_color(layout,
                                   scene,
                                   options):

    # Excitatory synapses color option
    color_row = layout.row()
    color_row.prop(scene, 'NMV_ExcitatorySynapsesColor')
    options.synaptics.excitatory_synapses_color = scene.NMV_ExcitatorySynapsesColor


####################################################################################################
# @draw_inhibitory_synapses_color
####################################################################################################
def draw_inhibitory_synapses_color(layout,
                                   scene,
                                   options):

    # Excitatory synapses color option
    color_row = layout.row()
    color_row.prop(scene, 'NMV_InhibitorySynapsesColor')
    options.synaptics.inhibitory_synapses_color = scene.NMV_InhibitorySynapsesColor


####################################################################################################
# @draw_excitatory_options
####################################################################################################
def draw_excitatory_options(layout,
                            scene,
                            options):

    draw_excitatory_synapses_color(
        layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_inhibitory_options
####################################################################################################
def draw_inhibitory_options(layout,
                            scene,
                            options):

    draw_inhibitory_synapses_color(
        layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_excitatory_and_inhibitory_options
####################################################################################################
def draw_excitatory_and_inhibitory_options(layout,
                                           scene,
                                           options):
    draw_excitatory_synapses_color(
        layout=layout, scene=scene, options=options)

    draw_inhibitory_synapses_color(
        layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_synapses_color_option
####################################################################################################
def draw_synapses_color_option(layout,
                               scene,
                               options):

    # Excitatory synapses color option
    color_row = layout.row()
    color_row.prop(scene, 'NMV_SynapsesColor')
    options.synaptics.synapses_color = scene.NMV_SynapsesColor


####################################################################################################
# @draw_mtype_color_palette
####################################################################################################
def draw_mtype_color_palette(layout,
                             scene,
                             options):

    # Get the default palette of all the mtypes
    mtypes = nmv.bbp.get_all_mtypes_in_circuit(circuit_config=options.morphology.blue_config)
    print(mtypes)

    pass


####################################################################################################
# @draw_etype_color_palette
####################################################################################################
def draw_etype_color_palette(layout,
                             scene,
                             options):

    # Get the default palette of all the mtypes
    etypes = nmv.bbp.get_all_etypes_in_circuit(circuit_config=options.morphology.blue_config)
    print(etypes)


    pass


####################################################################################################
# @draw_afferent_options
####################################################################################################
def draw_afferent_options(layout,
                          scene,
                          options):

    color_scheme_row = layout.row()
    color_scheme_row.prop(scene, 'NMV_AfferentColorCoding')
    options.synaptics.afferent_color_coding = scene.NMV_AfferentColorCoding

    scheme = options.synaptics.afferent_color_coding
    if scheme == nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR:
        draw_synapses_color_option(
            layout=layout, scene=scene, options=options)
    elif scheme == nmv.enums.Synaptics.ColorCoding.COLOR_CODED_PRE_SYNAPTIC_MTYPE:
        print('1')
        #draw_mtype_color_palette(
        #    layout=layout, scene=scene, options=options)
    elif scheme == nmv.enums.Synaptics.ColorCoding.COLOR_CODED_PRE_SYNAPTIC_ETYPE:
        print('2')
        #draw_etype_color_palette(
        #    layout=layout, scene=scene, options=options)
















def draw_efferent_options(layout,
                          scene,
                          synaptics_options):

    color_scheme_row = layout.row()
    color_scheme_row.prop(scene, 'NMV_EfferentColorCoding')
    synaptics_options.efferent_color_coding = scene.NMV_EfferentColorCoding



def draw_afferent_and_efferent_options(layout,
                                       scene,
                                       synaptics_options):

    color_scheme_row = layout.row()
    color_scheme_row.prop(scene, 'NMV_AfferentAndEfferentColorCoding')



def draw_specific_color_coded_set_options(layout,
                                          scene,
                                          synaptics_options):

    color_scheme_row = layout.row()
    color_scheme_row.prop(scene, 'NMV_SpecificColorCoding')
