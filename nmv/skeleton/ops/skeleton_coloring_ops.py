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
import random
from mathutils import Vector

# Internal imports
import nmv
import nmv.consts
import nmv.shading


####################################################################################################
# @create_materials
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
    materials_list = []

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
