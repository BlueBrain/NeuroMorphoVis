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

# System imports
import sys

# Blender imports
import bpy

# Internal imports
import nmv
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


####################################################################################################
# @MeshPanel
####################################################################################################
class MeshPanel(bpy.types.Panel):
    """MeshPanel class"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if nmv.utilities.is_blender_280() else 'TOOLS'
    bl_idname = "OBJECT_PT_NMV_MeshingToolBox"
    bl_label = 'Mesh Toolbox'
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

        # Meshing options
        draw_meshing_options(panel=self, scene=context.scene)

        # Color options
        draw_color_options(panel=self, scene=context.scene)

        # Mesh reconstruction button
        draw_mesh_reconstruction_button(panel=self, scene=context.scene)

        # Rendering options
        draw_rendering_options(panel=self, scene=context.scene)

        # Mesh export options
        draw_mesh_export_options(panel=self, scene=context.scene)

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(self.layout)


####################################################################################################
# @ReconstructNeuronMesh
####################################################################################################
class ReconstructNeuronMesh(bpy.types.Operator):
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

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Meshing technique
        meshing_technique = nmv.interface.ui_options.mesh.meshing_technique

        # Piece-wise watertight meshing
        if meshing_technique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
            mesh_builder = nmv.builders.PiecewiseBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Union
        elif meshing_technique == nmv.enums.Meshing.Technique.UNION:
            mesh_builder = nmv.builders.UnionBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Skinning
        elif meshing_technique == nmv.enums.Meshing.Technique.SKINNING:
            mesh_builder = nmv.builders.SkinningBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Meta Balls
        elif meshing_technique == nmv.enums.Meshing.Technique.META_OBJECTS:
            mesh_builder = nmv.builders.MetaBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        else:

            # Invalid method
            self.report({'ERROR'}, 'Invalid Meshing Technique')

        return {'FINISHED'}


####################################################################################################
# @RenderMeshFront
####################################################################################################
class RenderMeshFront(bpy.types.Operator):
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

        # Render the image
        nmv.interface.ui.render_mesh_image(self, context.scene, nmv.enums.Camera.View.FRONT)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMeshSide
####################################################################################################
class RenderMeshSide(bpy.types.Operator):
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

        # Render the image
        nmv.interface.ui.render_mesh_image(self, context.scene, nmv.enums.Camera.View.SIDE)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMeshTop
####################################################################################################
class RenderMeshTop(bpy.types.Operator):
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

        # Render the image
        nmv.interface.ui.render_mesh_image(self, context.scene, nmv.enums.Camera.View.TOP)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMesh360
####################################################################################################
class RenderMesh360(bpy.types.Operator):
    """Render a 360 view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.render_mesh_360"
    bl_label = "360"

    # Timer parameters
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
                    nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

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
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.sequences_directory)

        # Compute the bounding box for a close up view
        if context.scene.NMV_MeshRenderingView == nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            rendering_bbox = nmv.bbox.compute_unified_extent_bounding_box(
                extent=context.scene.NMV_MeshCloseUpSize)

        # Compute the bounding box for a mid shot view
        elif context.scene.NMV_MeshRenderingView == nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW:

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
        self.bounding_box_360.extend_bbox(delta=nmv.consts.Image.GAP_DELTA)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_mesh_360' % (
            nmv.interface.ui_options.io.sequences_directory,
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
# @SaveNeuronMeshBLEND
####################################################################################################
class ExportMesh(bpy.types.Operator):
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
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Get a list of all the meshes in the scene
        mesh_objects = nmv.scene.get_list_of_meshes_in_scene()

        # Export
        nmv.file.export_mesh_objects_to_file(mesh_objects,
                                             nmv.interface.ui_options.io.meshes_directory,
                                             nmv.interface.ui_morphology.label,
                                             context.scene.NMV_ExportedMeshFormat,
                                             context.scene.NMV_ExportIndividuals)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Register all the classes in this panel"""

    # Mesh reconstruction panel
    bpy.utils.register_class(MeshPanel)

    # Mesh reconstruction button
    bpy.utils.register_class(ReconstructNeuronMesh)

    # Mesh rendering
    bpy.utils.register_class(RenderMeshFront)
    bpy.utils.register_class(RenderMeshSide)
    bpy.utils.register_class(RenderMeshTop)
    bpy.utils.register_class(RenderMesh360)

    # Neuron mesh saving operators
    bpy.utils.register_class(ExportMesh)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-register all the classes in this panel"""

    # Mesh reconstruction panel
    bpy.utils.unregister_class(MeshPanel)

    # Mesh reconstruction button
    bpy.utils.unregister_class(ReconstructNeuronMesh)

    # Mesh rendering
    bpy.utils.unregister_class(ExportMesh)

    # Neuron mesh saving operators
    bpy.utils.unregister_class(ExportMesh)

