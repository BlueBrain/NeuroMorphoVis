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
# @draw_excitatory_synapses_color
####################################################################################################
def draw_excitatory_synapses_color(layout, scene, options):

    color_row = layout.row()
    color_row.prop(scene, 'NMV_ExcitatorySynapsesColor')
    options.synaptics.excitatory_synapses_color = scene.NMV_ExcitatorySynapsesColor


####################################################################################################
# @draw_inhibitory_synapses_color
####################################################################################################
def draw_inhibitory_synapses_color(layout, scene, options):

    color_row = layout.row()
    color_row.prop(scene, 'NMV_InhibitorySynapsesColor')
    options.synaptics.inhibitory_synapses_color = scene.NMV_InhibitorySynapsesColor


####################################################################################################
# @draw_excitatory_options
####################################################################################################
def draw_excitatory_options(layout, scene, options):

    draw_excitatory_synapses_color(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_inhibitory_options
####################################################################################################
def draw_inhibitory_options(layout, scene, options):

    draw_inhibitory_synapses_color(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_excitatory_and_inhibitory_options
####################################################################################################
def draw_excitatory_and_inhibitory_options(layout, scene, options):

    draw_excitatory_synapses_color(layout=layout, scene=scene, options=options)
    draw_inhibitory_synapses_color(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_synapses_color_option
####################################################################################################
def draw_synapses_color_option(layout, scene, options):

    color_row = layout.row()
    color_row.prop(scene, 'NMV_SynapsesColor')
    options.synaptics.synapses_color = scene.NMV_SynapsesColor


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


####################################################################################################
# @draw_efferent_synapses_color_option
####################################################################################################
def draw_efferent_synapses_color_option(layout, scene, options):

    color_row = layout.row()
    color_row.prop(scene, 'NMV_EfferentSynapsesColor')
    options.synaptics.efferent_synapses_color = scene.NMV_EfferentSynapsesColor


####################################################################################################
# @draw_mtype_color_palette
####################################################################################################
def draw_mtype_color_palette(layout, scene, options):

    if nmv.consts.Circuit.MTYPES is not None:
        options.shading.mtypes_colors = list()

        # Add the colormap element to the UI
        colors = layout.column()
        for i in range(len(nmv.consts.Circuit.MTYPES)):
            values = colors.row()
            values.prop(scene, 'NMV_MtypeColor_%d' % i)

            # Get the color value from the panel
            options.shading.mtypes_colors.append(getattr(scene, 'NMV_MtypeColor_%d' % i))


####################################################################################################
# @draw_etype_color_palette
####################################################################################################
def draw_etype_color_palette(layout, scene, options):

    # Fill list of colors
    if nmv.consts.Circuit.ETYPES is not None:

        options.shading.etypes_colors = list()

        # Add the colormap element to the UI
        colors = layout.column()
        for i in range(len(nmv.consts.Circuit.ETYPES)):
            values = colors.row()
            values.prop(scene, 'NMV_EtypeColor_%d' % i)

            # Get the color value from the panel
            options.shading.etypes_colors.append(getattr(scene, 'NMV_EtypeColor_%d' % i))


####################################################################################################
# @draw_afferent_options
####################################################################################################
def draw_afferent_options(layout, scene, options):

    color_scheme_row = layout.row()
    color_scheme_row.prop(scene, 'NMV_AfferentColorCoding')
    options.synaptics.afferent_color_coding = scene.NMV_AfferentColorCoding

    scheme = options.synaptics.afferent_color_coding
    if scheme == nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR:
        draw_afferent_synapses_color_option(
            layout=layout, scene=scene, options=options)
    elif scheme == nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED:
        draw_mtype_color_palette(
            layout=layout, scene=scene, options=options)
    elif scheme == nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED:
        draw_etype_color_palette(
            layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_efferent_options
####################################################################################################
def draw_efferent_options(layout, scene, options):

    color_scheme_row = layout.row()
    color_scheme_row.prop(scene, 'NMV_EfferentColorCoding')
    options.synaptics.efferent_color_coding = scene.NMV_EfferentColorCoding

    scheme = options.synaptics.efferent_color_coding
    if scheme == nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR:
        draw_efferent_synapses_color_option(
            layout=layout, scene=scene, options=options)
    elif scheme == nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED:
        draw_mtype_color_palette(
            layout=layout, scene=scene, options=options)
    elif scheme == nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED:
        draw_etype_color_palette(
            layout=layout, scene=scene, options=options)


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
# @draw_common_options_for_all_use_cases
####################################################################################################
def draw_common_options_for_all_use_cases(layout, scene, options):

    draw_synapse_radius_options(layout=layout, scene=scene, options=options)
    draw_synapse_percentage_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_neuron_radius_option
####################################################################################################
def draw_neuron_radius_option(layout, scene, options):

    neuron_radius_row = layout.row()
    unify_radius_column = neuron_radius_row.column()
    unify_radius_column.prop(scene, 'NMV_SYNAPTICS_UnifyRadius')
    options.synaptics.unify_branch_radii = scene.NMV_SYNAPTICS_UnifyRadius

    neuron_radius_column = neuron_radius_row.column()
    neuron_radius_column.prop(scene, 'NMV_SYNAPTICS_UnifiedNeuronRadius')
    options.synaptics.unified_radius = scene.NMV_SYNAPTICS_UnifiedNeuronRadius

    # Disable the column
    neuron_radius_column.enabled = False if not scene.NMV_SYNAPTICS_UnifyRadius else True


####################################################################################################
# @draw_single_neuron_options
####################################################################################################
def draw_single_neuron_options(layout, scene, options):

    # Reconstruction options
    neuron_options_row = layout.row()
    neuron_options_row.label(text='Neuron Options:', icon='OUTLINER_OB_EMPTY')

    dendrites_row = layout.row()
    add_dendrites_column = dendrites_row.column()
    add_dendrites_column.prop(scene, 'NMV_SYNAPTICS_DisplayDendrites')
    options.synaptics.display_dendrites = scene.NMV_SYNAPTICS_DisplayDendrites

    dendrites_options_column = dendrites_row.column()
    dendrites_options_column.prop(scene, 'NMV_SYNAPTICS_DendritesColor')
    options.synaptics.dendrites_color = scene.NMV_SYNAPTICS_DendritesColor

    if not scene.NMV_SYNAPTICS_DisplayDendrites:
        dendrites_options_column.enabled = False
    else:
        dendrites_options_column.enabled = True

    axons_row = layout.row()
    add_axons_column = axons_row.column()
    add_axons_column.prop(scene, 'NMV_SYNAPTICS_DisplayAxons')
    options.synaptics.display_axons = scene.NMV_SYNAPTICS_DisplayAxons

    axons_options_column = axons_row.column()
    axons_options_column.prop(scene, 'NMV_SYNAPTICS_AxonsColor')
    options.synaptics.axons_color = scene.NMV_SYNAPTICS_AxonsColor

    if not scene.NMV_SYNAPTICS_DisplayAxons:
        axons_options_column.enabled = False
    else:
        axons_options_column.enabled = True

    draw_neuron_radius_option(layout, scene, options)


####################################################################################################
# @draw_neuron_pair_options
####################################################################################################
def draw_neuron_pair_options(layout, scene, options):

    # Reconstruction options
    neuron_options_row = layout.row()
    neuron_options_row.label(text='Neurons Options:', icon='OUTLINER_OB_EMPTY')

    for i in ['PreSynaptic', 'PostSynaptic']:

        dendrites_row = layout.row()
        add_dendrites_column = dendrites_row.column()
        add_dendrites_column.prop(scene, 'NMV_SYNAPTICS_Display%sDendrites' % i)
        dendrites_options_column = dendrites_row.column()
        dendrites_options_column.prop(scene, 'NMV_SYNAPTICS_%sDendritesColor' % i)

        if not getattr(scene, 'NMV_SYNAPTICS_Display%sDendrites' % i):
            dendrites_options_column.enabled = False
        else:
            dendrites_options_column.enabled = True

        axons_row = layout.row()
        add_axons_column = axons_row.column()
        add_axons_column.prop(scene, 'NMV_SYNAPTICS_Display%sAxons' % i)
        axons_options_column = axons_row.column()
        axons_options_column.prop(scene, 'NMV_SYNAPTICS_%sAxonsColor' % i)

        if not getattr(scene, 'NMV_SYNAPTICS_%sAxonsColor' % i):
            axons_options_column.enabled = False
        else:
            axons_options_column.enabled = True

    draw_neuron_radius_option(layout, scene, options)


####################################################################################################
# @draw_neuron_pair_options
####################################################################################################
def reconstruct_synaptics(operator, context, circuit, options):

    # Clear the scene
    nmv.scene.clear_scene()

    # Afferent synapses only (on dendrites)
    if options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT:
        nmv.bbp.visualize_afferent_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

    # Efferent synapses (on axon)
    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EFFERENT:
        nmv.bbp.visualize_efferent_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

    # Afferent and efferent synapses
    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT_AND_EFFERENT:
        nmv.bbp.visualize_afferent_and_efferent_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options,
            visualize_afferent=True, visualize_efferent=True)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

    # Excitatory synapses only
    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY:
        nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options,
            visualize_excitatory=True, visualize_inhibitory=False)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

    # Inhibitory synapses only
    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.INHIBITORY:
        nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
            circuit=circuit, gid=nmv.interface.ui_options.morphology.gid,
            visualize_excitatory=False, visualize_inhibitory=True, options=options)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

    # Excitatory and inhibitory synapses
    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY_AND_INHIBITORY:
        nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
            circuit=circuit, gid=nmv.interface.ui_options.morphology.gid,
            visualize_excitatory=True, visualize_inhibitory=True, options=options)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PATHWAY_PRE_SYNAPTIC:

        # Initially, try to get a list of synapses shared between the two cells
        shared_synapses_ids = circuit.get_shared_synapses_ids_between_two_neurons(
            pre_gid=options.synaptics.pre_synaptic_gid,
            post_gid=options.morphology.gid)

        # If that list is Zero, then report the error and exit
        if len(shared_synapses_ids) == 0:
            operator.report({'ERROR'}, 'No shared synapses between the given neurons [%s - %s]'
                            % (str(options.synaptics.pre_synaptic_gid),
                               str(options.morphology.gid)))
            return {'FINISHED'}

        # Create the post-synaptic neuron AT ORIGIN - THIS IS THE FOCUS
        post_synaptic_neuron_mesh = nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Create the pre-synaptic neuron AT ORIGIN
        pre_synaptic_neuron_mesh = nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.synaptics.pre_synaptic_gid, options=options)

        # Get the transformations of the pre- and post-synaptic neurons
        pre_synaptic_transformation = circuit.get_neuron_transformation_matrix(
            gid=options.synaptics.pre_synaptic_gid)
        post_synaptic_transformation = circuit.get_neuron_transformation_matrix(
            gid=options.morphology.gid)

        # Since the focus is given to the post-synaptic neuron; it is the originally loaded one,
        # transform the pre-synaptic neuron w.r.t to the post synaptic one
        pre_synaptic_neuron_mesh.matrix_world = pre_synaptic_transformation
        pre_synaptic_neuron_mesh.matrix_world = \
            post_synaptic_transformation.inverted() @ pre_synaptic_neuron_mesh.matrix_world

        # Transform the synapses to be loaded on the post-synaptic neuron
        nmv.bbp.visualize_shared_synapses_between_two_neurons(
            circuit=circuit,
            pre_gid=options.synaptics.pre_synaptic_gid,
            post_gid=options.morphology.gid,
            options=options,
            inverse_transformation=post_synaptic_transformation.inverted())

    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PATHWAY_POST_SYNAPTIC:

        # Initially, try to get a list of synapses shared between the two cells
        shared_synapses_ids = circuit.get_shared_synapses_ids_between_two_neurons(
            pre_gid=options.morphology.gid,
            post_gid=options.synaptics.post_synaptic_gid)

        # If that list is Zero, then report the error and exit
        if len(shared_synapses_ids) == 0:
            operator.report({'ERROR'}, 'No shared synapses between the given neurons [%s - %s]'
                            % (str(options.morphology.gid),
                               str(options.synaptics.post_synaptic_gid)))
            return {'FINISHED'}

        # Create the pre-synaptic neuron AT ORIGIN - THIS IS THE FOCUS
        pre_synaptic_neuron_mesh = nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Create the post-synaptic neuron AT ORIGIN
        post_synaptic_neuron_mesh = nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.synaptics.post_synaptic_gid, options=options)

        # Get the transformations of the pre- and post-synaptic neurons
        pre_synaptic_transformation = circuit.get_neuron_transformation_matrix(
            gid=options.morphology.gid)
        post_synaptic_transformation = circuit.get_neuron_transformation_matrix(
            gid=options.synaptics.post_synaptic_gid)

        # Since the focus is given to the pre-synaptic neuron; it is the originally loaded one,
        # transform the post-synaptic neuron w.r.t to the pre synaptic one
        post_synaptic_neuron_mesh.matrix_world = post_synaptic_transformation
        post_synaptic_neuron_mesh.matrix_world = \
            pre_synaptic_transformation.inverted() @ post_synaptic_neuron_mesh.matrix_world

        nmv.bbp.visualize_shared_synapses_between_two_neurons(
            circuit=circuit,
            pre_gid=nmv.interface.ui_options.morphology.gid,
            post_gid=options.synaptics.post_synaptic_gid,
            options=options,
            inverse_transformation=pre_synaptic_transformation.inverted())

    # Done
    return {'FINISHED'}

