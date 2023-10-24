####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
# @NMV_RenderMorphology360
####################################################################################################
class NMV_RenderMorphology360(bpy.types.Operator):
    """Render a 360 sequence of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_360"
    bl_label = "360"

    # Timer parameters
    event_timer = None
    timer_limits = 0
    start_time = 0

    # Output data
    output_directory = None

    # The bounding box snap keep a copy of the bounding box at the first frame only to preserve
    # it during the entire sequence
    bounding_box_snap = None

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self, context, event):

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > 360:

            # Reset the orientation of the mesh
            nmv.scene.reset_orientation_of_objects(
                scene_objects=nmv.interface.ui_reconstructed_skeleton)

            # Stats.
            rendering_time = time.time()
            context.scene.NMV_MorphologyRenderingTime = rendering_time - self.start_time
            nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                                  context.scene.NMV_MorphologyRenderingTime)

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel and return
            self.cancel(context)
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Set the frame name
            image_name = '%s/%s' % (self.output_directory, '{0:05d}'.format(self.timer_limits))

            nmv.interface.render_morphology_relevant_image_at_angle(
                options=nmv.interface.ui_options,
                morphology=nmv.interface.ui_morphology,
                bounding_box=self.bounding_box_snap,
                angle=self.timer_limits,
                image_name=image_name,
                scene_objects=nmv.interface.ui_reconstructed_skeleton,
                panel=self)

            # Update the progress shell
            nmv.utilities.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            context.scene.NMV_MorphologyRenderingProgress = int(100 * self.timer_limits / 360.0)

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # If this is a dendrogram rendering, handle it in a very specific way.
        if nmv.interface.ui_options.morphology.reconstruction_method == \
                nmv.enums.Skeleton.Method.DENDROGRAM:

            # Cannot render a 360 of the dendrogram
            self.report({'INFO'}, 'Cannot render a 360 of the dendrogram')
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
                                 nmv.consts.Suffix.MORPHOLOGY_360)
        nmv.file.ops.clean_and_create_directory(self.output_directory)

        # Bounding box computation
        if nmv.interface.ui_options.rendering.rendering_view == nmv.enums.Rendering.View.CLOSEUP:
            bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
                extent=nmv.interface.ui_options.rendering.close_up_dimensions)
        elif nmv.interface.ui_options.rendering.rendering_view == nmv.enums.Rendering.View.MID_SHOT:
            bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes()
        else:
            bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=nmv.interface.ui_options.morphology)

        # Compute a 360 bounding box to fit the arbors
        bounding_box_360 = nmv.bbox.compute_360_bounding_box(
            bounding_box, nmv.interface.ui_morphology.soma.centroid)

        # Stretch the bounding box by few microns
        bounding_box_360.extend_bbox_uniformly(delta=nmv.consts.Image.GAP_DELTA)
	
	# Make a snap of the bounding box 
        self.bounding_box_snap = copy.deepcopy(bounding_box_360)

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

        # Multi-threading
        wm = context.window_manager
        wm.event_timer_remove(self.event_timer)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Rendering Done')

        # Confirm operation done
        return {'FINISHED'}
