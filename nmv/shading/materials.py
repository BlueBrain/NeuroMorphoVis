####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# System imports
import os 

# Blender imports
import bpy
import mathutils

# Internal imports
import nmv.consts
import nmv.enums
import nmv.scene
import nmv.utilities


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
# @switch_freestyle
####################################################################################################
def switch_freestyle(use_freestyle=False):
    """Turns on and off the free-style mode.

    :param use_freestyle:
        A flag to switch on and off the free-style mode.
    """

    # Should we use the freestyle mode or not
    bpy.context.scene.render.use_freestyle = use_freestyle


####################################################################################################
# @create_shadow_material
####################################################################################################
def create_shadow_material(name,
                           color=nmv.consts.Color.WHITE):
    """Creates a material with shadow. This requires creating two light sources if they don't exist
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
    current_scene.render.engine = 'CYCLES'

    # Use 64 samples per pixel to create a nice image.
    bpy.context.scene.cycles.samples = 64

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

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_super_electron_light_material
####################################################################################################
def create_super_electron_light_material(name,
                                         color=nmv.consts.Color.WHITE):
    """Creates a light electron shader.

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
    current_scene.render.engine = 'CYCLES'

    # Use only 2 samples
    bpy.context.scene.cycles.samples = nmv.consts.Image.DEFAULT_SPP

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

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_super_electron_dark_material
####################################################################################################
def create_principled_shader(name,
                             color=nmv.consts.Color.WHITE):
    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    current_scene.render.engine = 'CYCLES'

    # Use only 2 samples
    bpy.context.scene.cycles.samples = nmv.consts.Image.DEFAULT_SPP

    # Import the material from the library
    material_reference = import_shader(shader_name='principled')

    # Rename the material
    material_reference.name = str(name)

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_super_electron_dark_material
####################################################################################################
def create_super_electron_dark_material(name,
                                        color=nmv.consts.Color.WHITE):
    """Creates a light electron shader.

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
    current_scene.render.engine = 'CYCLES'

    # Use only 2 samples
    bpy.context.scene.cycles.samples = nmv.consts.Image.DEFAULT_SPP

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

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_flat_material
####################################################################################################
def create_flat_material(name,
                         color=nmv.consts.Color.WHITE):
    """Creates a flat shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    if nmv.utilities.is_blender_280():

        # Set the current rendering engine to Blender
        current_scene.render.engine = 'BLENDER_WORKBENCH'

        # Create a new material (color) and assign it to the line
        color = mathutils.Vector((color[0], color[1], color[2], 1.0))

        # Create a new material (color) and assign it to the line
        material_reference = bpy.data.materials.new('%s' % name)
        material_reference.diffuse_color = color

        # Zero-metallic and roughness
        material_reference.roughness = 0.0
        material_reference.metallic = 0.0

        # Flat shading
        bpy.context.scene.display.shading.light = 'FLAT'
        nmv.scene.set_scene_transparency(transparent=False)

        # Switch the view port shading
        nmv.scene.switch_scene_shading('RENDERED')

    else:

        # Switch the rendering engine to cycles to be able to create the material
        current_scene.render.engine = 'CYCLES'

        # Use only 2 samples
        bpy.context.scene.cycles.samples = nmv.consts.Image.DEFAULT_SPP

        # Import the material from the library
        material_reference = import_shader(shader_name='flat-material')

        # Rename the material
        material_reference.name = str(name)

        # Update the color gradient
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2]

        # Switch the view port shading
        nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_transparent_material
####################################################################################################
def create_transparent_material(name,
                                color=nmv.consts.Color.WHITE):
    """Creates a flat shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    if nmv.utilities.is_blender_280():

        # Set the current rendering engine to Blender
        current_scene.render.engine = 'BLENDER_WORKBENCH'

        # Create a new material (color) and assign it to the line
        color = mathutils.Vector((color[0], color[1], color[2], 1.0))

        # Create a new material (color) and assign it to the line
        material_reference = bpy.data.materials.new('%s' % name)
        material_reference.diffuse_color = color

        # Zero-metallic and roughness
        material_reference.roughness = 0.0
        material_reference.metallic = 0.0

        # Transparent shading
        bpy.context.scene.display.shading.light = 'STUDIO'
        bpy.context.scene.display.shading.studio_light = 'Default'
        bpy.context.scene.display.shading.show_xray = True

        # Switch the view port shading
        nmv.scene.switch_scene_shading('SOLID')

        # Switch to transparent
        nmv.scene.set_scene_transparency(transparent=True)

    else:

        # Switch the rendering engine to cycles to be able to create the material
        current_scene.render.engine = 'CYCLES'

        # Use only 2 samples
        bpy.context.scene.cycles.samples = nmv.consts.Image.DEFAULT_SPP

        # Import the material from the library
        material_reference = import_shader(shader_name='flat-material')

        # Rename the material
        material_reference.name = str(name)

        # Update the color gradient
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2]

        # Switch the view port shading
        nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_toon_material
####################################################################################################
def create_toon_material(name,
                            color=nmv.consts.Color.WHITE):
    """Creates a carton shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    if nmv.utilities.is_blender_280():

        # Set the current rendering engine to Blender
        current_scene.render.engine = 'BLENDER_WORKBENCH'

        # Create a new material (color) and assign it to the line
        color = mathutils.Vector((color[0], color[1], color[2], 1.0))

        # Create a new material (color) and assign it to the line
        material_reference = bpy.data.materials.new('%s' % name)
        material_reference.diffuse_color = color

        # Zero-metallic and roughness
        material_reference.roughness = 0.0
        material_reference.metallic = 0.0

        # Flat shading
        bpy.context.scene.display.shading.light = 'MATCAP'
        bpy.context.scene.display.shading.studio_light = 'toon.exr'
        nmv.scene.set_scene_transparency(transparent=False)

        # Switch the view port shading
        nmv.scene.switch_scene_shading('SOLID')

    else:

        # Switch the rendering engine to cycles to be able to create the material
        current_scene.render.engine = 'CYCLES'

        bpy.context.scene.cycles.samples = 2

        # Import the material from the library
        material_reference = import_shader(shader_name='flat-material')

        # Rename the material
        material_reference.name = str(name)

        # Update the color gradient
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1]
        material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2]

        # Switch the view port shading
        nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_voronoi_cells_material
####################################################################################################
def create_voronoi_cells_material(name,
                                 color=nmv.consts.Color.WHITE):
    """Creates a voronoi shader.

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
    current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='voronoi-cells')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2]

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_wire_frame_material
####################################################################################################
def create_wire_frame_material(name,
                                 color=nmv.consts.Color.WHITE):
    """Creates a wire frame shader.

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
    current_scene.render.engine = 'CYCLES'

    # Use only 2 samples
    bpy.context.scene.cycles.samples = nmv.consts.Image.DEFAULT_SPP

    # Import the material from the library
    material_reference = import_shader(shader_name='wire-frame')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2]

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_electron_light_material
####################################################################################################
def create_electron_light_material(name,
                                   color=nmv.consts.Color.WHITE):
    """Creates a light electron shader.

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
    current_scene.render.engine = 'CYCLES'

    # Use only 2 samples
    bpy.context.scene.cycles.samples = nmv.consts.Image.DEFAULT_SPP

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

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_electron_dark_material
####################################################################################################
def create_electron_dark_material(name,
                                  color=nmv.consts.Color.WHITE):
    """Creates a light electron shader.

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
    current_scene.render.engine = 'CYCLES'

    # Use only 2 samples
    bpy.context.scene.cycles.samples = nmv.consts.Image.DEFAULT_SPP

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

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_default_material
####################################################################################################
def create_lambert_ward_material(name,
                                 color=nmv.consts.Color.WHITE,
                                 specular=(1, 1, 1),
                                 alpha=0.0):
    """Creates a a texture material.

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

    # Get active scene
    current_scene = bpy.context.scene

    # Set the current rendering engine to Blender

    if nmv.utilities.is_blender_280():
        current_scene.render.engine = 'BLENDER_WORKBENCH'

        # Create a new material (color) and assign it to the line
        color = mathutils.Vector((color[0], color[1], color[2], 1.0))

        # Create a new material (color) and assign it to the line
        line_material = bpy.data.materials.new('%s' % name)
        line_material.diffuse_color = color

        # Zero-metallic and roughness
        line_material.roughness = 0.0
        line_material.metallic = 0.0

        # Switch the view port shading
        nmv.scene.switch_scene_shading('SOLID')

        bpy.context.scene.display.shading.light = 'STUDIO'
        bpy.context.scene.display.shading.studio_light = 'Default'
        nmv.scene.set_scene_transparency(transparent=False)

        # Return a reference to the material
        return line_material

    else:
        current_scene.render.engine = 'BLENDER_RENDER'

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

        # Switch the view port shading
        nmv.scene.switch_scene_shading('SOLID')

        # Return a reference to the material
        return material_reference


####################################################################################################
# @create_free_style_material
####################################################################################################
def create_free_style_material(name,
                               color=nmv.consts.Color.WHITE,
                               specular=(1, 1, 1),
                               alpha=0.0):
    """Creates a a texture material.

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

    # Get active scene
    current_scene = bpy.context.scene

    # Blender 2.8
    if nmv.utilities.is_blender_280():

        # Set the current rendering engine to Blender
        current_scene.render.engine = 'BLENDER_EEVEE'

        # Create a new material (color) and assign it to the line
        color = mathutils.Vector((color[0], color[1], color[2], 1.0))

        # Create a new material (color) and assign it to the line
        line_material = bpy.data.materials.new('%s' % name)
        line_material.diffuse_color = color

        # Zero-metallic and roughness
        line_material.specular_intensity = 0.5
        line_material.roughness = 0.015
        line_material.metallic = 0.0

        # Disable the transparency
        nmv.scene.set_scene_transparency(transparent=False)

        # Use the free style
        current_scene.render.use_freestyle = True

        # Return a reference to the material
        return line_material

    else:
        current_scene.render.engine = 'BLENDER_RENDER'

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

        # Switch the view port shading
        nmv.scene.switch_scene_shading('SOLID')

        # Return a reference to the material
        return material_reference


####################################################################################################
# @create_glossy_material
####################################################################################################
def create_glossy_material(name,
                           color=nmv.consts.Color.WHITE):
    """Creates a glossy shader.

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
    current_scene.render.engine = 'CYCLES'

    # Use 64 samples per pixel to create a nice image.
    bpy.context.scene.cycles.samples = 64

    # Import the material from the library
    material_reference = import_shader(shader_name='glossy')

    # Rename the material
    material_reference.name = str(name)

    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[0] = color[0]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[1] = color[1]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[2] = color[2]

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_glossy_blending_material
####################################################################################################
def create_glossy_blending_material(name,
                                    color=nmv.consts.Color.WHITE):
    """Creates a glossy shader.

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
    current_scene.render.engine = 'BLENDER_EEVEE'

    # Use 64 samples per pixel to create a nice image.
    bpy.context.scene.cycles.samples = 64

    # Import the material from the library
    material_reference = import_shader(shader_name='glossy-blending')

    # Rename the material
    material_reference.name = str(name)

    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[0] = color[0]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[1] = color[1]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[2] = color[2]

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_glossy_material
####################################################################################################
def create_glossy_bumpy_material(name,
                                 color=nmv.consts.Color.WHITE):
    """Creates a glossy bumpy shader.

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
    current_scene.render.engine = 'CYCLES'

    # Use 64 samples per pixel to create a nice image.
    bpy.context.scene.cycles.samples = 64

    # Import the material from the library
    material_reference = import_shader(shader_name='glossy-bumpy')

    # Rename the material
    material_reference.name = str(name)

    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[0] = color[0]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[1] = color[1]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[2] = color[2]

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_material
####################################################################################################
def create_material(name,
                    color,
                    material_type=nmv.enums.Shader.LAMBERT_WARD):
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

    # By default, set colors to filmic
    nmv.scene.set_colors_to_filimc()

    # Setting the scene transparency to False before the creating of any shader
    nmv.scene.set_scene_transparency(transparent=False)

    # Turn off the free-style modes
    switch_freestyle(use_freestyle=False)

    # Lambert Ward
    if material_type == nmv.enums.Shader.LAMBERT_WARD:
        return create_lambert_ward_material(name='%s' % name, color=color)

    # Free-style material
    elif material_type == nmv.enums.Shader.FREE_STYLE:
        return create_free_style_material(name='%s' % name, color=color)

    # Super electron light
    elif material_type == nmv.enums.Shader.SUPER_ELECTRON_LIGHT:
        return create_super_electron_light_material(name='%s' % name, color=color)

    # Super electron dark
    elif material_type == nmv.enums.Shader.SUPER_ELECTRON_DARK:
        return create_super_electron_dark_material(name='%s' % name, color=color)

    # Electron light
    elif material_type == nmv.enums.Shader.ELECTRON_LIGHT:
        return create_electron_light_material(name='%s' % name, color=color)

    # Electron dark
    elif material_type == nmv.enums.Shader.ELECTRON_DARK:
        return create_electron_dark_material(name='%s' % name, color=color)

    # Glossy
    elif material_type == nmv.enums.Shader.GLOSSY:
        return create_glossy_material(name='%s' % name, color=color)

    # Glossy blending
    elif material_type == nmv.enums.Shader.GLOSSY_BLENDING:
        return create_glossy_blending_material(name='%s' % name, color=color)

    # Glossy
    elif material_type == nmv.enums.Shader.WAX:
        return create_glossy_material(name='%s' % name, color=color)

    # Glossy bumpy
    elif material_type == nmv.enums.Shader.GLOSSY_BUMPY:
        return create_glossy_bumpy_material(name='%s' % name, color=color)

    # Wire frame
    elif material_type == nmv.enums.Shader.WIRE_FRAME:
        return create_wire_frame_material(name='%s' % name, color=color)

    # Flat
    elif material_type == nmv.enums.Shader.FLAT:
        # Always set the colors to raw when using the flat material
        nmv.scene.set_colors_to_raw()
        return create_flat_material(name='%s' % name, color=color)

    # Toon
    elif material_type == nmv.enums.Shader.TOON:
        return create_toon_material(name='%s' % name, color=color)

    # Transparent
    elif material_type == nmv.enums.Shader.TRANSPARENT:
        return create_transparent_material(name='%s' % name, color=color)

    # Default
    else:
        return create_lambert_ward_material(name='%s' % name, color=color)


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

    # Clear the previous materials assigned to this mesh object
    mesh_object.data.materials.clear()

    # Assign the material to the given object.
    mesh_object.data.materials.append(material_reference)


####################################################################################################
# @adjust_material_uv
####################################################################################################
def adjust_material_uv(mesh_object,
                       size=5.0):
    """Update the texture space of the created meshes

    :param mesh_object:
        A given mesh object.
    :param size:
        The texture space size of the material, by default set to 1.
    """
    # Select the mesh
    nmv.scene.set_active_object(mesh_object)

    # Set the 'auto_texspace' to False
    mesh_object.data.use_auto_texspace = False

    # Update the texture space size
    mesh_object.data.texspace_size[0] = size
    mesh_object.data.texspace_size[1] = size
    mesh_object.data.texspace_size[2] = size


################################################################################################
# @adjust_materials_uv
################################################################################################
def adjust_materials_uv(mesh_objects,
                        texspace_size=5.0):
    """Adjusts the UV mapping of a list of meshes.
    This operation is recommended to be called after any mesh operation.

    :param mesh_objects:
        A list of meshes.
    :param texspace_size:
        Texture space size, by default 5.0.
    """

    # Adjust the UVs
    for i, mesh_object in enumerate(mesh_objects):
        nmv.shading.adjust_material_uv(mesh_object, size=texspace_size)


####################################################################################################
# @create_materials
####################################################################################################
def create_materials(material_type,
                     name,
                     color):
    """Creates just two materials of the mesh on the input parameters of the user.

    :param material_type:
        The type of the material.
    :param name:
        The name of the material/color.
    :param color:
        The code of the given colors.
    :return:
        A list of two elements (different or same colors) where we can apply later to the drawn
        sections or segments.
    """

    # By default, no transparency
    nmv.scene.set_scene_transparency(transparent=False)

    # Turn off the free-style mode
    switch_freestyle(use_freestyle=False)

    # Create a list of two materials such that you can switch between them in the scene
    materials_list = list()
    for i in range(nmv.consts.Color.NUMBER_MATERIALS):
        materials_list.append(nmv.shading.create_material(
            name='%s %d' % (name, i + 1), color=color, material_type=material_type))

    # Return the materials list
    return materials_list
