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
# Meshing
####################################################################################################
class Meshing:
    """Meshing constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Minimum tessellation level
    MIN_TESSELLATION_LEVEL = 0.1

    # Maximum tessellation level
    MAX_TESSELLATION_LEVEL = 1.0

    # Default sides of a bevel object
    BEVEL_OBJECT_SIDES = 16

    # The percentages of random spines added to the neuron
    RANDOM_SPINES_PERCENTAGE = 50.0

    # PLY extension
    PLY_EXTENSION = '.ply'

    # OBJ extension
    OBJ_EXTENSION = '.obj'

    # STL extension
    STL_EXTENSION = '.stl'

    # BLEND extension
    BLEND_EXTENSION = '.blend'

