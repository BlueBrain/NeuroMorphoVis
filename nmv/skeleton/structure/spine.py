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

# Blender Imports
from mathutils import Vector


####################################################################################################
# Spine
####################################################################################################
class Spine:
    """Morphological Spine.

    The spines are the connections between pre-synaptic and post-synaptic neurons with six
    different shapes.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Pre-synaptic position
        self.pre_synaptic_position = Vector((0.0, 0.0, 0.0))

        # Post-synaptic position
        self.post_synaptic_position = Vector((0.0, 0.0, 0.0))

        # Spine size (initially 1 micron)
        self.size = 1.0

        # The radius of the post-synaptic branch
        self.post_synaptic_radius = 1.0

