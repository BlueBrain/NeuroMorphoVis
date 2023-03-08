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

# System imports
import numpy

# Blender imports
from mathutils import Vector, Matrix

# Internal imports
import nmv.utilities
from .circuit import Circuit


####################################################################################################
# @BBPCircuit
####################################################################################################
class BBPCircuit(Circuit):
    """A wrapper on top of the circuit loading API of BluePy to facilitate loading circuit-based
    data from old circuits that are not stored in libSonata format."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 circuit_config):

        # Propagate to the base
        Circuit.__init__(self, circuit_config=circuit_config)

        # Load the circuit
        self.circuit = self.load_circuit()

    ################################################################################################
    # @get_circuit_config
    ################################################################################################
    def get_circuit_config(self):
        return self.circuit_config

    ################################################################################################
    # @get_neuron_morphology_path
    ################################################################################################
    def get_neuron_morphology_path(self,
                                   gid):

        return self.circuit.morph.get_filepath(int(gid))

    ################################################################################################
    # @load_circuit
    ################################################################################################
    def load_circuit(self):
        import bluepy
        return bluepy.Circuit(self.circuit_config)

    ################################################################################################
    # @get_mtype_strings_set
    ################################################################################################
    def get_mtype_strings_set(self):
        return sorted(self.circuit.cells.mtypes)

    ################################################################################################
    # @get_circuit_mtype_strings_list
    ################################################################################################
    def get_mtype_strings_list(self):

        return list(self.get_mtype_strings_set())

    ################################################################################################
    # @get_etype_strings_set
    ################################################################################################
    def get_etype_strings_set(self):
        return sorted(self.circuit.cells.etypes)

    ################################################################################################
    # @get_etype_strings_list
    ################################################################################################
    def get_etype_strings_list(self):
        return list(self.get_etype_strings_set())

    ################################################################################################
    # @get_neuron_translation_vector
    ################################################################################################
    def get_neuron_translation_vector(self,
                                      gid):
        # Translation
        neuron = self.circuit.cells.get(int(gid))
        return Vector((neuron['x'], neuron['y'], neuron['z']))

    ################################################################################################
    # @get_neuron_orientation_matrix
    ################################################################################################
    def get_neuron_orientation_matrix(self,
                                      gid):
        # Orientation
        neuron = self.circuit.cells.get(int(gid))
        o = neuron['orientation']
        o0 = Vector((o[0][0], o[0][1], o[0][2]))
        o1 = Vector((o[1][0], o[1][1], o[1][2]))
        o2 = Vector((o[2][0], o[2][1], o[2][2]))

        # Initialize the orientation matrix to I
        orientation_matrix = Matrix()

        orientation_matrix[0][0] = o0[0]
        orientation_matrix[0][1] = o0[1]
        orientation_matrix[0][2] = o0[2]
        orientation_matrix[0][3] = 1.0

        orientation_matrix[1][0] = o1[0]
        orientation_matrix[1][1] = o1[1]
        orientation_matrix[1][2] = o1[2]
        orientation_matrix[1][3] = 1.0

        orientation_matrix[2][0] = o2[0]
        orientation_matrix[2][1] = o2[1]
        orientation_matrix[2][2] = o2[2]
        orientation_matrix[2][3] = 1.0

        orientation_matrix[3][0] = 0.0
        orientation_matrix[3][1] = 0.0
        orientation_matrix[3][2] = 0.0
        orientation_matrix[3][3] = 1.0

        return orientation_matrix

    ################################################################################################
    # @get_neuron_transformation_matrix
    ################################################################################################
    def get_neuron_transformation_matrix(self,
                                         gid):
        # Translation
        translation_vector = self.get_neuron_translation_vector(gid=gid)

        # Get the orientation and update the translation elements in the orientation matrix
        matrix = self.get_neuron_orientation_matrix(gid=gid)
        matrix[0][3] = translation_vector[0]
        matrix[1][3] = translation_vector[1]
        matrix[2][3] = translation_vector[2]

        return matrix

    ################################################################################################
    # @get_neuron_inverse_transformation_matrix
    ################################################################################################
    def get_neuron_inverse_transformation_matrix(self,
                                                 gid):
        return self.get_neuron_transformation_matrix(gid=gid).inverted()

    ################################################################################################
    # @get_afferent_synapses_ids
    ################################################################################################
    def get_afferent_synapses_ids(self,
                                  gid):
        ids = self.circuit.connectome.afferent_synapses(int(gid))
        return ids if isinstance(ids, list) else ids.tolist()

    ################################################################################################
    # @get_efferent_synapses_ids
    ################################################################################################
    def get_efferent_synapses_ids(self,
                                  gid):
        ids = self.circuit.connectome.efferent_synapses(int(gid))
        return ids if isinstance(ids, list) else ids.tolist()

    ################################################################################################
    # @get_all_synapses_ids
    ################################################################################################
    def get_all_synapses_ids(self,
                             gid):
        synapses_ids_list = self.get_afferent_synapses_ids(gid=gid)
        synapses_ids_list.extend(self.get_efferent_synapses_ids(gid=gid))
        return synapses_ids_list

    ################################################################################################
    # @get_synapse_types_ids
    ################################################################################################
    def get_synapse_types_ids(self,
                              synapse_ids_list):

        import bluepy
        ids = self.circuit.connectome.synapse_properties(
            numpy.array(synapse_ids_list),
            [bluepy.enums.Synapse.TYPE])[bluepy.enums.Synapse.TYPE].values.tolist()

    ################################################################################################
    # @get_pre_synaptic_synapse_positions
    ################################################################################################
    def get_pre_synaptic_synapse_positions(self,
                                           synapse_ids_list,
                                           synapse_location='center'):

        # synapse_location could be 'contour' or 'center'
        return self.circuit.connectome.synapse_positions(
            numpy.array(synapse_ids_list), 'pre', synapse_location).values.tolist()

    ################################################################################################
    # @get_post_synaptic_synapse_positions
    ################################################################################################
    def get_post_synaptic_synapse_positions(self,
                                            synapse_ids_list,
                                            synapse_location='center'):

        return self.circuit.connectome.synapse_positions(
            numpy.array(synapse_ids_list), 'post', synapse_location).values.tolist()

    ################################################################################################
    # @get_synapse_mtypes_ids
    ################################################################################################
    def get_synapse_mtypes_ids(self,
                               synapse_ids_list):

        import bluepy
        return self.circuit.connectome.synapse_properties(
            numpy.array(synapse_ids_list),
            [bluepy.enums.Synapse.TYPE])[bluepy.enums.Synapse.TYPE].values.tolist()

    ################################################################################################
    # @get_pre_synaptic_mtypes
    ################################################################################################
    def get_pre_synaptic_mtypes(self,
                                afferent_synapses_ids_list):

        import bluepy
        pre_synaptic_gids = self.circuit.connectome.synapse_properties(
            numpy.array(afferent_synapses_ids_list),
            [bluepy.enums.Synapse.PRE_GID])[bluepy.enums.Synapse.PRE_GID].values.tolist()
        return self.circuit.cells.get(pre_synaptic_gids)['mtype'].values.tolist()

    ################################################################################################
    # @get_post_synaptic_mtypes
    ################################################################################################
    def get_post_synaptic_mtypes(self,
                                 efferent_synapses_ids_list):

        import bluepy
        post_synaptic_gids = self.circuit.connectome.synapse_properties(
            numpy.array(efferent_synapses_ids_list),
            [bluepy.enums.Synapse.POST_GID])[bluepy.enums.Synapse.POST_GID].values.tolist()
        return self.circuit.cells.get(post_synaptic_gids)['mtype'].values.tolist()

    ################################################################################################
    # @get_pre_synaptic_etypes
    ################################################################################################
    def get_pre_synaptic_etypes(self,
                                afferent_synapses_ids_list):

        import bluepy
        pre_synaptic_gids = self.circuit.connectome.synapse_properties(
            numpy.array(afferent_synapses_ids_list),
            [bluepy.enums.Synapse.PRE_GID])[bluepy.enums.Synapse.PRE_GID].values.tolist()
        return self.circuit.cells.get(pre_synaptic_gids)['etype'].values.tolist()

    ################################################################################################
    # @get_post_synaptic_etypes
    ################################################################################################
    def get_post_synaptic_etypes(self,
                                 efferent_synapses_ids_list):

        import bluepy
        post_synaptic_gids = self.circuit.connectome.synapse_properties(
            numpy.array(efferent_synapses_ids_list),
            [bluepy.enums.Synapse.POST_GID])[bluepy.enums.Synapse.POST_GID].values.tolist()
        return self.circuit.cells.get(post_synaptic_gids)['etype'].values.tolist()

    ################################################################################################
    # @is_synapse_excitatory
    ################################################################################################
    def is_synapse_excitatory(self,
                              synapse_type_id):

        return True if synapse_type_id > 100 else False

    ################################################################################################
    # @is_synapse_inhibitory
    ################################################################################################
    def is_synapse_inhibitory(self,
                              synapse_id):

        # TODO: Verify the latest types and their IDs and if there is a more robust way to do it
        return True if synapse_id < 100 else False

    def is_axo_somatic_synapse(self,
                               synapse_id):

        import bluepy
        value = self.circuit.connectome.synapse_properties(
            numpy.array([synapse_id]), [bluepy.enums.Synapse.POST_BRANCH_TYPE]).values.tolist()[0]
        print(value)
        if value == 1:
            return True
        else:
            return False

    ################################################################################################
    # @get_excitatory_synapses_ids
    ################################################################################################
    def get_excitatory_synapses_ids(self,
                                    gid):

        # Get the IDs of all the synapses on the neuron
        synapse_ids_list = self.get_all_synapses_ids(gid=gid)

        # Get the IDs of the types of the synapses
        synapse_types_ids = self.get_synapse_types_ids(synapse_ids_list=synapse_ids_list)

        # A list to collect all the synapse IDs
        excitatory_synapses = list()
        for i, synapse_type_id in enumerate(synapse_types_ids):
            if self.is_synapse_excitatory(synapse_type_id=synapse_type_id):
                excitatory_synapses.append(synapse_ids_list[i])
        return excitatory_synapses

    ################################################################################################
    # @get_inhibitory_synapses_ids
    ################################################################################################
    def get_inhibitory_synapses_ids(self,
                                    gid):

        # Get the IDs of all the synapses on the neuron
        synapse_ids_list = self.get_all_synapses_ids(gid=gid)

        # Get the IDs of the types of the synapses
        synapse_types_ids = self.get_synapse_types_ids(
            synapse_ids_list=synapse_ids_list)

        # A list to collect all the synapse IDs
        inhibitory_synapses = list()
        for i, synapse_type_id in enumerate(synapse_types_ids):
            if not self.is_synapse_excitatory(synapse_type_id=synapse_type_id):
                inhibitory_synapses.append(synapse_ids_list[i])
        return inhibitory_synapses

    ################################################################################################
    # @get_excitatory_synapses_ids
    ################################################################################################
    def get_excitatory_and_inhibitory_synapses_ids(self,
                                                   gid):

        # Get the IDs of all the synapses on the neuron
        synapse_ids_list = self.get_all_synapses_ids(gid=gid)

        # Get the IDs of the types of the synapses
        synapse_types_ids = self.get_synapse_types_ids(synapse_ids_list=synapse_ids_list)

        # A list to collect all the synapse IDs
        excitatory_synapses = list()
        inhibitory_synapses = list()
        for synapse_type_id in synapse_types_ids:
            if self.is_synapse_excitatory(synapse_type_id=synapse_type_id):
                excitatory_synapses.append(synapse_type_id)
            else:
                inhibitory_synapses.append(synapse_type_id)
        return excitatory_synapses, inhibitory_synapses

    ################################################################################################
    # @get_shared_synapses_ids_between_two_neurons
    ################################################################################################
    def get_shared_synapses_ids_between_two_neurons(self,
                                                    pre_gid,
                                                    post_gid):

        import bluepy

        # Get the afferent synapses of the post-synaptic neuron
        post_afferent_synapses_ids = self.get_afferent_synapses_ids(gid=post_gid)

        # Get a corresponding list of GIDs that represent the pre-synaptic neurons
        pre_gids = self.circuit.connectome.synapse_properties(
            post_afferent_synapses_ids, [bluepy.enums.Synapse.PRE_GID]).values

        # Determine the synapses that only connect with the pre_gid neuron
        shared_synapses_ids = list()
        for i in range(len(pre_gids)):
            if int(pre_gid) == int(pre_gids[i]):
                shared_synapses_ids.append(post_afferent_synapses_ids[i])

        # Return the resulting list
        return shared_synapses_ids
