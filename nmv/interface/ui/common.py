####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import time

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv.consts
import nmv.enums
import nmv.interface
import nmv.skeleton
import nmv.bbox
import nmv.rendering
import nmv.scene
import nmv.geometry
import nmv.interface


####################################################################################################
# @load_icons
####################################################################################################
def load_icons():
    """Loads the external icons to Blender to be able to use them on the panel interface."""

    nmv.interface.ui_icons = bpy.utils.previews.new()
    images_path = '%s/../../../data/images' % os.path.dirname(os.path.realpath(__file__))
    nmv.interface.ui_icons.load("github", os.path.join(images_path, "github-logo.png"), 'IMAGE')
    nmv.interface.ui_icons.load("bbp", os.path.join(images_path, "bbp-logo.png"), 'IMAGE')
    nmv.interface.ui_icons.load("epfl", os.path.join(images_path, "epfl-logo.png"), 'IMAGE')
    nmv.interface.ui_icons.load("nmv", os.path.join(images_path, "nmv-logo.png"), 'IMAGE')


####################################################################################################
# @unload_icons
####################################################################################################
def unload_icons():
    """Unloads the external icons, after loading them to Blender."""

    bpy.utils.previews.remove(nmv.interface.ui_icons)


####################################################################################################
# @load_fonts
####################################################################################################
def load_fonts():
    """Loads all the fonts to the Blender system to be able to use them for the plotting."""

    # Get all the font files in the fonts directory and load them into the scene
    font_files = nmv.file.get_files_in_directory(
        directory=nmv.consts.Paths.FONTS_DIRECTORY, file_extension='ttf')
    for font_file in font_files:
        font = '%s/%s' % (nmv.consts.Paths.FONTS_DIRECTORY, font_file)
        bpy.data.fonts.load(font)


####################################################################################################
# @enable_or_disable_layout
####################################################################################################
def enable_or_disable_layout(layout):
    """Activates or deactivates the layout based on the status of the morphology.

    :param layout:
        A given layout to enable or disable.
    """

    layout.enabled = False if nmv.interface.ui_morphology is None else True


####################################################################################################
# @load_morphology_from_file
####################################################################################################
def load_morphology_from_file(panel,
                              scene,
                              options):
    """Loads an individual morphology file. Note that the path information is available in @options.
    NOTE: In case of failure, a specific error is reported and a None is returned to terminate
    the loading operation.

    :param panel:
        Current I/O panel.
    :param scene:
        Blender scene.
    :param options:
        A reference to the NeuroMorphoVis options.
    :return:
        A reference to the morphology object if successfully loaded, or None otherwise.
    """

    # If no file is given from the user, handle the error
    if nmv.consts.Strings.SELECT_FILE in options.morphology.morphology_file_path:
        panel.report({'ERROR'}, 'To load a morphology, please select a valid morphology file')
        return None

    # If the given morphology path is not valid, handle the error
    if not os.path.isfile(options.morphology.morphology_file_path):
        panel.report({'ERROR'}, 'The given morphology path is not a valid file. '
                                'Please select a valid file morphology file with an existing path')
        return None

    # Load the morphology object
    morphology_object = nmv.file.readers.read_morphology_from_file(options=options, panel=panel)

    # If the loaded morphology object is not None, update the global references
    if morphology_object is None:
        panel.report({'ERROR'}, 'The selected morphology cannot be loaded!')
        return None
    else:
        options.morphology.label = nmv.file.ops.get_file_name_from_path(scene.NMV_MorphologyFile)
        nmv.interface.ui_morphology = morphology_object
        return 'VALID_MORPHOLOGY'


####################################################################################################
# @load_morphology_from_circuit
####################################################################################################
def load_morphology_from_circuit(panel,
                                 scene,
                                 options):
    """Loads the morphology from a digitally reconstructed circuit. Note that the circuit
    information is available in @options.
    NOTE: In case of failure, a specific error is reported and a None is returned to terminate
    the loading operation.

    :param panel:
        Current I/O panel.
    :param scene:
        Blender scene.
    :param options:
        A reference to the NeuroMorphoVis options.
    :return:
        A reference to the morphology object if successfully loaded, or None otherwise.
    """

    # In case users do not select a circuit file or give a wrong circuit file, handle the error
    if nmv.consts.Strings.SELECT_CIRCUIT_FILE in options.morphology.blue_config or \
            not os.path.isfile(options.morphology.blue_config):
        panel.report({'ERROR'}, 'Please select a valid circuit')
        return None

    # In case a non-valid GID is provided
    if nmv.consts.Strings.ADD_GID in str(options.morphology.gid):
        panel.report({'ERROR'}, 'Please provide a valid GID')
        return None

    # If the given GID contains non-integer characters
    try:
        int(options.morphology.gid)
    except:
        panel.report({'ERROR'}, 'The provided GID must be an integer')
        return None

    # Load the morphology from the circuit
    morphology_object = nmv.file.readers.read_morphology_from_circuit(
        options=nmv.interface.ui_options)

    # If the loaded morphology object is not None, update the global references
    if morphology_object is None:
        panel.report({'ERROR'}, 'The selected morphology cannot be loaded!')
        return None
    else:
        options.morphology.label = str(scene.NMV_Gid)
        nmv.interface.ui_morphology = morphology_object
        return 'VALID_MORPHOLOGY'


####################################################################################################
# @load_morphology
####################################################################################################
def load_morphology(panel,
                    scene):
    """Loads a morphology into NeuroMorphoVis from a specific input source.

    :param panel:
        Current I/O panel.
    :param scene:
        Blender scene.
    """

    # Load the morphology either from an individual file or from a digitally reconstructed circuit
    if bpy.context.scene.NMV_InputSource == nmv.enums.Input.MORPHOLOGY_FILE:
        return load_morphology_from_file(
            panel=panel, scene=scene, options=nmv.interface.ui_options)
    elif bpy.context.scene.NMV_InputSource == nmv.enums.Input.CIRCUIT_GID:
        return load_morphology_from_circuit(
            panel=panel, scene=scene, options=nmv.interface.ui_options)
    else:
        panel.report({'ERROR'}, 'Invalid Input Source')
        return None


####################################################################################################
# @configure_output_directory
####################################################################################################
def configure_output_directory(options,
                               context=None):
    """Configures the output directory after loading the data.

    :param options:
        System options.
    :param context:
        Context.
    """

    # If the output directory is not set
    if options.io.output_directory is None:

        # Suggest an output directory at the home folder
        suggested_output_folder = '%s/neuromorphovis-output' % os.path.expanduser('~')

        # Check if the output directory already exists or not
        if os.path.exists(suggested_output_folder):

            # Update the system options
            nmv.interface.ui_options.io.output_directory = suggested_output_folder

            # Update the UI
            context.scene.NMV_OutputDirectory = suggested_output_folder

        # Otherwise, create it
        else:

            # Try to create the directory there
            try:

                # Create the directory
                os.mkdir(suggested_output_folder)

                # Update the system options
                nmv.interface.ui_options.io.output_directory = suggested_output_folder

                # Update the UI
                context.scene.NMV_OutputDirectory = suggested_output_folder

            # Voila
            except ValueError:
                pass


####################################################################################################
# @validate_output_directory
####################################################################################################
def validate_output_directory(panel,
                              context_scene):
    """Validates the existence of the output directory.

    :param panel:
        An object of a UI panel.

    :param context_scene:
        Current scene in the rendering context.

    :return
        True if the output directory is valid or False otherwise.
    """

    # Ensure that there is a valid directory where the images will be written to
    if nmv.interface.ui_options.io.output_directory is None:
        panel.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
        return False

    if not nmv.file.ops.path_exists(context_scene.NMV_OutputDirectory):
        panel.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
        return False

    # The output directory is valid
    return True


####################################################################################################
# @render_morphology_image
####################################################################################################
def render_morphology_image(panel,
                            context_scene,
                            view,
                            image_format=nmv.enums.Image.Extension.PNG):
    """Renders an image of the morphology reconstructed in the scene.

    :param panel:
        UI Panel.
    :param context_scene:
        A reference to the Blender scene.
    :param view:
        Rendering view.
    :param image_format:
        Image extension or file format, by default .PNG.
    """

    nmv.logger.header('Rendering Image')

    # Start
    start_time = time.time()

    # Validate the output directory
    if not nmv.interface.ui.validate_output_directory(
            panel=panel, context_scene=context_scene):
        return

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
        nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

    # Report the process starting in the UI
    panel.report({'INFO'}, 'Rendering ... Wait')

    # Update the image file format
    bpy.context.scene.render.image_settings.file_format = image_format

    # If this is a dendrogram rendering, handle it in a very specific way.
    if nmv.interface.ui_options.morphology.reconstruction_method == \
            nmv.enums.Skeleton.Method.DENDROGRAM:

        # Compute the bounding box of the dendrogram and stretch it
        bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves()
        delta = bounding_box.get_largest_dimension() * 0.05
        bounding_box.extend_bbox(delta_x=1.5 * delta, delta_y=delta)

        # Render the image
        nmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=nmv.enums.Camera.View.FRONT,
            image_resolution=context_scene.NMV_MorphologyFrameResolution,
            image_name='%s_dendrogram' % nmv.interface.ui_options.morphology.label,
            image_format=image_format,
            image_directory=nmv.interface.ui_options.io.images_directory,
            keep_camera_in_scene=False)

    # All other cases are okay
    else:

        # Compute the bounding box for a close up view
        if context_scene.NMV_MorphologyRenderingView == \
                nmv.enums.Rendering.View.CLOSE_UP:

            # Compute the bounding box for a close up view
            bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
                extent=context_scene.NMV_MorphologyCloseUpDimensions)

        # Compute the bounding box for a mid shot view
        elif context_scene.NMV_MorphologyRenderingView == \
                nmv.enums.Rendering.View.MID_SHOT:

            # Compute the bounding box for the available curves and meshes
            bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes()

        # Compute the bounding box for the wide shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=nmv.interface.ui_morphology)

        # Get the image suffix
        if view == nmv.enums.Camera.View.FRONT:
            suffix = nmv.consts.Suffix.MORPHOLOGY_FRONT
        elif view == nmv.enums.Camera.View.SIDE:
            suffix = nmv.consts.Suffix.MORPHOLOGY_SIDE
        elif view == nmv.enums.Camera.View.TOP:
            suffix = nmv.consts.Suffix.MORPHOLOGY_TOP
        else:
            suffix = nmv.consts.Suffix.MORPHOLOGY_FRONT

        # Draw the morphology scale bar 
        if context_scene.NMV_RenderMorphologyScaleBar:
            scale_bar = nmv.interface.draw_scale_bar(
                bounding_box=bounding_box,
                material_type=nmv.interface.ui_options.shading.morphology_material,
                view=view)

        # Render at a specific resolution
        if context_scene.NMV_RenderingType == nmv.enums.Rendering.Resolution.FIXED:

            # Render the image
            nmv.rendering.render(
                bounding_box=bounding_box,
                camera_view=view,
                image_resolution=context_scene.NMV_MorphologyFrameResolution,
                image_name='%s%s' % (nmv.interface.ui_options.morphology.label, suffix),
                image_format=image_format,
                image_directory=nmv.interface.ui_options.io.images_directory,
                keep_camera_in_scene=False)

        # Render at a specific scale factor
        else:

            # Render the image
            nmv.rendering.render_to_scale(
                bounding_box=bounding_box,
                camera_view=view,
                image_scale_factor=context_scene.NMV_MorphologyFrameScaleFactor,
                image_name='%s%s' % (nmv.interface.ui_options.morphology.label, suffix),
                image_format=image_format,
                image_directory=nmv.interface.ui_options.io.images_directory,
                keep_camera_in_scene=False)

        # Delete the morphology scale bar, if rendered 
        if context_scene.NMV_RenderMorphologyScaleBar:
            nmv.scene.delete_object_in_scene(scene_object=scale_bar)

    nmv.logger.statistics('Image rendered in [%f] seconds' % (time.time() - start_time))

    # Report the process termination in the UI
    panel.report({'INFO'}, 'Rendering Done')


####################################################################################################
# @render_mesh_image
####################################################################################################
def render_mesh_image(panel,
                      context_scene,
                      view,
                      image_format=nmv.enums.Image.Extension.PNG):
    """Renders an image of a mesh in the scene.

    :param panel:
        UI Panel.
    :param context_scene:
        A reference to the Blender scene.
    :param view:
        Rendering view.
    :param image_format:
        Image extension or file format, by default .PNG.
    """

    nmv.logger.header('Rendering Image')

    # Start
    start_time = time.time()

    # Validate the output directory
    if not nmv.interface.ui.validate_output_directory(panel=panel, context_scene=context_scene):
        return

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
        nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

    # Report the process starting in the UI
    panel.report({'INFO'}, 'Rendering ... Wait')

    # Update the image file format
    bpy.context.scene.render.image_settings.file_format = image_format

    # Compute the bounding box for a close up view
    if context_scene.NMV_MeshRenderingView == nmv.enums.Rendering.View.CLOSE_UP:

        # Compute the bounding box for a close up view
        bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
            extent=context_scene.NMV_MeshCloseUpSize)

    # Compute the bounding box for a mid shot view
    elif context_scene.NMV_MeshRenderingView == nmv.enums.Rendering.View.MID_SHOT:

        # Compute the bounding box for the available meshes only
        bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

    # Compute the bounding box for the wide shot view that correspond to the whole morphology
    else:

        # Compute the full morphology bounding box
        bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
            morphology=nmv.interface.ui_morphology)

    # Get the image suffix
    if view == nmv.enums.Camera.View.FRONT:
        suffix = nmv.consts.Suffix.MESH_FRONT
    elif view == nmv.enums.Camera.View.SIDE:
        suffix = nmv.consts.Suffix.MESH_SIDE
    elif view == nmv.enums.Camera.View.TOP:
        suffix = nmv.consts.Suffix.MESH_TOP
    else:
        suffix = nmv.consts.Suffix.MESH_FRONT

    # Draw the morphology scale bar
    if context_scene.NMV_RenderMeshScaleBar:
        scale_bar = nmv.interface.draw_scale_bar(
            bounding_box=bounding_box,
            material_type=nmv.interface.ui_options.shading.mesh_material,
            view=view)

    # Render at a specific resolution
    if context_scene.NMV_MeshRenderingResolution == nmv.enums.Rendering.Resolution.FIXED:

        # Render the image
        nmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=view,
            image_resolution=context_scene.NMV_MeshFrameResolution,
            image_name='%s%s' % (nmv.interface.ui_options.morphology.label, suffix),
            image_format=image_format,
            image_directory=nmv.interface.ui_options.io.images_directory)

    # Render at a specific scale factor
    else:

        # Render the image
        nmv.rendering.render_to_scale(
            bounding_box=bounding_box,
            camera_view=view,
            image_scale_factor=context_scene.NMV_MeshFrameScaleFactor,
            image_name='%s%s' % (nmv.interface.ui_options.morphology.label, suffix),
            image_format=image_format,
            image_directory=nmv.interface.ui_options.io.images_directory)

    # Delete the morphology scale bar, if rendered
    if context_scene.NMV_RenderMeshScaleBar:
        nmv.scene.delete_object_in_scene(scene_object=scale_bar)

    nmv.logger.statistics('Image rendered in [%f] seconds' % (time.time() - start_time))

    # Report the process termination in the UI
    panel.report({'INFO'}, 'Rendering Done')


####################################################################################################
# @render_morphology_image
####################################################################################################
def render_morphology_image_for_catalogue(resolution_scale_factor=10,
                                          view='FRONT'):
    """Renders an image of the morphology reconstructed in the scene.

    :param resolution_scale_factor:
        The scale factor that will determine the resolution.
    :param view:
        Rendering view.
    """

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
        nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

    # Compute the bounding box for the available curves and meshes
    bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes()

    # Get the view prefix
    if view == nmv.enums.Camera.View.FRONT:
        view_prefix = 'FRONT'
    elif view == nmv.enums.Camera.View.SIDE:
        view_prefix = 'SIDE'
    elif view == nmv.enums.Camera.View.TOP:
        view_prefix = 'TOP'
    else:
        view_prefix = ''

    # Render the image
    nmv.rendering.render_to_scale(
        bounding_box=bounding_box,
        camera_view=view,
        image_scale_factor=resolution_scale_factor,
        image_name='MORPHOLOGY_%s_%s' % (view_prefix, nmv.interface.ui_options.morphology.label),
        image_directory=nmv.interface.ui_options.io.analysis_directory)


####################################################################################################
# @initialize_synaptic_colors
####################################################################################################
def initialize_synaptic_colors():

    import random

    # UI color elements for the color map
    if nmv.consts.Circuit.MTYPES is not None:
        for i in range(len(nmv.consts.Circuit.MTYPES)):
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)

            setattr(bpy.types.Scene, 'NMV_MtypeColor_%d' % i,
                    bpy.props.FloatVectorProperty(
                        name='%s' % nmv.consts.Circuit.MTYPES[i],
                        subtype='COLOR', default=Vector((r, g, b)), min=0.0, max=1.0,
                        description=''))

            setattr(bpy.types.Scene, 'NMV_Synaptic_MtypeCount_%d' % i,
                    bpy.props.IntProperty(
                        name="Count",
                        description="The number of synapses of this specific morphological type",
                        default=0, min=0, max=1000000))

    # UI color elements for the color map
    if nmv.consts.Circuit.ETYPES is not None:
        for i in range(len(nmv.consts.Circuit.ETYPES)):
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            setattr(bpy.types.Scene, 'NMV_EtypeColor_%d' % i,
                    bpy.props.FloatVectorProperty(
                        name='%s' % nmv.consts.Circuit.ETYPES[i],
                        subtype='COLOR', default=Vector((r, g, b)), min=0.0, max=1.0,
                        description=''))

            setattr(bpy.types.Scene, 'NMV_Synaptic_EtypeCount_%d' % i,
                    bpy.props.IntProperty(
                        name="Count",
                        description="The number of synapses of this specific electrical type",
                        default=0, min=0, max=1000000))


####################################################################################################
# @initialize_relevant_parameters
####################################################################################################
def initialize_relevant_parameters(scene):
    initialize_synaptic_colors()






