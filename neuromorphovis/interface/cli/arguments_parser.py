####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# System imports
import argparse, os, sys
from argparse import RawTextHelpFormatter


# Internal imports
sys.path.append("%s/" % os.path.dirname(os.path.realpath(__file__)))
from args import *


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments():
    """Parse the command line arguments.

    NOTE: We do not define a destination to facilitate printing to a string and doing another
    iteration of parsing for blender.

    :return:
        A structure with all the system options.
    """

    # Create an argument parser, and then add the options one by one
    app_help = 'NeuroMorphoVis: a collaborative framework for analysis and visualization of ' \
               'morphological skeletons reconstructed from microscopy stacks'
    parser = argparse.ArgumentParser(description=app_help, formatter_class=RawTextHelpFormatter)

    ################################################################################################
    # Blender arguments
    ################################################################################################
    # Blender executable path, by default we will use the one installed on the system
    arg_help = 'Blender executable'
    parser.add_argument(Args.BLENDER_EXECUTABLE,
                        action='store', default='blender',
                        help=arg_help)

    ################################################################################################
    # Input arguments
    ################################################################################################
    # Input source (gid, target, morphology file, or a directory containing a group of morphologies)
    arg_options = ['gid', 'target', 'file', 'directory']
    arg_help = 'Input morphology sources. \n'\
               'Options: %s' % arg_options
    parser.add_argument(Args.INPUT_SOURCE,
                        action='store', default='gid',
                        help=arg_help)

    # Cell GID, requires a circuit configuration
    arg_help = 'Morphology file (.H5 or .SWC)'
    parser.add_argument(Args.MORPHOLOGY_FILE,
                        action='store', default=None,
                        help=arg_help)

    # Cell GID, requires a circuit configuration
    arg_help = 'Morphology directory containing (.H5 or .SWC) files'
    parser.add_argument(Args.MORPHOLOGY_DIRECTORY,
                        action='store', default=None,
                        help=arg_help)

    # Cell GID, requires a circuit configuration
    arg_help = 'Cell GID'
    parser.add_argument(Args.GID,
                        action='store', default=None,
                        help=arg_help)

    # Cell target
    arg_help = 'Cell target in target file'
    parser.add_argument(Args.TARGET,
                        action='store', default=None,
                        help=arg_help)

    # Circuit configuration
    arg_help = 'Circuit configuration'
    parser.add_argument(Args.BLUE_CONFIG,
                        action='store', default=None,
                        help=arg_help)

    ################################################################################################
    # Output arguments
    ################################################################################################
    # Output directory
    arg_help = 'Root output directory'
    parser.add_argument(Args.OUTPUT_DIRECTORY,
                        action='store', default=None,
                        help=arg_help)

    ################################################################################################
    # Soma arguments
    ################################################################################################
    # Soma stiffness
    arg_help = 'Soma surface stiffness (0.001 - 0.999), by default 0.25.'
    parser.add_argument(Args.SOMA_STIFFNESS,
                        action='store', type=float, default=0.25,
                        help=arg_help)

    # Soma subdivision level
    arg_help = 'Soma surface subdivision level, between (3-7), by default 4.'
    parser.add_argument(Args.SOMA_SUBDIVISION_LEVEL,
                        action='store', type=int, default=4,
                        help=arg_help)

    ################################################################################################
    # Morphology arguments
    ################################################################################################
    # Reconstruct the morphology of entire neuron
    arg_help = 'Reconstruct the morphology skeleton for visualization or analysis, by default False'
    parser.add_argument(Args.RECONSTRUCT_MORPHOLOGY_SKELETON,
                        action='store_true', default=False,
                        help=arg_help)

    # Morphology reconstruction algorithm
    arg_help = 'Morphology reconstruction algorithm, by default \'connected-sections\''
    parser.add_argument(Args.MORPHOLOGY_SKELETON,
                        action='store', default='original',
                        help=arg_help)

    # Morphology skeleton
    arg_help = 'Morphology skeleton: original, tapered, zigzag or tapered-zigza, by default ' \
               '\'original\''
    parser.add_argument(Args.MORPHOLOGY_RECONSTRUCTION_ALGORITHM, action='store',
        default='connected-sections', help=arg_help)

    # Soma building using a specific approach
    arg_help = 'Soma representation (ignore/sphere/profile), profile by default.'
    parser.add_argument(Args.SOMA_REPRESENTATION,
                        action='store', default='profile',
                        help=arg_help)

    # Axon building
    arg_help = 'Ignore building the axon, by default False. This is recommended for mesh ' \
               'reconstruction as the axon takes few minutes in certain cases to be meshes.'
    parser.add_argument(Args.IGNORE_AXON,
                        action='store_true', default=False,
                        help=arg_help)

    # Basal dendrites
    arg_help = 'Ignore building basal dendrites, by default False.'
    parser.add_argument(Args.IGNORE_BASAL_DENDRITES,
                        action='store_true', default=False,
                        help=arg_help)

    # Apical dendrite
    arg_help = 'Ignore building apical dendrites, by default False.'
    parser.add_argument(Args.IGNORE_APICAL_DENDRITES,
                        action='store_true', default=False,
                        help=arg_help)

    # Build spines
    arg_help = 'Build the spines (ignore, circuit or random), by default \'ignore\''
    parser.add_argument(Args.SPINES,
                        action='store', default='ignore',
                        help=arg_help)

    # Spines quality
    arg_help = 'The quality of the spine meshes (hq or lq), by default \'lq\''
    parser.add_argument(Args.SPINES_QUALITY,
                        action='store', default='lq',
                        help=arg_help)

    # Random spines percentage
    arg_help = 'The percentage of the spines that are added randomly (0-100), by default 50.'
    parser.add_argument(Args.RANDOM_SPINES_PERCENTAGE,
                        action='store', type=float, default=50.0,
                        help=arg_help)

    # Axon branching branching order
    arg_help = 'Maximum branching order for the axon [1, infinity], by default 5.'
    parser.add_argument(Args.AXON_BRANCHING_ORDER,
                        action='store', type=int, default=5,
                        help=arg_help)

    # Basal dendrites branching order
    arg_help = 'Maximum branching order for the basal dendrites [1, infinity], by default infinity.'
    parser.add_argument(Args.BASAL_DENDRITES_BRANCHING_ORDER,
                        action='store', type=int, default=10000000000,
                        help=arg_help)

    # Apical dendrite branching order
    arg_help = 'Maximum branching order for the apical dendrite [1, infinity]. by default infinity.'
    parser.add_argument(Args.APICAL_DENDRITES_BRANCHING_ORDER,
                        action='store', type=int, default=10000000000,
                        help=arg_help)

    # Section radii (default, scaled or fixed)
    arg_options = ['(default)', 'scaled', 'fixed']
    arg_help = 'The radii of the morphological sections.\n' \
               'Options: %s' % arg_options
    parser.add_argument(Args.SECTIONS_RADII,
                        action='store', default='default',
                        help=arg_help)

    # Section radii scale factor
    arg_help = 'A scale factor used to scale the radii of the morphology.\n' \
               'Valid only if --sections-radii = scaled.\n' \
               'Default is 1.0'
    parser.add_argument(Args.RADII_SCALE_FACTOR,
                        action='store', type=float, default=1.0,
                        help=arg_help)

    # Section fixed radius (to enlarge the thin branches)
    arg_help = 'A fixed radius for all morphology sections.\n'\
               'Valid only if --sections-radii = fixed.\n' \
               'Default is 1.0'
    parser.add_argument(Args.FIXED_SECTION_RADIUS,
                        action='store', type=float, default=1.0,
                        help=arg_help)

    # Morphology bevel object sides (sets the quality of the morphology)
    arg_help = 'The number of sides of the bevel object used to reconstruct the morphology 4-64, ' \
               'by default 16.'
    parser.add_argument(Args.MORPHOLOGY_BEVEL_SIDES,
                        action='store', type=int, default=16,
                        help=arg_help)

    ################################################################################################
    # Materials and colors arguments
    ################################################################################################
    # Soma color
    arg_help = 'Soma color'
    parser.add_argument(Args.SOMA_COLOR,
                        action='store', default='1.0_1.0_1.0',
                        help=arg_help)

    # Axon color
    arg_help = 'Axon color'
    parser.add_argument(Args.AXON_COLOR,
                        action='store', default='0.0_0.0_1.0',
                        help=arg_help)

    # Basal dendrites color
    arg_help = 'Basal dendrites color'
    parser.add_argument(Args.BASAL_DENDRITES_COLOR,
                        action='store', default='0.0_1.0_0.0',
                        help=arg_help)

    # Basal dendrites color
    arg_help = 'Apical dendrite color'
    parser.add_argument(Args.APICAL_DENDRITES_COLOR,
                        action='store', default='1.0_0.0_0.0',
                        help=arg_help)

    # Spines color
    arg_help = 'Spines color'
    parser.add_argument(Args.SPINES_COLOR,
                        action='store', default='1.0_0.0_0.0',
                        help=arg_help)

    # Articulation color, in case of using articulated sections method
    arg_help = 'Articulations color for the articulated sections method, by default Yellow.'
    parser.add_argument(Args.ARTICULATIONS_COLOR,
                        action='store', default='1.0_1.0_0.0',
                        help=arg_help)

    # Material used to render the neuron
    arg_help = 'The material (or shader, or shading mode) used to render the data, by default ' \
               'lambert.'
    parser.add_argument(Args.SHADER,
                        action='store', default='lambert',
                        help=arg_help)

    ################################################################################################
    # Meshing arguments
    ################################################################################################
    # Reconstruct the mesh of the soma only
    arg_help = 'Reconstruct the mesh of the soma only, by default False.'
    parser.add_argument(Args.RECONSTRUCT_SOMA_MESH,
                        action='store_true', default=False,
                        help=arg_help)

    # Reconstruct the mesh of entire neuron
    arg_help = 'Reconstruct the mesh of the entire neuron, by default False.'
    parser.add_argument(Args.RECONSTRUCT_NEURON_MESH,
                        action='store_true', default=False,
                        help=arg_help)

    # Meshing algorithm
    arg_help = 'Meshing algorithm (piecewise-watertight/union/bridging), by default ' \
               'piecewise-watertight.'
    parser.add_argument(Args.NEURON_MESHING_ALGORITHM,
                        action='store', default='piecewise-watertight',
                        help=arg_help)

    # The edges of the reconstructed meshes
    arg_help = 'The edges of the arbors (smooth or hard), by default set to hard. This option ' \
               'does not apply to the morphology, only the meshes.'
    parser.add_argument(Args.MESH_EDGES,
                        action='store', default='hard',
                        help=arg_help)

    # The edges of the reconstructed meshes
    arg_help = 'The surface of the neuron mesh, whether rough or smooth.'
    parser.add_argument(Args.MESH_SURFACE,
                        action='store', default='smooth',
                        help=arg_help)

    # The branching algorithm
    arg_help = 'Arbors branching based on (angles or radii), by default set to angles.'
    parser.add_argument(Args.BRANCHING_METHOD,
                        action='store', default='angles',
                        help=arg_help)

    # Mesh tessellation level
    arg_help = 'Mesh tessellation factor between (0.1, 1.0), by default set to 1.0 tessellation.'
    parser.add_argument(Args.MESH_TESSELLATION_LEVEL,
                        action='store', type=float, default=1.0,
                        help=arg_help)

    # Export the mesh at global coordinates
    arg_help = 'Exports the mesh at global coordinates. This option is valid only for BBP ' \
               'circuits.'
    parser.add_argument(Args.MESH_GLOBAL_COORDINATES,
                        action='store_true', default=False,
                        help=arg_help)

    ################################################################################################
    # Geometry export arguments
    ################################################################################################
    # Export the morphologies in .SWC format
    arg_help = 'Exports the morphology to (.SWC) file, by default False.'
    parser.add_argument(Args.EXPORT_SWC_MORPHOLOGY,
                        action='store_true', default=False,
                        help=arg_help)

    # Export the morphologies in .H5 format (after fixing the artifacts)
    arg_help = 'Exports the morphology to (.H5) file, by default False.'
    parser.add_argument(Args.EXPORT_H5_MORPHOLOGY,
                        action='store_true', default=False,
                        help=arg_help)

    # Export the morphology as a Blender file in .BLEND format
    arg_help = 'Exports the morphology as a Blender file (.BLEND), by default False.'
    parser.add_argument(Args.EXPORT_BLEND_MORPHOLOGY,
                        action='store_true', default=False,
                        help=arg_help)

    # Export the meshes in .PLY format
    arg_help = 'Exports the neuron mesh to (.PLY) file, by default False.'
    parser.add_argument(Args.EXPORT_PLY_NEURON,
                        action='store_true', default=False,
                        help=arg_help)

    # Export the neuron mesh in .OBJ format
    arg_help = 'Exports the neuron mesh to (.OBJ) file, by default False.'
    parser.add_argument(Args.EXPORT_OBJ_NEURON,
                        action='store_true', default=False,
                        help=arg_help)

    # Export the neuron mesh in .STL format
    arg_help = 'Exports the neuron mesh to (.STL) file, by default False.'
    parser.add_argument(Args.EXPORT_STL_NEURON,
                        action='store_true', default=False,
                        help=arg_help)

    # Export the neuron mesh in .BLEND format
    arg_help = 'Exports the neuron mesh as a Blender file (.BLEND), by default False'
    parser.add_argument(Args.EXPORT_BLEND_NEURON,
                        action='store_true', default=False,
                        help=arg_help)

    # Export the soma mesh in .PLY format
    arg_help = 'Exports the soma mesh to a (.PLY) file, by default False.'
    parser.add_argument(Args.EXPORT_PLY_SOMA,
                        action='store_true', default=False,
                        help=arg_help)

    # Export the soma mesh in .OBJ format
    arg_help = 'Exports the soma mesh to a (.OBJ) file, by default False.'
    parser.add_argument(Args.EXPORT_OBJ_SOMA,
                        action='store_true', default=False,
                        help=arg_help)

    # Export the soma mesh in .STL format
    arg_help = 'Exports the soma mesh to a (.STL) file, by default False.'
    parser.add_argument(Args.EXPORT_STL_SOMA,
                        action='store_true', default=False,
                        help=arg_help)

    # Export the soma mesh in .BLEND format
    arg_help = 'Exports the soma mesh to a Blender file (.BLEND), by default False.'
    parser.add_argument(Args.EXPORT_BLEND_SOMA,
                        action='store_true', default=False,
                        help=arg_help)

    ################################################################################################
    # Rendering arguments
    ################################################################################################
    # Render morphology
    arg_help = 'Render a static image of the morphology skeleton, by default False'
    parser.add_argument(Args.RENDER_NEURON_MORPHOLOGY,
                        action='store_true', default=False,
                        help=arg_help)

    # Render morphology 360 sequence
    arg_help = 'Render a 360 sequence of the morphology skeleton, by default False.'
    parser.add_argument(Args.RENDER_NEURON_MORPHOLOGY_360,
                        action='store_true', default=False,
                        help=arg_help)

    # Render morphology progressively
    arg_help = 'Render a progressive reconstruction of the morphology skeleton, by default False.'
    parser.add_argument(Args.RENDER_NEURON_MORPHOLOGY_PROGRESSIVE,
                        action='store_true', default=False,
                        help=arg_help)

    # Render soma skeleton
    arg_help = 'Render a static image of the soma skeleton (connected profile), by default False.'
    parser.add_argument(Args.RENDER_SOMA_SKELETON,
                        action='store_true', default=False,
                        help=arg_help)

    # Render soma
    arg_help = 'Render a static image of the reconstructed soma mesh, by default False.'
    parser.add_argument(Args.RENDER_SOMA_MESH,
                        action='store_true', default=False,
                        help=arg_help)

    # Render soma 360
    arg_help = 'Render a 360 sequence of the reconstructed soma mesh, by default False.'
    parser.add_argument(Args.RENDER_SOMA_MESH_360,
                        action='store_true', default=False,
                        help=arg_help)

    # Render soma progressively
    arg_help = 'Render a sequence of the progressive reconstruction of the soma mesh, by default ' \
               'False.'
    parser.add_argument(Args.RENDER_SOMA_MESH_PROGRESSIVE,
                        action='store_true', default=False,
                        help=arg_help)

    # Render mesh
    arg_help = 'Render a static image of the reconstructed neuron mesh, by default False.'
    parser.add_argument(Args.RENDER_NEURON_MESH,
                        action='store_true', default=False,
                        help=arg_help)

    # Render morphology close up
    arg_help = 'Render a 360 sequence of the reconstructed neuron mesh, by default False.'
    parser.add_argument(Args.RENDER_NEURON_MESH_360,
                        action='store_true', default=False,
                        help=arg_help)

    # Render mesh to scale (i.e. resolution is equivalent to size in microns)
    arg_help = 'Render morphology and mesh to scale (i.e. resolution is equivalent to a ' \
               'scale factor of the largest dimension of the skeleton in microns). This option ' \
               'is not used for soma rendering. To change the resolution of the final image, ' \
               'update --resolution-scale-factor to a value that is greater than 1.'
    parser.add_argument(Args.RENDER_TO_SCALE,
                        action='store_true', default=False,
                        help=arg_help)

    # Rendering view
    arg_help = 'The rendering view of the skeleton either for the morphology or for the mesh ' \
               '(close-up/mid-shot/wide-shot) but not for soma rendering, by default set to ' \
               'mid-shot.'
    parser.add_argument(Args.RENDERING_VIEW,
                        action='store', default='wide-shot',
                        help=arg_help)

    # Rendering view
    arg_help = 'The view or direction of the camera (front/side/top), by default set to front.'
    parser.add_argument(Args.CAMERA_VIEW,
                        action='store', default='front',
                        help=arg_help)

    # Close up dimensions (the view around the soma in microns)
    arg_help = 'Close up dimensions (the view around the soma in microns), by default 20 ' \
               'microns. This option is used only when the --rendering-view is set to ' \
               'close-up, otherwise ignored.'
    parser.add_argument(Args.CLOSE_UP_DIMENSIONS,
                        action='store', type=int, default=20,
                        help=arg_help)

    # Full view resolution
    arg_help = 'The base resolution of full view images that are either wide-shot or mid-shot ' \
               'images, by default 1024.'
    parser.add_argument(Args.FULL_VIEW_RESOLUTION,
                        action='store', type=int, default=1024,
                        help=arg_help)

    # Full view resolution
    arg_help = 'The base resolution of close-up images that focus on the soma, by default 512.' \
               'This option is used only when the --rendering-view is set to close-up, ' \
               'otherwise ignored.'
    parser.add_argument(Args.CLOSE_UP_RESOLUTION,
                        action='store', type=int, default=512,
                        help=arg_help)

    # Full view scale factor
    arg_help = 'If the \'render--to-scale\' flag is set, the images are rendered to scale ' \
               'based on the skeleton dimensions. This factos is used to scale the size of ' \
               'the images for high resolution images, by default 1.0.'
    parser.add_argument(Args.RESOLUTION_SCALE_FACTOR,
                        action='store', type=float, default=1.0,
                        help=arg_help)

    ################################################################################################
    # Execution arguments
    ################################################################################################
    # Execution node
    arg_help = 'Execution node (local/cluster), by default set to local'
    parser.add_argument(Args.EXECUTION_NODE,
                        action='store', default='local',
                        help=arg_help)

    # Execution cores
    arg_help = 'Number of cores required to run the jobs on the cluster, by default 256.'
    parser.add_argument(Args.NUMBER_CORES,
                        action='store', type=int, default=256,
                        help=arg_help)

    # Job granularity
    arg_help = 'The granularity of the jobs running on the cluster, (high/low), by default low.'
    parser.add_argument(Args.JOB_GRANULARITY,
                        action='store', default='low',
                        help=arg_help)

    # Parse the arguments, and return a list of them
    return parser.parse_args()


####################################################################################################
# @get_arguments_string_as_list
####################################################################################################
def get_arguments_string_as_list(arguments):
    """Convert the system parsed arguments into a list of strings to be given to an instance when
    we use the cluster to launch parallel jobs.

    :param arguments:
        Parsed arguments.
    :return:
        A list of all the arguments that were originally given to the system.
    """

    # A list of all the arguments that were originally given to the system.
    arguments_string = []

    # Compose the arguments string list
    for arg in vars(arguments):

        # Make the argument name by replacing the '_' with a '-'
        arg_option_name = arg.replace('_', '-')

        # Get the argument value
        arg_value = getattr(arguments, arg)

        # Ignore the unset flags
        if arg_value is False:
            continue

        elif arg_value is True:
            arguments_string.append('--%s ' % arg_option_name)
        else:

            # Add them to the argument string, and prepend the argument with '--'
            arguments_string.append('--%s=%s ' % (arg_option_name, arg_value))

    return arguments_string


####################################################################################################
# @get_arguments_string
####################################################################################################
def get_arguments_string(arguments):
    """Convert the system parsed arguments into a stream of strings to be given to an instance when
    we use the cluster to launch parallel jobs.

    :param arguments:
        System parsed arguments.
    :return:
        A string of all the arguments that were originally given to the system.
    """

    # A string of all the arguments that were originally given to the system.
    arguments_string = ''

    # Get the arguments string list
    arguments_string_list = get_arguments_string_as_list(arguments=arguments)

    # Compose the arguments string
    for string in arguments_string_list:
        arguments_string += string

    # Return the arguments string
    return arguments_string


####################################################################################################
# @get_arguments_string_for_individual_file
####################################################################################################
def get_arguments_string_for_individual_file(arguments,
                                             morphology_file):
    """Get the arguments string for an individual morphology file by replacing the --input to file
    and update the --morphology-file option.

    :param arguments:
        Parsed arguments
    :param morphology_file:
        Input morphology file.
    :return:
        A string of the updated arguments.
    """

    # Get the arguments string list
    arguments_string_list = get_arguments_string_as_list(arguments=arguments)

    # Replace the input argument
    for i, argument in enumerate(arguments_string_list):
        if '--input=' in argument:
            arguments_string_list[i] = '--input=file '

    # Add the absolute path of the file
    arguments_string_list.append('--morphology-file=%s/%s' % (
        arguments.morphology_directory, morphology_file))

    # Compose the arguments string
    arguments_string = ''
    for string in arguments_string_list:
        arguments_string += '\t' + string + ' '

    # Return the arguments string
    return arguments_string


####################################################################################################
# @get_arguments_string_for_individual_gid
####################################################################################################
def get_arguments_string_for_individual_gid(arguments,
                                            gid):
    """Get the arguments string for an individual morphology GID by replacing the --input to gid
    and update the --gid option.

    :param arguments:
        Parsed arguments
    :param gid:
        Morphology GID.
    :return:
        A string of the updated arguments.
    """

    # Get the arguments string list
    arguments_string_list = get_arguments_string_as_list(arguments=arguments)

    # Replace the --input=target argument with --input=gid
    for i, argument in enumerate(arguments_string_list):
        if '--input=' in argument:
            arguments_string_list[i] = '--input=gid '

    # Add the absolute path of the file
    arguments_string_list.append('--gid=%s ' % gid)

    # Compose the arguments string
    arguments_string = ''
    for string in arguments_string_list:
        arguments_string += ' ' + string

    # Return the arguments string
    return arguments_string


####################################################################################################
# @create_executable_for_single_morphology_file
####################################################################################################
def create_executable_for_single_morphology_file(arguments,
                                                 morphology_file):
    """Create an EXECUTABLE command for processing a single morphology file in a directory.

    :param arguments:
        Command line arguments.
    :param morphology_file:
        The path to the morphology file.
    :return:
        An executable shell command to call NeuroMorphoVis for a single morphology file.
    """

    # Format a string with blender arguments
    arguments_string = get_arguments_string_for_individual_file(arguments, morphology_file)

    # Retrieve the path to the CLI interface
    cli_interface = '%s/cli_interface.py' % os.path.dirname(os.path.realpath(__file__))

    # Setup the shell command
    shell_command = '%s -b --verbose 0 --python %s -- %s' % \
                    (arguments.blender, cli_interface, arguments_string)

    # Return the shell command
    return shell_command


####################################################################################################
# @create_executable_for_single_gid
####################################################################################################
def create_executable_for_single_gid(arguments,
                                     gid):
    """Create an EXECUTABLE command for a processing single morphology skeleton identified by its
    GID from a given target.

    :param arguments:
        Command line arguments.
    :param gid:
        Neuron GID.
    :return:
        An executable shell command to call NeuroMorphoVis for a single GID.
    """

    # Format a string with blender arguments
    arguments_string = get_arguments_string_for_individual_gid(arguments, gid)

    # Retrieve the path to the interface
    cli_interface = '%s/cli_interface.py' % os.path.dirname(os.path.realpath(__file__))

    # Setup the shell command
    shell_command = '%s -b --verbose 0 --python %s -- %s' % (
        arguments.blender, cli_interface, arguments_string)

    # Return the shell command
    return shell_command
