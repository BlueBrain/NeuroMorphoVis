####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
import sys
import subprocess


####################################################################################################
# @_version_
####################################################################################################
def install_dependen():
    """Gets NeuroMorphoVis version.

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
            version = (int(string[0]), int(string[1]), int(string[2]))
            break
    version_file.close()
    return version


####################################################################################################
# @get_python_executable
####################################################################################################
def get_python_executable():
    """Returns the python path of this specific version of blender.

    :return:
        The python path of this specific version of blender.
    """

    # Return the python executable
    return '%s/bin/python3.7m' % sys.prefix


####################################################################################################
# @get_python_executable
####################################################################################################
def install_pip():

    # The python executable
    python_executable = get_python_executable()

    # Get pip
    get_pip_script = '%s/get_pip.py' % os.path.dirname(os.path.realpath(__file__))

    # Command
    shell_command = '%s %s' % (python_executable, get_pip_script)
    print('INSTALL: %s' % shell_command)
    subprocess.call(shell_command, shell=True)

    # Return the pip executable
    return '%s/bin/pip' % sys.prefix


####################################################################################################
# @pip_wheel
####################################################################################################
def pip_wheel(package_name):

    # Get the pip executable
    pip_executable = install_pip()

    # Command
    shell_command = '%s install %s --force-reinstall' % (pip_executable,
                                                                            package_name)
    print('INSTALL: %s' % shell_command)
    subprocess.call(shell_command, shell=True)
