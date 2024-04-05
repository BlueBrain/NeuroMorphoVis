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
import spine_artifacts
import branching_artefacts


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

    # Path to spine terminals
    arg_help = 'The absolute path to the spines terminals file'
    parser.add_argument('--spines-terminals-file', action='store', help=arg_help)

    # Path to center lines
    arg_help = 'The absolute path to the center lines file'
    parser.add_argument('--center-lines-file', action='store', help=arg_help)

    # Path to spines bounds
    arg_help = 'The absolute path to the center lines file'
    parser.add_argument('--spines-bounds-file', action='store', help=arg_help)

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
# @compute_number_of_vertices_of_mesh
####################################################################################################
def draw_center_lines(center_lines_file,
                      output_directory):

    # Load and draw the center lines
    center_lines_mesh = branching_artefacts.import_center_lines_and_draw(
        file_path=center_lines_file, radius=0.1)

    # Compute the unified bounding box
    bounding_box = mesh_bounding_box.compute_bounding_box(edge_gap_percentage=0.1)

    # Render the neuron with transparency to show the spine terminals
    mesh_rendering.enable_transparency(alpha=0.25)
    mesh_rendering.render_scene(output_directory,
                                image_name=mesh_name + "_center_lines",
                                bounding_box=bounding_box, render_scale_bar=False)

    mesh_exporters.save_blend_file(output_directory=output_directory,
                                   file_name=mesh_name + "_center_lines")

    # Delete the center-lines mesh
    nmv.scene.delete_object_in_scene(center_lines_mesh)


####################################################################################################
# @compute_number_of_vertices_of_mesh
####################################################################################################
def draw_center_lines_and_spine_terminals(center_lines_file,
                                          spines_terminals_file,
                                          output_directory):
    # Load and draw the spine terminals
    spine_terminals_mesh_object = spine_artifacts.import_and_draw_spines_terminals(
        file_path=spines_terminals_file, radius=0.3)

    # Load and draw the center lines
    center_lines_mesh = branching_artefacts.import_center_lines_and_draw(
        file_path=center_lines_file, radius=0.1)

    # Compute the unified bounding box
    bounding_box = mesh_bounding_box.compute_bounding_box(edge_gap_percentage=0.1)

    # Render the neuron with transparency to show the spine terminals
    mesh_rendering.enable_transparency(alpha=0.25)
    mesh_rendering.render_scene(output_directory,
                                image_name=mesh_name + "_spine_terminals",
                                bounding_box=bounding_box, render_scale_bar=False)

    mesh_exporters.save_blend_file(output_directory=output_directory,
                                   file_name=mesh_name + "_spine_terminals")

    # Delete the center-lines and spine terminals meshes
    nmv.scene.delete_list_objects([spine_terminals_mesh_object, center_lines_mesh])


####################################################################################################
# @draw_spine_bounds
####################################################################################################
def draw_spine_bounds(spines_bounds_file,
                      output_directory):

    # Create the bounds cubes
    spines_bounds_meshes = spine_artifacts.import_and_draw_spines_bounds(
        file_path=spines_bounds_file)

    # Create the wireframe bounds
    spines_bounds_mesh = mesh_bounding_box.draw_wireframe_meshes_bounding_boxes(
        meshes_list=spines_bounds_meshes, wireframe_thickness=0.1)

    # Delete the input cubes
    nmv.scene.delete_list_objects(object_list=spines_bounds_meshes)

    # Compute the unified bounding box
    bounding_box = mesh_bounding_box.compute_bounding_box(edge_gap_percentage=0.1)

    # Render the neuron with transparency to show the spine terminals
    mesh_rendering.disable_transparency()
    mesh_rendering.set_pearl_rendering_mode()
    mesh_rendering.render_scene(output_directory,
                                image_name=mesh_name + "_spine_bounds",
                                bounding_box=bounding_box, render_scale_bar=False)

    mesh_exporters.save_blend_file(output_directory=output_directory,
                                   file_name=mesh_name + "_spine_bounds")

    # Delete the bounds mesh
    nmv.scene.delete_object_in_scene(spines_bounds_mesh)


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

    # Decompose the mesh into multiple partitions
    mesh_partitions = mesh_partitioning.split_mesh_object_into_partitions(mesh_object=mesh_object)

    draw_center_lines(center_lines_file=args.center_lines_file,
                      output_directory=args.output_directory)

    draw_center_lines_and_spine_terminals(center_lines_file=args.center_lines_file,
                                          spines_terminals_file=args.spines_terminals_file,
                                          output_directory=args.output_directory)

    draw_spine_bounds(spines_bounds_file=args.spines_bounds_file,
                      output_directory=args.output_directory)