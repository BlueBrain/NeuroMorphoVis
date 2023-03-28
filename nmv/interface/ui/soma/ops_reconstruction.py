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
import time

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.utilities
import nmv.scene
import nmv.builders
import nmv.mesh


####################################################################################################
# @NMV_ReconstructSoma
####################################################################################################
class NMV_ReconstructSoma(bpy.types.Operator):
    """Soma reconstruction"""

    # Operator parameters
    bl_idname = "nmv.reconstruct_soma"
    bl_label = "Reconstruct Soma"

    # Timer parameters
    event_timer = None
    timer_limits = 0

    # Builder parameters
    soma_builder = None
    soma_sphere_object = None

    # Reconstruction time
    reconstruction_time = 0

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self,
              context,
              event):
        """Threading and non-blocking handling.

        :param context:
            Panel context.
        :param event:
            A given event for the panel.
        """

        # Get a reference to the scene
        scene = context.scene

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or \
                self.timer_limits > scene.NMV_SimulationSteps:

            # Get the reconstruction time to update the UI
            scene.NMV_SomaReconstructionTime = time.time() - self.reconstruction_time
            nmv.logger.info_done('Soma reconstructed in [%f] seconds' %
                            scene.NMV_MorphologyLoadingTime)

            # Set the reconstruction flag to on
            nmv.interface.ui_soma_reconstructed = True

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

            # Update the progress shell
            nmv.utilities.show_progress(
                'Simulation', self.timer_limits, scene.NMV_SimulationSteps)

            # Update the progress bar
            scene.NMV_SomaSimulationProgress = \
                int(100.0 * self.timer_limits / scene.NMV_SimulationSteps)

            # Upgrade the timer limits
            self.timer_limits += 1

        # View all the objects in the scene
        nmv.scene.ops.view_all_scene()

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # If no morphology file is loaded, load the morphology file
        if nmv.interface.ui_morphology is None:
            loading_result = nmv.interface.ui.load_morphology(self, context.scene)
            if loading_result is None:
                self.report({'ERROR'}, 'Please select a morphology file')
                return {'FINISHED'}

        # Reconstruction time
        self.reconstruction_time = time.time()

        # MetaBall reconstruction
        if nmv.interface.ui_options.soma.method == nmv.enums.Soma.Representation.META_BALLS:

            # Create a some builder, and reconstruct the soma in a single step
            self.soma_builder = nmv.builders.SomaMetaBuilder(
                nmv.interface.ui_morphology, nmv.interface.ui_options)
            nmv.interface.ui_soma_mesh = self.soma_builder.reconstruct_soma_mesh()

            # Get the reconstruction time to update the UI
            self.reconstruction_time = time.time() - self.reconstruction_time
            context.scene.NMV_SomaReconstructionTime = self.reconstruction_time
            nmv.logger.info_done('Soma reconstructed in [%f] seconds' %
                                 context.scene.NMV_MorphologyLoadingTime)

            # Set the reconstruction flag to True
            nmv.interface.ui_soma_reconstructed = True

            # View all the objects in the scene
            nmv.scene.ops.view_all_scene()

            # Finished
            return {'FINISHED'}

        # MetaBall reconstruction
        elif bpy.context.scene.NMV_SomaReconstructionMethod == nmv.enums.Soma.Representation.HYBRID:

            # Create a some builder, and reconstruct the soma in a single step
            self.soma_builder = nmv.builders.SomaHybridBuilder(
                nmv.interface.ui_morphology, nmv.interface.ui_options)
            nmv.interface.ui_soma_mesh = self.soma_builder.reconstruct_soma_mesh()

            # Get the reconstruction time to update the UI
            self.reconstruction_time = time.time() - self.reconstruction_time
            context.scene.NMV_SomaReconstructionTime = self.reconstruction_time
            nmv.logger.info_done('Soma reconstructed in [%f] seconds' %
                                 context.scene.NMV_MorphologyLoadingTime)

            # Set the reconstruction flag to True
            nmv.interface.ui_soma_reconstructed = True

            # View all the objects in the scene
            nmv.scene.ops.view_all_scene()

            # Finished
            return {'FINISHED'}

        # Soft-body reconstruction
        else:

            # SoftBody reconstruction
            self.soma_builder = nmv.builders.SomaSoftBodyBuilder(
                nmv.interface.ui_morphology, nmv.interface.ui_options)

            # Build the basic profile of the soma from the soft body operation, but don't run the
            # simulation now. Run the simulation in the '@modal' mode, to avoid freezing the UI
            profile_option = nmv.interface.ui_options.soma.profile
            if profile_option == nmv.enums.Soma.Profile.ARBORS_ONLY:
                self.soma_sphere_object = self.soma_builder.build_soma_soft_body()
            elif profile_option == nmv.enums.Soma.Profile.PROFILE_POINTS_ONLY:
                self.soma_sphere_object = self.soma_builder.build_soma_based_on_profile_points_only()
            elif profile_option == nmv.enums.Soma.Profile.COMBINED:
                self.soma_sphere_object = self.soma_builder.build_soma_soft_body(
                    use_profile_points=True)
            else:
                self.soma_sphere_object = self.soma_builder.build_soma_soft_body()

            # Use the event timer to update the UI during the soma building
            wm = context.window_manager
            self.event_timer = wm.event_timer_add(time_step=0.01, window=context.window)
            wm.modal_handler_add(self)

            # View all the objects in the scene
            nmv.scene.ops.view_all_scene()

            # Modal
            return {'RUNNING_MODAL'}

    ################################################################################################
    # @cancel
    ################################################################################################
    def cancel(self, context):
        """Cancel the panel processing and return to the interaction mode.

        :param context:
            Panel context.
        """

        # Get a reference to the scene
        scene = context.scene

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
            'Simulation', self.timer_limits, scene.NMV_SimulationSteps, done=True)

        if nmv.interface.ui_options.soma.profile == nmv.enums.Soma.Profile.PROFILE_POINTS_ONLY:

            # Decimate the mesh using 25%
            nmv.logger.info('Decimation')
            nmv.mesh.ops.decimate_mesh_object(self.soma_sphere_object, decimation_ratio=0.25)

            # Smooth the mesh again to look nice
            nmv.logger.info('Smoothing')
            nmv.mesh.ops.smooth_object(self.soma_sphere_object, level=2)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Soma Reconstruction Done')
