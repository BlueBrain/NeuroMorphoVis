####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

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
    SOMA = Vector((0.05, 0.5, 0.75))

    # Basal dendrites color
    BASAL_DENDRITES = Vector((0.9, 0.5, 0.75))

    # Apical dendrites color
    APICAL_DENDRITES = Vector((0.0, 0.9, 0.75))

    # Axons color
    AXONS = Vector((0.0, 0.0, 1.0))

    # Articulations (connections between sections) color
    ARTICULATION = Vector((1.0, 1.0, 0.0))

    # Spines color
    SPINES = Vector((0.1, 0.75, 0.45))

    # Nuclei color
    NUCLEI = Vector((0.75, 0.41, 0.77))
