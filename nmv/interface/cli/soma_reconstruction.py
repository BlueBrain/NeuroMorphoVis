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
import sys

# Blender imports
import bpy

import os

# Append the internal modules into the system paths to avoid Blender importing conflicts
import_paths = ['neuromorphovis']
for import_path in import_paths:
    sys.path.append(('%s/../../..' % (os.path.dirname(os.path.realpath(__file__)))))

# Internal imports
import nmv
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.options
import nmv.rendering
import nmv.scene


####################################################################################################
# @render_soma_two_dimensional_profile
####################################################################################################
def render_soma_two_dimensional_profile(morphology_object,
                                        options):
    """Reconstruct the skeleton of the two-dimensional soma profile and render it.
    TODO: Implement this function.

    :param morphology_object:
        A given morphology object.
    :param options:
        System options.
    """

    # Clear the scene
    nmv.scene.ops.clear_scene()

    # TODO: Implement this function


####################################################################################################
# @reconstruct_soma_three_dimensional_profile_mesh
####################################################################################################
def reconstruct_soma_three_dimensional_profile_mesh(cli_morphology,
                                                    cli_options):
    """Reconstructs a three-dimensional profile of the soma and renders it.

    :param cli_morphology:
        The morphology loaded from the command line interface (CLI).
    :param cli_options:
        System options parsed from the command line interface (CLI).
    :return
        A mesh that represents the reconstructed three-dimensional profile of the morphology.
    """

    # Clear the scene
    nmv.scene.ops.clear_scene()

    # Create a soma builder object
    soma_builder = nmv.builders.SomaBuilder(cli_morphology, cli_options)

    # Reconstruct the three-dimensional profile of the soma mesh
    soma_mesh = soma_builder.reconstruct_soma_mesh()

    # Export the reconstructed soma mesh
    if cli_options.soma.reconstruct_soma_mesh:

        # Soma mesh file prefix
        soma_mesh_file_name = 'SOMA_MESH_%s' % cli_options.morphology.label

        # Export the mesh
        nmv.file.export_mesh_object(
            soma_mesh,
            cli_options.io.meshes_directory,
            soma_mesh_file_name,
            ply=cli_options.soma.export_ply,
            obj=cli_options.soma.export_obj,
            stl=cli_options.soma.export_stl,
            blend=cli_options.soma.export_blend)

    # Render a static frame of the reconstructed soma mesh
    if cli_options.soma.render_soma_mesh:

        # Image name (for a front view only)
        image_name = 'SOMA_MESH_%s_%s' % (nmv.enums.Camera.View.FRONT, cli_options.morphology.label)

        # Render the image
        nmv.rendering.SomaRenderer.render(
            view_extent=cli_options.soma.rendering_extent,
            camera_view=cli_options.soma.camera_view,
            image_resolution=cli_options.soma.rendering_resolution,
            image_name=image_name,
            image_directory=cli_options.io.images_directory)

    # Render a 360 sequence of the soma mesh
    if cli_options.soma.render_soma_mesh_360:

        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(cli_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(cli_options.io.sequences_directory)

        # Create a specific directory for this mesh
        output_directory = '%s/SOMA_MESH_360_%s' % (cli_options.io.sequences_directory,
                                                    cli_options.morphology.label)
        nmv.file.ops.clean_and_create_directory(output_directory)

        # Render the frames
        for i in range(360):

            # Set the frame name
            image_name = '%s/%s' % (output_directory, '{0:05d}'.format(i))

            # Render a frame
            nmv.rendering.SomaRenderer.render_at_angle(
                soma_mesh=soma_mesh,
                angle=i,
                view_extent=cli_options.soma.rendering_extent,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=cli_options.soma.rendering_resolution,
                image_name=image_name)

    # Render a progressive reconstruction of the soma
    if cli_options.soma.render_soma_mesh_progressive:

        # Clear the scene to do the reconstruction again while rendering the frames
        nmv.scene.ops.clear_scene()

        # Build the soft body of the soma
        soma_soft_body = soma_builder.build_soma_soft_body()

        # Create a specific directory for this mesh
        output_directory = '%s/SOMA_MESH_PROGRESSIVE_%s' % (cli_options.io.sequences_directory,
                                                            cli_options.morphology.label)
        nmv.file.ops.clean_and_create_directory(output_directory)

        # Simulation
        for i in range(nmv.consts.Simulation.MIN_FRAME, nmv.consts.Simulation.MAX_FRAME):

            # Update the frame based on the soft body simulation
            bpy.context.scene.frame_set(i)

            # Set the frame name
            image_name = '%s/%s' % (output_directory, '{0:05d}'.format(i))

            # Render a frame
            nmv.rendering.SomaRenderer.render_at_angle(
                soma_mesh=soma_mesh,
                angle=i,
                view_extent=cli_options.soma.rendering_extent,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=cli_options.soma.rendering_resolution,
                image_name=image_name)

        # Clear the scene again
        nmv.scene.ops.clear_scene()


####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Ignore blender extra arguments required to launch blender given to the command line interface
    args = sys.argv
    sys.argv = args[args.index("--") + 1:]

    # Parse the command line arguments, filter them and report the errors
    arguments = nmv.interface.cli.parse_command_line_arguments()

    # Verify the output directory before screwing things !
    if not nmv.file.ops.path_exists(arguments.output_directory):
        nmv.logger.log('ERROR: Please set the output directory to a valid path')
        exit(0)
    else:
        print('Output: [%s]' % arguments.output_directory)

    # Get the options from the arguments
    cli_options = nmv.options.NeuroMorphoVisOptions()

    # Convert the CLI arguments to system options
    cli_options.consume_arguments(arguments=arguments)

    # Read the morphology
    cli_morphology = None

    # If the input is a GID, then open the circuit and read it
    if arguments.input == 'gid':

        # Load the morphology from the file
        loading_flag, cli_morphology = nmv.file.BBPReader.load_morphology_from_circuit(
            blue_config=cli_options.morphology.blue_config,
            gid=cli_options.morphology.gid)

        if not loading_flag:
            nmv.logger.log('ERROR: Cannot load the GID [%s] from the circuit [%s]' %
                           cli_options.morphology.blue_config, str(cli_options.morphology.gid))
            exit(0)

    # If the input is a morphology file, then use the parser to load it directly
    elif arguments.input == 'file':

        # Read the morphology file
        loading_flag, cli_morphology = nmv.file.read_morphology_from_file(options=cli_options)

        if not loading_flag:
            nmv.logger.log('ERROR: Cannot load the morphology file [%s]' %
                           str(cli_options.morphology.morphology_file_path))
            exit(0)

    else:
        nmv.logger.log('ERROR: Invalid input option')
        exit(0)

    # TODO: Implement the render_soma_two_dimensional_profile() function
    # render_soma_two_dimensional_profile(cli_morphology=cli_morphology, cli_options=cli_options)

    # Soma mesh reconstruction and visualization
    reconstruct_soma_three_dimensional_profile_mesh(cli_morphology=cli_morphology,
                                                    cli_options=cli_options)
    nmv.logger.log('NMV Done')


