####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# Internal imports
import nmv.enums
import nmv.interface


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

        start_time = time.time()
        context.scene.NMV_SynapticsRenderingTime = nmv.interface.ui.render_synaptics_image(
            self, scene=context.scene, options=nmv.interface.ui_options,
            view=nmv.enums.Camera.View.FRONT)
        rendering_time = time.time()

        # Update the UI
        nmv.interface.ui_synaptics_rendered = True
        context.scene.NMV_SynapticsRenderingTime = rendering_time - start_time
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

        start_time = time.time()
        context.scene.NMV_SynapticsRenderingTime = nmv.interface.ui.render_synaptics_image(
            self, scene=context.scene, options=nmv.interface.ui_options,
            view=nmv.enums.Camera.View.SIDE)
        rendering_time = time.time()

        # Update the UI
        nmv.interface.ui_synaptics_rendered = True
        context.scene.NMV_SynapticsRenderingTime = rendering_time - start_time
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

        start_time = time.time()
        context.scene.NMV_SynapticsRenderingTime = nmv.interface.ui.render_synaptics_image(
            self, scene=context.scene, options=nmv.interface.ui_options,
            view=nmv.enums.Camera.View.TOP)
        rendering_time = time.time()

        # Update the UI
        nmv.interface.ui_synaptics_rendered = True
        context.scene.NMV_SynapticsRenderingTime = rendering_time - start_time
        return {'FINISHED'}

