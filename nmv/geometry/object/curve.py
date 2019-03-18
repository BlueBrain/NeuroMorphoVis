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
from mathutils import Vector, Matrix

# Internal imports
import nmv
import nmv.scene


####################################################################################################
# @draw_cyclic_curve_from_points
####################################################################################################
def draw_cyclic_curve_from_points(curve_name,
                                  list_points):
    """Draw a cyclic poly curve form a list of points.

    :param curve_name:
        The name of the curve.
    :param list_points:
        A list of points to draw the curve from.
    :return:
        A reference to the drawn curve.
    """

    # Create the curve data
    curve_data = bpy.data.curves.new(name="c_%s" % curve_name, type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.fill_mode = 'FULL'
    curve_data.bevel_depth = 0.25
    line_material = bpy.data.materials.new('color')
    line_material.diffuse_color = (1, 1, 0.1)
    curve_data.materials.append(line_material)

    # Create an object to the curve and link it to the scene
    curve_object = bpy.data.objects.new("o_%s" % curve_name, curve_data)
    curve_object.location = (0, 0, 0)
    bpy.context.scene.objects.link(curve_object)

    curve = curve_data.splines.new('POLY')
    curve.points.add(len(list_points) - 1)
    for i in range(len(list_points)):
        vector = list_points[i]
        curve.points[i].co = ((vector[0], vector[1], vector[2])) + (1,)

    curve.order_u = len(curve.points) - 1
    curve.use_cyclic_u = True

    # Return a reference to the created curve object
    return curve


####################################################################################################
# @draw_closed_circle
####################################################################################################
def draw_closed_circle(radius=1,
                       location=Vector((0, 0, 0)),
                       vertices=4,
                       name='circle',
                       caps=True):
    """Create a local circle that doesn't account for the transformations applied on it.

    :param radius:
        The radius of the circle.
    :param location:
        The location of the circle.
    :param vertices:
        The number of vertices used to construct the sides of the circle.
    :param name:
        The name of the circle.
    :param caps:
        A flag to indicate whether to close the caps of the circle or not.
    :return:
        A reference to the circle object.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Fill the circle
    fill = 'NGON' if caps else 'NOTHING'
    bpy.ops.mesh.primitive_circle_add(
        vertices=vertices, radius=radius/2, location=location, fill_type=fill)

    # Return a reference to the circle objects
    circle = bpy.context.scene.objects.active

    # Rename the circle
    circle.name = name

    # Return a reference to the created circle.
    return circle