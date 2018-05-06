"""
utilities.py:
    Generic utilities for managing the python code.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# System imports
import sys

# Blender imports
import bpy
from mathutils import Vector


####################################################################################################
# @get_blender_version
####################################################################################################
def get_blender_version():
    """
    Gets the version of the running Blender.
    :return: A list of the version of the running Blender.
    """

    return bpy.app.version


####################################################################################################
# @get_blender_version_string
####################################################################################################
def get_blender_version_string():
    """
    Gets the version of the running Blender.
    :return: A string of the version of the running Blender.
    """

    # Get the version list
    version = get_blender_version()

    # Return the version as a string
    return '%s_%s_%s' % (str(version[0]), str(version[1]), str(version[2]))


####################################################################################################
# @disable_std_output
####################################################################################################
def disable_std_output():
    """
    Ignores the output from verbose function to make the output more clear to read.

    :return: A hook for stdout.
    """

    # hooks the stdout until further notice
    hook = sys.stdout
    sys.stdout = open('trash.output', 'w')
    return hook


####################################################################################################
# @enable_std_output
####################################################################################################
def enable_std_output(hook=None):
    """
    Re-enable stdout again.

    :param hook: A hook for std.
    """

    if hook is None:
        return
    else:
        sys.stdout = hook


####################################################################################################
# @parse_color_from_argument
####################################################################################################
def parse_color_from_argument(color_argument):
    """
    Gets the RGB values from the color arguments. This function is compatible with an RGB color
    format with 0-255 or 0.0-0.1 representations.

    :param color_argument: A given color argument.
    :return: A vector having RGB color components.
    """

    # Split the string
    rgb_values = color_argument.split('_')

    # Get the RGB values
    r = float(rgb_values[0])
    g = float(rgb_values[1])
    b = float(rgb_values[2])

    # Verify the values whether in 0-255 range or in 0.0-1.0 range
    if r > 255: r = 255
    if r < 0: r = 0
    if g > 255: g = 255
    if g < 0: g = 0
    if b > 255: b = 255
    if b < 0: b = 0

    # RGB colors (normalized)
    if r > 1.0: r /= 256.0
    if g > 1.0: g /= 256.0
    if b > 1.0: b /= 256.0

    # Build the RGB color vector
    rgb_color = Vector((r, g, b))

    # Return the RGB color
    return rgb_color
