"""ui_soft_body_panel.py:
    The panel that has the soft body options for somata reconstruction.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2017, Blue Brain Project / EPFL"
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# System imports
import sys, os

# Blender imports
import bpy
from mathutils import Vector
from bpy.props import (IntProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty,
                       FloatVectorProperty)

# Append the modules path to the system paths to be able to load the internal python modules
sys.path.append("%s/../modules" % os.path.dirname(os.path.realpath(__file__)))

# Internal modules
import bounding_box
import camera_ops
import consts
import enumerators
import exporters
import file_ops
import morphology_loader
import rendering_ops
import scene_ops
import soma_builder
import time_line
import ui_interface


# A global reference to the reconstructed soma mesh.
# This reference is used to link the operations in the other panels in the add-on with this panel.
reconstructed_soma_mesh = None


####################################################################################################
# @SoftBodyOptions
####################################################################################################
class SoftBodyOptions(bpy.types.Panel):
    """Soft body options for somata reconstruction"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Soma Reconstruction Options'
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

    # Soma material lambert or electron
    bpy.types.Scene.SomaMaterial = EnumProperty(
        items=[(enumerators.__rendering_lambert__,
                'Lambert',
                "Use a Lambert shader"),
               (enumerators.__rendering_super_electron_light__,
                'Super Electron Light',
                "Use Highly Detailed Light Electron Shader"),
               (enumerators.__rendering_super_electron_dark__,
                'Super Electron Dark',
                "Use Highly Detailed Dark Electron Shader"),
               (enumerators.__rendering_electron_light__,
                'Electron Light',
                "Use Light Electron shader"),
               (enumerators.__rendering_electron_dark__,
                'Electron Dark',
                "Use Dark Electron shader"),
               (enumerators.__rendering_shadow__,
                'Shadow',
                "Use Shadows Shader"),
               (enumerators.__rendering_flat__,
                'Flat',
                "Use Flat Shader")],
        name="Material",
        default=enumerators.__rendering_lambert__)

    # Soft body stiffness option
    bpy.types.Scene.Stiffness = FloatProperty(
        name="Stiffness",
        description="The spring factor (or stiffness) of the soft body",
        default=0.5, min=0.001, max=0.999)

    # Ico-sphere subdivision level option
    bpy.types.Scene.SubdivisionLevel = IntProperty(
        name="Subdivision",
        description="Subdivision level of the ico-sphere (2-10), convenient 4",
        default=4, min=2, max=10)

    # Simulation step option
    bpy.types.Scene.SimulationSteps = IntProperty(
        name="Simulation Steps",
        description="The number of steps required to do the simulation",
        default=100, min=10, max=1000)

    # Soma simulation progress bar
    bpy.types.Scene.SomaSimulationProgress = IntProperty(
        name="Soma Simulation Progress", default=0, min=0, max=100, subtype='PERCENTAGE')

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
        name="Soma Rendering Progress", default=0, min=0, max=100, subtype='PERCENTAGE')

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

        # Get a reference to the scene
        scene = context.scene

        # Color options
        colors_row = layout.row()
        colors_row.label(text='Colors & Materials:', icon='COLOR')

        # Soma color
        soma_base_color_row = layout.row()
        soma_base_color_row.prop(scene, 'SomaBaseColor')

        # Pass options from UI to system
        color = scene.SomaBaseColor
        soma_base_color_value = Vector((color.r, color.g, color.b))
        ui_interface.options.soft_body.soma_color = soma_base_color_value

        # Soma material option
        soma_material_row = layout.row()
        soma_material_row.prop(scene, 'SomaMaterial')

        # Pass options from UI to system
        ui_interface.options.soft_body.soma_material = scene.SomaMaterial

        # Soft body options
        soft_body_params_row = layout.row()
        soft_body_params_row.label(text='Soft Body Parameters:', icon='GROUP_UVS')

        # Soft body stiffness option
        stiffness_row = layout.row()
        stiffness_row.prop(scene, 'Stiffness')

        # Pass options from UI to system
        ui_interface.options.soft_body.stiffness = scene.Stiffness

        # Ico-sphere subdivision level option
        subdivision_level_row = layout.row()
        subdivision_level_row.prop(scene, 'SubdivisionLevel')

        # Pass options from UI to system
        ui_interface.options.soft_body.subdivision_level = scene.SubdivisionLevel

        # Simulation steps
        simulation_steps_row = layout.row()
        simulation_steps_row.prop(scene, 'SimulationSteps')

        # Pass options from UI to system
        ui_interface.options.soft_body.simulation_steps = scene.SimulationSteps

        # Soma reconstruction options
        soma_reconstruction_row = layout.row()
        soma_reconstruction_row.label(text='Quick Reconstruction:', icon='META_DATA')

        # Soma reconstruction buttons
        soma_reconstruction_buttons_row = layout.row(align=True)
        soma_reconstruction_buttons_row.operator('reconstruct.soma', icon='FORCE_LENNARDJONES')
        soma_reconstruction_buttons_row.operator('reconstruct.soma_profile', icon='SURFACE_NSPHERE')

        # Soma simulation progress bar
        soma_simulation_progress_row = layout.row()
        soma_simulation_progress_row.prop(scene, 'SomaSimulationProgress')
        soma_simulation_progress_row.enabled = False

        # Soma rendering options
        quick_rendering_row = layout.row()
        quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')

        # Soma frame resolution option
        frame_resolution_row = layout.row()
        frame_resolution_row.label(text='Frame Resolution:')
        frame_resolution_row.prop(scene, 'SomaFrameResolution')

        # Soma view dimensions in micron option
        view_dimensions_row = layout.row()
        view_dimensions_row.label(text='View Dimensions:')
        view_dimensions_row.prop(scene, 'ViewDimensions')
        view_dimensions_row.enabled = False

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
        soma_rendering_progress_row.prop(scene, 'SomaRenderingProgress')
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

        # If no given data, then disable some buttons
        global reconstructed_soma_mesh
        if nmv.scene.ops.is_object_in_scene(reconstructed_soma_mesh):
            save_soma_mesh_buttons_column.enabled = True
            view_dimensions_row.enabled = True
            frame_resolution_row.enabled = True
            render_view_buttons_row.enabled = True
            render_animations_buttons_row.enabled = True
        else:
            save_soma_mesh_buttons_column.enabled = False
            view_dimensions_row.enabled = False
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

    # Meshy soma builder parameters
    meshy_soma_builder = None
    soma_sphere_object = None
    min_simulation_limit = nmv.consts.__min_simulation_frame__
    max_simulation_limit = nmv.consts.__max_simulation_frame__

    ################################################################################################
    # @load_morphology
    ################################################################################################
    def load_morphology(self, scene):
        """
        Loads the morphology from file.

        :param scene: Scene.
        """

        # Read the data from a given morphology file either in .h5 or .swc formats
        if bpy.context.scene.InputSource == enumerators.__input_h5_swc_file__:

            # Pass options from UI to system
            ui_interface.options.morphology.morphology_file_path = scene.MorphologyFile

            # Update the morphology label
            ui_interface.options.morphology.label = file_ops.get_file_name_from_path(
                scene.MorphologyFile)

            # Load the morphology from the file
            loading_flag, morphology_object = morphology_loader.load_from_file(
                options=ui_interface.options)

            # Verify the loading operation
            if loading_flag:

                # Update the morphology
                ui_interface.morphology = morphology_object

            # Otherwise, report an ERROR
            else:
                self.report({'ERROR'}, 'Invalid Morphology File')

        # Read the data from a specific gid in a given circuit
        elif bpy.context.scene.InputSource == enumerators.__input_circuit_gid__:

            # Pass options from UI to system
            ui_interface.options.morphology.blue_config = scene.CircuitFile
            ui_interface.options.morphology.gid = scene.Gid

            # Update the morphology label
            ui_interface.options.morphology.label = 'neuron_' + str(scene.Gid)

            # Load the morphology from the circuit
            loading_flag, morphology_object = morphology_loader.load_from_circuit(
                options=ui_interface.options)

            # Verify the loading operation
            if loading_flag:

                # Update the morphology
                ui_interface.morphology = morphology_object

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
            time_line.show_progress('Simulation', self.timer_limits, self.max_simulation_limit)

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
        self.meshy_soma_builder = soma_builder.SomaBuilder(
            ui_interface.morphology, ui_interface.options)

        # Build the basic profile of the some from the soft body operation, but don't run the
        # simulation now. Run the simulation in the '@modal' mode, to avoid freezing the UI
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
        global reconstructed_soma_mesh
        reconstructed_soma_mesh = self.soma_sphere_object

        # Show the progress, Done
        time_line.show_progress(
            'Simulation', self.timer_limits, self.max_simulation_limit, done=True)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Soma Reconstruction Done')


####################################################################################################
# @ReconstructSomaProfile
####################################################################################################
class ReconstructSomaProfile(bpy.types.Operator):
    """Soma profile reconstruction operator"""

    # Operator parameters
    bl_idname = "reconstruct.soma_profile"
    bl_label = "Profile"

    # Timer parameters
    event_timer = None
    timer_limits = bpy.props.IntProperty(default=0)

    # Meshy soma builder parameters
    meshy_soma_builder = None
    soma_sphere_object = None
    min_simulation_limit = nmv.consts.__min_simulation_frame__
    max_simulation_limit = nmv.consts.__max_simulation_frame__

    ################################################################################################
    # @load_morphology
    ################################################################################################
    def load_morphology(self, scene):
        """
        Loads the morphology from file.

        :param scene: Scene.
        """

        # Read the data from a given morphology file either in .h5 or .swc formats
        if bpy.context.scene.InputSource == enumerators.__input_h5_swc_file__:

            # Pass options from UI to system
            ui_interface.options.morphology.morphology_file_path = scene.MorphologyFile

            # Update the morphology label
            ui_interface.options.morphology.label = file_ops.get_file_name_from_path(
                scene.MorphologyFile)

            # Load the morphology from the file
            loading_flag, morphology_object = morphology_loader.load_from_file(
                options=ui_interface.options)

            # Verify the loading operation
            if loading_flag:

                # Update the morphology
                ui_interface.morphology = morphology_object

            # Otherwise, report an ERROR
            else:
                self.report({'ERROR'}, 'Invalid Morphology File')

        # Read the data from a specific gid in a given circuit
        elif bpy.context.scene.InputSource == enumerators.__input_circuit_gid__:

            # Pass options from UI to system
            ui_interface.options.morphology.blue_config = scene.CircuitFile
            ui_interface.options.morphology.gid = scene.Gid

            # Update the morphology label
            ui_interface.options.morphology.label = 'neuron_' + str(scene.Gid)

            # Load the morphology from the circuit
            loading_flag, morphology_object = morphology_loader.load_from_circuit(
                options=ui_interface.options)

            # Verify the loading operation
            if loading_flag:

                # Update the morphology
                ui_interface.morphology = morphology_object

            # Otherwise, report an ERROR
            else:
                self.report({'ERROR'}, 'Cannot Load Morphology from Circuit')

        else:
            # Report an invalid input source
            self.report({'ERROR'}, 'Invalid Input Source')

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self, context, event):
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
            time_line.show_progress('Simulation', self.timer_limits, self.max_simulation_limit)

            # Update the progress bar
            context.scene.SomaSimulationProgress = self.timer_limits

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """
        Execute the operator.

        :param context: Panel context.
        """

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology
        self.load_morphology(scene=context.scene)

        # Construct a soma builder
        self.meshy_soma_builder = soma_builder.SomaBuilder(
            ui_interface.morphology, ui_interface.options)

        # Build the basic profile of the some from the soft body operation, but don't run the
        # simulation now. Run the simulation in the '@modal' mode, to avoid freezing the UI
        self.soma_sphere_object = self.meshy_soma_builder.build_soma_based_on_profile_points_only()

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
        global reconstructed_soma_mesh
        reconstructed_soma_mesh = self.soma_sphere_object

        # Show the progress, Done
        time_line.show_progress(
            'Simulation', self.timer_limits, self.max_simulation_limit, done=True)

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

        # Get a reference to the scene
        scene = context.scene

        # Ensure that there is a valid directory where the images will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.images_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.images_directory)

        # Render the close up
        rendering_ops.render_close_up(
            image_name='%s_soma_mesh' % ui_interface.options.morphology.label,
            image_output_directory=ui_interface.options.output.images_directory,
            image_base_resolution=scene.SomaFrameResolution,
            camera_view='FRONT',
            close_up_dimension=scene.ViewDimensions)

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

        # Get a reference to the scene
        scene = context.scene

        # Ensure that there is a valid directory where the images will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.images_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.images_directory)

        # Render the close up
        rendering_ops.render_close_up(
            image_name='%s_soma_mesh' % ui_interface.options.morphology.label,
            image_output_directory=ui_interface.options.output.images_directory,
            image_base_resolution=scene.SomaFrameResolution, camera_view='SIDE',
            close_up_dimension=scene.ViewDimensions)

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

        # Get a reference to the scene
        scene = context.scene

        # Ensure that there is a valid directory where the images will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.images_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.images_directory)

        # Render the close up
        rendering_ops.render_close_up(
            image_name='%s_soma_mesh' % ui_interface.options.morphology.label,
            image_output_directory=ui_interface.options.output.images_directory,
            image_base_resolution=scene.SomaFrameResolution, camera_view='TOP',
            close_up_dimension=scene.ViewDimensions)

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

    # Camera parameters
    camera_360 = None

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

        # Get a reference to the scene
        scene = context.scene

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
            frame_name = '%s/frame_%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Render a frame
            global reconstructed_soma_mesh
            rendering_ops.render_frame_at_angle(scene_objects=[reconstructed_soma_mesh],
                camera=self.camera_360, angle=self.timer_limits, frame_name=frame_name)

            # Update the progress shell
            time_line.show_progress('Rendering', self.timer_limits, 360)

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

        # Get a reference to the scene
        scene = context.scene

        # Ensure that there is a valid directory where the images will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.sequences_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.sequences_directory)

        # Create the camera
        self.camera_360 = camera_ops.create_soma_close_up_camera(
            film_base_resolution=scene.SomaFrameResolution, close_up_dimension=scene.ViewDimensions)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_soma_mesh_360' % (
            ui_interface.options.output.sequences_directory, ui_interface.options.morphology.label)
        file_ops.clean_and_create_directory(self.output_directory)

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

        # Delete the camera
        nmv.scene.ops.delete_list_objects([self.camera_360])

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

    # Camera parameters
    camera_progressive = None

    # Output data
    output_directory = None

    # Morphology parameters
    morphology_object = None

    # Meshy soma builder parameters
    meshy_soma_builder = None
    soma_sphere_object = None
    min_simulation_limit = nmv.consts.__min_simulation_frame__
    max_simulation_limit = nmv.consts.__max_simulation_frame__

    ################################################################################################
    # @load_morphology
    ################################################################################################
    def load_morphology(self,
                        scene):
        """
        Loads the morphology from file.

        :param scene: Scene.
        """

        # Read the data from a given morphology file either in .h5 or .swc formats
        if bpy.context.scene.InputSource == enumerators.__input_h5_swc_file__:
            # Pass options from UI to system
            ui_interface.options.morphology.morphology_file_path = scene.MorphologyFile

            # Update the morphology label
            ui_interface.options.morphology.label = file_ops.get_file_name_from_path(
                scene.MorphologyFile)

            # Load the morphology from the file
            loading_flag, morphology_object = morphology_loader.load_from_file(
                options=ui_interface.options)

            # Verify the loading operation
            if loading_flag:
                # Update the morphology
                ui_interface.morphology = morphology_object

            # Otherwise, report an ERROR
            else:
                self.report({'ERROR'}, 'Invalid Morphology File')

        # Read the data from a specific gid in a given circuit
        elif bpy.context.scene.InputSource == enumerators.__input_circuit_gid__:
            # Pass options from UI to system
            ui_interface.options.morphology.blue_config = scene.CircuitFile
            ui_interface.options.morphology.gid = scene.Gid

            # Update the morphology label
            ui_interface.options.morphology.label = 'neuron_' + str(scene.Gid)

            # Load the morphology from the circuit
            loading_flag, morphology_object = morphology_loader.load_from_circuit(
                options=ui_interface.options)

            # Verify the loading operation
            if loading_flag:
                # Update the morphology
                ui_interface.morphology = morphology_object

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
            frame_name = '%s/frame_%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Render a frame
            rendering_ops.render_frame_at_angle(scene_objects=[self.soma_sphere_object],
                camera=self.camera_progressive, angle=0, frame_name=frame_name)

            # Update the progress shell
            time_line.show_progress('Rendering', self.timer_limits, self.max_simulation_limit)

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
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Get a reference to the scene
        scene = context.scene

        # Create the sequences directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.sequences_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.sequences_directory)

        # Setup a unified scale bounding box based on the close up dimension
        p_min = Vector((-scene.ViewDimensions, -scene.ViewDimensions, -scene.ViewDimensions))
        p_max = Vector((scene.ViewDimensions, scene.ViewDimensions, scene.ViewDimensions))

        # Create a symmetric bounding box that fits certain unified bounds for all the somata.
        unified_scale_bounding_box = bounding_box.BoundingBox(p_min=p_min, p_max=p_max)

        # Create the camera
        self.camera_progressive = camera_ops.create_camera(
            view_bounding_box=unified_scale_bounding_box,
            image_base_resolution=scene.SomaFrameResolution,
            camera_view='FRONT')

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_soma_mesh_progressive' % (
            ui_interface.options.output.sequences_directory, ui_interface.options.morphology.label)
        file_ops.clean_and_create_directory(self.output_directory)

        # Load the morphology
        self.load_morphology(scene=context.scene)

        # Create a some builder object
        self.meshy_soma_builder = soma_builder.SomaBuilder(
            ui_interface.morphology, ui_interface.options)

        # Build the basic profile of the some from the soft body operation, but don't run the
        # simulation now. Run the simulation in the '@modal' mode, to avoid freezing the UI
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
        global reconstructed_soma_mesh
        reconstructed_soma_mesh = self.soma_sphere_object

        # Show the progress, Done
        time_line.show_progress(
            'Rendering', self.timer_limits, self.max_simulation_limit, done=True)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Soma Rendering Done')

        # Delete the camera
        nmv.scene.ops.delete_list_objects([self.camera_progressive, self.soma_sphere_object])


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
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.meshes_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.meshes_directory)

        # Export the selected soma mesh as an .obj file
        global reconstructed_soma_mesh
        exporters.export_object_to_obj_file(
            mesh_object=reconstructed_soma_mesh,
            output_directory=ui_interface.options.output.meshes_directory,
            output_file_name='%s_soma' % ui_interface.morphology.label)

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
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.meshes_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.meshes_directory)

        # Export the selected soma mesh as an .ply file
        exporters.export_object_to_ply_file(
            mesh_object=reconstructed_soma_mesh,
            output_directory=ui_interface.options.output.meshes_directory,
            output_file_name='%s_soma' % ui_interface.morphology.label)

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
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.meshes_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.meshes_directory)

        # Export the selected soma mesh as an .stl file
        exporters.export_object_to_stl_file(
            mesh_object=reconstructed_soma_mesh,
            output_directory=ui_interface.options.output.meshes_directory,
            output_file_name='%s_soma' % ui_interface.morphology.label)

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
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.meshes_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.meshes_directory)

        # Export the selected soma mesh as an .blend file
        exporters.export_object_to_blend_file(
            mesh_object=reconstructed_soma_mesh,
            output_directory=ui_interface.options.output.meshes_directory,
            output_file_name='%s_soma' % ui_interface.morphology.label)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """
    Registers all the classes in this panel.
    """

    # Soma reconstruction panel
    bpy.utils.register_class(SoftBodyOptions)

    # Soma reconstruction operators
    bpy.utils.register_class(ReconstructSomaOperator)
    bpy.utils.register_class(ReconstructSomaProfile)

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
    bpy.utils.unregister_class(SoftBodyOptions)

    # Soma reconstruction
    bpy.utils.unregister_class(ReconstructSomaOperator)
    bpy.utils.unregister_class(ReconstructSomaProfile)

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
