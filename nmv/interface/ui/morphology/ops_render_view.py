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
import nmv.consts
import nmv.enums


####################################################################################################
# @NMV_RenderMorphologyFront
####################################################################################################
class NMV_RenderMorphologyFront(bpy.types.Operator):
    """Render the front view (XY) of the morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_front"
    bl_label = "Front"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Render the frame
        start_time = time.time()
        nmv.interface.render_morphology_relevant_image(
            options=nmv.interface.ui_options,
            morphology=nmv.interface.ui_morphology,
            camera_view=nmv.enums.Camera.View.FRONT,
            image_suffix=nmv.consts.Suffix.MORPHOLOGY_FRONT)
        rendering_time = time.time()

        # Update the UI
        nmv.interface.ui_morphology_rendered = True
        context.scene.NMV_MorphologyRenderingTime = rendering_time - start_time
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderMorphologySide
####################################################################################################
class NMV_RenderMorphologySide(bpy.types.Operator):
    """Render the side view (YZ) of the morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_side"
    bl_label = "Side"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Render the frame
        start_time = time.time()
        nmv.interface.render_morphology_relevant_image(
            options=nmv.interface.ui_options,
            morphology=nmv.interface.ui_morphology,
            camera_view=nmv.enums.Camera.View.SIDE,
            image_suffix=nmv.consts.Suffix.MORPHOLOGY_SIDE)
        rendering_time = time.time()

        # Update the UI
        nmv.interface.ui_morphology_rendered = True
        context.scene.NMV_MorphologyRenderingTime = rendering_time - start_time
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderMorphologyTop
####################################################################################################
class NMV_RenderMorphologyTop(bpy.types.Operator):
    """Render the top view (XZ) of the morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_top"
    bl_label = "Top"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Render the frame
        start_time = time.time()
        nmv.interface.render_morphology_relevant_image(
            options=nmv.interface.ui_options,
            morphology=nmv.interface.ui_morphology,
            camera_view=nmv.enums.Camera.View.TOP,
            image_suffix=nmv.consts.Suffix.MORPHOLOGY_TOP)
        rendering_time = time.time()

        # Update the UI
        nmv.interface.ui_morphology_rendered = True
        context.scene.NMV_MorphologyRenderingTime = rendering_time - start_time
        return {'FINISHED'}
