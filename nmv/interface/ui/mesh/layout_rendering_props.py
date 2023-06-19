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

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.bbp
import nmv.scene


from .layout_buttons import draw_mesh_rendering_buttons


####################################################################################################
# draw_still_frame_rendering_options
####################################################################################################
def draw_still_frame_rendering_options(panel, scene, options, show_stats=False):

    nmv.interface.ui.common.draw_rendering_header(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_morphology_rendering_view_option(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_resolution_basis_option(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_resolution_options(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_image_format_option(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_scale_bar_option(
        layout=panel.layout, scene=scene, options=options)

    draw_mesh_rendering_buttons(panel=panel)

    if show_stats:
        row = panel.layout.row()
        row.prop(scene, 'NMV_MeshRenderingTime')
        row.enabled = False


####################################################################################################
# @draw_animated_360_rendering_buttons
####################################################################################################
def draw_animated_360_rendering_buttons(panel, scene):

    # Animation row
    animation_row = panel.layout.row()
    animation_row.label(text='Render Animation (Front View - XY)', icon='CAMERA_DATA')

    # Buttons
    buttons_row = panel.layout.row(align=True)
    buttons_row.operator('nmv.render_mesh_360', icon='FORCE_MAGNETIC')
    buttons_row.enabled = True

    # Progress bar
    progress_bar_row = panel.layout.row()
    progress_bar_row.prop(scene, 'NMV_MeshRenderingProgress')
    progress_bar_row.enabled = False

    if nmv.interface.ui_mesh_reconstructed:
        animation_row.enabled = True
        buttons_row.enabled = True
    else:
        animation_row.enabled = False
        buttons_row.enabled = False


####################################################################################################
# draw_rendering_options
####################################################################################################
def draw_rendering_options(panel, scene, options, show_stats=False):

    draw_still_frame_rendering_options(
        panel=panel, scene=scene, options=options, show_stats=show_stats)
    panel.layout.separator()

    draw_animated_360_rendering_buttons(panel=panel, scene=scene)

