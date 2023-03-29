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


import time

import bpy

import nmv.enums
import nmv.interface


####################################################################################################
# @NMV_RenderMeshFront
####################################################################################################
class NMV_RenderMeshFront(bpy.types.Operator):
    """Render front view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.render_mesh_front"
    bl_label = "Front"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator

        :param context:
            Rendering Context.
        :return:
            'FINISHED'
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_mesh_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.FRONT,
            image_format=nmv.interface.ui_options.rendering.image_format)

        # Stats.
        rendering_time = time.time()
        nmv.interface.ui_mesh_rendered = True
        context.scene.NMV_MeshRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MeshRenderingTime)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderMeshSide
####################################################################################################
class NMV_RenderMeshSide(bpy.types.Operator):
    """Render side view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.render_mesh_side"
    bl_label = "Side"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator

        :param context:
            Rendering context.
        :return:
            'FINISHED'
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_mesh_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.SIDE,
            image_format=nmv.interface.ui_options.rendering.image_format)

        # Stats.
        rendering_time = time.time()
        nmv.interface.ui_mesh_rendered = True
        context.scene.NMV_MeshRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MeshRenderingTime)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @NMV_RenderMeshTop
####################################################################################################
class NMV_RenderMeshTop(bpy.types.Operator):
    """Render top view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.render_mesh_top"
    bl_label = "Top"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator

        :param context:
            Rendering context.
        :return:
            'FINISHED'.
        """

        # Timer
        start_time = time.time()

        # Render the image
        nmv.interface.ui.render_mesh_image(
            self, context_scene=context.scene, view=nmv.enums.Camera.View.TOP,
            image_format=nmv.interface.ui_options.rendering.image_format)

        # Stats.
        rendering_time = time.time()
        nmv.interface.ui_mesh_rendered = True
        context.scene.NMV_MeshRenderingTime = rendering_time - start_time
        nmv.logger.statistics('Morphology rendered in [%f] seconds' %
                              context.scene.NMV_MeshRenderingTime)

        # Confirm operation done
        return {'FINISHED'}

