####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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

import sys, os
import argparse

import bpy
import nmv
import nmv.file
import nmv.rendering
import nmv.scene
import nmv.mesh


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments():
    """
    Parses the command line arguments.
    NOTE: We do not define a destination to facilitate printing to a string and doing another
    iteration of parsing for blender.

    :return: A structure with all the system options.
    """

    # Create an argument parser, and then add the options one by one
    parser = argparse.ArgumentParser()

    # Output directory
    arg_help = 'Output directory'
    parser.add_argument('--output-directory',
                        action='store', default=None,
                        help=arg_help)

    # Morphology directory
    arg_help = 'Morphology (.blend) directory containing multiple files'
    parser.add_argument('--morphology-directory',
                        action='store', default=None,
                        help=arg_help)

    # Distance between the morphologies
    arg_help = 'Distance between the mtype groups'
    parser.add_argument('--distance',
                        action='store', type=float, default=300,
                        help=arg_help)

    # Frame name
    arg_help = 'The name of the output image'
    parser.add_argument('--frame-name',
                        action='store', default='image',
                        help=arg_help)

    # Base resolution of the frame
    arg_help = 'Resolution scale factor of the frame'
    parser.add_argument('--resolution-scale-factor',
                        action='store', type=int, default=5,
                        help=arg_help)

    # Parse the arguments, and return a list of them
    return parser.parse_args()


####################################################################################################
# @load_morphologies
####################################################################################################
def load_morphologies(meshes_directory):

    # List all the files in the directory (.blend)
    mesh_files = nmv.file.ops.get_files_in_directory(directory=meshes_directory,
        file_extension='blend')

    # Sort
    mesh_files.sort()

    # A list of all the meshes
    meshes = []

    for mesh_file in mesh_files:

        # Load the mesh
        mesh_objects = nmv.file.import_object_from_blend_file(meshes_directory, mesh_file)

        # Join all the meshes into a single mesh
        mesh_objects = [nmv.mesh.ops.join_mesh_objects(mesh_objects, mesh_file)]

        # If the meshes are merged into a single object, we must override the texture values
        # Update the texture space of the created mesh
        scene_object = mesh_objects[0]
        scene_object.select = True
        bpy.context.scene.objects.active = scene_object
        bpy.context.object.data.use_auto_texspace = False
        bpy.context.object.data.texspace_size[0] = 5
        bpy.context.object.data.texspace_size[1] = 5
        bpy.context.object.data.texspace_size[2] = 5
        scene_object.select = False

        # Clear the default scene
        nmv.scene.ops.clear_default_scene()

        # Get the mesh from all the objects in the scene
        for scene_object in mesh_objects:
            if scene_object.type == 'MESH':
                meshes.append(scene_object)
            else:
                nmv.scene.ops.delete_list_objects([scene_object])

    return meshes


####################################################################################################
# @how_many_items_in_list
####################################################################################################
def how_many_items_in_list(mtype_list, layer_sub_string):
    """
    Find how many mtypes in the list.

    :param mtype_list:
    :param layer_sub_string:
    :return:
    """
    return [s for s in mtype_list if layer_sub_string in s]


####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Ignore blender extra arguments required to launch blender given to the command line interface
    args = sys.argv
    sys.argv = args[args.index("--") + 1:]

    # Parse the command line arguments, filter them and report the errors
    args = parse_command_line_arguments()

    # Column dimensions
    # <layer id="1” thickness (µm) = "164.94915873"/>
    # <layer id="2” thickness (µm) = "148.87602025"/>
    # <layer id="3” thickness (µm) = "352.92508322"/>
    # <layer id="4” thickness (µm) = "189.57183895"/>
    # <layer id="5” thickness (µm) = "525.05585701"/>
    # <layer id="6” thickness (µm) = "700.37845971”/>

    layer_1_height = 164.94915873
    layer_2_height = 148.87602025
    layer_3_height = 352.92508322
    layer_4_height = 189.57183895
    layer_5_height = 525.05585701
    layer_6_height = 700.37845971

    # Assuming that layer 6 starts at y_cords = 0
    layer_6_y_center = layer_6_height / 2.0
    layer_5_y_center = layer_6_y_center + (layer_6_height / 2.0) + (layer_5_height / 2.0)
    layer_4_y_center = layer_5_y_center + (layer_5_height / 2.0) + (layer_4_height / 2.0)
    layer_3_y_center = layer_4_y_center + (layer_4_height / 2.0) + (layer_3_height / 2.0)
    layer_2_y_center = layer_3_y_center + (layer_3_height / 2.0) + (layer_2_height / 2.0)
    layer_1_y_center = layer_2_y_center + (layer_2_height / 2.0) + (layer_1_height / 2.0)

    # Clear the default scene
    nmv.scene.ops.clear_scene()

    # Get all the mtypes from the directories
    mtypes = os.listdir(args.morphology_directory)

    # Sort the mtypes
    mtypes.sort()

    # Load the meshes from the blend files
    meshes = load_morphologies(args.morphology_directory)

    # Get the number of meshes
    n_meshes = len(meshes)

    if n_meshes == 0:
        print('Zero meshes loaded!')
        exit(0)

    # Shift the cells
    for i, mesh in enumerate(meshes):

        # Compute the translation factor
        x_translation = (i * args.distance)

        # Deselect all the cells in the scene
        nmv.scene.ops.deselect_all()

        # Get the location of the mesh
        mesh_location = nmv.scene.ops.get_object_location(mesh)

        # Update the x-coordinate
        mesh_location[0] = x_translation

        # Relocate the mesh
        nmv.scene.ops.set_object_location(mesh, mesh_location)

    # Export the scene to keep a reference for it later
    nmv.file.export_object_to_blend_file(None, args.output_directory, args.frame_name)

    # Render the scene
    rendering_path = '%s/%s' % (args.output_directory, args.frame_name)
    camera = nmv.rendering.Camera()
    camera.render_scene_to_scale(
        scale_factor=args.resolution_scale_factor,image_name = rendering_path,
        keep_camera_in_scene=True)

