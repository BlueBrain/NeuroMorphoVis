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
import random

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.utilities


####################################################################################################
# @get_circuit_mtype_strings_list
####################################################################################################
def get_all_mtypes_in_circuit(circuit_config):

    circuit = nmv.bbp.BBPCircuit(circuit_config=circuit_config)
    return circuit.get_mtype_strings_list()


####################################################################################################
# @get_all_etypes_in_circuit
####################################################################################################
def get_all_etypes_in_circuit(circuit_config):

    circuit = nmv.bbp.BBPCircuit(circuit_config=circuit_config)
    return circuit.get_etype_strings_list()


####################################################################################################
# @get_circuit_mtype_strings_set
####################################################################################################
def get_circuit_mtype_strings_set(circuit):
    """Returns a set of all the morphological types of the neurons in a given circuit.

    :param circuit:
        A BBP circuit.
    :return:
        A set of all the morphological types of the neurons in a given circuit.
    """

    return sorted(circuit.cells.mtypes)


####################################################################################################
# @get_circuit_mtype_strings_list
####################################################################################################
def get_circuit_mtype_strings_list(circuit):
    """Returns a linear list of all the morphological types of the neurons in a given circuit.

    :param circuit:
        A BBP circuit.
    :return:
        A dictionary of all the morphological types of the neurons in a given circuit.
    """

    return list(get_circuit_mtype_strings_set(circuit=circuit))


####################################################################################################
# @get_circuit_etype_strings_set
####################################################################################################
def get_circuit_etype_strings_set(circuit):
    """Returns a set of all the electrical types of the neurons in a given circuit.

    :param circuit:
        A BBP circuit.
    :return:
        A set of all the electrical types of the neurons in a given circuit.
    """

    return sorted(circuit.cells.etypes)


####################################################################################################
# @get_circuit_etype_strings_list
####################################################################################################
def get_circuit_etype_strings_list(circuit):
    """Returns a linear list of all the electrical types of the neurons in a given circuit.

    :param circuit:
        A BBP circuit.
    :return:
        A linear list of all the electrical types of the neurons in a given circuit.
    """

    return list(get_circuit_etype_strings_set(circuit=circuit))


####################################################################################################
# @create_random_color_coded_mtype_dict
####################################################################################################
def create_random_color_coded_mtype_dict(circuit):
    """

    :param circuit:
    :type circuit:
    :return:
    :rtype:
    """

    # Get all the mtypes in the circuit
    mtypes_strings_list = get_circuit_mtype_strings_list(circuit=circuit)

    # Construct a color coded dictionary, dict = {mtype: color}
    color_coded_mtype_dict = {}
    for i in range(len(mtypes_strings_list)):
        r = random.uniform(0.0, 1.0)
        g = random.uniform(0.0, 1.0)
        b = random.uniform(0.0, 1.0)
        hex_color = nmv.utilities.rgb_vector_to_hex(rgb=Vector((r, g, b)))
        color_coded_mtype_dict[mtypes_strings_list[i]] = hex_color

    return color_coded_mtype_dict


####################################################################################################
# @create_random_color_coded_etype_dict
####################################################################################################
def create_random_color_coded_etype_dict(circuit):
    """

    :param circuit:
    :type circuit:
    :return:
    """

    # Get all the mtypes in the circuit
    mtypes_strings_list = get_circuit_etype_strings_list(circuit=circuit)

    # Construct a color coded dictionary, dict = {mtype: color}
    color_coded_mtype_dict = {}
    for i in range(len(mtypes_strings_list)):
        r = random.uniform(0.0, 1.0)
        g = random.uniform(0.0, 1.0)
        b = random.uniform(0.0, 1.0)
        hex_color = nmv.utilities.rgb_vector_to_hex(rgb=Vector((r, g, b)))
        color_coded_mtype_dict[mtypes_strings_list[i]] = hex_color

    return color_coded_mtype_dict

