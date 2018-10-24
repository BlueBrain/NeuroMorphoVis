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


####################################################################################################
# AnalysisItem
####################################################################################################
class AnalysisItem:
    """Each analysis item will appear in the UI and will be registered into Blender with a specific
    variable name. This class encapsulates the parameters of each entry.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 variable,
                 name,
                 filter=None,
                 description='',
                 format='FLOAT',
                 unit='NONE'):
        """Constructor

        :param variable:
            The name of the variable name of the analysis entry. This entry can be then updated from
            Blender by changing context.scene.[the variable]
        :param name:
            The name of the entry as appears in the GUI.
        :param filter:
            The filter function that will be applied on the arbor when the morphology is analyzed.
        :param description:
            A little description of the entry to appear as a tooltip in the GUI.
        :param format:
            The format of the entry. This could be one of the following options:
            'INT', 'FLOAT'
        :param unit:
            The unit of the entry. This could be one of the following options:
            ‘NONE’, ‘LENGTH’, ‘AREA’, ‘VOLUME’, ‘ROTATION’, ‘TIME’, ‘VELOCITY’, ‘ACCELERATION’
        """

        # Scene variable for registration
        self.variable = variable

        # Entry name
        self.name = name

        # Analysis filter
        self.filter = filter

        # Entry description
        self.description = description

        # Entry format
        self.format = format

        # Entry unit
        self.unit = unit

        # Filter result
        self.result = None

    ################################################################################################
    # @create_blender_entry
    ################################################################################################
    def register_ui_entry(self,
                          neurite):
        """Registers this entry for this analysis item in Blender and add it to the UI.
        
        :param neurite:
            A specific neurite.
        """

        # Float entry
        if self.format == 'FLOAT':
            setattr(bpy.types.Scene, '%s%s' % (str(neurite), self.variable),
                    FloatProperty(name=self.name, description=self.description, unit=self.unit))

        # Int entry
        elif self.format == 'INT':
            setattr(bpy.types.Scene, '%s%s' % (str(neurite), self.variable),
                    IntProperty(name=self.name, description=self.description))

    ################################################################################################
    # @apply_filter
    ################################################################################################
    def apply_filter(self,
                     neurite,
                     context):

        # Get the result
        self.result = self.filter(neurite)

        # Update the user interface
        setattr(context.scene, '%s%s' % ('Axon', self.variable), self.result)

