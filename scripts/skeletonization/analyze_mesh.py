####################################################################################################
# Copyright (c) 2024, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import os
import sys
import argparse

# Blender imports
import bpy

# Internal imports
import nmv.file
import nmv.mesh
import nmv.scene

sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))
import mesh_importers
import mesh_exporters
import mesh_partitioning
import mesh_bounding_box
import mesh_rendering
import mesh_analysis


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments():
    """Parser

    :return:
        Parsed arguments.
    """

    # Create an argument parser, and then add the options one by one
    parser = argparse.ArgumentParser()

    # Path to input mesh
    arg_help = 'The absolute path to the input mesh'
    parser.add_argument('--mesh', action='store', help=arg_help)

    # Path to output directory
    arg_help = 'The absolute path to the output directory'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    arg_help = 'X-axis scale factor'
    parser.add_argument('--x-scale', action='store', default=1.0, type=float,
                        help=arg_help)

    arg_help = 'Y-axis scale factor'
    parser.add_argument('--y-scale', action='store', default=1.0, type=float,
                        help=arg_help)

    arg_help = 'Z-axis scale factor'
    parser.add_argument('--z-scale', action='store', default=1.0, type=float,
                        help=arg_help)

    arg_help = 'Export the result to a Blender file.'
    parser.add_argument('--export-blend-file', action='store_true',
                        default=False, help=arg_help)

    # Parse the arguments, and return a list of them
    return parser.parse_args()


####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":
    # Ignore blender extra arguments required to launch blender given to the command line interface
    args = sys.argv
    args = args[args.index("--") + 0:]
    sys.argv = args

    # Main
    args = parse_command_line_arguments()

    # Keep a reference to the mesh name
    mesh_name = os.path.splitext(os.path.basename(args.mesh))[0]

    # Clean the objects in the scene before doing anything
    nmv.scene.clear_scene()

    # Import the input mesh
    mesh_object = nmv.file.import_mesh(args.mesh)

    # Scale the mesh
    mesh_object.delta_scale[0] = args.x_scale
    mesh_object.delta_scale[1] = args.y_scale
    mesh_object.delta_scale[2] = args.z_scale

    # Ensure that the mesh is triangulated, i.e. with only triangular faces
    nmv.mesh.triangulate_mesh(mesh_object=mesh_object)

    # Decompose the mesh into multiple partitions
    mesh_partitions = mesh_partitioning.split_mesh_object_into_partitions(mesh_object=mesh_object)

    # Write the analysis results of the resulting partitions
    mesh_analysis.write_mesh_analysis_results(
        output_directory=args.output_directory, partitions=mesh_partitions)

    # Compute the unified bounding box
    bounding_box = mesh_bounding_box.compute_bounding_box(edge_gap_percentage=0.1)

    # Render the image without bounding box
    mesh_rendering.render_scene(args.output_directory, image_name=mesh_name,
                                bounding_box=bounding_box, render_scale_bar=True)

    # Create the bounding box
    mesh_bounding_box = mesh_bounding_box.draw_wireframe_meshes_bounding_boxes(
        meshes_list=mesh_partitions)

    # Render with the bounding box
    mesh_rendering.render_scene(args.output_directory, image_name=mesh_name + "_bbox",
                                bounding_box=bounding_box, render_scale_bar=False)

    # Render with the bounding box, and transparent
    bpy.context.scene.display.shading.show_xray = True
    bpy.context.scene.display.shading.xray_alpha = 0.25
    mesh_rendering.render_scene(args.output_directory, image_name=mesh_name + "_bbox_transparent",
                                bounding_box=bounding_box, render_scale_bar=False)

    # Save the result into a Blender file
    if args.export_blend_file:
        mesh_exporters.save_blend_file(output_directory=args.output_directory,
                                       file_name=mesh_name)
