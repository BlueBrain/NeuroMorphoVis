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
from tqdm import tqdm

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

    :type synapse_type:
        An integer representing the type of the synapse.
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
# @create_synapse_group_mesh_using_spheres
####################################################################################################
def create_synapse_group_mesh_using_spheres(positions,
                                            synapse_size,
                                            group_name='synapses'):

    all_synapse_objects = list()
    per_iteration_synapse_objects = list()

    for i in range(len(positions)):

        # Create a sphere representing the synapse and append it to the list
        synapse_symbolic_sphere = nmv.geometry.create_ico_sphere(
            radius=synapse_size, location=positions[i], subdivisions=3, name='synapse_%d' % i)
        per_iteration_synapse_objects.append(synapse_symbolic_sphere)

        # NOTE: To reduce to overhead of the number of objects in the scene, we group every few
        # objects into a single object
        if i % 50 == 0:
            all_synapse_objects.append(nmv.mesh.join_mesh_objects(
                mesh_list=per_iteration_synapse_objects, name='group_%d' % (i % 100)))

            # Clear the per-iteration list
            per_iteration_synapse_objects.clear()

    # If the per-iteration list still have some synapses, append them
    if len(per_iteration_synapse_objects) == 0:
        pass
    elif len(per_iteration_synapse_objects) == 1:
        all_synapse_objects.append(per_iteration_synapse_objects[0])
    else:
        all_synapse_objects.append(nmv.mesh.join_mesh_objects(
            mesh_list=per_iteration_synapse_objects, name='group_n'))

    # Join all the synapse objects into a single mesh
    all_synapse_objects = nmv.mesh.join_mesh_objects(mesh_list=all_synapse_objects, name=group_name)

    # Return a reference to the collected synapses
    return all_synapse_objects


####################################################################################################
# @create_color_coded_synapses_mesh
####################################################################################################
def create_color_coded_synapses_mesh(circuit,
                                     color_coded_synapses_list,
                                     synapse_size=4,
                                     inverted_transformation=None,
                                     material_type=nmv.enums.Shader.LAMBERT_WARD):

    # For every group in the synapse list, create a mesh and color code it.
    for group in color_coded_synapses_list:

        # The key is the color code in HEX
        key = group[0]

        # The list of IDs
        synapse_ids = group[1]

        # The post-synaptic position
        positions = circuit.connectome.synapse_positions(
            numpy.array(synapse_ids), 'post', 'center').values.tolist()

        # Update the positions taking into consideration the transformation
        for i in range(len(positions)):
            position = Vector((positions[i][0], positions[i][1], positions[i][2]))
            if inverted_transformation is not None:
                position = inverted_transformation @ position
            positions[i] = position

        # Create the corresponding synapse mesh
        synapse_group_mesh = create_synapse_group_mesh_using_spheres(positions=positions,
                                                                     synapse_size=synapse_size,
                                                                     group_name='synapses_%s' % key)
        # Create the corresponding shader
        material_rgb_color = nmv.utilities.confirm_rgb_color(key)
        material = nmv.shading.create_material(
            name='synapses_%s' % key, color=material_rgb_color, material_type=material_type)
        nmv.shading.set_material_to_object(
            mesh_object=synapse_group_mesh, material_reference=material)










