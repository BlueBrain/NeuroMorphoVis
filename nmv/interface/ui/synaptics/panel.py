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
import sys

# Blender imports
import bpy

# Internal imports
import nmv.bbp
import nmv.enums
import nmv.interface
import nmv.utilities
import nmv.scene
from .layout_props import *


####################################################################################################
# @NMV_SynapticsPanel
####################################################################################################
class NMV_SynapticsPanel(bpy.types.Panel):
    """NMV Synaptics panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_idname = "OBJECT_PT_NMV_Synaptics"
    bl_label = 'Synaptics Toolbox'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):

        # Get a reference to the options
        options = nmv.interface.ui_options

        # If a circuit is loaded, enable this panel, otherwise disable it
        if nmv.interface.ui_circuit is not None:

            # Select a use case
            use_case_row = self.layout.row()
            use_case_row.prop(context.scene, 'NMV_SynapticsUseCase')
            options.synaptics.use_case = context.scene.NMV_SynapticsUseCase
            self.layout.separator()

            # Display the options accordingly, based on the use case selection
            if context.scene.NMV_SynapticsUseCase != nmv.enums.Synaptics.UseCase.NOT_SELECTED:

                # Draw the reconstruction options
                draw_synaptics_reconstruction_options(
                    layout=self.layout, scene=context.scene, options=options)
                self.layout.separator()

                # Draw the reconstruction button
                draw_synaptics_reconstruction_button(layout=self.layout, scene=context.scene)
                self.layout.separator()

                # Draw the rendering operations
                draw_synaptics_rendering_options(panel=self, scene=context.scene, options=options)

        # Otherwise, draw the out of context message and disable the panel
        else:
            draw_out_of_context_message(layout=self.layout, scene=context.scene, options=options)
            self.layout.enabled = False if nmv.interface.ui_circuit is None else True



