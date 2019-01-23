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

# Blender imports
import bpy
from mathutils import Vector
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import FloatVectorProperty

import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.analysis
import neuromorphovis.repair
import neuromorphovis.enums
import neuromorphovis.file
import neuromorphovis.interface
import neuromorphovis.skeleton


# Morphology repairing object
morphology_repairer = None


####################################################################################################
# @RepairPanel
####################################################################################################
class RepairPanel(bpy.types.Panel):
    """Repair panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Morphology Repair'
    bl_context = 'objectmode'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    # Register a variable that indicates that the morphology is analyzed to be able to update the UI
    bpy.types.Scene.MorphologyAnalyzed = BoolProperty(default=False)

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel

        :param context:
            Rendering context
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Morphology analysis button
        repair_morphology_column = layout.column(align=True)
        repair_morphology_column.operator('repair.morphology', icon='MESH_DATA')


####################################################################################################
# @RepairMorphology
####################################################################################################
class RepairMorphology(bpy.types.Operator):
    """Repair the morphology skeleton, detect the artifacts and fix them"""

    # Operator parameters
    bl_idname = "repair.morphology"
    bl_label = "Repair Morphology"

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

        """
        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        nmv.logger.log(context.scene.OutputDirectory)
        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the analysis directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.analysis_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.analysis_directory)
        """

        # Load the morphology file
        nmv.interface.ui.load_morphology(self, context.scene)

        # Create an object of the repairer
        global morphology_repairer
        morphology_repairer = nmv.repair.MorphologyRepairer(
            morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Create the morphological skeleton
        morphology_repairer.create_morphological_skeleton()

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.register_class(RepairPanel)

    # Morphology analysis button
    bpy.utils.register_class(RepairMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.unregister_class(RepairPanel)

    # Morphology analysis button
    bpy.utils.unregister_class(RepairMorphology)
