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
import nmv.builders
import nmv.enums
import nmv.scene
import nmv.options

sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))
import mesh_importers
import mesh_exporters
import mesh_partitioning
import mesh_bounding_box
import mesh_rendering
import mesh_analysis
import spine_artifacts


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
    arg_help = 'The absolute path to the input morphology'
    parser.add_argument('--morphology', action='store', help=arg_help)

    # Path to output directory
    arg_help = 'The absolute path to the spine meshes directory'
    parser.add_argument('--spine-meshes-directory', action='store', help=arg_help)

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
    reference_name = os.path.splitext(os.path.basename(args.morphology))[0] + "_segmented_spines"

    # Clean the objects in the scene before doing anything
    nmv.scene.clear_scene()

    # Create default NMV options with fixed radius value for the visualization
    nmv_options = nmv.options.NeuroMorphoVisOptions()
    nmv_options.morphology.morphology_file_path = args.morphology
    nmv_options.morphology.axon_branch_order = 1e5
    nmv_options.morphology.center_at_origin = False
    nmv_options.mesh.soma_type = nmv.enums.Soma.Representation.META_BALLS

    # Load the SWC morphology and reconstruct a mesh
    morphology_object = nmv.file.readers.read_morphology_from_file(nmv_options)
    mesh_builder = nmv.builders.PiecewiseBuilder(morphology=morphology_object, options=nmv_options)
    mesh_builder.reconstruct_mesh()

    # Load and draw the spine meshes
    spine_meshes = spine_artifacts.import_and_draw_spine_meshes(
        spines_directory=args.spine_meshes_directory, meshes_extension='.obj')

    # Render the neuron with transparency to show the spine terminals
    mesh_rendering.disable_transparency()
    mesh_rendering.set_toon_rendering_mode()
    mesh_rendering.render_scene(args.output_directory,
                                image_name=reference_name,
                                resolution_scale_factor=10,
                                bounding_box=None,
                                render_scale_bar=False)

    # Save the result into a Blender file
    if args.export_blend_file:
        mesh_exporters.save_blend_file(output_directory=args.output_directory,
                                       file_name=reference_name)
