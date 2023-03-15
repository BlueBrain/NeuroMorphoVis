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
    layout.separator()


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

    layout.separator()


####################################################################################################
# draw_export_options
####################################################################################################
def draw_export_options(layout):

    # Saving morphology options
    row = layout.row()
    row.label(text='Export Morphology', icon='MESH_UVSPHERE')

    row = layout.column(align=True)
    row.operator('nmv.save_morphology_blend', icon='OUTLINER_OB_META')
    row.operator('nmv.save_morphology_swc', icon='GROUP_VERTEX')
    row.operator('nmv.save_morphology_segments', icon='GROUP_VERTEX')
    row.enabled = True
    layout.separator()

