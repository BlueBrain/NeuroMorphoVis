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
import os
import argparse
import random

# Internal imports
import_paths = ['core']
for import_path in import_paths:
    sys.path.append(('%s/%s' % (os.path.dirname(os.path.realpath(__file__)), import_path)))

import circuit_data
import color_map
import neuron_data
import synaptome

# Internal imports
import nmv.bbox
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.geometry
import nmv.options
import nmv.mesh
import nmv.rendering
import nmv.scene
import nmv.shading
import nmv.utilities
import nmv.bbp

# BBP imports
from bluepy import Synapse, Circuit

# Blender imports
from mathutils import Vector


# Just set the shader beforehand and create a dummy material
shader = nmv.enums.Shader.LAMBERT_WARD


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
    description = 'This add-on uses NeuroMorphoVis to create a Blender file and list of images ' \
                  'to visualize a custom list of synapses on the dendrites of a post-synaptic ' \
                  'neuron in a BBP circuit. '
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'BBP circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)

    arg_help = 'The GID of the post-synaptic neuron'
    parser.add_argument('--gid',
                        action='store', dest='gid', type=int, help=arg_help)

    arg_help = 'A JSON file containing the IDs of the synapses and their corresponding colors in ' \
               'the following format: ' \
               '{"R_G_B": [6563274686, 6563274687, ..], "R_G_B": [6563277480, 6563277481, .. ]}'
    parser.add_argument('--synapses-file',
                        action='store', dest='synapses_file', help=arg_help)

    arg_help = 'Output directory, where the final artifacts will be generated'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'Neuron color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--neuron-color',
                        action='store', dest='neuron_color', help=arg_help)

    arg_help = 'Synapse size (in um)'
    parser.add_argument('--synapse-size',
                        action='store', dest='synapse_size', type=float, help=arg_help)

    arg_help = 'The percentage of synapses to be drawn in the rendering'
    parser.add_argument('--synapse-percentage',
                        action='store', dest='synapse_percentage', type=float, help=arg_help)

    arg_help = 'Base image resolution'
    parser.add_argument('--image-resolution',
                        action='store', default=2048, type=int, dest='image_resolution',
                        help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @parse_arguments
####################################################################################################
def parse_arguments():
    """ Parse the command line arguments and return a clean list after the '--'.
    :return:
        The list of arguments.
    """

    system_args = sys.argv
    sys.argv = system_args[system_args.index("--") + 0:]
    return parse_command_line_arguments()


####################################################################################################
# @get_color_coded_synapse_list
####################################################################################################
def get_color_coded_synapse_list(synapse_json_file):

    # The returning synapse list
    synapse_list = list()

    # Load the data from the JSON file
    try:
        f = open(synapse_json_file)
    except FileNotFoundError:
        print("The file %s is NOT found!" % synapse_json_file)
        exit(0)

    # Load all the data from the file
    import json
    data = json.load(f)

    # Get all the keys and the corresponding arrays
    keys = data.keys()

    # Create the synapses list
    for key in keys:
        group = list()
        for i in data[key]:
            group.append(int(i))
        synapse_list.append([key, group])

    # Close the file
    f.close()

    # Return the synapse list
    return synapse_list


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    args = parse_arguments()

    nmv.logger.header('Synaptome generation')

    # Clear the scene
    nmv.logger.info('Cleaning Scene')
    nmv.scene.clear_scene()

    material_type = nmv.enums.Shader.LAMBERT_WARD

    # Read the circuit
    nmv.logger.info('Loading circuit')
    circuit = Circuit(args.circuit_config)

    # Create the neuron mesh
    nmv.logger.info('Creating the neuron mesh')
    neuron_mesh = neuron_data.create_neuron_mesh(
        circuit=circuit, gid=args.gid, color=nmv.utilities.confirm_rgb_color(args.neuron_color),
        material_type=material_type)

    # Create the synapses mesh
    nmv.logger.info('Creating the synapse mesh')
    color_coded_synapses_list = nmv.bbp.get_excitatory_and_inhibitory_synapses_color_coded_list(
        circuit=circuit, gid=int(args.gid))

    transformation = nmv.bbp.get_neuron_transformation_matrix(circuit=circuit, gid=int(args.gid))
    synapses_mesh = nmv.bbp.create_color_coded_synapses_mesh(
        circuit=circuit, color_coded_synapses_list=color_coded_synapses_list,
        synapse_size=args.synapse_size,
        inverted_transformation=transformation.inverted(),
        material_type=material_type)

    # Render the image
    nmv.logger.info('Rendering image')
    nmv.rendering.render(
        camera_view=nmv.enums.Camera.View.FRONT,
        bounding_box=nmv.bbox.compute_scene_bounding_box_for_meshes(),
        image_resolution=args.image_resolution,
        image_name=str(args.gid),
        image_directory=args.output_directory)

    # Export the scene into a blender file for interactive visualization
    nmv.logger.info('Exporting the scene')
    nmv.file.export_scene_to_blend_file(output_directory=args.output_directory,
                                        output_file_name=str(args.gid))
