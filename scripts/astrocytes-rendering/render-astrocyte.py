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
import argparse

# NeuroMorphoVis imports
import nmv.scene
import nmv.enums
import nmv.consts
import nmv.shading
import nmv.bbox
import nmv.rendering
import nmv.mesh
import nmv.utilities


####################################################################################################
# @get_astrocytes_paths_from_list
####################################################################################################
def get_astrocytes_paths_from_list(astrocytes_list):
    """Gets a list of all the astrocytes paths from the given list.

    :param astrocytes_list:
        Given file that contains a list of the astrocytes to be rendered.
    :return:
        A list of the astrocytes that will be rendered.
    """

    astrocytes_paths = list()

    file = open(astrocytes_list, 'r')
    for line in file:
        astrocytes_paths.append(line.replace('\n', '').replace(' ', ''))
    file.close()

    # Return the GIDs list
    return astrocytes_paths


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
    description = 'Rendering astrocytes'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Input directory, where the meshes will be found'
    parser.add_argument('--input-directory', action='store', help=arg_help)

    arg_help = 'Output directory, where the final image/movies and scene will be stored'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    arg_help = 'A list that contains all the names of the astrocytes'
    parser.add_argument('--astrocytes-list', action='store', help=arg_help)

    arg_help = 'Render the optimized version including the high quality rendering'
    parser.add_argument('--consider-optimized', action='store_true', default=False, help=arg_help)

    arg_help = 'Astrocyte color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--astrocyte-color', action='store', help=arg_help)

    arg_help = 'Base full-view resolution'
    parser.add_argument('--resolution', action='store', default=2000, type=int, help=arg_help)

    arg_help = 'Export blender scene'
    parser.add_argument('--export-blend', action='store_true', default=False, help=arg_help)

    # Parse the arguments
    return parser.parse_args()


################################################################################
# @ Main
################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Get the astrocytes
    astrocytes = get_astrocytes_paths_from_list(args.astrocytes_list)

    # For each astrocyte, do it
    for astrocyte in astrocytes:

        # Clear the scene
        nmv.scene.clear_scene()

        # Load the astrocyte mesh
        astrocyte_mesh = nmv.file.import_obj_file(
            input_directory=args.input_directory, input_file_name=astrocyte)

        # Rotate the astrocyte to adjust the orientation in front of the camera
        nmv.scene.rotate_object(astrocyte_mesh, 0, 0, 0)

        # Get the bounding box
        astrocyte_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Create the illumination
        nmv.shading.create_lambert_ward_illumination()

        # Create a simple shader
        mesh_material = nmv.shading.create_lambert_ward_material(
            name='astro', color=nmv.utilities.parse_color_from_argument(args.astrocyte_color))

        # Assign the wire-frame shader, using an input color
        nmv.shading.set_material_to_object(
            mesh_object=astrocyte_mesh, material_reference=mesh_material)

        # Create a wireframe
        wireframe_mesh = nmv.mesh.create_wire_frame(
            mesh_object=astrocyte_mesh, wireframe_thickness=0.05)

        # Create a wireframe shader
        wireframe_material = nmv.shading.create_lambert_ward_material(
            name='wireframe', color=nmv.consts.Color.BLACK)

        # Assign the wire-frame shader, using an input color
        nmv.shading.set_material_to_object(
            mesh_object=wireframe_mesh, material_reference=wireframe_material)

        # Render based on the bounding box
        nmv.rendering.render(bounding_box=astrocyte_bbox,
                             image_directory=args.output_directory,
                             image_resolution=args.resolution,
                             keep_camera_in_scene=True)

        # Save the final scene into a blender file
        nmv.file.export_scene_to_blend_file(output_directory=args.output_directory,
                                            output_file_name=astrocyte.replace('.obj', ''))
        # Assign the subsurface scattering shader

        # Render based on the bounding box

        # Done

    '''
    # Add a flat shader to forc NMV to switch to Blender workbench render
    shader = nmv.enums.Shader.LAMBERT_WARD

    # Neuron material
    neuron_material = color_map.create_neuron_material(neuron_color=args.neuron_color,
                                                       shader=shader)

    # Create the color-map dictionary of the synapses
    synaptome_color_map_materials = color_map.create_color_map(color_map_file=args.color_map_file,
                                                               material_type=shader)

    # Create the synaptome
    synaptome_mesh = synaptome.create_synaptome(
        circuit_config=args.circuit_config,
        gid=args.gid,
        synapse_size=args.synapse_size,
        synapse_percentage=args.synapse_percentage,
        synaptome_color_map_materials=synaptome_color_map_materials,
        neuron_material=neuron_material,
        show_excitatory_inhibitory=args.show_exc_inh)

    # Compute the mesh bounding box
    synaptome_bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

    # Create the dummy material to adjust the renderer
    dummy_material = color_map.create_dummy_material(shader=shader)

    # Create the output directory where the artifacts will be created
    output_directory = args.output_directory + '/%s' % synaptome_mesh.name

    # Create the output directory if it does not exist
    if not nmv.file.ops.path_exists(output_directory):
        nmv.file.ops.clean_and_create_directory(output_directory)

    # Render a 360 of the full view
    full_view_frames = rendering.render_synaptome_full_view_360(
        output_directory=output_directory, resolution=args.full_view_resolution)

    # Render a 360 of the soma close up
    close_up_frames = rendering.render_synaptome_close_up_on_soma_360(
        output_directory=output_directory, close_up_size=args.close_up_size,
        resolution=args.close_up_resolution)

    # Compose the 360 frames on the background
    frames_directory, composed_frames = rendering.compose_360_frames(
        full_view_frames=full_view_frames, close_up_frames=close_up_frames,
        background_image_file=args.background_image, output_directory=output_directory,
        bounding_box=synaptome_bounding_box)

    # Create a movie from the final frames
    rendering.create_movie(frames_directory=frames_directory, movie_name=synaptome_mesh.name,
                           output_directory=output_directory)

    # Export the scene into a blender file for reference
    nmv.file.export_scene_to_blend_file(output_directory=output_directory,
                                        output_file_name='%s' % synaptome_mesh.name)
    '''
