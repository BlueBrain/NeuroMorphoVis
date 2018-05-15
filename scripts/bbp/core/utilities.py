"""
morphology_utils.py:
    A set of utilities for handling morphologies and their data.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
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