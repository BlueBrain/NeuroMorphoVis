####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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
import argparse
import subprocess


####################################################################################################
# @get_gids_from_file
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
def construct_generation_command(args,
                                 gids):
    """Construct the command line per gid.

    :param args:
        Input arguments.
    :param gids:
        List of GIDs.
    :return:
        A list of command.
    """

    # A list of commands that will be executed either in serial or in parallel
    commands_list = list()

    # Per astrocyte
    for gid in gids:

        # Make the command
        shell_command = '%s' % args.blender_executable
        shell_command += ' -b --verbose 0 --python astrocyte_generator.py --'
        shell_command += ' --gid=%s' % gid
        shell_command += ' --output-directory=%s' % args.output_directory
        shell_command += ' --circuit-path=%s' % args.circuit_path
        shell_command += ' --soma-style=%s' % args.soma_style
        shell_command += ' --mesh-type=%s' % args.mesh_type
        shell_command += ' --decimation-factor=%s' % args.decimation_factor
        shell_command += ' --ultra-clean-mesh-executable=%s' % args.ultra_clean_mesh_executable

        if args.export_obj:
            shell_command += ' --export-obj'
        if args.export_blend:
            shell_command += ' --export-blend'
        if args.create_optimized:
            shell_command += ' --create-optimized'
        if args.center_morphology:
            shell_command += ' --center-morphology'

        # Append to the commands list
        commands_list.append(shell_command)

    # Return the commands list
    return commands_list


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

    arg_help = 'The type of the resulting meshes, [simulation], [visualization] or [both]'
    parser.add_argument('--mesh-type',
                        action='store', dest='mesh_type', help=arg_help)

    arg_help = 'Execution mode, serial or parallel'
    parser.add_argument('--execution',
                        action='store', dest='execution', default='serial', help=arg_help)
                        
    arg_help = 'NUmber of cores for parallel processing'
    parser.add_argument('--number-cores',
                        action='store', dest='number_cores', default='4', type=int, help=arg_help)

    arg_help = 'The path to the NGV circuit'
    parser.add_argument('--circuit-path',
                        action='store', dest='circuit_path', help=arg_help)

    arg_help = 'The style of the soma'
    parser.add_argument('--soma-style',
                        action='store', dest='soma_style', help=arg_help)

    arg_help = 'The GIDs of the astrocytes'
    parser.add_argument('--gids-file',
                        action='store', dest='gids_file', help=arg_help)

    arg_help = 'A range of GIDs'
    parser.add_argument('--gids-range',
                        action='store', dest='gids_range', default='0', help=arg_help)

    arg_help = 'Center the morphology at the origin'
    parser.add_argument('--center-morphology',
                        action='store_true', default=False, help=arg_help)

    arg_help = 'Export the result into an .OBJ file'
    parser.add_argument('--export-obj',
                        action='store_true', dest='export_obj', default=False, help=arg_help)

    arg_help = 'Export the result into an .BLEND file'
    parser.add_argument('--export-blend',
                        action='store_true', dest='export_blend', default=False, help=arg_help)

    arg_help = 'Create the optimized mesh'
    parser.add_argument('--create-optimized',
                        action='store_true', dest='create_optimized', default=False, help=arg_help)

    arg_help = 'ultraCleanMesh executable'
    parser.add_argument('--ultra-clean-mesh-executable',
                        action='store', dest='ultra_clean_mesh_executable', help=arg_help)

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

    # One must export a valid mesh
    if (not args.export_blend) and (not args.export_obj):
        print('You must export either a .BLEND or .OBJ mesh')
        exit(0)

    # Get the GIDs
    if args.gids_range is not '0':
        gids_string = args.gids_range.split('-')
        gids = list(range(int(gids_string[0]), int(gids_string[1]) + 1))
    else:
        gids = get_gids_from_file(gids_file=args.gids_file)

    # Build the commands
    commands = construct_generation_command(args, gids)

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    # Execute the commands
    if 'parallel' in args.execution:
        from joblib import Parallel, delayed
        Parallel(n_jobs=args.number_cores)(delayed(run_command)(i) for i in commands)
    else:
        for command in commands:
            run_command(command)


