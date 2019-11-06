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

# System imports
import os


####################################################################################################
# @_version_
####################################################################################################
def get_nmv_version():
    """Get NeuroMorphoVis version.

    :return:
        NeuroMorphoVis version tuple.
    """

    # Load the version from the version file
    version_file_path = '%s/../../__init__.py' % os.path.dirname(os.path.realpath(__file__))
    version_file = open(version_file_path, 'r')
    version_string = ''
    for line in version_file:
        if '"version":' in line:
            string = line.split('\"version\": (')[1].split(')')[0].split(', ')
            version_string = '%d.%d.%d' % (int(string[0]), int(string[1]), int(string[2]))
            break
    version_file.close()
    return version_string


####################################################################################################
# @get_blender_version
####################################################################################################
def get_blender_version():
    """Get Blender version.

    :return:
        A list of the version of the running Blender.
    """

    import bpy
    return bpy.app.version


####################################################################################################
# @get_blender_version_string
####################################################################################################
def get_blender_version_string():
    """Gets Blender version as a string.

    :return:
        A string of the version of the running Blender.
    """

    # Get the version list
    version = get_blender_version()

    # Return the version as a string
    return '%s_%s_%s' % (str(version[0]), str(version[1]), str(version[2]))


####################################################################################################
# @is_blender_280
####################################################################################################
def is_blender_280():
    """Checks if the used version of Blender is greater than 2.8 or not.

    :return:
        True if this version of Blender is 2.8, otherwise False.
    """

    if get_blender_version() >= (2, 80, 0):
        return True
    return False
