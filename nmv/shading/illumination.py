####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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


# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.scene
import nmv.utilities


####################################################################################################
# @create_lambert_ward_illumination
####################################################################################################
def create_lambert_ward_illumination():
    """Creates an illumination specific for the default shader.
    """

    # Deselect all
    nmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [(-0.78, 0.000, -0.78),
                      (0.000, 3.140, 0.000),
                      (1.570, 0.000, 0.000),
                      (-1.57, 0.000, 0.000),
                      (0.000, 1.570, 0.000),
                      (0.000, -1.57, 0.000)]

    # Add the lights
    for i, angle in enumerate(light_rotation):
        if nmv.utilities.is_blender_280():
            bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.energy = 0.5
        else:
            bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.use_specular = True if i == 0 else False
            lamp_reference.data.energy = 0.5


####################################################################################################
# @create_shadow_illumination
####################################################################################################
def create_shadow_illumination():
    """Creates an illumination specific for the shadow shader.
    """

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


####################################################################################################
# @create_glossy_illumination
####################################################################################################
def create_glossy_illumination():
    """Creates an illumination specific for the glossy shader.
    """

    nmv.scene.ops.clear_lights()

    # deselect all
    nmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [(0.000, 0, 0.000),
                      (-1.57, 0.000, 0.000),
                      (0.000, -1.57, 0.000)]

    light_position = [(0, 0, 0.1),
                      (0, 0.1, 0),
                      (-0.1, 0, 0)]

    # Add the light sources
    for i, angle in enumerate(light_rotation):

        if nmv.utilities.is_blender_280():
            bpy.ops.object.light_add(type='SUN', radius=1, location=light_position[i])
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.energy = 2.5

        else:
            lamp_data = bpy.data.lamps.new(name='Lamp%d' % i, type='HEMI')
            lamp_object = bpy.data.objects.new(name='Lamp%d' % i, object_data=lamp_data)
            bpy.context.scene.objects.link(lamp_object)
            lamp_object.rotation_euler = angle
            lamp_object.location = light_position[i]
            bpy.data.lamps['Lamp%d' % i].use_nodes = True
            bpy.data.lamps['Lamp%d' % i].node_tree.nodes["Emission"].inputs[
                1].default_value = 1e5


####################################################################################################
# @create_glossy_bumpy_illumination
####################################################################################################
def create_glossy_bumpy_illumination():
    """Creates an illumination specific for the glossy-bumpy shader.
    """

    # Deselect all
    nmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [(-1.57, 0.000, 0.000),
                      (0.000, 1.570, 0.000),
                      (0.000, -1.57, 0.000)]

    # Add the lights
    for i, angle in enumerate(light_rotation):
        if nmv.utilities.is_blender_280():
            bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.energy = 10
        else:
            bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.use_specular = True if i == 0 else False
            lamp_reference.data.energy = 10


####################################################################################################
# @create_material_specific_illumination
####################################################################################################
def create_material_specific_illumination(material_type):
    """Create a specific illumination that corresponds to a given material.

    :param material_type:
        Material type.
    """

    # Lambert Ward
    if material_type == nmv.enums.Shader.LAMBERT_WARD:
        return create_lambert_ward_illumination()

    # Glossy bumpy
    elif material_type == nmv.enums.Shader.GLOSSY_BUMPY:
        return create_glossy_illumination()

    # Glossy
    elif material_type == nmv.enums.Shader.GLOSSY:
        return create_glossy_illumination()

    elif material_type == nmv.enums.Shader.GLOSSY_BUMPY:
        return create_glossy_bumpy_illumination()

    # Default, just use the lambert shader illumination
    else:
        return create_lambert_ward_illumination()
