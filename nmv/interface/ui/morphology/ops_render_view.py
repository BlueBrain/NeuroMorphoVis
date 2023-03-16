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
import copy

# Blender imports
import bpy

# Internal imports
import nmv.bbox
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.shading
import nmv.scene
import nmv.skeleton
import nmv.utilities
import nmv.rendering
import nmv.geometry



####################################################################################################
# @NMV_RenderMorphologyFront
####################################################################################################
class NMV_RenderMorphologyFront(bpy.types.Operator):
    """Render front view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_front"
    bl_label = "Front"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Rendering Context.
        :return:
            'FINISHED'.
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_morphology_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.FRONT,
            image_format=nmv.interface.ui.globals.options.morphology.image_format)

        # Stats.
        rendering_time = time.time()
        nmv.interface.ui.is_morphology_rendered = True
        context.scene.NMV_MorphologyRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MorphologyRenderingTime)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderMorphologySide
####################################################################################################
class NMV_RenderMorphologySide(bpy.types.Operator):
    """Render side view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_side"
    bl_label = "Side"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator.

        :param context:
            Rendering context.
        :return:
            'FINISHED'.
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_morphology_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.SIDE,
            image_format=nmv.interface.ui.globals.options.morphology.image_format)

        # Stats.
        rendering_time = time.time()
        nmv.interface.ui.is_morphology_rendered = True
        context.scene.NMV_MorphologyRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MorphologyRenderingTime)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderMorphologyTop
####################################################################################################
class NMV_RenderMorphologyTop(bpy.types.Operator):
    """Render top view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "nmv.render_morphology_top"
    bl_label = "Top"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator.

        :param context:
            Rendering context.
        :return:
            'FINISHED'.
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_morphology_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.TOP,
            image_format=nmv.interface.ui.globals.options.morphology.image_format)

        # Stats.
        rendering_time = time.time()
        nmv.interface.ui.is_morphology_rendered = True
        context.scene.NMV_MorphologyRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MorphologyRenderingTime)

        # Confirm operation done
        return {'FINISHED'}