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
from bpy.props import IntProperty
from bpy.props import FloatProperty


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
                 filter_function=None,
                 description='',
                 data_format='FLOAT',
                 unit='NONE'):
        """Constructor

        :param variable:
            The name of the variable name of the analysis entry. This entry can be then updated from
            Blender by changing context.scene.[the variable]
        :param name:
            The name of the entry as appears in the GUI.
        :param filter_function:
            The filter function that will be applied on the arbor when the morphology is analyzed.
        :param description:
            A little description of the entry to appear as a tooltip in the GUI.
        :param data_format:
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
        self.filter_function = filter_function

        # Entry description
        self.description = description

        # Entry format
        self.data_format = data_format

        # Entry unit
        self.unit = unit

        # Filter result
        self.result = None

    ################################################################################################
    # @create_blender_entry
    ################################################################################################
    def register_ui_entry(self,
                          arbor_prefix):
        """Registers this entry for this analysis item in Blender and add it to the UI.
        
        :param arbor_prefix:
             The prefix 'in string format' that is used to tag or identify the arbor.
        """

        # Float entry
        if self.data_format == 'FLOAT':
            setattr(bpy.types.Scene, '%s%s' % (arbor_prefix, self.variable),
                    FloatProperty(name=self.name, description=self.description, unit=self.unit))

        # Int entry
        elif self.data_format == 'INT':
            setattr(bpy.types.Scene, '%s%s' % (arbor_prefix, self.variable),
                    IntProperty(name=self.name, description=self.description))

    ################################################################################################
    # @apply_filter
    ################################################################################################
    def apply_filter(self,
                     arbor,
                     arbor_prefix,
                     context=None):
        """Applies the analysis filter to the given arbor and update the corresponding
        scene parameter.

        :param arbor:
            A given arbor to get the filter applied on it.
        :param arbor_prefix:
            The prefix 'in string format' that is used to tag or identify the arbor.
        :param context:
            Blender context.
        """

        # Get the result
        self.result = self.filter_function(arbor)

        # Update the context, but make sure that the result is not None and the context exists
        if context is not None or self.result is not None:

            # Update the scene parameter
            setattr(context.scene, '%s%s' % (arbor_prefix, self.variable), self.result)

    ################################################################################################
    # @apply_filter_and_return_result
    ################################################################################################
    def apply_filter_and_return_result(self,
                                       arbor):
        """Applies the filter and then returns the result corresponding to the filter.

        :param arbor:
            A given arbor to get the filter applied to it.
        :return:
            The results of applying the filter function on the arbor.
        """

        # Apply the filter
        return self.apply_filter(arbor)

    ################################################################################################
    # @update_ui_entry
    ################################################################################################
    def update_ui_entry(self,
                        arbor_prefix,
                        ui_layout,
                        context):
        """Updates the UI entry that corresponds to the filter.

        :param arbor_prefix:
            The prefix 'in string format' that is used to tag or identify the arbor.
        :param ui_layout:
            The layout of the panel in the UI.
        :param context:
            The UI context from the panel.
        """

        # Update the corresponding UI layout
        ui_layout.prop(context.scene, '%s%s' % (arbor_prefix, self.variable))

