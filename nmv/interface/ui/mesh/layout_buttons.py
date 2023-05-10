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

    # Mesh quick reconstruction options
    row = panel.layout.row()
    row.label(text='Quick Reconstruction', icon='PARTICLE_POINT')

    # Mesh reconstruction options
    row = panel.layout.row()
    row.operator('nmv.reconstruct_mesh', icon='MESH_DATA')

    if nmv.interface.ui_mesh_reconstructed:
        row = panel.layout.row()
        row.prop(scene, 'NMV_MeshReconstructionTime')
        row.enabled = False


####################################################################################################
# @draw_mesh_rendering_buttons
####################################################################################################
def draw_mesh_rendering_buttons(panel):

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
# @draw_export_components_option
####################################################################################################
def draw_export_components_option(panel, scene, options):

    # The objects must be disconnected
    if options.mesh.neuron_objects_connection == nmv.enums.Meshing.ObjectsConnection.DISCONNECTED:

        # It does work only with OBJ files
        if scene.NMV_ExportedMeshFormat == nmv.enums.Meshing.ExportFormat.OBJ:

            # Only for the piecewise-watertight and skinning-based meshing
            if scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT or \
               scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.SKINNING:
                export_individual_row = panel.layout.row()
                export_individual_row.prop(scene, 'NMV_ExportIndividuals')


####################################################################################################
# @draw_mesh_export_options
####################################################################################################
def draw_mesh_export_options(panel, scene, options):

    # Mesh export
    save_neuron_mesh_row = panel.layout.row()
    save_neuron_mesh_row.label(text='Export Mesh', icon='MESH_UVSPHERE')

    export_format_row = panel.layout.row()
    export_format_row.prop(scene, 'NMV_ExportedMeshFormat', icon='GROUP_VERTEX')

    # Display the export components option
    draw_export_components_option(panel=panel, scene=scene, options=options)

    # Save button
    save_neuron_mesh_buttons_column = panel.layout.column(align=True)
    save_neuron_mesh_buttons_column.operator('nmv.export_mesh', icon='MESH_DATA')

    if nmv.interface.ui_mesh_reconstructed:
        export_format_row.enabled = True
        save_neuron_mesh_buttons_column.enabled = True
    else:
        export_format_row.enabled = False
        save_neuron_mesh_buttons_column.enabled = False

