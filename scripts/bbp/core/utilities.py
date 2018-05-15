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

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# imports
import math


################################################################################
# @get_minimum_and_maximum_radii
################################################################################
def get_minimum_and_maximum_radii(profile_points):
    """Get the minimum and maximum radii for a cell based on their profile points.

    :param profile_points:
        Morphology soma profile points.
    :return:
        Minimum and maximum radii of the neuron.
    """

    min_radius = 1e32
    max_radius = -1e32
    for profile_point in profile_points:
        x = profile_point[0]
        y = profile_point[1]
        z = profile_point[2]
        radius = math.sqrt(x * x + y * y + z * z)
        if radius < min_radius: min_radius = radius
        if radius > max_radius: max_radius = radius
    return min_radius, max_radius