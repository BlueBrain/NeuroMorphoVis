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

# imports
import bpy


####################################################################################################
# @create_electron_material
####################################################################################################
def create_electron_material(name='electron',
                             color_1=(1.0, 0.0, 0.0),
                             color_2=(0.0, 0.0, 0.0),
                             scale=100,
                             detail=1.0,
                             level=1):
    """
    Creates an electron shader material.

    :param name:
        The name of the shader.
    :param color_1:
        Color 1.
    :param color_2:
        Color 2.
    :param scale:
        Shader scale.
    :param detail:
        Shader detail.
    :param level:
        Shader level.

    :return: A reference to the electron shader.
    """

    # Get active scene
    scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not scene.render.engine == 'CYCLES':
        scene.render.engine = 'CYCLES'

    # Create the material
    material = bpy.data.materials.new(name)

    # Use nodes to edit the properties of the material
    material.use_nodes = True

    # Get a reference for the nodes to edit them
    nodes = material.node_tree.nodes

    # Move the Material Output node
    node = nodes['Material Output']
    node.location = 900, 100

    # Move the DIffuse BSDF node
    node = nodes['Diffuse BSDF']
    node.location = 500, 400

    # Add a MixShader node
    node = nodes.new('ShaderNodeMixShader')
    node.label = 'MixShader'
    node.name = 'MixShader'
    node.location = 700, 200

    # Add a Multiply node
    node = nodes.new('ShaderNodeMath')
    node.operation = 'MULTIPLY'
    node.label = 'Multiply'
    node.name = 'Multiply'
    node.location = 700, 0
    node.inputs[1].default_value = level

    # Add a Noise Texture node
    node = nodes.new('ShaderNodeTexNoise')
    node.label = 'NoiseTexture'
    node.name = 'NoiseTexture'
    node.location = 500, 0
    node.inputs['Scale'].default_value = scale
    node.inputs['Detail'].default_value = detail

    # Add an Emission node
    node = nodes.new('ShaderNodeEmission')
    node.label = 'Emission'
    node.name = 'Emission'
    node.location = 500, 200

    # Add a ColorRamp node
    node = nodes.new('ShaderNodeValToRGB')
    node.label = 'ColorRamp'
    node.name = 'ColorRamp'
    node.location = 200, 0
    node.color_ramp.interpolation = 'B_SPLINE'
    node.color_ramp.elements[0].color = (color_1[0], color_1[1], color_1[2], 1)
    node.color_ramp.elements[1].color = (color_1[0] * 0.25, color_1[1] * 0.25, color_1[2] * 0.25, 1)

    # Add a LayerWeight node
    node = nodes.new('ShaderNodeLayerWeight')
    node.label = 'LayerWeight'
    node.name = 'LayerWeight'
    node.location = 0, 0
    node.inputs[0].default_value = 0.75

    # Connect
    output = nodes['MixShader'].outputs['Shader']
    input = nodes['Material Output'].inputs['Surface']
    material.node_tree.links.new(output, input)

    # Connect
    output = nodes['Multiply'].outputs['Value']
    input = nodes['Material Output'].inputs['Displacement']
    material.node_tree.links.new(output, input)

    # Connect
    output = nodes['NoiseTexture'].outputs['Color']
    input = nodes['Multiply'].inputs[0]
    material.node_tree.links.new(output, input)

    # Connect
    output = nodes['Emission'].outputs['Emission']
    input = nodes['MixShader'].inputs[2]
    material.node_tree.links.new(output, input)

    # Connect
    output = nodes['ColorRamp'].outputs['Color']
    input = nodes['Emission'].inputs['Color']
    material.node_tree.links.new(output, input)

    # Connect
    output = nodes['LayerWeight'].outputs['Facing']
    input = nodes['ColorRamp'].inputs['Fac']
    material.node_tree.links.new(output, input)

    # Connect
    output = nodes['LayerWeight'].outputs['Facing']
    input = nodes['MixShader'].inputs['Fac']
    material.node_tree.links.new(output, input)
    pass

    # Return a reference to the created material
    return material
