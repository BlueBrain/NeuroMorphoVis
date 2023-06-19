####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import copy
import time

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.scene
import nmv.utilities

from .layout_props import *


####################################################################################################
# @NMV_IOPanel
####################################################################################################
class NMV_IOPanel(bpy.types.Panel):
    """The input and output data panel of NeuroMorphoVis"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_idname = "OBJECT_PT_NMV_IO"
    bl_label = 'Input / Output'
    bl_category = 'NeuroMorphoVis'

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):

        draw_io_documentation_button(panel=self)
        self.layout.separator()

        draw_input_data_options(
            panel=self, scene=context.scene, options=nmv.interface.ui_options)
        self.layout.separator()

        draw_morphology_loading_button(panel=self)
        self.layout.separator()

        draw_morphology_loading_statistics(
            panel=self, scene=context.scene, morphology=nmv.interface.ui_morphology)
        self.layout.separator()

        draw_output_data_options(
            panel=self, scene=context.scene, options=nmv.interface.ui_options)



