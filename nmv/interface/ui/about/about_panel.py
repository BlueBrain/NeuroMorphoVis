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

# System imports
import sys
import os
import subprocess

# Blender imports
import bpy
import bpy.utils.previews

# Internal imports
import nmv.enums
import nmv.interface
import nmv.utilities

nmv_icons = None


####################################################################################################
# @IOPanel
####################################################################################################
class NMV_AboutPanel(bpy.types.Panel):
    """NMV About Us panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if nmv.utilities.is_blender_280() else 'TOOLS'
    bl_idname = "OBJECT_PT_NMV_About"
    bl_label = 'About'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel.

        :param context:
            Blender context.
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Credits
        credits_column = layout.column()
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
        version_column = layout.column()
        version = nmv.utilities.get_nmv_version()
        version_column.label(text='Version: %d.%d.%d' % (version[0], version[1], version[2]))

        update_button = layout.column()
        update_button.operator('nmv.update', emboss=True, icon='NODETREE')
        update_button.operator('nmv.open_github', emboss=True, icon='SCRIPT')
        update_button.operator('nmv.open_wiki', emboss=True, icon='URL')


####################################################################################################
# @OpenDocumentation
####################################################################################################
class NMV_OpenDocumentation(bpy.types.Operator):
    """Open the GitHub repository page"""

    # Operator parameters
    bl_idname = "nmv.open_wiki"
    bl_label = "Documentation"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis/wiki')
        return {'FINISHED'}


####################################################################################################
# @OpenRepository
####################################################################################################
class NMV_OpenRepository(bpy.types.Operator):
    """Open the GitHub repository page"""

    # Operator parameters
    bl_idname = "nmv.open_github"
    bl_label = "Code"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis')
        return {'FINISHED'}


####################################################################################################
# @UpdateNeuroMorphoVis
####################################################################################################
class NMV_Update(bpy.types.Operator):
    """Update NeuroMorphoVis"""

    # Operator parameters
    bl_idname = "nmv.update"
    bl_label = "Update"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        # git must be installed to update the tool.
        if not nmv.utilities.command_exists('git'):
            self.report({'INFO'}, 'Cannot update NeuroMorphoVis! git must be installed.')
            return {'FINISHED'}

        # TODO: Verify git or use wget or curl.
        # TODO: Ignore this option for windows.

        # Get the current path
        current_path = os.path.dirname(os.path.realpath(__file__))

        # Go to the main directory and pull the latest master
        os.chdir(current_path)
        shell_command = 'git pull origin master'
        nmv.logger.log('Updating NeuroMorphoVis ...')
        subprocess.call(shell_command, shell=True)

        # Call blender and exit this one
        shell_command = '%s &' % bpy.app.binary_path
        nmv.logger.log('Restarting Blender with NeuroMorphoVis ...')
        subprocess.call(shell_command, shell=True)

        # Exiting blender
        exit(0)


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Panel
    bpy.utils.register_class(NMV_AboutPanel)

    # Buttons
    bpy.utils.register_class(NMV_Update)
    bpy.utils.register_class(NMV_OpenRepository)
    bpy.utils.register_class(NMV_OpenDocumentation)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Panel
    bpy.utils.unregister_class(NMV_AboutPanel)

    # Buttons
    bpy.utils.unregister_class(NMV_Update)
    bpy.utils.unregister_class(NMV_OpenRepository)
    bpy.utils.unregister_class(NMV_OpenDocumentation)
