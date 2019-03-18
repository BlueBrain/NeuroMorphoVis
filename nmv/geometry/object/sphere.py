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

# Blender imports
import bpy

# Internal imports
import nmv
import nmv.shading
import nmv.scene


####################################################################################################
# @create_uv_sphere
####################################################################################################
def create_uv_sphere(radius=1, 
                     location=(0, 0, 0), 
                     subdivisions=32, 
                     name='uv_sphere',
                     color=None):
    """Create a UV sphere and returns a reference to it.

    :param radius:
        Sphere radius.
    :param location:
        Sphere location.
    :param subdivisions:
        Number of sphere subdivisions, 32 by default.
    :param name:
        Sphere name.
    :param color:
        Sphere color.
    :return:
        A reference to the created uv-sphere object.
    """

    # Deselect all objects
    nmv.scene.ops.deselect_all()
    
    # Add the sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=subdivisions, size=radius, location=location)
    
    # Select the sphere to set its name and returns a reference to it
    sphere = bpy.context.scene.objects.active

    # Update the sphere name
    sphere.name = name

    # Smoothing via shade smoothing
    nmv.scene.ops.deselect_all()
    nmv.scene.ops.select_object_by_name(sphere)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.object.editmode_toggle()

    # Create a material and assign it to the sphere
    if color is not None:
        sphere_material = nmv.shading.create_lambert_ward_material(name='sphere_color', color=color)
        nmv.shading.set_material_to_object(sphere, sphere_material)

    # Return a reference to the created sphere object
    return sphere


####################################################################################################
# @create_ico_sphere
####################################################################################################
def create_ico_sphere(radius=1, 
                      location=(0, 0, 0), 
                      subdivisions=3, 
                      name='ico_sphere'):
    """Create a default ico-sphere and returns a reference to it.

    :param radius:
        Sphere radius.
    :param location:
        Sphere location.
    :param subdivisions:
        Number of sphere subdivisions, 3 by default.
    :param name:
        Sphere name.
    :return:
        A reference to the created ico-sphere object.
    """

    # Deselect all objects
    nmv.scene.ops.deselect_all()
    
    # Add the sphere
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, size=radius, location=location)
    
    # Select the sphere to set its name and returns a reference to it
    sphere = bpy.context.scene.objects.active

    # Update the sphere name
    sphere.name = name

    # Smoothing via shade smoothing
    nmv.scene.ops.deselect_all()
    nmv.scene.ops.select_object_by_name(sphere)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.object.editmode_toggle()

    # Return a reference to the sphere
    return sphere

