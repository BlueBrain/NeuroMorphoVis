####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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

# Blender imports
from mathutils import Vector


####################################################################################################
# @Color
####################################################################################################
class Color:
    """Color constants"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Red
    RED = Vector((1.0, 0.0, 0.0))

    # Green
    GREEN = Vector((0.0, 1.0, 0.0))

    # Blue
    BLUE = Vector((0.0, 0.0, 1.0))

    # Light red
    LIGHT_RED = Vector((1.0, 0.338, 0.253))

    # Sky blue
    SKY_BLUE = Vector((0.167, 0.521, 1.0))

    # White
    WHITE = Vector((1.0, 1.0, 1.0))

    # Very white, used to solve a bug in Blender 2.8
    VERY_WHITE = Vector((10.0, 10.0, 10.0))

    # Gray
    GRAY = Vector((0.5, 0.5, 0.5))

    # Greysh (a lighter gradient from gray)
    GREYSH = Vector((0.9, 0.9, 0.9))

    # Matt black
    MATT_BLACK = Vector((0.1, 0.1, 0.1))

    # Black
    BLACK = Vector((0.0, 0.0, 0.0))

    # Default number of materials
    NUMBER_MATERIALS = 2

    # The number of color elements in the color map
    COLORMAP_RESOLUTION = 16
