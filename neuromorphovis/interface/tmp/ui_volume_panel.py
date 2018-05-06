"""ui_volume_panel.py:
    The panel that has the volume generation tools.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2017, Blue Brain Project / EPFL"
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


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
    bl_context = 'objectmode'
    bl_category = 'NeuroMorphoVis'

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
