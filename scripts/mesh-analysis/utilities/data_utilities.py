####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Internal imports
import nmv.enums


####################################################################################################
# @get_view
####################################################################################################
def get_view(arg):
    """Gets the correct camera from the input arguments.

    :param arg:
        Input arguments.
    :return:
        Camera view.
    """

    if 'side' in arg:
        return nmv.enums.Camera.View.SIDE
    elif 'top' in arg:
        return nmv.enums.Camera.View.TOP
    else:
        return nmv.enums.Camera.View.FRONT


####################################################################################################
# @verify_plotting_packages
####################################################################################################
def verify_plotting_packages():
    """Verifies that all the plotting packages are installed. Otherwise, install the missing one.
    """

    # Import the fonts
    font_dirs = [os.path.dirname(os.path.realpath(__file__)) + '/fonts/']
    font_dirs .extend([os.path.dirname(os.path.realpath(__file__)) + '/../fonts/'])
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
# @get_super
####################################################################################################
def get_super(x):

    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)


####################################################################################################
# @format_number_to_power_string
####################################################################################################
def format_number_to_power_string(number):
    """Formats the string to make it readable.

    :param number:
        Input number.
    :return:
        Corresponding string.
    """

    if float(number) < 1e3:
        return '%2.2f' % number
    elif (float(number) > 1e3) and (float(number) < 1e6):
        value = float(number) / float(1e3)
        return '%2.2f x10%s' % (value, get_super('3'))
    elif (float(number) > 1e6) and (float(number) < 1e9):
        value = float(number) / float(1e6)
        return '%2.2f x10%s' % (value, get_super('6'))
    elif (float(number) > 1e9) and (float(number) < 1e12):
        value = float(number) / float(1e9)
        return "%2.2f x10%s" % (value, get_super('9'))
    else:
        value = float(number) / float(1e12)
        return '%2.2f x10%s' % (value, get_super('12'))


####################################################################################################
# @convert_color
####################################################################################################
def convert_color(palette_color):
    """Converts a given paletter color from Matplotlib into an RGB tuple color used by Blender.

    :param palette_color:
    :return:
    """

    return (int(palette_color[0] * 255), int(palette_color[1] * 255), int(palette_color[2] * 255))
