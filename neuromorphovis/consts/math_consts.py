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
# Math
####################################################################################################
class Math:
    """Math constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Infinity
    INFINITY = 1e30

    # Epsilon
    EPSILON = 0.99

    # Little Epsilon
    LITTLE_EPSILON = 1e-5

    # Origin
    ORIGIN = Vector((0.0, 0.0, 0.0))

    # X-axis
    X_AXIS = Vector((1.0, 0.0, 0.0))

    # Y-axis
    Y_AXIS = Vector((0.0, 1.0, 0.0))

    # Z-axis
    Z_AXIS = Vector((.0, 0.0, 1.0))
