####################################################################################################
# Copyright (c) 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
# @Circuit
####################################################################################################
class Circuit:
    """Base class for the Circuit."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 circuit_config):
        """Constructor

        :param circuit_config:
            Circuit configuration file.
        """

        # Configuration file
        self.circuit_config = circuit_config

        # This circuit must be loaded before being used later to access its contents
        self.nmv_circuit = None

