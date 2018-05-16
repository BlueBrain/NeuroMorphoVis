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
import sys

# Blender imports
import bpy

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.bbox
import neuromorphovis.builders
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.file
import neuromorphovis.interface
import neuromorphovis.mesh
import neuromorphovis.options
import neuromorphovis.rendering
import neuromorphovis.scene
import neuromorphovis.skeleton


####################################################################################################
# @reconstruct_soma_skeleton
####################################################################################################
def reconstruct_soma_skeleton(morphology_object,
                              options):
    """Reconstruct the skeleton of the soma profile and render it.

    :param morphology_object:
        A given morphology object.
    :param options:
        System options.
    """

    # Clear the scene
    nmv.scene.ops.clear_scene()


####################################################################################################
# @proceed_morphology_reconstruction_visualization
####################################################################################################
def proceed_neuron_morphology_reconstruction_visualization(cli_morphology,
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
    skeleton_builder = nmv.builders.SkeletonBuilder(morphology=cli_morphology, options=cli_options)

    # Reconstruct the reconstructed morphology skeleton
    morphology_skeleton_objects = skeleton_builder.draw_morphology_skeleton()

    # Export to .BLEND file
    if cli_options.morphology.export_blend:

        # Export the morphology to a .BLEND file, None indicates all components the scene
        nmv.file.export_mesh_object(
            None, cli_options.io.morphologies_directory, cli_morphology.label,
            blend=cli_options.morphology.export_blend)

    # Render a static image of the reconstructed morphology skeleton
    if cli_options.morphology.render:

        # A reference to the bounding box that will be used for the rendering
        bounding_box = None

        # Compute the bounding box for a close up view
        if cli_options.morphology.rendering_view == \
                nmv.enums.Skeletonization.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
                extent=cli_options.morphology.close_up_dimensions)

        # Compute the bounding box for a mid shot view
        elif cli_options.morphology.rendering_view == \
                nmv.enums.Skeletonization.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves()

        # Compute the bounding box for the wide shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=cli_morphology)

        # Render at a specific resolution
        if cli_options.morphology.resolution_basis == \
                nmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION:

            # Render the image
            nmv.rendering.NeuronSkeletonRenderer.render(
                bounding_box=bounding_box,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=cli_options.morphology.full_view_resolution,
                image_name='MORPHOLOGY_FRONT_%s' % cli_morphology.label,
                image_directory=cli_options.io.images_directory)

        # Render at a specific scale factor
        else:

            # Render the image
            nmv.rendering.NeuronSkeletonRenderer.render_to_scale(
                bounding_box=bounding_box,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_scale_factor=cli_options.mesh.resolution_scale_factor,
                image_name='MESH_FRONT_%s' % cli_morphology.label,
                image_directory=cli_options.io.images_directory)

        pass

    # Render a 360 sequence of the reconstructed morphology skeleton
    if cli_options.morphology.render_360:
        pass

    # Render a sequence of the progressive reconstruction of the morphology skeleton
    if cli_options.morphology.render_progressive:
        pass

    # Export to .blend file
    if cli_options.morphology.export_blend:

        # Export the morphology to a .blend file
        nmv.file.export_mesh_object(None,
            cli_options.io.morphologies_directory, cli_options.morphology.label,
            blend=cli_options.morphology.export_blend)


####################################################################################################
# @proceed_soma_mesh_reconstruction_visualization
####################################################################################################
def proceed_soma_mesh_reconstruction_visualization(cli_morphology,
                                                   cli_options):
    """Soma mesh reconstruction and visualization operations.

    :param cli_morphology:
        The morphology loaded from the command line interface (CLI).
    :param cli_options:
        System options parsed from the command line interface (CLI).
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

        # Image name
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
        output_directory = '%s/%s_soma_mesh_360' % (cli_options.io.sequences_directory,
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
        output_directory = '%s/%s_soma_mesh_progressive' % (cli_options.io.sequences_directory,
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
# @proceed_neuron_mesh_reconstruction_visualization
####################################################################################################
def proceed_neuron_mesh_reconstruction_visualization(cli_morphology,
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

    # The neuron mesh is reconstructed as a list of meshes that is composed of the different
    # parts of the neuron including the soma, arbors and optionally the spines as well.
    # If the list contains a single object, this means that the neuron objects are grouped and
    # connected to a single mesh object.
    neuron_mesh_objects = neuron_mesh_builder.reconstruct_mesh()

    # Export the neuron mesh to different file formats
    if cli_options.mesh.reconstruct_neuron_mesh:

        # Update the file prefix
        neuron_mesh_file_name = '%s' % cli_options.morphology.label

        # A reference to the neuron mesh object as a SINGLE item
        neuron_mesh_object = None

        # If the list contains a single mesh object, then export it as it is
        if len(neuron_mesh_objects) == 1:

            # Use the first object only
            neuron_mesh_object = neuron_mesh_objects[0]

        # Otherwise, group all the objects in a single object using a joint operation
        else:

            # Join all the meshes into a single mesh object
            neuron_mesh_object = nmv.mesh.ops.join_mesh_objects(
                neuron_mesh_objects, cli_options.morphology.label)

        # Export the neuron mesh
        nmv.file.export_mesh_object(neuron_mesh_object,
                                    cli_options.io.meshes_directory,
                                    neuron_mesh_file_name,
                                    ply=cli_options.mesh.export_ply,
                                    obj=cli_options.mesh.export_obj,
                                    stl=cli_options.mesh.export_stl,
                                    blend=cli_options.mesh.export_blend)

    # Render a static frame of the reconstructed mesh
    if cli_options.mesh.render:

        # A reference to the bounding box that will be used for the rendering
        bounding_box = None

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
        if cli_options.mesh.resolution_basis == \
                nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

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

    # Render a 360 sequence
    if cli_options.mesh.render_360:

        # A reference to the bounding box that will be used for the rendering
        bounding_box = None

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

        # Compute a 360 bounding box to fit the arbors
        bounding_box_360 = nmv.bbox.compute_360_bounding_box(
            bounding_box, cli_morphology.soma.centroid)

        # Create a specific directory for this mesh
        output_directory = '%s/%s_mesh_360' % (cli_options.io.sequences_directory,
                                               cli_options.morphology.label)
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
                    mesh_objects=neuron_mesh_objects,
                    angle=i,
                    bounding_box=bounding_box_360,
                    camera_view=nmv.enums.Camera.View.FRONT_360,
                    image_resolution=cli_options.mesh.full_view_resolution,
                    image_name=image_name)

            # Render at a specific scale factor
            else:

                # Render the image
                nmv.rendering.NeuronMeshRenderer.render_at_angle_to_scale(
                    mesh_objects=neuron_mesh_objects,
                    angle=i,
                    bounding_box=bounding_box_360,
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

        # Reconstruct the morphology skeleton
    proceed_neuron_morphology_reconstruction_visualization(cli_morphology=cli_morphology,
        cli_options=cli_options)

    ################################################################################################
    # Soma mesh reconstruction
    ################################################################################################
    if arguments.render_soma_mesh or                \
       arguments.render_soma_mesh_360 or            \
       arguments.render_soma_mesh_progressive or    \
       arguments.reconstruct_soma_mesh:

        # Soma mesh reconstruction and visualization
        proceed_soma_mesh_reconstruction_visualization(cli_morphology=cli_morphology,
                                                       cli_options=cli_options)

    ################################################################################################
    # Whole neuron mesh reconstruction
    ################################################################################################
    if arguments.render_neuron_mesh or              \
       arguments.render_neuron_mesh_360 or          \
       arguments.reconstruct_neuron_mesh:

        # Neuron mesh reconstruction and visualization
        proceed_neuron_mesh_reconstruction_visualization(cli_morphology=cli_morphology,
                                                         cli_options=cli_options)

    ################################################################################################
    # Morphology skeleton reconstruction
    ################################################################################################


