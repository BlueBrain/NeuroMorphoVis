####################################################################################################
# Copyright (c) 2023, EPFL / Blue Brain Project
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
