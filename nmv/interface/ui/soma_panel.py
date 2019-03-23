####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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

# Blender imports
import bpy
from mathutils import Vector
from bpy.props import IntProperty
from bpy.props import BoolProperty
from bpy.props import FloatProperty
from bpy.props import EnumProperty
from bpy.props import FloatVectorProperty

# Internal modules
import nmv
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


####################################################################################################
# @SomaPanel
####################################################################################################
class SomaPanel(bpy.types.Panel):
    """Soma panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
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

        # Get a reference to the panel layout
        layout = self.layout

        reconstruction_method_row = layout.row()
        reconstruction_method_row.label(text='Method:')
        reconstruction_method_row.prop(context.scene, 'SomaReconstructionMethod', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.soma.method = context.scene.SomaReconstructionMethod

        # Soft body options
        soft_body_params_row = layout.row()
        soft_body_params_row.label(text='Soft Body Parameters:', icon='GROUP_UVS')

        # Soft body stiffness option
        stiffness_row = layout.row()
        stiffness_row.prop(context.scene, 'Stiffness')

        # Pass options from UI to system
        nmv.interface.ui_options.soma.stiffness = context.scene.Stiffness

        # Ico-sphere subdivision level option
        subdivision_level_row = layout.row()
        subdivision_level_row.prop(context.scene, 'SubdivisionLevel')
        irregular_subdivisions_row = layout.row()
        irregular_subdivisions_row.prop(context.scene, 'IrregularSubdivisions')

        # Pass options from UI to system
        nmv.interface.ui_options.soma.subdivision_level = context.scene.SubdivisionLevel
        nmv.interface.ui_options.soma.irregular_subdivisions = context.scene.IrregularSubdivisions

        # Color options
        colors_row = layout.row()
        colors_row.label(text='Colors & Materials:', icon='COLOR')

        # Soma color
        soma_base_color_row = layout.row()
        soma_base_color_row.prop(context.scene, 'SomaBaseColor')

        # Pass options from UI to system
        color = context.scene.SomaBaseColor
        soma_base_color_value = Vector((color.r, color.g, color.b))
        nmv.interface.ui_options.soma.soma_color = soma_base_color_value

        # Soma material option
        soma_material_row = layout.row()
        soma_material_row.prop(context.scene, 'SomaMaterial')

        # Pass options from UI to system
        nmv.interface.ui_options.soma.soma_material = context.scene.SomaMaterial

        # Soma reconstruction options
        soma_reconstruction_row = layout.row()
        soma_reconstruction_row.label(text='Quick Reconstruction:', icon='META_DATA')

        # Soma reconstruction button
        soma_reconstruction_buttons_row = layout.row(align=True)
        soma_reconstruction_buttons_row.operator('reconstruct.soma', icon='FORCE_LENNARDJONES')

        # Soma simulation progress bar
        soma_simulation_progress_row = layout.row()
        soma_simulation_progress_row.prop(context.scene, 'SomaSimulationProgress')
        soma_simulation_progress_row.enabled = False

        # Soma rendering options
        quick_rendering_row = layout.row()
        quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')

        # Soma frame resolution option
        frame_resolution_row = layout.row()
        frame_resolution_row.label(text='Frame Resolution:')
        frame_resolution_row.prop(context.scene, 'SomaFrameResolution')

        # Soma view dimensions in micron option
        view_dimensions_row = layout.row()
        view_dimensions_row.label(text='View Dimensions:')
        view_dimensions_row.prop(context.scene, 'ViewDimensions')
        view_dimensions_row.enabled = False

        # Soma view dimensions in micron option
        keep_cameras_row = layout.row()
        keep_cameras_row.prop(context.scene, 'KeepSomaCameras')
        keep_cameras_row.enabled = False

        # Render view buttons
        render_view_row = layout.row()
        render_view_row.label(text='Render View:', icon='RESTRICT_RENDER_OFF')
        render_view_buttons_row = layout.row(align=True)
        render_view_buttons_row.operator('render_soma.front', icon='AXIS_FRONT')
        render_view_buttons_row.operator('render_soma.side', icon='AXIS_SIDE')
        render_view_buttons_row.operator('render_soma.top', icon='AXIS_TOP')
        render_view_buttons_row.enabled = False

        # Soma render animation buttons
        render_animation_row = layout.row()
        render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
        render_animations_buttons_row = layout.row(align=True)
        render_animations_buttons_row.operator('render_soma.360', icon='FORCE_MAGNETIC')
        render_animations_buttons_row.operator('render_soma.progressive', icon='FORCE_HARMONIC')

        # Soma rendering progress bar
        soma_rendering_progress_row = layout.row()
        soma_rendering_progress_row.prop(context.scene, 'SomaRenderingProgress')
        soma_rendering_progress_row.enabled = False

        # Saving somata parameters
        save_soma_mesh_row = layout.row()
        save_soma_mesh_row.label(text='Save Soma Mesh As:', icon='MESH_UVSPHERE')

        # Saving somata buttons
        save_soma_mesh_buttons_column = layout.column(align=True)
        save_soma_mesh_buttons_column.operator('save_soma_mesh.obj', icon='MESH_DATA')
        save_soma_mesh_buttons_column.operator('save_soma_mesh.ply', icon='GROUP_VERTEX')
        save_soma_mesh_buttons_column.operator('save_soma_mesh.stl', icon='RETOPO')
        save_soma_mesh_buttons_column.operator('save_soma_mesh.blend', icon='OUTLINER_OB_META')

        # If the reconstructed soma is not available in the scene, then deactivate these buttons
        # NOTE: To activate the rendering and saving buttons in the soma panel, the reconstructed
        # soma mesh must exist in the scene, otherwise the rendered image and the saved meshes
        # will contain invalid data. To verify whether the soma is reconstructed or not, we search
        # for the soma mesh by name and accordingly activate or deactivate the buttons.

        # Ensure that the morphology is loaded to get its label
        if nmv.interface.ui_options.morphology.label is not None:

            # Get the soma mesh name
            reconstructed_soma_mesh_name = nmv.interface.ui_options.morphology.label + '_soma'

            # Does the soma mesh exist in the scene
            if nmv.scene.ops.is_object_in_scene_by_name(reconstructed_soma_mesh_name):

                # Activate the buttons
                save_soma_mesh_buttons_column.enabled = True
                view_dimensions_row.enabled = True
                keep_cameras_row.enabled = True
                frame_resolution_row.enabled = True
                render_view_buttons_row.enabled = True
                render_animations_buttons_row.enabled = True

            # The soma mesh is not in the scene
            else:

                # Deactivate the buttons
                save_soma_mesh_buttons_column.enabled = False
                view_dimensions_row.enabled = False
                keep_cameras_row.enabled = False
                frame_resolution_row.enabled = False
                render_view_buttons_row.enabled = False
                render_animations_buttons_row.enabled = False

        # No morphology is loaded
        else:

            # Deactivate the buttons
            save_soma_mesh_buttons_column.enabled = False
            view_dimensions_row.enabled = False
            keep_cameras_row.enabled = False
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
    bl_idname = "reconstruct.soma"
    bl_label = "Reconstruct Soma"

    # Timer parameters
    event_timer = None
    timer_limits = bpy.props.IntProperty(default=0)

    meshy_soma_builder = None
    soma_sphere_object = None
    min_simulation_limit = nmv.consts.Simulation.MIN_FRAME
    max_simulation_limit = nmv.consts.Simulation.MAX_FRAME

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

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > self.max_simulation_limit:

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel context
            self.cancel(context)

            # Done
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Update the frame based on the soft body simulation
            bpy.context.scene.frame_set(self.timer_limits)

            # Update the progress shell
            nmv.utilities.show_progress(
                'Simulation', self.timer_limits, self.max_simulation_limit)

            # Update the progress bar
            context.scene.SomaSimulationProgress = self.timer_limits

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

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Create a some builder
        self.meshy_soma_builder = nmv.builders.SomaBuilder(
            nmv.interface.ui_morphology, nmv.interface.ui_options)

        # Build the basic profile of the some from the soft body operation, but don't run the
        # simulation now. Run the simulation in the '@modal' mode, to avoid freezing the UI
        if bpy.context.scene.SomaReconstructionMethod == \
                nmv.enums.Soma.ReconstructionMethod.ARBORS_ONLY:
            self.soma_sphere_object = self.meshy_soma_builder.build_soma_soft_body()
        elif bpy.context.scene.SomaReconstructionMethod == \
                nmv.enums.Soma.ReconstructionMethod.PROFILE_POINTS_ONLY:
            self.soma_sphere_object = \
                self.meshy_soma_builder.build_soma_based_on_profile_points_only()
        elif bpy.context.scene.SomaReconstructionMethod == \
                nmv.enums.Soma.ReconstructionMethod.COMBINED:
            self.soma_sphere_object = self.meshy_soma_builder.build_soma_soft_body(
                use_profile_points=True)
        else:
            self.soma_sphere_object = self.meshy_soma_builder.build_soma_soft_body()

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        self.event_timer = wm.event_timer_add(time_step=0.01, window=context.window)
        wm.modal_handler_add(self)

        # View all the objects in the scene
        nmv.scene.ops.view_all_scene()

        # Done
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
        self.soma_sphere_object = self.meshy_soma_builder.build_soma_mesh_from_soft_body_object(
            self.soma_sphere_object)

        # Keep a reference to the mesh object in case we need to save or texture it
        nmv.interface.ui_soma_mesh = self.soma_sphere_object

        # Show the progress, Done
        nmv.utilities.show_progress(
            'Simulation', self.timer_limits, self.max_simulation_limit, done=True)

        if bpy.context.scene.SomaReconstructionMethod == \
                nmv.enums.Soma.ReconstructionMethod.PROFILE_POINTS_ONLY:

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
    bl_idname = "render_soma.front"
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

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        nmv.logger.log(context.scene.OutputDirectory)
        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

        # Render the soma
        nmv.rendering.SomaRenderer.render(
            view_extent=context.scene.ViewDimensions,
            camera_view=nmv.enums.Camera.View.FRONT,
            image_resolution=context.scene.SomaFrameResolution,
            image_name='SOMA_MESH_FRONT_%s' % nmv.interface.ui_options.morphology.label,
            image_directory=nmv.interface.ui_options.io.images_directory,
            keep_camera_in_scene=context.scene.KeepSomaCameras)

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
    bl_idname = "render_soma.side"
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

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

        # Render the soma
        nmv.rendering.SomaRenderer.render(
            view_extent=context.scene.ViewDimensions,
            camera_view=nmv.enums.Camera.View.SIDE,
            image_resolution=context.scene.SomaFrameResolution,
            image_name='SOMA_MESH_SIDE_%s' % nmv.interface.ui_options.morphology.label,
            image_directory=nmv.interface.ui_options.io.images_directory,
            keep_camera_in_scene=context.scene.KeepSomaCameras)

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
    bl_idname = "render_soma.top"
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

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

        # Render the soma
        nmv.rendering.SomaRenderer.render(
            view_extent=context.scene.ViewDimensions,
            camera_view=nmv.enums.Camera.View.TOP,
            image_resolution=context.scene.SomaFrameResolution,
            image_name='SOMA_MESH_TOP_%s' % nmv.interface.ui_options.morphology.label,
            image_directory=nmv.interface.ui_options.io.images_directory,
            keep_camera_in_scene=context.scene.KeepSomaCameras)

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
    bl_idname = "render_soma.360"
    bl_label = "360"

    # Timer parameters
    event_timer = None
    timer_limits = bpy.props.IntProperty(default=0)

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

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > 360:

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

            # Render a frame
            nmv.rendering.SomaRenderer.render_at_angle(
                soma_mesh=nmv.interface.ui_soma_mesh,
                angle=self.timer_limits,
                view_extent=context.scene.ViewDimensions,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=context.scene.SomaFrameResolution,
                image_name=image_name)

            # Update the progress shell
            nmv.utilities.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            context.scene.SomaRenderingProgress = int(100 * self.timer_limits / 360.0)

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

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.sequences_directory)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_soma_mesh_360' % \
                                (nmv.interface.ui_options.io.sequences_directory,
                                 nmv.interface.ui_options.morphology.label)
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

        :param context:
            Panel context.
        """

        # Multi-threading
        wm = context.window_manager
        wm.event_timer_remove(self.event_timer)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Soma Rendering Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderSomaProgressive
####################################################################################################
class RenderSomaProgressive(bpy.types.Operator):
    """Render progressive soma reconstruction"""

    # Operator parameters
    bl_idname = "render_soma.progressive"
    bl_label = "Progressive"

    # Timer parameters
    event_timer = None
    timer_limits = bpy.props.IntProperty(default=0)

    # Output data
    output_directory = None

    # Morphology parameters
    morphology_object = None

    # Meshy soma builder parameters
    soma_builder = None
    soma_sphere_object = None
    min_simulation_limit = nmv.consts.Simulation.MIN_FRAME
    max_simulation_limit = nmv.consts.Simulation.MAX_FRAME

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
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > self.max_simulation_limit:

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel context
            self.cancel(context)

            # Done
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Update the frame based on the soft body simulation
            bpy.context.scene.frame_set(self.timer_limits)

            # Set the frame name
            image_name = '%s/frame_%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Render a frame
            nmv.rendering.SomaRenderer.render_at_angle(
                soma_mesh=nmv.interface.ui_soma_mesh,
                angle=0.0,
                view_extent=context.scene.ViewDimensions,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=context.scene.SomaFrameResolution,
                image_name=image_name)

            # Update the progress shell
            nmv.utilities.show_progress('Rendering', self.timer_limits, self.max_simulation_limit)

            # Update the progress bar
            context.scene.SomaRenderingProgress = self.timer_limits

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

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Get a reference to the scene
        scene = context.scene

        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.sequences_directory)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_soma_mesh_progressive' % (
            nmv.interface.ui_options.io.sequences_directory,
            nmv.interface.ui_options.morphology.label)
        nmv.file.ops.clean_and_create_directory(self.output_directory)

        # Load the morphology
        self.load_morphology(context_scene=context.scene)

        # Create a some builder object
        self.soma_builder = nmv.builders.SomaBuilder(
            nmv.interface.ui_morphology, nmv.interface.ui_options)

        # Build the basic profile of the some from the soft body operation, but don't run the
        # simulation now. Run the simulation in the '@modal' mode, to avoid freezing the UI
        self.soma_sphere_object = self.soma_builder.build_soma_soft_body()

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
            'Rendering', self.timer_limits, self.max_simulation_limit, done=True)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Soma Rendering Done')

        # Delete the camera
        nmv.scene.ops.delete_list_objects([self.soma_sphere_object])


####################################################################################################
# @SaveSomaMeshOBJ
####################################################################################################
class SaveSomaMeshOBJ(bpy.types.Operator):
    """Save the soma in OBJ file"""

    # Operator parameters
    bl_idname = "save_soma_mesh.obj"
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

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Export the selected soma mesh as an .obj file
        nmv.file.export_object_to_obj_file(
            mesh_object=nmv.interface.ui_soma_mesh,
            output_directory=nmv.interface.ui_options.io.meshes_directory,
            output_file_name='%s_soma' % nmv.interface.ui_morphology.label)

        return {'FINISHED'}


####################################################################################################
# @SaveSomaMeshPLY
####################################################################################################
class SaveSomaMeshPLY(bpy.types.Operator):
    """Save the soma in PLY file"""

    # Operator parameters
    bl_idname = "save_soma_mesh.ply"
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

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Export the selected soma mesh as an .ply file
        nmv.file.export_object_to_ply_file(
            mesh_object=nmv.interface.ui_soma_mesh,
            output_directory=nmv.interface.ui_options.io.meshes_directory,
            output_file_name='%s_soma' % nmv.interface.ui_morphology.label)

        return {'FINISHED'}


####################################################################################################
# @SaveSomaMeshSTL
####################################################################################################
class SaveSomaMeshSTL(bpy.types.Operator):
    """Save the soma in STL file"""

    # Operator parameters

    bl_idname = "save_soma_mesh.stl"
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

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Export the selected soma mesh as an .stl file
        nmv.file.export_object_to_stl_file(
            mesh_object=nmv.interface.ui_soma_mesh,
            output_directory=nmv.interface.ui_options.io.meshes_directory,
            output_file_name='%s_soma' % nmv.interface.ui_morphology.label)

        return {'FINISHED'}


####################################################################################################
# @SaveSomaMeshBlend
####################################################################################################
class SaveSomaMeshBLEND(bpy.types.Operator):
    """Save the soma in a blender file"""

    # Operator parameters
    bl_idname = "save_soma_mesh.blend"
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

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Export the selected soma mesh as an .blend file
        nmv.file.export_object_to_blend_file(
            mesh_object=nmv.interface.ui_soma_mesh,
            output_directory=nmv.interface.ui_options.io.meshes_directory,
            output_file_name='%s_soma' % nmv.interface.ui_morphology.label)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel.
    """

    # Soma reconstruction panel
    bpy.utils.register_class(SomaPanel)

    # Soma reconstruction operators
    bpy.utils.register_class(ReconstructSomaOperator)

    # Soma rendering operators
    bpy.utils.register_class(RenderSomaFront)
    bpy.utils.register_class(RenderSomaSide)
    bpy.utils.register_class(RenderSomaTop)
    bpy.utils.register_class(RenderSoma360)
    bpy.utils.register_class(RenderSomaProgressive)

    # Soma saving operators
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

    # Soma reconstruction
    bpy.utils.unregister_class(ReconstructSomaOperator)

    # Soma rendering
    bpy.utils.unregister_class(RenderSomaFront)
    bpy.utils.unregister_class(RenderSomaSide)
    bpy.utils.unregister_class(RenderSomaTop)
    bpy.utils.unregister_class(RenderSoma360)
    bpy.utils.unregister_class(RenderSomaProgressive)

    # Soma saving
    bpy.utils.unregister_class(SaveSomaMeshOBJ)
    bpy.utils.unregister_class(SaveSomaMeshPLY)
    bpy.utils.unregister_class(SaveSomaMeshSTL)
    bpy.utils.unregister_class(SaveSomaMeshBLEND)
