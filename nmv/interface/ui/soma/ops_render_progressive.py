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

# Blender imports
import bpy

# Internal imports
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.interface
import nmv.scene
import nmv.utilities


####################################################################################################
# @NMV_RenderSomaProgressive
####################################################################################################
class NMV_RenderSomaProgressive(bpy.types.Operator):
    """Render progressive soma reconstruction sequence"""

    # Operator parameters
    bl_idname = "nmv.render_soma_progressive"
    bl_label = "Progressive"

    # Timer parameters
    event_timer = None
    timer_limits = 0

    # Output data
    output_directory = None

    # Morphology parameters
    morphology_object = None

    # Soma builder parameters
    soma_builder = None
    soma_sphere_object = None

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self, context, event):

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > context.scene.NMV_SimulationSteps:

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel context
            self.cancel(context)

            # Finished
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Update the frame based on the soft body simulation
            bpy.context.scene.frame_set(self.timer_limits)

            # Set the frame name
            image_name = '%s/%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Render a frame
            nmv.rendering.SomaRenderer.render_at_angle(
                soma_mesh=self.soma_sphere_object,
                angle=0.0,
                view_extent=scene.NMV_ViewDimensions,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=scene.NMV_SomaFrameResolution,
                image_name=image_name)

            # Update the progress shell
            nmv.utilities.show_progress('Rendering',
                                        self.timer_limits, scene.NMV_SimulationSteps)

            # Update the progress bar
            scene.NMV_SomaRenderingProgress = self.timer_limits

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.sequences_directory)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s%s' % (
            nmv.interface.ui_options.io.sequences_directory,
            nmv.interface.ui_options.morphology.label,
            nmv.consts.Suffix.SOMA_PROGRESSIVE)
        nmv.file.ops.clean_and_create_directory(self.output_directory)

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Create a some builder object
        self.soma_builder = nmv.builders.SomaSoftBodyBuilder(
            nmv.interface.ui_morphology, nmv.interface.ui_options)

        # Build the basic profile of the some from the soft body operation, but don't run the
        # simulation now. Run the simulation in the '@modal' mode, to avoid freezing the UI
        self.soma_sphere_object = self.soma_builder.build_soma_soft_body()

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

        # Multi-threading
        wm = context.window_manager
        wm.event_timer_remove(self.event_timer)

        # Build the mesh from the soft body object
        self.soma_sphere_object = self.soma_builder.build_soma_mesh_from_soft_body_object(
            self.soma_sphere_object)

        # Keep a reference to the mesh object in case we need to save or texture it
        nmv.interface.ui_soma_mesh = self.soma_sphere_object

        # Show the progress, Done
        nmv.utilities.show_progress(
            'Rendering', self.timer_limits, context.scene.NMV_SimulationSteps, done=True)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Soma Rendering Done')

        # Delete the camera
        # nmv.scene.ops.delete_list_objects([self.soma_sphere_object])


