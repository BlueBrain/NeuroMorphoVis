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
import neuromorphovis as nmv
import neuromorphovis.builders
import neuromorphovis.bbox
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.file
import neuromorphovis.mesh
import neuromorphovis.skeleton
import neuromorphovis.interface
import neuromorphovis.options
import neuromorphovis.rendering
import neuromorphovis.scene


####################################################################################################
# @reconstruct_neuron_mesh
####################################################################################################
def reconstruct_neuron_mesh(cli_morphology,
                            cli_options):
    """Neuron mesh reconstruction and visualization operations.

    :param cli_morphology:
        The morphology loaded from the command line interface (CLI).
    :param cli_options:
        System options parsed from the command line interface (CLI).
    """

    # Clear the scene
    nmv.scene.ops.clear_scene()

    # Neuron mesh reconstruction
    neuron_mesh_builder = None

    # UnionBuilder
    if cli_options.mesh.meshing_technique == nmv.enums.Meshing.Technique.UNION:

        nmv.logger.log('Builder: Union')
        neuron_mesh_builder = nmv.builders.UnionBuilder(cli_morphology, cli_options)

    # BridgingBuilder
    elif cli_options.mesh.meshing_technique == nmv.enums.Meshing.Technique.BRIDGING:
        nmv.logger.log('Builder: Bridging')
        neuron_mesh_builder = nmv.builders.BridgingBuilder(cli_morphology, cli_options)

    # PiecewiseBuilder
    elif cli_options.mesh.meshing_technique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
        nmv.logger.log('Builder: Piecewise Watertight')
        neuron_mesh_builder = nmv.builders.PiecewiseBuilder(cli_morphology, cli_options)

    # Unknown, kill NeuroMorphoVis
    else:

        # Invalid meshing algorithm
        nmv.logger.log('ERROR: INVALID meshing algorithm')

        # Kill NeuroMorphoVis
        nmv.kill()

    # A single mesh object of the neuron
    reconstructed_neuron_mesh = neuron_mesh_builder.reconstruct_mesh()

    # Return a reference to the reconstructed neuron mesh
    return reconstructed_neuron_mesh


####################################################################################################
# @save_neuron_mesh
####################################################################################################
def save_neuron_mesh(neuron_mesh,
                     cli_options):
    """Save the reconstructed neuron mesh to a file.

    :param neuron_mesh:
        A reconstructed neuron mesh object.
    :param cli_options:
        CLI options given by the user.
    """

    # Header
    nmv.logger.header('Saving mesh')

    # Update the file prefix
    neuron_mesh_file_name = '%s' % cli_options.morphology.label

    # Export the neuron mesh
    nmv.file.export_mesh_object(neuron_mesh, cli_options.io.meshes_directory,
                                neuron_mesh_file_name, ply=cli_options.mesh.export_ply,
                                obj=cli_options.mesh.export_obj, stl=cli_options.mesh.export_stl,
                                blend=cli_options.mesh.export_blend)


####################################################################################################
# @render_neuron_mesh_to_static_frame
####################################################################################################
def render_neuron_mesh_to_static_frame(neuron_mesh,
                                       cli_options,
                                       cli_morphology):
    """Renders a static frame of the reconstructed neuron mesh.

    :param neuron_mesh:
        A reconstructed neuron mesh.
    :param cli_options:
        CLI options.
    :param cli_morphology:
        Original morphology.
    """

    # Header
    nmv.logger.header('Rendering static frame of the neuron mesh')

    # Compute the bounding box for a close up view
    if cli_options.mesh.rendering_view == nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

        # Compute the bounding box for a close up view
        bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
            extent=cli_options.mesh.close_up_dimensions)

    # Compute the bounding box for a mid shot view
    elif cli_options.mesh.rendering_view == nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW:

        # Compute the bounding box for the available meshes only
        bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

    # Compute the bounding box for the wide shot view that correspond to the whole morphology
    else:

        # Compute the full morphology bounding box
        bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
            morphology=cli_morphology)

    # Render at a specific resolution
    if cli_options.mesh.resolution_basis == nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

        # Render the image
        nmv.rendering.NeuronMeshRenderer.render(
            bounding_box=bounding_box,
            camera_view=nmv.enums.Camera.View.FRONT,
            image_resolution=cli_options.mesh.full_view_resolution,
            image_name='MESH_FRONT_%s' % cli_morphology.label,
            image_directory=cli_options.io.images_directory)

    # Render at a specific scale factor
    else:

        # Render the image
        nmv.rendering.NeuronMeshRenderer.render_to_scale(
            bounding_box=bounding_box,
            camera_view=nmv.enums.Camera.View.FRONT,
            image_scale_factor=cli_options.mesh.resolution_scale_factor,
            image_name='MESH_FRONT_%s' % cli_morphology.label,
            image_directory=cli_options.io.images_directory)


####################################################################################################
# @render_mesh_360
####################################################################################################
def render_neuron_mesh_360(neuron_mesh,
                           cli_options,
                           cli_morphology):
    """Renders a 360 sequence of the reconstructed neuron mesh.

    :param neuron_mesh:
        Reconstructed neuron mesh.
    :param cli_options:
        CLI options.
    :param cli_morphology:
        The original morphology.
    """

    # Header
    nmv.logger.header('Rendering a 360 sequence of the neuron mesh')

    # Render a 360 sequence
    if cli_options.mesh.render_360:

        # Compute the bounding box for a close up view
        if cli_options.mesh.rendering_view == nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
                extent=cli_options.mesh.close_up_dimensions)

        # Compute the bounding box for a mid shot view
        elif cli_options.mesh.rendering_view == nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Compute the bounding box for the wide shot view that correspond to whole morphology
        else:

            # Compute the full morphology bounding box
            bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=cli_morphology)

        # Compute a 360 bounding box to fit the arbors
        bounding_box_360 = nmv.bbox.compute_360_bounding_box(bounding_box,
                                                             cli_morphology.soma.centroid)

        # Create a specific directory for this mesh
        output_directory = '%s/%s_mesh_360' % (
            cli_options.io.sequences_directory, cli_options.morphology.label)
        nmv.file.ops.clean_and_create_directory(output_directory)

        # Render 360
        for i in range(360):

            # Set the frame name
            image_name = '%s/%s' % (output_directory, '{0:05d}'.format(i))

            # Render at a specific resolution
            if cli_options.mesh.resolution_basis == \
                    nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

                # Render the image
                nmv.rendering.NeuronMeshRenderer.render_at_angle(
                    mesh_objects=[neuron_mesh], angle=i, bounding_box=bounding_box_360,
                    camera_view=nmv.enums.Camera.View.FRONT_360,
                    image_resolution=cli_options.mesh.full_view_resolution,
                    image_name=image_name)

            # Render at a specific scale factor
            else:

                # Render the image
                nmv.rendering.NeuronMeshRenderer.render_at_angle_to_scale(
                    mesh_objects=[neuron_mesh], angle=i, bounding_box=bounding_box_360,
                    camera_view=nmv.enums.Camera.View.FRONT_360,
                    image_scale_factor=cli_options.mesh.resolution_scale_factor,
                    image_name=image_name)


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

    # Soma mesh reconstruction and visualization
    neuron_mesh = reconstruct_neuron_mesh(cli_morphology=cli_morphology, cli_options=cli_options)

    # Saving the mesh
    if cli_options.mesh.export_ply or cli_options.mesh.export_obj or \
       cli_options.mesh.export_stl or cli_options.mesh.export_blend:

        # Save the neuron mesh
        save_neuron_mesh(neuron_mesh=neuron_mesh, cli_options=cli_options)

    # Render the mesh
    if cli_options.mesh.render:
        render_neuron_mesh_to_static_frame(neuron_mesh=neuron_mesh, cli_options=cli_options,
                                           cli_morphology=cli_morphology)

    # Render 360 of the mesh
    if cli_options.mesh.render_360:
        render_neuron_mesh_360(neuron_mesh=neuron_mesh, cli_options=cli_options,
                               cli_morphology=cli_morphology)

    # Rendering the mesh
    nmv.logger.log('NMV Done')


