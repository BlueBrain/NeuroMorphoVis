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
import nmv.scene

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

        # Verify the presence of a reconstructed mesh in the scene
        if len(nmv.interface.ui_reconstructed_mesh) > 0:
            if nmv.scene.verify_objects_list_in_scene(nmv.interface.ui_reconstructed_mesh):
                nmv.interface.ui_mesh_reconstructed = True
            else:
                nmv.interface.ui_mesh_reconstructed = False
        else:
            nmv.interface.ui_mesh_reconstructed = False

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
