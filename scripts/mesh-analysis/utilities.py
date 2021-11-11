####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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

# System imports
import os
import matplotlib.font_manager as font_manager


####################################################################################################
# @verify_plotting_packages
####################################################################################################
def verify_plotting_packages():
    """Verifies that all the plotting packages are installed. Otherwise, install the missing one.
    """

    # Import the fonts
    font_dirs = [os.path.dirname(os.path.realpath(__file__)) + '/fonts/']
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)


####################################################################################################
# @normalize_array
####################################################################################################
def normalize_array(array):
    """Normalizes an input array.

    :param array:
        The given array to be normalized.
    """

    # Gets the maximum value
    max_value = max(array)

    # Normalize
    for i in range(len(array)):
        array[i] /= max_value


####################################################################################################
# @search_for_dist
####################################################################################################
def search_for_dist(distributions,
                    keyword_1,
                    keyword_2):
    """Searchs for a specific histogram in a list of given ones with two ketwords.

    :param distributions:
        List of given distributions files.
    :param keyword_1:
        Keyword 1
    :param keyword_2:
        Keyword 2
    :return:
        If found, the file name, otherwise None.
    """

    # Search by the keywords
    for distribution in distributions:
        if keyword_1 in distribution and keyword_2 in distribution:
            return distribution

    # Otherwise, return None
    return None


####################################################################################################
# @read_dist_file
####################################################################################################
def read_dist_file(file_path,
                   invert=False):
    """Reads the distribution file into a list.

    :param file_path:
        The path to the input file.
    :param invert:
        If set to True, invert the read values.
    :return:
    """

    # Data list
    data = list()

    # Open the file
    f = open(file_path, 'r')
    for line in f:
        content = line.strip(' ').split(' ')
        value = float(content[1])
        if invert:
            value = 1.0 / value
        data.append(value)
    f.close()

    # Return a list of the data read from the file
    return data