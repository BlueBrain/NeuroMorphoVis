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

# Blender imports
import bpy
from mathutils import Vector

# Internal modules
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.mesh
import nmv.rendering
import nmv.scene
import nmv.utilities
from .soma_panel_options import *

# A global flag to indicate if the soma is reconstructed or not
is_soma_reconstructed = False


####################################################################################################
# @SomaPanel
####################################################################################################
class SomaPanel(bpy.types.Panel):
    """Soma panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if nmv.utilities.is_blender_280() else 'TOOLS'
    bl_idname = "OBJECT_PT_NMV_SomaToolBox"
    bl_label = 'Soma Toolbox'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """Draws the panel

        :param context:
            Panel context.
        """

        # Get a reference to the scene
        scene = context.scene

        # Get a reference to the panel layout
        layout = self.layout

        # Documentation button
        documentation_button = layout.column()
        documentation_button.operator('nmv.documentation_soma', icon='URL')
        documentation_button.separator()

        # Get a reference to the soma options
        soma_options = nmv.interface.ui_options.soma

        reconstruction_method_row = layout.row()
        reconstruction_method_row.prop(scene, 'NMV_SomaReconstructionMethod')

        if scene.NMV_SomaReconstructionMethod == nmv.enums.Soma.Representation.META_BALLS:
            reconstruction_method_row = layout.row()
            reconstruction_method_row.prop(scene, 'NMV_SomaMetaBallResolution')
            soma_options.meta_ball_resolution = scene.NMV_SomaMetaBallResolution

        elif scene.NMV_SomaReconstructionMethod == nmv.enums.Soma.Representation.SOFT_BODY or \
                scene.NMV_SomaReconstructionMethod == nmv.enums.Soma.Representation.HYBRID:

            reconstruction_method_row = layout.row()
            reconstruction_method_row.prop(scene, 'NMV_SomaProfile')
            soma_options.method = scene.NMV_SomaProfile

            # Soft body options
            soft_body_params_row = layout.row()
            soft_body_params_row.label(text='Soft Body Parameters:', icon='GROUP_UVS')

            # Simulation steps
            simulation_steps_row = layout.row()
            simulation_steps_row.prop(scene, 'NMV_SimulationSteps')
            soma_options.simulation_steps = scene.NMV_SimulationSteps

            # Soft body stiffness option
            stiffness_row = layout.row()
            stiffness_row.prop(scene, 'NMV_Stiffness')
            soma_options.stiffness = scene.NMV_Stiffness

            # Radius scale factor
            radius_scale_factor_row = layout.row()
            radius_scale_factor_row.prop(scene, 'NMV_SomaRadiusScaleFactor')
            soma_options.radius_scale_factor = scene.NMV_SomaRadiusScaleFactor

            # Ico-sphere subdivision level option
            subdivision_level_row = layout.row()
            subdivision_level_row.prop(scene, 'NMV_SubdivisionLevel')
            soma_options.subdivision_level = scene.NMV_SubdivisionLevel

        else:
            pass

        # Color options
        colors_row = layout.row()
        colors_row.label(text='Colors & Materials:', icon='COLOR')

        # Soma color
        soma_base_color_row = layout.row()
        soma_base_color_row.prop(scene, 'NMV_SomaBaseColor')

        # Pass options from UI to system
        color = scene.NMV_SomaBaseColor
        soma_base_color_value = Vector((color.r, color.g, color.b))
        nmv.interface.ui_options.shading.soma_color = soma_base_color_value

        # Soma material option
        soma_material_row = layout.row()
        soma_material_row.prop(scene, 'NMV_SomaMaterial')
        nmv.interface.ui_options.shading.soma_material = scene.NMV_SomaMaterial

        # Soma reconstruction options
        soma_reconstruction_row = layout.row()
        soma_reconstruction_row.label(text='Quick Reconstruction:', icon='META_DATA')

        # Soma reconstruction button
        soma_reconstruction_buttons_row = layout.row(align=True)
        soma_reconstruction_buttons_row.operator('nmv.reconstruct_soma', icon='FORCE_LENNARDJONES')

        # Progress
        if scene.NMV_SomaReconstructionMethod == \
                nmv.enums.Soma.Representation.SOFT_BODY:

            # Soma simulation progress bar
            soma_simulation_progress_row = layout.row()
            soma_simulation_progress_row.prop(scene, 'NMV_SomaSimulationProgress')
            soma_simulation_progress_row.enabled = False

        # Report the stats
        global is_soma_reconstructed
        if is_soma_reconstructed:
            soma_stats_row = layout.row()
            soma_stats_row.label(text='Stats:', icon='RECOVER_LAST')

            reconstruction_time_row = layout.row()
            reconstruction_time_row.prop(scene, 'NMV_SomaReconstructionTime')
            reconstruction_time_row.enabled = False

        # Soma rendering options
        quick_rendering_row = layout.row()
        quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')

        # Soma frame resolution option
        frame_resolution_row = layout.row()
        frame_resolution_row.label(text='Frame Resolution:')
        frame_resolution_row.prop(scene, 'NMV_SomaFrameResolution')

        # Soma view dimensions in micron option
        view_dimensions_row = layout.row()
        view_dimensions_row.label(text='View Dimensions:')
        view_dimensions_row.prop(scene, 'NMV_ViewDimensions')
        view_dimensions_row.enabled = False

        # Image extension
        image_extension_row = layout.row()
        image_extension_row.label(text='Image Format:')
        image_extension_row.prop(scene, 'NMV_SomaImageFormat')
        nmv.interface.ui_options.soma.image_format = scene.NMV_SomaImageFormat

        # Render view buttons
        render_view_row = layout.row()
        render_view_row.label(text='Render View:', icon='RESTRICT_RENDER_OFF')
        render_view_buttons_row = layout.row(align=True)
        render_view_buttons_row.operator('nmv.render_soma_front', icon='AXIS_FRONT')
        render_view_buttons_row.operator('nmv.render_soma_side', icon='AXIS_SIDE')
        render_view_buttons_row.operator('nmv.render_soma_top', icon='AXIS_TOP')
        render_view_buttons_row.enabled = False

        # Soma render animation buttons
        render_animation_row = layout.row()
        render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
        render_animations_buttons_row = layout.row(align=True)
        render_animations_buttons_row.operator('nmv.render_soma_360', icon='FORCE_MAGNETIC')

        # Progressive rendering is only for the soft body physics
        if bpy.context.scene.NMV_SomaReconstructionMethod == nmv.enums.Soma.Representation.SOFT_BODY:
            render_animations_buttons_row.operator('nmv.render_soma_progressive',
                                                   icon='FORCE_HARMONIC')

        # Soma rendering progress bar
        soma_rendering_progress_row = layout.row()
        soma_rendering_progress_row.prop(scene, 'NMV_SomaRenderingProgress')
        soma_rendering_progress_row.enabled = False

        # Saving somata parameters
        save_soma_mesh_row = layout.row()
        save_soma_mesh_row.label(text='Save Soma Mesh As:', icon='MESH_UVSPHERE')

        # Saving somata buttons
        save_soma_mesh_buttons_column = layout.column(align=True)
        save_soma_mesh_buttons_column.operator('nmv.save_soma_mesh_obj', icon='MESH_DATA')
        save_soma_mesh_buttons_column.operator('nmv.save_soma_mesh_ply', icon='GROUP_VERTEX')
        save_soma_mesh_buttons_column.operator('nmv.save_soma_mesh_stl', icon='MESH_DATA')
        save_soma_mesh_buttons_column.operator('nmv.save_soma_mesh_blend', icon='OUTLINER_OB_META')

        # If the reconstructed soma is not available in the scene, then deactivate these buttons
        # NOTE: To activate the rendering and saving buttons in the soma panel, the reconstructed
        # soma mesh must exist in the scene, otherwise the rendered image and the saved meshes
        # will contain invalid data. To verify whether the soma is reconstructed or not, we search
        # for the soma mesh by name and accordingly activate or deactivate the buttons.

        # Ensure that the morphology is loaded to get its label
        if nmv.interface.ui_options.morphology.label is not None:

            # Does the soma mesh exist in the scene, then activate the buttons
            if nmv.scene.ops.is_object_in_scene_by_name(nmv.consts.Skeleton.SOMA_PREFIX):
                save_soma_mesh_buttons_column.enabled = True
                view_dimensions_row.enabled = True
                frame_resolution_row.enabled = True
                render_view_buttons_row.enabled = True
                render_animations_buttons_row.enabled = True

            # The soma mesh is not in the scene, then deactivate the buttons
            else:
                save_soma_mesh_buttons_column.enabled = False
                view_dimensions_row.enabled = False
                frame_resolution_row.enabled = False
                render_view_buttons_row.enabled = False
                render_animations_buttons_row.enabled = False

        # No morphology is loaded, then deactivate the buttons
        else:
            save_soma_mesh_buttons_column.enabled = False
            view_dimensions_row.enabled = False
            frame_resolution_row.enabled = False
            render_view_buttons_row.enabled = False
            render_animations_buttons_row.enabled = False

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(layout)


####################################################################################################
# @ReconstructSoma
####################################################################################################
class ReconstructSomaOperator(bpy.types.Operator):
    """Soma reconstruction operator"""

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

            # Set the reconstruction flag to on
            global is_soma_reconstructed
            is_soma_reconstructed = True

            # Get the reconstruction time to update the UI
            scene.NMV_SomaReconstructionTime = time.time() - self.reconstruction_time
            nmv.logger.info_done('Soma reconstructed in [%f] seconds' %
                            scene.NMV_MorphologyLoadingTime)

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
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Panel context.
        """

        # Get a reference to the scene
        scene = context.scene

        # Reset the scene
        nmv.scene.reset_scene()

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Reconstruction time
        self.reconstruction_time = time.time()

        # Set the reconstruction flag to on
        global is_soma_reconstructed

        # MetaBall reconstruction
        if bpy.context.scene.NMV_SomaReconstructionMethod == \
                nmv.enums.Soma.Representation.META_BALLS:

            # Create a some builder
            self.soma_builder = nmv.builders.SomaMetaBuilder(
                nmv.interface.ui_morphology, nmv.interface.ui_options)

            # Reconstruct the soma in a single step
            nmv.interface.ui_soma_mesh = self.soma_builder.reconstruct_soma_mesh()

            # Get the reconstruction time to update the UI
            self.reconstruction_time = time.time() - self.reconstruction_time
            scene.NMV_SomaReconstructionTime = self.reconstruction_time
            nmv.logger.info_done('Soma reconstructed in [%f] seconds' %
                                 scene.NMV_MorphologyLoadingTime)

            # Set the reconstruction flag to on
            is_soma_reconstructed = True

            # View all the objects in the scene
            nmv.scene.ops.view_all_scene()

            # Finished
            return {'FINISHED'}

        # MetaBall reconstruction
        elif bpy.context.scene.NMV_SomaReconstructionMethod == nmv.enums.Soma.Representation.HYBRID:

            # Create a some builder
            self.soma_builder = nmv.builders.SomaHybridBuilder(
                nmv.interface.ui_morphology, nmv.interface.ui_options)

            # Reconstruct the soma in a single step
            nmv.interface.ui_soma_mesh = self.soma_builder.reconstruct_soma_mesh()

            # Get the reconstruction time to update the UI
            self.reconstruction_time = time.time() - self.reconstruction_time
            scene.NMV_SomaReconstructionTime = self.reconstruction_time
            nmv.logger.info_done('Soma reconstructed in [%f] seconds' %
                                 scene.NMV_MorphologyLoadingTime)

            is_soma_reconstructed = True

            # View all the objects in the scene
            nmv.scene.ops.view_all_scene()

            # Finished
            return {'FINISHED'}

        # Softbody reconstruction
        else:

            # SoftBody reconstruction
            self.soma_builder = nmv.builders.SomaSoftBodyBuilder(
                nmv.interface.ui_morphology, nmv.interface.ui_options)

            # Build the basic profile of the some from the soft body operation, but don't run the
            # simulation now. Run the simulation in the '@modal' mode, to avoid freezing the UI
            if bpy.context.scene.NMV_SomaProfile == \
                    nmv.enums.Soma.Profile.ARBORS_ONLY:
                self.soma_sphere_object = self.soma_builder.build_soma_soft_body()
            elif bpy.context.scene.NMV_SomaProfile == \
                    nmv.enums.Soma.Profile.PROFILE_POINTS_ONLY:
                self.soma_sphere_object = \
                    self.soma_builder.build_soma_based_on_profile_points_only()
            elif bpy.context.scene.NMV_SomaProfile == \
                    nmv.enums.Soma.Profile.COMBINED:
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

        if bpy.context.scene.NMV_SomaProfile == \
                nmv.enums.Soma.Profile.PROFILE_POINTS_ONLY:

            # Decimate the mesh using 25%
            nmv.logger.info('Decimation')
            nmv.mesh.ops.decimate_mesh_object(self.soma_sphere_object, decimation_ratio=0.25)

            # Smooth the mesh again to look nice
            nmv.logger.info('Smoothing')
            nmv.mesh.ops.smooth_object(self.soma_sphere_object, level=2)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Soma Reconstruction Done')


####################################################################################################
# @RenderSomaFront
####################################################################################################
class RenderSomaFront(bpy.types.Operator):
    """Rendering front view of the soma operator"""

    # Operator parameters
    bl_idname = "nmv.render_soma_front"
    bl_label = "Front"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator.

        :param context:
            Context.
        :return:
            'FINISHED'
        """

        # Get a reference to the scene
        scene = context.scene

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

        # Render the soma
        nmv.rendering.SomaRenderer.render(
            view_extent=scene.NMV_ViewDimensions,
            camera_view=nmv.enums.Camera.View.FRONT,
            image_resolution=scene.NMV_SomaFrameResolution,
            image_name='%s%s' % (nmv.interface.ui_options.morphology.label,
                                 nmv.consts.Suffix.SOMA_FRONT),
            image_format=nmv.interface.ui_options.soma.image_format,
            image_directory=nmv.interface.ui_options.io.images_directory)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Rendering Soma Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderSomaSide
####################################################################################################
class RenderSomaSide(bpy.types.Operator):
    """Render side view of the reconstructed soma"""

    # Operator parameters
    bl_idname = "nmv.render_soma_side"
    bl_label = "Side"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator.

        :param context:
            Context.
        :return:
            'FINISHED'
        """

        # Get a reference to the scene
        scene = context.scene

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

        # Render the soma
        nmv.rendering.SomaRenderer.render(
            view_extent=scene.NMV_ViewDimensions,
            camera_view=nmv.enums.Camera.View.SIDE,
            image_resolution=scene.NMV_SomaFrameResolution,
            image_name='%s%s' % (nmv.interface.ui_options.morphology.label,
                                 nmv.consts.Suffix.SOMA_SIDE),
            image_format=nmv.interface.ui_options.soma.image_format,
            image_directory=nmv.interface.ui_options.io.images_directory)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Soma Reconstruction Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderSomaTop
####################################################################################################
class RenderSomaTop(bpy.types.Operator):
    """Render top view of the reconstructed soma"""

    # Operator parameters
    bl_idname = "nmv.render_soma_top"
    bl_label = "Top"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator.

        :param context:
            Context.
        :return:
            'FINISHED'
        """

        # Get a reference to the scene
        scene = context.scene

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

        # Render the soma
        nmv.rendering.SomaRenderer.render(
            view_extent=scene.NMV_ViewDimensions,
            camera_view=nmv.enums.Camera.View.TOP,
            image_resolution=scene.NMV_SomaFrameResolution,
            image_name='%s%s' % (nmv.interface.ui_options.morphology.label,
                                 nmv.consts.Suffix.SOMA_TOP),
            image_format=nmv.interface.ui_options.soma.image_format,
            image_directory=nmv.interface.ui_options.io.images_directory)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Soma Reconstruction Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderSoma360
####################################################################################################
class RenderSoma360(bpy.types.Operator):
    """Render 360 movie of the soma reconstruction process"""

    # Operator parameters
    bl_idname = "nmv.render_soma_360"
    bl_label = "360"

    # Timer parameters
    event_timer = None
    timer_limits = 0

    # Output data
    output_directory = None

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self,
              context,
              event):
        """
        Threading and non-blocking handling.

        :param context:
            Panel context.
        :param event:
            A given event for the panel.
        """

        # Get a reference to the scene
        scene = context.scene

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

            # Render a frame
            nmv.rendering.SomaRenderer.render_at_angle(
                soma_mesh=nmv.interface.ui_soma_mesh,
                angle=self.timer_limits,
                view_extent=scene.NMV_ViewDimensions,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=scene.NMV_SomaFrameResolution,
                image_name=image_name)

            # Update the progress shell
            nmv.utilities.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            scene.NMV_SomaRenderingProgress = int(100 * self.timer_limits / 360.0)

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


####################################################################################################
# @RenderSomaProgressive
####################################################################################################
class RenderSomaProgressive(bpy.types.Operator):
    """Render progressive soma reconstruction"""

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
    def modal(self,
              context,
              event):
        """
        Threading and non-blocking handling.

        :param context:
            Panel context.
        :param event:
            A given event for the panel.
        """

        # Get a reference to the scene
        scene = context.scene

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > scene.NMV_SimulationSteps:

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
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Panel context.
        """

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
        """Cancel the panel processing and return to the interaction mode.

        :param context:
            Panel context.
        """

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


####################################################################################################
# @SaveSomaMeshOBJ
####################################################################################################
class SaveSomaMeshOBJ(bpy.types.Operator):
    """Save the soma in OBJ file"""

    # Operator parameters
    bl_idname = "nmv.save_soma_mesh_obj"
    bl_label = "Wavefront (.obj)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """
        Executes the operator.

        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Export the selected soma mesh as an .obj file
        nmv.file.export_object_to_obj_file(
            mesh_object=nmv.interface.ui_soma_mesh,
            output_directory=nmv.interface.ui_options.io.meshes_directory,
            file_name='%s%s' % (nmv.interface.ui_morphology.label, nmv.consts.Suffix.SOMA_MESH))

        # Finished
        return {'FINISHED'}


####################################################################################################
# @SaveSomaMeshPLY
####################################################################################################
class SaveSomaMeshPLY(bpy.types.Operator):
    """Save the soma in PLY file"""

    # Operator parameters
    bl_idname = "nmv.save_soma_mesh_ply"
    bl_label = "Stanford (.ply)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """
        Executes the operator.

        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Export the selected soma mesh as an .ply file
        nmv.file.export_object_to_ply_file(
            mesh_object=nmv.interface.ui_soma_mesh,
            output_directory=nmv.interface.ui_options.io.meshes_directory,
            file_name='%s%s' % (nmv.interface.ui_morphology.label, nmv.consts.Suffix.SOMA_MESH))

        # Finished
        return {'FINISHED'}


####################################################################################################
# @SaveSomaMeshSTL
####################################################################################################
class SaveSomaMeshSTL(bpy.types.Operator):
    """Save the soma in STL file"""

    # Operator parameters

    bl_idname = "nmv.save_soma_mesh_stl"
    bl_label = "Stereolithography CAD (.stl)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """
        Executes the operator.

        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Export the selected soma mesh as an .stl file
        nmv.file.export_object_to_stl_file(
            mesh_object=nmv.interface.ui_soma_mesh,
            output_directory=nmv.interface.ui_options.io.meshes_directory,
            file_name='%s%s' % (nmv.interface.ui_morphology.label, nmv.consts.Suffix.SOMA_MESH))

        # Finished
        return {'FINISHED'}


####################################################################################################
# @SaveSomaMeshBlend
####################################################################################################
class SaveSomaMeshBLEND(bpy.types.Operator):
    """Save the soma in a blender file"""

    # Operator parameters
    bl_idname = "nmv.save_soma_mesh_blend"
    bl_label = "Blender Format (.blend)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """
        Executes the operator.

        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        # Get a reference to the scene
        scene = context.scene

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Export the selected soma mesh as a .blend file
        nmv.file.export_scene_to_blend_file(
            output_directory=nmv.interface.ui_options.io.meshes_directory,
            output_file_name='%s%s' % (nmv.interface.ui_morphology.label,
                                       nmv.consts.Suffix.SOMA_MESH))

        # Finished
        return {'FINISHED'}


####################################################################################################
# @SomaReconstructionDocumentation
####################################################################################################
class SomaReconstructionDocumentation(bpy.types.Operator):
    """Open the online documentation page of the Soma Reconstruction panel."""

    # Operator parameters
    bl_idname = "nmv.documentation_soma"
    bl_label = "Online User Guide"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis/wiki/Soma-Reconstruction')
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel.
    """

    # Soma reconstruction panel
    bpy.utils.register_class(SomaPanel)

    # Buttons
    bpy.utils.register_class(SomaReconstructionDocumentation)
    bpy.utils.register_class(ReconstructSomaOperator)
    bpy.utils.register_class(RenderSomaFront)
    bpy.utils.register_class(RenderSomaSide)
    bpy.utils.register_class(RenderSomaTop)
    bpy.utils.register_class(RenderSoma360)
    bpy.utils.register_class(RenderSomaProgressive)
    bpy.utils.register_class(SaveSomaMeshOBJ)
    bpy.utils.register_class(SaveSomaMeshPLY)
    bpy.utils.register_class(SaveSomaMeshSTL)
    bpy.utils.register_class(SaveSomaMeshBLEND)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel.
    """

    # Soma reconstruction panel
    bpy.utils.unregister_class(SomaPanel)

    # Buttons
    bpy.utils.unregister_class(SomaReconstructionDocumentation)
    bpy.utils.unregister_class(ReconstructSomaOperator)
    bpy.utils.unregister_class(RenderSomaFront)
    bpy.utils.unregister_class(RenderSomaSide)
    bpy.utils.unregister_class(RenderSomaTop)
    bpy.utils.unregister_class(RenderSoma360)
    bpy.utils.unregister_class(RenderSomaProgressive)
    bpy.utils.unregister_class(SaveSomaMeshOBJ)
    bpy.utils.unregister_class(SaveSomaMeshPLY)
    bpy.utils.unregister_class(SaveSomaMeshSTL)
    bpy.utils.unregister_class(SaveSomaMeshBLEND)
