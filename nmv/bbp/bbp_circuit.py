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
from mathutils import Vector

# Internal imports
import nmv.utilities
from .circuit import Circuit


class BBPCircuit(Circuit):

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self, circuit_config):

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
    # @get_afferent_synapses_ids
    ################################################################################################
    def get_afferent_synapses_ids(self,
                                  gid):
        return self.circuit.connectome.afferent_synapses(int(gid)).tolist()

    ################################################################################################
    # @get_efferent_synapses_ids
    ################################################################################################
    def get_efferent_synapses_ids(self,
                                  gid):
        return self.circuit.connectome.efferent_synapses(int(gid)).tolist()

    ################################################################################################
    # @get_all_synapses_ids
    ################################################################################################
    def get_all_synapses_ids(self,
                             gid):
        synapses_ids_list = self.get_afferent_synapses_ids(gid=gid)
        synapses_ids_list.extend(self.get_efferent_synapses_ids(gid=gid))
        return synapses_ids_list

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




