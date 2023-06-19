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


####################################################################################################
# @draw_documentation_button
####################################################################################################
def draw_documentation_button(layout):

    row = layout.column()
    row.operator('nmv.documentation_editing', icon='URL')
    row.separator()


####################################################################################################
# @draw_sketch_skeleton_button
####################################################################################################
def draw_sketch_skeleton_button(layout):

    row = layout.column(align=True)
    row.operator('sketch.skeleton', icon='PARTICLE_POINT')


####################################################################################################
# @draw_skeleton_edit_header
####################################################################################################
def draw_skeleton_edit_header(layout):

    row = layout.row()
    row.label(text='Editing Samples Coordinates', icon='OUTLINER_OB_EMPTY')


####################################################################################################
# @draw_edit_skeleton_button
####################################################################################################
def draw_edit_skeleton_button(layout):

    draw_skeleton_edit_header(layout=layout)

    row = layout.column(align=True)
    row.operator('edit.morphology_coordinates', icon='MESH_DATA')


####################################################################################################
# @draw_update_skeleton_button
####################################################################################################
def draw_update_skeleton_button(layout):

    draw_skeleton_edit_header(layout=layout)

    row = layout.column(align=True)
    row.operator('update.morphology_coordinates', icon='MESH_DATA')


####################################################################################################
# @draw_morphology_export_button
####################################################################################################
def draw_morphology_export_button(layout):
    row = layout.row()
    row.label(text='Export Morphology', icon='MESH_UVSPHERE')

    row = layout.column(align=True)
    row.operator('export_morphology.swc', icon='GROUP_VERTEX')