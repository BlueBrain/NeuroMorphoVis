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

# Blender modules
import bpy

# Internal modules
import nmv
import nmv.scene


####################################################################################################
# @create_plane
####################################################################################################
def create_plane(radius=1,
                 location=(0, 0, 0),
                 name='plane'):
    """Create a plane mesh object that is linked to the scene and returns a reference to it.

    :param radius:
        The radius of the plane.
    :param location:
        The location of the plane.
    :param name:
        The name of the created object.
    :return:
        A reference to the created plane.
    """

    # Deselect all objects in the scene
    nmv.scene.ops.deselect_all()

    # Add new plane mesh object
    bpy.ops.mesh.primitive_plane_add(radius=radius, location=location)

    # Get a reference to it, from the current active objects
    plane_mesh = bpy.context.scene.objects.active

    # Rename it
    plane_mesh.name = name

    # Return a reference to it
    return plane_mesh


####################################################################################################
# @create_ico_sphere
####################################################################################################
def create_ico_sphere(radius=1,
                      location=(0, 0, 0),
                      subdivisions=1,
                      name='ico_sphere'):
    """Create an ico-sphere mesh object that is linked to the scene and returns a reference to it.

    :param radius:
        The radius of the ico-sphere, by default 1.
    :param location:
        The XYZ-coordinates of the center of the ico-sphere, by default the origin.
    :param subdivisions:
        Number of subdivisions of the ico-sphere, by default 1.
    :param name:
        The name of the sphere, by default 'ico_sphere'.
    :return:
        A reference to the created sphere.
    """

    # Deselect all objects in the scene
    nmv.scene.ops.deselect_all()

    # Add new ico-sphere mesh object
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, size=radius, location=location)

    # Get a reference to it, from the current active objects
    ico_sphere_mesh = bpy.context.scene.objects.active

    # Rename it
    ico_sphere_mesh.name = name

    # Return a reference to it
    return ico_sphere_mesh


####################################################################################################
# @create_uv_sphere
####################################################################################################
def create_uv_sphere(radius=1,
                     location=(0, 0, 0),
                     subdivisions=32,
                     name='uv_sphere'):
    """Create a default UV sphere linked to the scene and return a reference to it.

    :param radius:
        The radius of the uv-sphere, by default 1.
    :param location:
        The XYZ-coordinates of the center of the uv-sphere, by default the origin.
    :param subdivisions:
        Number of subdivisions of the uv-sphere, by default 32.
    :param name:
        The name of the sphere, by default 'uv_sphere'.
    :return:
        A reference to the created sphere.
    """

    # Deselect all objects in the scene
    nmv.scene.ops.deselect_all()

    # Add a new sphere
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=subdivisions, ring_count=16, size=radius, location=location)

    # Get a reference to it
    sphere_mesh = bpy.context.scene.objects.active

    # Rename it
    sphere_mesh.name = name

    # Return a reference to it
    return sphere_mesh


####################################################################################################
# @create_circle
####################################################################################################
def create_circle(radius=1,
                  location=(0, 0, 0),
                  vertices=4,
                  caps=True,
                  name='circle'):
    """Create a circle mesh object that is linked to the scene and return a reference to it.

    :param radius:
        The radius of the circle, by default 1.
    :param location:
        The XYZ-coordinates of the center of the circle, by default the origin.
    :param vertices:
        Number of vertices composing the circle, by default 4.
    :param caps:
        An option to add a cap to the circle, mainly for extrusion, by default True.
    :param name:
        The name of the circle, by default 'circle'.
    :return:
        A reference to the created circle.
    """

    # Deselect all objects in the scene
    nmv.scene.ops.deselect_all()

    # Check if the circle will be filled with a face or not
    fill = 'NGON' if caps else 'NOTHING'

    # Add the circle
    bpy.ops.mesh.primitive_circle_add(
        vertices=vertices, radius=radius, location=location, fill_type=fill)

    # Get a reference to it
    circle_mesh = bpy.context.scene.objects.active

    # Rename it
    circle_mesh.name = name

    # Return a reference to it
    return circle_mesh


####################################################################################################
# @create_bezier_circle
####################################################################################################
def create_bezier_circle(radius=1,
                         vertices=4,
                         location=(0, 0, 0),
                         name='bezier_circle'):
    """Create a BEZIER circle mesh object that is linked to the scene and return a reference to it.

    :param radius:
        The radius of the circle.
    :param vertices:
        Number of vertices composing the circle, by default 4.
    :param location:
        The XYZ-coordinates of the center of the circle, by default the origin.
    :param name:
        The name of the circle.
    :return:
        A reference to the circle.
    """

    # Deselect all objects in the scene
    nmv.scene.ops.deselect_all()

    # Add the circle
    bpy.ops.curve.primitive_bezier_circle_add(location=location)

    # Get a reference to it
    bpy.context.object.data.resolution_u = vertices / 4
    circle_mesh = bpy.context.scene.objects.active

    # Set the radius
    circle_mesh.scale[0] = radius
    circle_mesh.scale[1] = radius
    circle_mesh.scale[2] = radius

    # Rename it
    circle_mesh.name = name

    # Return a reference to it
    return circle_mesh


####################################################################################################
# @create_cube
####################################################################################################
def create_cube(radius=1,
                location=(0, 0, 0),
                name='cube'):
    """Create a cube mesh object that is linked to the scene and returns a reference to it.

    :param radius: T
        he radius 'diagonal length' of the cube, by default 1.
    :param location:
        The XYZ-coordinate of the center of the cube, by default origin.
    :param name:
        The name of the cube, by default 'cube'.
    :return:
        A reference to the cube.
    """

    # Deselect all objects in the scene
    nmv.scene.ops.deselect_all()

    # Add the cube
    bpy.ops.mesh.primitive_cube_add(radius=radius, location=location)

    # Get a reference to it
    cube_mesh = bpy.context.scene.objects.active

    # Rename it
    cube_mesh.name = name

    # Return a reference to it
    return cube_mesh
