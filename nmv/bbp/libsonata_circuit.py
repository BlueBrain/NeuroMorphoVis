####################################################################################################
# Copyright (c) 2023, EPFL / Blue Brain Project
# Author(s): Nadir Roman <nadir.roman@epfl.ch>
#            Adrien Fleury <adrien.fleury@epfl.ch>
#            Marwan Abdellah <marwan.abdellah@epfl.ch>
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
from pathlib import Path

# Blender imports
from mathutils import Vector, Quaternion

# Internal imports
from .circuit import Circuit


####################################################################################################
# @libSonataCircuit
####################################################################################################
class libSonataCircuit(Circuit):
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
    # @get_number_cells_in_population
    ################################################################################################   
    def get_number_cells_in_population(self,
                                       population):
        nodes = self.circuit.node_population(population)
        return nodes.size
    
    ################################################################################################
    # @get_number_cells_in_population
    ################################################################################################ 
    def get_morphio_morphology(self, gid, population):
        """
        Get the morphology of a neuron in MorphIO format.
        :param gid: The global ID of the neuron.
        :param population: The population to which the neuron belongs.
        :return: A MorphIO morphology object.
        """
        from morphio import Morphology, Collection
        import os 
        
        # Let's contruct a file path for the morphology and try to load it 
        folder, morphology, type = self.get_neuron_morphology_attributes(gid=gid, population=population)
        morpholoyg_file_path = f"{folder}/{morphology}.{type}"
        if os.path.exists(morpholoyg_file_path):
            return Morphology(morpholoyg_file_path)
        else:
            # Use a collection to read the morphology from the circuit    
            collection = Collection(folder)
            return collection.load(morphology)
        
    ################################################################################################
    # @get_neuron_morphology_attributes
    ################################################################################################ 
    def get_neuron_morphology_attributes(self,
                                         gid,
                                         population):
        folder = None
        type = None

        properties = self.circuit.node_population_properties(population)
        if properties.morphologies_dir and Path(properties.morphologies_dir).exists():
            folder = properties.morphologies_dir
            type = "swc"
        else:
            types_extension = {
                "neurolucida-asc": "asc",
                "h5v1": "h5",
            }
            for type_name, path in properties.alternate_morphology_formats.items():
                if Path(path).exists():
                    folder = path
                    type = types_extension[type_name]
                    break

        if folder is None or type is None:
            raise Exception(
                "Could not determine morphology folder and/or extension")

        nodes = self.circuit.node_population(population)
        morphology = nodes.get_attribute("morphology", gid)
        return (folder, morphology, type)
        
    ################################################################################################
    # @get_neuron_morphology_path
    ################################################################################################
    def get_neuron_morphology_path(self,
                                   gid,
                                   population):
        folder = None
        type = None
        type, folder, morphology = self.get_neuron_morphology_attributes(
            gid=gid, population=population)
        return f"{folder}/{morphology}.{type}"

    ################################################################################################
    # @load_circuit
    ################################################################################################
    def load_circuit(self):
        import libsonata
        try:
            return libsonata.CircuitConfig.from_file(self.circuit_config)
        except:
            try:
                sim_config = libsonata.SimulationConfig.from_file(
                    self.circuit_config)
                return libsonata.CircuitConfig.from_file(sim_config.network)
            except:
                pass

        raise Exception(
            f"Cannot parse SONATA configuration {self.circuit_config}")

    ################################################################################################
    # @get_number_cells_in_population
    ################################################################################################
    def get_number_cells_in_population(self, population):
         return self.circuit.node_population(population).size

    ################################################################################################
    # @get_mtype_strings_set
    ################################################################################################
    def get_mtype_strings_set(self,
                              population):
        nodes = self.circuit.node_population(population)
        m_types = nodes.get_attribute("mtype", nodes.select_all())
        return sorted(set(m_types))
    
    ################################################################################################
    # @get_mtype_strings_set
    ################################################################################################
    def get_morphologies(self,
                         population):
        nodes = self.circuit.node_population(population)
        return nodes.get_attribute("morphology", nodes.select_all())
    
    ################################################################################################
    # @get_morphology
    ################################################################################################
    def get_morphology(self,
                       gid,
                       population):
        nodes = self.circuit.node_population(population)
        return nodes.get_attribute("morphology", gid)
        
    ################################################################################################
    # @get_layers
    ################################################################################################
    def get_layers(self, population):
        """
        Get the layers of the circuit for a given population.
        :param population: The population to get the layers for.
        :return: A list of layers.
        """
        nodes = self.circuit.node_population(population)
        layers = nodes.get_attribute("layer", nodes.select_all())
        return layers

    ################################################################################################
    # @get_circuit_mtype_strings_list
    ################################################################################################
    def get_mtype_strings_list(self,
                               population):
        return list(self.get_mtype_strings_set(population))

    ################################################################################################
    # @get_etype_strings_set
    ################################################################################################
    def get_etype_strings_set(self,
                              population):
        nodes = self.circuit.node_population(population)
        m_types = nodes.get_attribute("etype", nodes.select_all())
        return sorted(set(m_types))

    ################################################################################################
    # @get_etype_strings_list
    ################################################################################################
    def get_etype_strings_list(self,
                               population):
        return list(self.get_etype_strings_set(population))
    
    ################################################################################################
    # @get_translations
    ################################################################################################
    def get_translations(self,
                         population):
        """
        Get the translations of the nodes in a given population.
        :param population: The population to get the translations for.
        :return: A list of translations as Vector objects.
        """
        nodes = self.circuit.node_population(population)
        xs = nodes.get_attribute("x", nodes.select_all())
        ys = nodes.get_attribute("y", nodes.select_all())
        zs = nodes.get_attribute("z", nodes.select_all())
        return [Vector((x, y, z)) for x, y, z in zip(xs, ys, zs)]
    
    ################################################################################################
    # @get_orientations
    ################################################################################################
    def get_orientations(self,
                         population):
        """
        Get the orientations of the nodes in a given population.
        :param population: The population to get the orientations for.
        :return: A list of orientations as Quaternion objects.
        """
        nodes = self.circuit.node_population(population)
        qx = nodes.get_attribute("orientation_x", nodes.select_all())
        qy = nodes.get_attribute("orientation_y", nodes.select_all())
        qz = nodes.get_attribute("orientation_z", nodes.select_all())
        qw = nodes.get_attribute("orientation_w", nodes.select_all())
        return [Quaternion((qw[i], qx[i], qy[i], qz[i])).normalized() for i in range(len(qx))]
    
    ################################################################################################
    # @get_transformations
    ################################################################################################
    def get_transformations(self,
                            population):
        """
        Get the transformation matrices of the nodes in a given population.
        :param population: The population to get the transformations for.
        :return: A list of transformation matrices as 4x4 Matrix objects.
        """
        translations = self.get_translations(population)
        orientations = self.get_orientations(population)

        transformations = []
        for i in range(len(translations)):
            matrix = orientations[i].to_matrix().to_4x4()
            matrix[0][3] = translations[i][0]
            matrix[1][3] = translations[i][1]
            matrix[2][3] = translations[i][2]
            transformations.append(matrix)
        
        return transformations

    ################################################################################################
    # @get_neuron_translation_vector
    ################################################################################################
    def get_neuron_translation_vector(self,
                                      gid,
                                      population):
        nodes = self.circuit.node_population(population)
        x = nodes.get_attribute("x", gid)
        y = nodes.get_attribute("y", gid)
        z = nodes.get_attribute("z", gid)
        return Vector((x, y, z))

    ################################################################################################
    # @get_neuron_orientation_matrix
    ################################################################################################
    def get_neuron_orientation_matrix(self,
                                      gid,
                                      population):
        nodes = self.circuit.node_population(population)
        qx = nodes.get_attribute("orientation_x", gid)
        qy = nodes.get_attribute("orientation_y", gid)
        qz = nodes.get_attribute("orientation_z", gid)
        qw = nodes.get_attribute("orientation_w", gid)
        q = Quaternion((qw, qx, qy, qz)).normalized()
        return q.to_matrix()

    ################################################################################################
    # @get_neuron_transformation_matrix
    ################################################################################################
    def get_neuron_transformation_matrix(self,
                                         gid,
                                         population):
        # Translation
        translation_vector = self.get_neuron_translation_vector(
            gid=gid, population=population)

        # Get the orientation and update the translation elements in the orientation matrix
        matrix = self.get_neuron_orientation_matrix(gid=gid, population=population)
        matrix = matrix.to_4x4()  # Convert to a 4x4 matrix
        
        # Set the translation vector in the last column of the matrix
        matrix[0][3] = translation_vector[0]
        matrix[1][3] = translation_vector[1]
        matrix[2][3] = translation_vector[2]

        return matrix

    ################################################################################################
    # @get_neuron_inverse_transformation_matrix
    ################################################################################################
    def get_neuron_inverse_transformation_matrix(self,
                                                 gid,
                                                 population):
        return self.get_neuron_transformation_matrix(gid=gid, population=population).inverted()

    ################################################################################################
    # @get_afferent_synapses_ids
    ################################################################################################
    def get_afferent_synapses_ids(self,
                                  gid,
                                  edge_population):
        edges = self.circuit.edge_population(edge_population)
        return edges.afferent_edges(gid).flatten()

    ################################################################################################
    # @get_efferent_synapses_ids
    ################################################################################################
    def get_efferent_synapses_ids(self,
                                  gid,
                                  edge_population):
        edges = self.circuit.edge_population(edge_population)
        return edges.efferent_edges(gid).flatten()

    ################################################################################################
    # @get_all_synapses_ids
    ################################################################################################
    def get_all_synapses_ids(self,
                             gid,
                             edge_population):

        synapses_ids_list = self.get_afferent_synapses_ids(
            gid=gid, edge_population=edge_population)
        synapses_ids_list.extend(self.get_efferent_synapses_ids(
            gid=gid, edge_population=edge_population))
        return synapses_ids_list

    ################################################################################################
    # @get_synapse_types_ids
    ################################################################################################
    def get_synapse_types_ids(self,
                              synapse_ids_list,
                              edge_population):
        import libsonata
        edges = self.circuit.edge_population(edge_population)
        return edges.get_attribute("syn_type_id", libsonata.Selection(synapse_ids_list))

    ################################################################################################
    # @get_pre_synaptic_synapse_positions
    ################################################################################################
    def get_pre_synaptic_synapse_positions(self,
                                           edge_population,
                                           synapse_ids_list,
                                           synapse_location='center'):

        # synapse_location could be 'contour' or 'center'
        import libsonata

        edges = self.circuit.edge_population(edge_population)
        selection = libsonata.Selection(synapse_ids_list)

        attribute = "center" if synapse_location == "center" else "surface"
        xs = edges.get_attribute(f"afferent_{attribute}_x", selection)
        ys = edges.get_attribute(f"afferent_{attribute}_y", selection)
        zs = edges.get_attribute(f"afferent_{attribute}_z", selection)
        return [[x, y, z] for x, y, z in zip(xs, ys, zs)]

    ################################################################################################
    # @get_post_synaptic_synapse_positions
    ################################################################################################
    def get_post_synaptic_synapse_positions(self,
                                            edge_population,
                                            synapse_ids_list,
                                            synapse_location='center'):

        # synapse_location could be 'contour' or 'center'
        import libsonata

        edges = self.circuit.edge_population(edge_population)
        selection = libsonata.Selection(synapse_ids_list)

        attribute = "center" if synapse_location == "center" else "surface"
        xs = edges.get_attribute(f"efferent_{attribute}_x", selection)
        ys = edges.get_attribute(f"efferent_{attribute}_y", selection)
        zs = edges.get_attribute(f"efferent_{attribute}_z", selection)
        return [[x, y, z] for x, y, z in zip(xs, ys, zs)]

    ################################################################################################
    # @get_pre_synaptic_mtypes
    ################################################################################################
    def get_pre_synaptic_mtypes(self,
                                edge_population,
                                afferent_synapses_ids_list):

        import libsonata

        edges = self.circuit.edge_population(edge_population)
        selection = libsonata.Selection(afferent_synapses_ids_list)
        nodes = self.circuit.edge_population(edges.source)
        src_nodes = edges.source_nodes(selection)

        return nodes.get_attribute("mtype", libsonata.Selection(src_nodes))

    ################################################################################################
    # @get_post_synaptic_mtypes
    ################################################################################################
    def get_post_synaptic_mtypes(self,
                                 edge_population,
                                 efferent_synapses_ids_list):

        import libsonata

        edges = self.circuit.edge_population(edge_population)
        selection = libsonata.Selection(efferent_synapses_ids_list)
        nodes = self.circuit.edge_population(edges.target)
        target_nodes = edges.target_nodes(selection)

        return nodes.get_attribute("mtype", libsonata.Selection(target_nodes))

    ################################################################################################
    # @get_pre_synaptic_etypes
    ################################################################################################
    def get_pre_synaptic_etypes(self,
                                edge_population,
                                afferent_synapses_ids_list):

        import libsonata

        edges = self.circuit.edge_population(edge_population)
        selection = libsonata.Selection(afferent_synapses_ids_list)
        nodes = self.circuit.edge_population(edges.source)
        src_nodes = edges.source_nodes(selection)

        return nodes.get_attribute("etype", libsonata.Selection(src_nodes))

    ################################################################################################
    # @get_post_synaptic_etypes
    ################################################################################################
    def get_post_synaptic_etypes(self,
                                 edge_population,
                                 efferent_synapses_ids_list):

        import libsonata

        edges = self.circuit.edge_population(edge_population)
        selection = libsonata.Selection(efferent_synapses_ids_list)
        nodes = self.circuit.edge_population(edges.target)
        target_nodes = edges.target_nodes(selection)

        return nodes.get_attribute("etype", libsonata.Selection(target_nodes))

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

    ################################################################################################
    # @get_excitatory_synapses_ids
    ################################################################################################
    def get_excitatory_synapses_ids(self,
                                    gid,
                                    edge_population):

        # Get the IDs of all the synapses on the neuron
        synapse_ids_list = self.get_all_synapses_ids(
            gid=gid, edge_population=edge_population)

        # Get the IDs of the types of the synapses
        synapse_types_ids = self.get_synapse_types_ids(
            synapse_ids_list=synapse_ids_list, edge_population=edge_population)

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
                                    gid,
                                    edge_population):

        # Get the IDs of all the synapses on the neuron
        synapse_ids_list = self.get_all_synapses_ids(
            gid=gid, edge_population=edge_population)

        # Get the IDs of the types of the synapses
        synapse_types_ids = self.get_synapse_types_ids(
            synapse_ids_list=synapse_ids_list, edge_population=edge_population)

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
                                                   gid,
                                                   edge_population):

        # Get the IDs of all the synapses on the neuron
        synapse_ids_list = self.get_all_synapses_ids(
            gid=gid, edge_population=edge_population)

        # Get the IDs of the types of the synapses
        synapse_types_ids = self.get_synapse_types_ids(
            synapse_ids_list=synapse_ids_list, edge_population=edge_population)

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
                                                    post_gid,
                                                    edge_population):

        import libsonata

        # Get the afferent synapses of the post-synaptic neuron
        post_afferent_synapses_ids = self.get_afferent_synapses_ids(
            gid=post_gid, edge_population=edge_population)

        # Get a corresponding list of GIDs that represent the pre-synaptic neurons
        edges = self.circuit.edge_population(edge_population)
        pre_gids = edges.source_nodes(
            libsonata.Selection(post_afferent_synapses_ids))

        # Determine the synapses that only connect with the pre_gid neuron
        shared_synapses_ids = list()
        for i in range(len(pre_gids)):
            if int(pre_gid) == int(pre_gids[i]):
                shared_synapses_ids.append(post_afferent_synapses_ids[i])
