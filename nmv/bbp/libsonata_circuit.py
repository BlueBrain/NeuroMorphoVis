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

# System imports
import numpy

# Blender imports
from mathutils import Vector, Matrix

# Internal imports
import nmv.utilities
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

        # TODO: Implement this class