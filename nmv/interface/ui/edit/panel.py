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
import nmv.interface
from .layout_props import *


####################################################################################################
# @NMV_EditPanel
####################################################################################################
class NMV_EditPanel(bpy.types.Panel):
    """Edit panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_idname = "OBJECT_PT_NMV_MorphologyEditing"
    bl_label = 'Morphology Editing'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    # Register a variable that indicates that the morphology is sketched to be able to update the UI
    bpy.types.Scene.NMV_MorphologySketched = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.NMV_MorphologyCoordinatesEdited = bpy.props.BoolProperty(default=False)

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):

        # Draw the documentation button
        draw_documentation_button(layout=self.layout)
        self.layout.separator()

        # Draw the morphology sketching button if the edit mode is not activated
        if not nmv.interface.ui_in_edit_mode:
            draw_sketch_skeleton_button(layout=self.layout)
            self.layout.separator()

        # If the skeleton is not being edited, draw the edit button, otherwise the update one
        if not nmv.interface.ui_is_skeleton_edited:
            draw_edit_skeleton_button(layout=self.layout)
            self.layout.separator()
        else:
            draw_update_skeleton_button(layout=self.layout)
            self.layout.separator()

        # Draw the morphology export button(s)
        if not nmv.interface.ui_in_edit_mode:
            draw_morphology_export_button(layout=self.layout)
            self.layout.separator()

        # Enable or disable the layout
        nmv.interface.enable_or_disable_layout(self.layout)
