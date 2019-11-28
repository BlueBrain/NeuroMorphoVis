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
import argparse


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):
    """Parses the input arguments.

    :param arguments:
        Command line arguments.
    :return:
        Arguments list.
    """

    # add all the options
    description = 'Installing NeuroMorphoVis from scratch. Simply, easy and awesome!' \
                  'This script is valid for *nix-based operating systems including macOSX and ' \
                  'Linux distributions. For windows, you can download a zip package from the ' \
                  'release page. \n' \
                  'NOTE: git, wget or curl must be installed to run this script.'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Blender version. 2.79, 2.80, or 2.81. 2.8 by default.'
    parser.add_argument('--blender-version',
                        action='store', dest='blender_version', help=arg_help)

    arg_help = 'Installation directory.'
    parser.add_argument('--install-prefix',
                        action='store', dest='install_prefix', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @install_for_linux
####################################################################################################
def install_for_linux(directory, blender_version):
    """Install NeuroMorphoVis on Linux operating system.

    :param directory:
        Installation directory.
    """

    # Blender url
    server = 'https://download.blender.org/release/Blender2.80/'
    package_name = 'blender-2.80rc3-linux-glibc217-x86_64'
    blender_url = '%s/%s.tar.bz2' % (server, package_name)

    # wet (Download)
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

    # Removing the previous numpy installation
    blender_python_wheels = '%s/blender-neuromorphovis/2.80/python/lib/site-packages/' % directory
    shell_command = 'rm -rf %s/numpy*' % blender_python_wheels
    print(shell_command)
    subprocess.call(shell_command, shell=True)

    shell_command = '%s %s' % (blender_python, get_pip_script)
    print('INSTALL: %s' % shell_command)
    subprocess.call(shell_command, shell=True)

    pip_executable = '%s/pip' % blender_python_prefix

    for wheel in pip_wheels:

        # Command
        shell_command = '%s install --ignore-installed %s' % (pip_executable, wheel)
        print('INSTALL: %s' % shell_command)
        subprocess.call(shell_command, shell=True)


####################################################################################################
# @install_for_mac
####################################################################################################
def install_for_mac(directory, blender_version):
    """Install NeuroMorphoVis on macOSX operating system.

    :param directory:
        Installation directory.
    """

    # Server
    server = 'https://download.blender.org/release/Blender%s/' % blender_version

    # Blender url
    if blender_version == '2.79':
        package_name = 'blender-2.79b-macOS-10.6.dmg'
    elif blender_version == '2.80':
        package_name = 'blender-2.80rc3-macOS'
    elif blender_version == '2.81':
        package_name = 'blender-2.81-macOS.dmg'
    else:
        print('ERROR: Wrong Blender version [%s]' % blender_version)
        exit(0)

    # Blender url
    blender_url = '%s/%s.dmg' % (server, package_name)
    print('Downloading Blender [%s] from %s' % (blender_version, blender_url))

    # curl (Download)
    shell_command = 'curl %s -o %s/blender.dmg' % (blender_url, directory)
    print('INSTALL: ' + shell_command)
    subprocess.call(shell_command, shell=True)

    # Extract
    shell_command = 'hdiutil attach %s/blender.dmg' % directory
    print('INSTALL: ' + shell_command)
    subprocess.call(shell_command, shell=True)

    # Copy the Blender.app
    shell_command = 'cp -r /Volumes/Blender/Blender.app %s/.' % directory
    print('INSTALL: ' + shell_command)
    subprocess.call(shell_command, shell=True)

    # Detach
    shell_command = 'hdiutil detach /Volumes/Blender'
    print('INSTALL: ' + shell_command)
    subprocess.call(shell_command, shell=True)

    # Clone NeuroMorphoVis into the 'addons' directory
    blender_app_directory = '%s/Blender.app' % directory
    addons_directory = '%s/Contents/Resources/%s/scripts/addons/' % (blender_app_directory,
                                                                     blender_version)
    neuromorphovis_url = 'https://github.com/BlueBrain/NeuroMorphoVis.git'
    shell_command = 'git clone %s %s/neuromorphovis' % (neuromorphovis_url, addons_directory)
    print('INSTALL: ' + shell_command)
    subprocess.call(shell_command, shell=True)

    # Blender python
    blender_python_prefix = '%s/Contents/Resources/%s/python/bin/' % (blender_app_directory,
                                                                      blender_version)
    blender_python = '%s/python3.7m' % blender_python_prefix

    # Pip installation
    get_pip_script_url = 'https://bootstrap.pypa.io/get-pip.py'
    shell_command = 'curl  %s -o %s/get-pip.py' % (get_pip_script_url, blender_python_prefix)
    print('INSTALL: ' + shell_command)
    subprocess.call(shell_command, shell=True)

    # Activate the get-pip.py script
    get_pip_script = '%s/get-pip.py' % blender_python_prefix
    shell_command = 'chmod +x %s' % get_pip_script
    print('INSTALL: ' + shell_command)
    subprocess.call(shell_command, shell=True)

    shell_command = '%s %s' % (blender_python, get_pip_script)
    print('INSTALL: ' + shell_command)
    subprocess.call(shell_command, shell=True)

    pip_executable = '%s/pip' % blender_python_prefix

    # Removing the previous numpy installation
    blender_python_wheels = '%s/Contents/Resources/%s/python/lib/site-packages' % (
        blender_app_directory, blender_version)
    shell_command = 'rm -rf %s/numpy*' % blender_python_wheels
    print(shell_command)
    subprocess.call(shell_command, shell=True)

    # Installing dependencies
    pip_wheels = ['h5py', 'numpy', 'matplotlib', 'seaborn', 'pandas', 'Pillow']

    for wheel in pip_wheels:
        # Command
        shell_command = '%s install --ignore-installed %s' % (pip_executable, wheel)
        print('INSTALL: %s' % shell_command)
        subprocess.call(shell_command, shell=True)


####################################################################################################
# @install_neuromorphovis
####################################################################################################
def install_neuromorphovis(directory, blender_version):
    """Installs NeuroMorphoVis

    :param directory:
        Installation directory.
    :param blender_version:
        The version of Blender.
    """

    # Linux
    if sys.platform == "linux" or sys.platform == "linux2":
        install_for_linux(directory, blender_version)

    # OS X
    elif sys.platform == "darwin":
        install_for_mac(directory, blender_version)

    # Windows
    elif sys.platform == "win32":
        print('This script is only valid for *nix-based operating systems. '
              'For windows, you can download a zip package from the release page.')
        exit(0)

    else:
        print('ERROR: Unrecognized operating system %s' % sys.platform)
        exit(0)


####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Parse the arguments
    args = parse_command_line_arguments()

    # Get the current directory
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Create the installation directory
    if not os.path.exists(args.install_prefix):
        os.mkdir(args.install_prefix)

    # Verify blender version
    if args.blender_version == '2.79':
        print('Blender 2.79')
    elif args.blender_version == '2.80':
        print('Blender 2.80')
    elif args.blender_version == '2.81':
        print('Blender 2.81')
    else:
        print('NeuroMorphoVis is ONLY available for Blender versions 2.79, 2.80, 2.81 ')
        exit(0)

    # Download blender based on the software
    install_neuromorphovis(args.install_prefix, args.blender_version)
