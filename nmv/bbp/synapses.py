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
import nmv.consts


def is_axo_somatic_synapse(circuit, synapse_id):
    import bluepy
    import morphio
    value = circuit.connectome.synapse_properties(
        numpy.array([synapse_id]), [bluepy.enums.Synapse.POST_SECTION_ID])\
        [bluepy.enums.Synapse.POST_SECTION_ID].values.tolist()[0]
    print(type(value), value)
    if value == 0:

        return True
    else:
        return False


####################################################################################################
# @is_inhibitory_synapse
####################################################################################################
def is_inhibitory_synapse(circuit,
                          synapse_type):
    """Returns True if the synapse, that is identified by its type, is inhibitory, otherwise False.

    :param synapse_type:
        An integer representing the synapse type. It is agreed in BluePy that all the synapse types
        above 100 are excitatory, otherwise inhibitory.
    :return:
        True if the synapse is inhibitory, and False otherwise.
    """

    return circuit.is_synapse_inhibitory(synapse_type_id=synapse_type)


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

    synapses_ids_list = circuit.get_afferent_synapses_ids(gid=gid)
    synapses_ids_list.extend(circuit.get_efferent_synapses_ids(gid=gid))
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
# @create_color_coded_synapse_groups_by_pre_etype
####################################################################################################
def create_color_coded_synapse_groups_by_pre_etype(circuit,
                                                   post_gid,
                                                   etype_color_dict=None):
    # Get the afferent synapses of the post_gid
    afferent_synapses_ids = circuit.get_afferent_synapses_ids(gid=post_gid)

    # Get the mtypes of the pre-synaptic cells
    afferent_synapses_etypes = circuit.get_pre_synaptic_etypes(
        afferent_synapses_ids_list=afferent_synapses_ids)

    return create_color_coded_synapse_groups_by_etype(circuit=circuit,
                                                      synapses_ids=afferent_synapses_ids,
                                                      synapses_mtypes=afferent_synapses_etypes,
                                                      etype_color_dict=etype_color_dict)


####################################################################################################
# @create_color_coded_synapse_groups_by_post_etype
####################################################################################################
def create_color_coded_synapse_groups_by_post_etype(circuit,
                                                    pre_gid,
                                                    mtype_color_dict=None):
    # Get the afferent synapses of the post_gid
    efferent_synapses_ids = get_efferent_synapses_ids(circuit=circuit, gid=pre_gid)

    # Get the mtypes of the pre-synaptic cells
    efferent_synapses_etypes = get_post_synaptic_etypes(
        circuit=circuit, efferent_synapses_ids_list=efferent_synapses_ids)

    return create_color_coded_synapse_groups_by_etype(circuit=circuit,
                                                      synapses_ids=efferent_synapses_ids,
                                                      synapses_mtypes=efferent_synapses_etypes,
                                                      etype_color_dict=etype_color_dict)


def get_spines(circuit, post_gid):

    import bluepy
    # Get the IDs of the afferent synapses of a given GID
    afferent_synapses_ids = circuit.connectome.afferent_synapses(post_gid)

    # Get the GIDs of all the pre-synaptic cells
    pre_gids = circuit.connectome.synapse_properties(
        afferent_synapses_ids, [bluepy.enums.Synapse.PRE_GID]).values
    pre_gids = [gid[0] for gid in pre_gids]

    # Get the positions of the incoming synapses at the post synaptic side
    post_synaptic_center_positions = circuit.connectome.synapse_positions(
        afferent_synapses_ids, 'post', 'center').values.tolist()

    pre_synaptic_center_positions = circuit.connectome.synapse_positions(
        afferent_synapses_ids, 'pre', 'center').values.tolist()

    pre_synaptic_contour_positions = circuit.connectome.synapse_positions(
        afferent_synapses_ids, 'pre', 'contour').values.tolist()

    import nmv.skeleton
    spines = list()
    for i in range(len(pre_gids)):

        #if random.uniform(0, 1) > 0.25: continue

        # Synapse position is the mid-way between the pre- and post-synaptic centers
        post_synaptic_center_position = Vector((post_synaptic_center_positions[i][0],
                                         post_synaptic_center_positions[i][1],
                                         post_synaptic_center_positions[i][2]))

        pre_synaptic_center_position = Vector((pre_synaptic_center_positions[i][0],
                                        pre_synaptic_center_positions[i][1],
                                        pre_synaptic_center_positions[i][2]))

        pre_synaptic_contour_position = Vector((pre_synaptic_contour_positions[i][0],
                                               pre_synaptic_contour_positions[i][1],
                                               pre_synaptic_contour_positions[i][2]))

        #position = 0.5 * (post_synaptic_position + pre_synaptic_position)

        spine = nmv.skeleton.Spine()
        spine.pre_synaptic_position = pre_synaptic_center_position
        spine.post_synaptic_position = post_synaptic_center_position

        # To determine the spine size
        spine.size = (pre_synaptic_contour_position - post_synaptic_center_position).length
        print(spine.size)
        spines.append(spine)

    return spines


def get_spines_for_synaptic_pair(circuit,
                                      pre_gid,
                                      post_gid):

    import bluepy
    # Get the IDs of the afferent synapses of a given GID
    afferent_synapses_ids = circuit.connectome.afferent_synapses(post_gid)

    # Get the GIDs of all the pre-synaptic cells
    pre_gids = circuit.connectome.synapse_properties(
        afferent_synapses_ids, [bluepy.enums.Synapse.PRE_GID]).values
    pre_gids = [gid[0] for gid in pre_gids]

    # Get the positions of the incoming synapses at the post synaptic side
    post_synaptic_positions = circuit.connectome.synapse_positions(
        afferent_synapses_ids, 'post', 'center').values.tolist()
    pre_synaptic_positions = circuit.connectome.synapse_positions(
        afferent_synapses_ids, 'pre', 'contour').values.tolist()

    import nmv.skeleton
    spines = list()
    for i in range(len(pre_gids)):

        # Get only the shared synapses with the pre-synaptic gid
        if pre_gid == int(pre_gids[i]):

            # Synapse position is the mid-way between the pre- and post-synaptic centers
            post_synaptic_position = Vector((post_synaptic_positions[i][0],
                                             post_synaptic_positions[i][1],
                                             post_synaptic_positions[i][2]))

            pre_synaptic_position = Vector((pre_synaptic_positions[i][0],
                                            pre_synaptic_positions[i][1],
                                            pre_synaptic_positions[i][2]))

            position = 0.5 * (post_synaptic_position + pre_synaptic_position)

            spine = nmv.skeleton.Spine()
            spine.pre_synaptic_position = pre_synaptic_position
            spine.post_synaptic_position = post_synaptic_position

            spines.append(spine)

    return spines


def create_shared_synapse_group(circuit,
                                pre_gid,
                                post_gid):

    import bluepy

    # Get the IDs of the afferent synapses of a given GID
    afferent_synapses_ids = circuit.connectome.afferent_synapses(post_gid)

    # Get the GIDs of all the pre-synaptic cells
    pre_gids = circuit.connectome.synapse_properties(
        afferent_synapses_ids, [bluepy.enums.Synapse.PRE_GID]).values
    pre_gids = [gid[0] for gid in pre_gids]

    # A list that will contain all the synapse meshes
    synapse_objects = list()

    # Get the positions of the incoming synapses at the post synaptic side
    post_synaptic_positions = circuit.connectome.synapse_positions(
        afferent_synapses_ids, 'post', 'center').values.tolist()
    pre_synaptic_positions = circuit.connectome.synapse_positions(
        afferent_synapses_ids, 'pre', 'contour').values.tolist()

    # Do it for all the synapses
    synapses_ids_list = list()
    for i in range(len(pre_gids)):

        # Get only the shared synapses with the pre-synaptic gid
        if pre_gid == int(pre_gids[i]):
            synapses_ids_list.append(afferent_synapses_ids[i])

            continue
            # Synapse position is the mid-way between the pre- and post-synaptic centers
            post_synaptic_position = Vector((post_synaptic_positions[i][0],
                                             post_synaptic_positions[i][1],
                                             post_synaptic_positions[i][2]))

            pre_synaptic_position = Vector((pre_synaptic_positions[i][0],
                                            pre_synaptic_positions[i][1],
                                            pre_synaptic_positions[i][2]))

            position = 0.5 * (post_synaptic_position + pre_synaptic_position)

    return [nmv.bbp.SynapseGroup(name='Shared',
                                 synapses_ids_list=synapses_ids_list, color=(1.0, 0.0, 0.0))]


####################################################################################################
# @get_excitatory_synapse_group
####################################################################################################
def get_excitatory_synapse_group(circuit,
                                 gid,
                                 color):

    return nmv.bbp.SynapseGroup(
        name='Excitatory Synapses',
        color=nmv.utilities.confirm_rgb_color_from_color_string(color),
        synapses_ids_list=circuit.get_excitatory_synapses_ids(gid=gid))


####################################################################################################
# @get_inhibitory_synapse_group
####################################################################################################
def get_inhibitory_synapse_group(circuit,
                                 gid,
                                 color):

    return nmv.bbp.SynapseGroup(
        name='Inhibitory Synapses',
        color=nmv.utilities.confirm_rgb_color_from_color_string(color),
        synapses_ids_list=circuit.get_inhibitory_synapses_ids(gid=gid))


####################################################################################################
# @get_shared_synapses_group_between_two_neurons
####################################################################################################
def get_shared_synapses_group_between_two_neurons(circuit,
                                                  pre_gid,
                                                  post_gid,
                                                  color):

    # Get the shared synapses IDs
    shared_synapses_ids = circuit.get_shared_synapses_ids_between_two_neurons(
        pre_gid=pre_gid, post_gid=post_gid)

    return nmv.bbp.SynapseGroup(
        name='Shared Synapses [%s -> %s]' % (str(pre_gid), str(post_gid)),
        color=nmv.utilities.confirm_rgb_color_from_color_string(color),
        synapses_ids_list=shared_synapses_ids)


####################################################################################################
# @get_afferent_synapse_groups_color_coded_by_pre_mtypes
####################################################################################################
def get_afferent_synapse_groups_color_coded_by_pre_mtypes(circuit,
                                                          gid,
                                                          mtype_color_dict):

    # Get the afferent synapses of the given GID
    afferent_synapses_ids = circuit.get_afferent_synapses_ids(gid=gid)

    # Get the mtypes of the pre-synaptic cells
    afferent_synapses_mtypes = circuit.get_pre_synaptic_mtypes(
        afferent_synapses_ids_list=afferent_synapses_ids)

    # Create and return the color coded synapses
    return nmv.bbp.create_color_coded_synapse_groups_by_mtype(
        circuit=circuit, synapses_ids=afferent_synapses_ids,
        synapses_mtypes=afferent_synapses_mtypes, mtype_color_dict=mtype_color_dict)


####################################################################################################
# @get_afferent_synapse_groups_color_coded_by_pre_etypes
####################################################################################################
def get_afferent_synapse_groups_color_coded_by_pre_etypes(circuit,
                                                          gid,
                                                          etype_color_dict):

    # Get the afferent synapses of the given GID
    afferent_synapses_ids = circuit.get_afferent_synapses_ids(gid=gid)

    # Get the mtypes of the pre-synaptic cells
    afferent_synapses_etypes = circuit.get_pre_synaptic_etypes(
        afferent_synapses_ids_list=afferent_synapses_ids)

    # Create and return the color coded synapses
    return nmv.bbp.create_color_coded_synapse_groups_by_etype(
        circuit=circuit, synapses_ids=afferent_synapses_ids,
        synapses_etypes=afferent_synapses_etypes, etype_color_dict=etype_color_dict)


####################################################################################################
# @get_efferent_synapse_groups_color_coded_by_post_mtypes
####################################################################################################
def get_efferent_synapse_groups_color_coded_by_post_mtypes(circuit,
                                                           gid,
                                                           mtype_color_dict):

    # Get the efferent synapses of the given GID
    efferent_synapses_ids = circuit.get_efferent_synapses_ids(gid=gid)

    # Get the mtypes of the post-synaptic cells
    efferent_synapses_mtypes = circuit.get_post_synaptic_mtypes(
        efferent_synapses_ids_list=efferent_synapses_ids)

    # Create and return the color coded synapses
    return nmv.bbp.create_color_coded_synapse_groups_by_mtype(
        circuit=circuit, synapses_ids=efferent_synapses_ids,
        synapses_mtypes=efferent_synapses_mtypes, mtype_color_dict=mtype_color_dict)


####################################################################################################
# @get_efferent_synapse_groups_color_coded_by_post_etypes
####################################################################################################
def get_efferent_synapse_groups_color_coded_by_post_etypes(circuit,
                                                           gid,
                                                           etype_color_dict):

    # Get the efferent synapses of the given GID
    efferent_synapses_ids = circuit.get_efferent_synapses_ids(gid=gid)

    # Get the etypes of the post-synaptic cells
    efferent_synapses_etypes = circuit.get_post_synaptic_etypes(
        efferent_synapses_ids_list=efferent_synapses_ids)

    # Create and return the color coded synapses
    return nmv.bbp.create_color_coded_synapse_groups_by_etype(
        circuit=circuit, synapses_ids=efferent_synapses_ids,
        synapses_etypes=efferent_synapses_etypes, etype_color_dict=etype_color_dict)


####################################################################################################
# @get_excitatory_and_inhibitory_synapse_groups
####################################################################################################
def get_excitatory_and_inhibitory_synapse_groups(circuit,
                                                 gid,
                                                 load_excitatory=True,
                                                 load_inhibitory=True,
                                                 exc_color='#ff0000',
                                                 inh_color='#0000ff'):

    # Get the color coded dictionary
    color_coded_synapses_dict = nmv.bbp.get_excitatory_and_inhibitory_synapses_color_coded_dict(
        circuit=circuit, gid=gid, load_excitatory=load_excitatory, load_inhibitory=load_inhibitory,
        exc_color=exc_color, inh_color=inh_color)

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
# @get_afferent_synapse_group
####################################################################################################
def get_afferent_synapse_group(circuit,
                               gid,
                               color):

    return nmv.bbp.SynapseGroup(
        name='Afferent Synapses',
        color=nmv.utilities.confirm_rgb_color_from_color_string(color),
        synapses_ids_list=circuit.get_afferent_synapses_ids(gid=gid))


####################################################################################################
# @get_efferent_synapse_group
####################################################################################################
def get_efferent_synapse_group(circuit,
                               gid,
                               color):

    return nmv.bbp.SynapseGroup(
        name='Efferent Synapses',
        color=nmv.utilities.confirm_rgb_color_from_color_string(color),
        synapses_ids_list=circuit.get_efferent_synapses_ids(gid=gid))
