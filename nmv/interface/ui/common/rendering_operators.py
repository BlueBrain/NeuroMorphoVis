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


# Blender imports
import bpy


####################################################################################################
# @NMV_RenderFrontView
####################################################################################################
class NMV_RenderFrontView(bpy.types.Operator):
    """Render front view of the reconstructed scene in NeuroMorphoVis"""

    # Operator parameters
    bl_idname = "nmv.render_front_view_button"
    bl_label = "Front"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):


        # Render the image and report the rendering time
        #context.scene.NMV_SynapticsRenderingTime = nmv.interface.ui.render_synaptics_image(
        #    self, scene=context.scene, options=nmv.interface.ui_options,
        #    view=nmv.enums.Camera.View.FRONT)
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderSideView
####################################################################################################
class NMV_RenderSideView(bpy.types.Operator):
    """Render side view of the reconstructed scene in NeuroMorphoVis"""

    # Operator parameters
    bl_idname = "nmv.render_side_view_button"
    bl_label = "Side"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Render the image and report the rendering time
        #context.scene.NMV_SynapticsRenderingTime = nmv.interface.ui.render_synaptics_image(
        #    self, scene=context.scene, options=nmv.interface.ui_options,
        #    view=nmv.enums.Camera.View.FRONT)
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderTopView
####################################################################################################
class NMV_RenderTopView(bpy.types.Operator):
    """Render top view of the reconstructed scene in NeuroMorphoVis"""

    # Operator parameters
    bl_idname = "nmv.render_top_view_button"
    bl_label = "Top"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Render the image and report the rendering time
        #context.scene.NMV_SynapticsRenderingTime = nmv.interface.ui.render_synaptics_image(
        #    self, scene=context.scene, options=nmv.interface.ui_options,
        #    view=nmv.enums.Camera.View.FRONT)
        return {'FINISHED'}


####################################################################################################
# @register_common_operators
####################################################################################################
def register_common_operators():
    """Registers all the common operators"""

    # Buttons
    bpy.utils.register_class(NMV_RenderFrontView)
    bpy.utils.register_class(NMV_RenderSideView)
    bpy.utils.register_class(NMV_RenderTopView)


####################################################################################################
# @unregister_common_operators
####################################################################################################
def unregister_common_operators():
    """Un-registers all the common operators"""

    # Buttons
    bpy.utils.unregister_class(NMV_RenderFrontView)
    bpy.utils.unregister_class(NMV_RenderSideView)
    bpy.utils.unregister_class(NMV_RenderTopView)

