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
sys.path.append(('%s/../../' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Internal imports
import nmv.scene
import nmv.mesh
import nmv.enums
import nmv.file
import nmv.utilities

import remesher


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

    description = 'Generating astrocytes'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'The path to the input mesh'
    parser.add_argument('--input-mesh',
                        action='store', dest='input_mesh', help=arg_help)

    arg_help = 'Output directory where the generated astrocyte will be written'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'Export the result into an .OBJ file'
    parser.add_argument('--export-obj',
                        action='store_true', dest='export_obj', default=False, help=arg_help)

    arg_help = 'Export the result into an .BLEND file'
    parser.add_argument('--export-blend',
                        action='store_true', dest='export_blend', default=False, help=arg_help)

    arg_help = 'Decimation factor, between 1.0 and 0.01'
    parser.add_argument('--decimation-factor',
                        action='store', dest='decimation_factor', type=float, default=1.0,
                        help=arg_help)

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

    # One must export a valid mesh
    if (not args.export_blend) and (not args.export_obj):
        print('You must export either a .BLEND or .OBJ mesh')
        exit(0)

    # Clear the scene
    nmv.scene.clear_scene()

    # Read the input mesh
    input_mesh = nmv.file.import_mesh(args.input_mesh)

    # Rotate the input by 90
    nmv.scene.rotate_object(input_mesh, 0, 0, 0)

    # Select the input mesh
    nmv.scene.select_object(input_mesh)

    # Generate the astrocyte
    builder = remesher.MetaBuilderRemesher(input_mesh=input_mesh)
    builder.reconstruct_mesh()

    # Export the mesh to a .BLEND file
    nmv.file.export_scene_to_blend_file(output_directory=args.output_directory,
                                        output_file_name=input_mesh.name)

