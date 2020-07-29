####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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
import sys
import argparse
import subprocess


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def get_gids_from_file(gids_file):
    """Parse a list of GIDs from a file.

    :param gids_file:
        Given file that contains a list of the GIDs of the astrocytes to be generated.
    :return:
        A list of the GIDs of the astrocytes that will be generated.
    """
    gids_list = list()

    file = open(gids_file, 'r')
    for line in file:
        gids_list.append(line.replace('\n', ' '))
    file.close()

    # Return the GIDs list
    return gids_list


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def construct_generation_command(args, gids):

    # A list of commands that will be executed either in serial or in parallel
    commands = list()

    # Per astrocyte
    for gid in gids:

        # Make the command
        command = '%s' % args.blender_executable
        command += ' -b --verbose 0 --python astrocyte_generator.py --'
        command += ' --gid=%s' % gid
        command += ' --output-directory=%s' % args.output_directory
        command += ' --circuit-path=%s' % args.circuit_path
        command += ' --decimation-factor=%s' % args.decimation_factor

        # Append to the commands list
        commands.append(command)

    # Return the commands list
    return commands


####################################################################################################
# @run_command
####################################################################################################
def run_command(command):
    """Runs a given command
    :param command:
        A given command to be executed
    :return:
    """
    print(command)
    subprocess.call(command, shell=True)


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def run_serial_astrocyte_generation(commands):

    # Run every command one by one
    for command in commands:
        print(command)
        subprocess.call(command, shell=True)
        break


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

    description = 'Generating astrocytes'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Blender executable'
    parser.add_argument('--blender-executable',
                        action='store', dest='blender_executable', help=arg_help)

    arg_help = 'Output directory where the generated astrocyte will be written'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'Execution mode, serial or parallel'
    parser.add_argument('--execution',
                        action='store', dest='execution', default='parallel', help=arg_help)

    arg_help = 'The path to the NGV circuit'
    parser.add_argument('--circuit-path',
                        action='store', dest='circuit_path', help=arg_help)

    arg_help = 'The GID of the astrocyte'
    parser.add_argument('--gids-file',
                        action='store', dest='gids_file', help=arg_help)

    arg_help = 'Decimation factor, between 1.0 and 0.01'
    parser.add_argument('--decimation-factor',
                        action='store', dest='decimation_factor', type=float, default=1.0,
                        help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Get the GIDs
    gids = get_gids_from_file(gids_file=args.gids_file)

    # Build the commands
    commands = construct_generation_command(args, gids)

    # Execute the commands
    if 'parallel' in args.execution:
        print('parallel')
        from joblib import Parallel, delayed
        import multiprocessing
        Parallel(n_jobs=multiprocessing.cpu_count())(delayed(run_command)(command) for command in commands)
    else:
        for command in commands:
            run_command(command)


