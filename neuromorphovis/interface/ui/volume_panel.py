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
import sys, os

# Blender imports
import bpy
from mathutils import Vector
from bpy.props import (IntProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty,
                       FloatVectorProperty)


####################################################################################################
# @VolumeOptions
####################################################################################################
class VolumeOptions(bpy.types.Panel):
    """Volume options"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Volume Reconstruction Options'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """
        Draws the panel.

        :param context: Panel context.
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Get a reference to the scene
        scene = context.scene


        create_neuron_volume_column = layout.column(align=True)
        create_neuron_volume_column.operator('create_neuron.volume', icon='MESH_DATA')


####################################################################################################
# @SaveSomaMeshBlend
####################################################################################################
class CreateNeuronVolume(bpy.types.Operator):
    """Create a volume for the entire neuron"""

    # Operator parameters
    bl_idname = "create_neuron.volume"
    bl_label = "Create Neuron Volume"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """
        Executes the operator.

        :param context: Operator context.
        :return: {'FINISHED'}
        """


        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """
    Registers all the classes in this panel.
    """

    # Soma reconstruction panel
    bpy.utils.register_class(VolumeOptions)

    bpy.utils.register_class(CreateNeuronVolume)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """
    Un-registers all the classes in this panel.
    """

    # Soma reconstruction panel
    bpy.utils.unregister_class(VolumeOptions)


    bpy.utils.unregister_class(CreateNeuronVolume)
