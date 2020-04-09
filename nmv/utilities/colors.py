####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
# @rgb_vector_to_hex
####################################################################################################
def rgb_vector_to_hex(rgb):
    """Converts an rgb color to a hex color.

    :param rgb:
        A given rgb color.
    :return:
        The hex code for a hed color
    """

    # Return the HEX code of the color
    return '#%02x%02x%02x' % (int(rgb[0] * 255),
                              int(rgb[1] * 255),
                              int(rgb[2] * 255))


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
