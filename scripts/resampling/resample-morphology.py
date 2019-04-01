####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
import sys, os, bpy

sys.path.append(('%s/../../' %(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/core' %(os.path.dirname(os.path.realpath(__file__)))))

# System imports
import argparse

# NeuroMorphoVis imports
import nmv
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

    arg_help = 'An input morphology'
    parser.add_argument('--morphology',
                        action='store', dest='morphology', help=arg_help)

    arg_help = 'Output directory where the resampled morphology will be written'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)
                        
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

    # Load the morphology file 
    loading_flag, morphology_object = \
        nmv.file.readers.read_morphology_from_file_naively(args.morphology)

    # Verify the loading operation
    if not loading_flag:
        print({'ERROR'}, 'Invalid Morphology File')
        exit(0)

    # Resample the morphology skeleton
    nmv.skeleton.ops.apply_operation_to_morphology(
        *[morphology_object, nmv.skeleton.ops.resample_section_adaptively])

    # Export the morphology skeleton
    nmv.file.write_morphology_to_swc_file(morphology_object, args.output_directory)
