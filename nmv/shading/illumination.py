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


# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv.consts
import nmv.enums
import nmv.scene
import nmv.utilities


####################################################################################################
# @create_six_sun_lights
####################################################################################################
def create_six_sun_lights(power=0.5,
                          location=nmv.consts.Math.ORIGIN):
    """Creates a set of six sun-lights at specific location with a uniform power to cover the
    illumination from all the directions around the object.

    :param power:
        The energy of the light sources.
    :param location:
        The locations of the light sources.
    :return
        A list of all the created light sources.
    """

    # A list that will contain all the created light sources
    lights = list()

    # Multiple light sources from different directions
    light_directions = [(-0.78, 0.000, -0.78), (0.000, 3.140, 0.000), (1.570, 0.000, 0.000),
                        (-1.57, 0.000, 0.000), (0.000, 1.570, 0.000), (0.000, -1.57, 0.000)]

    # Add the lights
    for i, direction in enumerate(light_directions):

        # The light creation functions are different for Blender 2.79 and 2.8
        if nmv.utilities.is_blender_280():
            bpy.ops.object.light_add(type='SUN', radius=1, location=location)
        else:
            bpy.ops.object.lamp_add(type='SUN', radius=1, location=location)

        # Get a reference to the lamp
        lamp_reference = bpy.context.object

        # Set the name
        lamp_reference.name = 'Light%d_SUN' % i
        lamp_reference.data.name = "Light%d_SUN" % i

        # Set the direction
        lamp_reference.rotation_euler = direction

        # Set the power
        lamp_reference.data.energy = power

        lights.append(lamp_reference)

    # Return the lights
    return lights


####################################################################################################
# @create_free_style_illumination
####################################################################################################
def create_free_style_illumination(location=nmv.consts.Math.ORIGIN):

    """Creates an illumination specific for the default shader.
    """

    # Deselect all
    nmv.scene.ops.deselect_all()

    # Create the set of six sun lights
    return create_six_sun_lights(power=2.0, location=location)


####################################################################################################
# @create_lambert_ward_illumination
####################################################################################################
def create_lambert_ward_illumination(location=nmv.consts.Math.ORIGIN):
    """Creates an illumination specific for the default shader.
    """

    # Deselect all
    nmv.scene.ops.deselect_all()

    # Deselect all
    nmv.scene.ops.deselect_all()

    # Create the set of six sun lights
    return create_six_sun_lights(power=1.0, location=location)


####################################################################################################
# @create_shadow_illumination
####################################################################################################
def create_shadow_illumination(location=nmv.consts.Math.ORIGIN):
    """Creates an illumination specific for the shadow shader.
    """

    # A list that will contain all the created light sources
    lights = list()

    # If no light sources in the scene, then create two sources one towards the top and the
    # other one towards the bottom
    if not nmv.scene.ops.is_object_in_scene_by_name('LampUp'):
        nmv.scene.ops.deselect_all()

        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'LampUp'
        lamp_reference.data.name = "LampUp"
        lamp_reference.location = location
        lamp_reference.rotation_euler[0] = 1.5708
        bpy.data.lamps['LampUp'].node_tree.nodes["Emission"].inputs[1].default_value = 5
        lights.append(lamp_reference)

        nmv.scene.ops.deselect_all()
        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'LampDown'
        lamp_reference.data.name = "LampDown"
        lamp_reference.location[0] = location
        lamp_reference.rotation_euler[0] = -1.5708
        bpy.data.lamps['LampDown'].node_tree.nodes["Emission"].inputs[1].default_value = 5
        lights.append(lamp_reference)

    # Return the lights
    return lights


####################################################################################################
# @create_glossy_illumination
####################################################################################################
def create_glossy_illumination(location=nmv.consts.Math.ORIGIN):
    """Creates an illumination specific for the glossy shader.
    """

    nmv.scene.ops.clear_lights()

    # A list that will contain all the created light sources
    lights = list()

    # deselect all
    nmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [(0.000, 0, 0.000),
                      (-1.57, 0.000, 0.000),
                      (0.000, -1.57, 0.000)]

    light_position = [Vector((0, 0, 0.1)),
                      Vector((0, 0.1, 0)),
                      Vector((-0.1, 0, 0))]

    # Add the light sources
    for i, angle in enumerate(light_rotation):

        if nmv.utilities.is_blender_280():
            bpy.ops.object.light_add(type='SUN', radius=1, location=light_position[i] + location)
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.energy = 2.5
            lights.append(lamp_reference)

        else:
            lamp_data = bpy.data.lamps.new(name='Lamp%d' % i, type='HEMI')
            lamp_object = bpy.data.objects.new(name='Lamp%d' % i, object_data=lamp_data)
            bpy.context.scene.objects.link(lamp_object)
            lamp_object.rotation_euler = angle
            lamp_object.location = light_position[i] + location
            bpy.data.lamps['Lamp%d' % i].use_nodes = True
            bpy.data.lamps['Lamp%d' % i].node_tree.nodes["Emission"].inputs[1].default_value = 1e5
            lights.append(lamp_object)

    # Return the lights
    return lights


####################################################################################################
# @create_glossy_bumpy_illumination
####################################################################################################
def create_glossy_bumpy_illumination(location=nmv.consts.Math.ORIGIN):
    """Creates an illumination specific for the glossy-bumpy shader.
    """

    # Deselect all
    nmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [Vector((-1.57, 0.000, 0.000)),
                      Vector((0.000, 1.570, 0.000)),
                      Vector((0.000, -1.57, 0.000))]
    # A list that will contain all the created light sources
    lights = list()

    # Add the lights
    for i, angle in enumerate(light_rotation):
        if nmv.utilities.is_blender_280():
            bpy.ops.object.light_add(type='SUN', radius=1, location=location)
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.energy = 10
            lights.append(lamp_reference)
        else:
            bpy.ops.object.lamp_add(type='SUN', radius=1, location=location)
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.use_specular = True if i == 0 else False
            lamp_reference.data.energy = 10
            lights.append(lamp_reference)

    # Return the lights
    return lights


####################################################################################################
# @create_material_specific_illumination
####################################################################################################
def create_material_specific_illumination(material_type,
                                          location=nmv.consts.Math.ORIGIN):
    """Create a specific illumination that corresponds to a given material.

    :param material_type:
        Material type.
    :param location:
        The location where the illumination sources will be added
    """

    # Lambert Ward
    if material_type == nmv.enums.Shader.LAMBERT_WARD:
        return create_lambert_ward_illumination(location=location)

    # Free-style
    elif material_type == nmv.enums.Shader.FREE_STYLE:
        return create_free_style_illumination(location=location)

    # Glossy bumpy
    elif material_type == nmv.enums.Shader.GLOSSY_BUMPY:
        return create_glossy_illumination(location=location)

    # Glossy
    elif material_type == nmv.enums.Shader.GLOSSY:
        return create_glossy_illumination(location=location)

    elif material_type == nmv.enums.Shader.GLOSSY_BUMPY:
        return create_glossy_bumpy_illumination(location=location)

    # Default, just use the lambert shader illumination
    else:
        return create_lambert_ward_illumination(location=location)
