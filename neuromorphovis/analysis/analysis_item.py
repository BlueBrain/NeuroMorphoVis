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
                 kernel=None,
                 description='',
                 data_format='FLOAT',
                 unit='NONE'):
        """Constructor

        :param variable:
            The name of the variable name of the analysis item. This entry can be then updated from
            Blender by changing context.scene.[variable].
        :param name:
            The name of the entry as appears in the GUI.
        :param kernel:
            The kernel function that will be applied on the morphology when analyzed.
        :param description:
            A little description of the entry to appear as a tooltip in the GUI.
        :param data_format:
            The format of the entry. This could be one of the following options:
                'INT', 'FLOAT'.
        :param unit:
            The unit of the entry. This could be one of the following options:
                ‘NONE’, ‘LENGTH’, ‘AREA’, ‘VOLUME’, ‘ROTATION’, ‘TIME’, ‘VELOCITY’, ‘ACCELERATION’.
        """

        # Scene variable for registration
        self.variable = variable

        # Entry name
        self.name = name

        # Analysis filter
        self.kernel = kernel

        # Entry description
        self.description = description

        # Entry format
        self.data_format = data_format

        # Entry unit
        self.unit = unit

        # Analysis result for the entire morphology of type @MorphologyAnalysisResult
        self.result = None

    ################################################################################################
    # @register_variable
    ################################################################################################
    def register_variable(self,
                          variable_prefix):
        """Registers this entry for this analysis item in Blender and add it to the UI.

        :param variable_prefix:
             The prefix 'in string format' that is used to tag or identify the analysis component.
        """

        # Float entry
        if self.data_format == 'FLOAT':
            setattr(bpy.types.Scene, '%s%s' % (variable_prefix, self.variable),
                    FloatProperty(name=self.name, description=self.description, subtype='FACTOR',
                                  min=0, max=1e32, precision=5))

        # Int entry
        elif self.data_format == 'INT':
            setattr(bpy.types.Scene, '%s%s' % (variable_prefix, self.variable),
                    IntProperty(name=self.name, description=self.description, subtype='FACTOR'))

    ################################################################################################
    # @register_morphology_variables
    ################################################################################################
    def register_analysis_variables(self,
                                      morphology):

        # Apical dendrite
        if morphology.apical_dendrite is not None:
            self.register_variable(variable_prefix=morphology.apical_dendrite.get_type_prefix())

        # Basal dendrites
        if morphology.dendrites is not None:

            # For each basal dendrite
            for i, basal_dendrite in enumerate(morphology.dendrites):
                self.register_variable(
                    variable_prefix='%s%i' % (basal_dendrite.get_type_prefix(), i))

        # Axon
        if morphology.axon is not None:
            self.register_variable(variable_prefix=morphology.axon.get_type_prefix())

    ################################################################################################
    # @update_analysis_variable
    ################################################################################################
    def update_analysis_variable(self,
                                 arbor,
                                 result,
                                 context):
        """

        :param arbor:
        :param result:
        :param context:
        :return:
        """

        # Update the context, but make sure that the result is not None and the context exists
        if context is not None or result is not None:

            # Update the scene parameter
            setattr(context.scene, '%s%s' % (arbor.get_type_prefix(), self.variable), result)

    ################################################################################################
    # @update_analysis_variables
    ################################################################################################
    def update_analysis_variables(self,
                                  morphology,
                                  context):
        """

        :param morphology:
        :param context:
        :return:
        """

        # Apical dendrite
        if morphology.apical_dendrite is not None:

            # Get the apical dendrite result
            result = self.result.apical_dendrite_result

            # Update the corresponding analysis variable
            self.update_analysis_variable(
                arbor=morphology.apical_dendrite, result=result, context=context)

        # Basal dendrites
        if morphology.dendrites is not None:

            # For each basal dendrite
            for i, basal_dendrite in enumerate(morphology.dendrites):

                # Get the result of this basal dendrite
                result = self.result.basal_dendrites_result[i]

                # Update the corresponding analysis variable
                self.update_analysis_variable(arbor=basal_dendrite, result=result, context=context)

        # Axon
        if morphology.axon is not None:

            # Get the axon result
            result = self.result.axon_result

            # Update the corresponding analysis variable
            self.update_analysis_variable(
                arbor=morphology.axon, result=result, context=context)

    ################################################################################################
    # @apply_analysis_kernel
    ################################################################################################
    def apply_analysis_kernel(self,
                              morphology,
                              context):

        # Get the result
        self.result = self.kernel(morphology)

        # Update the variables
        self.update_analysis_variables(morphology=morphology, context=context)