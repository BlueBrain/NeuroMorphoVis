####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import os
import subprocess

# Blender imports
import bpy

# Internal imports
import nmv.utilities


####################################################################################################
# @NMV_Update
####################################################################################################
class NMV_Update(bpy.types.Operator):
    """Update NeuroMorphoVis and pull the latest changes to the master branch on GitHub"""

    # Operator parameters
    bl_idname = "nmv.update"
    bl_label = "Update"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # git must be installed to update the tool.
        if not nmv.utilities.command_exists('git'):
            self.report({'INFO'}, 'Cannot update NeuroMorphoVis! git must be installed.')
            return {'FINISHED'}

        if 'posix' in os.name:
            nmv.logger.log('Updating NeuroMorphoVis on a unix-based OS')
        else:
            self.report({'ERROR'}, 'Cannot update NeuroMorphoVis on Windows! '
                                   'Please download the latest version from the GitHub '
                                   'Release page.')
            return {'FINISHED'}

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
# @NMV_OpenDocumentation
####################################################################################################
class NMV_OpenDocumentation(bpy.types.Operator):
    """Open the documentation page on GitHub"""

    # Operator parameters
    bl_idname = "nmv.open_wiki"
    bl_label = "Documentation"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        try:
            import webbrowser
            webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis/wiki')
            return {'FINISHED'}
        except ImportError:
            self.report({'ERROR'}, 'The package webbrowser must be installed!')
            return {'FINISHED'}


####################################################################################################
# @NMV_OpenRepository
####################################################################################################
class NMV_OpenRepository(bpy.types.Operator):
    """Open the GitHub repository page"""

    # Operator parameters
    bl_idname = "nmv.open_github"
    bl_label = "Code"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis')
        return {'FINISHED'}

