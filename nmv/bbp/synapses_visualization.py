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
from mathutils import Vector

# Internal imports
import nmv.bbox
import nmv.consts
import nmv.enums
import nmv.utilities


####################################################################################################
# @visualize_afferent_synapses
####################################################################################################
def visualize_afferent_synapses(circuit,
                                gid,
                                options,
                                context=None):
    """Visualizes the afferent synapses of a specific neuron in a circuit.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param options:
        NMV options.
    :param context:
        Blender context, for UI operations.
    :return:
        A reference to the created synapse group.
    """

    # Create the synapse groups
    synapse_groups = list()

    # Select what to visualize based on the selected color coding scheme
    color_coding_scheme = options.synaptics.afferent_color_coding
    if color_coding_scheme == nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR:

        # Create the afferent synapse group
        afferent_group = nmv.bbp.get_afferent_synapse_group(
            circuit=circuit, gid=gid,
            color=nmv.utilities.rgb_vector_to_hex(options.synaptics.afferent_synapses_color))
        synapse_groups.append(afferent_group)

        # Synapses count
        if context is not None:
            afferent_synapses_count = len(afferent_group.synapses_ids_list)
            context.scene.NMV_SynapticsNumberAfferentSynapses = afferent_synapses_count

    elif color_coding_scheme == nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED:

        # Get the color-coding dictionary from the UI
        color_dict = {}
        for i in range(len(nmv.consts.Circuit.MTYPES)):
            color_dict[nmv.consts.Circuit.MTYPES[i]] = options.synaptics.mtypes_colors[i]

        # Create the afferent synapse groups
        synapse_groups = nmv.bbp.get_afferent_synapse_groups_color_coded_by_pre_mtypes(
            circuit=circuit, gid=gid, mtype_color_dict=color_dict)

        if context is not None:
            for i in range(len(nmv.consts.Circuit.MTYPES)):
                setattr(context.scene, 'NMV_Synaptic_MtypeCount_%d' % i,
                        len(synapse_groups[i].synapses_ids_list))

    elif color_coding_scheme == nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED:

        # Get the color-coding dictionary from the UI
        color_dict = {}
        for i in range(len(nmv.consts.Circuit.ETYPES)):
            color_dict[nmv.consts.Circuit.ETYPES[i]] = options.synaptics.etypes_colors[i]

        # Create the afferent synapse group
        synapse_groups = nmv.bbp.get_afferent_synapse_groups_color_coded_by_pre_etypes(
            circuit=circuit, gid=gid, etype_color_dict=color_dict)

        if context is not None:
            for i in range(len(nmv.consts.Circuit.ETYPES)):
                setattr(context.scene, 'NMV_Synaptic_EtypeCount_%d' % i,
                        len(synapse_groups[i].synapses_ids_list))

    else:
        pass

    nmv.logger.info('Adding synapses to the scene')
    nmv.bbp.create_color_coded_synapses_particle_system(
        circuit=circuit, synapse_groups=synapse_groups,
        synapse_radius=options.synaptics.synapses_radius,
        synapses_percentage=options.synaptics.percentage,
        inverted_transformation=circuit.get_neuron_inverse_transformation_matrix(gid=gid),
        material_type=options.synaptics.shader)

    # Return the synapse groups for statistics
    return synapse_groups


####################################################################################################
# @visualize_afferent_synapses_for_projection
####################################################################################################
def visualize_afferent_synapses_for_projection(circuit,
                                               gid,
                                               options,
                                               context=None):

    # Create the synapse groups
    synapse_groups = list()

    # Select what to visualize based on the selected color coding scheme
    color_coding_scheme = options.synaptics.afferent_color_coding
    if color_coding_scheme == nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR:

        # Create the afferent synapse group
        afferent_group = nmv.bbp.get_afferent_synapse_group_for_projection(
            circuit=circuit, gid=gid, projection_name=options.synaptics.projection_name,
            color=nmv.utilities.rgb_vector_to_hex(options.synaptics.afferent_synapses_color))
        synapse_groups.append(afferent_group)

        # Synapses count
        if context is not None:
            afferent_synapses_count = len(afferent_group.synapses_ids_list)
            context.scene.NMV_SynapticsNumberAfferentSynapses = afferent_synapses_count

    elif color_coding_scheme == nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED:

        # Get the color-coding dictionary from the UI
        color_dict = {}
        for i in range(len(nmv.consts.Circuit.MTYPES)):
            color_dict[nmv.consts.Circuit.MTYPES[i]] = options.synaptics.mtypes_colors[i]

        # Create the afferent synapse groups
        synapse_groups = nmv.bbp.get_afferent_synapse_groups_color_coded_by_pre_mtypes(
            circuit=circuit, gid=gid, mtype_color_dict=color_dict)

        if context is not None:
            for i in range(len(nmv.consts.Circuit.MTYPES)):
                setattr(context.scene, 'NMV_Synaptic_MtypeCount_%d' % i,
                        len(synapse_groups[i].synapses_ids_list))

    elif color_coding_scheme == nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED:

        # Get the color-coding dictionary from the UI
        color_dict = {}
        for i in range(len(nmv.consts.Circuit.ETYPES)):
            color_dict[nmv.consts.Circuit.ETYPES[i]] = options.synaptics.etypes_colors[i]

        # Create the afferent synapse group
        synapse_groups = nmv.bbp.get_afferent_synapse_groups_color_coded_by_pre_etypes(
            circuit=circuit, gid=gid, etype_color_dict=color_dict)

        if context is not None:
            for i in range(len(nmv.consts.Circuit.ETYPES)):
                setattr(context.scene, 'NMV_Synaptic_EtypeCount_%d' % i,
                        len(synapse_groups[i].synapses_ids_list))

    else:
        pass

    nmv.logger.info('Adding synapses to the scene')
    nmv.bbp.create_color_coded_synapses_particle_system(
        circuit=circuit, synapse_groups=synapse_groups,
        synapse_radius=options.synaptics.synapses_radius,
        synapses_percentage=options.synaptics.percentage,
        inverted_transformation=circuit.get_neuron_inverse_transformation_matrix(gid=gid),
        material_type=options.synaptics.shader)

    # Return the synapse groups for statistics
    return synapse_groups


####################################################################################################
# @visualize_efferent_synapses
####################################################################################################
def visualize_efferent_synapses(circuit,
                                gid,
                                options,
                                context=None):
    """Visualizes the efferent synapses of a specific neuron in a circuit.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param options:
        NMV options.
    :param context:
        Blender context, for UI operations.
    :return:
        A reference to the created synapse group.
    """

    # Create the synapse groups
    synapse_groups = list()

    # Select what to visualize based on the selected color coding scheme
    efferent_scheme = options.synaptics.efferent_color_coding
    if efferent_scheme == nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR:

        # Create the afferent synapse group
        efferent_group = nmv.bbp.get_efferent_synapse_group(
            circuit=circuit, gid=gid,
            color=nmv.utilities.rgb_vector_to_hex(options.synaptics.efferent_synapses_color))
        synapse_groups.append(efferent_group)

        # Synapses count
        if context is not None:
            efferent_synapses_count = len(efferent_group.synapses_ids_list)
            context.scene.NMV_SynapticsNumberEfferentSynapses = efferent_synapses_count

    elif efferent_scheme == nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED:

        # Get the color-coding dictionary from the UI
        color_dict = {}
        for i in range(len(nmv.consts.Circuit.MTYPES)):
            color_dict[nmv.consts.Circuit.MTYPES[i]] = options.synaptics.mtypes_colors[i]

        # Create the efferent synapse groups
        synapse_groups = nmv.bbp.get_efferent_synapse_groups_color_coded_by_post_mtypes(
            circuit=circuit, gid=gid, mtype_color_dict=color_dict)

        if context is not None:
            for i in range(len(nmv.consts.Circuit.MTYPES)):
                setattr(context.scene, 'NMV_Synaptic_MtypeCount_%d' % i,
                        len(synapse_groups[i].synapses_ids_list))

    elif efferent_scheme == nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED:

        # Get the color-coding dictionary from the UI
        color_dict = {}
        for i in range(len(nmv.consts.Circuit.ETYPES)):
            color_dict[nmv.consts.Circuit.ETYPES[i]] = options.synaptics.etypes_colors[i]

        # Create the efferent synapse groups
        synapse_groups = nmv.bbp.get_efferent_synapse_groups_color_coded_by_post_etypes(
            circuit=circuit, gid=gid, etype_color_dict=color_dict)

        if context is not None:
            for i in range(len(nmv.consts.Circuit.ETYPES)):
                setattr(context.scene, 'NMV_Synaptic_EtypeCount_%d' % i,
                        len(synapse_groups[i].synapses_ids_list))

    else:
        pass

    nmv.logger.info('Adding synapses to the scene')
    nmv.bbp.create_color_coded_synapses_particle_system(
        circuit=circuit, synapse_groups=synapse_groups,
        synapse_radius=options.synaptics.synapses_radius,
        synapses_percentage=options.synaptics.percentage,
        inverted_transformation=circuit.get_neuron_inverse_transformation_matrix(gid=gid),
        material_type=options.synaptics.shader)

    # Return the synapse groups for statistics
    return synapse_groups


####################################################################################################
# @visualize_afferent_and_efferent_synapses
####################################################################################################
def visualize_afferent_and_efferent_synapses(circuit,
                                             gid,
                                             options,
                                             visualize_afferent=True,
                                             visualize_efferent=True):
    """Visualizes the afferent and/or efferent synapses of a specific neuron in a circuit.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param options:
        NMV options.
    :param visualize_afferent:
        If this flag is set the afferent synapses will be visualized.
    :param visualize_efferent:
        If this flag is set the efferent synapses will be visualized.
    :return:
        A reference to the synapse groups list.
    """

    nmv.logger.info('Loading synapses and creating synapse groups')
    synapse_groups = list()
    if visualize_afferent:
        afferent_group = nmv.bbp.get_afferent_synapse_group(
            circuit=circuit, gid=gid,
            color=nmv.utilities.rgb_vector_to_hex(options.synaptics.afferent_synapses_color))
        synapse_groups.append(afferent_group)

    if visualize_efferent:
        efferent_group = nmv.bbp.get_efferent_synapse_group(
            circuit=circuit, gid=gid,
            color=nmv.utilities.rgb_vector_to_hex(options.synaptics.efferent_synapses_color))
        synapse_groups.append(efferent_group)

    nmv.logger.info('Adding synapses to the scene')
    nmv.bbp.create_color_coded_synapses_particle_system(
        circuit=circuit, synapse_groups=synapse_groups,
        synapse_radius=options.synaptics.synapses_radius,
        synapses_percentage=options.synaptics.percentage,
        inverted_transformation=circuit.get_neuron_inverse_transformation_matrix(gid=gid),
        material_type=options.synaptics.shader)

    # Return the synapse groups for statistics
    return synapse_groups


####################################################################################################
# @visualize_excitatory_and_inhibitory_synapses
####################################################################################################
def visualize_excitatory_and_inhibitory_synapses(circuit,
                                                 gid,
                                                 options,
                                                 visualize_excitatory=True,
                                                 visualize_inhibitory=True):
    """Visualizes the excitatory and/or inhibitory synapses of a specific neuron in a circuit.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param options:
        NMV options.
    :param visualize_excitatory:
        If this flag is set, the excitatory synapses will be visualized.
    :param visualize_inhibitory:
        If this flag is set, the inhibitory synapses will be visualized.
    :return:
         A reference to the synapse groups list.
    """

    #
    nmv.logger.info('Loading synapses and creating synapse groups')
    synapse_groups = list()
    if visualize_excitatory:
        excitatory_group = nmv.bbp.get_excitatory_synapse_group(
            circuit=circuit, gid=gid,
            color=nmv.utilities.rgb_vector_to_hex(options.synaptics.excitatory_synapses_color))
        synapse_groups.append(excitatory_group)

    if visualize_inhibitory:
        inhibitory_group = nmv.bbp.get_inhibitory_synapse_group(
            circuit=circuit, gid=gid,
            color=nmv.utilities.rgb_vector_to_hex(options.synaptics.inhibitory_synapses_color))
        synapse_groups.append(inhibitory_group)

    #
    nmv.logger.info('Adding synapses to the scene')
    nmv.bbp.create_color_coded_synapses_particle_system(
        circuit=circuit, synapse_groups=synapse_groups,
        synapse_radius=options.synaptics.synapses_radius,
        synapses_percentage=options.synaptics.percentage,
        inverted_transformation=circuit.get_neuron_inverse_transformation_matrix(gid=gid),
        material_type=options.synaptics.shader)

    # Return the synapse groups for statistics
    return synapse_groups


####################################################################################################
# @visualize_excitatory_and_inhibitory_synapses
####################################################################################################
def visualize_shared_synapses_between_two_neurons(circuit,
                                                  pre_gid,
                                                  post_gid,
                                                  options,
                                                  inverse_transformation):
    """Visualizes the shared synapses between two neurons in a circuit.

    :param circuit:
        BBP circuit.
    :param pre_gid:
        The GID of the pre-synaptic neuron.
    :param post_gid:
        The GID of the post-synaptic neuron.
    :param options:
        NMV options.
    :param inverse_transformation:
        The inverse transformation used to align the neurons at the origin.
    :return:
        A reference to the created synapse groups list.
    """

    # Create the shared group
    synapse_groups = list()
    synapse_groups.append(
        nmv.bbp.get_shared_synapses_group_between_two_neurons(
            circuit=circuit, pre_gid=pre_gid, post_gid=post_gid,
            color=nmv.utilities.rgb_vector_to_hex(options.synaptics.synapses_color)))

    nmv.logger.info('Adding synapses to the scene')
    nmv.bbp.create_color_coded_synapses_particle_system(
        circuit=circuit, synapse_groups=synapse_groups,
        synapse_radius=options.synaptics.synapses_radius,
        synapses_percentage=options.synaptics.percentage,
        inverted_transformation=inverse_transformation,
        material_type=options.synaptics.shader)

    # Return the synapse groups for statistics
    return synapse_groups


####################################################################################################
# @visualize_synapse_groups
####################################################################################################
def visualize_synapse_groups(circuit,
                             synapse_groups,
                             gid,
                             options):
    """A generic function to visualize a set of synapse groups.

    :param circuit:
        BBP circuit.
    :param synapse_groups:
        A list of synapse groups to be visualized.
    :param gid:
        The GID of the neuron.
    :param options:
        NMV options.
    """

    nmv.logger.info('Adding synapses to the scene')
    nmv.bbp.create_color_coded_synapses_particle_system(
        circuit=circuit, synapse_groups=synapse_groups,
        synapse_radius=options.synaptics.synapses_radius,
        synapses_percentage=options.synaptics.percentage,
        inverted_transformation=circuit.get_neuron_inverse_transformation_matrix(gid=gid),
        material_type=options.synaptics.shader)



