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
import sys
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
# @run_command
####################################################################################################
def run_command(shell_command):
    """Runs a given command
    :param shell_command:
        A given command to be executed
    :return:
    """
    print(shell_command)
    subprocess.call(shell_command, shell=True)


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

    # Per gid
    for gid in gids:

        # Make the command
        display = os.getenv('VGL_DISPLAY')
        shell_command = 'DISPLAY=:5 %s' % args.blender_executable
        shell_command += ' -b --verbose 0 --python create-synaptome.py --'
        shell_command += ' --circuit-config=%s' % args.circuit_config
        shell_command += ' --gid=%s' % gid
        shell_command += ' --output-directory=%s' % args.output_directory
        shell_command += ' --color-map=%s' % args.color_map_file
        shell_command += ' --neuron-color=%s' % args.neuron_color
        shell_command += ' --full-view-resolution=%s' % args.full_view_resolution
        shell_command += ' --close-up-resolution=%s' % args.close_up_resolution
        shell_command += ' --synapse-percentage=%s' % args.synapse_percentage
        shell_command += ' --synapse-size=%s' % args.synapse_size
        shell_command += ' --close-up-size=%s' % args.close_up_size
        shell_command += ' --background-image=%s' % args.background_image

        if args.show_exc_inh:
            shell_command += ' --show-exc-inh'
        if args.render_frames:
            shell_command += ' --render-frames'
        if args.render_movies:
            shell_command += ' --render-movies'

        # Append to the commands list
        commands_list.append(shell_command)

    # Return the commands list
    return commands_list


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

    # Add all the options
    description = 'Synaptome creator: creates static images and 360s of synaptomes'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Blender executable'
    parser.add_argument('--blender-executable',
                        action='store', dest='blender_executable', help=arg_help)

    arg_help = 'Circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)

    arg_help = 'A list of all the neuron gids'
    parser.add_argument('--gids-file',
                        action='store', dest='gids_file', help=arg_help)

    arg_help = 'The percentage of synapses to be drawn in the rendering'
    parser.add_argument('--synapse-percentage',
                        action='store', dest='synapse_percentage', type=float, help=arg_help)

    arg_help = 'Show the excitatory and inhibitory neurons'
    parser.add_argument('--show-exc-inh',
                        action='store_true', default=False, dest='show_exc_inh', help=arg_help)

    arg_help = 'Render static frames'
    parser.add_argument('--render-frames',
                        action='store_true', default=False, dest='render_frames', help=arg_help)

    arg_help = 'Render static frames'
    parser.add_argument('--render-movies',
                        action='store_true', default=False, dest='render_movies', help=arg_help)

    arg_help = 'Output directory, where the final image/movies and scene will be stored'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'Synaptic color map'
    parser.add_argument('--color-map',
                        action='store', dest='color_map_file', help=arg_help)

    arg_help = 'Neuron color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--neuron-color',
                        action='store', dest='neuron_color', help=arg_help)

    arg_help = 'Synapse size (in um)'
    parser.add_argument('--synapse-size',
                        action='store', dest='synapse_size', type=float, help=arg_help)

    arg_help = 'Close-up view size'
    parser.add_argument('--close-up-size',
                        action='store', default=50, type=int, dest='close_up_size',
                        help=arg_help)

    arg_help = 'Base full-view resolution'
    parser.add_argument('--full-view-resolution',
                        action='store', default=2000, type=int, dest='full_view_resolution',
                        help=arg_help)

    arg_help = 'Base close-up resolution'
    parser.add_argument('--close-up-resolution',
                        action='store', default=1000, type=int, dest='close_up_resolution',
                        help=arg_help)

    arg_help = 'Background image'
    parser.add_argument('--background-image',
                        action='store', dest='background_image', help=arg_help)

    arg_help = 'Execution mode, serial or parallel'
    parser.add_argument('--execution',
                        action='store', dest='execution', default='serial', help=arg_help)

    arg_help = 'Number of parallel cores. Valid only if the execution is parallel'
    parser.add_argument('--number-parallel-cores',
                        action='store', default=4, type=int, dest='number_parallel_cores',
                        help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Get a list of all the gids from a given file
    gids = get_gids_from_file(gids_file=args.gids_file)

    # Build the commands
    commands = construct_generation_command(args, gids)

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    # Loading modules
    shell_command = 'module load unstable'
    subprocess.call(shell_command, shell=True)

    shell_command = 'module load virtualgl/2.5.2'
    subprocess.call(shell_command, shell=True)

    # Execute the commands
    if 'parallel' in args.execution:
        from joblib import Parallel, delayed
        import multiprocessing
        Parallel(n_jobs=args.number_parallel_cores)(delayed(run_command)(i) for i in commands)
    else:
        for command in commands:
            print(command)
            #run_command(command)
