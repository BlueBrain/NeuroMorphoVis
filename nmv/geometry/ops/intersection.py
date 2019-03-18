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

# System imports
import math

# Blender imports
from mathutils import Vector, Matrix


####################################################################################################
# @sphere_line
####################################################################################################
def sphere_point(sphere_center,
                 sphere_radius,
                 point):
    """
    Checks if a sphere intersects a point or not by verifying if the point is located inside the
    sphere or not.

    :param sphere_center: The center of the sphere.
    :param sphere_radius: The radius of the sphere.
    :param point: The coordinates of the point.
    :return: True or False.
    """
    distance = (sphere_center - point).length
    if distance < sphere_radius:
        return True
    return False


####################################################################################################
# @sphere_line
####################################################################################################
def sphere_line(sphere_center,
                sphere_radius,
                point_1,
                point_2):
    """
    Checks if sphere intersects with a line or not.

    :param sphere_center: The center of the sphere.
    :param sphere_radius: The radius of the sphere.
    :param point_1: P1 of the line.
    :param point_2: P2 of the line.
    :return: True or False
    """
    difference = (point_2 - point_1)
    a = difference.dot(difference.normalized())
    b = 2.0 * difference.dot(point_1 - sphere_center)
    c = sphere_center.dot(sphere_center) + \
        point_1.dot(point_1) - 2.0 * sphere_center.dot(point_1) - \
        sphere_radius * sphere_radius
    root = (b * b) - (4 * a * c)
    if root < 0.0:
        return False

    # Check if the distances is before or after the two points
    d1 = -b + math.sqrt(root); d2 = -b - math.sqrt(root)
    if (d1 < 0.0 or d1 > difference.length) and \
        (d2 < 0.0 or d2 > difference.length):
        return False

    # Otherwise, an intersection exists
    return True
    
