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
import subprocess

# Blender imports
import bpy
from mathutils import Vector

# NeuroMorphoVis imports
import nmv.scene
import nmv.enums
import nmv.consts
import nmv.shading
import nmv.bbox
import nmv.rendering
import nmv.mesh
import nmv.utilities

sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/../../' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/core' % (os.path.dirname(os.path.realpath(__file__)))))

# Blender imports
import plotting


####################################################################################################
# @create_area_light_from_bounding_box
####################################################################################################
def create_area_light_from_bounding_box(location):
    """Create an area light source that is above the mesh

    :param mesh_bbox:
        Mesh bounding box.
    :return:
        Reference to the light source
    """

    # Deselect all
    nmv.scene.deselect_all()

    # Create the light source
    bpy.ops.object.light_add(type='AREA', radius=1, location=(0, 0, 0))

    # Get a reference to the light source
    light_reference = nmv.scene.get_active_object()

    # Adjust the position
    light_reference.location = location

    # Adjust the orientation
    light_reference.rotation_euler[0] = -1.5708

    # Adjust the power
    light_reference.data.energy = 1e5

    # Return the light source
    return light_reference


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
# @run_quality_checker
####################################################################################################
def run_quality_checker(mesh_path,
                        quality_checker_executable,
                        output_directory):
    """Runs the quality checker to create stats. about the mesh.

    :param mesh_path:
        The path to the mesh file.
    :param quality_checker_executable:
        The executable of Ultraliser checker.
    :param output_directory:
        The root output directory
    """

    # Make sure that this directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Construct the command
    command = '%s --mesh %s --output-directory %s' % \
              (quality_checker_executable, mesh_path, stats_output_directory)
    subprocess.call(command, shell=True)


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

    arg_help = 'Render the artistic version with high quality rendering'
    parser.add_argument('--artistic', action='store_true', default=False, help=arg_help)

    arg_help = 'Astrocyte color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--astrocyte-color', action='store', help=arg_help)

    arg_help = 'Wireframe thickness'
    parser.add_argument('--wireframe-thickness', action='store', default=0.02, type=float, help=arg_help)

    arg_help = 'Base full-view resolution'
    parser.add_argument('--resolution', action='store', default=2000, type=int, help=arg_help)

    arg_help = 'Export blender scene'
    parser.add_argument('--export-blend', action='store_true', default=False, help=arg_help)

    arg_help = 'Quality checker executable'
    parser.add_argument('--quality-checker-executable', action='store', help=arg_help)

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

    # For each astrocyte, do it
    for astrocyte in astrocytes:

        # Clear the scene
        nmv.scene.clear_scene()

        # Load the astrocyte mesh
        astrocyte_mesh = nmv.file.import_obj_file(
            input_directory=args.input_directory, input_file_name=astrocyte)

        # Rotate the astrocyte to adjust the orientation in front of the camera
        nmv.scene.rotate_object(astrocyte_mesh, 0, 0, 0)

        # Get the bounding box and compute the unified one, to render the astrocyte in the middle
        astrocyte_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()
        astrocyte_bbox = nmv.bbox.compute_unified_bounding_box(astrocyte_bbox)

        # Create the illumination
        nmv.shading.create_lambert_ward_illumination()

        # Create a simple shader
        color = nmv.utilities.parse_color_from_argument(args.astrocyte_color)
        mesh_material = nmv.shading.create_lambert_ward_material(
            name='astro', color=nmv.utilities.parse_color_from_argument(args.astrocyte_color))

        # Assign the wire-frame shader, using an input color
        nmv.shading.set_material_to_object(
            mesh_object=astrocyte_mesh, material_reference=mesh_material)

        # Create a wireframe
        wireframe_mesh = nmv.mesh.create_wire_frame(
            mesh_object=astrocyte_mesh, wireframe_thickness=args.wireframe_thickness)

        # Create a wireframe shader
        wireframe_material = nmv.shading.create_lambert_ward_material(
            name='wireframe', color=nmv.consts.Color.BLACK)

        # Assign the wire-frame shader, using an input color
        nmv.shading.set_material_to_object(
            mesh_object=wireframe_mesh, material_reference=wireframe_material)

        # Set the background to WHITE for the compositing
        bpy.context.scene.render.film_transparent = False
        bpy.context.scene.world.color[0] = 10
        bpy.context.scene.world.color[1] = 10
        bpy.context.scene.world.color[2] = 10

        # Render based on the bounding box
        nmv.rendering.render(bounding_box=astrocyte_bbox,
                             image_directory=intermediate_directory,
                             image_name=astrocyte_mesh.name,
                             image_resolution=args.resolution,
                             keep_camera_in_scene=True)

        # Save the final scene into a blender file
        if args.export_blend:
            nmv.file.export_scene_to_blend_file(output_directory=scenes_directory,
                                                output_file_name=astrocyte_mesh.name)

        # Run the quality checker app
        mesh_path = '%s/%s' % (args.input_directory, astrocyte)
        stats_output_directory = '%s/%s-stats' % (intermediate_directory, astrocyte_mesh.name)
        run_quality_checker(mesh_path=mesh_path,
                            quality_checker_executable=args.quality_checker_executable,
                            output_directory=stats_output_directory)

        # Plot the stats. of the mesh into a single image
        vertical_stats_image, horizontal_stats_image = plotting.plot_mesh_stats(
            name=astrocyte_mesh.name,
            distributions_directory=stats_output_directory,
            output_directory=intermediate_directory,
            color=(color[0] * 0.75, color[1] * 0.75, color[2] * 0.75))

        # Combine the wire-frame rendering with the stats image side-by-side
        plotting.combine_stats_with_rendering(
            rendering_image='%s/%s.png' % (intermediate_directory, astrocyte_mesh.name),
            vertical_stats_image=vertical_stats_image,
            horizontal_stats_image=horizontal_stats_image,
            output_image_path='%s/%s' % (images_directory, astrocyte_mesh.name))

        # Artistic rendering
        if args.artistic:

            bpy.context.scene.render.film_transparent = True

            # Delete the wireframe mesh
            nmv.scene.delete_object_in_scene(scene_object=wireframe_mesh)

            # Remove all the lights in the scene
            nmv.scene.clear_lights()

            # Create a wax shader
            wax_shader = nmv.shading.create_glossy_material(name='astro-glossy')

            # Assign the subsurface scattering shader
            nmv.shading.set_material_to_object(
                mesh_object=astrocyte_mesh, material_reference=wax_shader)

            # Get the light location from the camera
            camera = nmv.scene.get_object_by_name('nmvCamera_FRONT')
            light_location = Vector((0, 0, 0))
            light_location[0] = camera.location[0]
            light_location[1] = astrocyte_bbox.center[1] + astrocyte_bbox.bounds[1]
            light_location[2] = camera.location[2]

            # From the bounding box, clear an area light
            area_light = create_area_light_from_bounding_box(location=light_location)

            # Use the denoiser
            bpy.context.scene.view_layers[0].cycles.use_denoising = True

            # Render based on the bounding box
            nmv.rendering.render(bounding_box=astrocyte_bbox,
                                 image_directory=intermediate_directory,
                                 image_name='%s-artistic' % astrocyte_mesh.name,
                                 image_resolution=args.resolution,
                                 keep_camera_in_scene=True)

            # Save the final scene into a blender file
            if args.export_blend:
                nmv.file.export_scene_to_blend_file(
                    output_directory=scenes_directory,
                    output_file_name='%s-artistic' % astrocyte.replace('.obj', ''))