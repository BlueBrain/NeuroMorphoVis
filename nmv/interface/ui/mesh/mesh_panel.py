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

from .mesh_panel_options import *
from .mesh_panel_ops import *

# Is the mesh reconstructed or not
is_mesh_reconstructed = False

# Is the mesh rendered or not
is_mesh_rendered = False


####################################################################################################
# @NMV_MeshPanel
####################################################################################################
class NMV_MeshPanel(bpy.types.Panel):
    """MeshPanel class"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_idname = "OBJECT_PT_NMV_MeshingToolBox"
    bl_label = 'Meshing Toolbox'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @draw
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Shown / Hidden rows
        # A list of rows that will be activated or deactivated based on availability of the mesh
        self.shown_hidden_rows = list()

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel

        :param context:
            Rendering context.
        """

        # Documentation button
        documentation_button = self.layout.column()
        documentation_button.operator('nmv.documentation_mesh', icon='URL')
        documentation_button.separator()

        # Meshing options
        draw_meshing_options(panel=self, scene=context.scene)

        # Color options
        draw_color_options(panel=self, scene=context.scene)

        # Mesh reconstruction button
        draw_mesh_reconstruction_button(panel=self, scene=context.scene)

        # Profiling
        if is_mesh_reconstructed:
            morphology_stats_row = self.layout.row()
            morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')
            reconstruction_time_row = self.layout.row()
            reconstruction_time_row.prop(context.scene, 'NMV_MeshReconstructionTime')
            reconstruction_time_row.enabled = False

        # Rendering options
        draw_rendering_options(panel=self, scene=context.scene)

        global is_mesh_rendered
        if is_mesh_rendered:
            morphology_stats_row = self.layout.row()
            morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')
            rendering_time_row = self.layout.row()
            rendering_time_row.prop(context.scene, 'NMV_MeshRenderingTime')
            rendering_time_row.enabled = False

        # Mesh export options
        draw_mesh_export_options(panel=self, scene=context.scene)

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(self.layout)


####################################################################################################
# @NMV_ReconstructNeuronMesh
####################################################################################################
class NMV_ReconstructNeuronMesh(bpy.types.Operator):
    """Reconstructs the mesh of the neuron"""

    # Operator parameters
    bl_idname = "nmv.reconstruct_neuron_mesh"
    bl_label = "Reconstruct Mesh"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Executes the operator

        Keyword arguments:
        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        import time

        # Reset the scene
        nmv.scene.reset_scene()

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Meshing technique
        meshing_technique = nmv.interface.ui.globals.options.mesh.meshing_technique

        # Start reconstruction
        start_time = time.time()

        # Piece-wise watertight meshing
        if meshing_technique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
            mesh_builder = nmv.builders.PiecewiseBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui.globals.options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Union
        elif meshing_technique == nmv.enums.Meshing.Technique.UNION:
            mesh_builder = nmv.builders.UnionBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui.globals.options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Skinning
        elif meshing_technique == nmv.enums.Meshing.Technique.SKINNING:
            mesh_builder = nmv.builders.SkinningBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui.globals.options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Meta Balls
        elif meshing_technique == nmv.enums.Meshing.Technique.META_OBJECTS:
            mesh_builder = nmv.builders.MetaBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui.globals.options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        else:

            # Invalid method
            self.report({'ERROR'}, 'Invalid Meshing Technique')
            return {'FINISHED'}

        # Mesh reconstructed
        reconstruction_time = time.time()
        global is_mesh_reconstructed
        is_mesh_reconstructed = True
        context.scene.NMV_MeshReconstructionTime = reconstruction_time - start_time
        nmv.logger.statistics('Mesh reconstructed in [%f] seconds' %
                              context.scene.NMV_MeshReconstructionTime)

        return {'FINISHED'}


####################################################################################################
# @NMV_RenderMeshFront
####################################################################################################
class NMV_RenderMeshFront(bpy.types.Operator):
    """Render front view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.render_mesh_front"
    bl_label = "Front"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator

        :param context:
            Rendering Context.
        :return:
            'FINISHED'
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_mesh_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.FRONT,
            image_format=nmv.interface.ui.globals.options.mesh.image_format)

        # Stats.
        rendering_time = time.time()
        global is_mesh_rendered
        is_mesh_rendered = True
        context.scene.NMV_MeshRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MeshRenderingTime)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderMeshSide
####################################################################################################
class NMV_RenderMeshSide(bpy.types.Operator):
    """Render side view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.render_mesh_side"
    bl_label = "Side"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator

        :param context:
            Rendering context.
        :return:
            'FINISHED'
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_mesh_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.SIDE,
            image_format=nmv.interface.ui.globals.options.mesh.image_format)

        # Stats.
        rendering_time = time.time()
        global is_mesh_rendered
        is_mesh_rendered = True
        context.scene.NMV_MeshRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MeshRenderingTime)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderMeshTop
####################################################################################################
class NMV_RenderMeshTop(bpy.types.Operator):
    """Render top view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.render_mesh_top"
    bl_label = "Top"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator

        :param context:
            Rendering context.
        :return:
            'FINISHED'.
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_mesh_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.TOP,
            image_format=nmv.interface.ui.globals.options.mesh.image_format)

        # Stats.
        rendering_time = time.time()
        global is_mesh_rendered
        is_mesh_rendered = True
        context.scene.NMV_MeshRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MeshRenderingTime)

        # Confirm operation done
        return {'FINISHED'}


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
            context.scene.NMV_NeuronMeshRenderingProgress = int(100 * self.timer_limits / 360.0)

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator

        :param context:
            Panel context.
        """

        # Timer
        self.start_time = time.time()

        # If no morphology is loaded, report it
        if nmv.interface.ui_morphology is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Validate the output directory
        nmv.interface.ui.validate_output_directory(
            panel_object=self, context_scene=context.scene)

        # Get a list of all the meshes in the scene
        self.scene_objects = nmv.scene.get_list_of_meshes_in_scene()

        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui.globals.options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui.globals.options.io.sequences_directory)

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
            nmv.interface.ui.globals.options.io.sequences_directory,
            nmv.interface.ui.globals.options.morphology.label,
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
        self.report({'INFO'}, 'Morphology Rendering Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @NMV_ExportMesh
####################################################################################################
class NMV_ExportMesh(bpy.types.Operator):
    """Export neuron mesh"""

    # Operator parameters
    bl_idname = "nmv.export_neuron_mesh"
    bl_label = "Export"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Executes the operator

        :param context:
            Rendering context.
        :return:
            'FINISHED'
        """

        # If no morphology is loaded, report it
        if nmv.interface.ui_morphology is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Validate the output directory
        nmv.interface.ui.validate_output_directory(panel_object=self, context_scene=context.scene)

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui.globals.options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui.globals.options.io.meshes_directory)

        # Get a list of all the meshes in the scene
        mesh_objects = nmv.scene.get_list_of_meshes_in_scene()

        # Export
        nmv.file.export_mesh_objects_to_file(mesh_objects,
                                             nmv.interface.ui.globals.options.io.meshes_directory,
                                             nmv.interface.ui_morphology.label,
                                             context.scene.NMV_ExportedMeshFormat,
                                             context.scene.NMV_ExportIndividuals)

        return {'FINISHED'}


####################################################################################################
# @NMV_MeshReconstructionDocumentation
####################################################################################################
class NMV_MeshReconstructionDocumentation(bpy.types.Operator):
    """Open the online documentation page of the Mesh Reconstruction panel."""

    # Operator parameters
    bl_idname = "nmv.documentation_mesh"
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
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis/wiki/Mesh-Reconstruction')
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Register all the classes in this panel"""

    # Mesh reconstruction panel
    bpy.utils.register_class(NMV_MeshPanel)

    # Buttons
    bpy.utils.register_class(NMV_MeshReconstructionDocumentation)
    bpy.utils.register_class(NMV_ReconstructNeuronMesh)
    bpy.utils.register_class(NMV_RenderMeshFront)
    bpy.utils.register_class(NMV_RenderMeshSide)
    bpy.utils.register_class(NMV_RenderMeshTop)
    bpy.utils.register_class(NMV_RenderMesh360)
    bpy.utils.register_class(NMV_ExportMesh)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-register all the classes in this panel"""

    # Mesh reconstruction panel
    bpy.utils.unregister_class(NMV_MeshPanel)

    # Buttons
    bpy.utils.unregister_class(NMV_MeshReconstructionDocumentation)
    bpy.utils.unregister_class(NMV_ReconstructNeuronMesh)
    bpy.utils.unregister_class(NMV_RenderMeshFront)
    bpy.utils.unregister_class(NMV_RenderMeshSide)
    bpy.utils.unregister_class(NMV_RenderMeshTop)
    bpy.utils.unregister_class(NMV_RenderMesh360)
    bpy.utils.unregister_class(NMV_ExportMesh)

