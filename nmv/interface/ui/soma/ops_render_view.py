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
import time

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @NMV_RenderSomaFront
####################################################################################################
class NMV_RenderSomaFront(bpy.types.Operator):
    """Render the Front view of the soma"""

    # Operator parameters
    bl_idname = "nmv.render_soma_front"
    bl_label = "Front (XY)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        start_time = time.time()
        nmv.interface.render_meshes_relevant_image(
            options=nmv.interface.ui_options,
            morphology=nmv.interface.ui_morphology,
            camera_view=nmv.enums.Camera.View.FRONT,
            image_suffix=nmv.consts.Suffix.SOMA_FRONT)
        rendering_time = time.time()

        # Update the UI
        nmv.interface.ui_soma_rendered = True
        context.scene.NMV_SomaRenderingTime = rendering_time - start_time
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderSomaSide
####################################################################################################
class NMV_RenderSomaSide(bpy.types.Operator):
    """Render the Side view of the soma"""

    # Operator parameters
    bl_idname = "nmv.render_soma_side"
    bl_label = "Side (YZ)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        start_time = time.time()
        nmv.interface.render_meshes_relevant_image(
            options=nmv.interface.ui_options,
            morphology=nmv.interface.ui_morphology,
            camera_view=nmv.enums.Camera.View.SIDE,
            image_suffix=nmv.consts.Suffix.SOMA_SIDE)
        rendering_time = time.time()

        # Update the UI
        nmv.interface.ui_soma_rendered = True
        context.scene.NMV_SomaRenderingTime = rendering_time - start_time
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderSomaTop
####################################################################################################
class NMV_RenderSomaTop(bpy.types.Operator):
    """Render the Top view of the soma"""

    # Operator parameters
    bl_idname = "nmv.render_soma_top"
    bl_label = "Top (XZ)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        start_time = time.time()
        nmv.interface.render_meshes_relevant_image(
            options=nmv.interface.ui_options,
            morphology=nmv.interface.ui_morphology,
            camera_view=nmv.enums.Camera.View.TOP,
            image_suffix=nmv.consts.Suffix.SOMA_TOP)
        rendering_time = time.time()

        # Update the UI
        nmv.interface.ui_soma_rendered = True
        context.scene.NMV_SomaRenderingTime = rendering_time - start_time
        return {'FINISHED'}
