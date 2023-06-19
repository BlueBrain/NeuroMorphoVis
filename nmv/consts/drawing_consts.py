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


####################################################################################################
# @Color
####################################################################################################
class Drawing:
    """Drawing constants, to draw the particle simulations"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Blend only
    BLEND = 0

    # Multiply blend
    MULTIPLY_BLEND = 1

    # Add and blend
    ADDITIVE_BLEND = 2

    # The width of the edge in a particle system
    LINE_WIDTH = 1

    # The radius of a particle
    PARTICLE_SIZE = 3
