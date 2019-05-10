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
from bpy.props import EnumProperty
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import BoolProperty
from bpy.props import FloatVectorProperty

# Internal imports
import nmv
import nmv.bbox
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.shading
import nmv.scene
import nmv.skeleton
import nmv.rendering
import nmv.utilities


####################################################################################################
# @MorphologyPanel
####################################################################################################
class MorphologyPanel(bpy.types.Panel):
    """Morphology tools panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Morphology Toolbox'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # Panel options
    ################################################################################################
    # Build soma
    bpy.types.Scene.BuildSoma = EnumProperty(
        items=[(nmv.enums.Soma.Representation.IGNORE,
                'Ignore',
                'Ignore soma reconstruction'),
               (nmv.enums.Soma.Representation.SPHERE,
                'Sphere',
                'Represent the soma by a sphere'),
               (nmv.enums.Soma.Representation.REALISTIC,
                'Profile',
                'Reconstruct a 3D profile of the soma')],
        name='Soma',
        default=nmv.enums.Soma.Representation.SPHERE)

    # Build axon
    bpy.types.Scene.BuildAxon = BoolProperty(
        name="Build Axon",
        description="Select this flag to reconstruct the axon",
        default=True)

    # Axon branching order
    # Since the axon is so complicated, we will set its default branching order to 5
    bpy.types.Scene.AxonBranchingLevel = IntProperty(
        name="Branching Order",
        description="Branching order for the axon",
        default=nmv.consts.Arbors.AXON_DEFAULT_BRANCHING_ORDER, min=1, max=100)

    # Build basal dendrites
    bpy.types.Scene.BuildBasalDendrites = BoolProperty(
        name="Build Basal Dendrites",
        description="Select this flag to reconstruct the basal dendrites",
        default=True)

    # Basal dendrites branching order
    bpy.types.Scene.BasalDendritesBranchingLevel = IntProperty(
        name="Branching Order",
        description="Branching order for the basal dendrites",
        default=nmv.consts.Arbors.MAX_BRANCHING_ORDER, min=1, max=100)

    # Build apical dendrite
    bpy.types.Scene.BuildApicalDendrite = BoolProperty(
        name="Build Apical Dendrites",
        description="Select this flag to reconstruct the apical dendrite (if exists)",
        default=True)

    # Apical dendrite branching order
    bpy.types.Scene.ApicalDendriteBranchingLevel = IntProperty(
        name="Branching Order",
        description="Branching order for the apical dendrite",
        default=nmv.consts.Arbors.MAX_BRANCHING_ORDER, min=1, max=100)

    # Display bounding box info
    bpy.types.Scene.DisplayBoundingBox = BoolProperty(
        name="Display Bounding Box Info",
        description="Displays the bounding box of the morphology",
        default=False)

    # Morphology material
    bpy.types.Scene.MorphologyMaterial = EnumProperty(
        items=nmv.enums.Shading.MATERIAL_ITEMS,
        name="Material",
        default=nmv.enums.Shading.LAMBERT_WARD)

    # Color arbor by part
    bpy.types.Scene.ColorArborByPart = BoolProperty(
        name="Color Arbor By Part",
        description="Each component of the arbor will be assigned a different color",
        default=False)

    # Color arbor using black and white alternatives
    bpy.types.Scene.ColorArborBlackAndWhite = BoolProperty(
        name="Black / White",
        description="Each component of the arbor will be assigned a either black or white",
        default=False)

    # Use single color for the all the objects in the morphology
    bpy.types.Scene.MorphologyHomogeneousColor = BoolProperty(
        name="Homogeneous Color",
        description="Use a single color for rendering all the objects of the morphology",
        default=False)

    # A homogeneous color for all the objects of the morphology
    bpy.types.Scene.NeuronMorphologyColor = FloatVectorProperty(
        name="Membrane Color",
        subtype='COLOR', default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
        description="The homogeneous color of the reconstructed morphology membrane")

    # Soma color
    bpy.types.Scene.SomaColor = FloatVectorProperty(
        name="Soma Color",
        subtype='COLOR', default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
        description="The color of the reconstructed soma")

    # Axon color
    bpy.types.Scene.AxonColor = FloatVectorProperty(
        name="Axon Color",
        subtype='COLOR', default=nmv.enums.Color.AXONS, min=0.0, max=1.0,
        description="The color of the reconstructed axon")

    # Basal dendrites color
    bpy.types.Scene.BasalDendritesColor = FloatVectorProperty(
        name="Basal Dendrites  Color",
        subtype='COLOR', default=nmv.enums.Color.BASAL_DENDRITES, min=0.0, max=1.0,
        description="The color of the reconstructed basal dendrites")

    # Apical dendrite color
    bpy.types.Scene.ApicalDendriteColor = FloatVectorProperty(
        name="Apical Dendrite Color",
        subtype='COLOR', default=nmv.enums.Color.APICAL_DENDRITES, min=0.0, max=1.0,
        description="The color of the reconstructed apical dendrite")

    # Articulation color
    bpy.types.Scene.ArticulationColor = FloatVectorProperty(
        name="Articulation Color",
        subtype='COLOR', default=nmv.enums.Color.ARTICULATION, min=0.0, max=1.0,
        description="The color of the articulations in the Articulated Section mode")

    # Reconstruction method
    bpy.types.Scene.MorphologyReconstructionTechnique = EnumProperty(
        items=[(nmv.enums.Skeletonization.Method.DISCONNECTED_SEGMENTS,
                'Disconnected Segments',
                "Each segment is an independent object (this approach is time consuming)"),
               (nmv.enums.Skeletonization.Method.DISCONNECTED_SECTIONS,
                'Disconnected Sections',
                "Each section is an independent object"),
               (nmv.enums.Skeletonization.Method.ARTICULATED_SECTIONS,
                'Articulated Sections',
                "Each section is an independent object, but connected with a pivot"),
               (nmv.enums.Skeletonization.Method.SAMPLES,
                'Samples',
                "Each sample is drawn as a sphere (this approach is very time consuming)"),
               (nmv.enums.Skeletonization.Method.CONNECTED_SECTION_ORIGINAL,
                'Connected Sections (Original)',
                "The sections of a single arbor are connected together"),
               (nmv.enums.Skeletonization.Method.CONNECTED_SECTION_REPAIRED,
                'Connected Sections (Repaired)',
                "The morphology is repaired and fully reconstructed ")],
        name="Method",
        default=nmv.enums.Skeletonization.Method.DISCONNECTED_SECTIONS)

    # Arbors style
    bpy.types.Scene.ArborsStyle = EnumProperty(
        items=nmv.enums.Arbors.Style.MORPHOLOGY_STYLE_ITEMS,
        name="Skeleton Style",
        default=nmv.enums.Arbors.Style.ORIGINAL)

    # Branching, is it based on angles or radii
    bpy.types.Scene.MorphologyBranching = EnumProperty(
        items=[(nmv.enums.Skeletonization.Branching.ANGLES,
                'Angles',
                'Make the branching based on the angles at branching points'),
               (nmv.enums.Skeletonization.Branching.RADII,
                'Radii',
                'Make the branching based on the radii of the children at the branching points')],
        name='Branching Style',
        default=nmv.enums.Skeletonization.Branching.ANGLES)

    # Soma connection to roots
    bpy.types.Scene.SomaConnectionToRoot = EnumProperty(
        items=[(nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN,
                'Connect Connected',
                'Connect the arbors that are physically connected to the origin of the soma'),
               (nmv.enums.Arbors.Roots.ALL_CONNECTED_TO_ORIGIN,
                'All Connected',
                'Connect the all the arbors to the origin of the soma even if they intersect'),
               (nmv.enums.Arbors.Roots.DISCONNECTED_FROM_SOMA,
                'All Disconnected',
                'Disconnect all the arbors from the soma')],
        name='Arbors To Soma',
        default=nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN)

    # Arbor quality
    bpy.types.Scene.ArborQuality = IntProperty(
        name="Sides",
        description="Number of vertices of the cross-section of each segment along the arbor",
        default=16, min=4, max=128)

    # Section radius
    bpy.types.Scene.SectionsRadii = EnumProperty(
        items=[(nmv.enums.Skeletonization.ArborsRadii.AS_SPECIFIED,
                'As Specified in Morphology',
                "Use the cross-sectional radii reported in the morphology file"),
               (nmv.enums.Skeletonization.ArborsRadii.FIXED,
                'At a Fixed Diameter',
                "Set all the arbors to a fixed radius"),
               (nmv.enums.Skeletonization.ArborsRadii.SCALED,
                'With Scale Factor',
                "Scale all the arbors using a specified scale factor"),
               (nmv.enums.Skeletonization.ArborsRadii.FILTERED,
                'Filtered',
                "Filter section with lower values than the threshold"), ],
        name="Sections Radii",
        default=nmv.enums.Skeletonization.ArborsRadii.AS_SPECIFIED)

    # Fixed section radius value
    bpy.types.Scene.FixedRadiusValue = FloatProperty(
        name="Value (micron)",
        description="The value of the radius in microns between (0.05 and 5.0) microns",
        default=1.0, min=0.05, max=5.0)

    # Threshold value for the radius
    bpy.types.Scene.FilteredRadiusThreshold = FloatProperty(
        name="Threshold",
        description="The value of the threshold radius in microns between (0.005 and 5.0) microns",
        default=1.0, min=0.005, max=5.0)

    # Global radius scale value
    bpy.types.Scene.RadiusScaleValue= FloatProperty(
        name="Scale",
        description="A scale factor for scaling the radii of the arbors between (0.01 and 5.0)",
        default=1.0, min=0.01, max=5.0)

    # Rendering type
    bpy.types.Scene.RenderingType = EnumProperty(
        items=[(nmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION,
                'Fixed Resolution',
                'Renders a full view of the morphology at a specified resolution'),
               (nmv.enums.Skeletonization.Rendering.Resolution.TO_SCALE,
                'To Scale',
                'Renders an image of the full view at the right scale in (um)')],
        name='Type',
        default=nmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION)

    # Rendering view
    bpy.types.Scene.MorphologyRenderingView = EnumProperty(
        items=[(nmv.enums.Skeletonization.Rendering.View.WIDE_SHOT_VIEW,
                'Wide Shot',
                'Renders an image of the full view'),
               (nmv.enums.Skeletonization.Rendering.View.MID_SHOT_VIEW,
                'Mid Shot',
                'Renders an image of the reconstructed arbors only'),
               (nmv.enums.Skeletonization.Rendering.View.CLOSE_UP_VIEW,
                'Close Up',
                'Renders a close up image the focuses on the soma')],
        name='View',
        default=nmv.enums.Skeletonization.Rendering.View.MID_SHOT_VIEW)

    # Frame resolution
    bpy.types.Scene.MorphologyFrameResolution = IntProperty(
        name="Resolution",
        default=512, min=128, max=1024 * 10,
        description="The resolution of the image generated from rendering the morphology")

    # Frame scale factor 'for rendering to scale option '
    bpy.types.Scene.MorphologyFrameScaleFactor = FloatProperty(
        name="Scale",
        default=1.0, min=1.0, max=100.0,
        description="The scale factor for rendering a morphology to scale")

    # Morphology close up dimensions
    bpy.types.Scene.MorphologyCloseUpDimensions = FloatProperty(
        name="Dimensions",
        default=20, min=5, max=100,
        description="The dimensions of the view that will be rendered in microns")

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """Draw the panel.

        :param context:
            Panel context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Get a reference to the scene
        current_scene = context.scene

        # Set the skeleton options
        nmv.interface.ui.morphology_panel_options.set_skeleton_options(
            layout=layout, scene=current_scene, options=nmv.interface.ui_options)

        # Set the reconstruction options
        nmv.interface.ui.morphology_panel_options.set_reconstruction_options(
            layout=layout, scene=current_scene, options=nmv.interface.ui_options)

        # Set the color options
        nmv.interface.ui.morphology_panel_options.set_color_options(
            layout=layout, scene=current_scene, options=nmv.interface.ui_options)

        # Reconstruction button
        quick_reconstruction_row = layout.row()
        quick_reconstruction_row.label(text='Quick Reconstruction:', icon='PARTICLE_POINT')
        reconstruct_morphology_button_row = layout.row()
        reconstruct_morphology_button_row.operator('reconstruct.morphology', icon='RNA_ADD')
        reconstruct_morphology_button_row.enabled = True

        # Set the rendering options
        nmv.interface.ui.morphology_panel_options.set_rendering_options(
            layout=layout, scene=current_scene, options=nmv.interface.ui_options)

        # Set the rendering options
        nmv.interface.ui.morphology_panel_options.set_export_options(
            layout=layout, scene=current_scene, options=nmv.interface.ui_options)

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(layout)


####################################################################################################
# ReconstructMorphologyOperator
####################################################################################################
class ReconstructMorphologyOperator(bpy.types.Operator):
    """Morphology reconstruction operator"""

    # Operator parameters
    bl_idname = "reconstruct.morphology"
    bl_label = "Reconstruct Morphology"

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

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a valid morphology file')
            return {'FINISHED'}

        # Create a skeletonizer object to build the morphology skeleton
        builder = nmv.builders.SkeletonBuilder(
            nmv.interface.ui_morphology, nmv.interface.ui_options)

        # Draw the morphology skeleton and return a list of all the reconstructed objects
        nmv.interface.ui_reconstructed_skeleton = builder.draw_morphology_skeleton()

        # View all the objects in the scene
        # nmv.scene.ops.view_all_scene()

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphologyFront
####################################################################################################
class RenderMorphologyFront(bpy.types.Operator):
    """Render front view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "render_morphology.front"
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

        # Render the image
        nmv.interface.ui.render_morphology_image(self, context.scene, nmv.enums.Camera.View.FRONT)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphologySide
####################################################################################################
class RenderMorphologySide(bpy.types.Operator):
    """Render side view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "render_morphology.side"
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

        # Render the image
        nmv.interface.ui.render_morphology_image(self, context.scene, nmv.enums.Camera.View.SIDE)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphologyTop
####################################################################################################
class RenderMorphologyTop(bpy.types.Operator):
    """Render top view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "render_morphology.top"
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

        # Render the image
        nmv.interface.ui.render_morphology_image(self, context.scene, nmv.enums.Camera.View.TOP)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphology360
####################################################################################################
class RenderMorphology360(bpy.types.Operator):
    """Render a 360 view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "render_morphology.360"
    bl_label = "360"

    # Timer parameters
    event_timer = None
    timer_limits = bpy.props.IntProperty(default=0)

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

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel context
            self.cancel(context)

            # Done
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Set the frame name
            image_name = '%s/frame_%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Compute the bounding box for a close up view
            if context.scene.MorphologyRenderingView == \
                    nmv.enums.Skeletonization.Rendering.View.CLOSE_UP_VIEW:

                # Compute the bounding box for a close up view
                rendering_bbox = nmv.bbox.compute_unified_extent_bounding_box(
                    extent=context.scene.MorphologyCloseUpDimensions)

            # Compute the bounding box for a mid-shot view
            elif context.scene.MorphologyRenderingView == \
                    nmv.enums.Skeletonization.Rendering.View.MID_SHOT_VIEW:

                # Compute the bounding box for the available meshes only
                rendering_bbox = nmv.bbox.compute_scene_bounding_box_for_curves()

            # Compute the bounding box for the wide-shot view that corresponds to the whole
            # morphology
            else:

                # Compute the full morphology bounding box
                rendering_bbox = nmv.skeleton.compute_full_morphology_bounding_box(
                    morphology=nmv.interface.ui_morphology)

            # Compute a 360 bounding box to fit the arbors
            bounding_box_360 = nmv.bbox.compute_360_bounding_box(rendering_bbox,
                nmv.interface.ui_morphology.soma.centroid)

            # Stretch the bounding box by few microns
            bounding_box_360.extend_bbox(delta=nmv.consts.Image.GAP_DELTA)

            # Render a frame
            nmv.rendering.renderer.render_at_angle(
                scene_objects=nmv.interface.ui_reconstructed_skeleton,
                angle=self.timer_limits,
                bounding_box=bounding_box_360,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=context.scene.MorphologyFrameResolution,
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
    def execute(self, context):
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
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.sequences_directory)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_morphology_360' % \
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
        self.report({'INFO'}, 'Morphology Rendering Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphologyProgressive
####################################################################################################
class RenderMorphologyProgressive(bpy.types.Operator):
    """Render a progressive sequence of the reconstruction procedure (time-consuming)"""

    # Operator parameters
    bl_idname = "render_morphology.progressive"
    bl_label = "Progressive"

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
        if nmv.interface.ui_options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not file_ops.path_exists(nmv.interface.ui_options.output.sequences_directory):
            file_ops.clean_and_create_directory(nmv.interface.ui_options.output.sequences_directory)

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # NOTE: To render a progressive reconstruction sequence, this requires setting the
        # morphology progressive rendering flag to True and then passing the nmv.interface.ui_options
        # to the morphology builder and disabling it after the rendering
        nmv.interface.ui_options.morphology.render_progressive = True

        # Create a skeleton builder object
        morphology_builder = skeleton_builder.SkeletonBuilder(
            ui_interface.morphology, nmv.interface.ui_options)

        # Reconstruct the morphology
        morphology_skeleton_objects = morphology_builder.draw_morphology_skeleton()

        # Setting the progressive rendering flag to False (default value)
        nmv.interface.ui_options.morphology.render_progressive = False

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
    bl_idname = "save_morphology.swc"
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

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.morphologies_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.morphologies_directory)

        # Export the reconstructed morphology as an .blend file
        # NOTE: Since we don't have meshes, then the mesh_object argument will be set to None and
        # the exported blender file will contain all the morphology objects.
        nmv.file.write_morphology_to_swc_file(
            nmv.interface.ui_morphology, nmv.interface.ui_options.io.morphologies_directory)

        return {'FINISHED'}


####################################################################################################
# @SaveMorphologySegments
####################################################################################################
class SaveMorphologySegments(bpy.types.Operator):
    """Save the reconstructed morphology as a list of segments into file"""

    # Operator parameters
    bl_idname = "save_morphology.segments"
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

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.morphologies_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.morphologies_directory)

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
    bl_idname = "save_morphology.blend"
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

        if not nmv.file.ops.file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.morphologies_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.morphologies_directory)

        # Export the reconstructed morphology as an .blend file
        # NOTE: Since we don't have meshes, then the mesh_object argument will be set to None and
        # the exported blender file will contain all the morphology objects.
        nmv.file.export_object_to_blend_file(
            mesh_object=None,
            output_directory=nmv.interface.ui_options.io.morphologies_directory,
            output_file_name=nmv.interface.ui_morphology.label)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Soma reconstruction panel
    bpy.utils.register_class(MorphologyPanel)

    # Soma reconstruction operator
    bpy.utils.register_class(ReconstructMorphologyOperator)

    # Morphology rendering
    bpy.utils.register_class(RenderMorphologyFront)
    bpy.utils.register_class(RenderMorphologySide)
    bpy.utils.register_class(RenderMorphologyTop)
    bpy.utils.register_class(RenderMorphology360)
    bpy.utils.register_class(RenderMorphologyProgressive)

    # Saving morphology
    bpy.utils.register_class(SaveMorphologyBLEND)
    bpy.utils.register_class(SaveMorphologySWC)
    bpy.utils.register_class(SaveMorphologySegments)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Morphology reconstruction panel
    bpy.utils.unregister_class(MorphologyPanel)

    # Morphology reconstruction operator
    bpy.utils.unregister_class(ReconstructMorphologyOperator)

    # Morphology rendering
    bpy.utils.unregister_class(RenderMorphologyTop)
    bpy.utils.unregister_class(RenderMorphologySide)
    bpy.utils.unregister_class(RenderMorphologyFront)
    bpy.utils.unregister_class(RenderMorphology360)
    bpy.utils.unregister_class(RenderMorphologyProgressive)

    # Saving morphology
    bpy.utils.unregister_class(SaveMorphologyBLEND)
    bpy.utils.unregister_class(SaveMorphologySWC)
    bpy.utils.unregister_class(SaveMorphologySegments)

