####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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
import histograms


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
    description = 'This script takes the path to an input mesh and creates the corresponding ' \
                  'watertight mesh and the stats. of both meshes and creates a comparative result'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'The input directory that contains all the meshes'
    parser.add_argument('--input-directory', action='store', help=arg_help)

    arg_help = 'Output directory, where the final image/movies and scene will be stored'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    arg_help = 'Mesh scale'
    parser.add_argument('--mesh-scale', action='store', default=1, type=float, help=arg_help)

    arg_help = 'Mesh2Mesh executable from Ultraliser'
    parser.add_argument('--ultraMesh2Mesh', action='store', default='ultraMesh2Mesh',
                        help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @run_quality_checker_on_input_mesh
####################################################################################################
def create_watertight_mesh(arguments,
                           input_mesh_path,
                           output_directory):
    # Create the shell command
    shell_command = '%s ' % arguments.ultraMesh2Mesh
    shell_command += '--mesh %s ' % input_mesh_path
    shell_command += '--output-directory %s ' % output_directory
    shell_command += '--auto-resolution --voxels-per-micron 1 '
    shell_command += '--solid '
    shell_command += '--ignore-marching-cubes-mesh --ignore-laplacian-mesh --ignore-optimized-mesh '
    shell_command += '--export-obj-mesh '
    shell_command += '--stats --dists '

    # Execute the shell command
    print(shell_command)
    subprocess.call(shell_command, shell=True)


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Get all the meshes in the path, either obj or ply
    list_meshes = nmv.file.get_files_in_directory(args.input_directory, file_extension='.obj')
    list_meshes.extend(nmv.file.get_files_in_directory(args.input_directory, file_extension='.ply'))

    # For every mesh in the list
    for mesh_file in list_meshes:

        # Full path
        mesh_path = '%s/%s' % (args.input_directory, mesh_file)

        # Create the watertight mesh, and the stats.
        create_watertight_mesh(
            arguments=args, input_mesh_path=mesh_path, output_directory=args.output_directory)

        # Plot the distributions
        histograms.plot_distributions(arguments=args)






