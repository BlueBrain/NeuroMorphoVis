#!/usr/bin/python
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
import os
import sys
import platform
import subprocess
import argparse
import shutil
import shlex


####################################################################################################
# @get_pip_wheels
####################################################################################################
def get_pip_wheels():
    """Returns a lit of the required wheels that should be installed to be able to run NMV.

    :return:
        A list of lists, where each item in the list is composed of two strings. The first string
        is the name of the pip package, and the second string is the recommended version.
        If the second version if empty, the latest version will be installed.
    :rtype:
    """

    return [['numpy', ''],
            ['h5py', ''],
            ['matplotlib', ''],
            ['seaborn', ''],
            ['pandas', ''],
            ['Pillow', ''],
            ['webbrowser', ''],
            ['tqdm', ''],
            ['morphio', '']]


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
    description = 'Installing NeuroMorphoVis simple, easy and awesome! ' \
                  'This script is valid for *nix-based operating systems including macOSX and ' \
                  'Linux distributions. For windows, you can download a .zip package from the ' \
                  'release page. \n' \
                  'NOTE: python, git, wget or curl must be installed to run this script.'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Blender version. 2.79, 2.80, 3.1 and 3.5; default (3.5)' \
               'It is recommended to avoid all preceding versions as much as possible.'
    parser.add_argument('--blender-version',
                        action='store', dest='blender_version', default='3.5', help=arg_help)

    arg_help = 'Installation directory.'
    parser.add_argument('--prefix',
                        action='store', dest='install_prefix', required=True, help=arg_help)

    arg_help = 'Enable to get a detailed log, otherwise only the basic operations'
    parser.add_argument('--verbose',
                        action='store_true', default=False, dest='verbose', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @run_command
####################################################################################################
def run_command(shell_command,
                verbose=False):
    """Runs a shell command.

    :param shell_command:
        A shell command to execute.
    :param verbose:
        Flag to print more massages for debugging.
    """

    if verbose:
        print('\t* SHELL: ' + shell_command)
        subprocess.call(shell_command, shell=True)
    else:
        devnull = open(os.devnull, 'w')
        subprocess.call(shlex.split(shell_command), stdout=devnull)


####################################################################################################
# @log_header
####################################################################################################
def log_header(msg):
    """Header.

    :param msg:
        Message.
    """
    print('* %s' % msg)


####################################################################################################
# @log_process
####################################################################################################
def log_process(msg):
    """Process.

   :param msg:
       Message.
   """
    print('\t* %s' % msg)


####################################################################################################
# @log_detail
####################################################################################################
def log_detail(msg):
    """Detail.

   :param msg:
       Message.
   """
    print('\t\t* %s' % msg)


####################################################################################################
# @install_for_linux
####################################################################################################
def install_for_linux(directory, blender_version, verbose=False):
    """Install NeuroMorphoVis on Linux operating system.

    :param directory:
        Installation directory.
    :param blender_version
        The version of Blender.
    :param verbose:
        Verbose.
    """

    # Blender url
    if blender_version == '2.79':
        python_version = '3.5'
        package_name = 'blender-2.79-linux-glibc219-x86_64'
        extension = 'tar.bz2'
    elif blender_version == '2.80':
        python_version = '3.7'
        package_name = 'blender-2.80-linux-glibc217-x86_64'
        extension = 'tar.bz2'
    elif blender_version == '3.1':
        python_version = '3.10'
        package_name = 'blender-3.1.0-linux-x64'
        extension = 'tar.xz'
    elif blender_version == '3.5':
        python_version = '3.10'
        package_name = 'blender-3.5.0-linux-x64'
        extension = 'tar.xz'
    else:
        print('ERROR: Unsupported Blender version [%s]' % blender_version)
        exit(0)

    # Blender url
    server = 'https://download.blender.org/release/Blender%s/' % blender_version
    blender_url = '%s/%s.%s' % (server, package_name, extension)

    # wet (Download)
    log_process('Downloading Blender [%s] from %s' % (blender_version, blender_url))
    shell_command = 'wget -O %s/blender.%s %s' % (directory, extension, blender_url)
    run_command(shell_command, verbose)

    # Extract
    if '.bz2' in extension:
        shell_command = 'tar xjfv %s/blender.%s -C %s' % (directory, extension, directory)
    else:
        shell_command = 'tar xf %s/blender.%s -C %s' % (directory, extension, directory)
    run_command(shell_command, verbose)

    # Moving to blender
    blender_directory = '%s/blender-bbp' % directory
    shell_command = 'mv %s/%s %s' % (directory, package_name, blender_directory)
    if os.path.exists(blender_directory):
        os.rmdir(blender_directory)
    run_command(shell_command, verbose)

    # Clone NeuroMorphoVis into the 'addons' directory
    addons_directory = '%s/blender-bbp/%s/scripts/addons/' % (directory, blender_version)
    neuromorphovis_url = 'https://github.com/BlueBrain/NeuroMorphoVis.git'
    shell_command = 'git clone %s %s/neuromorphovis' % (neuromorphovis_url, addons_directory)
    run_command(shell_command, verbose)

    # Removing the site-packages directory
    blender_python_wheels = '%s/blender-bbp/%s/python/lib/python%s/site-packages/' % \
                            (directory, blender_version, python_version)
    shell_command = 'rm -rf %s/numpy' % blender_python_wheels
    run_command(shell_command, verbose)

    # Blender python
    blender_python_prefix = '%s/%s/python/bin/' % (blender_directory, blender_version)

    if float(blender_version) < 3.1:
        blender_python = '%s/python%sm' % (blender_python_prefix, python_version)
    else:
        blender_python = '%s/python%s' % (blender_python_prefix, python_version)

    # Pip installation
    get_pip_script_url = 'https://bootstrap.pypa.io/get-pip.py'
    shell_command = 'wget -O %s/get-pip.py %s' % (blender_python_prefix, get_pip_script_url)
    run_command(shell_command, verbose)

    # Activate the get-pip.py script
    get_pip_script = '%s/get-pip.py' % blender_python_prefix
    shell_command = 'chmod +x %s' % get_pip_script
    run_command(shell_command, verbose)

    shell_command = '%s %s' % (blender_python, get_pip_script)
    run_command(shell_command, verbose)

    # Pip executable
    pip_executable = '%s/pip' % blender_python_prefix

    # Installing dependencies
    pip_wheels = get_pip_wheels()

    # packages
    for i, wheel in enumerate(pip_wheels):
        shell_command = '%s install --ignore-installed %s' % (pip_executable, wheel[0])
        print('INSTALL: %s' % shell_command)
        run_command(shell_command, verbose)

    # h5py specific version
    shell_command = '%s install --ignore-installed h5py==2.10.0' % pip_executable
    print('INSTALL: %s' % shell_command)
    run_command(shell_command, verbose)

    try:
        bbp_devpi = 'https://bbpteam.epfl.ch/repository/devpi/simple/'
        log_detail('Installing: BBP dependencies')
        shell_command = '%s install -i %s bluepy' % (pip_executable, bbp_devpi)
        run_command(shell_command, verbose)

        shell_command = '%s install -i %s bluepy_configfile' % (pip_executable, bbp_devpi)
        run_command(shell_command, verbose)

    except ImportError:
        print('The BBP dependencies were not installed. Can NOT use BluePy or load circuits!')

    # Remove the archive
    log_process('Cleaning')
    shell_command = 'rm %s/blender.%s' % (directory, extension)
    run_command(shell_command, verbose)


####################################################################################################
# @install_for_mac
####################################################################################################
def install_for_mac(directory, blender_version, arch, verbose=False):
    """Install NeuroMorphoVis on macOSX operating system.

    :param directory:
        Installation directory.
    :param blender_version
        The version of Blender.
    :param arch:
        Hardware architecture.
    :param verbose:
        Verbose.
    """

    # Server
    server = 'https://download.blender.org/release/Blender%s/' % blender_version

    # Blender url
    if blender_version == '2.79':
        python_version = '3.5'
        package_name = 'blender-2.79b-macOS-10.6.dmg'
    elif blender_version == '2.80':
        python_version = '3.7'
        package_name = 'blender-2.80rc3-macOS.dmg'
    elif blender_version == '3.1':
        python_version = '3.10'
        package_name = 'blender-3.1.0-macos-x64.dmg'
    elif blender_version == '3.5':
        python_version = '3.10'
        if 'x86' in arch:
            package_name = 'blender-3.5.0-macos-x64.dmg'
        elif 'arm' in arch:
            package_name = 'blender-3.5.0-macos-arm64.dmg'
        else:
            print('ERROR: Unsupported architecture [%s]' % arch)
            exit(0)
    else:
        print('ERROR: Wrong Blender version [%s]' % blender_version)
        exit(0)

    # curl (Download)
    blender_url = '%s/%s' % (server, package_name)
    log_process('Downloading Blender [%s] from %s' % (blender_version, blender_url))
    shell_command = 'curl %s -o %s/blender.dmg' % (blender_url, directory)
    run_command(shell_command, verbose)

    # Extract
    log_process('Extracting Blender')
    shell_command = 'hdiutil attach %s/blender.dmg' % directory
    run_command(shell_command, verbose)

    # Copy the Blender.app
    log_process('Copying Blender')
    if blender_version == '2.79':
        shell_command = 'cp -r /Volumes/Blender/Blender %s/.' % directory
    else:
        shell_command = 'cp -r /Volumes/Blender/Blender.app %s/.' % directory
    run_command(shell_command, verbose)

    # Detach
    log_process('Detaching DMG Image')
    shell_command = 'hdiutil detach /Volumes/Blender'
    run_command(shell_command, verbose)

    # Clone NeuroMorphoVis into the 'addons' directory
    log_process('Clone NeuroMorphoVis')
    if blender_version == '2.79':
        blender_app_directory = '%s/Blender/blender.app' % directory
    else:
        blender_app_directory = '%s/Blender.app' % directory
    addons_directory = '%s/Contents/Resources/%s/scripts/addons/' % (blender_app_directory,
                                                                     blender_version)
    neuromorphovis_url = 'https://github.com/BlueBrain/NeuroMorphoVis.git'
    shell_command = 'git clone %s %s/neuromorphovis' % (neuromorphovis_url, addons_directory)
    run_command(shell_command, verbose)

    # Blender python
    blender_python_prefix = '%s/Contents/Resources/%s/python/bin/' % (blender_app_directory,
                                                                      blender_version)
    if float(blender_version) < 3.1:
        blender_python = '%s/python%sm' % (blender_python_prefix, python_version)
    else:
        blender_python = '%s/python%s' % (blender_python_prefix, python_version)

    # Pip installation
    log_process('Installing Dependencies')
    get_pip_script_url = 'https://bootstrap.pypa.io/get-pip.py'
    shell_command = 'curl %s -o %s/get-pip.py' % (get_pip_script_url, blender_python_prefix)
    run_command(shell_command, verbose)

    # Activate the get-pip.py script
    log_detail('Installing: pip')
    get_pip_script = '%s/get-pip.py' % blender_python_prefix
    shell_command = 'chmod +x %s' % get_pip_script
    run_command(shell_command, verbose)
    shell_command = '%s %s' % (blender_python, get_pip_script)
    run_command(shell_command, verbose)

    pip_executable = '%s/pip' % blender_python_prefix

    # Removing the previous numpy installation
    log_detail('Uninstalling: numpy')
    blender_python_wheels = '%s/Contents/Resources/%s/python/lib/python%s/site-packages' % (
        blender_app_directory, blender_version, python_version)
    shell_command = 'rm -rf %s/numpy*' % blender_python_wheels
    run_command(shell_command, verbose)

    # Installing dependencies
    pip_wheels = get_pip_wheels()
    for wheel in pip_wheels:
        log_detail('Installing: %s' % wheel)
        shell_command = '%s install --ignore-installed %s' % (pip_executable, wheel[0])
        run_command(shell_command, verbose)

    # h5py specific version
    shell_command = '%s install --ignore-installed h5py==2.10.0' % pip_executable
    print('INSTALL: %s' % shell_command)
    run_command(shell_command, verbose)

    try:
        bbp_devpi = 'https://bbpteam.epfl.ch/repository/devpi/simple/'
        log_detail('Installing: BBP dependencies')
        shell_command = '%s install -i %s bluepy' % (pip_executable, bbp_devpi)
        run_command(shell_command, verbose)

        shell_command = '%s install -i %s bluepy_configfile' % (pip_executable, bbp_devpi)
        run_command(shell_command, verbose)

    except ImportError:
        print('The BBP dependencies were not installed. Can NOT use BluePy or load circuits!')

    # Copying the perf file to load NMV directly

    # Remove the .dmg file
    log_process('Cleaning')
    shell_command = 'rm %s/blender.dmg' % directory
    run_command(shell_command, verbose)


####################################################################################################
# @install_neuromorphovis
####################################################################################################
def install_neuromorphovis(directory, blender_version, verbose=False):
    """Installs NeuroMorphoVis

    :param directory:
        Installation directory.
    :param blender_version:
        The version of Blender.
    :param verbose:
        Verbose.
    """

    # Get the platform details
    platform_uname = platform.uname()

    # Header
    log_header('Installing Blender for %s' % platform_uname.system)
    log_process('Installation Directory: %s' % directory)

    # Verify the OS
    if "linux" in platform_uname.system.lower():
        install_for_linux(directory, blender_version, verbose)
    elif "darwin" in platform_uname.system.lower():
        install_for_mac(directory, blender_version, platform_uname.machine, verbose)
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

    # Check that the apps required to install NMV are all there.
    # check_apps()

    # Create the installation directory
    if not os.path.exists(args.install_prefix):
        os.mkdir(args.install_prefix)

    # Verify blender version
    if args.blender_version == '2.79':
        log_header('Blender 2.79')
    elif args.blender_version == '2.80':
        log_header('Blender 2.80')
    elif args.blender_version == '3.1':
        log_header('Blender 3.1')
    elif args.blender_version == '3.5':
        log_header('Blender 3.5')
    else:
        log_header('NeuroMorphoVis is ONLY available for the following Blender versions '
                   '2.79, 2.80, 3.1 and 3.5. Recommended version: 3.5')
        exit(0)

    # Installation directory
    installation_directory = '%s/bbp-blender-%s' % (args.install_prefix, args.blender_version)

    # Verify the installation directory
    if not os.path.exists(args.install_prefix):
        os.mkdir(args.install_prefix)
    if not os.path.exists(installation_directory):
        os.mkdir(installation_directory)
    else:
        shutil.rmtree(installation_directory)
        os.mkdir(installation_directory)

    # Download blender based on the software
    install_neuromorphovis(installation_directory, args.blender_version, args.verbose)