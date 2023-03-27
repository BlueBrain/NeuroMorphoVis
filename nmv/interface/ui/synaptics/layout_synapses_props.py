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

# Internal imports
import nmv.consts
import nmv.enums
import nmv.bbp
import nmv.scene


####################################################################################################
# @draw_shading_options_header
####################################################################################################
def draw_shading_options_header(layout):

    row = layout.row()
    row.label(text='Shading Options', icon='OUTLINER_OB_EMPTY')


####################################################################################################
# @draw_shading_option
####################################################################################################
def draw_shading_option(layout, scene, options):

    # Shading options
    row = layout.row()
    row.label(text='Shading')
    row.prop(scene, 'NMV_SynapticsShader')
    options.synaptics.shader = scene.NMV_SynapticsShader


####################################################################################################
# @draw_shading_options
####################################################################################################
def draw_shading_options(layout, scene, options):

    draw_shading_options_header(layout=layout)
    draw_shading_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_excitatory_synapses_color_and_count
####################################################################################################
def draw_excitatory_synapses_color_and_count(layout, scene, options):

    color_row = layout.row()
    color_row.prop(scene, 'NMV_ExcitatorySynapsesColor')
    options.synaptics.excitatory_synapses_color = scene.NMV_ExcitatorySynapsesColor
    synapse_count_column = color_row.column()
    synapse_count_column.prop(scene, 'NMV_SynapticsNumberExcitatorySynapses')
    synapse_count_column.enabled = False


####################################################################################################
# @draw_inhibitory_synapses_color_and_count
####################################################################################################
def draw_inhibitory_synapses_color_and_count(layout, scene, options):

    color_row = layout.row()
    color_row.prop(scene, 'NMV_InhibitorySynapsesColor')
    options.synaptics.inhibitory_synapses_color = scene.NMV_InhibitorySynapsesColor
    synapse_count_column = color_row.column()
    synapse_count_column.prop(scene, 'NMV_SynapticsNumberInhibitorySynapses')
    synapse_count_column.enabled = False


####################################################################################################
# @draw_excitatory_options
####################################################################################################
def draw_excitatory_options(layout, scene, options):

    draw_excitatory_synapses_color_and_count(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_inhibitory_options
####################################################################################################
def draw_inhibitory_options(layout, scene, options):

    draw_inhibitory_synapses_color_and_count(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_excitatory_and_inhibitory_options
####################################################################################################
def draw_excitatory_and_inhibitory_options(layout, scene, options):

    draw_excitatory_synapses_color_and_count(layout=layout, scene=scene, options=options)
    draw_inhibitory_synapses_color_and_count(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_synapses_color_option
####################################################################################################
def draw_synapses_color_option(layout, scene, options):

    color_row = layout.row()
    color_row.prop(scene, 'NMV_SynapsesColor')
    options.synaptics.synapses_color = scene.NMV_SynapsesColor

    synapse_count_column = color_row.column()
    synapse_count_column.prop(scene, 'NMV_SynapticsNumberSharedSynapses')
    synapse_count_column.enabled = False


####################################################################################################
# @draw_pre_synaptic_gid
####################################################################################################
def draw_pre_synaptic_gid(layout, scene, options):

    gid_row = layout.row()
    gid_row.prop(scene, 'NMV_PreSynapticGID')
    options.synaptics.pre_synaptic_gid = scene.NMV_PreSynapticGID


####################################################################################################
# @draw_post_synaptic_gid
####################################################################################################
def draw_post_synaptic_gid(layout, scene, options):

    gid_row = layout.row()
    gid_row.prop(scene, 'NMV_PostSynapticGID')
    options.synaptics.post_synaptic_gid = scene.NMV_PostSynapticGID


####################################################################################################
# @draw_pre_synaptic_pathway_options
####################################################################################################
def draw_pre_synaptic_pathway_options(layout, scene, options):

    draw_pre_synaptic_gid(layout=layout, scene=scene, options=options)
    draw_synapses_color_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_post_synaptic_pathway_options
####################################################################################################
def draw_post_synaptic_pathway_options(layout, scene, options):

    draw_post_synaptic_gid(layout=layout, scene=scene, options=options)
    draw_synapses_color_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_afferent_synapses_color_option
####################################################################################################
def draw_afferent_synapses_color_option(layout, scene, options):

    color_row = layout.row()
    color_row.prop(scene, 'NMV_AfferentSynapsesColor')
    options.synaptics.afferent_synapses_color = scene.NMV_AfferentSynapsesColor
    synapse_count_column = color_row.column()
    synapse_count_column.prop(scene, 'NMV_SynapticsNumberAfferentSynapses')
    synapse_count_column.enabled = False


####################################################################################################
# @draw_efferent_synapses_color_option
####################################################################################################
def draw_efferent_synapses_color_option(layout, scene, options):

    color_row = layout.row()
    color_row.prop(scene, 'NMV_EfferentSynapsesColor')
    options.synaptics.efferent_synapses_color = scene.NMV_EfferentSynapsesColor
    synapse_count_column = color_row.column()
    synapse_count_column.prop(scene, 'NMV_SynapticsNumberEfferentSynapses')
    synapse_count_column.enabled = False


####################################################################################################
# @draw_mtype_color_palette
####################################################################################################
def draw_mtype_color_palette(layout, scene, options):

    # A circuit must be loaded
    if nmv.consts.Circuit.MTYPES is not None:
        options.synaptics.mtypes_colors = list()

        # Add the colormap element to the UI
        colors = layout.column()
        for i in range(len(nmv.consts.Circuit.MTYPES)):
            values = colors.row()
            values.prop(scene, 'NMV_MtypeColor_%d' % i)
            count_column = values.column()
            count_column.prop(scene, 'NMV_Synaptic_MtypeCount_%d' % i)
            count_column.enabled = False

            # Get the color value from the panel
            options.synaptics.mtypes_colors.append(getattr(scene, 'NMV_MtypeColor_%d' % i))


####################################################################################################
# @draw_etype_color_palette
####################################################################################################
def draw_etype_color_palette(layout, scene, options):

    # A circuit must be loaded
    if nmv.consts.Circuit.ETYPES is not None:
        options.synaptics.etypes_colors = list()

        # Add the colormap element to the UI
        colors = layout.column()
        for i in range(len(nmv.consts.Circuit.ETYPES)):
            values = colors.row()
            values.prop(scene, 'NMV_EtypeColor_%d' % i)
            count_column = values.column()
            count_column.prop(scene, 'NMV_Synaptic_EtypeCount_%d' % i)
            count_column.enabled = False

            # Get the color value from the panel
            options.synaptics.etypes_colors.append(getattr(scene, 'NMV_EtypeColor_%d' % i))


####################################################################################################
# @draw_afferent_options
####################################################################################################
def draw_afferent_options(layout, scene, options):

    color_scheme_row = layout.row()
    color_scheme_row.prop(scene, 'NMV_AfferentColorCoding')
    options.synaptics.afferent_color_coding = scene.NMV_AfferentColorCoding

    scheme = options.synaptics.afferent_color_coding
    if scheme == nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR:
        draw_afferent_synapses_color_option(layout=layout, scene=scene, options=options)
    elif scheme == nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED:
        draw_mtype_color_palette(layout=layout, scene=scene, options=options)
    elif scheme == nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED:
        draw_etype_color_palette(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_efferent_options
####################################################################################################
def draw_efferent_options(layout, scene, options):

    color_scheme_row = layout.row()
    color_scheme_row.prop(scene, 'NMV_EfferentColorCoding')
    options.synaptics.efferent_color_coding = scene.NMV_EfferentColorCoding

    scheme = options.synaptics.efferent_color_coding
    if scheme == nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR:
        draw_efferent_synapses_color_option(layout=layout, scene=scene, options=options)
    elif scheme == nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED:
        draw_mtype_color_palette(layout=layout, scene=scene, options=options)
    elif scheme == nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED:
        draw_etype_color_palette(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_afferent_and_efferent_options
####################################################################################################
def draw_afferent_and_efferent_options(layout, scene, options):

    draw_afferent_synapses_color_option(layout=layout, scene=scene, options=options)
    draw_efferent_synapses_color_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_specific_color_coded_set_options
####################################################################################################
def draw_specific_color_coded_set_options(layout, scene, options):

    color_scheme_row = layout.row()
    color_scheme_row.prop(scene, 'NMV_SpecificColorCoding')


####################################################################################################
# @draw_synapse_percentage_option
####################################################################################################
def draw_synapse_percentage_option(layout, scene, options):

    row = layout.row()
    row.label(text='Synapses Percentage')
    row.prop(scene, 'NMV_SynapsesPercentage')
    options.synaptics.percentage = scene.NMV_SynapsesPercentage


####################################################################################################
# @draw_synapse_radius_options
####################################################################################################
def draw_synapse_radius_options(layout, scene, options):

    row = layout.row()
    row.label(text='Synapses Radius')
    row.prop(scene, 'NMV_SynapseRadius')
    options.synaptics.synapses_radius = scene.NMV_SynapseRadius


####################################################################################################
# @draw_common_options
####################################################################################################
def draw_common_options(layout, scene, options):

    draw_synapse_radius_options(layout=layout, scene=scene, options=options)
    draw_synapse_percentage_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_synaptic_targets
####################################################################################################
def draw_synaptic_targets(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_SynapticsJsonFile')
    options.synaptics.synaptics_json_file = scene.NMV_SynapticsJsonFile

    # If the target is loaded, show the color map
    if nmv.interface.ui_synaptics_file_loaded:

        # Get the colors of the customized synapses
        options.synaptics.customized_colors = list()

        # Add the colormap element to the UI
        colors = layout.column()
        for i, group in enumerate(options.synaptics.customized_synaptics_group):
            values = colors.row()
            values.prop(scene, 'NMV_CustomizedColor%d' % i)
            values.enabled = False
            count_column = values.column()
            count_column.prop(scene, 'NMV_CustomizedCount%d' % i)
            count_column.enabled = False

            # Get the color value from the panel
            options.synaptics.customized_synaptics_colors.append(
                getattr(scene, 'NMV_CustomizedColor%d' % i))


####################################################################################################
# @draw_synaptics_afferent_projection
####################################################################################################
def draw_synaptics_afferent_projection(layout, scene, options):

    row = layout.row()
    row.label(text='Projection Name')
    row.prop(scene, 'NMV_SynapticsProjectionName')
    options.synaptics.projection_name = scene.NMV_SynapticsProjectionName
    