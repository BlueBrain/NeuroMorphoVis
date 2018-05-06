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
# @parse_color_from_argument
####################################################################################################
def parse_color_from_argument(color_argument):
    """
    Gets the RGB values from the color arguments. This function is compatible with an RGB color
    format with 0-255 or 0.0-0.1 representations.

    :param color_argument: A given color argument.
    :return: A vector having RGB color components.
    """

    # Split the string
    rgb_values = color_argument.split('_')

    # Get the RGB values
    r = float(rgb_values[0])
    g = float(rgb_values[1])
    b = float(rgb_values[2])

    # Verify the values whether in 0-255 range or in 0.0-1.0 range
    if r > 255:
        r = 255

    if r < 0:
        r = 0

    if g > 255:
        g = 255

    if g < 0:
        g = 0

    if b > 255:
        b = 255

    if b < 0:
        b = 0

    # RGB colors (normalized)
    if r > 1.0:
        r /= 256.0

    if g > 1.0:
        g /= 256.0

    if b > 1.0:
        b /= 256.0

    # Build the RGB color vector
    rgb_color = Vector((r, g, b))

    # Return the RGB color
    return rgb_color
