####################################################################################################
# Copyright (c) 2016 - 2021, EPFL / Blue Brain Project
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
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.shading
import nmv.scene
import nmv.skeleton
import nmv.utilities
import nmv.rendering
import nmv.geometry
from .morphology_panel_options import *

# Is the morphology reconstructed or not
is_morphology_reconstructed = False

# Is the morphology rendered or not
is_morphology_rendered = False

# What is the selected morphology builder
morphology_builder = None


####################################################################################################
# @MorphologyPanel
####################################################################################################
class MorphologyPanel(bpy.types.Panel):
    """Morphology tools panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if nmv.utilities.is_blender_280() else 'TOOLS'
    bl_idname = "OBJECT_PT_NMV_MorphologyToolBox"
    bl_label = 'Morphology Toolbox'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @update_ui_colors
    ################################################################################################
    def update_ui_colors(self, context):

        # Get a list of initial colors from the selected colormap
        colors = nmv.utilities.create_colormap_from_hex_list(
            nmv.enums.ColorMaps.get_hex_color_list(context.scene.NMV_ColorMap),
            nmv.consts.Color.COLORMAP_RESOLUTION)

        # Invert the colormap
        if context.scene.NMV_InvertColorMap:
            colors.reverse()

        # Update the colormap in the UI
        for color_index in range(nmv.consts.Color.COLORMAP_RESOLUTION):
            setattr(context.scene, 'NMV_Color%d' % color_index, colors[color_index])

    # A list of all the color maps available in NeuroMorphoVis
    # Note that once a new colormap is selected, the corresponding colors will be set in the UI
    bpy.types.Scene.NMV_ColorMap = bpy.props.EnumProperty(
        items=nmv.enums.ColorMaps.COLOR_MAPS,
        name='',
        default=nmv.enums.ColorMaps.GNU_PLOT,
        update=update_ui_colors)

    bpy.types.Scene.NMV_InvertColorMap = bpy.props.BoolProperty(
        name='Invert',
        description='Invert the selected colormap',
        default=False,
        update=update_ui_colors)

    # Create a list of colors from the selected colormap
    colors = nmv.utilities.create_colormap_from_hex_list(
        nmv.enums.ColorMaps.get_hex_color_list(bpy.types.Scene.NMV_ColorMap),
        nmv.consts.Color.COLORMAP_RESOLUTION)

    # Update the UI color elements from the color map list
    for index in range(nmv.consts.Color.COLORMAP_RESOLUTION):
        setattr(bpy.types.Scene, 'NMV_Color%d' % index, bpy.props.FloatVectorProperty(
            name='', subtype='COLOR', default=colors[index], min=0.0, max=1.0, description=''))

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel.

        :param context:
            Panel context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Get a reference to the scene
        current_scene = context.scene

        # Documentation button
        documentation_button = layout.column()
        documentation_button.operator('nmv.documentation_morphology', icon='URL')
        documentation_button.separator()

        # Set the reconstruction options
        nmv.interface.ui.morphology_panel_ops.set_reconstruction_options(
            layout=layout, scene=current_scene, options=nmv.interface.ui_options)

        # Set the skeleton options
        nmv.interface.ui.morphology_panel_ops.set_skeleton_options(
            layout=layout, scene=current_scene, options=nmv.interface.ui_options)

        # Set the color options
        nmv.interface.ui.morphology_panel_ops.add_color_options(
            layout=layout, scene=current_scene, options=nmv.interface.ui_options)

        # Reconstruction button
        quick_reconstruction_row = layout.row()
        quick_reconstruction_row.label(text='Quick Reconstruction:', icon='PARTICLE_POINT')
        reconstruct_morphology_button_row = layout.row()
        reconstruct_morphology_button_row.operator('nmv.reconstruct_morphology',
                                                   text=bpy.types.Scene.NMV_MorphologyButtonLabel,
                                                   icon='RNA_ADD')
        reconstruct_morphology_button_row.enabled = True

        global is_morphology_reconstructed
        if is_morphology_reconstructed:
            morphology_stats_row = layout.row()
            morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')
            reconstruction_time_row = layout.row()
            reconstruction_time_row.prop(context.scene, 'NMV_MorphologyReconstructionTime')
            reconstruction_time_row.enabled = False

        # Set the rendering options
        nmv.interface.ui.morphology_panel_ops.set_rendering_options(
            layout=layout, scene=current_scene, options=nmv.interface.ui_options)

        global is_morphology_rendered
        if is_morphology_rendered:
            morphology_stats_row = layout.row()
            morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')
            rendering_time_row = layout.row()
            rendering_time_row.prop(context.scene, 'NMV_MorphologyRenderingTime')
            rendering_time_row.enabled = False

        # Set the rendering options
        nmv.interface.ui.morphology_panel_ops.set_export_options(
            layout=layout, scene=current_scene, options=nmv.interface.ui_options)

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(layout)


####################################################################################################
# ReconstructMorphologyOperator
####################################################################################################
class ReconstructMorphologyOperator(bpy.types.Operator):
    """Morphology reconstruction operator"""

    # Operator parameters
    bl_idname = "nmv.reconstruct_morphology"
    bl_label = bpy.types.Scene.NMV_MorphologyButtonLabel

    ################################################################################################
    # @load_morphology
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Context.
        :return:
            'FINISHED'
        """

        # Reset the scene
        nmv.scene.reset_scene()

        # Clear the scene
        nmv.scene.clear_scene()

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a valid morphology file')
            return {'FINISHED'}

        # Start reconstruction
        start_time = time.time()

        global morphology_builder
        # Create a skeleton builder object to build the morphology skeleton
        method = nmv.interface.ui_options.morphology.reconstruction_method
        if method == nmv.enums.Skeleton.Method.DISCONNECTED_SEGMENTS:
            morphology_builder = nmv.builders.DisconnectedSegmentsBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Draw the morphology as a set of disconnected tubes, where each SECTION is a tube
        elif method == nmv.enums.Skeleton.Method.DISCONNECTED_SECTIONS or \
                method == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
            morphology_builder = nmv.builders.DisconnectedSectionsBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Draw the morphology as a set of spheres, where each SPHERE represents a sample
        elif method == nmv.enums.Skeleton.Method.SAMPLES:
            morphology_builder = nmv.builders.SamplesBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        elif method == nmv.enums.Skeleton.Method.CONNECTED_SECTIONS:
            morphology_builder = nmv.builders.ConnectedSectionsBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        elif method == nmv.enums.Skeleton.Method.PROGRESSIVE:
            morphology_builder = nmv.builders.ProgressiveBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        elif method == nmv.enums.Skeleton.Method.DENDROGRAM:
            morphology_builder = nmv.builders.DendrogramBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Default: DisconnectedSectionsBuilder
        else:
            morphology_builder = nmv.builders.DisconnectedSectionsBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Draw the morphology skeleton and return a list of all the reconstructed objects
        nmv.interface.ui_reconstructed_skeleton = morphology_builder.draw_morphology_skeleton(
            context=context)

        # Interpolations
        scale = float(context.scene.NMV_MaximumValue) - float(context.scene.NMV_MinimumValue)
        delta = scale / float(nmv.consts.Color.COLORMAP_RESOLUTION)

        # Fill the list of colors
        for color_index in range(nmv.consts.Color.COLORMAP_RESOLUTION):
            r0_value = float(context.scene.NMV_MinimumValue) + (color_index * delta)
            r1_value = float(context.scene.NMV_MinimumValue) + ((color_index + 1) * delta)
            setattr(context.scene, 'NMV_R0_Value%d' % color_index, r0_value)
            setattr(context.scene, 'NMV_R1_Value%d' % color_index, r1_value)

        # Morphology reconstructed
        reconstruction_time = time.time()
        global is_morphology_reconstructed
        is_morphology_reconstructed = True
        context.scene.NMV_MorphologyReconstructionTime = reconstruction_time - start_time
        nmv.logger.statistics('Morphology reconstructed in [%f] seconds' %
                              context.scene.NMV_MorphologyReconstructionTime)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphologyFront
####################################################################################################
class RenderMorphologyFront(bpy.types.Operator):
    """Render front view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_front"
    bl_label = "Front"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Rendering Context.
        :return:
            'FINISHED'.
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_morphology_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.FRONT,
            image_format=nmv.interface.ui_options.morphology.image_format)

        # Stats.
        rendering_time = time.time()
        global is_morphology_rendered
        is_morphology_rendered = True
        context.scene.NMV_MorphologyRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MorphologyRenderingTime)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphologySide
####################################################################################################
class RenderMorphologySide(bpy.types.Operator):
    """Render side view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_side"
    bl_label = "Side"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator.

        :param context:
            Rendering context.
        :return:
            'FINISHED'.
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_morphology_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.SIDE,
            image_format=nmv.interface.ui_options.morphology.image_format)

        # Stats.
        rendering_time = time.time()
        global is_morphology_rendered
        is_morphology_rendered = True
        context.scene.NMV_MorphologyRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MorphologyRenderingTime)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphologyTop
####################################################################################################
class RenderMorphologyTop(bpy.types.Operator):
    """Render top view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_top"
    bl_label = "Top"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator.

        :param context:
            Rendering context.
        :return:
            'FINISHED'.
        """
        
        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_morphology_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.TOP,
            image_format=nmv.interface.ui_options.morphology.image_format)

        # Stats.
        rendering_time = time.time()
        global is_morphology_rendered
        is_morphology_rendered = True
        context.scene.NMV_MorphologyRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MorphologyRenderingTime)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphology360
####################################################################################################
class RenderMorphology360(bpy.types.Operator):
    """Render a 360 view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_360"
    bl_label = "360"

    # Timer parameters
    event_timer = None
    timer_limits = 0
    start_time = 0

    # Output data
    output_directory = None

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
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > 360:

            # Reset the orientation of the mesh
            nmv.scene.reset_orientation_of_objects(
                scene_objects=nmv.interface.ui_reconstructed_skeleton)

            # Stats.
            rendering_time = time.time()
            global is_morphology_rendered
            is_morphology_rendered = True
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

            # Set the frame name
            image_name = '%s/%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Compute the bounding box for a close up view
            if context.scene.NMV_MorphologyRenderingView == \
                    nmv.enums.Rendering.View.CLOSE_UP:

                # Compute the bounding box for a close up view
                rendering_bbox = nmv.bbox.compute_unified_extent_bounding_box(
                    extent=context.scene.NMV_MorphologyCloseUpDimensions)

            # Compute the bounding box for a mid-shot view
            elif context.scene.NMV_MorphologyRenderingView == \
                    nmv.enums.Rendering.View.MID_SHOT:

                # Compute the bounding box for the available meshes only
                rendering_bbox = nmv.bbox.compute_scene_bounding_box_for_curves()

            # Compute the bounding box for the wide-shot view that corresponds to the whole
            # morphology
            else:

                # Compute the full morphology bounding box
                rendering_bbox = nmv.skeleton.compute_full_morphology_bounding_box(
                    morphology=nmv.interface.ui_morphology)

            # Compute a 360 bounding box to fit the arbors
            bounding_box_360 = nmv.bbox.compute_360_bounding_box(
                rendering_bbox, nmv.interface.ui_morphology.soma.centroid)

            # Stretch the bounding box by few microns
            bounding_box_360.extend_bbox_uniformly(delta=nmv.consts.Image.GAP_DELTA)

            # Render a frame
            nmv.rendering.renderer.render_at_angle(
                scene_objects=nmv.interface.ui_reconstructed_skeleton,
                angle=self.timer_limits,
                bounding_box=bounding_box_360,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=context.scene.NMV_MorphologyFrameResolution,
                image_name=image_name)

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
        """
        Execute the operator.

        :param context: Panel context.
        """

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


####################################################################################################
# @RenderMorphologyProgressive
####################################################################################################
class RenderMorphologyProgressive(bpy.types.Operator):
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
            global is_morphology_rendered
            is_morphology_rendered = True
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

            # Render a frame
            nmv.rendering.renderer.render(
                bounding_box=self.morphology_bounding_box,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=context.scene.NMV_MorphologyFrameResolution,
                image_name=image_name,
                image_directory=self.output_directory)

            # Update the progress shell
            nmv.utilities.show_progress('Rendering', self.timer_limits, bpy.context.scene.frame_end)

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
        if view == nmv.enums.Rendering.View.CLOSE_UP:
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


####################################################################################################
# @SaveMorphologySWC
####################################################################################################
class SaveMorphologySWC(bpy.types.Operator):
    """Save the reconstructed morphology in an SWC file"""

    # Operator parameters
    bl_idname = "nmv.save_morphology_swc"
    bl_label = "SWC (.swc)"

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

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.morphologies_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.morphologies_directory)

        # Export the reconstructed morphology as an .blend file
        # NOTE: Since we don't have meshes, then the mesh_object argument will be set to None and
        # the exported blender file will contain all the morphology objects.
        global morphology_builder
        nmv.file.write_morphology_to_swc_file(
            morphology_builder.morphology, nmv.interface.ui_options.io.morphologies_directory)

        return {'FINISHED'}


####################################################################################################
# @SaveMorphologySegments
####################################################################################################
class SaveMorphologySegments(bpy.types.Operator):
    """Save the reconstructed morphology as a list of segments into file"""

    # Operator parameters
    bl_idname = "nmv.save_morphology_segments"
    bl_label = "Segments (.segments)"

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

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.morphologies_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.morphologies_directory)

        # Export the reconstructed morphology as an .blend file
        # NOTE: Since we don't have meshes, then the mesh_object argument will be set to None and
        # the exported blender file will contain all the morphology objects.
        nmv.file.write_morphology_to_segments_file(
            nmv.interface.ui_morphology, nmv.interface.ui_options.io.morphologies_directory)

        return {'FINISHED'}


####################################################################################################
# @SaveMorphologyBLEND
####################################################################################################
class SaveMorphologyBLEND(bpy.types.Operator):
    """Save the reconstructed morphology in a blender file"""

    # Operator parameters
    bl_idname = "nmv.save_morphology_blend"
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

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.morphologies_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.morphologies_directory)

        # Export the reconstructed morphology as an .blend file
        # NOTE: Since we don't have meshes, then the mesh_object argument will be set to None and
        # the exported blender file will contain all the morphology objects.
        nmv.file.export_scene_to_blend_file(
            output_directory=nmv.interface.ui_options.io.morphologies_directory,
            output_file_name=nmv.interface.ui_morphology.label)

        return {'FINISHED'}


####################################################################################################
# @MorphologyReconstructionDocumentation
####################################################################################################
class MorphologyReconstructionDocumentation(bpy.types.Operator):
    """Open the online documentation page of the Morphology Reconstruction panel."""

    # Operator parameters
    bl_idname = "nmv.documentation_morphology"
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
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis/wiki/Morphology-Reconstruction')
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # ColorMap
    # bpy.utils.register_class(ColorMapOperator)

    # Soma reconstruction panel
    bpy.utils.register_class(MorphologyPanel)

    # Buttons
    bpy.utils.register_class(MorphologyReconstructionDocumentation)
    bpy.utils.register_class(ReconstructMorphologyOperator)
    bpy.utils.register_class(RenderMorphologyFront)
    bpy.utils.register_class(RenderMorphologySide)
    bpy.utils.register_class(RenderMorphologyTop)
    bpy.utils.register_class(RenderMorphology360)
    bpy.utils.register_class(RenderMorphologyProgressive)
    bpy.utils.register_class(SaveMorphologyBLEND)
    bpy.utils.register_class(SaveMorphologySWC)
    bpy.utils.register_class(SaveMorphologySegments)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # ColorMap
    # bpy.utils.unregister_class(ColorMapOperator)

    # Morphology reconstruction panel
    bpy.utils.unregister_class(MorphologyPanel)

    # Buttons
    bpy.utils.unregister_class(MorphologyReconstructionDocumentation)
    bpy.utils.unregister_class(ReconstructMorphologyOperator)
    bpy.utils.unregister_class(RenderMorphologyTop)
    bpy.utils.unregister_class(RenderMorphologySide)
    bpy.utils.unregister_class(RenderMorphologyFront)
    bpy.utils.unregister_class(RenderMorphology360)
    bpy.utils.unregister_class(RenderMorphologyProgressive)
    bpy.utils.unregister_class(SaveMorphologyBLEND)
    bpy.utils.unregister_class(SaveMorphologySWC)
    bpy.utils.unregister_class(SaveMorphologySegments)

