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
# @create_neuron_mesh
####################################################################################################
def create_neuron_mesh(circuit,
                       gid,
                       neuron_color,
                       output_directory):
    """Creates the mesh of the neuron.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param neuron_color:
        The color of the neuron in a RGB Vector((R, G, B)) format
    :return:
    """
    # Get the morphology file path from its GID
    # We must ensure that the GID is integer, that's why the cast is there
    h5_morphology_path = circuit.morph.get_filepath(int(gid))

    # Use the H5 morphology loader to load this file
    # Don't center the morphology, as it is assumed to be cleared and reviewed by the team
    h5_reader = nmv.file.H5Reader(h5_file=h5_morphology_path, center_morphology=False)
    morphology = h5_reader.read_file()

    # Adjust the label to be set according to the GID not the morphology label
    morphology.label = str(gid)

    # Create default NMV options
    nmv_options = nmv.options.NeuroMorphoVisOptions()
    nmv_options.io.statistics_directory = output_directory
    # nmv_options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.UNIFIED
    # nmv_options.morphology.samples_unified_radii_value = 1.0
    nmv_options.mesh.neuron_objects_connection = nmv.enums.Meshing.ObjectsConnection.CONNECTED
    nmv_options.shading.mesh_material = nmv.enums.shading_enums.Shader.FLAT # shader
    nmv_options.mesh.soma_type = nmv.enums.Soma.Representation.META_BALLS

    # Create a meta balls meshing builder, and ignore the watertight checks
    # mesh_builder = nmv.builders.MetaBuilder(morphology=morphology, options=nmv_options,
    #                                         ignore_watertightness=True)

    mesh_builder = nmv.builders.SkinningBuilder(morphology=morphology, options=nmv_options)

    # Create the neuron mesh
    neuron_mesh = mesh_builder.reconstruct_mesh()

    # Add the material top the reconstructed mesh
    neuron_material = color_map.create_material_from_color_string(
        color_string=neuron_color, material_name='neuron_material', material_type=shader)
    nmv.shading.set_material_to_object(mesh_object=neuron_mesh, material_reference=neuron_material)

    # Return a reference to the neuron mesh
    return neuron_mesh


####################################################################################################
# @create_projection_synapses_mesh
####################################################################################################
def create_projection_synapses_mesh(circuit,
                                    post_gid,
                                    projection_target,
                                    synapse_percentage,
                                    synapse_size,
                                    synapse_color):
    """Creates a synapse mesh for the specified projection.

    :param circuit:
        A given BBP circuit.
    :param post_gid:
        The GID of the post synaptic cell.
    :param projection_target:
        THe target name of the projection.
    :param synapse_percentage:
        The percentage of the synapses.
    :param synapse_size:
        The size of the synapses.
    :param synapse_color:
        The RGB color of the synapses in the string format, separated by underscores.
    :return:
    """

    # Note that projection has the same methods of circuit.connectome but applied to the projection
    projection = circuit.projection(projection_target)

    # Get all the afferent synapses
    afferent_synapses = projection.afferent_synapses(
            gid=int(post_gid),
            properties=[Synapse.POST_X_CENTER, Synapse.POST_Y_CENTER, Synapse.POST_Z_CENTER])

    # Values and to list
    afferent_synapses = list(afferent_synapses.values)

    # Construct the synapse list in a Vector format
    synapse_list = list()
    for synapse in afferent_synapses:
        synapse_list.append(Vector((synapse[0], synapse[1], synapse[2])))

    # Get the cell transformation matrix
    transformation = circuit_data.get_cell_transformation(circuit=circuit, gid=post_gid)

    # Invert the transformation matrix
    inverted_transformation = transformation.inverted()

    # We need the color and the position to draw the synaptome
    synapse_objects = list()
    synapse_groups = list()

    # Do it for all the synapses
    for i, synapse in enumerate(synapse_list):

        # Show progress
        nmv.utilities.time_line.show_iteration_progress('Synapses', i, len(synapse_list))

        # Random selection
        if synapse_percentage < random.uniform(0, 100):
            continue

        # Position
        post_synaptic_position = synapse
        position = inverted_transformation @ post_synaptic_position

        # A synapse sphere object
        synapse_sphere = nmv.geometry.create_ico_sphere(
            radius=synapse_size, location=position, subdivisions=3, name='synapse_%d' % i)

        # Add the sphere to the group
        synapse_objects.append(synapse_sphere)

        # Group every 100 objects into a single group
        if i % 50 == 0:
            # Join the meshes into a group
            synapse_group = nmv.mesh.join_mesh_objects(
                mesh_list=synapse_objects, name='group_%d' % (i % 100))

            # Add the group to the list
            synapse_groups.append(synapse_group)

            # Clear the object list
            synapse_objects.clear()

    # Join the meshes into a group
    synapse_group = nmv.mesh.join_mesh_objects(
        mesh_list=synapse_objects, name='group_%d' % (i % 100))

    # Add the group to the list
    synapse_groups.append(synapse_group)

    # Done
    nmv.utilities.time_line.show_iteration_progress('Synapses',
                                                    len(synapse_list), len(synapse_list), done=True)

    # Join the meshes into a group
    synapses_mesh = nmv.mesh.join_mesh_objects(mesh_list=synapse_groups, name='synapses')

    # Material
    synapse_material = color_map.create_material_from_color_string(
        color_string=synapse_color, material_name='synapse_material', material_type=shader)
    nmv.shading.set_material_to_object(mesh_object=synapses_mesh,
                                       material_reference=synapse_material)

    # Return a reference to the synapse mesh
    return synapses_mesh


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

    color_coded_synapses_list = get_color_coded_synapse_list(args.synapses_file)

    # Get the cell transformation matrix
    transformation = nmv.bbp.get_neuron_transformation_matrix(circuit=circuit, gid=int(args.gid))

    synapses_mesh = nmv.bbp.create_color_coded_synapses_mesh(
        circuit=circuit, color_coded_synapses_list=color_coded_synapses_list,
        synapse_size=args.synapse_size, inverted_transformation=transformation.inverted(),
        material_type=material_type)


    # Render the image

    # Save the Blender scene for interactive visualization
    # Export the scene into a blender file
    prefix = 'example'#'synapses_%s_%s' % (args.projection, str(args.gid))
    nmv.logger.info('Exporting %s' % prefix)
    nmv.file.export_scene_to_blend_file(output_directory=args.output_directory,
                                        output_file_name=prefix)

    exit(0)


    # Parse the gids from the config file
    gids = args.gids.split('_')

    # Produce an image for every gid in the list
    for gid in gids:
        nmv.logger.info('GID: %s' % str(gid))

        # Clear the scene
        nmv.logger.info('Cleaning Scene')
        nmv.scene.clear_scene()

        # Read the circuit
        nmv.logger.info('Loading circuit')
        circuit = Circuit(args.circuit_config)

        # Create neuron meshes
        nmv.logger.info('Creating neuron mesh')
        neuron_mesh = create_neuron_mesh(
            circuit=circuit, gid=gid, neuron_color=args.neuron_color,
            output_directory=args.output_directory)

        # Create synapses meshes
        nmv.logger.info('Creating synapse mesh')
        synapse_mesh = create_projection_synapses_mesh(
            circuit=circuit, post_gid=int(gid), projection_target=args.projection,
            synapse_percentage=args.synapse_percentage, synapse_size=args.synapse_size,
            synapse_color=args.synapse_color)

        # Compute the mesh bounding box
        bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Export the scene into a blender file
        prefix = 'projection_%s_%s_%dp' % (args.projection, str(gid), args.synapse_percentage)
        nmv.logger.info('Exporting %s' % prefix)
        nmv.file.export_scene_to_blend_file(output_directory=args.output_directory,
                                            output_file_name=prefix)

        # Render the image
        nmv.logger.info('Rendering %s' % prefix)
        nmv.rendering.render(
            camera_view=nmv.enums.Camera.View.FRONT,
            bounding_box=bounding_box,
            image_resolution=args.image_resolution,
            image_name=prefix,
            image_directory=args.output_directory)