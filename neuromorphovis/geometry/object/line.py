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


####################################################################################################
# @create_line_object_from_data
####################################################################################################
def create_line_object_from_data(data,
                                 point1,
                                 point2,
                                 name='line'):
    """Create a line object and returns a reference to it.

    :param data:
        Properties of the line such as caps, depth, dimensions, ect... .
    :param point1:
        Starting point of the line.
    :param point2:
        End point of the line.
    :param name:
        The name of the line object.
    :return:
        A reference to the created line object.
    """

    # Create a line object and link it to the scene
    line_object = bpy.data.objects.new(str(name), data)
    bpy.context.scene.objects.link(line_object)

    # Add the two points to the line object
    # NOTE: Once the strip is created, it contains by default a single point, so we need to add
    # another point to make an array fr two points
    line_strip = data.splines.new('NURBS')
    line_strip.points.add(1)

    # Add the coordinates of the two points
    line_strip.points[0].co = (point1[0], point1[1], point1[2]) + (1.0,)
    line_strip.points[1].co = (point2[0], point2[1], point2[2]) + (1.0,)
    line_strip.order_u = 1

    # Return a reference to the line object
    return line_object
