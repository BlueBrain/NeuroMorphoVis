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

    sketching_morphology_column = layout.column(align=True)
    sketching_morphology_column.operator('sketch.skeleton', icon='PARTICLE_POINT')


####################################################################################################
# @draw_edit_skeleton_button
####################################################################################################
def draw_edit_skeleton_button(layout):

    edit_morphology_column = layout.column(align=True)
    edit_morphology_column.operator('edit.morphology_coordinates', icon='MESH_DATA')


####################################################################################################
# @draw_edit_skeleton_button
####################################################################################################
def draw_skeleton_update_button(layout):

    update_morphology_column = layout.column(align=True)
    update_morphology_column.operator('update.morphology_coordinates', icon='MESH_DATA')


####################################################################################################
# @draw_morphology_export_button
####################################################################################################
def draw_morphology_export_button(layout):
    save_morphology_row = layout.row()
    save_morphology_row.label(text='Save Morphology As:', icon='MESH_UVSPHERE')

    save_morphology_buttons_column = self.layout.column(align=True)
    save_morphology_buttons_column.operator('export_morphology.swc', icon='GROUP_VERTEX')