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

# Blender imports
import bpy

# Internal imports
import nmv.bbox
import nmv.consts
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.mesh
import nmv.rendering
import nmv.scene
import nmv.skeleton
import nmv.utilities


####################################################################################################
# @NMV_RenderMesh360
####################################################################################################
class NMV_RenderMesh360(bpy.types.Operator):
    """Render a 360 view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.render_mesh_360"
    bl_label = "360"

    # Timer parameters
    start_time = 0
    event_timer = None
    timer_limits = 0

    # Collect a list of the scene objects (meshes) to be rendered before starting the rendering loop
    scene_objects = list()

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

            # Reset the orientation of the mesh
            nmv.scene.reset_orientation_of_objects(scene_objects=self.scene_objects)

            # Stats.
            rendering_time = time.time()
            global is_mesh_rendered
            is_mesh_rendered = True
            context.scene.NMV_MeshRenderingTime = rendering_time - self.start_time
            nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                                  context.scene.NMV_MeshRenderingTime)

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel context
            self.cancel(context)

            # Done
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Set the frame name
            image_name = '%s/%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Render at a specific resolution
            if context.scene.NMV_MeshRenderingResolution == \
                    nmv.enums.Rendering.Resolution.FIXED:

                # Render the image
                nmv.rendering.renderer.render_at_angle(
                    scene_objects=self.scene_objects,
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=nmv.enums.Camera.View.FRONT_360,
                    image_resolution=context.scene.NMV_MeshFrameResolution,
                    image_name=image_name)

            # Render at a specific scale factor
            else:

                # Render the image
                nmv.rendering.renderer.render_at_angle_to_scale(
                    scene_objects=self.scene_objects,
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=nmv.enums.Camera.View.FRONT_360,
                    image_scale_factor=context.scene.NMV_MeshFrameScaleFactor,
                    image_name=image_name)

            # Update the progress shell
            nmv.utilities.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            context.scene.NMV_MeshRenderingProgress = int(100 * self.timer_limits / 360.0)

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Timer
        self.start_time = time.time()

        # If no morphology is loaded, report it
        if nmv.interface.ui_morphology is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Validate the output directory
        nmv.interface.ui.validate_output_directory(panel=self, context_scene=context.scene)

        # Get a list of all the meshes in the scene
        self.scene_objects = nmv.scene.get_list_of_meshes_in_scene()

        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.sequences_directory)

        # Compute the bounding box for a close up view
        if context.scene.NMV_MeshRenderingView == nmv.enums.Rendering.View.CLOSEUP:

            # Compute the bounding box for a close up view
            rendering_bbox = nmv.bbox.compute_unified_extent_bounding_box(
                extent=context.scene.NMV_MeshCloseUpSize)

        # Compute the bounding box for a mid shot view
        elif context.scene.NMV_MeshRenderingView == nmv.enums.Rendering.View.MID_SHOT:

            # Compute the bounding box for the available meshes only
            rendering_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Compute the bounding box for the wide shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            rendering_bbox = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=nmv.interface.ui_morphology)

        # Compute a 360 bounding box to fit the arbors
        self.bounding_box_360 = nmv.bbox.compute_360_bounding_box(
            rendering_bbox, nmv.interface.ui_morphology.soma.centroid)

        # Stretch the bounding box by few microns
        self.bounding_box_360.extend_bbox_uniformly(delta=nmv.consts.Image.GAP_DELTA)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s%s' % (
            nmv.interface.ui_options.io.sequences_directory,
            nmv.interface.ui_options.morphology.label,
            nmv.consts.Suffix.MESH_360)
        nmv.file.ops.clean_and_create_directory(self.output_directory)

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
        self.report({'INFO'}, 'Mesh Rendering is Cancelled!')

        # Confirm operation done
        return {'FINISHED'}
