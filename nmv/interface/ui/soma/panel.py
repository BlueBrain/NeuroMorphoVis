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


from .layout_buttons import draw_documentation_button
from .layout_buttons import draw_soma_mesh_export_button
from .layout_color_props import draw_soma_color_options
from .layout_rendering_props import draw_soma_frame_rendering_options
from .layout_rendering_props import draw_soma_progressive_rendering_options
from .layout_reconstruction_props import draw_soma_reconstruction_options
from .layout_reconstruction_props import draw_soma_reconstruction_button


####################################################################################################
# @NMV_SomaPanel
####################################################################################################
class NMV_SomaPanel(bpy.types.Panel):
    """Soma panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_idname = "OBJECT_PT_NMV_SomaToolBox"
    bl_label = 'Soma Toolbox'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):

        options = nmv.interface.ui_options
        morphology = nmv.interface.ui_morphology

        # Documentation button
        draw_documentation_button(layout=self.layout)
        self.layout.separator()

        # Soma reconstruction options
        draw_soma_reconstruction_options(
            panel=self, scene=context.scene, options=options, morphology=morphology)
        self.layout.separator()

        # Color options
        draw_soma_color_options(
            panel=self, scene=context.scene, options=options)
        self.layout.separator()

        # Reconstruction buttons
        draw_soma_reconstruction_button(
            layout=self.layout, scene=context.scene, options=options)
        self.layout.separator()

        # Still-frame rendering options
        draw_soma_frame_rendering_options(
            panel=self, scene=context.scene, options=options)
        self.layout.separator()

        # Progressive rendering options
        draw_soma_progressive_rendering_options(
            panel=self, scene=context.scene, options=options)
        self.layout.separator()

        draw_soma_mesh_export_button(panel=self, scene=context.scene)

        return

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




