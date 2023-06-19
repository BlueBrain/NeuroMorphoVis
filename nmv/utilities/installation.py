####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import sys
import subprocess

# Internal imports
import nmv.utilities
import nmv.consts


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
# @pip_install_wheel
####################################################################################################
def pip_install_wheel(package_name):
    """Installs a package.

    :param package_name:
        The name of the pip package.
    """

    # Get the pip executable
    pip_executable = install_pip()

    # Command
    shell_command = '%s install %s --force-reinstall' % (pip_executable, package_name)
    print('INSTALL: %s' % shell_command)
    subprocess.call(shell_command, shell=True)


####################################################################################################
# @pip_install_wheel
####################################################################################################
def pip_uninstall_wheel(package_name):
    """Uninstalls a package.

    :param package_name:
        The name of the pip package to be removed.
    """

    # Get the pip executable
    pip_executable = install_pip()

    # Command
    shell_command = '%s uninstall %s' % (pip_executable, package_name)
    print('INSTALL: %s' % shell_command)
    subprocess.call(shell_command, shell=True)


####################################################################################################
# @verify_plotting_packages
####################################################################################################
def verify_plotting_packages():
    """Verifies that all the plotting packages are installed. Otherwise, install the missing one.
    """

    # Installing dependencies
    try:
        import numpy
    except ImportError:
        print('Package *numpy* is not installed. Installing it.')
        pip_install_wheel(package_name='numpy')

    try:
        import matplotlib
    except ImportError:
        print('Package *matplotlib* is not installed. Installing it.')
        pip_install_wheel(package_name='matplotlib')

    try:
        import seaborn
    except ImportError:
        print('Package *seaborn* is not installed. Installing it.')
        pip_install_wheel(package_name='seaborn')

    try:
        import pandas
    except ImportError:
        print('Package *pandas* is not installed. Installing it.')
        pip_install_wheel(package_name='pandas')

    import matplotlib
    matplotlib.use('agg')  # To resolve the tkinter issue
    from matplotlib import font_manager

    # Import the fonts
    font_dirs = [nmv.consts.Paths.FONTS_DIRECTORY]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    if nmv.utilities.is_blender_280():
        for font_file in font_files:
            font_manager.fontManager.addfont(font_file)
    else:
        font_list = font_manager.createFontList(font_files)
        font_manager.fontManager.ttflist.extend(font_list)

