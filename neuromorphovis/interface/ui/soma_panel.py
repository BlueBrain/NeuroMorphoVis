####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# Blender imports
import bpy
from mathutils import Vector
from bpy.props import IntProperty
from bpy.props import BoolProperty
from bpy.props import FloatProperty
from bpy.props import EnumProperty
from bpy.props import FloatVectorProperty

# Internal modules
import neuromorphovis as nmv
import neuromorphovis.builders
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.file
import neuromorphovis.interface
import neuromorphovis.mesh
import neuromorphovis.rendering
import neuromorphovis.scene
import neuromorphovis.utilities


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
    bl_context = 'objectmode'
    bl_category = 'NeuroMorphoVis'

    ################################################################################################
    # Panel options
    ################################################################################################
    # Soma color option
    bpy.types.Scene.SomaBaseColor = FloatVectorProperty(
        name="Soma Base Color", subtype='COLOR',
        description="The color of the reconstructed soma",
        default=(1.0, 0.0, 0.0), min=0.0, max=1.0)

    # Reconstruction method
    bpy.types.Scene.SomaReconstructionMethod = EnumProperty(
        items=[(nmv.enums.Soma.ReconstructionMethod.COMBINED,
                'Complex',
                'Reconstruct a complex shape for the soma using all available data'),
               (nmv.enums.Soma.ReconstructionMethod.ARBORS_ONLY,
                'Arbors',
                'Reconstruct the shape of the soma using the arbors only'),
               (nmv.enums.Soma.ReconstructionMethod.PROFILE_POINTS_ONLY,
                'Profile',
                'Reconstruct the shape of the soma using the profile points only')],
        name='Method',
        default=nmv.enums.Soma.ReconstructionMethod.ARBORS_ONLY)

    # The material applied to the soma mesh following to the reconstruction
    bpy.types.Scene.SomaMaterial = EnumProperty(
        items=nmv.enums.Shading.MATERIAL_ITEMS,
        name="Material",
        default=nmv.enums.Shading.LAMBERT_WARD)

    # Soft body stiffness option
    bpy.types.Scene.Stiffness = FloatProperty(
        name="Stiffness",
        description="The spring factor (or stiffness) of the soft body",
        default=0.1, min=0.001, max=0.999)

    # Ico-sphere subdivision level option
    bpy.types.Scene.SubdivisionLevel = IntProperty(
        name="Subdivisions",
        description="Subdivision level of the ico-sphere (2-10), convenient 5",
        default=5, min=2, max=10)

    # Simulation step option
    bpy.types.Scene.SimulationSteps = IntProperty(
        name="Simulation Steps",
        description="The number of steps required to do the simulation",
        default=100, min=10, max=1000)

    # Soma simulation progress bar
    bpy.types.Scene.SomaSimulationProgress = IntProperty(
        name="Soma Simulation Progress",
        default=0, min=0, max=100, subtype='PERCENTAGE')

    # Keep cameras
    bpy.types.Scene.KeepSomaCameras = BoolProperty(
        name="Keep Cameras & Lights in Scene",
        description="Keep the cameras in the scene to be used later if this file is saved",
        default=False)

    # View size option in microns
    bpy.types.Scene.ViewDimensions = FloatProperty(
        name="Dimensions",
        description="The dimensions of the view that will be rendered in microns",
        default=20, min=5, max=50)

    # Frame resolution option
    bpy.types.Scene.SomaFrameResolution = IntProperty(
        name="Resolution",
        description="The resolution of the image generated from rendering the soma",
        default=512, min=128, max=1024 * 10)

    # Soma rendering progress bar
    bpy.types.Scene.SomaRenderingProgress = IntProperty(
        name="Soma Rendering Progress",
        default=0, min=0, max=100, subtype='PERCENTAGE')

    # Irregular subdivisions for the faces extruded for emanating the arbors
    bpy.types.Scene.IrregularSubdivisions = BoolProperty(
        name="Irregular Subdivisions",
        description="Make further irregular subdivisions for the faces created for the arbors",
        default=True)

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """
        Draws the panel.

        :param context: Panel context.
        """

        # Get a reference to the panel layout
        layout = self.layout

        reconstruction_method_row = layout.row()
        reconstruction_method_row.label(text='Method:')
        reconstruction_method_row.prop(context.scene, 'SomaReconstructionMethod', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.soma.method = context.scene.SomaReconstructionMethod

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

        # Simulation steps
        simulation_steps_row = layout.row()
        simulation_steps_row.prop(context.scene, 'SimulationSteps')

        # Pass options from UI to system
        nmv.interface.ui_options.soma.simulation_steps = context.scene.SimulationSteps

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


####################################################################################################
# @ReconstructSoma
####################################################################################################
class ReconstructSomaOperator(bpy.types.Operator):
    """Soma reconstruction operator"""

    # Operator parameters
    bl_idname = "reconstruct.soma"
    bl_label = "Soma"

    # Timer parameters
    event_timer = None
    timer_limits = bpy.props.IntProperty(default=0)

    meshy_soma_builder = None
    soma_sphere_object = None
    min_simulation_limit = nmv.consts.Simulation.MIN_FRAME
    max_simulation_limit = nmv.consts.Simulation.MAX_FRAME

    ################################################################################################
    # @load_morphology
    ################################################################################################
    def load_morphology(self,
                        scene):
        """Loads the morphology.

        :param scene:
            Scene.
        """

        # Read the data from a given morphology file either in .h5 or .swc formats
        if bpy.context.scene.InputSource == nmv.enums.Input.H5_SWC_FILE:

            # Pass options from UI to system
            nmv.interface.ui_options.morphology.morphology_file_path = scene.MorphologyFile

            # Update the morphology label
            nmv.interface.ui_options.morphology.label = nmv.file.ops.get_file_name_from_path(
                scene.MorphologyFile)

            # Load the morphology from the file
            loading_flag, morphology_object = nmv.file.readers.read_morphology_from_file(
                options=nmv.interface.ui_options)

            # Verify the loading operation
            if loading_flag:

                # Update the morphology
                nmv.interface.ui_morphology = morphology_object

            # Otherwise, report an ERROR
            else:
                self.report({'ERROR'}, 'Invalid Morphology File')

        # Read the data from a specific gid in a given circuit
        elif bpy.context.scene.InputSource == nmv.enums.Input.CIRCUIT_GID:

            # Pass options from UI to system
            nmv.interface.ui_options.morphology.blue_config = scene.CircuitFile
            nmv.interface.ui_options.morphology.gid = scene.Gid

            # Update the morphology label
            nmv.interface.ui_options.morphology.label = 'neuron_' + str(scene.Gid)

            # Load the morphology from the circuit
            loading_flag, morphology_object = \
                nmv.file.readers.BBPReader.load_morphology_from_circuit(
                    blue_config=nmv.interface.ui_options.morphology.blue_config,
                    gid=nmv.interface.ui_options.morphology.gid)

            # Verify the loading operation
            if loading_flag:

                # Update the morphology
                nmv.interface.ui_morphology = morphology_object

            # Otherwise, report an ERROR
            else:

                self.report({'ERROR'}, 'Cannot Load Morphology from Circuit')

        else:

            # Report an invalid input source
            self.report({'ERROR'}, 'Invalid Input Source')

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self,
              context,
              event):
        """
        Threading and non-blocking handling.

        :param context: Panel context.
        :param event: A given event for the panel.
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

            # Update the progress shell
            nmv.utilities.show_progress(
                'Simulation', self.timer_limits, self.max_simulation_limit)

            # Update the progress bar
            context.scene.SomaSimulationProgress = self.timer_limits

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """
        Execute the operator.

        :param context: Panel context.
        """

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology
        self.load_morphology(scene=context.scene)

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
            nmv.logger.log_sub_header('Decimation')
            nmv.mesh.ops.decimate_mesh_object(self.soma_sphere_object, decimation_ratio=0.25)

            # Smooth the mesh again to look nice
            nmv.logger.log_sub_header('Smoothing')
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
        """
        Execute the operator.

        :param context: Context.
        :return: 'FINISHED'
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
        """
        Execute the operator.

        :param context: Context.
        :return: 'FINISHED'
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
        """
        Execute the operator.

        :param context: Context.
        :return: 'FINISHED'
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

        :param context: Panel context.
        :param event: A given event for the panel.
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
        """
        Execute the operator.

        :param context: Panel context.
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

        :param context: Panel context.
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
    # @load_morphology
    ################################################################################################
    def load_morphology(self,
                        context_scene):
        """
        Loads the morphology from file.

        :param context_scene:
            The current scene in the rendering context.
        """

        # Read the data from a given morphology file either in .h5 or .swc formats
        if bpy.context.scene.InputSource == nmv.enums.Input.H5_SWC_FILE:

            # Pass options from UI to system
            nmv.interface.ui_options.morphology.morphology_file_path = context_scene.MorphologyFile

            # Update the morphology label
            nmv.interface.ui_options.morphology.label = nmv.file.ops.get_file_name_from_path(
                context_scene.MorphologyFile)

            # Load the morphology from the file
            loading_flag, morphology_object = nmv.file.read_morphology_from_file(
                options=nmv.interface.ui_options)

            # Verify the loading operation
            if loading_flag:
                # Update the morphology
                nmv.interface.ui_morphology = morphology_object

            # Otherwise, report an ERROR
            else:
                self.report({'ERROR'}, 'Invalid Morphology File')

        # Read the data from a specific gid in a given circuit
        elif bpy.context.scene.InputSource == nmv.enums.Input.CIRCUIT_GID:
            # Pass options from UI to system
            nmv.interface.ui_options.morphology.blue_config = context_scene.CircuitFile
            nmv.interface.ui_options.morphology.gid = context_scene.Gid

            # Update the morphology label
            nmv.interface.ui_options.morphology.label = 'neuron_' + str(context_scene.Gid)

            # Load the morphology from the circuit
            loading_flag, morphology_object = nmv.file.load_from_circuit(
                options=nmv.interface.ui_options)

            # Verify the loading operation
            if loading_flag:
                # Update the morphology
                nmv.interface.ui_morphology = morphology_object

            # Otherwise, report an ERROR
            else:
                self.report({'ERROR'}, 'Cannot Load Morphology from Circuit')

        else:
            # Report an invalid input source
            self.report({'ERROR'}, 'Invalid Input Source')

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self,
              context,
              event):
        """
        Threading and non-blocking handling.

        :param context: Panel context.
        :param event: A given event for the panel.
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
        """
        Execute the operator.

        :param context: Panel context.
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
        """
        Cancel the panel processing and return to the interaction mode.

        :param context: Panel context.
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

        :param context: Operator context.
        :return: {'FINISHED'}
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

        :param context: Operator context.
        :return: {'FINISHED'}
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

        :param context: Operator context.
        :return: {'FINISHED'}
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

        :param context: Operator context.
        :return: {'FINISHED'}
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
    """
    Registers all the classes in this panel.
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
    """
    Un-registers all the classes in this panel.
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
