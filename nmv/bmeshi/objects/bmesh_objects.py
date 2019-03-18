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
import bmesh

# Internal imports
import nmv
import nmv.utilities


####################################################################################################
# @create_vertex
####################################################################################################
def create_vertex(location=(0, 0, 0)):
    """Creates a bmhes vertex.

    :param location:
        The location of the vertex.
    :return:
        A reference to the bmesh vertex.
    """

    # Create a new bmesh object
    bmesh_vertex = bmesh.new()

    # Create a new vertex
    bmesh.ops.create_vert(bmesh_vertex, co=location)

    # Return a reference to the bmesh
    return bmesh_vertex


####################################################################################################
# @create_uv_sphere
####################################################################################################
def create_uv_sphere(radius=1,
                     location=(0, 0, 0),
                     subdivisions=10):
    """Create a uv sphere bmesh object and returns a reference to that object.

    :param radius:
        The radius of the sphere.
    :param location:
        The location of the sphere, by default the origin.
    :param subdivisions:
        The number of the subdivisions of the sphere, by default 1.
    :return:
        A reference to the created ico-sphere.
    """

    # Create a new bmesh object
    bmesh_uv_sphere = bmesh.new()

    # Create a uv-sphere
    bmesh.ops.create_uvsphere(
        bmesh_uv_sphere, u_segments=subdivisions, v_segments=subdivisions, diameter=radius)
    # bmesh.ops.create_icosphere(bmesh_uv_sphere, subdivisions=subdivisions, diameter=radius)

    # Translate it to the specified position
    bmesh.ops.translate(bmesh_uv_sphere, verts=bmesh_uv_sphere.verts[:], vec=location)

    # Return a reference to the bmesh
    return bmesh_uv_sphere


####################################################################################################
# @create_ico_sphere
####################################################################################################
def create_ico_sphere(radius=1,
                      location=(0, 0, 0),
                      subdivisions=1):
    """Create an ico-sphere bmesh object and returns a reference to that object.

    :param radius:
        The radius of the sphere.
    :param location:
        The location of the sphere, by default the origin.
    :param subdivisions:
        The number of the subdivisions of the sphere, by default 1.
    :return:
        A reference to the created ico-sphere.
    """

    # Create a new bmesh object
    bmesh_ico_sphere = bmesh.new()

    # Create an ico-sphere
    bmesh.ops.create_icosphere(bmesh_ico_sphere, subdivisions=subdivisions, diameter=radius)

    # Translate it to the specified position
    bmesh.ops.translate(bmesh_ico_sphere, verts=bmesh_ico_sphere.verts[:], vec=location)

    # Return a reference to the bmesh
    return bmesh_ico_sphere


####################################################################################################
# @create_circle
####################################################################################################
def create_circle(radius=1,
                  location=(0, 0, 0),
                  vertices=4,
                  caps=True):
    """Create a circle bmesh object and returns a reference to that object.

    :param radius:
        The radius of the circle.
    :param location:
        The location of the circle, by default the origin.
    :param vertices:
        Number of vertices composing the circle, by default 4.
    :param caps:
        If the caps option is set to True, the circle will be covered.
    :return:
        A reference to the circle.
    """

    # Create a new bmesh object
    bmesh_circle = bmesh.new()

    # Get the version of the running Blender [MAJOR, MINOR, PATCH]
    blender_version = nmv.utilities.get_blender_version()

    # NOTE: Previous versions of blender were mistaken for the argument diameter
    if int(blender_version[0]) >= 2 and int(blender_version[1]) > 78:

        # Create a circle
        bmesh.ops.create_circle(bmesh_circle, cap_ends=caps, diameter=radius, segments=vertices)

    else:

        # Create a circle
        bmesh.ops.create_circle(bmesh_circle, cap_ends=caps, diameter=radius, segments=vertices)

    # Translate it to the specified position
    bmesh.ops.translate(bmesh_circle, verts=bmesh_circle.verts[:], vec=location)

    # Return a reference to the bmesh
    return bmesh_circle


####################################################################################################
# @create_bmesh_cube
####################################################################################################
def create_cube(radius=1,
                location=(0, 0, 0)):
    """Create a cube bmesh object and returns a reference to that object.

    :param radius:
        The radius (diagonal) of the cube.
    :param location:
        The location of the cube, by default the origin.
    :return:
        A reference to the cube.
    """

    # Create a new bmesh object
    bmesh_cube = bmesh.new()

    # Create a cube
    bmesh.ops.create_cube(bmesh_cube, size=radius)

    # Translate it to the specified position.
    bmesh.ops.translate(bmesh_cube, verts=bmesh_cube.verts[:], vec=location)

    # Return a reference to the bmesh
    return bmesh_cube
