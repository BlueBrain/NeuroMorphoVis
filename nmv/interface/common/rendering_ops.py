####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import time

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
    """Creates a rendering of the dendrogram.

    :param options:
        NeuroMorphoVis options.
    """

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
        keep_camera_in_scene=True)


####################################################################################################
# @render_morphology_relevant_image
####################################################################################################
def render_morphology_relevant_image(options,
                                     morphology,
                                     camera_view,
                                     image_suffix,
                                     panel=None):

    # Profile the rendering
    start_time = time.time()

    # Verify the output directory
    nmv.interface.verify_output_directory(options=options, panel=panel)

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(options.io.images_directory):
        nmv.file.ops.clean_and_create_directory(options.io.images_directory)

    # Report the process starting in the UI
    if panel is not None:
        panel.report({'INFO'}, 'Rendering morphology ... Wait')

    # If this is a dendrogram rendering, handle it in a very specific way
    if options.morphology.reconstruction_method == nmv.enums.Skeleton.Method.DENDROGRAM:
        render_dendrogram(options=options)
    else:

        # Bounding box computation
        if options.rendering.rendering_view == nmv.enums.Rendering.View.CLOSEUP:
            bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
                extent=options.rendering.close_up_dimensions)
        elif options.rendering.rendering_view == nmv.enums.Rendering.View.MID_SHOT:
            bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes()
        else:
            bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(morphology=morphology)

        # Draw the morphology scale bar
        scale_bar = None
        if options.rendering.render_scale_bar:
            scale_bar = nmv.interface.draw_scale_bar(
                bounding_box=bounding_box,
                material_type=options.shading.morphology_material,
                view=camera_view)

        # Resolution basis
        if options.rendering.resolution_basis == nmv.enums.Rendering.Resolution.FIXED:
            nmv.rendering.render(
                bounding_box=bounding_box,
                camera_view=camera_view,
                image_resolution=options.rendering.frame_resolution,
                image_name='%s%s' % (morphology.label, image_suffix),
                image_format=options.rendering.image_format,
                image_directory=options.io.images_directory,
                keep_camera_in_scene=False)
        else:
            nmv.rendering.render_to_scale(
                bounding_box=bounding_box,
                camera_view=camera_view,
                image_scale_factor=options.rendering.resolution_scale_factor,
                image_name='%s%s' % (options.morphology.label, image_suffix),
                image_format=options.rendering.image_format,
                image_directory=options.io.images_directory,
                keep_camera_in_scene=False)

        # Delete the morphology scale bar, if rendered
        if scale_bar is not None:
            nmv.scene.delete_object_in_scene(scene_object=scale_bar)

    nmv.logger.statistics('Image rendered in [%f] seconds' % (time.time() - start_time))

    # Report the process termination in the UI
    if panel is not None:
        panel.report({'INFO'}, 'Rendering Done')


####################################################################################################
# @render_meshes_relevant_image
####################################################################################################
def render_meshes_relevant_image(options,
                                 morphology,
                                 camera_view,
                                 image_suffix,
                                 panel=None):

    # Profile the rendering
    start_time = time.time()

    # Verify the output directory
    nmv.interface.verify_output_directory(options=options, panel=panel)

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(options.io.images_directory):
        nmv.file.ops.clean_and_create_directory(options.io.images_directory)

    # Report the process starting in the UI
    if panel is not None:
        panel.report({'INFO'}, 'Rendering mesh ... Wait')

    # Bounding box computation
    if options.rendering.rendering_view == nmv.enums.Rendering.View.CLOSEUP:
        bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
            extent=options.rendering.close_up_dimensions)
    elif options.rendering.rendering_view == nmv.enums.Rendering.View.MID_SHOT:
        bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()
    else:
        bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(morphology=morphology)

    # Draw the morphology scale bar
    scale_bar = None
    if options.rendering.render_scale_bar:
        scale_bar = nmv.interface.draw_scale_bar(
            bounding_box=bounding_box,
            material_type=options.shading.mesh_material,
            view=camera_view)

    # Resolution basis
    if options.rendering.resolution_basis == nmv.enums.Rendering.Resolution.FIXED:
        nmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=camera_view,
            image_resolution=options.rendering.frame_resolution,
            image_name='%s%s' % (morphology.label, image_suffix),
            image_format=options.rendering.image_format,
            image_directory=options.io.images_directory,
            keep_camera_in_scene=False)
    else:
        nmv.rendering.render_to_scale(
            bounding_box=bounding_box,
            camera_view=camera_view,
            image_scale_factor=options.rendering.resolution_scale_factor,
            image_name='%s%s' % (options.morphology.label, image_suffix),
            image_format=options.rendering.image_format,
            image_directory=options.io.images_directory,
            keep_camera_in_scene=False)

    # Delete the morphology scale bar, if rendered
    if scale_bar is not None:
        nmv.scene.delete_object_in_scene(scene_object=scale_bar)

    nmv.logger.statistics('Image rendered in [%f] seconds' % (time.time() - start_time))

    # Report the process termination in the UI
    if panel is not None:
        panel.report({'INFO'}, 'Rendering Done')




