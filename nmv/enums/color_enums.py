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

# Blender imports
from mathutils import Vector


####################################################################################################
# @Colors
####################################################################################################
class Color:
    """Color enumerator
    """

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    # Soma color
    SOMA = Vector((1.0, 0.8, 0.15))

    # Basal dendrites color
    BASAL_DENDRITES = Vector((0.9, 0.1, 0.075))

    # Apical dendrites color
    APICAL_DENDRITES = Vector((0.4, 0.9, 0.2))

    # Axons color
    AXONS = Vector((0.4, 0.7, 1.0))

    # Articulations (connections between sections) color
    ARTICULATION = Vector((1.0, 1.0, 0.0))

    # Spines color
    SPINES = Vector((0.1, 0.75, 0.45))

    # Nuclei color
    NUCLEI = Vector((0.75, 0.41, 0.77))
