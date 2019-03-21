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


# Blender imports
import bpy

# Internal imports
import nmv
import nmv.consts
import nmv.enums
import nmv.scene


####################################################################################################
# @create_lambert_ward_illumination
####################################################################################################
def create_lambert_ward_illumination():

    # If no light sources in the scene, then create two sources one towards the top and the
    # other one towards the bottom
    if not nmv.scene.ops.is_object_in_scene_by_name('DefaultLamp'):
        nmv.scene.ops.deselect_all()

        # Lamp 1
        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'Lamp1'
        lamp_reference.data.name = "Lamp1"
        lamp_reference.location = (0, 0, 0)
        lamp_reference.rotation_euler = (0, 0, 0)
        lamp_reference.data.energy = 0.5

        # Lamp 2
        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'Lamp2'
        lamp_reference.data.name = "Lamp2"
        lamp_reference.location = (0, 0, 0)
        lamp_reference.rotation_euler = (0, 3.14159, 0)
        lamp_reference.data.energy = 0.5

        # Lamp 3
        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'Lamp3'
        lamp_reference.data.name = "Lamp3"
        lamp_reference.location = (0, 0, 0)
        lamp_reference.rotation_euler = (1.5708, 0, 0)
        lamp_reference.data.energy = 0.5

        # Lamp 4
        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'Lamp4'
        lamp_reference.data.name = "Lamp4"
        lamp_reference.location = (0, 0, 0)
        lamp_reference.rotation_euler = (-1.5708, 0, 0)
        lamp_reference.data.energy = 0.5

    return


####################################################################################################
# @create_shadow_illumination
####################################################################################################
def create_shadow_illumination():

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
# @create_glossy_bumpy_illumination
####################################################################################################
def create_glossy_bumpy_illumination():

    bpy.ops.object.lamp_add(type='HEMI', location=(0, 0, 0))
    lamp_reference = bpy.context.object
    lamp_reference.name = 'DefaultLamp'
    lamp_reference.data.name = "DefaultLamp"
    lamp_reference.location[0] = 0
    lamp_reference.location[1] = 5
    lamp_reference.location[2] = 0
    lamp_reference.rotation_euler[0] = -1.5708


####################################################################################################
# @create_voroni_cells_illumination
####################################################################################################
def create_voroni_cells_illumination():
    """

    :param name:
    :return:
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Lamp up
    bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
    lamp_reference = bpy.context.object
    lamp_reference.name = 'LampUp'
    lamp_reference.data.name = "LampUp"
    lamp_reference.location[0] = 0
    lamp_reference.location[1] = 0
    lamp_reference.location[2] = 0
    lamp_reference.rotation_euler[0] = 1.5708
    bpy.data.lamps['LampUp'].node_tree.nodes["Emission"].inputs[1].default_value = 2.5

    # Lamp down
    nmv.scene.ops.deselect_all()
    bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
    lamp_reference = bpy.context.object
    lamp_reference.name = 'LampDown'
    lamp_reference.data.name = "LampDown"
    lamp_reference.location[0] = 0
    lamp_reference.location[1] = 0
    lamp_reference.location[2] = 0
    lamp_reference.rotation_euler[0] = -1.5708
    bpy.data.lamps['LampDown'].node_tree.nodes["Emission"].inputs[1].default_value = 2.5


####################################################################################################
# @create_illumination
####################################################################################################
def create_material_specific_illumination(material_type):
    """Create a specific illumination that corresponds to a given material.

    :param material_type:
        Material type.
    """

    # Lambert Ward
    if material_type == nmv.enums.Shading.LAMBERT_WARD:
        return create_lambert_ward_illumination()

    # Shadow
    elif material_type == nmv.enums.Shading.SHADOW:
        return create_shadow_illumination()

    # Glossy bumpy
    elif material_type == nmv.enums.Shading.GLOSSY_BUMPY:
        return create_glossy_bumpy_illumination()

    # Voroni
    elif material_type == nmv.enums.Shading.VORONI:
        return create_voroni_cells_illumination()

    # Default, do not create any illumination
    else:
        pass
