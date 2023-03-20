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
import nmv.interface

# Layout
from .layout_buttons import *
from .layout_color_props import *
from .layout_reconstruction_props import *
from .layout_rendering_props import *


####################################################################################################
# @NMV_MeshPanel
####################################################################################################
class NMV_MeshPanel(bpy.types.Panel):
    """Meshing Tools Panel"""

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

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):

        draw_documentation_button(layout=self.layout)
        self.layout.separator()

        draw_mesh_reconstruction_options(
            panel=self, scene=context.scene,
            options=nmv.interface.ui_options, morphology=nmv.interface.ui_morphology)
        self.layout.separator()

        draw_mesh_color_options(layout=self.layout, scene=context.scene,
                                options=nmv.interface.ui_options,
                                morphology=nmv.interface.ui_morphology)
        self.layout.separator()

        draw_mesh_reconstruction_button(panel=self, scene=context.scene)
        self.layout.separator()

        draw_rendering_options(panel=self, scene=context.scene, options=nmv.interface.ui_options)
        self.layout.separator()

        draw_mesh_export_options(
            panel=self, scene=context.scene, options=nmv.interface.ui_options)
        self.layout.separator()

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(self.layout)

        """
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

        """





