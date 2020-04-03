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
import nmv.bbox
import nmv.enums
import nmv.file
import nmv.skeleton
import nmv.interface
import nmv.options
import nmv.rendering
import nmv.scene
import nmv.utilities


####################################################################################################
# @proceed_morphology_reconstruction_visualization
####################################################################################################
def reconstruct_neuron_morphology(cli_morphology,
                                  cli_options):
    """Morphology reconstruction and visualization operations.

    :param cli_morphology:
        The morphology loaded from the command line interface (CLI).
    :param cli_options:
        System options parsed from the command line interface (CLI).
    """

    # Clear the scene
    nmv.scene.ops.clear_scene()

    cli_options.morphology.connect_to_soma = True

    # Skeleton builder
    skeleton_builder = nmv.builders.SkeletonBuilder(morphology=cli_morphology,
                                                    options=cli_options)

    # Reconstruct the reconstructed morphology skeleton
    morphology_skeleton_objects = skeleton_builder.draw_morphology_skeleton()

    # Export to .BLEND file
    if cli_options.morphology.export_blend:
        # Export the morphology to a .BLEND file, None indicates all components the scene
        nmv.file.export_mesh_object(
            None, cli_options.io.morphologies_directory, cli_morphology.label,
            blend=cli_options.morphology.export_blend)

    # Set the background color
    nmv.scene.set_background_color(nmv.consts.Color.WHITE, transparent=True)

    # Render a static image of the reconstructed morphology skeleton
    if cli_options.morphology.render:

        # Compute the bounding box for a close up view
        if cli_options.morphology.rendering_view == \
                nmv.enums.Skeleton.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
                extent=cli_options.morphology.close_up_dimensions)

        # Compute the bounding box for a mid shot view
        elif cli_options.morphology.rendering_view == \
                nmv.enums.Skeleton.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes()

        # Compute the bounding box for the wide shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=cli_morphology)

        # Render at a specific resolution
        if cli_options.morphology.resolution_basis == \
                nmv.enums.Skeleton.Rendering.Resolution.FIXED_RESOLUTION:

            # Render the image
            nmv.rendering.render(
                bounding_box=bounding_box,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=cli_options.morphology.full_view_resolution,
                image_name='MORPHOLOGY_FRONT_%s' % cli_morphology.label,
                image_directory=cli_options.io.images_directory)

        # Render at a specific scale factor
        else:

            # Render the image
            nmv.rendering.render_to_scale(
                bounding_box=bounding_box,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_scale_factor=cli_options.mesh.resolution_scale_factor,
                image_name='MESH_FRONT_%s' % cli_morphology.label,
                image_directory=cli_options.io.images_directory)

    # Render a 360 sequence of the reconstructed morphology skeleton
    if cli_options.morphology.render_360:

        # Compute the bounding box for a close up view
        if cli_options.morphology.rendering_view == \
                nmv.enums.Skeleton.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            rendering_bbox = nmv.bbox.compute_unified_extent_bounding_box(
                extent=cli_options.morphology.close_up_dimensions)

        # Compute the bounding box for a mid shot view
        elif cli_options.morphology.rendering_view == \
                nmv.enums.Skeleton.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            rendering_bbox = nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes()

        # Compute the bounding box for the wide shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            rendering_bbox = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=cli_morphology)

        # Compute a 360 bounding box to fit the arbors
        bounding_box_360 = nmv.bbox.compute_360_bounding_box(rendering_bbox,
                                                             cli_morphology.soma.centroid)

        # Stretch the bounding box by few microns
        bounding_box_360.extend_bbox(delta=nmv.consts.Image.GAP_DELTA)


        for i in range(0, 360):

            # Set the frame name
            image_name = '%s/%s/frame_%s' % (
                cli_options.io.sequences_directory, cli_morphology.label, '{0:05d}'.format(i))

            # Render a frame
            nmv.rendering.renderer.render_at_angle(
                scene_objects=nmv.scene.get_list_of_objects_in_scene(),
                angle=i,
                bounding_box=bounding_box_360,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=cli_options.morphology.full_view_resolution,
                image_name=image_name)

    # Render a sequence of the progressive reconstruction of the morphology skeleton
    if cli_options.morphology.render_progressive:

        # We must reconstruct the morphology with the Progressive builder
        nmv.scene.clear_scene()

        # Reconstruct the morphology using the progressive builder
        progressive_builder = nmv.builders.ProgressiveBuilder(
            morphology=cli_morphology, options=cli_options)
        progressive_builder.draw_morphology_skeleton()

        import bpy

        # Compute the bounding box for a close up view
        if cli_options.morphology.rendering_view == \
                nmv.enums.Skeleton.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            rendering_bbox = nmv.bbox.compute_unified_extent_bounding_box(
                extent=cli_options.morphology.close_up_dimensions)

        # Compute the bounding box for a mid shot view
        elif cli_options.morphology.rendering_view == \
                nmv.enums.Skeleton.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            rendering_bbox = nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes()

        # Compute the bounding box for the wide shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            rendering_bbox = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=cli_morphology)

        # Move to the last frame to get the bounding box of all the drawn objects
        bpy.context.scene.frame_set(0)

        for i in range(0, 100):
            bpy.context.scene.frame_set(i)

            # Set the frame name
            image_name = '%s' % '{0:05d}'.format(i)

            # Set the frame name
            image_name = '%s/%s/%s' % (
                cli_options.io.sequences_directory, cli_morphology.label, '{0:05d}'.format(i))

            # Render a frame
            nmv.rendering.renderer.render(
                bounding_box=rendering_bbox,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=cli_options.morphology.full_view_resolution,
                image_name=image_name,
                image_directory=None)


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

    # Neuron morphology reconstruction and visualization
    reconstruct_neuron_morphology(cli_morphology=cli_morphology, cli_options=cli_options)
    nmv.logger.log('NMV Done')


