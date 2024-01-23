####################################################################################################
# Copyright (c) 2024, EPFL / Blue Brain Project
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


import sys
import argparse
import subprocess
import nmv.file

####################################################################################################
# @construct_per_mesh_command
####################################################################################################
def construct_per_mesh_command(args, input_mesh):

    command = ''
    command += ' %s ' % args.blender_executable
    command += ' -b --verbose 0 --python optimize_mesh.py -- '
    command += ' --input-directory %s ' % args.input_directory
    command += ' --input-mesh %s ' % input_mesh
    command += ' --output-directory %s>%s/%s.txt' % (args.output_directory, args.output_directory, input_mesh)
    return command


####################################################################################################
# @execute_command
####################################################################################################
def execute_command(command):

    print(command)
    subprocess.call(command, shell=True)


####################################################################################################
# @execute_commands_parallel
####################################################################################################
def execute_commands_parallel(shell_commands, num_cores):

    from joblib import Parallel, delayed
    Parallel(n_jobs=num_cores)(delayed(execute_command)(i) for i in shell_commands)


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
    description = 'Verify the number of self-intersections w.r.t optimization iterations'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Blender executable'
    parser.add_argument('--blender-executable',
                        action='store', dest='blender_executable', help=arg_help)

    arg_help = 'The input directory that contains the meshes'
    parser.add_argument('--input-directory', action='store', help=arg_help)

    arg_help = 'The input mesh file name'
    parser.add_argument('--input-mesh', action='store', help=arg_help)

    arg_help = 'Output directory, where the final result stored'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    arg_help = 'Number of parallel cores'
    parser.add_argument('--num-cores',
                        action='store', default=1, type=int, help=arg_help)

    # Parse the arguments
    return parser.parse_args()

####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Load all the OBJ meshes
    meshes_list = nmv.file.get_files_in_directory(args.input_directory, '.obj')
    meshes_list.extend(nmv.file.get_files_in_directory(args.input_directory, '.stl'))

    commands = list()
    for input_mesh in meshes_list:
        commands.append(construct_per_mesh_command(args=args, input_mesh=input_mesh))

    execute_commands_parallel(commands, num_cores=args.num_cores)