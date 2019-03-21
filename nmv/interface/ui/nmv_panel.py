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


####################################################################################################
# @IOPanel
####################################################################################################
class NMVPanel(bpy.types.Panel):
    """NMV header panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'NeuroMorphoVis'
    bl_category = 'NeuroMorphoVis'
    bl_options = {"HIDE_HEADER"}

    ################################################################################################
    # Panel parameters
    ################################################################################################
    def draw(self, context):
        """Draws the panel.

        :param context:
            Context
        """
        pass


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Panel
    bpy.utils.register_class(NMVPanel)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Panel
    bpy.utils.unregister_class(NMVPanel)
