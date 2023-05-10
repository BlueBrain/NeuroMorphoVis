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

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.interface
import nmv.utilities

# Layout
from .layout_buttons import *
from .layout_skeleton_props import *
from .layout_reconstruction_props import *
from .layout_color_props import *
from .layout_rendering_props import *


####################################################################################################
# @NMV_MorphologyPanel
####################################################################################################
class NMV_MorphologyPanel(bpy.types.Panel):
    """Morphology Tools Panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
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
    def draw(self, context):

        # Verify the presence of a reconstructed morphology in the scene
        if len(nmv.interface.ui_reconstructed_skeleton) > 0:
            if nmv.scene.verify_objects_list_in_scene(nmv.interface.ui_reconstructed_skeleton):
                nmv.interface.ui_morphology_reconstructed = True
            else:
                nmv.interface.ui_morphology_reconstructed = False
        else:
            nmv.interface.ui_morphology_reconstructed = False

        draw_documentation_button(layout=self.layout)
        self.layout.separator()

        draw_morphology_reconstruction_options(
            layout=self.layout, scene=context.scene,
            options=nmv.interface.ui_options, morphology=nmv.interface.ui_morphology)
        self.layout.separator()

        draw_morphology_skeleton_display_options(
            layout=self.layout, scene=context.scene,
            options=nmv.interface.ui_options, morphology=nmv.interface.ui_morphology)
        self.layout.separator()

        draw_morphology_color_options(
            layout=self.layout, scene=context.scene,
            options=nmv.interface.ui_options, morphology=nmv.interface.ui_morphology)
        self.layout.separator()

        method = nmv.interface.ui_options.morphology.reconstruction_method
        if method == nmv.enums.Skeleton.Method.DENDROGRAM:
            draw_morphology_reconstruction_button(
                layout=self.layout, scene=context.scene, label='Reconstruct Dendrogram',
                show_stats=nmv.interface.ui_morphology_reconstructed)
        else:
            draw_morphology_reconstruction_button(
                layout=self.layout, scene=context.scene, label='Reconstruct Morphology',
                show_stats=nmv.interface.ui_morphology_reconstructed)
        self.layout.separator()

        draw_rendering_options(
            panel=self, scene=context.scene, options=nmv.interface.ui_options,
            show_stats=nmv.interface.ui_morphology_rendered)
        self.layout.separator()

        # Export buttons
        draw_morphology_export_options(panel=self)
        self.layout.separator()

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(self.layout)
