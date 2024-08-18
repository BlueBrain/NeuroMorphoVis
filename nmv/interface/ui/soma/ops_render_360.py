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

# Blender imports
import bpy

# Internal imports
import nmv.bbox
import nmv.consts
import nmv.enums
import nmv.rendering
import nmv.utilities
import nmv.scene

####################################################################################################
# @NMV_RenderSoma360
####################################################################################################
class NMV_RenderSoma360(bpy.types.Operator):
    """Render a 360 movie of the soma reconstruction process"""

    # Operator parameters
    bl_idname = "nmv.render_soma_360"
    bl_label = "360"

    # Timer parameters
    event_timer = None
    timer_limits = 0

    # 360 bounding box
    bounding_box_360 = None

    # Output data
    output_directory = None

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self, context, event):

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > 360:

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel context
            self.cancel(context)

            # Finished
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Set the frame name
            image_name = '%s/%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Get a list of all the meshes in the scene
            scene_objects = nmv.scene.get_list_of_meshes_in_scene()

            nmv.rendering.renderer.render_at_angle(
                scene_objects=scene_objects,
                angle=self.timer_limits,
                bounding_box=self.bounding_box_360,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=context.scene.NMV_SomaFrameResolution,
                image_name=image_name)

            # Update the progress shell
            nmv.utilities.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            context.scene.NMV_SomaRenderingProgress = int(100 * self.timer_limits / 360.0)

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Panel context.
        """

        # Get a reference to the scene
        scene = context.scene

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.sequences_directory)

        # Compute the bounding box for the available meshes only
        rendering_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Compute a 360 bounding box to fit the arbors
        self.bounding_box_360 = nmv.bbox.compute_360_bounding_box(
            rendering_bbox, nmv.interface.ui_morphology.soma.centroid)

        # Stretch the bounding box by few microns
        self.bounding_box_360.extend_bbox_uniformly(delta=nmv.consts.Image.GAP_DELTA)

        # Create a specific directory for this soma mesh
        self.output_directory = '%s/%s%s' % \
                                (nmv.interface.ui_options.io.sequences_directory,
                                 nmv.interface.ui_options.morphology.label,
                                 nmv.consts.Suffix.SOMA_360)
        nmv.file.ops.clean_and_create_directory(self.output_directory)

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        self.event_timer = wm.event_timer_add(time_step=0.01, window=context.window)
        wm.modal_handler_add(self)

        # Modal
        return {'RUNNING_MODAL'}

    ################################################################################################
    # @cancel
    ################################################################################################
    def cancel(self, context):
        """
        Cancel the panel processing and return to the interaction mode.

        :param context:
            Panel context.
        """

        # Multi-threading
        wm = context.window_manager
        wm.event_timer_remove(self.event_timer)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Soma Rendering Done')

        # Finished
        return {'FINISHED'}


