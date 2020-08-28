####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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
def _zip_endfeet_data(endfeet_ids, endfeetome):
    """Returns a generator of the endfeet data per endfoot
    
    :param endfeet_ids:
        THe IDs of the end-feet.
    :param endfeetome: 
        End-feet data.
    :return:
        End-feet data zipped in a specific structure.
    """

    endfeet_areas = endfeetome.areas
    endfeet_targets = endfeetome.targets.endfoot_surface_coordinates

    for i, endfoot_id in enumerate(endfeet_ids):
        yield endfeet_areas[endfoot_id], endfeet_targets[endfoot_id]


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
    """
    This is a slow object oriented way to access the circuit data from the point of view of
    the astrocytes.

    Args:
        astrocyte_ids (iterable)
        circuit_directory (string): absolute path to circuit directory (parent of build/ directory)

    Returns:
        A generator of AstrocyteData objects that correspond to astrocyte_ids.
    """

    # NGV circuit
    ngv_circuit = NGVCircuit(circuit_directory)

    # Configuration
    cfg = ngv_circuit.config

    # The astrocyte bodies
    astrocytes = ngv_circuit.data.astrocytes

    # The end-feet
    endfeetome = ngv_circuit.data.endfeetome

    # The connectivity
    gv_conn = ngv_circuit.connectome.gliovascular

    # For each astrocyte, generate the astrocyte data w/o destroying the local variables
    for astrocyte_id in astrocyte_ids:

        # Astrocyte name
        name = astrocytes.astrocyte_names[astrocyte_id].decode('utf-8')

        # Astrocyte morphology full path
        file_path = os.path.join(cfg.morphology_directory, name + '.h5')

        # Construct the circuit data
        circuit_data = _circuit_data(astrocytes.astrocyte_point_data[astrocyte_id])

        # Get a list of all the end-feet
        endfeet_data = list(
            _zip_endfeet_data(gv_conn.astrocyte.to_endfoot(astrocyte_id), endfeetome))

        # Generate the astrocyte data
        yield AstrocyteData(file_path, circuit_data, endfeet_data)