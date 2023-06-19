####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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
import ntpath
import os
import sys
import argparse

# Internal
sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/utilities/' % (os.path.dirname(os.path.realpath(__file__)))))

import geometry_utilities as gutils
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
    parser = argparse.ArgumentParser(sys.argv)

    # Morphology directory
    arg_help = 'Input mesh'
    parser.add_argument('--mesh', action='store', help=arg_help)

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

    # Get the file name
    file_name, file_extension = os.path.splitext(args.mesh)

    # Import the file
    if '.ply' == file_extension:
        mesh_object = gutils.import_ply_file(args.mesh)
    elif '.obj' == file_extension:
        mesh_object = gutils(args.mesh)
    else:
        print('Unsupported file format! Exiting')
        mesh_object = None
        exit(0)

    mesh_analysis.analyze_mesh(mesh_object=mesh_object)
        

