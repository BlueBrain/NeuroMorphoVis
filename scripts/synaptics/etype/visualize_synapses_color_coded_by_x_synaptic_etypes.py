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

# BBP imports
from bluepy import Circuit

# Internal imports
import nmv.bbox
import nmv.bbp
import nmv.enums
import nmv.rendering
import nmv.scene
import nmv.utilities


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

    arg_help = 'BBP circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)

    arg_help = 'The GID of the post-synaptic neuron'
    parser.add_argument('--gid',
                        action='store', dest='gid', type=int, help=arg_help)

    arg_help = 'A JSON file containing the color-map of the synapses based on the mtypes of the ' \
               'pre-synaptic neuron in the following format: ' \
               '{MTYPE_0: HEX_COLOR_0, MTYPE_1: HEX_COLOR_1, ...}'
    parser.add_argument('--synapses-color-map',
                        action='store', dest='synapses_color_map', help=arg_help)

    arg_help = 'Output directory, where the final artifacts will be generated'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'Neuron color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--neuron-color',
                        action='store', dest='neuron_color', help=arg_help)

    arg_help = 'Display the synapses based on the etypes of the pre- or the post-synaptic neurons'
    parser.add_argument('--pre-or-post',
                        action='store', dest='pre_or_post', help=arg_help)

    arg_help = 'If this variable is set to yes, we will use the UNIFIED_NEURON_RADIUS value for ' \
               'all the branches'
    parser.add_argument('--unify-branches-radii',
                        dest='unify_branches_radii', action='store_true', default=False,
                        help=arg_help)

    arg_help = 'The value of the branches unified radius (in um)'
    parser.add_argument('--unified-branches-radius',
                        action='store', dest='unified_branches_radius', type=float, help=arg_help)

    arg_help = 'The branching order of the axon. By default, it is 1 to highlight the synapses'
    parser.add_argument('--axon-branching-order',
                        action='store', dest='axon_branching_order', type=int, default=10000,
                        help=arg_help)

    arg_help = 'Synapse radius (in um)'
    parser.add_argument('--synapse-radius',
                        action='store', dest='synapse_radius', type=float, help=arg_help)

    arg_help = 'The percentage of synapses to be drawn in the rendering'
    parser.add_argument('--synapse-percentage',
                        action='store', dest='synapse_percentage', type=float, help=arg_help)

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
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    system_args = sys.argv
    sys.argv = system_args[system_args.index("--") + 0:]
    args = parse_command_line_arguments()

    # Clear the scene
    nmv.logger.info('Cleaning Scene')
    nmv.scene.clear_scene()

    material_type = nmv.enums.Shader.LAMBERT_WARD

    # Read the circuit
    nmv.logger.info('Loading circuit')
    circuit = Circuit(args.circuit_config)

    # Creating the synapse group from the mesh
    nmv.logger.info('Loading synapses from the synapses file ')
    if args.pre_or_post == 'pre':
        synapse_groups = nmv.bbp.create_color_coded_synapse_groups_by_pre_etype(
            circuit=circuit, post_gid=int(args.gid), mtype_color_dict=
            nmv.bbp.get_color_coded_synapse_dict(args.synapses_color_map))
    else:
        synapse_groups = nmv.bbp.create_color_coded_synapse_groups_by_post_etype(
            circuit=circuit, pre_gid=int(args.gid), mtype_color_dict=
            nmv.bbp.get_color_coded_synapse_dict(args.synapses_color_map))

    # Create the neuron mesh
    nmv.logger.info('Creating the neuron mesh')
    neuron_color = nmv.utilities.confirm_rgb_color_from_color_string(args.neuron_color)
    neuron_mesh = nmv.bbp.create_symbolic_neuron_mesh_in_circuit(
        circuit=circuit, gid=args.gid,

        unified_radius=args.unify_branches_radii,
        branch_radius=args.unified_branches_radius,
        soma_color=neuron_color,
        basal_dendrites_color=neuron_color,
        apical_dendrites_color=neuron_color,
        axons_color=neuron_color,
        material_type=material_type,
        axon_branching_order=args.axon_branching_order)

    neuron_mesh2 = nmv.bbp.create_symbolic_neuron_mesh_in_circuit(
        circuit=circuit, gid=8848,
        unified_radius=args.unify_branches_radii,
        branch_radius=args.unified_branches_radius,
        soma_color=neuron_color,
        basal_dendrites_color=neuron_color,
        apical_dendrites_color=neuron_color,
        axons_color=neuron_color,
        material_type=material_type,
        axon_branching_order=args.axon_branching_order)

    # Create the synapses mesh
    nmv.logger.info('Creating the synapse mesh')
    transformation = nmv.bbp.get_neuron_transformation_matrix(circuit=circuit, gid=int(args.gid))
    synapses_mesh = nmv.bbp.create_color_coded_synapses_particle_system(
        circuit=circuit, synapse_groups=synapse_groups,
        synapse_radius=args.synapse_radius,
        synapses_percentage=args.synapse_percentage,
        inverted_transformation=transformation.inverted(),
        material_type=material_type)

    # Render the image
    nmv.logger.info('Rendering image')
    nmv.rendering.render(
        camera_view=nmv.enums.Camera.View.FRONT,
        bounding_box=nmv.bbox.compute_scene_bounding_box_for_meshes(),
        image_resolution=args.image_resolution,
        image_name='%s-%s' % (str(args.gid), args.pre_or_post),
        image_directory=args.output_directory)

    # Export the scene into a blender file for interactive visualization
    if args.save_blend_file:
        nmv.logger.info('Saving into a .BLEND file [%s/%s-%s.blend]' %
                        (args.output_directory, str(args.gid), args.pre_or_post))
        nmv.file.export_scene_to_blend_file(
            output_directory=args.output_directory,
            output_file_name='%s-%s' % (str(args.gid), args.pre_or_post))
