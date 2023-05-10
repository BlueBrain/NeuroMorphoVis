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

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.bbp
import nmv.scene


####################################################################################################
# @draw_rendering_buttons
####################################################################################################
def draw_synaptics_rendering_buttons(panel, scene, options):

    view_row = panel.layout.row()
    view_row.label(text='Render View', icon='RESTRICT_RENDER_OFF')
    buttons_row = panel.layout.row(align=True)
    buttons_row.operator('nmv.render_synaptics_front', icon='AXIS_FRONT')
    buttons_row.operator('nmv.render_synaptics_side', icon='AXIS_SIDE')
    buttons_row.operator('nmv.render_synaptics_top', icon='AXIS_TOP')

    if nmv.interface.ui_synaptics_rendered:
        row = panel.layout.row()
        row.prop(scene, 'NMV_SynapticsRenderingTime')
        row.enabled = False


####################################################################################################
# @draw_rendering_buttons
####################################################################################################
def draw_synaptics_rendering_options(panel, scene, options):

    # Rendering header
    nmv.interface.ui.draw_rendering_header(
        layout=panel.layout, scene=scene, options=options)

    # Rendering view
    nmv.interface.ui.draw_synaptics_rendering_view_option(
        layout=panel.layout, scene=scene, options=options)

    # Resolution basis
    nmv.interface.ui.draw_resolution_basis_option(
        layout=panel.layout, scene=scene, options=options)

    # Resolution
    nmv.interface.ui.draw_resolution_options(
        layout=panel.layout, scene=scene, options=options)

    # Image format
    nmv.interface.ui.draw_image_format_option(
        layout=panel.layout, scene=scene, options=options)

    # Scale bar
    nmv.interface.ui.draw_scale_bar_option(
        layout=panel.layout, scene=scene, options=options)

    # Rendering buttons
    draw_synaptics_rendering_buttons(
        panel=panel, scene=scene, options=options)

