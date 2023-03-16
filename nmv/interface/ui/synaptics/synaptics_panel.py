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
import time

# Blender imports
import bpy

# Internal imports
import nmv.bbp
import nmv.enums
import nmv.interface
import nmv.utilities
import nmv.scene

import nmv.interface.ui

from .synaptics_panel_ops import *
from .synaptics_panel_draw_ops import *
from .synaptics_panel_options import *


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
        options = nmv.interface.ui.globals.options

        # If a circuit is loaded, enable this panel, otherwise disable it
        if True:#nmv.interface.ui_circuit is not None:

            # Select a use case
            use_case_row = self.layout.row()
            use_case_row.prop(context.scene, 'NMV_SynapticsUseCase')
            options.synaptics.use_case = context.scene.NMV_SynapticsUseCase

            # Display the options accordingly, based on the use case selection
            if context.scene.NMV_SynapticsUseCase != nmv.enums.Synaptics.UseCase.NOT_SELECTED:

                # Draw the reconstruction options
                draw_synaptics_reconstruction_options(
                    layout=self.layout, scene=context.scene, options=options)

                # Draw the rendering operations
                draw_synaptics_rendering_options(panel=self, scene=context.scene, options=options)

        # Otherwise, draw the out of context message and disable the panel
        else:
            draw_out_of_context_message(layout=self.layout, scene=context.scene, options=options)
            #self.layout.enabled = False if nmv.interface.ui_circuit is None else True


####################################################################################################
# @NMV_ReconstructSynaptics
####################################################################################################
class NMV_ReconstructSynaptics(bpy.types.Operator):
    """Reconstruct the synaptics scene"""

    # Operator parameters
    bl_idname = "nmv.reconstruct_synaptics"
    bl_label = "Reconstruct Synaptics"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        return reconstruct_synaptics(operator=self, context=context,
                                     circuit=nmv.interface.ui_circuit,
                                     options=nmv.interface.ui.globals.options)


####################################################################################################
# @NMV_RenderSynapticsFront
####################################################################################################
class NMV_RenderSynapticsFront(bpy.types.Operator):
    """Render front view of the reconstructed scene"""

    # Operator parameters
    bl_idname = "nmv.render_synaptics_front"
    bl_label = "Front"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        # Render the image and report the rendering time
        context.scene.NMV_SynapticsRenderingTime = nmv.interface.ui.render_synaptics_image(
            self, scene=context.scene, options=nmv.interface.ui.globals.options,
            view=nmv.enums.Camera.View.FRONT)
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderSynapticsSide
####################################################################################################
class NMV_RenderSynapticsSide(bpy.types.Operator):
    """Render side view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.render_synaptics_side"
    bl_label = "Side"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        # Render the image and report the rendering time
        context.scene.NMV_SynapticsRenderingTime = nmv.interface.ui.render_synaptics_image(
            self, scene=context.scene, options=nmv.interface.ui.globals.options,
            view=nmv.enums.Camera.View.SIDE)
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderSynapticsTop
####################################################################################################
class NMV_RenderSynapticsTop(bpy.types.Operator):
    """Render top view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.render_synaptics_top"
    bl_label = "Top"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Render the image and report the rendering time
        context.scene.NMV_SynapticsRenderingTime = nmv.interface.ui.render_synaptics_image(
            self, scene=context.scene, options=nmv.interface.ui.globals.options,
            view=nmv.enums.Camera.View.TOP)
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Panel
    bpy.utils.register_class(NMV_SynapticsPanel)

    # Button(s)
    bpy.utils.register_class(NMV_ReconstructSynaptics)
    bpy.utils.register_class(NMV_RenderSynapticsFront)
    bpy.utils.register_class(NMV_RenderSynapticsSide)
    bpy.utils.register_class(NMV_RenderSynapticsTop)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Panel
    bpy.utils.unregister_class(NMV_SynapticsPanel)

    # Button(s)
    bpy.utils.unregister_class(NMV_ReconstructSynaptics)
    bpy.utils.unregister_class(NMV_RenderSynapticsFront)
    bpy.utils.unregister_class(NMV_RenderSynapticsSide)
    bpy.utils.unregister_class(NMV_RenderSynapticsTop)
