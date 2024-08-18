####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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

# Internal imports
import nmv.consts
import nmv.enums
import nmv.bbp
import nmv.scene


####################################################################################################
# @draw_render_view_header
####################################################################################################
def draw_render_view_header(layout):

    row = layout.row()
    row.label(text='Render View', icon='RESTRICT_RENDER_OFF')


####################################################################################################
# @draw_render_animation_header
####################################################################################################
def draw_render_animation_header(layout):

    row = layout.row()
    row.label(text='Render Animation', icon='CAMERA_DATA')


####################################################################################################
# @draw_soma_rendering_buttons
####################################################################################################
def draw_soma_rendering_buttons(panel, scene):

    draw_render_view_header(layout=panel.layout)

    row = panel.layout.row(align=True)
    row.operator('nmv.render_soma_front', icon='AXIS_FRONT')
    row.operator('nmv.render_soma_side', icon='AXIS_SIDE')
    row.operator('nmv.render_soma_top', icon='AXIS_TOP')


####################################################################################################
# @draw_soma_render_animation_buttons
####################################################################################################
def draw_soma_render_animation_buttons(layout, scene, options):

    row = layout.row(align=True)
    row.operator('nmv.render_soma_360', icon='FORCE_MAGNETIC')

    # Progressive rendering is only for the soft body physics
    if options.soma.method == nmv.enums.Soma.Representation.SOFT_BODY:
        row.operator('nmv.render_soma_progressive', icon='FORCE_HARMONIC')


####################################################################################################
# @draw_soma_animation_rendering_progress
####################################################################################################
def draw_soma_animation_rendering_progress(layout, scene):

    row = layout.row()
    row.prop(scene, 'NMV_SomaRenderingProgress')
    row.enabled = False


####################################################################################################
# @draw_soma_rendering_time
####################################################################################################
def draw_soma_rendering_time(layout, scene):

    row = layout.row()
    row.prop(scene, 'NMV_SomaRenderingTime')
    row.enabled = False


####################################################################################################
# draw_soma_frame_rendering_options
####################################################################################################
def draw_soma_frame_rendering_options(panel, scene, options):

    nmv.interface.ui.common.draw_rendering_header(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_frame_resolution_basis_options(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_image_format_option(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_scale_bar_option(
        layout=panel.layout, scene=scene, options=options)
    panel.layout.separator()

    draw_soma_rendering_buttons(panel=panel, scene=scene)

    if nmv.interface.ui_soma_rendered:
        draw_soma_rendering_time(layout=panel.layout, scene=scene)
        panel.layout.separator()


####################################################################################################
# draw_soma_progressive_rendering_options
####################################################################################################
def draw_soma_progressive_rendering_options(panel, scene, options):

    draw_render_animation_header(layout=panel.layout)

    draw_soma_render_animation_buttons(layout=panel.layout, scene=scene, options=options)

    draw_soma_animation_rendering_progress(layout=panel.layout, scene=scene)
