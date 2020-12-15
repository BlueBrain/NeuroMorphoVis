####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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
import copy
import sys
import os

import_paths = ['core']
for import_path in import_paths:
    sys.path.append(('%s/%s' % (os.path.dirname(os.path.realpath(__file__)), import_path)))

import parsing

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.enums
import nmv.shading


####################################################################################################
# @create_color_map_materials
####################################################################################################
def create_color_map_materials(color_map,
                               material_type=nmv.enums.Shader.FLAT):
    """Creates a list of all the materials that will be applied on the meshes of the synapses and
    the neurons as well.

    :param color_map:
        A given color-map dictionary.
    :param material_type:
        The type of the material.
    :return:
        A dictionary with all the materials created for the synapses.
    """

    # A dictionary of all the materials
    materials = {}

    # Create the list
    for i, item in enumerate(color_map):

        # Getting the color from the dictionary
        color = color_map[item]

        # Create the material
        material = nmv.shading.create_material(color=color, name='material_%d' % i,
                                               material_type=material_type)

        # Add the material to the material list
        materials[item] = material

    # Excitatory
    excitatory_color = Vector((0.7, 0.06, 0.14))
    excitatory_material = nmv.shading.create_material(
        color=excitatory_color, name='material_exc', material_type=material_type)
    materials['EXC'] = excitatory_material

    # Inhibitory
    inhibitory_color = Vector((0.23074, 0.496933, 0.938686))

    # A new color from Caitlin
    inhibitory_color = Vector((0.012983, 0.279, 0.93))

    inhibitory_material = nmv.shading.create_material(
        color=inhibitory_color, name='material_inh', material_type=material_type)
    materials['INH'] = inhibitory_material

    # Return a reference to the materials list
    return materials


####################################################################################################
# @create_json_color_map_materials
####################################################################################################
def create_json_color_map_materials(color_map,
                                    material_type=nmv.enums.Shader.FLAT):
    """Creates a list of all the materials that will be applied on the meshes of the synapses and
    the neurons as well.

    :param color_map:
        A given color-map dictionary.
    :param material_type:
        The type of the material.
    :return:
        A dictionary with all the materials created for the synapses.
    """

    # A list of all the materials
    materials = {}

    # Create the list
    for i, color in enumerate(color_map):

        # Keep a copy of the mtype
        mtype = copy.deepcopy(color)

        # Parse the color code to convert it to a Vector
        color = (color_map[color]).split(' ')

        # Convert the color vector
        color = Vector((float(color[0]), float(color[1]), float(color[2])))

        # Create the material
        material = nmv.shading.create_material(color=color, name='material_%d' % i,
                                               material_type=material_type)

        # Add the material to the material list
        materials[mtype] = material

    # Excitatory
    excitatory_color = Vector((1, 0, 0))
    excitatory_material = nmv.shading.create_material(
        color=excitatory_color, name='material_exc', material_type=material_type)
    materials['EXC'] = excitatory_material

    # Inhibitory
    inhibitory_color = Vector((0, 0, 1))
    inhibitory_material = nmv.shading.create_material(
        color=inhibitory_color, name='material_inh', material_type=material_type)
    materials['INH'] = inhibitory_material

    # Return a reference to the materials list
    return materials


####################################################################################################
# @create_color_map
####################################################################################################
def create_color_map(color_map_file,
                     material_type):
    """Creates the color-map materials list.

    :param color_map_file:
        A given color-map file.
    :return:
        A dictionary of the color-map for the synapses.
    """

    # Read the color-map file
    color_map = parsing.parse_color_map(color_map_file=color_map_file)

    # Create the color-map materials list
    color_map_materials = create_color_map_materials(color_map, material_type=material_type)

    # Return a reference to the created color map palette
    return color_map_materials


####################################################################################################
# @create_neuron_material
####################################################################################################
def create_neuron_material(neuron_color,
                           shader=nmv.enums.Shader.FLAT):
    """Creates the material of the neuron mesh.

    :param neuron_color:
        The color.
    :param shader:
        The shader.
    :return:
        A reference to the material
    """

    # Get the color
    color = neuron_color.split('_')
    color = Vector((float(color[0]) / 255.0, float(color[1]) / 255.0, float(color[2]) / 255.0))

    # Return a reference to the material
    return nmv.shading.create_material(name='neuron_material', color=color, material_type=shader)


####################################################################################################
# @create_neuron_material
####################################################################################################
def create_dummy_material(shader=nmv.enums.Shader.FLAT):
    """Creates a dummy material to adjust the rendering engine.

    :param shader:
        The shader.
    :return:
        A reference to the material
    """

    # Return a reference to the material
    return nmv.shading.create_material(name='dummy_material', color=Vector((0, 0, 0)),
                                       material_type=shader)
