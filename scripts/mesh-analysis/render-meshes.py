####################################################################################################
# Copyright (c) 2022, EPFL / Blue Brain Project
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


# Blender imports
import bpy

# NeuroMorphoVis imports
import nmv.interface
import nmv.shading
import nmv.scene
import nmv.bbox
import nmv.rendering
import nmv.enums
import nmv.utilities

sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/../../' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/utilities' % (os.path.dirname(os.path.realpath(__file__)))))

import data_utilities as dutils
import rendering_utilities as rutils


####################################################################################################
# @add_light
####################################################################################################
def add_light(bbox,
              camera_view=nmv.enums.Camera.View.FRONT,
              power=1e6):

    # Deselect all
    nmv.scene.deselect_all()

    # Create the light source
    bpy.ops.object.light_add(type='POINT', radius=1, location=(0, 0, 0))

    # Get a reference to the light source
    light_reference = nmv.scene.get_active_object()

    # Adjust the power
    light_reference.data.energy = power

    # Shadow radius
    light_reference.data.shadow_soft_size = 100

    # Front view
    if camera_view is nmv.enums.Camera.View.FRONT:
        light_reference.location[0] = bbox.center[0]
        light_reference.location[1] = bbox.center[1]
        light_reference.location[2] = bbox.center[2]

        light_reference.rotation_euler[0] = 1.5708
        light_reference.rotation_euler[0] = -1.5708
        light_reference.rotation_euler[0] = -1.5708

    elif nmv.enums.Camera.View.SIDE:

        # Location
        light_reference.location[0] = bbox.center[0] - (0.5 * bbox.bounds[0])
        light_reference.location[1] = bbox.center[1]
        light_reference.location[2] = bbox.center[2]

        # Orientation
        light_reference.rotation_euler[0] = 1.5708
        light_reference.rotation_euler[1] = -1.5708
        light_reference.rotation_euler[2] = -1.5708

    elif nmv.enums.Camera.View.TOP:
        light_reference.location[0] = bbox.center[0]
        light_reference.location[0] = bbox.center[1]
        light_reference.location[0] = bbox.center[2]
        light_reference.rotation_euler[0] = 1.5708
        light_reference.rotation_euler[0] = -1.5708
        light_reference.rotation_euler[0] = -1.5708

    else:
        light_reference.location[0] = bbox.center[0]
        light_reference.location[1] = bbox.center[1]
        light_reference.location[2] = bbox.center[2]

    # Return the light source
    return light_reference


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
    description = 'This script renders a list of input meshes into image or a movie'
    parser = argparse.ArgumentParser(description=description)

    # Input mesh path
    arg_help = 'The input directory that will contains all the meshes that will be rendered'
    parser.add_argument('--input-directory', action='store', help=arg_help)

    # Output directory
    arg_help = 'Output directory, where the final image/movies and scene will be stored'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    arg_help = 'The mesh color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--mesh-color', action='store', help=arg_help)

    arg_help = 'Camera view: top, front or side'
    parser.add_argument('--camera-view', action='store', default='front', help=arg_help)

    arg_help = 'Wireframe thickness'
    parser.add_argument('--wireframe-thickness', action='store', default=0.02, type=float,
                        help=arg_help)

    arg_help = 'Base full-view resolution'
    parser.add_argument('--resolution', action='store', default=2000, type=int, help=arg_help)

    arg_help = 'Export blender scene'
    parser.add_argument('--export-blend', action='store_true', default=False, help=arg_help)

    # Wireframe or not
    arg_help = 'If this option is set, the wireframe of the mesh will be rendered'
    parser.add_argument('--wireframe', action='store_true', default=False, help=arg_help)

    arg_help = 'If this option is set, a 360 of the mesh will be rendered'
    parser.add_argument('--render-360', action='store_true', default=False, help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Create the output hierarchy
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)
    intermediate_directory = '%s/intermediate-images' % args.output_directory
    if not os.path.exists(intermediate_directory):
        os.makedirs(intermediate_directory)
    images_directory = '%s/images' % args.output_directory
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)
    scenes_directory = '%s/scenes' % args.output_directory
    if not os.path.exists(scenes_directory):
        os.makedirs(scenes_directory)
    movies_directory = '%s/movies' % args.output_directory
    if not os.path.exists(movies_directory):
        os.makedirs(movies_directory)

    # Clear the scene
    nmv.scene.clear_scene()

    # Get all the meshes in the path, either obj or ply
    list_meshes = nmv.file.get_files_in_directory(args.input_directory, file_extension='.obj')
    list_meshes.extend(nmv.file.get_files_in_directory(args.input_directory, file_extension='.ply'))
    list_meshes.extend(nmv.file.get_files_in_directory(args.input_directory, file_extension='.stl'))

    # For every mesh in the list
    for mesh_file in list_meshes:

        # Clear the scene to render a new mesh
        nmv.scene.clear_scene()

        # Load the skinned astrocyte mesh
        mesh_object = nmv.file.import_mesh('%s/%s' % (args.input_directory, mesh_file))

        # Parse the color value
        mesh_color = nmv.utilities.parse_color_from_argument(args.mesh_color)

        # Get the camera view
        camera_view = dutils.get_view(args.camera_view)

        # Render the mesh
        rutils.render_mesh_with_wireframe_shader(mesh_object=mesh_object,
                                                 output_directory=images_directory,
                                                 mesh_color=mesh_color,
                                                 resolution=args.resolution,
                                                 camera_view=camera_view)

        # Save the scene into a Blender file
        if args.export_blend:
            nmv.file.export_scene_to_blend_file(
                output_directory=scenes_directory, output_file_name=mesh_object.name)




    #




    #camera_view = nmv.enums.Camera.View.SIDE

    # nmv.shading.create_lambert_ward_illumination()
    #add_light(bbox=mesh_bbox, camera_view=camera_view)

