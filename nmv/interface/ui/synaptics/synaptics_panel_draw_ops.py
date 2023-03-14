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

    percentage_row = layout.row()
    percentage_row.prop(scene, 'NMV_SynapsesPercentage')
    options.synaptics.percentage = scene.NMV_SynapsesPercentage


####################################################################################################
# @draw_synapse_radius_options
####################################################################################################
def draw_synapse_radius_options(layout, scene, options):

    synapse_radius_row = layout.row()
    synapse_radius_row.prop(scene, 'NMV_SynapseRadius')
    options.synaptics.synapses_radius = scene.NMV_SynapseRadius


####################################################################################################
# @draw_common_options
####################################################################################################
def draw_common_options(layout, scene, options):

    draw_synapse_radius_options(layout=layout, scene=scene, options=options)
    draw_synapse_percentage_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_neuron_radius_option
####################################################################################################
def draw_neuron_radius_option(layout, scene, options):

    neuron_radius_row = layout.row()
    unify_radius_column = neuron_radius_row.column()
    unify_radius_column.prop(scene, 'NMV_SynapticsUnifyRadius')
    options.synaptics.unify_branch_radii = scene.NMV_SynapticsUnifyRadius

    neuron_radius_column = neuron_radius_row.column()
    neuron_radius_column.prop(scene, 'NMV_SynapticsUnifiedNeuronRadius')
    options.synaptics.unified_radius = scene.NMV_SynapticsUnifiedNeuronRadius

    # Disable the column
    neuron_radius_column.enabled = False if not scene.NMV_SynapticsUnifyRadius else True


####################################################################################################
# @draw_single_neuron_options
####################################################################################################
def draw_single_neuron_options(layout, scene, options):

    # Reconstruction options
    neuron_options_row = layout.row()
    neuron_options_row.label(text='Neuron Options:', icon='OUTLINER_OB_EMPTY')

    dendrites_row = layout.row()
    add_dendrites_column = dendrites_row.column()
    add_dendrites_column.prop(scene, 'NMV_DisplayDendrites')
    options.synaptics.display_dendrites = scene.NMV_DisplayDendrites

    dendrites_options_column = dendrites_row.column()
    dendrites_options_column.prop(scene, 'NMV_SynapticsDendritesColor')
    options.synaptics.dendrites_color = scene.NMV_SynapticsDendritesColor

    axons_row = layout.row()
    add_axons_column = axons_row.column()
    add_axons_column.prop(scene, 'NMV_DisplayAxons')
    options.synaptics.display_axons = scene.NMV_DisplayAxons

    axons_options_column = axons_row.column()
    axons_options_column.prop(scene, 'NMV_SynapticsAxonsColor')
    options.synaptics.axons_color = scene.NMV_SynapticsAxonsColor

    dendrites_options_column.enabled = True if scene.NMV_DisplayDendrites else False
    axons_options_column.enabled = True if scene.NMV_DisplayAxons else False

    # Common other options
    draw_neuron_radius_option(layout, scene, options)


####################################################################################################
# @draw_neuron_pair_options
####################################################################################################
def draw_neuron_pair_options(layout, scene, options):

    # Reconstruction options
    neuron_options_row = layout.row()
    neuron_options_row.label(text='Neurons Options:', icon='OUTLINER_OB_EMPTY')

    # Pre-synaptic neuron
    pre_dendrites_row = layout.row()
    add_dendrites_column = pre_dendrites_row.column()
    add_dendrites_column.prop(scene, 'NMV_DisplayPreSynapticDendrites')
    options.synaptics.display_pre_synaptic_dendrites = scene.NMV_DisplayPreSynapticDendrites

    dendrites_options_column = pre_dendrites_row.column()
    dendrites_options_column.prop(scene, 'NMV_PreSynapticDendritesColor')
    options.synaptics.pre_synaptic_dendrites_color = scene.NMV_PreSynapticDendritesColor

    pre_axons_row = layout.row()
    add_axons_column = pre_axons_row.column()
    add_axons_column.prop(scene, 'NMV_DisplayPreSynapticAxons')
    options.synaptics.display_pre_synaptic_axons = scene.NMV_DisplayPreSynapticAxons

    axons_options_column = pre_axons_row.column()
    axons_options_column.prop(scene, 'NMV_PreSynapticAxonsColor')
    options.synaptics.pre_synaptic_axons_color = scene.NMV_PreSynapticAxonsColor

    dendrites_options_column.enabled = True if scene.NMV_DisplayPreSynapticDendrites else False
    axons_options_column.enabled = True if scene.NMV_DisplayPreSynapticAxons else False

    # Post-synaptic neuron
    post_dendrites_row = layout.row()
    add_dendrites_column = post_dendrites_row.column()
    add_dendrites_column.prop(scene, 'NMV_DisplayPostSynapticDendrites')
    options.synaptics.display_post_synaptic_dendrites = scene.NMV_DisplayPostSynapticDendrites

    dendrites_options_column = post_dendrites_row.column()
    dendrites_options_column.prop(scene, 'NMV_PostSynapticDendritesColor')
    options.synaptics.post_synaptic_dendrites_color = scene.NMV_PostSynapticDendritesColor

    axons_row = layout.row()
    add_axons_column = axons_row.column()
    add_axons_column.prop(scene, 'NMV_DisplayPostSynapticAxons')
    options.synaptics.display_post_synaptic_axons = scene.NMV_DisplayPostSynapticAxons

    axons_options_column = axons_row.column()
    axons_options_column.prop(scene, 'NMV_PostSynapticAxonsColor')
    options.synaptics.post_synaptic_axons_color = scene.NMV_PostSynapticAxonsColor

    dendrites_options_column.enabled = True if scene.NMV_DisplayPostSynapticDendrites else False
    axons_options_column.enabled = True if scene.NMV_DisplayPostSynapticAxons else False

    # Common other options
    draw_neuron_radius_option(layout, scene, options)




####################################################################################################
# @draw_synaptics_rendering_options
####################################################################################################
def draw_synaptics_rendering_options(layout, scene, options):

    # Rendering options
    quick_rendering_row = layout.row()
    quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')

    # Rendering view
    rendering_view_row = layout.row()
    rendering_view_row.label(text='View:')
    rendering_view_row.prop(scene, 'NMV_SynapticsRenderingView', expand=True)

    # Add the closeup size option
    if scene.NMV_MeshRenderingView == nmv.enums.Rendering.View.CLOSE_UP:

        # Closeup size option
        close_up_size_row = layout.row()
        close_up_size_row.label(text='Closeup Size:')
        close_up_size_row.prop(scene, 'NMV_SynapticsCloseUpSize')
        close_up_size_row.enabled = True

        # Frame resolution option (only for the close up mode)
        frame_resolution_row = layout.row()
        frame_resolution_row.label(text='Frame Resolution:')
        frame_resolution_row.prop(scene, 'NMV_SynapticsFrameResolution')
        frame_resolution_row.enabled = True

    # Otherwise, render the Mid and Wide shot modes
    else:

        # Rendering resolution
        rendering_resolution_row = layout.row()
        rendering_resolution_row.label(text='Resolution:')
        rendering_resolution_row.prop(scene, 'NMV_SynapticsRenderingResolution', expand=True)

        # Add the frame resolution option
        if scene.NMV_MeshRenderingResolution == \
                nmv.enums.Rendering.Resolution.FIXED:

            # Frame resolution option (only for the close up mode)
            frame_resolution_row = layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(scene, 'NMV_SynapticsFrameResolution')
            frame_resolution_row.enabled = True

        # Otherwise, add the scale factor option
        else:

            # Scale factor option
            scale_factor_row = layout.row()
            scale_factor_row.label(text='Resolution Scale:')
            scale_factor_row.prop(scene, 'NMV_SynapticsFrameScaleFactor')
            scale_factor_row.enabled = True

    # Image extension
    image_extension_row = layout.row()
    image_extension_row.label(text='Image Format:')
    image_extension_row.prop(scene, 'NMV_SynapticsImageFormat')
    nmv.interface.ui_options.mesh.image_format = scene.NMV_MeshImageFormat

    # Scale bar
    scale_bar_row = layout.row()
    scale_bar_row.prop(scene, 'NMV_SynapticsScaleBar')
    nmv.interface.ui_options.rendering.render_scale_bar = scene.NMV_RenderMeshScaleBar

    # Rendering view
    render_view_row = layout.row()
    render_view_row.label(text='Render View:', icon='RESTRICT_RENDER_OFF')
    render_view_buttons_row = layout.row(align=True)
    render_view_buttons_row.operator('nmv.render_mesh_front', icon='AXIS_FRONT')
    render_view_buttons_row.operator('nmv.render_mesh_side', icon='AXIS_SIDE')
    render_view_buttons_row.operator('nmv.render_mesh_top', icon='AXIS_TOP')
    render_view_buttons_row.enabled = True


####################################################################################################
# @draw_synaptics_reconstruction_options
####################################################################################################
def draw_synaptics_reconstruction_options(layout, scene, options):

    # Reconstruction options
    synapses_options_row = layout.row()
    synapses_options_row.label(text='Synapses Options:', icon='OUTLINER_OB_EMPTY')

    use_case = options.synaptics.use_case
    if use_case == nmv.enums.Synaptics.UseCase.AFFERENT:
        draw_afferent_options(
            layout=layout, scene=scene, options=options)
        draw_common_options(
            layout=layout, scene=scene, options=options)
        draw_single_neuron_options(
            layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.EFFERENT:
        draw_efferent_options(
            layout=layout, scene=scene, options=options)
        draw_common_options(
            layout=layout, scene=scene, options=options)
        draw_single_neuron_options(
            layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.AFFERENT_AND_EFFERENT:
        draw_afferent_and_efferent_options(
            layout=layout, scene=scene, options=options)
        draw_common_options(
            layout=layout, scene=scene, options=options)
        draw_single_neuron_options(
            layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.EXCITATORY:
        draw_excitatory_options(
            layout=layout, scene=scene, options=options)
        draw_common_options(
            layout=layout, scene=scene, options=options)
        draw_single_neuron_options(
            layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.INHIBITORY:
        draw_inhibitory_options(
            layout=layout, scene=scene, options=options)
        draw_common_options(
            layout=layout, scene=scene, options=options)
        draw_single_neuron_options(
            layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.EXCITATORY_AND_INHIBITORY:
        draw_excitatory_and_inhibitory_options(
            layout=layout, scene=scene, options=options)
        draw_common_options(
            layout=layout, scene=scene, options=options)
        draw_single_neuron_options(
            layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.SPECIFIC_COLOR_CODED_SET:
        draw_specific_color_coded_set_options(
            layout=layout, scene=scene, options=options)
        draw_common_options(
            layout=layout, scene=scene, options=options)
        draw_single_neuron_options(
            layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.PATHWAY_PRE_SYNAPTIC:
        draw_pre_synaptic_pathway_options(
            layout=layout, scene=scene, options=options)
        draw_synapse_radius_options(
            layout=layout, scene=scene, options=options)
        draw_neuron_pair_options(
            layout=layout, scene=scene, options=options)

    elif use_case == nmv.enums.Synaptics.UseCase.PATHWAY_POST_SYNAPTIC:
        draw_post_synaptic_pathway_options(
            layout=layout, scene=scene, options=options)
        draw_synapse_radius_options(
            layout=layout, scene=scene, options=options)
        draw_neuron_pair_options(
            layout=layout, scene=scene, options=options)
    else:
        pass

    # Shading options
    layout.row().separator()
    shading_options_row = layout.row()
    shading_options_row.label(text='Shading Options:', icon='OUTLINER_OB_EMPTY')
    shading_row = layout.row()
    shading_row.prop(scene, 'NMV_MeshMaterial')
    options.shading.mesh_material = scene.NMV_MeshMaterial

    # Draw the reconstruction button
    layout.row().separator()
    reconstruction_button_row = layout.row()
    reconstruction_button_row.operator('nmv.reconstruct_synaptics')

    # Statistics
    layout.row().separator()
    stats_row = layout.row()
    stats_row.label(text='Stats:', icon='RECOVER_LAST')
    time_row = layout.row()
    time_row.prop(scene, 'NMV_SynapticReconstructionTime')
    time_row.enabled = False


####################################################################################################
# @draw_out_of_context_message
####################################################################################################
def draw_out_of_context_message(layout, scene, options):

    message_row = layout.row()
    message_row.label(text='The Synaptics panel can ONLY be used with a circuit!')
