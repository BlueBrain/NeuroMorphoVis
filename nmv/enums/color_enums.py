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
    """Color enumerators"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # COLORS #######################################################################################
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

    # Endfeet colors
    ENDFEET = Vector((0.5, 1.0, 0.1))

    # Spines color
    SPINES = Vector((0.1, 0.75, 0.45))

    # Synapses color
    SYNAPSES = Vector((0.1, 0.75, 0.45))

    # Excitatory synapses color
    EXCITATORY_SYNAPSES = Vector((1.0, 0.0, 0.0))

    # Inhibitory synapses color
    INHIBITORY_SYNAPSES = Vector((0.0, 0.0, 1.0))

    # Afferent synapses color
    AFFERENT_SYNAPSES = Vector((1.0, 1.0, 0.0))

    # Efferent synapses color
    EFFERENT_SYNAPSES = Vector((1.0, 0.0, 1.0))

    # Nuclei color
    NUCLEI = Vector((0.75, 0.41, 0.77))

    # MATERIALS INDICES ############################################################################
    # The soma materials are found at the indices 0 and 1
    SOMA_MATERIAL_START_INDEX = 0

    # The apical dendrites materials are found at the indices 2 and 3
    APICAL_DENDRITE_MATERIAL_START_INDEX = 2

    # The basal dendrites materials are found at the indices 4 and 5
    BASAL_DENDRITES_MATERIAL_START_INDEX = 4

    # The axon materials are found at the indices 6 and 7
    AXON_MATERIAL_START_INDEX = 6

    # The gray (shaded or non-highlighted) materials are found at the indices 8 and 9
    GRAY_MATERIAL_START_INDEX = 8

    # The articulation materials are found at the indices 10 and 11
    ARTICULATION_MATERIAL_START_INDEX = 10

    # The endfeet materials are found at the indices 12 and 13
    ENDFEET_MATERIAL_START_INDEX = 12



