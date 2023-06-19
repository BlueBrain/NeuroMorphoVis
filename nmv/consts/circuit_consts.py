####################################################################################################
# Copyright (c) 2016 _ 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender_based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################


####################################################################################################
# @Circuit
####################################################################################################
class Circuit:
    """Circuit constants"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # A list of all the morphological types in the circuit. Initially, this variable is set to None
    # until a circuit is loaded, and then it is filled with the correct values
    MTYPES = None

    # A list of all the electro-physiological types in the circuit. Initially, this variable is set
    # to None until a circuit is loaded, and then it is filled with the correct values
    ETYPES = None
