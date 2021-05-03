####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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

import subprocess
import argparse


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments():

    # Create an argument parser, and then add the options one by one
    parser = argparse.ArgumentParser()
    
    # Morphology directory
    arg_help = 'Input mesh'
    parser.add_argument('--mesh', action='store', help=arg_help)
    
    # Blender
    arg_help = 'Blender executable, at least version 2.80!'
    parser.add_argument('--blender', action='store', default='blender', help=arg_help)
                        
    # Output directory
    arg_help = 'Output directory'
    parser.add_argument('--output-directory', action='store', default=None, help=arg_help)
                        
    # Parse the arguments, and return a list of them
    return parser.parse_args()


####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Parse arguments 
    args = parse_command_line_arguments()

    # Output arguments 
    args_string = '--mesh=%s ' % args.mesh
    args_string += '--output-directory=%s ' % args.output_directory

    # Setup the shell command
    shell_command = '%s -b --verbose 0 --python %s -- %s' % (args.blender, 'core.py', args_string)
    print(shell_command)
    subprocess.call(shell_command, shell=True)







