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

# System imports
import os 

# Blender imports
import bpy

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.scene


####################################################################################################
# @import_shader
####################################################################################################
def import_shader(shader_name):
    """Import a shader from  the NeuroMorphoVis shading library.

    :param shader_name:
        The name of the shader file in the library.
    :return:
        A reference to the shader after being loaded into blender.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Get the path of this file
    current_file = os.path.dirname(os.path.realpath(__file__))
    shaders_directory = '%s/shaders/%s.blend/Material' % (current_file, shader_name)

    # Import the material
    bpy.ops.wm.append(filename='material', directory=shaders_directory)

    # Get a reference to the material
    material_reference = bpy.data.materials['material']

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_shadow_material
####################################################################################################
def create_shadow_material(name,
                           color=nmv.consts.Color.WHITE):
    """
    Creates a material with shadow. This requires creating two light sources if they don't exist
    in the scene.
    This function imports the shadow-material from the materials library and updates its parameters.
    :param name:
        Material name.
    :param color:
        Material color, by default white.
    :return:
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # If no light sources in the scene, then create two sources one towards the top and the
    # other one towards the bottom
    if not nmv.scene.ops.is_object_in_scene_by_name('LampUp'):
        nmv.scene.ops.deselect_all()

        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'LampUp'
        lamp_reference.data.name = "LampUp"
        lamp_reference.location[0] = 0
        lamp_reference.location[1] = 0
        lamp_reference.location[2] = 0
        lamp_reference.rotation_euler[0] = 1.5708
        bpy.data.lamps['LampUp'].node_tree.nodes["Emission"].inputs[1].default_value = 5

        nmv.scene.ops.deselect_all()
        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'LampDown'
        lamp_reference.data.name = "LampDown"
        lamp_reference.location[0] = 0
        lamp_reference.location[1] = 0
        lamp_reference.location[2] = 0
        lamp_reference.rotation_euler[0] = -1.5708
        bpy.data.lamps['LampDown'].node_tree.nodes["Emission"].inputs[1].default_value = 5

    # Import the material from the library
    material_reference = import_shader(shader_name='shadow-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_super_electron_light_material
####################################################################################################
def create_super_electron_light_material(name,
                                         color=nmv.consts.Color.WHITE):
    """
    Creates a light electron shader.

    :param name:
        Material name
    :param color:
        Material color, by default white.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='super-electron-light-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_super_electron_dark_material
####################################################################################################
def create_super_electron_dark_material(name,
                                        color=nmv.consts.Color.WHITE):
    """
    Creates a light electron shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='super-electron-dark-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_flat_material
####################################################################################################
def create_flat_material(name,
                         color=nmv.consts.Color.WHITE):
    """
    Creates a flat shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='flat-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_electron_light_material
####################################################################################################
def create_electron_light_material(name,
                                   color=nmv.consts.Color.WHITE):
    """
    Creates a light electron shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='electron-light-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_electron_dark_material
####################################################################################################
def create_electron_dark_material(name,
                                  color=nmv.consts.Color.WHITE):
    """
    Creates a light electron shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='electron-dark-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_default_material
####################################################################################################
def create_lambert_ward_material(name,
                                 color=nmv.consts.Color.WHITE,
                                 specular=(1, 1, 1),
                                 alpha=0.0):
    """
    Creates a a texture material.

    :param name:
        Material name.
    :param color:
        Diffuse component.
    :param specular:
        Specular component.
    :param alpha:
        Transparency value, default opaque alpha = 0.
    :return:
        A reference to the material.
    """

    # If no light sources in the scene, then create two sources one towards the top and the
    # other one towards the bottom
    if not nmv.scene.ops.is_object_in_scene_by_name('DefaultLamp'):
        nmv.scene.ops.deselect_all()

        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'DefaultLamp'
        lamp_reference.data.name = "DefaultLamp"
        lamp_reference.location[0] = 0
        lamp_reference.location[1] = 0
        lamp_reference.location[2] = 0

    # Create a new material
    material_reference = bpy.data.materials.new(name)

    # Set the diffuse parameters
    material_reference.diffuse_color = color
    material_reference.diffuse_shader = 'LAMBERT'
    material_reference.diffuse_intensity = 1.0

    # Set the specular parameters
    material_reference.specular_color = specular
    material_reference.specular_shader = 'WARDISO'
    material_reference.specular_intensity = 1

    # Transparency
    material_reference.alpha = alpha

    # Set the ambient parameters
    material_reference.ambient = 1.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_material
####################################################################################################
def create_material(name,
                    color,
                    material_type):
    """Create a specific material given its type and color.

    :param name:
        Material name.
    :param color:
        Material color.
    :param material_type:
        Material type.
    :return:
        A reference to the created material
    """

    # Lambert Ward
    if material_type == nmv.enums.Shading.LAMBERT_WARD:
        return create_lambert_ward_material(name='%s_color' % name, color=color)

    # Super electron light
    elif material_type == nmv.enums.Shading.SUPER_ELECTRON_LIGHT:
        return create_super_electron_light_material(name='%s_color' % name, color=color)

    # Super electron dark
    elif material_type == nmv.enums.Shading.SUPER_ELECTRON_DARK:
        return create_super_electron_dark_material(name='%s_color' % name, color=color)

    # Electron light
    elif material_type == nmv.enums.Shading.ELECTRON_LIGHT:
        return create_electron_light_material(name='%s_color' % name, color=color)

    # Electron dark
    elif material_type == nmv.enums.Shading.ELECTRON_DARK:
        return create_electron_dark_material(name='%s_color' % name, color=color)

    # Shadow
    elif material_type == nmv.enums.Shading.SHADOW:
        return create_shadow_material(name='%s_color' % name, color=color)

    # Flat
    elif material_type == nmv.enums.Shading.FLAT:
        return create_flat_material(name='%s_color' % name, color=color)

    # Default
    else:
        return create_lambert_ward_material(name='%s_color' % name, color=color)


####################################################################################################
# @set_material_to_object
####################################################################################################
def set_material_to_object(mesh_object,
                           material_reference):
    """Assign the given material to a given mesh object.

    :param mesh_object:
        A surface mesh object.
    :param material_reference:
        The material to be assigned to the object.
    """

    # assign the material to the given object.
    mesh_object.data.materials.clear()
    mesh_object.data.materials.append(material_reference)
