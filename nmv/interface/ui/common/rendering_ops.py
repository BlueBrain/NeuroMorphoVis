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
# @render_dendrogram
####################################################################################################
def render_dendrogram(options):

    # Compute the bounding box of the dendrogram (that is a morphology) and stretch it
    bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves()
    delta = bounding_box.get_largest_dimension() * 0.05
    bounding_box.extend_bbox(delta_x=1.5 * delta, delta_y=delta)

    # Render the dendrogram image, and always use the FRONT view
    nmv.rendering.render(
        bounding_box=bounding_box,
        camera_view=nmv.enums.Camera.View.FRONT,
        image_resolution=options.rendering.frame_resolution,
        image_name='%s%s' % (options.morphology.label, nmv.consts.Suffix.DENDROGRAM),
        image_format=options.rendering.image_format,
        image_directory=options.io.images_directory,
        keep_camera_in_scene=False)


####################################################################################################
# @render_morphology_image
####################################################################################################
def render_morphology_image(panel,
                            options,
                            view):

    nmv.logger.header('Rendering Image')

    # Start
    start_time = time.time()

    # Validate the output directory
    #if not nmv.interface.ui.validate_output_directory(
    #        panel=panel, context_scene=context_scene):
    #    return

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(options.io.images_directory):
        nmv.file.ops.clean_and_create_directory(options.io.images_directory)

    # Report the process starting in the UI
    panel.report({'INFO'}, 'Rendering ... Wait')

    # If this is a dendrogram rendering, handle it in a very specific way
    if options.morphology.reconstruction_method == nmv.enums.Skeleton.Method.DENDROGRAM:
        render_dendrogram(options=options)
    else:

        # Compute the bounding box for a close up view
        if options.rendering_view == nmv.enums.Rendering.View.CLOSEUP:

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
                material_type=nmv.interface.ui.globals.options.shading.morphology_material,
                view=view)

        # Render at a specific resolution
        if context_scene.NMV_RenderingType == nmv.enums.Rendering.Resolution.FIXED:

            # Render the image
            nmv.rendering.render(
                bounding_box=bounding_box,
                camera_view=view,
                image_resolution=context_scene.NMV_MorphologyFrameResolution,
                image_name='%s%s' % (nmv.interface.ui.globals.options.morphology.label, suffix),
                image_format=image_format,
                image_directory=nmv.interface.ui.globals.options.io.images_directory,
                keep_camera_in_scene=False)

        # Render at a specific scale factor
        else:

            # Render the image
            nmv.rendering.render_to_scale(
                bounding_box=bounding_box,
                camera_view=view,
                image_scale_factor=context_scene.NMV_MorphologyFrameScaleFactor,
                image_name='%s%s' % (nmv.interface.ui.globals.options.morphology.label, suffix),
                image_format=image_format,
                image_directory=nmv.interface.ui.globals.options.io.images_directory,
                keep_camera_in_scene=False)

        # Delete the morphology scale bar, if rendered
        if context_scene.NMV_RenderMorphologyScaleBar:
            nmv.scene.delete_object_in_scene(scene_object=scale_bar)

    nmv.logger.statistics('Image rendered in [%f] seconds' % (time.time() - start_time))

    # Report the process termination in the UI
    panel.report({'INFO'}, 'Rendering Done')