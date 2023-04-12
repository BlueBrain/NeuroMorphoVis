####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import random

# Internal imports
import nmv.consts
import nmv.shading


####################################################################################################
# @create_single_material
####################################################################################################
def create_single_material(name,
                           material_type,
                           color):
    """Creates a single slot material for a specific material type and a given color.

    :param name:
        The name of the material/color.
    :param material_type:
        The material type.
    :param color:
        The RGB color code of the material in a Vector((R, G, B)) format.
    :return:
        A reference to the created material.
    """

    return nmv.shading.create_material(name=name, color=color, material_type=material_type)


####################################################################################################
# @create_multiple_materials_with_same_color
####################################################################################################
def create_multiple_materials_with_same_color(name,
                                              material_type,
                                              color,
                                              number_elements):
    """Creates a multiple slot material list with multiple elements for a given material type and
    a given color.

    NOTE: The created list will have the exact same material. It is only a convenient way to address
    the automated material and color update from the GUI on-the-fly.

    :param name:
        The name of the material/color.
    :param material_type:
        The material type.
    :param color:
        The RGB color code of the material in a Vector((R, G, B)) format.
    :param number_elements:
        Number of elements in the list.
    :return:
        A reference to the created material.
    """

    # A list that will contain the material
    material_list = list()

    # Iterate and append
    for i in range(number_elements):
        material_list.append(create_single_material(name='%s %d' % (name, i), color=color,
                                                    material_type=material_type))

    # Return a reference to the material list
    return material_list


####################################################################################################
# @create_multiple_materials
####################################################################################################
def create_multiple_materials(name,
                              material_type,
                              color_list):
    """Creates a list of materials (or a single material with multiple slots) with the given
    material type corresponding to the given color list.

    :param name:
        The name of the material.
    :param material_type:
        The material type.
    :param color_list:
        A list of RGB colors in a Vector((R, G, B)) format.
    :return:
        The list of created materials.
    """

    # A list that will contain all the created materials
    materials_list = list()

    # For every given color, create the corresponding material and append it to the list
    for i, color in enumerate(color_list):
        materials_list.append(create_single_material(
            name='%s_color_%d' % (name, i), color=color, material_type=material_type))

    # Return the created material list
    return materials_list


####################################################################################################
# @create_skeleton_materials
####################################################################################################
def create_skeleton_materials(name,
                              material_type,
                              color):
    """Creates two materials for any component of the skeleton based on the input parameters
    of the user.

    :param name:
        The name of the material/color.
    :param material_type:
        The material type.
    :param color:
        The code of the given colors.
    :return:
        A list of two elements (different or even same colors) where we can apply later to the
        drawn sections or segments.
    """

    # A list of the created materials
    materials_list = list()

    # Random colors
    if color.x == -1 and color.y == 0 and color.z == 0:

        # Initialize the color vector to black
        color_vector = nmv.consts.Color.BLACK

        # Generate random colors
        for i in range(2):
            color_vector.x = random.uniform(0.0, 1.0)
            color_vector.y = random.uniform(0.0, 1.0)
            color_vector.z = random.uniform(0.0, 1.0)

            # Create the material and append it to the list
            material = nmv.shading.create_material(
                name='%s_random_%d' % (name, i), color=color_vector, material_type=material_type)
            materials_list.append(material)

    # If set to black / white
    elif color.x == 0 and color.y == -1 and color.z == 0:

        # Create the material and append it to the list
        material = nmv.shading.create_material(
            name='%s_bw_0' % name, color=nmv.consts.Color.MATT_BLACK , material_type=material_type)
        materials_list.append(material)

        # Create the material and append it to the list
        material = nmv.shading.create_material(
            name='%s_bw_1' % name, color=nmv.consts.Color.WHITE, material_type=material_type)
        materials_list.append(material)

    # Specified colors
    else:
        for i in range(2):

            # Create the material and append it to the list
            material = nmv.shading.create_material(
                name='%s_color_%d' % (name, i), color=color, material_type=material_type)
            materials_list.append(material)

    # Return the list
    return materials_list
