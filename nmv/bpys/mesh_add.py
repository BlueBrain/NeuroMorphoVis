####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# NeuroMorphoVis imports    
import nmv.consts
import nmv.utilities


####################################################################################################
# @add_plane_mesh
####################################################################################################
def add_plane_mesh(size=1.0,
                   location=nmv.consts.Math.ORIGIN):
    """Add a plane mesh to the scene.
    :param size:
        The size of the plane, by default it is 1.0.
    :param location:
        The location of the plane, by default it is at the origin.
    """

    bpy.ops.mesh.primitive_plane_add(size=size, location=location)


####################################################################################################
# @add_ico_sphere_mesh
####################################################################################################
def add_ico_sphere_mesh(radius=1.0,
                        location=nmv.consts.Math.ORIGIN,
                        subdivisions=2):
    """Add an icosphere mesh to the scene.
    :param radius:
        The radius of the icosphere, by default it is 1.0.
    :param location:
        The location of the icosphere, by default it is at the origin.
    :param subdivisions:
        The number of subdivisions of the icosphere, by default it is 2.
    """

    bpy.ops.mesh.primitive_ico_sphere_add(radius=radius,
                                          location=location,
                                          subdivisions=subdivisions)

####################################################################################################
# @add_uv_sphere_mesh
####################################################################################################
def add_uv_sphere_mesh(radius=1.0,
                       location=nmv.consts.Math.ORIGIN,
                       segments=16,
                       ring_count=16):
    """Add a UV sphere mesh to the scene.
    :param radius:
        The radius of the UV sphere, by default it is 1.0.
    :param location:
        The location of the UV sphere, by default it is at the origin.
    :param segments:
        The number of segments of the UV sphere, by default it is 16.
    :param ring_count:
        The number of rings of the UV sphere, by default it is 16.
    """

    if nmv.utilities.is_blender_280():
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=segments, ring_count=ring_count, radius=radius, location=location)
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=segments, ring_count=ring_count, size=radius, location=location)


####################################################################################################
# @add_circle_mesh
####################################################################################################
def add_circle_mesh(radius=1.0,
                    location=nmv.consts.Math.ORIGIN,
                    vertices=8,
                    caps=False):
    """Add a circle mesh to the scene.
    :param radius:
        The radius of the circle, by default it is 1.0.
    :param location:
        The location of the circle, by default it is at the origin.
    :param vertices:
        The number of vertices of the circle, by default it is 8.
    :param caps:
        Whether to add caps to the circle, by default it is False.
    """

    bpy.ops.mesh.primitive_circle_add(
        vertices=vertices, radius=radius, location=location,
        fill_type='NGON' if caps else 'NOTHING')


####################################################################################################
# @add_cube_mesh
####################################################################################################
def add_cube_mesh(size=1.0,
                  location=nmv.consts.Math.ORIGIN):
    """Add a cube mesh to the scene.
    :param size:
        The size of the cube, by default it is 1.0.
    :param location:
        The location of the cube, by default it is at the origin.
    """

    bpy.ops.mesh.primitive_cube_add(size=size, location=location)

