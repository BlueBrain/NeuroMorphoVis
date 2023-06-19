####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import argparse
import json

# Blender imports
from mathutils import Vector


####################################################################################################
# @parse_synaptome_command_line_arguments
####################################################################################################
def parse_synaptome_command_line_arguments(arguments=None):
    """Parses the input arguments.

    :param arguments:
        Command line arguments.
    :return:
        Arguments list.
    """

    # add all the options
    description = 'Synaptome creator: creates static images and 360s of synaptomes'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)

    arg_help = 'Neuron GID'
    parser.add_argument('--gid',
                        action='store', dest='gid', type=int, help=arg_help)

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

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @parse_synaptic_pathway_command_line_arguments
####################################################################################################
def parse_synaptic_pathway_command_line_arguments(arguments=None):
    """Parses the input arguments of the synaptic pathway script.

    :param arguments:
        Command line arguments.
    :return:
        Arguments list.
    """

    # add all the options
    description = 'Synaptic pairs creator: creates static images synaptic pairs'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)

    arg_help = 'Pre-synaptic neuron GID'
    parser.add_argument('--pre-gid',
                        action='store', type=int, dest='pre_gid',
                        help=arg_help)

    arg_help = 'Post-synaptic neuron GID'
    parser.add_argument('--post-gid',
                        action='store', type=int, dest='post_gid',
                        help=arg_help)

    arg_help = 'Output directory, where the final image/movies and scene will be stored'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'Pre-GID Neuron color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--pre-neuron-color',
                        action='store', dest='pre_neuron_color', help=arg_help)

    arg_help = 'Post-GID Neuron color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--post-neuron-color',
                        action='store', dest='post_neuron_color', help=arg_help)

    arg_help = 'Synapse color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--synapse-color',
                        action='store', dest='synapse_color', help=arg_help)

    arg_help = 'Synapse size (in um)'
    parser.add_argument('--synapse-size',
                        action='store', dest='synapse_size', type=float, help=arg_help)

    arg_help = 'Base image resolution'
    parser.add_argument('--image-resolution',
                        action='store', default=2000, type=int, dest='image_resolution',
                        help=arg_help)

    arg_help = 'Background image'
    parser.add_argument('--background-image',
                        action='store', dest='background_image', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @parse_synaptic_pathways_command_line_arguments
####################################################################################################
def parse_synaptic_pathways_command_line_arguments(arguments=None):
    """Parses the input arguments of the synaptic pathways script.

    :param arguments:
        Command line arguments.
    :return:
        Arguments list.
    """

    # add all the options
    description = 'Synaptic pairs creator: creates static images synaptic pairs'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)

    arg_help = 'Synaptic pairs file'
    parser.add_argument('--synaptic-pairs-file',
                        action='store', dest='synaptic_pairs_file', help=arg_help)

    arg_help = 'Output directory, where the final image/movies and scene will be stored'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'Pre-GID Neuron color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--pre-neuron-color',
                        action='store', dest='pre_neuron_color', help=arg_help)

    arg_help = 'Post-GID Neuron color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--post-neuron-color',
                        action='store', dest='post_neuron_color', help=arg_help)

    arg_help = 'Synapse color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--synapse-color',
                        action='store', dest='synapse_color', help=arg_help)

    arg_help = 'Synapse size (in um)'
    parser.add_argument('--synapse-size',
                        action='store', dest='synapse_size', type=float, help=arg_help)

    arg_help = 'Base image resolution'
    parser.add_argument('--image-resolution',
                        action='store', default=2000, type=int, dest='image_resolution',
                        help=arg_help)

    arg_help = 'Background image'
    parser.add_argument('--background-image',
                        action='store', dest='background_image', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @parse_color_map
####################################################################################################
def parse_color_map(color_map_file):
    """Parses the color map from the file based on the mtypes of the pre-synaptic cells.
    NOTE: Ask Srikanth Ramaswamy for the format.

    :param color_map_file:
        A given color map.
    :return:
        A color map dictionary with mtypes keys.
    """

    # Open the file
    handle = open(color_map_file, 'r')

    # A dictionary that will have the color-map
    color_map = {}

    for line in handle:

        # If empty line skip
        if not line.strip():
            continue

        # String processing
        line = line.replace('\n', '')
        line = line.replace('[', '')
        line = line.replace(']', '')
        line = line.split(' ')

        # Color-map
        color_map[line[0]] = Vector((float(line[1]) / 256.0,
                                     float(line[2]) / 256.0,
                                     float(line[3]) / 256.0))

        # Close the file
    handle.close()

    # Return a reference to the color-map
    return color_map


####################################################################################################
# @parse_json_color_map
####################################################################################################
def parse_json_color_map(color_map_file):
    """Parse a json color map.

    :param color_map_file:
        A given color map file.
    :return:
        A dictionary for the color-map.
    """

    # Open the file
    handle = open(color_map_file, 'r')

    # Read the map
    color_map_string = str(handle.read())
    color_map_string = color_map_string.replace("'", "\"")

    # Close the file
    handle.close()

    # Return the dictionary
    return json.loads(color_map_string)


####################################################################################################
# @parse_synaptic_pairs
####################################################################################################
def parse_synaptic_pairs(synaptic_pairs_file):
    """Parse the synaptic pairs.

    :param synaptic_pairs_file:
        A file containing the synaptic pairs.
    :return:
        A list of the pre- and post-synaptic neurons.
    """

    # Open the file
    handle = open(synaptic_pairs_file, 'r')

    # A list that will contain the pairs
    pairs = list()

    # Get every pair
    for line in handle:

        # If empty line skip
        if not line.strip():
            continue

        # String processing
        line = line.replace("\t", " ")
        line = line.replace('\n', '')
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.split(' ')

        # Append it to the pairs list
        pairs.append([int(line[0]), int(line[1])])

        # Close the file
    handle.close()

    # Return a reference to the pairs
    return pairs


####################################################################################################
# @parse_synaptomes_gids
####################################################################################################
def parse_synaptomes_gids(synaptome_gids_file):
    """Parse the synaptic pairs.

    :param synaptome_gids_file:
        A file containing the GIDs of the synaptomes.
    :return:
        A list of GIDs.
    """

    # Open the file
    handle = open(synaptome_gids_file, 'r')

    # A list that will contain the GIDs
    pairs = list()

    # Get every GID in the file
    for line in handle:

        # If empty line skip
        if not line.strip():
            continue

        # String processing
        line = line.replace('\n', '')

        # Append it to the pairs list
        pairs.append(line)

        # Close the file
    handle.close()

    # Return a reference to the GIDs
    return pairs


####################################################################################################
# @parse_color
####################################################################################################
def parse_color(color_string):
    """Gets the vector of a color.

    :param color_string:
        String representing the color.
    :return:
        A Vector of the color code.
    """

    color = color_string.split('_')
    return Vector((float(color[0]) / 255.0, int(color[1]) / 255.0, int(color[2]) / 255.0))
