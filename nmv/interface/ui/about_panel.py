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
from bpy.props import EnumProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty

# Internal imports
import nmv
import nmv.enums
import nmv.interface


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
    bl_label = 'About NeuroMorphoVis'
    bl_category = 'NeuroMorphoVis'
    bl_nmv_version = (1, 3, 0)

    ################################################################################################
    # Panel options
    ################################################################################################


    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """Draw the panel.

        :param context:
            Panel context.
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Get a reference to the scene
        scene = context.scene

        # Input data options
        input_data_options_row = layout.row()
        input_data_options_row.label(text='About Us:', icon='LIBRARY_DATA_DIRECT')

        # Export analysis button
        export_analysis_row = layout.row()
        export_analysis_row.operator('update.nmv', icon='MESH_DATA')


####################################################################################################
# @UpdateNeuroMorphoVis
####################################################################################################
class UpdateNeuroMorphoVis(bpy.types.Operator):
    """Update NeuroMorphoVis button"""

    # Operator parameters
    bl_idname = "update.nmv"
    bl_label = "Update NeuroMorphoVis"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Rendering context
        :return:
            'FINISHED'
        """

        print(AboutPanel.bl_nmv_version)
        print(sys.platform)

        # Get the current path
        current_path = os.path.dirname(os.path.realpath(__file__))

        # Go to the main directory and pull the latest master
        os.chdir(current_path)
        shell_command = 'git pull origin union'
        nmv.logger.log('Updating NeuroMorphoVis')
        subprocess.call(shell_command, shell=True)

        # Get the blender path from the current path, NOTE the differences on different OSes
        if 'darwin' in sys.platform:
            blender_executable = '%s/../../../../../../../../MacOS/blender' % current_path
        elif 'linux' in sys.platform:
            blender_executable = '%s/../../../../../../../blender' % current_path
        elif 'win' in sys.platform or 'Win' in sys.platform:
            blender_executable = '%s/../../../../../../../blender.exe' % current_path
        else:
            nmv.logger.info('Error: Unknown Platform!')
            exit(0)

        # Call blender and exit this one
        shell_command = '%s &' % blender_executable
        nmv.logger.log('Restarting Blender')
        subprocess.call(shell_command, shell=True)
        exit(0)

        #
        #shell_command = 'git clone https://github.com/BlueBrain/NeuroMorphoVis.git /home/abdellah/Desktop/data/'
        #subprocess.call(shell_command, shell=True)


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
