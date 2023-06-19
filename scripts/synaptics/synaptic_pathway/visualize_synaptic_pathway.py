####################################################################################################
# Copyright (c) 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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

    arg_help = 'Output directory, where the final artifacts will be generated'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'BBP circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)

    arg_help = 'The GID of the pre-synaptic neuron'
    parser.add_argument('--pre-synaptic-neuron-gid',
                        action='store', dest='pre_gid', type=int, help=arg_help)

    arg_help = 'The GID of the post-synaptic neuron'
    parser.add_argument('--post-synaptic-neuron-gid',
                        action='store', dest='post_gid', type=int, help=arg_help)

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
# @get_branch_radius_type
####################################################################################################
def get_branch_radius_type(in_type):
    """Gets the type of the radii of the branches of the neuron.

    :param in_type:
        The input string that defines the type from the interface.
    :return:
        The corresponding enumerator.
    """

    if 'original' in in_type.lower():
        return nmv.enums.Skeleton.Radii.ORIGINAL
    elif 'scaled' in in_type.lower():
        return nmv.enums.Skeleton.Radii.SCALED
    elif 'unified' in in_type.lower():
        return nmv.enums.Skeleton.Radii.UNIFIED
    else:
        return nmv.enums.Skeleton.Radii.ORIGINAL


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
    nmv.scene.clear_scene(deep_delete=True)

    material_type = nmv.enums.Shader.FLAT

    # Read the circuit
    nmv.logger.info('Loading circuit')
    bluepy_circuit = Circuit(args.circuit_config)

    # Make a NMV circuit
    circuit = nmv.bbp.BBPCircuit(circuit_config=args.circuit_config)

    # Get the radii of the branches
    branches_radii_type = get_branch_radius_type(in_type=args.branches_radii_type)

    # Create the mesh of the pre-synaptic neuron at the global coordinates
    nmv.logger.info('Creating the pre-synaptic neuron mesh')
    pre_synaptic_dendrites_color = nmv.utilities.confirm_rgb_color_from_color_string(
        args.pre_synaptic_dendrites_color)
    pre_synaptic_axons_color = nmv.utilities.confirm_rgb_color_from_color_string(
        args.pre_synaptic_axons_color)
    pre_synaptic_neuron_mesh = nmv.bbp.nmv.bbp.create_neuron_mesh_in_circuit(
        circuit=circuit, gid=args.pre_gid,
        branch_radius_type=branches_radii_type,
        branch_radius=args.unified_branches_radius,
        branch_radius_scale_factor=args.branches_radius_scale,
        soma_color=pre_synaptic_dendrites_color,
        basal_dendrites_color=pre_synaptic_dendrites_color,
        apical_dendrites_color=pre_synaptic_dendrites_color,
        axons_color=pre_synaptic_axons_color,
        material_type=material_type)

    nmv.logger.info('Creating the post-synaptic neuron mesh')
    post_synaptic_dendrites_color = nmv.utilities.confirm_rgb_color_from_color_string(
        args.post_synaptic_dendrites_color)
    post_synaptic_axons_color = nmv.utilities.confirm_rgb_color_from_color_string(
        args.post_synaptic_axons_color)
    post_synaptic_neuron_mesh = nmv.bbp.create_neuron_mesh_in_circuit(
        circuit=circuit, gid=args.post_gid,
        branch_radius_type=branches_radii_type,
        branch_radius=args.unified_branches_radius,
        branch_radius_scale_factor=args.branches_radius_scale,
        axon_branching_order=1,
        soma_color=post_synaptic_dendrites_color,
        basal_dendrites_color=post_synaptic_dendrites_color,
        apical_dendrites_color=post_synaptic_dendrites_color,
        axons_color=post_synaptic_axons_color,
        material_type=material_type)

    # Get the transformations of the pre- and post-synaptic neurons
    pre_synaptic_transformation = circuit.get_neuron_transformation_matrix(
        gid=args.pre_gid)
    post_synaptic_transformation = circuit.get_neuron_transformation_matrix(
        gid=args.post_gid)

    # Since the focus is given to the pre-synaptic neuron; it is the originally loaded one,
    # transform the post-synaptic neuron w.r.t to the pre synaptic one
    if post_synaptic_neuron_mesh is not None:
        post_synaptic_neuron_mesh.matrix_world = post_synaptic_transformation
        post_synaptic_neuron_mesh.matrix_world = \
            pre_synaptic_transformation.inverted() @ post_synaptic_neuron_mesh.matrix_world

    # Create the synapses mesh
    nmv.logger.info('Creating the synapse mesh')
    # Initially, try to get a list of synapses shared between the two cells
    shared_synapses_ids = circuit.get_shared_synapses_ids_between_two_neurons(
        pre_gid=args.pre_gid, post_gid=args.post_gid)

    # Create the shared group
    synapse_groups = list()
    synapse_groups.append(
        nmv.bbp.get_shared_synapses_group_between_two_neurons(
            circuit=circuit, pre_gid=args.pre_gid, post_gid=args.post_gid,
            color=args.synapses_color))

    nmv.logger.info('Adding synapses to the scene')
    nmv.bbp.create_color_coded_synapses_particle_system(
        circuit=circuit, synapse_groups=synapse_groups,
        synapse_radius=args.synapse_radius,
        synapses_percentage=100,
        inverted_transformation=pre_synaptic_transformation.inverted(),
        material_type=material_type)

    # Render the image
    nmv.logger.info('Rendering image')
    nmv.rendering.render(
        camera_view=nmv.enums.Camera.View.FRONT,
        bounding_box=nmv.bbox.compute_scene_bounding_box_for_meshes(),
        image_resolution=args.image_resolution,
        image_name='synaptic_pathways_%s-%s' % (str(args.pre_gid), args.pre_gid),
        image_directory=args.output_directory)

    # Export the scene into a blender file for interactive visualization
    if args.save_blend_file:
        nmv.logger.info('Saving into a .BLEND file [%s/%s-%s.blend]' %
                        (args.output_directory, str(args.pre_gid), args.pre_gid))
        nmv.file.export_scene_to_blend_file(
            output_directory=args.output_directory,
            output_file_name='%s-%s' % (str(args.pre_gid), args.pre_gid))
