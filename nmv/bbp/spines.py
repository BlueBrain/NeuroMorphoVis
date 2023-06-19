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


####################################################################################################
# @get_spines
####################################################################################################
def get_spines(circuit,
               post_gid):
    """Get a list of all the spines on a post synaptic neuron.

    :param circuit:
        BBP circuit.
    :param post_gid:
        The GID of the post-synaptic neuron.
    :return:
    """

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
        spines.append(spine)

    # Return the spines list
    return spines


####################################################################################################
# @get_spines_for_synaptic_pair
####################################################################################################
def get_spines_for_synaptic_pair(circuit,
                                 pre_gid,
                                 post_gid):
    """Gets the spines for a synaptic pair.

    :param circuit:
        BBP circuit.
    :param pre_gid:
        The GID of the pre-synaptic neuron.
    :param post_gid:
        The GID of the post-synaptic neuron.
    :return:
        A list of the resulting synapses.
    """

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

    # Return the spines list
    return spines
