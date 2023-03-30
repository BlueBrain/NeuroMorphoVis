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

# Internal imports
import nmv.consts
import nmv.enums
import nmv.bbp
import nmv.scene


####################################################################################################
# @draw_documentation_button
####################################################################################################
def draw_documentation_button(layout):

    row = layout.row()
    row.operator('nmv.documentation_mesh', icon='URL')


####################################################################################################
# @draw_mesh_reconstruction_button
####################################################################################################
def draw_mesh_reconstruction_button(panel, scene):

    # Get a reference to the layout of the panel
    layout = panel.layout

    # Mesh quick reconstruction options
    quick_reconstruction_row = layout.row()
    quick_reconstruction_row.label(text='Quick Reconstruction', icon='PARTICLE_POINT')

    # Mesh reconstruction options
    mesh_reconstruction_row = layout.row()
    mesh_reconstruction_row.operator('nmv.reconstruct_mesh', icon='MESH_DATA')

    if nmv.interface.ui_mesh_reconstructed:
        morphology_stats_row = panel.layout.row()
        morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')
        reconstruction_time_row = panel.layout.row()
        reconstruction_time_row.prop(scene, 'NMV_MeshReconstructionTime')
        reconstruction_time_row.enabled = False


####################################################################################################
# @draw_mesh_rendering_buttons
####################################################################################################
def draw_mesh_rendering_buttons(panel, scene, show_stats=False):

    view_row = panel.layout.row()
    view_row.label(text='Render View', icon='RESTRICT_RENDER_OFF')
    buttons_row = panel.layout.row(align=True)
    buttons_row.operator('nmv.render_mesh_front', icon='AXIS_FRONT')
    buttons_row.operator('nmv.render_mesh_side', icon='AXIS_SIDE')
    buttons_row.operator('nmv.render_mesh_top', icon='AXIS_TOP')

    if nmv.interface.ui_mesh_reconstructed:
        view_row.enabled = True
        buttons_row.enabled = True
    else:
        view_row.enabled = False
        buttons_row.enabled = False


####################################################################################################
# @draw_mesh_export_options
####################################################################################################
def draw_mesh_export_options(panel, scene, options):

    # Saving meshes parameters
    save_neuron_mesh_row = panel.layout.row()
    save_neuron_mesh_row.label(text='Export Mesh', icon='MESH_UVSPHERE')

    export_format_row = panel.layout.row()
    export_format_row.prop(scene, 'NMV_ExportedMeshFormat', icon='GROUP_VERTEX')

    if not scene.NMV_ExportedMeshFormat == nmv.enums.Meshing.ExportFormat.BLEND:
        if scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
            export_individual_row = panel.layout.row()
            export_individual_row.prop(scene, 'NMV_ExportIndividuals')

    # Save button
    save_neuron_mesh_buttons_column = panel.layout.column(align=True)
    save_neuron_mesh_buttons_column.operator('nmv.export_mesh', icon='MESH_DATA')

    if nmv.interface.ui_mesh_reconstructed:
        export_format_row.enabled = True
        save_neuron_mesh_buttons_column.enabled = True
    else:
        export_format_row.enabled = False
        save_neuron_mesh_buttons_column.enabled = False

