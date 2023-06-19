####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
#               Eleftherios Zisis <eleftherios.zisis@epfl.ch>
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
import os
from itertools import starmap
from collections import namedtuple
from cached_property import cached_property
import numpy as np

# BBP imports
import neurom
from archngv import NGVCircuit

# process types
PERIVASCULAR = neurom.AXON
PERISYNAPTIC = neurom.BASAL_DENDRITE

# in the future we will need to add the synapse annotations
PerisynapticProcess = namedtuple('PerisynapticProcess', ['root_section'])
PerivascularProcess = namedtuple('PerivascularProcess', ['root_section',
                                                         'endfoot_area_mesh',
                                                         'endfoot_target'])
EndfootAnnotation = namedtuple('Annotations', ['vessel_segment',
                                               'cell_section',
                                               'cell_segment',
                                               'cell_offset'])
SynapseData = namedtuple('Synapses', ['ids',
                                      'coordinates',
                                      'cell_sections',
                                      'cell_segments',
                                      'cell_offsets'])
MicrodomainData = namedtuple('Microdomain', ['geometry', 'neighbors'])


####################################################################################################
# @_perivascular_process
####################################################################################################
def _perivascular_process(root_section, endfoot_data):
    """ Creates a perivascular process given the root_section from MorphIO
        and the endfoot data that has been generated from the circuit build
    """
    mesh, target = endfoot_data
    return PerivascularProcess(
        root_section=root_section, endfoot_area_mesh=mesh, endfoot_target=target)


####################################################################################################
# @_perisynaptic_process
####################################################################################################
def _perisynaptic_process(root_section):
    """ Creates a perisynaptic process given the root_section from MorphIO"""
    return PerisynapticProcess(root_section)


####################################################################################################
# @AstrocyteData
####################################################################################################
class AstrocyteData:
    def __init__(self, filepath, circuit_data, endfeet_data):
        self.filepath = filepath
        self._endfeet_data = endfeet_data
        self.circuit_data = circuit_data

    @cached_property
    def morphology(self):
        return neurom.load_neuron(self.filepath)

    def _filter_roots(self, neurite_type):
        return filter(lambda s: s.type == neurite_type, self.morphology.neurites)

    @property
    def perivascular_processes(self):
        roots_with_data = zip(self._filter_roots(PERIVASCULAR), self._endfeet_data)
        return list(starmap(_perivascular_process, roots_with_data))

    @property
    def perisynaptic_processes(self):
        return list(map(_perisynaptic_process, self._filter_roots(PERISYNAPTIC)))


####################################################################################################
# @_zip_endfeet_data
####################################################################################################
def _endfeet_data(gv_conn, astrocyte_id):
    """Returns a generator of the endfeet data per endfoot
    :param endfeet_ids:
        THe IDs of the end-feet.
    :param endfeetome:
        End-feet data.
    :return:
        End-feet data zipped in a specific structure.
    """

    endfeet_ids = gv_conn.astrocyte_endfeet(astrocyte_id)

    if endfeet_ids.size == 0:
        return []

    meshes = gv_conn.surface_meshes

    targets = gv_conn.properties(
        endfeet_ids, ['endfoot_surface_x', 'endfoot_surface_y', 'endfoot_surface_z']).to_numpy()

    return [(meshes[endfoot_id], targets[i]) for i, endfoot_id in enumerate(endfeet_ids)]


####################################################################################################
# @_circuit_data
####################################################################################################
def _circuit_data(astrocyte_point_data):
    """Returns circuit related info in a structured array
    :param astrocyte_point_data:
        Astricyte point data.
    """

    # The soma position of the astrocyte as reported in the circuit
    circuit_soma_position = astrocyte_point_data[:3]

    # The radius of the astrocyte as reported in the circuit
    circuit_radius = astrocyte_point_data[3]

    # Specific structure !
    struct_dtype = np.dtype([('soma_radius', 'f4'), ('soma_position', 'f4', (3,))])
    return np.array((circuit_radius, circuit_soma_position), dtype=struct_dtype)


####################################################################################################
# @get_astrocyte_data
####################################################################################################
def get_astrocyte_data(astrocyte_ids, circuit_directory):
    """This is a slow object oriented way to access the circuit data from the point of view of
    the astrocytes.
    Args:
        astrocyte_ids (iterable)
        circuit_directory (string): absolute path to circuit directory (parent of build/ directory)
    Returns:
        A generator of AstrocyteData objects that correspond to astrocyte_ids.
    """

    # NGV circuit
    ngv_circuit = NGVCircuit(circuit_directory)

    # The astrocyte bodies
    astrocytes = ngv_circuit.astrocytes
    astro_data = astrocytes.get(group=astrocyte_ids, properties=['x', 'y', 'z', 'radius']).to_numpy()

    # The connectivity
    gv_connectome = ngv_circuit.gliovascular_connectome

    # For each astrocyte, generate the astrocyte data w/o destroying the local variables
    for i, astrocyte_id in enumerate(astrocyte_ids):

        # Astrocyte morphology full path
        filepath = astrocytes.morph.get_filepath(astrocyte_id)

        # Construct the circuit data
        circuit_data = _circuit_data(astro_data[i])

        # Get a list of all the end-feet
        endfeet_data = _endfeet_data(gv_connectome, astrocyte_id)

        # Generate the astrocyte data
        yield AstrocyteData(filepath, circuit_data, endfeet_data)
