####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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


####################################################################################################
# @Input
####################################################################################################
class Input:
    """Input enumerators
    """

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    # Load a single .H5 or .SWC file
    H5_SWC_FILE = 'INPUT_H5_SWC_FILE'

    # Load an entire directory of .H5 or .SWC files
    H5_SWC_DIRECTORY = 'INPUT_H5_SWC_DIRECTORY'

    # Load a neuron from a given circuit using its GID
    CIRCUIT_GID = 'INPUT_CIRCUIT_GID'

    # Load a full target from a given circuit
    CIRCUIT_TARGET = 'INPUT_TARGET'
