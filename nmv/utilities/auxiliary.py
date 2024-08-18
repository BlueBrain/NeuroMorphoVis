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

# System imports
import math
import random
import string

# Internal imports
import nmv.consts


####################################################################################################
# @get_index
####################################################################################################
def get_index(value,
              minimum_value,
              maximum_value,
              number_steps):
    """Gets an index for a given value that exists between and minimum and maximum values on scale.
    If the value does not exist between the given minimum and maximum values, the returned
    index will be [-1].

    :param value:
        A given value between the minimum and maximum values.
    :param minimum_value:
        The minimum value of the scale.
    :param maximum_value:
        The maximum value of the scale.
    :param number_steps:
        The number of steps with which the scale between the minimum and maximum values will
        be divided.
    :return:
        The index of the colormap.
    """

    if value < minimum_value:
        return nmv.consts.Math.INDEX_OUT_OF_RANGE

    if value > maximum_value:
        return nmv.consts.Math.INDEX_OUT_OF_RANGE

    # Compute the difference between the minimum and maximum values
    difference = maximum_value - minimum_value

    # Get the delta
    delta = (1.0 * difference) / number_steps

    # Return The index of the color map
    return math.ceil((value - minimum_value) / (1.0 * delta)) - 1


####################################################################################################
# @generate_random_string
####################################################################################################
def generate_random_string(length):
    """Generates and returns a random string with a specific length.

    :param length:
        The length of the string.
    :return:
        A randomly created string with specified length.
    """

    # Create a return the random string
    resulting_string = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    return resulting_string
