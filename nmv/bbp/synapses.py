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

# System imports
import numpy
import random

# Blender imports
from mathutils import Vector

# Internal import
import nmv.geometry
import nmv.mesh
import nmv.enums
import nmv.shading
import nmv.utilities


####################################################################################################
# @is_inhibitory_synapse
####################################################################################################
def is_inhibitory_synapse(synapse_type):
    """Returns True if the synapse, that is identified by its type, is inhibitory, otherwise False.

    :param synapse_type:
        An integer representing the synapse type. It is agreed in BluePy that all the synapse types
        above 100 are excitatory, otherwise inhibitory.
    :return:
        True if the synapse is inhibitory, and False otherwise.
    """

    return True if synapse_type < 100 else False


####################################################################################################
# @get_afferent_synapses_ids
####################################################################################################
def get_afferent_synapses_ids(circuit,
                              gid):
    """Returns a list of unique (on-the-circuit-level) IDs of the afferent (incoming) synapses of
    a post-synaptic neuron specified by its GID.

    NOTE: efferent (pre-synaptic) neuron -> synapse -> afferent (post-synaptic) neuron

    :param circuit:
        BBP circuit.
    :param gid:
        Post-synaptic GID.
    :return:
        Synapse IDs list.
    """

    return circuit.connectome.afferent_synapses(int(gid)).tolist()


####################################################################################################
# @get_efferent_synapses_ids
####################################################################################################
def get_efferent_synapses_ids(circuit,
                              gid):
    """Returns a list of unique (on-the-circuit-level) IDs of the efferent (outgoing) synapses of
    a pre-synaptic neuron specified by its GID.

    NOTE: efferent (pre-synaptic) neuron -> synapse -> afferent (post-synaptic) neuron

    :param circuit:
        BBP circuit.
    :param gid:
        Pre-synaptic GID.
    :return:
        Synapse IDs list.
    """
    return circuit.connectome.efferent_synapses(int(gid)).tolist()


####################################################################################################
# @get_all_synapses_ids
####################################################################################################
def get_all_synapses_ids(circuit,
                         gid):
    """Returns a list of unique (on-the-circuit-level) IDs of all the synapses of a neuron
    specified by its GID.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :return:
        Synapse IDs list.
    """

    synapses_ids_list = get_afferent_synapses_ids(circuit=circuit, gid=gid)
    synapses_ids_list.extend(get_efferent_synapses_ids(circuit=circuit, gid=gid))
    return synapses_ids_list


####################################################################################################
# @get_pre_synaptic_synapse_positions
####################################################################################################
def get_pre_synaptic_synapse_positions(circuit,
                                       synapse_ids_list):
    """Returns a list of all the pre-synaptic positions of a given list of synapses.

    NOTE: efferent (pre-synaptic) neuron -> synapse -> afferent (post-synaptic) neuron

    :param circuit:
        BBP circuit.
    :param synapse_ids_list:
        A list of all the IDs of the requested synapses.
    :return:
        A list of all the pre-synaptic positions of a given list of synapses.
    """

    return circuit.connectome.synapse_positions(
        numpy.array(synapse_ids_list), 'pre', 'contour').values.tolist()


####################################################################################################
# @get_post_synaptic_synapse_positions
####################################################################################################
def get_post_synaptic_synapse_positions(circuit,
                                        synapse_ids_list):
    """Returns a list of all the post-synaptic positions of a given list of synapses.

    NOTE: efferent (pre-synaptic) neuron -> synapse -> afferent (post-synaptic) neuron

    :param circuit:
        BBP circuit.
    :param synapse_ids_list:
        A list of all the IDs of the requested synapses.
    :return:
        A list of all the post-synaptic positions of a given list of synapses.
    """

    return circuit.connectome.synapse_positions(
        numpy.array(synapse_ids_list), 'post', 'center').values.tolist()


####################################################################################################
# @get_synapse_mtypes_ids
####################################################################################################
def get_synapse_mtypes_ids(circuit,
                           synapse_ids_list):
    """Returns the IDs of the morphological types of a given list of synapses.

    :param circuit:
        BBP circuit.
    :param synapse_ids_list:
        A list of IDs of synapses.
    :return:
        A list of IDs of the morphological types of the given synapses in the same order.
    """

    import bluepy
    return circuit.connectome.synapse_properties(
        numpy.array(synapse_ids_list),
        [bluepy.enums.Synapse.TYPE])[bluepy.enums.Synapse.TYPE].values.tolist()


####################################################################################################
# @get_pre_synaptic_mtypes
####################################################################################################
def get_pre_synaptic_mtypes(circuit,
                            afferent_synapses_ids_list):
    """Returns a list of strings representing the morphological types of the pre-synaptic cells
    forming the given afferent synapses list.

    NOTE: efferent (pre-synaptic) neuron -> synapse -> afferent (post-synaptic) neuron

    :param circuit:
        BBP circuit.
    :param afferent_synapses_ids_list:
        A list of the IDs of the afferent synapses.
    :return:
        A list of the morphological types of the pre-synaptic cells of the given synapses list in
        the same order.
    """

    import bluepy
    pre_synaptic_gids = circuit.connectome.synapse_properties(
        numpy.array(afferent_synapses_ids_list),
        [bluepy.enums.Synapse.PRE_GID])[bluepy.enums.Synapse.PRE_GID].values.tolist()
    return circuit.cells.get(pre_synaptic_gids)['mtype'].values.tolist()


####################################################################################################
# @get_post_synaptic_mtypes
####################################################################################################
def get_post_synaptic_mtypes(circuit,
                             efferent_synapses_ids_list):
    """Returns a list of strings representing the morphological types of the post-synaptic cells
   forming the given efferent synapses list.

   NOTE: efferent (pre-synaptic) neuron -> synapse -> afferent (post-synaptic) neuron

   :param circuit:
       BBP circuit.
   :param efferent_synapses_ids_list:
       A list of the IDs of the efferent synapses.
   :return:
       A list of the morphological types of the pre-synaptic cells of the given synapses list in
       the same order.
   """

    import bluepy
    post_synaptic_gids = circuit.connectome.synapse_properties(
        numpy.array(efferent_synapses_ids_list),
        [bluepy.enums.Synapse.POST_GID])[bluepy.enums.Synapse.POST_GID].values.tolist()
    return circuit.cells.get(post_synaptic_gids)['mtype'].values.tolist()


####################################################################################################
# @get_pre_synaptic_etypes
####################################################################################################
def get_pre_synaptic_etypes(circuit,
                            afferent_synapses_ids_list):
    """Returns a list of strings representing the electrophysiological types of the pre-synaptic
    cells forming the given afferent synapses list.

    NOTE: efferent (pre-synaptic) neuron -> synapse -> afferent (post-synaptic) neuron

    :param circuit:
        BBP circuit.
    :param afferent_synapses_ids_list:
        A list of the IDs of the afferent synapses.
    :return:
        A list of the electrophysiological types of the pre-synaptic cells of the given synapses
        list in the same order.
    """

    import bluepy
    pre_synaptic_gids = circuit.connectome.synapse_properties(
        numpy.array(afferent_synapses_ids_list),
        [bluepy.enums.Synapse.PRE_GID])[bluepy.enums.Synapse.PRE_GID].values.tolist()
    return circuit.cells.get(pre_synaptic_gids)['etype'].values.tolist()


####################################################################################################
# @get_post_synaptic_etypes
####################################################################################################
def get_post_synaptic_etypes(circuit,
                             efferent_synapses_ids_list):
    """Returns a list of strings representing the electrophysiological types of the post-synaptic
    cells forming the given efferent synapses list.

   NOTE: efferent (pre-synaptic) neuron -> synapse -> afferent (post-synaptic) neuron

   :param circuit:
       BBP circuit.
   :param efferent_synapses_ids_list:
       A list of the IDs of the efferent synapses.
   :return:
       A list of the electrophysiological types of the pre-synaptic cells of the given synapses
       list in the same order.
   """

    import bluepy
    post_synaptic_gids = circuit.connectome.synapse_properties(
        numpy.array(efferent_synapses_ids_list),
        [bluepy.enums.Synapse.POST_GID])[bluepy.enums.Synapse.POST_GID].values.tolist()
    return circuit.cells.get(post_synaptic_gids)['etype'].values.tolist()


####################################################################################################
# @get_excitatory_and_inhibitory_synapses_color_coded_dict
####################################################################################################
def get_excitatory_and_inhibitory_synapses_color_coded_dict(circuit,
                                                            gid,
                                                            exc_color='#ff0000',
                                                            inh_color='#0000ff'):
    """Returns a color-coded dictionary containing the inhibitory and excitatory synapses.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID for which the synapses will be returned. Note that the synapse IDs are unique.
    :param exc_color:
        A Vector containing the RGB color of the excitatory synapses.
    :param inh_color:
        A vector containing the RGB color of the inhibitory synapses.
    :return:
        A color-coded dictionary containing the inhibitory and excitatory synapses.
    """

    # Get the IDs of all the synapses on the neuron
    synapse_ids = get_all_synapses_ids(circuit=circuit, gid=gid)

    # Get the IDs of the types of the synapses
    synapse_mtypes_ids = get_synapse_mtypes_ids(circuit=circuit, synapse_ids_list=synapse_ids)

    # A list that will collect the synapses
    excitatory_synapses = list()
    inhibitory_synapses = list()

    for i, synapse in enumerate(synapse_mtypes_ids):
        if is_inhibitory_synapse(synapse):
            inhibitory_synapses.append(synapse_ids[i])
        else:
            excitatory_synapses.append(synapse_ids[i])

    # Construct and return the dict of the synapses
    synapses_color_coded_dict = {
        'Excitatory Synapses': {exc_color: excitatory_synapses},
        'Inhibitory Synapses': {inh_color: inhibitory_synapses}}
    return synapses_color_coded_dict


####################################################################################################
# @get_pre_mtype_synapses_mtype_coded_dict
####################################################################################################
def get_pre_mtype_synapses_mtype_coded_dict(circuit,
                                            post_gid,
                                            color_coded_mtype_dict):
    """
    # thats mainly on dendrites

    :param circuit:
    :type circuit:
    :param post_gid:
    :type post_gid:
    :return:
    :rtype:
    """

    # Get the afferent synapses of the post_gid
    afferent_synapses_ids = get_afferent_synapses_ids(circuit=circuit, gid=post_gid)

    # Get the mtypes of the pre-synaptic cells
    afferent_synapses_mtypes = get_pre_synaptic_mtypes(
        circuit=circuit, afferent_synapses_ids_list=afferent_synapses_ids)

    # Initially, get a dictionary where the lists corresponding to each mtype are empty
    mtype_set = nmv.bbp.get_circuit_mtype_strings_set(circuit=circuit)
    mtype_dict = dict.fromkeys(mtype_set, dict())

    # Update the mtypes lists
    synapses_mtype_coded_dict = dict.fromkeys(set(color_coded_mtype_dict.values()), list())
    print(synapses_mtype_coded_dict)
    for i, mtype in enumerate(afferent_synapses_mtypes):

        mtype_key = afferent_synapses_mtypes[i]
        synapse_id = afferent_synapses_ids[i]

        color = color_coded_mtype_dict[mtype_key]

        synapses_ids_list = synapses_mtype_coded_dict[color]
        synapses_ids_list.append(synapse_id)


    for key in color_coded_mtype_dict:
        mtype = key
        color = color_coded_mtype_dict[key]

        print(key, color)

        synapse_list = synapses_mtype_coded_dict[color]
        print(len(synapse_list))

        mtype_dict[mtype] = {color: synapse_list}







    return mtype_dict


####################################################################################################
# @get_color_coded_synapse_dict_from_color_coded_mtype_dict
####################################################################################################
def get_color_coded_synapse_dict_from_color_coded_mtype_dict(mtype_color_dict,
                                                             mtype_synapses_dict):
    color_coded_synapse_dict = {}
    for key in mtype_color_dict:
        color_coded_synapse_dict[key] = mtype_synapses_dict[key]








def get_post_mtype_synapses_color_coded_dict(circuit,
                                            pre_gid,
                                            mtype_color_coded_dict):


    # That's mainly on axons

    # Get the afferent synapses of the post_gid

    # Get the mtypes of the pre synaptic cells

    # Adjust the map

    # return the dictionary

    pass






####################################################################################################
# @get_color_coded_synapse_dict
####################################################################################################
def get_color_coded_synapse_dict(synapse_json_file):
    """Returns a dictionary containing color-coded lists of synapses. The keys represent the
    colors in hex format and the values are lists of synapse IDs.

    :param synapse_json_file:
        The absolute path to json files containing synapses IDs and their group colors.
    :return:
        A dictionary containing color-coded lists of synapses. The keys represent the
    colors in hex format and the values are lists of synapse IDs.
    """

    # Load the data from the JSON file
    try:
        f = open(synapse_json_file)
    except FileNotFoundError:
        print("The synapse json file [%s] is NOT found!" % synapse_json_file)
        return None

    # Load all the data from the file
    import json
    data_dict = json.load(f)
    f.close()

    # Return the loaded dictionary
    return data_dict


####################################################################################################
# @get_synapse_groups_from_color_coded_json_file
####################################################################################################
def get_synapse_groups_from_color_coded_json_file(synapse_json_file):

    # Read the file into the dictionary
    color_coded_synapses_dict = nmv.bbp.get_color_coded_synapse_dict(synapse_json_file)

    # Construct the groups
    synapse_groups = list()
    for key in color_coded_synapses_dict:

        group_name = key
        group_value = color_coded_synapses_dict[key]
        group_color = list(group_value.keys())[0]
        group_synapses_list = group_value[group_color]

        synapse_group = nmv.bbp.SynapseGroup(
            name=group_name,
            color=nmv.utilities.confirm_rgb_color_from_color_string(group_color),
            synapses_ids_list=group_synapses_list)
        synapse_groups.append(synapse_group)

    # Return a reference to the synapse group
    return synapse_groups


####################################################################################################
# @get_exc_and_inhibitory_synapse_groups_from_circuit
####################################################################################################
def get_exc_and_inhibitory_synapse_groups_from_circuit(circuit,
                                                       gid,
                                                       exc_color,
                                                       inh_color):

    # Get the color coded dictionary
    color_coded_synapses_dict = nmv.bbp.get_excitatory_and_inhibitory_synapses_color_coded_dict(
        circuit=circuit, gid=gid, exc_color=exc_color, inh_color=inh_color)

    # Construct the groups
    synapse_groups = list()
    for key in color_coded_synapses_dict:

        group_name = key
        group_value = color_coded_synapses_dict[key]
        group_color = list(group_value.keys())[0]
        group_synapses_list = group_value[group_color]

        synapse_group = nmv.bbp.SynapseGroup(
            name=group_name,
            color=nmv.utilities.confirm_rgb_color_from_color_string(group_color),
            synapses_ids_list=group_synapses_list)
        synapse_groups.append(synapse_group)

    # Return a reference to the synapse group
    return synapse_groups


####################################################################################################
# @create_color_coded_synapse_groups_by_mtype
####################################################################################################
def create_color_coded_synapse_groups_by_mtype(circuit,
                                               synapses_ids,
                                               synapses_mtypes,
                                               mtype_color_dict=None):

    # Initially, get a dictionary where the lists corresponding to each mtype are empty
    mtypes_set = nmv.bbp.get_circuit_mtype_strings_set(circuit=circuit)

    # Create a dictionary, initialized with empty lists
    mtype_dict = {}
    for key in mtypes_set:
        mtype_dict[key] = list()

    # Iterate over the afferent_synapses_ids and afferent_synapses_mtypes list
    for synapse_id, synapse_mtype in zip(synapses_ids, synapses_mtypes):
        mtype_dict[synapse_mtype].append(synapse_id)

    # Create the synapses groups
    synapse_groups = list()
    for mtype in mtype_dict:

        # Get a reference to the list of the synapses IDs and ensure that it is not empty
        synapses_ids_list = mtype_dict[mtype]
        if len(synapses_ids_list) > 0:

            # If the color dictionary is empty, then use random colors
            if mtype_color_dict is None:
                color = Vector((random.uniform(0.0, 1.0),
                                random.uniform(0.0, 1.0),
                                random.uniform(0.0, 1.0)))
            else:
                color = nmv.utilities.confirm_rgb_color_from_color_string(
                    color_string=mtype_color_dict[mtype])

            # Create the group and add it to the list
            synapse_groups.append(
                nmv.bbp.SynapseGroup(name=mtype, synapses_ids_list=synapses_ids_list, color=color))

    # Return a reference to the synapse groups
    return synapse_groups


####################################################################################################
# @create_color_coded_synapse_groups_by_pre_mtype
####################################################################################################
def create_color_coded_synapse_groups_by_pre_mtype(circuit,
                                                   post_gid,
                                                   mtype_color_dict=None):
    # Get the afferent synapses of the post_gid
    afferent_synapses_ids = get_afferent_synapses_ids(circuit=circuit, gid=post_gid)

    # Get the mtypes of the pre-synaptic cells
    afferent_synapses_mtypes = get_pre_synaptic_mtypes(
        circuit=circuit, afferent_synapses_ids_list=afferent_synapses_ids)

    return create_color_coded_synapse_groups_by_mtype(circuit=circuit,
                                                      synapses_ids=afferent_synapses_ids,
                                                      synapses_mtypes=afferent_synapses_mtypes,
                                                      mtype_color_dict=mtype_color_dict)


####################################################################################################
# @create_color_coded_synapse_groups_by_post_mtype
####################################################################################################
def create_color_coded_synapse_groups_by_post_mtype(circuit,
                                                    pre_gid,
                                                    mtype_color_dict=None):
    # Get the afferent synapses of the post_gid
    efferent_synapses_ids = get_efferent_synapses_ids(circuit=circuit, gid=pre_gid)

    # Get the mtypes of the pre-synaptic cells
    efferent_synapses_mtypes = get_post_synaptic_mtypes(
        circuit=circuit, efferent_synapses_ids_list=efferent_synapses_ids)

    return create_color_coded_synapse_groups_by_mtype(circuit=circuit,
                                                      synapses_ids=efferent_synapses_ids,
                                                      synapses_mtypes=efferent_synapses_mtypes,
                                                      mtype_color_dict=mtype_color_dict)


####################################################################################################
# @create_color_coded_synapse_groups_by_etype
####################################################################################################
def create_color_coded_synapse_groups_by_etype(circuit,
                                               synapses_ids,
                                               synapses_mtypes,
                                               mtype_color_dict=None):

    # Initially, get a dictionary where the lists corresponding to each mtype are empty
    etypes_set = nmv.bbp.get_circuit_etype_strings_set(circuit=circuit)

    # Create a dictionary, initialized with empty lists
    etype_dict = {}
    for key in etypes_set:
        etype_dict[key] = list()

    # Iterate over the afferent_synapses_ids and afferent_synapses_mtypes list
    for synapse_id, synapse_mtype in zip(synapses_ids, synapses_mtypes):
        etype_dict[synapse_mtype].append(synapse_id)

    # Create the synapses groups
    synapse_groups = list()
    for etype in etype_dict:

        # Get a reference to the list of the synapses IDs and ensure that it is not empty
        synapses_ids_list = etype_dict[etype]
        if len(synapses_ids_list) > 0:

            # If the color dictionary is empty, then use random colors
            if mtype_color_dict is None:
                color = Vector((random.uniform(0.0, 1.0),
                                random.uniform(0.0, 1.0),
                                random.uniform(0.0, 1.0)))
            else:
                color = nmv.utilities.confirm_rgb_color_from_color_string(
                    color_string=mtype_color_dict[etype])

            # Create the group and add it to the list
            synapse_groups.append(
                nmv.bbp.SynapseGroup(name=etype, synapses_ids_list=synapses_ids_list, color=color))

    # Return a reference to the synapse groups
    return synapse_groups


####################################################################################################
# @create_color_coded_synapse_groups_by_pre_etype
####################################################################################################
def create_color_coded_synapse_groups_by_pre_etype(circuit,
                                                   post_gid,
                                                   mtype_color_dict=None):
    # Get the afferent synapses of the post_gid
    afferent_synapses_ids = get_afferent_synapses_ids(circuit=circuit, gid=post_gid)

    # Get the mtypes of the pre-synaptic cells
    afferent_synapses_etypes = get_pre_synaptic_etypes(
        circuit=circuit, afferent_synapses_ids_list=afferent_synapses_ids)

    return create_color_coded_synapse_groups_by_etype(circuit=circuit,
                                                      synapses_ids=afferent_synapses_ids,
                                                      synapses_mtypes=afferent_synapses_etypes,
                                                      mtype_color_dict=mtype_color_dict)


