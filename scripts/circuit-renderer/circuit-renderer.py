####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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
import sys, os, bpy

sys.path.append(('%s/../../' %(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/core' %(os.path.dirname(os.path.realpath(__file__)))))

# System imports
import argparse

# NeuroMorphoVis imports
import nmv.file
import nmv.skeleton


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
    description = 'Resampling neurons to make them lighter while preserving skeletons'
    parser = argparse.ArgumentParser(description=description)
    
    arg_help = 'A circuit in sonata format'
    parser.add_argument('--circuit',
                        action='store', dest='circuit', help=arg_help)
    
    arg_help = 'The population name'
    parser.add_argument('--population',
                        action='store', dest='population', help=arg_help)
    
    arg_help = 'The RGBA color map to use for the circuit'
    parser.add_argument('--colormap-file',
                        action='store', dest='colormap_file', help=arg_help)
    
    arg_help = 'Image resolution for the circuit rendering (for the shortest side of the image)'
    parser.add_argument('--image-resolution',
                        action='store', dest='image_resolution', type=int, help=arg_help)
    
    arg_help = 'Rendering view or the camera view to use for the circuit rendering (e.g., "top", "side", "front")'
    parser.add_argument('--rendering-view',
                        action='store', dest='rendering_view', help=arg_help)
    
    
    arg_help = 'Output directory where the resulting data or images will be written'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)
    
    arg_help = 'Save the circuit as a Blender file'
    parser.add_argument('--save-blender-scene',
                        action='store_true', dest='save_blender_scene', default=False, help=arg_help)
                        
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
    print(args)

    # ERROR HANDLING
    
    
    print('Thanks')