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

    row = layout.row()
    row.operator('nmv.documentation_soma', icon='URL')


####################################################################################################
# @draw_soma_mesh_export_button
####################################################################################################
def draw_soma_mesh_export_button(panel, scene):

    row = panel.layout.row()
    row.label(text='Export Soma Mesh', icon='MESH_UVSPHERE')

    export_format = panel.layout.row()
    export_format.prop(scene, 'NMV_ExportedSomaMeshFormat', icon='GROUP_VERTEX')

    # Save button
    row = panel.layout.column()
    row.operator('nmv.export_soma_mesh', icon='MESH_DATA')