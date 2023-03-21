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
import nmv.utilities


####################################################################################################
# @NMV_AboutPanel
####################################################################################################
class NMV_AboutPanel(bpy.types.Panel):
    """NMV About panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_idname = "OBJECT_PT_NMV_About"
    bl_label = 'About'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):

        # Credits
        credits_column = self.layout.column()
        credits_column.label(text='Copyrights (c)')
        credits_column.label(text='Blue Brain Project (BBP)', icon='PMARKER')
        credits_column.label(text='École Polytechnique Fédérale de Lausanne (EPFL)', icon='PMARKER')
        credits_column.separator()

        credits_column.label(text='License')
        credits_column.label(text='GPL 3.0', icon='UNLOCKED')
        credits_column.separator()

        credits_column.label(text='Main Author')
        credits_column.label(text='Marwan Abdellah', icon='OUTLINER_DATA_ARMATURE')
        credits_column.separator()
        credits_column.label(text='Credits')
        credits_column.label(text='Juan Hernando', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Caitlin Monney', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Nadir Roman', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Alessandro Foni', icon='OUTLINER_DATA_ARMATURE')

        credits_column.separator()
        credits_column.label(text='Advisors')
        credits_column.label(text='Ahmet Bilgili', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Stefan Eilemann', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Henry Markram', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Felix Schürmann', icon='OUTLINER_DATA_ARMATURE')
        credits_column.separator()
        credits_column.label(text='Acknowledgements')
        credits_column.label(text='Pawel Podhajski', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Danny Dyer', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Alan Garner', icon='OUTLINER_DATA_ARMATURE')
        credits_column.separator()

        # Version
        version_column = self.layout.column()
        version = nmv.utilities.get_nmv_version()
        version_column.label(text='Version: %d.%d.%d' % (version[0], version[1], version[2]))

        update_button = self.layout.column()
        update_button.operator('nmv.update', emboss=True, icon='NODETREE')
        update_button.operator('nmv.open_github', emboss=True, icon='SCRIPT')
        update_button.operator('nmv.open_wiki', emboss=True, icon='URL')




