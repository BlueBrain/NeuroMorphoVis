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


####################################################################################################
# @draw_documentation_button
####################################################################################################
def draw_documentation_button(layout):

    row = layout.row()
    row.operator('nmv.documentation_morphology', icon='URL')


####################################################################################################
# @draw_morphology_reconstruction_button
####################################################################################################
def draw_morphology_reconstruction_button(layout,
                                          scene,
                                          label=bpy.types.Scene.NMV_MorphologyButtonLabel,
                                          show_stats=False):

    row = layout.row()
    row.label(text='Quick Reconstruction', icon='PARTICLE_POINT')
    button_row = layout.row()
    button_row.operator('nmv.reconstruct_morphology', text=label, icon='RNA_ADD')
    button_row.enabled = True

    if show_stats:
        row = layout.row()
        row.prop(scene, 'NMV_MorphologyReconstructionTime')
        row.enabled = False


####################################################################################################
# @draw_morphology_rendering_buttons
####################################################################################################
def draw_morphology_rendering_buttons(panel, scene, show_stats=False):

    view_row = panel.layout.row()
    view_row.label(text='Render View', icon='RESTRICT_RENDER_OFF')
    buttons_row = panel.layout.row(align=True)
    buttons_row.operator('nmv.render_morphology_front', icon='AXIS_FRONT')
    buttons_row.operator('nmv.render_morphology_side', icon='AXIS_SIDE')
    buttons_row.operator('nmv.render_morphology_top', icon='AXIS_TOP')


####################################################################################################
# @draw_dendrogram_rendering_button
####################################################################################################
def draw_dendrogram_rendering_button(panel, scene):

    row = panel.layout.row()
    row.label(text='Render Dendrogram', icon='RESTRICT_RENDER_OFF')
    buttons_row = panel.layout.row()
    buttons_row.operator('nmv.render_morphology_front', icon='AXIS_FRONT')


####################################################################################################
# @draw_animated_morphology_rendering_buttons
####################################################################################################
def draw_animated_morphology_rendering_buttons(panel, scene):

    animation_row = panel.layout.row()
    animation_row.label(text='Render Animation (Front View - XY)', icon='CAMERA_DATA')
    buttons_row = panel.layout.row(align=True)
    buttons_row.operator('nmv.render_morphology_360', icon='FORCE_MAGNETIC')
    buttons_row.operator('nmv.render_morphology_progressive', icon='FORCE_HARMONIC')
    buttons_row.enabled = True

    # Progress bar
    progress_bar_row = panel.layout.row()
    progress_bar_row.prop(scene, 'NMV_MorphologyRenderingProgress')
    progress_bar_row.enabled = False


####################################################################################################
# draw_export_options
####################################################################################################
def draw_export_options(layout):

    # Saving morphology options
    row = layout.row()
    row.label(text='Export Morphology', icon='MESH_UVSPHERE')

    row = layout.column(align=True)
    row.operator('nmv.save_morphology_blend', icon='MESH_MONKEY')
    row.operator('nmv.save_morphology_swc', icon='GRAPH')
    row.operator('nmv.save_morphology_segments', icon='NOCURVE')
    row.enabled = True


