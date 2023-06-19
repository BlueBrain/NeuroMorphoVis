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


####################################################################################################
# @draw_rendering_header
####################################################################################################
def draw_rendering_header(layout, scene, options):

    row = layout.row()
    row.label(text='Rendering Options', icon='RENDER_STILL')


####################################################################################################
# @draw_morphology_rendering_view_option
####################################################################################################
def draw_morphology_rendering_view_option(layout, scene, options):

    row = layout.row()
    row.label(text='Rendering View')
    row.prop(scene, 'NMV_MorphologyRenderingView', expand=True)
    options.rendering.rendering_view = scene.NMV_MorphologyRenderingView


####################################################################################################
# @draw_morphology_rendering_view_option_for
####################################################################################################
def draw_synaptics_rendering_view_option(layout, scene, options):

    row = layout.row()
    row.label(text='Rendering View')
    row.prop(scene, 'NMV_SynapticsRenderingView', expand=True)
    options.rendering.rendering_view = scene.NMV_SynapticsRenderingView


####################################################################################################
# @draw_resolution_basis_option
####################################################################################################
def draw_resolution_basis_option(layout, scene, options):

    row = layout.row()
    row.label(text='Resolution Basis')
    row.prop(scene, 'NMV_ResolutionBasis', expand=True)
    options.rendering.resolution_basis = scene.NMV_ResolutionBasis


####################################################################################################
# @draw_closeup_size_option
####################################################################################################
def draw_closeup_size_option(layout, scene, options):

    row = layout.row()
    row.label(text='Closeup Size')
    row.prop(scene, 'NMV_CloseupDimensions')
    options.rendering.close_up_dimensions = scene.NMV_CloseupDimensions


####################################################################################################
# @draw_frame_resolution_option
####################################################################################################
def draw_frame_resolution_option(layout, scene, options):

    resolution_row = layout.row()
    resolution_row.label(text='Frame Resolution')
    resolution_row.prop(scene, 'NMV_FrameResolution')
    options.rendering.frame_resolution = scene.NMV_FrameResolution


####################################################################################################
# @draw_frame_scale_factor_options
####################################################################################################
def draw_frame_scale_factor_options(layout, scene, options):

    scale_factor_row = layout.row()
    scale_factor_row.label(text='Resolution Scale Factor')
    scale_factor_row.prop(scene, 'NMV_ResolutionScaleFactor')
    options.rendering.resolution_scale_factor = scene.NMV_ResolutionScaleFactor


####################################################################################################
# @draw_frame_resolution_basis_options
####################################################################################################
def draw_image_format_option(layout, scene, options):

    row = layout.row()
    row.label(text='Image Format:')
    row.prop(scene, 'NMV_ImageFormat')
    options.rendering.image_format = scene.NMV_ImageFormat


####################################################################################################
# @draw_scale_bar_option
####################################################################################################
def draw_scale_bar_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_RenderScaleBar')
    options.rendering.render_scale_bar = scene.NMV_RenderScaleBar


####################################################################################################
# @draw_frame_resolution_basis_options
####################################################################################################
def draw_frame_resolution_basis_options(layout, scene, options):

    if options.rendering.resolution_basis == nmv.enums.Rendering.Resolution.FIXED:
        draw_frame_resolution_option(layout=layout, scene=scene, options=options)
    else:
        draw_frame_scale_factor_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_closeup_rendering_options
####################################################################################################
def draw_wide_shot_rendering_options(layout, scene, options):

    if options.rendering.resolution_basis == nmv.enums.Rendering.Resolution.FIXED:
        draw_frame_resolution_option(layout=layout, scene=scene, options=options)
    else:
        draw_frame_scale_factor_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_frame_resolution_basis_options
####################################################################################################
def draw_full_view_rendering_options(layout, scene, options):

    draw_frame_resolution_basis_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_resolution_options
####################################################################################################
def draw_resolution_options(layout, scene, options):

    if options.rendering.rendering_view == nmv.enums.Rendering.View.CLOSEUP:
        draw_closeup_size_option(layout=layout, scene=scene, options=options)

    if options.rendering.resolution_basis == nmv.enums.Rendering.Resolution.FIXED:
        draw_wide_shot_rendering_options(layout=layout, scene=scene, options=options)
    else:
        draw_full_view_rendering_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_rendering_buttons
####################################################################################################
def draw_rendering_buttons(panel, scene, options):

    # Rendering view
    view_row = panel.layout.row()
    view_row.label(text='Render View:', icon='RESTRICT_RENDER_OFF')
    buttons_row = panel.layout.row(align=True)
    buttons_row.operator('nmv.render_front_view_button', icon='AXIS_FRONT')
    buttons_row.operator('nmv.render_side_view_button', icon='AXIS_SIDE')
    buttons_row.operator('nmv.render_top_view_button', icon='AXIS_TOP')


