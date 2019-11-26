#!/usr/bin/python
####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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


def download_blender(directory):

    # Server
    blender_url = 'https://download.blender.org/release/Blender2.80/'

    # Linux
    linux_32_version_url = '%s/blender-2.80rc3-linux-glibc224-i686.tar.bz2' % blender_url
    linux_64_version_url = '%s/blender-2.80rc3-linux-glibc217-x86_64.tar.bz2' % blender_url

    # Windows
    windows_32_version_url = '%s/blender-2.80rc3-windows32.zip' % blender_url
    windows_64_version_url = '%s/blender-2.80rc3-windows32.zip' % blender_url

    # Mac
    mac_osx_version_url = '%s/blender-2.80rc3-macOS.dmg' % blender_url

    shell_command = 'wget -O %s/blender.tar.bz2 %s' % (directory, linux_64_version_url)
    print(shell_command)
    subprocess.call(shell_command, shell=True)

    # Extract
    shell_command = 'tar xjfv %s/blender.tar.bz2 -C %s' % (directory, directory)
    print(shell_command)
    subprocess.call(shell_command, shell=True)


####################################################################################################
# @install_neuromorphovis
####################################################################################################
def install_for_linux(directory):

    # Blender url
    server = 'https://download.blender.org/release/Blender2.80/'
    package_name = 'blender-2.80rc3-linux-glibc217-x86_64'
    blender_url = '%s/%s.tar.bz2' % (server, package_name)

    # Wget (Download)
    shell_command = 'wget -O %s/blender.tar.bz2 %s' % (directory, blender_url)
    print(shell_command)
    subprocess.call(shell_command, shell=True)

    # Extract
    shell_command = 'tar xjfv %s/blender.tar.bz2 -C %s' % (directory, directory)
    print(shell_command)
    subprocess.call(shell_command, shell=True)

    # Moving to blender
    blender_directory = '%s/blender-neuromorphovis' % directory
    shell_command = 'mv %s/%s %s' % (directory, package_name, blender_directory)
    print(shell_command)
    if os.path.exists(blender_directory):
        os.rmdir(blender_directory)
    subprocess.call(shell_command, shell=True)

    # Clone NeuroMorphoVis into the 'addons' directory
    addons_directory = '%s/blender-neuromorphovis/2.80/scripts/addons/' % directory
    neuromorphovis_url = 'https://github.com/BlueBrain/NeuroMorphoVis.git'
    shell_command = 'git clone %s %s/neuromorphovis' % (neuromorphovis_url, addons_directory)
    print(shell_command)
    subprocess.call(shell_command, shell=True)

    # Installing dependencies
    pip_wheels = ['h5py', 'numpy', 'matplotlib', 'seaborn', 'pandas', 'Pillow']

    # Blender python
    blender_python_prefix = '%s/2.80/python/bin/' % blender_directory
    blender_python = '%s/python3.7m' % blender_python_prefix

    # Pip installation
    get_pip_script_url = 'https://bootstrap.pypa.io/get-pip.py'
    shell_command = 'wget -O %s/get-pip.py %s' % (blender_python_prefix, get_pip_script_url)
    print(shell_command)
    subprocess.call(shell_command, shell=True)

    # Activate the get-pip.py script
    get_pip_script = '%s/get-pip.py' % blender_python_prefix
    shell_command = 'chmod +x %s' % get_pip_script
    print(shell_command)
    subprocess.call(shell_command, shell=True)

    shell_command = '%s %s' % (blender_python, get_pip_script)
    print('INSTALL: %s' % shell_command)
    subprocess.call(shell_command, shell=True)

    pip_executable = '%s/pip' % blender_python_prefix

    for wheel in pip_wheels:

        # Command
        shell_command = '%s install %s' % (pip_executable, wheel)
        print('INSTALL: %s' % shell_command)
        subprocess.call(shell_command, shell=True)


####################################################################################################
# @install_neuromorphovis
####################################################################################################
def install_for_mac(directory):
    pass


####################################################################################################
# @install_neuromorphovis
####################################################################################################
def install_for_windows(directory):
    pass


####################################################################################################
# @install_neuromorphovis
####################################################################################################
def install_neuromorphovis(directory):
    """Installs NeuroMorphoVis

    :param directory:
        Installation directory.
    """

    # Linux
    if sys.platform == "linux" or sys.platform == "linux2":
        install_for_linux(directory)

    # OS X
    elif sys.platform == "darwin":
        install_for_mac(directory)

    # Windows
    elif sys.platform == "win32":
        install_for_windows(directory)

    else:
        print('ERROR: Unrecognized operating system %s' % sys.platform)
        exit(0)


####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Current directory
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Installation directory
    install_directory = '%s/../blender-nmv' % current_directory

    # Create the installation directory
    if not os.path.exists(install_directory):
        os.mkdir(install_directory)

    # Download blender based on the software
    install_neuromorphovis(install_directory)
