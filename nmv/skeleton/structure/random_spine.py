####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# Blender Imports
from mathutils import Vector


####################################################################################################
# RandomSpine
####################################################################################################
class RandomSpine:
    """A random morphological spine that is generated to create a neuron mesh without a circuit.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Spine location
        self.location = Vector((0.0, 0.0, 0.0))

        # Spine normal
        self.normal = Vector((0.0, 1.0, 0.0))

        # The radius of the segment where the spine is emanating
        # NOTE: This must be updated during the building process
        self.segment_radius = None
