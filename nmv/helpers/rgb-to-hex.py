#!/usr/bin/python

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

# System imports
import sys


####################################################################################################
# @rgb_to_hex
####################################################################################################
def rgb_to_hex(rgb):
    """Converts an rgb color to a hex color.

    :param rgb:
        A given rgb color.
    :return:
        The hex code for a hed color
    """

    # Return the HEX code of the color
    return '#%02x%02x%02x' % rgb


####################################################################################################
# __main__
####################################################################################################
if __name__ == "__main__":

    # Get the colors
    args = sys.argv
    args = args.split(',')

    r = float(args[1])
    g = float(args[2])
    b = float(args[3])

    # Verify the range and update
    if r > 255:
        r = 255
    if r < 0:
        r = 0
    if 1.0 > r > 0.0:
        r = r * 256

    if g > 255:
        g = 255
    if g < 0:
        g = 0
    if 1.0 > g > 0.0:
        g = g * 256

    if b > 255:
        b = 255
    if b < 0:
        r = 0
    if 1.0 > b > 0.0:
        b = b * 256

    # Get the final color values
    r = int(r)
    g = int(g)
    b = int(b)

    # Print the HEX value
    print(rgb_to_hex((r, g, b)))
