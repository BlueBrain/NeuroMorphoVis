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
import os

# Blender imports
import bpy

# Internal imports
import nmv
import nmv.consts
import nmv.enums
import nmv.interface
import nmv.skeleton
import nmv.bbox
import nmv.rendering

# Global variables to notify us if a new morphology has been loaded to the system or not
current_morphology_label = None
current_morphology_path = None


####################################################################################################
# @load_morphology
####################################################################################################
def load_icons():
    """Loads the external icons.
    """
    nmv.interface.ui_icons = bpy.utils.previews.new()
    images_path = '%s/../../../data/images' % os.path.dirname(os.path.realpath(__file__))
    nmv.interface.ui_icons.load("github", os.path.join(images_path, "github-logo.png"), 'IMAGE')
    nmv.interface.ui_icons.load("bbp", os.path.join(images_path, "bbp-logo.png"), 'IMAGE')
    nmv.interface.ui_icons.load("epfl", os.path.join(images_path, "epfl-logo.png"), 'IMAGE')
    nmv.interface.ui_icons.load("nmv", os.path.join(images_path, "nmv-logo.png"), 'IMAGE')


####################################################################################################
# @load_morphology
####################################################################################################
def unload_icons():
    """Unloads the external icons, after loading them to Blender.
    """

    # Remove the icons
    bpy.utils.previews.remove(nmv.interface.ui_icons)


####################################################################################################
# @load_morphology
####################################################################################################
def enable_or_disable_layout(layout):
    """Activates or deactivates the layout based on the status of the morphology.

    :param layout:
        A given layout to enable or disable.
    """
    if nmv.interface.ui_morphology is None:
        layout.enabled = False
    else:
        layout.enabled = True


####################################################################################################
# @load_morphology
####################################################################################################
def load_morphology(panel_object,
                    context_scene):
    """Load a given morphology from file.

    :param panel_object:
        An object of a UI panel.

    :param context_scene:
        Current scene in the rendering context.
    """

    global current_morphology_label
    global current_morphology_path

    # Read the data from a given morphology file either in .h5 or .swc formats
    if bpy.context.scene.InputSource == nmv.enums.Input.H5_SWC_FILE:

        #try:
        if True:
            # Pass options from UI to system
            nmv.interface.ui_options.morphology.morphology_file_path = context_scene.MorphologyFile

            # Ensure that a file has been selected
            if 'Select File' in context_scene.MorphologyFile:
                return None

            # If no morphologies are loaded
            if current_morphology_path is None:

                # Update the morphology label
                nmv.interface.ui_options.morphology.label = nmv.file.ops.get_file_name_from_path(
                    context_scene.MorphologyFile)

                # Load the morphology file
                # Load the morphology from the file
                loading_flag, morphology_object = nmv.file.readers.read_morphology_from_file(
                    options=nmv.interface.ui_options)

                # Verify the loading operation
                if loading_flag:

                    # Update the morphology
                    nmv.interface.ui_morphology = morphology_object

                    # Update the current morphology path
                    current_morphology_path = context_scene.MorphologyFile

                    # New morphology loaded
                    return 'NEW_MORPHOLOGY_LOADED'

                # Otherwise, report an ERROR
                else:

                    # Report the issue
                    panel_object.report({'ERROR'}, 'Invalid Morphology File')

                    # None
                    return None

            # If there is file that is loaded
            else:

                # If the same path, then return
                if current_morphology_path == \
                   nmv.interface.ui_options.morphology.morphology_file_path:
                    return 'ALREADY_LOADED'

                # Load the new morphology file
                else:

                    # Update the morphology label
                    nmv.interface.ui_options.morphology.label = \
                        nmv.file.ops.get_file_name_from_path(context_scene.MorphologyFile)

                    # Load the morphology file
                    # Load the morphology from the file
                    loading_flag, morphology_object = nmv.file.readers.read_morphology_from_file(
                        options=nmv.interface.ui_options)

                    # Verify the loading operation
                    if loading_flag:

                        # Update the morphology
                        nmv.interface.ui_morphology = morphology_object

                        # Update the current morphology path
                        current_morphology_path = context_scene.MorphologyFile

                        # New morphology loaded
                        return 'NEW_MORPHOLOGY_LOADED'

                    # Otherwise, report an ERROR
                    else:

                        # Report the issue
                        panel_object.report({'ERROR'}, 'Invalid Morphology File')

                        # None
                        return None

        # Invalid morphology file
        #except ValueError:
        else:
            # Report the issue
            panel_object.report({'ERROR'}, 'CANNOT load. Invalid Morphology File')

            # None
            return None

    # Read the data from a specific gid in a given circuit
    elif bpy.context.scene.InputSource == nmv.enums.Input.CIRCUIT_GID:

        # Pass options from UI to system
        nmv.interface.ui_options.morphology.blue_config = context_scene.CircuitFile
        nmv.interface.ui_options.morphology.gid = context_scene.Gid

        # Update the morphology label
        nmv.interface.ui_options.morphology.label = 'neuron_' + str(context_scene.Gid)

        # Check if the morphology is loaded before or not
        if current_morphology_label is None:
            current_morphology_label = nmv.interface.ui_options.morphology.label
        else:
            if current_morphology_label == nmv.interface.ui_options.morphology.label:
                return 'ALREADY_LOADED'

        # Load the morphology from the circuit
        loading_flag, morphology_object = nmv.file.readers.BBPReader.load_morphology_from_circuit(
                blue_config=nmv.interface.ui_options.morphology.blue_config,
                gid=nmv.interface.ui_options.morphology.gid)

        # Verify the loading operation
        if loading_flag:

            # Update the morphology
            nmv.interface.ui_morphology = morphology_object

        # Otherwise, report an ERROR
        else:
            panel_object.report({'ERROR'}, 'Cannot Load Morphology from Circuit')

            # None
            return None

    else:
        # Report an invalid input source
        panel_object.report({'ERROR'}, 'Invalid Input Source')

        # None
        return None

    return 'NEW_MORPHOLOGY_LOADED'


####################################################################################################
# @validate_output_directory
####################################################################################################
def validate_output_directory(panel_object,
                              context_scene):
    """Validates the existence of the output directory.

    :param panel_object:
        An object of a UI panel.

    :param context_scene:
        Current scene in the rendering context.
    """

    # Ensure that there is a valid directory where the images will be written to
    if nmv.interface.ui_options.io.output_directory is None:
        panel_object.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
        return {'FINISHED'}

    if not nmv.file.ops.path_exists(context_scene.OutputDirectory):
        panel_object.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
        return {'FINISHED'}


####################################################################################################
# @render_mesh_image
####################################################################################################
def render_morphology_image(panel_object,
                            context_scene,
                            view):
    """Renders an image of the morphology reconstructed in the scene.

    :param panel_object:
        UI Panel.
    :param context_scene:
        A reference to the Blender scene.
    :param view:
        Rendering view.
    """

    # Validate the output directory
    nmv.interface.ui.validate_output_directory(
        panel_object=panel_object, context_scene=context_scene)

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
        nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

    # Report the process starting in the UI
    panel_object.report({'INFO'}, 'Rendering ... Wait')

    # Compute the bounding box for a close up view
    if context_scene.MorphologyRenderingView == \
            nmv.enums.Skeletonization.Rendering.View.CLOSE_UP_VIEW:

        # Compute the bounding box for a close up view
        bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
            extent=context_scene.MeshCloseUpSize)

    # Compute the bounding box for a mid shot view
    elif context_scene.MorphologyRenderingView == \
            nmv.enums.Skeletonization.Rendering.View.MID_SHOT_VIEW:

        # Compute the bounding box for the available meshes only
        bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves()

    # Compute the bounding box for the wide shot view that correspond to the whole morphology
    else:

        # Compute the full morphology bounding box
        bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
            morphology=nmv.interface.ui_morphology)

    # Get the view prefix
    if view == nmv.enums.Camera.View.FRONT:
        view_prefix = 'FRONT'
    elif view == nmv.enums.Camera.View.SIDE:
        view_prefix = 'SIDE'
    elif view == nmv.enums.Camera.View.TOP:
        view_prefix = 'TOP'
    else:
        view_prefix = ''

    # Render at a specific resolution
    if context_scene.RenderingType == \
            nmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION:

        # Render the image
        nmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=view,
            image_resolution=context_scene.MorphologyFrameResolution,
            image_name='MORPHOLOGY_%s_%s' % (view_prefix, nmv.interface.ui_options.morphology.label),
            image_directory=nmv.interface.ui_options.io.images_directory,
            keep_camera_in_scene=context_scene.KeepMeshCameras)

    # Render at a specific scale factor
    else:

        # Render the image
        nmv.rendering.render_to_scale(
            bounding_box=bounding_box,
            camera_view=view,
            image_scale_factor=context_scene.MorphologyFrameScaleFactor,
            image_name='MORPHOLOGY_%s_%s' % (view_prefix, nmv.interface.ui_options.morphology.label),
            image_directory=nmv.interface.ui_options.io.images_directory,
            keep_camera_in_scene=context_scene.KeepMeshCameras)

    # Report the process termination in the UI
    panel_object.report({'INFO'}, 'Rendering Done')


####################################################################################################
# @render_mesh_image
####################################################################################################
def render_mesh_image(panel_object,
                      context_scene,
                      view):
    """Renders an image of a mesh in the scene.

    :param panel_object:
        UI Panel.
    :param context_scene:
        A reference to the Blender scene.
    :param view:
        Rendering view.
    """

    # Validate the output directory
    nmv.interface.ui.validate_output_directory(
        panel_object=panel_object, context_scene=context_scene)

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
        nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

    # Report the process starting in the UI
    panel_object.report({'INFO'}, 'Rendering ... Wait')

    # Compute the bounding box for a close up view
    if context_scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

        # Compute the bounding box for a close up view
        bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
            extent=context_scene.MeshCloseUpSize)

    # Compute the bounding box for a mid shot view
    elif context_scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW:

        # Compute the bounding box for the available meshes only
        bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

    # Compute the bounding box for the wide shot view that correspond to the whole morphology
    else:

        # Compute the full morphology bounding box
        bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
            morphology=nmv.interface.ui_morphology)

    # Get the view prefix
    if view == nmv.enums.Camera.View.FRONT:
        view_prefix = 'FRONT'
    elif view == nmv.enums.Camera.View.SIDE:
        view_prefix = 'SIDE'
    elif view == nmv.enums.Camera.View.TOP:
        view_prefix = 'TOP'
    else:
        view_prefix = 'FRONT'

    # Render at a specific resolution
    if context_scene.MeshRenderingResolution == \
            nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

        # Render the image
        nmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=view,
            image_resolution=context_scene.MeshFrameResolution,
            image_name='MESH_%s_%s' % (view_prefix, nmv.interface.ui_options.morphology.label),
            image_directory=nmv.interface.ui_options.io.images_directory,
            keep_camera_in_scene=context_scene.KeepMeshCameras)

    # Render at a specific scale factor
    else:

        # Render the image
        nmv.rendering.render_to_scale(
            bounding_box=bounding_box,
            camera_view=view,
            image_scale_factor=context_scene.MeshFrameScaleFactor,
            image_name='MESH_%s_%s' % (view_prefix, nmv.interface.ui_options.morphology.label),
            image_directory=nmv.interface.ui_options.io.images_directory,
            keep_camera_in_scene=context_scene.KeepMeshCameras)

    # Report the process termination in the UI
    panel_object.report({'INFO'}, 'Rendering Done')
