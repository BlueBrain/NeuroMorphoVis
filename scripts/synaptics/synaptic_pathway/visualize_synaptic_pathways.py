####################################################################################################
# Copyright (c) 2023, EPFL / Blue Brain Project
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
def parse_command_line_arguments():
    """Parses the input arguments.

    :return:
        Arguments list.
    """

    # Add all the options
    description = 'This add-on uses NeuroMorphoVis to create a Blender file and list of images ' \
                  'to visualize a custom list of synapses on the dendrites of a post-synaptic ' \
                  'neuron in a BBP circuit. '
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'The path to blender'
    parser.add_argument('--blender',
                        action='store', dest='blender', help=arg_help)

    arg_help = 'Output directory, where the final artifacts will be generated'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'BBP circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)

    arg_help = 'The list of the pre- and post-synaptic pairs.'
    parser.add_argument('--pairs-list',
                        action='store', dest='pairs_list', help=arg_help)

    arg_help = 'The type of the radii of the neuronal branches'
    parser.add_argument('--branches-radii-type',
                        action='store', dest='branches_radii_type', help=arg_help)

    arg_help = 'The value of the unified radius of the branches (in um)'
    parser.add_argument('--unified-branches-radius',
                        action='store', dest='unified_branches_radius', type=float, help=arg_help)

    arg_help = 'A scale factor for the radii'
    parser.add_argument('--branches-radius-scale',
                        action='store', dest='branches_radius_scale', type=float, help=arg_help)

    arg_help = 'The color of the dendrites of the pre-synaptic neuron.'
    parser.add_argument('--pre-synaptic-dendrites-color',
                        action='store', dest='pre_synaptic_dendrites_color', help=arg_help)

    arg_help = 'The color of the axons of the pre-synaptic neuron.'
    parser.add_argument('--pre-synaptic-axons-color',
                        action='store', dest='pre_synaptic_axons_color', help=arg_help)

    arg_help = 'The color of the dendrites of the post-synaptic neuron.'
    parser.add_argument('--post-synaptic-dendrites-color',
                        action='store', dest='post_synaptic_dendrites_color', help=arg_help)

    arg_help = 'The color of the axons of the post-synaptic neuron.'
    parser.add_argument('--post-synaptic-axons-color',
                        action='store', dest='post_synaptic_axons_color', help=arg_help)

    arg_help = 'The color of the synapses.'
    parser.add_argument('--synapses-color',
                        action='store', dest='synapses_color', help=arg_help)

    arg_help = 'Synapse radius (in um)'
    parser.add_argument('--synapse-radius',
                        action='store', dest='synapse_radius', type=float, help=arg_help)

    arg_help = 'Base image resolution'
    parser.add_argument('--image-resolution',
                        action='store', default=2048, type=int, dest='image_resolution',
                        help=arg_help)

    arg_help = 'Save the scene into a 3D Blender file for interactive visualization later'
    parser.add_argument('--save-blend-file',
                        dest='save_blend_file', action='store_true', default=False, help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @parse_pair_file
####################################################################################################
def parse_pair_file(file_path):
    """Parses the input pair file and returns the pre- and post-synaptic pair.

    :param file_path:
        The input synaptic pair file.
    :return:
        A list of all the pairs.
    """

    # Open the file
    f = open(file_path, 'r')

    # Get the list
    pairs = list()
    for line in f:
        data = line.split('-')
        pre_gid = data[0].replace('a', '').replace('\n', '')
        post_gid = data[1].replace('a', '').replace('\n', '')
        pairs.append([pre_gid, post_gid])

    # Close the file
    f.close()

    # Return the list
    return pairs


####################################################################################################
# @construct_command
####################################################################################################
def construct_command(args,
                      pair):
    """Constructs the command that will be executed on a per-pair-basis.

    :param args:
        System args.
    :param pair:
        Neuron pair list, pre and post.
    :return:
        The execution command.
    """

    command = '%s -b --verbose 0 ' % args.blender
    command += '--python visualize_synaptic_pathway.py -- '
    command += '--output-directory %s ' % args.output_directory
    command += '--circuit %s ' % args.circuit_config
    command += '--pre-synaptic-neuron-gid %s ' % pair[0]
    command += '--post-synaptic-neuron-gid %s ' % pair[1]
    command += '--pre-synaptic-dendrites-color \'%s\' ' % args.pre_synaptic_dendrites_color
    command += '--pre-synaptic-axons-color \'%s\' ' % args.pre_synaptic_axons_color
    command += '--post-synaptic-dendrites-color \'%s\' ' % args.post_synaptic_dendrites_color
    command += '--post-synaptic-axons-color \'%s\' ' % args.post_synaptic_axons_color
    command += '--branches-radii-type %s ' % args.branches_radii_type
    command += '--unified-branches-radius %s ' % args.unified_branches_radius
    command += '--branches-radius-scale %s ' % args.branches_radius_scale
    command += '--synapses-color \'%s\' ' % args.synapses_color
    command += '--synapse-radius %s ' % args.synapse_radius
    command += '--image-resolution %s ' % args.image_resolution

    # Bool options
    if args.save_blend_file:
        command += '--save-blend-file '

    # Return the resulting command
    return command


####################################################################################################
# @execute_shell_command
####################################################################################################
def execute_shell_command(shell_command):
    """Executes the shell command.

    :param shell_command:
        A given shell command to execute.
    """
    print(shell_command)
    subprocess.call(shell_command, shell=True)


####################################################################################################
# @main
####################################################################################################
def main():
    """The main function."""

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Get the pairs
    pairs = parse_pair_file(file_path=args.pairs_list)

    # Run the command for the pairs
    commands = list()
    for pair in pairs:
        commands.append(construct_command(args=args, pair=pair))

    # Execute the commands
    for command in commands:
        execute_shell_command(shell_command=command)


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    main()
