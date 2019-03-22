####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
import nmv
import nmv.enums
import nmv.interface
import nmv.utilities

nmv_icons = None


####################################################################################################
# @IOPanel
####################################################################################################
class AboutPanel(bpy.types.Panel):
    """NMV About Us panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
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
        credits_column.label(text='Copyrights')
        credits_column.label(text='Blue Brain Project (BBP)',
                             icon_value=nmv.interface.ui_icons['bbp'].icon_id)
        credits_column.label(text='Ecole Polytechnique Federale de Lausanne (EPFL)',
                             icon_value=nmv.interface.ui_icons['epfl'].icon_id)
        credits_column.separator()

        credits_column.label(text='Main Author')
        credits_column.label(text='Marwan Abdellah', icon='OUTLINER_DATA_ARMATURE')
        credits_column.separator()
        credits_column.label(text='Credits')
        credits_column.label(text='Juan Hernando', icon='OUTLINER_DATA_POSE')
        credits_column.label(text='Ahmet Bilgili', icon='OUTLINER_DATA_POSE')
        credits_column.label(text='Stefan Eilemann', icon='OUTLINER_DATA_POSE')
        credits_column.label(text='Henry Markram', icon='OUTLINER_DATA_POSE')
        credits_column.label(text='Felix Shuermann', icon='OUTLINER_DATA_POSE')
        credits_column.separator()

        # Version
        version_column = layout.column()
        version = nmv.utilities.get_nmv_version()
        version_column.label(text='Version: %d.%d.%d' % (version[0], version[1], version[2]))

        update_button = layout.column()
        update_button.operator('update.nmv', emboss=True,
                               icon_value=nmv.interface.ui_icons['github'].icon_id)


####################################################################################################
# @UpdateNeuroMorphoVis
####################################################################################################
class UpdateNeuroMorphoVis(bpy.types.Operator):
    """Update NeuroMorphoVis"""

    # Operator parameters
    bl_idname = "update.nmv"
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

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Panel
    bpy.utils.register_class(AboutPanel)

    # Buttons
    bpy.utils.register_class(UpdateNeuroMorphoVis)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Panel
    bpy.utils.unregister_class(AboutPanel)

    # Buttons
    bpy.utils.unregister_class(UpdateNeuroMorphoVis)
