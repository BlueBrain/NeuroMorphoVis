####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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
import os
import argparse
import subprocess
from PIL import Image
import seaborn
import shutil

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
import nmv.interface

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

    :param location:
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
              (quality_checker_executable, mesh_path, output_directory)
    subprocess.call(command, shell=True)


####################################################################################################
# @create_mesh_fact_sheet_with_distribution
####################################################################################################
def create_mesh_fact_sheet_with_distribution(mesh_object,
                                             mesh_name,
                                             panels_directory,
                                             image_output_path,
                                             statistics_image,
                                             mesh_scale=1):
    """Creates a fact sheet for the mesh combined with the distributions.

    :param mesh_object:
        A mesh object.
    :param mesh_name:
        The name of the mesh.
    :panels_directory:
        The directory where the panels will be written.
    :param image_output_path:
        The output path of the resulting image.
    :param statistics_image:
        The stats. image.
    :return:
    """

    # Get image resolution

    # Get the resolution from the height of the stats. image
    stats_image = Image.open(statistics_image)
    stats_image_height = stats_image.size[1]

    # Create the fac-sheet image
    fact_sheet_image_path = plotting.create_mesh_fact_sheet(
            mesh_object=mesh_object, mesh_name=mesh_name, output_image_path=panels_directory,
            image_resolution=stats_image_height, mesh_scale=mesh_scale)

    fact_sheet_image = Image.open(fact_sheet_image_path)

    resulting_image = Image.new('RGB', (stats_image.width + fact_sheet_image.width,
                                        stats_image.height))
    resulting_image.paste(stats_image, (0, 0))
    resulting_image.paste(fact_sheet_image, (stats_image.width, 0))
    final_image_path = image_output_path + '/%s.png' % mesh_name
    resulting_image.save(final_image_path)

    # Close all the images.
    fact_sheet_image.close()
    stats_image.close()
    resulting_image.close()

    return resulting_image


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
    description = 'This script is used to render a mesh to be added to an analysis plot'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'The input directory that contains that meshes'
    parser.add_argument('--input-directory', action='store', help=arg_help)

    arg_help = 'Output directory, where the final image/movies and scene will be stored'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    arg_help = 'Render the artistic version with high quality rendering'
    parser.add_argument('--artistic', action='store_true', default=False, help=arg_help)

    arg_help = 'The mesh color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--mesh-color', action='store', help=arg_help)

    arg_help = 'Wireframe thickness'
    parser.add_argument('--wireframe-thickness', action='store', default=0.02, type=float,
                        help=arg_help)

    arg_help = 'Mesh scale'
    parser.add_argument('--mesh-scale', action='store', default=1, type=float,
                        help=arg_help)

    arg_help = 'Base full-view resolution'
    parser.add_argument('--resolution', action='store', default=2000, type=int, help=arg_help)

    arg_help = 'Export blender scene'
    parser.add_argument('--export-blend', action='store_true', default=False, help=arg_help)

    arg_help = 'Render artistic image'
    parser.add_argument('--render-artistic', action='store_true', default=False, help=arg_help)

    arg_help = 'Quality checker executable from Ultraliser'
    parser.add_argument('--quality-checker-executable', action='store', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @process_mesh
####################################################################################################
def process_mesh(arguments,
                 mesh_object,
                 path_to_mesh, 
                 mesh_name, 
                 mesh_color,
                 intermediate_directory,
                 images_directory,
                 scenes_directory, 
                 render_artistic=False):
    """Process a given mesh and analyze it.

    :param arguments:
        System arguments.
    :param mesh_object:
        A reference to the loaded mesh object.
    :param path_to_mesh:
        A path to the mesh file.
    :param mesh_name:
        The name of the mesh.
    :param mesh_color:
        The color of the mesh.
    :param intermediate_directory:
        Intermediate directory to store the data.
    :param images_directory:
        Directory to keep the images.
    :param scenes_directory:
        Scenes directory.
    :param render_artistic:
        If True, an artistic image will be rendered.
    :return:
    """

    # Loading the fonts
    nmv.interface.load_fonts()

    # Rotate the mesh object to adjust the orientation in front of the camera
    # nmv.scene.rotate_object(mesh_object, 0, 0, 0)

    # Get the bounding box and compute the unified one, to render the astrocyte in the middle
    mesh_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()
    mesh_bbox.extend_bbox(mesh_bbox.bounds[0] * 0.025,
                          mesh_bbox.bounds[1] * 0.025,
                          mesh_bbox.bounds[1] * 0.025)

    # Extend the bounding box

    # Create the illumination
    nmv.shading.create_lambert_ward_illumination()

    # Create a simple shader
    color = nmv.utilities.parse_color_from_argument(mesh_color)

    # Palette colors
    pcolors = seaborn.color_palette("deep", 8)

    if 'dmc' in mesh_name:
        color = Vector((pcolors[3][0], pcolors[3][1], pcolors[3][2]))
    elif 'optimized' in mesh_name:
        color = Vector((pcolors[2][0], pcolors[2][1], pcolors[2][2]))
    elif 'watertight' in mesh_name:
        color = Vector((pcolors[0][0], pcolors[0][1], pcolors[0][2]))
    else:
        color = nmv.utilities.parse_color_from_argument(mesh_color)

    mesh_material = nmv.shading.create_lambert_ward_material(
        name='mesh-color-%s' % mesh_name, color=color)

    # Assign the wire-frame shader, using an input color
    nmv.shading.set_material_to_object(mesh_object=mesh_object, material_reference=mesh_material)
    bpy.context.scene.display.shading.light = 'STUDIO'
    bpy.context.scene.display.shading.studio_light = 'outdoor.sl'

    # TBD: Ignore the wireframe mesh for the moment
    if False:
        # Create a wireframe
        wireframe_mesh = nmv.mesh.create_wire_frame(
            mesh_object=mesh_object, wireframe_thickness=arguments.wireframe_thickness)

        # Create a wireframe shader
        wireframe_material = nmv.shading.create_lambert_ward_material(
            name='wireframe-%s' % mesh_name, color=nmv.consts.Color.BLACK)

        # Assign the wire-frame shader, using an input color
        nmv.shading.set_material_to_object(
            mesh_object=wireframe_mesh, material_reference=wireframe_material)

    # Set the background to WHITE for the compositing
    bpy.context.scene.render.film_transparent = False
    bpy.context.scene.world.color[0] = 10
    bpy.context.scene.world.color[1] = 10
    bpy.context.scene.world.color[2] = 10

    panels_directory = '%s/%s-panels' % (intermediate_directory, mesh_name)
    if not os.path.exists(panels_directory):
        os.makedirs(panels_directory)

    # Render based on the bounding box
    nmv.rendering.render(bounding_box=mesh_bbox,
                         image_directory=panels_directory,
                         image_name=mesh_name,
                         image_resolution=arguments.resolution,
                         keep_camera_in_scene=True)

    # Save the final scene into a blender file
    if arguments.export_blend:
        nmv.file.export_scene_to_blend_file(
            output_directory=scenes_directory, output_file_name=mesh_name)

    # Run the quality checker app
    stats_output_directory = '%s/%s-stats' % (intermediate_directory, mesh_name)
    run_quality_checker(mesh_path=path_to_mesh,
                        quality_checker_executable=arguments.quality_checker_executable,
                        output_directory=stats_output_directory)

    vertical_stats_image, horizontal_stats_image = plotting.plot_mesh_stats(
        name=mesh_name,
        distributions_directory=stats_output_directory,
        output_directory=panels_directory,
        color=(color[0], color[1], color[2]))

    # Plot the statistics image
    fact_sheet_image = create_mesh_fact_sheet_with_distribution(
        mesh_object=mesh_object, mesh_name=mesh_name, image_output_path=images_directory,
        panels_directory=panels_directory, statistics_image=horizontal_stats_image,
        mesh_scale=args.mesh_scale)

    # Clean the stats data
    if os.path.exists(stats_output_directory):
        shutil.rmtree(stats_output_directory)

    '''
    # Combine the wire-frame rendering with the stats image side-by-side
    combined_vert, combined_horiz = plotting.combine_stats_with_rendering(
        rendering_image='%s/%s.png' % (panels_directory, mesh_name),
        vertical_stats_image=vertical_stats_image,
        horizontal_stats_image=horizontal_stats_image,
        output_image_path='%s/%s' % (images_directory, mesh_name))
    '''

    # Clean the stats data
    if os.path.exists(panels_directory):
        shutil.rmtree(panels_directory)

    # Smooth the faces of the mesh
    nmv.mesh.shade_smooth_object(mesh_object=mesh_object)

    # Subdivide
    # nmv.mesh.smooth_object(mesh_object=mesh_object, level=1)

    # Set back to transparent
    bpy.context.scene.render.film_transparent = True

    # Delete the wireframe mesh
    # nmv.scene.delete_object_in_scene(scene_object=wireframe_mesh)

    # Remove all the lights in the scene
    nmv.scene.clear_lights()

    # Create a wax shader
    # wax_shader = nmv.shading.create_glossy_material(name='mesh-glossy')

    # Assign the subsurface scattering shader
    # nmv.shading.set_material_to_object(mesh_object=mesh_object, material_reference=wax_shader)

    # Get the bounding box
    # bounds = nmv.bbox.confirm_object_bounding_box(mesh_object)

    # Create SUN light
    # bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
    # bpy.context.object.data.energy = 1

    # Use the denoiser
    # bpy.context.scene.view_layers[0].cycles.use_denoising = True

    # Render based on the bounding box
    nmv.rendering.render(bounding_box=mesh_bbox,
                         image_directory=images_directory,
                         image_name='%s-rendering' % mesh_object.name,
                         image_resolution=arguments.resolution,
                         keep_camera_in_scene=True)

    # Path to the artistic image
    artistic_image = '%s/%s-artistic.png' % (images_directory, mesh_object.name)

    # Save the final scene into a blender file
    if arguments.export_blend:
        nmv.file.export_scene_to_blend_file(
            output_directory=scenes_directory,
            output_file_name='%s-artistic' % mesh_name)


################################################################################
# @ Main
################################################################################
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

    # Get all the meshes in the path
    meshes = nmv.file.get_files_in_directory(args.input_directory, file_extension='.obj')
    meshes.extend(nmv.file.get_files_in_directory(args.input_directory, file_extension='.ply'))

    for mesh_file in meshes:
        mesh_path = '%s/%s' % (args.input_directory, mesh_file)

        # Clear the scene
        nmv.scene.clear_scene()

        # Load the skinned astrocyte mesh
        mesh_object = nmv.file.import_mesh(mesh_path)

        # Process the mesh
        process_mesh(
            arguments=args, mesh_object=mesh_object,
            path_to_mesh=mesh_path,
            mesh_name=os.path.basename(mesh_path),
            mesh_color=args.mesh_color,
            intermediate_directory=intermediate_directory,
            images_directory=images_directory,
            scenes_directory=scenes_directory,
            render_artistic=args.render_artistic)
