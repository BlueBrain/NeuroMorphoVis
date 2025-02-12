####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import copy

# Blender imports
import bpy

# Internal imports
import nmv.bbox
import nmv.utilities
import nmv.rendering
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.builders
import nmv.scene


####################################################################################################
# @NMV_RenderMorphologyProgressive
####################################################################################################
class NMV_RenderMorphologyProgressive(bpy.types.Operator):
    """Render a progressive sequence of the reconstruction procedure (time-consuming)"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_progressive"
    bl_label = "Progressive"

    # Timer parameters
    start_time = 0
    event_timer = None
    timer_limits = 0

    # Output data
    output_directory = None

    # The bounding box of the morphology
    morphology_bounding_box = None

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self, context, event):
        """
        Threading and non-blocking handling.

        :param context: Panel context.
        :param event: A given event for the panel.
        """

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > bpy.context.scene.frame_end:

            # Stats.
            rendering_time = time.time()
            context.scene.NMV_MorphologyRenderingTime = rendering_time - self.start_time
            nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                                  context.scene.NMV_MorphologyRenderingTime)

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel context
            self.cancel(context)

            # Done
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Update the frame number
            bpy.context.scene.frame_set(self.timer_limits)

            # Set the frame name
            image_name = '%s' % '{0:05d}'.format(self.timer_limits)

            # Draw the morphology scale bar
            scale_bar = None
            if nmv.interface.ui_options.rendering.render_scale_bar:
                scale_bar = nmv.interface.draw_scale_bar(
                    bounding_box=self.morphology_bounding_box,
                    material_type=nmv.interface.ui_options.shading.morphology_material,
                    view=nmv.enums.Camera.View.FRONT)

            # Resolution basis
            if nmv.interface.ui_options.rendering.resolution_basis == \
                    nmv.enums.Rendering.Resolution.FIXED:
                nmv.rendering.render(
                    bounding_box=self.morphology_bounding_box,
                    camera_view=nmv.enums.Camera.View.FRONT,
                    image_resolution=nmv.interface.ui_options.rendering.frame_resolution,
                    image_name=image_name,
                    image_directory=self.output_directory)
            else:
                nmv.rendering.render_to_scale(
                    bounding_box=self.morphology_bounding_box,
                    camera_view=nmv.enums.Camera.View.FRONT,
                    image_scale_factor=nmv.interface.ui_options.rendering.resolution_scale_factor,
                    image_name=image_name,
                    image_format=nmv.interface.ui_options.rendering.image_format,
                    image_directory=self.output_directory)

            # Delete the morphology scale bar, if rendered
            if scale_bar is not None:
                nmv.scene.delete_object_in_scene(scene_object=scale_bar)

            # Update the progress shell
            nmv.utilities.show_progress('Rendering',
                                        self.timer_limits, bpy.context.scene.frame_end)

            # Update the progress bar
            context.scene.NMV_MorphologyRenderingProgress = \
                int(100 * self.timer_limits / float(bpy.context.scene.frame_end))

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @compute_morphology_bounding_box_for_progressive_reconstruction
    ################################################################################################
    def compute_morphology_bounding_box_for_progressive_reconstruction(self,
                                                                       context):
        """Computes the bounding box of the reconstructed morphology from the progressive builder.

        :param context:
            Blender context.
        """

        # Move to the last frame to get the bounding box of all the drawn objects
        bpy.context.scene.frame_set(bpy.context.scene.frame_end)

        # Morphology view
        view = context.scene.NMV_MorphologyRenderingView

        # Compute the bounding box for a close up view
        if view == nmv.enums.Rendering.View.CLOSEUP:
            self.morphology_bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
                    extent=context.scene.NMV_MorphologyCloseUpDimensions)

        # Compute the bounding box for a mid-shot view
        elif view == nmv.enums.Rendering.View.MID_SHOT:
            self.morphology_bounding_box = copy.deepcopy(
                nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes())

        # The bounding box for the wide-shot view that corresponds to the whole morphology
        else:
            self.morphology_bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
                    morphology=nmv.interface.ui_morphology)

        # Stretch the bounding box by few microns
        self.morphology_bounding_box.extend_bbox_uniformly(delta=nmv.consts.Image.GAP_DELTA)

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """
        Execute the operator.

        :param context: Panel context.
        """

        # If this is a dendrogram rendering, handle it in a very specific way.
        if nmv.interface.ui_options.morphology.reconstruction_method == \
            nmv.enums.Skeleton.Method.DENDROGRAM:
            # Cannot render a 360 of the dendrogram
            self.report({'INFO'}, 'Cannot render a progressive reconstruction of the dendrogram')
            return {'FINISHED'}

        # Timer
        self.start_time = time.time()

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.sequences_directory)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s%s' % \
                                (nmv.interface.ui_options.io.sequences_directory,
                                 nmv.interface.ui_options.morphology.label,
                                 nmv.consts.Suffix.MORPHOLOGY_PROGRESSIVE)
        nmv.file.ops.clean_and_create_directory(self.output_directory)

        # Clear the scene
        nmv.scene.clear_scene()

        # Reconstruct the morphology using the progressive builder
        progressive_builder = nmv.builders.ProgressiveBuilder(
            morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
        progressive_builder.draw_morphology_skeleton()

        # Compute the bounding box of the morphology directly after the reconstruction
        self.compute_morphology_bounding_box_for_progressive_reconstruction(context=context)

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        self.event_timer = wm.event_timer_add(time_step=0.01, window=context.window)
        wm.modal_handler_add(self)

        # Done
        return {'RUNNING_MODAL'}

    ################################################################################################
    # @cancel
    ################################################################################################
    def cancel(self, context):
        """
        Cancel the panel processing and return to the interaction mode.

        :param context: Panel context.
        """

        # Multi-threading
        wm = context.window_manager
        wm.event_timer_remove(self.event_timer)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Morphology Rendering Done')

        # Confirm operation done
        return {'FINISHED'}
