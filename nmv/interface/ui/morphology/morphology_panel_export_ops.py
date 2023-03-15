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
# set_export_options
####################################################################################################
def set_export_options(layout, scene, options):

    # Saving morphology options
    save_morphology_row = layout.row()
    save_morphology_row.label(text='Save Morphology As:', icon='MESH_UVSPHERE')

    # Saving morphology buttons
    save_morphology_buttons_column = layout.column(align=True)
    save_morphology_buttons_column.operator('nmv.save_morphology_blend', icon='OUTLINER_OB_META')
    save_morphology_buttons_column.operator('nmv.save_morphology_swc', icon='GROUP_VERTEX')
    save_morphology_buttons_column.operator('nmv.save_morphology_segments', icon='GROUP_VERTEX')
    save_morphology_buttons_column.enabled = True
