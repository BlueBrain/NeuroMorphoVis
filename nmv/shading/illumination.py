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
    """

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

    nmv.scene.ops.clear_lights()

    # deselect all
    nmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [(0.000, 3.140, 0.000),
                      (-1.57, 0.000, 0.000),
                      (0.000, -1.57, 0.000)]

    # Add the light sources
    for i, angle in enumerate(light_rotation):
        lamp_data = bpy.data.lamps.new(name='HemiLamp%d' % i, type='HEMI')
        lamp_object = bpy.data.objects.new(name='HemiLamp%d' % i, object_data=lamp_data)
        bpy.context.scene.objects.link(lamp_object)
        lamp_object.rotation_euler = angle
        bpy.data.lamps['HemiLamp%d' % i].use_nodes = True
        bpy.data.lamps['HemiLamp%d' % i].node_tree.nodes["Emission"].inputs[1].default_value = 10


####################################################################################################
# @create_voronoi_cells_illumination
####################################################################################################
def create_voronoi_cells_illumination():
    """

    :param name:
    :return:
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # If no light sources in the scene, then create two sources one towards the top and the
    # other one towards the bottom
    if not nmv.scene.ops.is_object_in_scene_by_name('DefaultLamp'):
        nmv.scene.ops.deselect_all()

        light_rotation = [(0.000, 0.000, 0.000),
                          (0.000, 3.140, 0.000),
                          (1.570, 0.000, 0.000),
                          (-1.57, 0.000, 0.000),
                          (0.000, 1.570, 0.000),
                          (0.000, -1.57, 0.000)]

        for i, angle in enumerate(light_rotation):
            bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            bpy.data.lamps['Lamp%d' % i].node_tree.nodes["Emission"].inputs[1].default_value = 2.5


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
    elif material_type == nmv.enums.Shading.VORONOI:
        return create_voronoi_cells_illumination()

    # Default, just use the lambert shader illumination
    else:
        return create_lambert_ward_illumination()
