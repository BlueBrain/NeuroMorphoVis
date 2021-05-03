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

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.shading


####################################################################################################
# @interpolate_list
####################################################################################################
def interpolate_list(input_list,
                     fi):
    """Interpolation.

    :param input_list:
        Either R or G or B values list.
    :param fi:
        Index
    :return:
        Interpolated list
    """
    # Split floating-point index into whole & fractional parts
    i, f = int(fi // 1), fi % 1

    # Avoid index error
    j = i + 1 if f > 0 else i

    # Return the value
    return (1 - f) * input_list[i] + f * input_list[j]


####################################################################################################
# @ create_colormap_from_color_list
####################################################################################################
def create_colormap_from_color_list(color_list,
                                    number_colors):
    """Creates a well defined color-map with specific number of elements from a given color list.

    :param color_list:
        A given color list.
    :param number_colors:
        The number of colors in the color-map, by default 32.
    :return:
        The created color-map.
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
        interpolated_colors.append(Vector((interpolated_r_list[i],
                                           interpolated_g_list[i],
                                           interpolated_b_list[i])))

    return interpolated_colors


####################################################################################################
# @ create_colormap_materials
####################################################################################################
def create_colormap_materials(colormap):

    color_0 = Vector((1, 1, 0))
    color_1 = Vector((1, 0, 0))
    colors = [color_0, color_1]

    # Create the colormap
    colormap = create_colormap_from_color_list(colors, number_materials)

    # A list that will contain all the materials
    materials = list()
    for i in range(number_materials):
        materials.append(nmv.shading.create_lambert_ward_material('color_%d' % i, colormap[i]))

    # Return the materials list
    return materials
