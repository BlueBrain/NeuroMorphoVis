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

# System imports
import os 

# Blender imports
import bpy

# Internal imports
import nmv
import nmv.consts
import nmv.enums
import nmv.scene


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
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

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
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2]

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
    if not current_scene.render.engine == 'CYCLES':
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
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

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
    if not current_scene.render.engine == 'BLENDER_RENDER':
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
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='glossy')

    # Rename the material
    material_reference.name = str(name)

    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[0] = color[0]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[1] = color[1]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[2] = color[2]

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
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='glossy-bumpy')

    # Rename the material
    material_reference.name = str(name)

    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[0] = color[0]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[1] = color[1]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[2] = color[2]

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

    # Glossy
    elif material_type == nmv.enums.Shading.GLOSSY:
        return create_glossy_material(name='%s_color' % name, color=color)

    # Glossy bumpy
    elif material_type == nmv.enums.Shading.GLOSSY_BUMPY:
        return create_glossy_bumpy_material(name='%s_color' % name, color=color)

    # Voronoi
    elif material_type == nmv.enums.Shading.VORONOI:
        return create_voronoi_cells_material(name='%s_color' % name, color=color)

    # Wire frame
    elif material_type == nmv.enums.Shading.WIRE_FRAME:
        return create_wire_frame_material(name='%s_color' % name, color=color)

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
# @create_materials
################################################################################################
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

    # A list of the created materials
    materials_list = []
    for i in range(2):

        # Create the material
        material = nmv.shading.create_material(name='%s_color_%d' % (name, i), color=color,
                                               material_type=material_type)

        # Append the material to the materials list
        materials_list.append(material)

    # Return the list
    return materials_list
