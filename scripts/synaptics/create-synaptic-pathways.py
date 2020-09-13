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
import os

sys.path.append(('%s/../../' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/core' % (os.path.dirname(os.path.realpath(__file__)))))

# Blender imports
import parsing
import color_map
import synaptic_pathways
import rendering

# NeuroMorphoVis imports
import nmv.scene
import nmv.file
import nmv.enums


################################################################################
# @ Main
################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parsing.parse_synaptic_pairs_command_line_arguments()

    # Parse the pairs file
    pairs = parsing.parse_synaptic_pairs(args.synaptic_pairs_file)

    # Make sure that the given output directory exists
    if not nmv.file.ops.path_exists(args.output_directory):
        nmv.file.ops.clean_and_create_directory(args.output_directory)

    # Create the meshes directory
    meshes_directory = '%s/meshes' % args.output_directory
    if not nmv.file.ops.path_exists(meshes_directory):
        nmv.file.ops.clean_and_create_directory(meshes_directory)

    # Create the scenes directory
    scenes_directory = '%s/scenes' % args.output_directory
    if not nmv.file.ops.path_exists(scenes_directory):
        nmv.file.ops.clean_and_create_directory(scenes_directory)

    # Create the images directory
    images_directory = '%s/images' % args.output_directory
    if not nmv.file.ops.path_exists(images_directory):
        nmv.file.ops.clean_and_create_directory(images_directory)

    shader = nmv.enums.Shader.ELECTRON_LIGHT

    # Create an image for every pair
    for pair in pairs:

        # Clear the scene
        nmv.scene.clear_scene()

        # Create the synaptic pathway scene
        synaptic_pathways.create_synaptic_pathway_scene(
            circuit_config=args.circuit_config, pre_gid=pair[0], post_gid=pair[1],
            output_directory=meshes_directory, synapse_size=args.synapse_size, shader=shader,
            pre_synaptic_neuron_color=parsing.parse_color(args.pre_neuron_color),
            post_synaptic_neuron_color=parsing.parse_color(args.post_neuron_color),
            synapses_color=parsing.parse_color(args.synapse_color))

        # Create a dummy
        dummy_material = color_map.create_dummy_material(shader=shader)

        # Render an image
        rendering.render_image(output_directory=images_directory,
                               image_name='%d_%d_pathways' % (pair[0], pair[1]),
                               resolution=args.image_resolution)

        # Save the final scene
        nmv.file.export_scene_to_blend_file(scenes_directory,
                                            '%d_%d_pathways' % (pair[0], pair[1]))
