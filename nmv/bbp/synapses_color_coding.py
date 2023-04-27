####################################################################################################
# Copyright (c) 2023, EPFL / Blue Brain Project
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
import nmv.bbp


####################################################################################################
# @create_color_coded_synapse_groups_by_mtype
####################################################################################################
def create_color_coded_synapse_groups_by_mtype(circuit,
                                               synapses_ids,
                                               synapses_mtypes,
                                               mtype_color_dict):

    # Initially, get a dictionary where the lists corresponding to each mtype are empty
    mtypes_set = circuit.get_mtype_strings_set()

    # Create a dictionary, initialized with empty lists
    mtype_dict = {}
    for key in mtypes_set:
        mtype_dict[key] = list()

    # Iterate over the synapses ids and their corresponding mtypes to create a dictionary
    for synapse_id, synapse_mtype in zip(synapses_ids, synapses_mtypes):
        mtype_dict[synapse_mtype].append(synapse_id)

    # Create the synapses groups
    synapse_groups = list()
    for mtype in mtype_dict:

        # Create the synapse group for that specific mtype
        synapses_ids_list = mtype_dict[mtype]
        if len(synapses_ids_list) > 0:
            synapse_groups.append(nmv.bbp.SynapseGroup(
                name=mtype, synapses_ids_list=synapses_ids_list, color=mtype_color_dict[mtype]))

        # To keep consistency for the indexing over all the types, add an empty group
        else:
            synapse_groups.append(nmv.bbp.SynapseGroup(
                name=mtype, synapses_ids_list=list(), color=mtype_color_dict[mtype]))

    # Return a reference to the synapse groups
    return synapse_groups


####################################################################################################
# @create_color_coded_synapse_groups_by_etype
####################################################################################################
def create_color_coded_synapse_groups_by_etype(circuit,
                                               synapses_ids,
                                               synapses_etypes,
                                               etype_color_dict):

    # Initially, get a dictionary where the lists corresponding to each etype are empty
    etypes_set = circuit.get_etype_strings_set()

    # Create a dictionary, initialized with empty lists
    etype_dict = {}
    for key in etypes_set:
        etype_dict[key] = list()

    # Iterate over the synapses ids and their corresponding etypes to create a dictionary
    for synapse_id, synapse_etype in zip(synapses_ids, synapses_etypes):
        etype_dict[synapse_etype].append(synapse_id)

    # Create the synapses groups
    synapse_groups = list()
    for etype in etype_dict:

        # Create the synapse group for that specific etype
        synapses_ids_list = etype_dict[etype]
        if len(synapses_ids_list) > 0:
            synapse_groups.append(nmv.bbp.SynapseGroup(
                name=etype, synapses_ids_list=synapses_ids_list, color=etype_color_dict[etype]))

        # To keep consistency for the indexing over all the types, add an empty group
        else:
            synapse_groups.append(nmv.bbp.SynapseGroup(
                name=etype, synapses_ids_list=list(), color=etype_color_dict[etype]))

    # Return a reference to the synapse groups
    return synapse_groups


####################################################################################################
# @get_excitatory_and_inhibitory_synapses_color_coded_dict
####################################################################################################
def get_excitatory_and_inhibitory_synapses_color_coded_dict(circuit,
                                                            gid,
                                                            load_excitatory=True,
                                                            load_inhibitory=True,
                                                            exc_color='#ff0000',
                                                            inh_color='#0000ff'):
    """Returns a color-coded dictionary containing the inhibitory and excitatory synapses or either
    any of them.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID for which the synapses will be returned. Note that the synapse IDs are unique.
    :param load_excitatory:
        If this flag is set, the excitatory synapses will be loaded.
    :param load_inhibitory:
        If this flag is set, the inhibitory synapses will be loaded.
    :param exc_color:
        A Vector containing the RGB color of the excitatory synapses.
    :param inh_color:
        A vector containing the RGB color of the inhibitory synapses.
    :return:
        A color-coded dictionary containing the inhibitory and excitatory synapses.
    """

    # Get the IDs of all the synapses on the neuron
    synapse_ids_list = circuit.get_all_synapses_ids(gid=gid)

    # Get the IDs of the types of the synapses
    synapse_types_ids = circuit.get_synapse_types_ids(synapse_ids_list=synapse_ids_list)

    # A list that will collect the synapses
    excitatory_synapses = list()
    inhibitory_synapses = list()

    for i, synapse_type_id in enumerate(synapse_types_ids):
        if circuit.is_synapse_inhibitory(synapse_type_id):
            inhibitory_synapses.append(synapse_ids_list[i])
        else:
            excitatory_synapses.append(synapse_ids_list[i])

    # Construct and return the dict of the synapses
    if load_excitatory and load_inhibitory:
        synapses_color_coded_dict = {
            'Excitatory Synapses': {exc_color: excitatory_synapses},
            'Inhibitory Synapses': {inh_color: inhibitory_synapses}}
        return synapses_color_coded_dict
    elif load_excitatory and not load_inhibitory:
        synapses_color_coded_dict = {
            'Excitatory Synapses': {exc_color: excitatory_synapses}}
        return synapses_color_coded_dict
    elif not load_excitatory and load_inhibitory:
        synapses_color_coded_dict = {
            'Inhibitory Synapses': {inh_color: inhibitory_synapses}}
        return synapses_color_coded_dict

    return None