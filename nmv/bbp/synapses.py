####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Internal import
import nmv.geometry
import nmv.mesh
import nmv.enums
import nmv.shading
import nmv.utilities
import nmv.consts


####################################################################################################
# @get_excitatory_synapse_group
####################################################################################################
def get_excitatory_synapse_group(circuit,
                                 gid,
                                 color,
                                 group_name='Excitatory Synapses'):
    """Gets a SynapseGroup of all excitatory synapses of the neuron specified by the given GID.

    :param circuit:
        A digitally reconstructed circuit.
    :param gid:
        Neuron GID.
    :param color:
        A color used to label this synapse group.
    :param group_name:
        A name to label the group, default Excitatory Synapses.
    :return:
        A SynapseGroup of all excitatory synapses of the neuron specified by the given GID.
    """

    return nmv.bbp.SynapseGroup(
        name=group_name,
        color=nmv.utilities.confirm_rgb_color_from_color_string(color),
        synapses_ids_list=circuit.get_excitatory_synapses_ids(gid=gid))


####################################################################################################
# @get_inhibitory_synapse_group
####################################################################################################
def get_inhibitory_synapse_group(circuit,
                                 gid,
                                 color,
                                 group_name='Inhibitory Synapses'):
    """Gets a SynapseGroup of all inhibitory synapses of the neuron specified by the given GID.

    :param circuit:
        A digitally reconstructed circuit.
    :param gid:
        Neuron GID.
    :param color:
        A color used to label this synapse group.
    :param group_name:
        A name to label the group, default Inhibitory Synapses.
    :return:
        A SynapseGroup of all excitatory synapses of the neuron specified by the given GID.
    """
    return nmv.bbp.SynapseGroup(
        name=group_name,
        color=nmv.utilities.confirm_rgb_color_from_color_string(color),
        synapses_ids_list=circuit.get_inhibitory_synapses_ids(gid=gid))


####################################################################################################
# @get_shared_synapses_group_between_two_neurons
####################################################################################################
def get_shared_synapses_group_between_two_neurons(circuit,
                                                  pre_gid,
                                                  post_gid,
                                                  color):
    """Gets a SynapseGroup of the shared synapses between two neurons specified by their GIDs.

    :param circuit:
        A digitally reconstructed circuit.
    :param pre_gid:
        The GID of the pre-synaptic neuron.
    :param post_gid:
        The GID of the post-synaptic neuron.
    :param color:
        A color used to label this synapse group.
    :return:
        A SynapseGroup of the shared synapses between two neurons specified by their GIDs.
    """

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
    """Gets a list of SynapseGroup elements that color-code the afferent synapses of a given
    neuron based on the mtype of the pre-synaptic neurons.

    :param circuit:
        A digitally reconstructed circuit.
    :param gid:
        Neuron GID.
    :param mtype_color_dict:
        A color dictionary, where a HEX color defines each mtype.
    :return:
        A list of SynapseGroup elements that color-code the afferent synapses of a given neuron
        based on the mtype of the pre-synaptic neurons.
    """

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
# @get_afferent_synapse_group_for_projection
####################################################################################################
def get_afferent_synapse_group_for_projection(circuit,
                                              gid,
                                              projection_name,
                                              color):

    return nmv.bbp.SynapseGroup(
        name='Afferent Synapses',
        color=nmv.utilities.confirm_rgb_color_from_color_string(color),
        synapses_ids_list=circuit.get_afferent_synapses_ids_for_projection(
            gid=gid, projection_name=projection_name))


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


