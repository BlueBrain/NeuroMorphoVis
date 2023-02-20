####################################################################################################
# Copyright (c) 2016 - 2021, EPFL / Blue Brain Project
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

# Imports
from mathutils import Vector


####################################################################################################
# @rgb_vector_to_hex
####################################################################################################
def rgb_vector_to_hex(rgb):
    """Converts an RGB color in a mathutils.Vector format to a HEX color.

    :param rgb:
        A given RGB color in a mathutils.Vector format.
    :return:
        The HEX code for the given color.
    """

    # Return the HEX code of the color
    return '#%02x%02x%02x' % (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


####################################################################################################
# @rgb_to_hex
####################################################################################################
def rgb_to_hex(rgb):
    """Converts an RGB color to a HEX color.

    :param rgb:
        A given RGB color string.
    :return:
        The HEX code for the given color string.
    """

    # Return the HEX code of the color
    return '#%02x%02x%02x' % rgb


####################################################################################################
# @hex_to_rgb_tuple
####################################################################################################
def hex_to_rgb_tuple(hex_color):
    """Converts a HEX color code to an RGB color tuple.

    :param hex_color:
        A given HEX color to convert.
    :return:
        The color in RGB format in a tuple.
    """

    h = hex_color.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


####################################################################################################
# @interpolate_list
####################################################################################################
def interpolate_list(input_list,
                     fi):
    """Interpolates a list for generating a linear colormap.

    :param input_list:
        An input list of colors.
    :param fi:
        Fractional
    :return:
        Interpolated value.
    """
    # Split floating-point index into whole & fractional parts
    i, f = int(fi // 1), fi % 1

    # Avoid index error
    j = i + 1 if f > 0 else i

    # Return the value
    return (1 - f) * input_list[i] + f * input_list[j]


####################################################################################################
# @hex_to_rgb
####################################################################################################
def hex_to_rgb(hex_color):
    """Converts a hex color to an RGB tuple (as a mathutils.Vector)

    :param hex_color:
        A given hex color.
    :return:
        The RGB tuple (as a mathutils.Vector)
    """

    # Create an RGB tuple with 256
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    # Return the Vector for mathutils compatibility
    return Vector((rgb[0] / 256.0, rgb[1] / 256.0, rgb[2] / 256.0))


####################################################################################################
# @confirm_rgb_color
####################################################################################################
def confirm_rgb_color(color_string):
    """Ensures that the given color string is an RGB float vector.

    :param color_string:
        A given color string in any format.
    :return:
        An RGB color vector with a float precision.
    """

    # This is a hex color
    if '#' in color_string:
        return hex_to_rgb(hex_color=color_string.replace('#', ''))

    if '_' in color_string:
        rgb_list = color_string.split('_')
        r = int(rgb_list[0])
        g = int(rgb_list[1])
        b = int(rgb_list[2])

        if r > 1.0 and g > 1.0 and b > 1.0:
            return Vector((r / 256.0, g / 256.0, b / 256.0))
        else:
            return Vector((r, g, b))


####################################################################################################
# @ create_colormap_from_color_list
####################################################################################################
def create_colormap_from_color_list(color_list,
                                    number_colors):
    """Creates a colormap list with a given number of colors from a given color list with
    different number of colors.

    :param color_list:
        The given color list that will be used to construct the colormap.
    :param number_colors:
        The number of color items of the resulting colormap.
    :return:
        The resulting colormap with the given number of colors.
    """
    # RGB lists
    r_list = list()
    g_list = list()
    b_list = list()

    # Color list
    for color in color_list:
        r_list.append(color[0])
        g_list.append(color[1])
        b_list.append(color[2])

    # Delta
    delta = (len(color_list) - 1) / (number_colors - 1)

    # Interpolated lists
    interpolated_r_list = [interpolate_list(r_list, i * delta) for i in range(number_colors)]
    interpolated_g_list = [interpolate_list(g_list, i * delta) for i in range(number_colors)]
    interpolated_b_list = [interpolate_list(b_list, i * delta) for i in range(number_colors)]

    # Interpolated colors
    interpolated_colors = list()
    for i in range(len(interpolated_r_list)):
        interpolated_colors.append(
            Vector((interpolated_r_list[i], interpolated_g_list[i], interpolated_b_list[i])))

    return interpolated_colors


####################################################################################################
# @ create_colormap_from_hex_list
####################################################################################################
def create_colormap_from_hex_list(hex_list,
                                  number_colors):
    """Creates a colormap list with a given number of colors from a given color list with
    different number of colors in a hex coding.

    :param hex_list:
        A given colormap in a hex list.
    :param number_colors:
        The number of color items of the resulting colormap.
    :return:
        The resulting colormap with the given number of colors.
    """
    # A list of the RGB colors
    rgb_color_list = list()

    # Convert the HEX colors to RGB
    for color in hex_list:
        rgb_color_list.append(hex_to_rgb(color))

    # Create the RGB color list
    return create_colormap_from_color_list(rgb_color_list, number_colors)
