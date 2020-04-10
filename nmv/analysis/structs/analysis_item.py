####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
                'NONE', 'LENGTH', 'AREA', 'VOLUME', 'ROTATION', 'TIME', 'VELOCITY', 'ACCELERATION'.
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

        # Append a little detail to the description to indicate if this is morphology or arbor
        if 'Morphology' in variable_prefix:
            description = '%s %s' % (self.description, 'of the entire morphology')
        elif 'Dendrite' in variable_prefix:
            description = '%s %s' % (self.description, 'of the dendrite')
        elif 'Axon' in variable_prefix:
            description = '%s %s' % (self.description, 'of the axon')
        else:
            description = 'None'

        # Float entry
        if self.data_format == 'FLOAT':
            setattr(bpy.types.Scene, '%s%s' % (variable_prefix, self.variable),
                    FloatProperty(name=self.name, description=description, subtype='FACTOR',
                                  min=0, max=1e32, precision=5))

        elif self.data_format == 'NEGATIVE_FLOAT':
            setattr(bpy.types.Scene, '%s%s' % (variable_prefix, self.variable),
                    FloatProperty(name=self.name, description=description, subtype='FACTOR',
                                  min=-1e5, max=1e32, precision=5))

        # Int entry
        elif self.data_format == 'INT':
            setattr(bpy.types.Scene, '%s%s' % (variable_prefix, self.variable),
                    IntProperty(name=self.name, description=description, subtype='FACTOR'))

        # Otherwise, ignore
        else:
            pass

    ################################################################################################
    # @register_global_analysis_variables
    ################################################################################################
    def register_global_analysis_variables(self,
                                           morphology):
        """Registers each global analysis variable in the group.

        :param morphology:
            A given morphology to analyze.
        """

        # Float entry
        if self.data_format == 'FLOAT':
            setattr(bpy.types.Scene, '%s' % self.variable,
                    FloatProperty(name=self.name, description=self.description, subtype='FACTOR',
                                  min=0, max=1e32, precision=5))

        elif self.data_format == 'NEGATIVE_FLOAT':
            setattr(bpy.types.Scene, '%s' % self.variable,
                    FloatProperty(name=self.name, description=self.description, subtype='FACTOR',
                                  min=-1e5, max=1e32, precision=5))

        # Int entry
        elif self.data_format == 'INT':
            setattr(bpy.types.Scene, '%s' % self.variable,
                    IntProperty(name=self.name, description=self.description, subtype='FACTOR'))

    ################################################################################################
    # @register_per_arbor_analysis_variables
    ################################################################################################
    def register_per_arbor_analysis_variables(self,
                                              morphology):
        """Registers each per-arbor analysis variable in the group.

        :param morphology:
            A given morphology to analyze.
        """

        # Morphology
        self.register_variable(variable_prefix='Morphology')

        # Apical dendrites
        if morphology.has_apical_dendrites():
            for i, arbor in enumerate(morphology.apical_dendrites):
                self.register_variable(variable_prefix=arbor.tag)

        # Basal dendrites
        if morphology.has_basal_dendrites():
            for i, arbor in enumerate(morphology.basal_dendrites):
                self.register_variable(variable_prefix=arbor.tag)

        # Axons
        if morphology.has_axons():
            for i, arbor in enumerate(morphology.axons):
                self.register_variable(variable_prefix=arbor.tag)

    ################################################################################################
    # @update_analysis_variable
    ################################################################################################
    def update_analysis_variable(self,
                                 prefix,
                                 result,
                                 context):
        """Updates each analysis variable in the group.

        :param prefix:
            The prefix 'in string format' that is used to tag or identify the analysis component.
        :param result:
            The final results that should be assigned to the variable.
        :param context:
            Blender context.
        """

        # Update the context, but make sure that the result is not None and the context exists
        if context is not None or result is not None:

            # Update the scene parameter
            setattr(context.scene, '%s%s' % (prefix, self.variable), result)

    ################################################################################################
    # @get_analysis_result_string
    ################################################################################################
    def get_analysis_result_string(self,
                                   prefix,
                                   result):
        """Returns a string that contains the result of the analysis.
        :param prefix:
            The prefix 'in string format' that is used to tag or identify the analysis component.
        :param result:
            The final results that should be assigned to the variable.
        :return:
            A string that contains the result of the analysis operation.
        """

        # Ensure that the result is not None
        if result is not None:

            # For the results string
            result_string = '\t* %s : %s' % (prefix, str(result))

            # Return the string
            return result_string

        # Otherwise, return None
        else:
            return None

    ################################################################################################
    # @update_analysis_variables
    ################################################################################################
    def update_analysis_variables(self,
                                  morphology,
                                  context):
        """Updates the analysis variables after the analysis is finished.

        :param morphology:
            A given morphology to analyze.
        :param context:
            Blender context.
        """

        # Morphology
        self.update_analysis_variable(
            prefix='Morphology', result=self.result.morphology_result, context=context)

        # Apical dendrites
        if morphology.has_apical_dendrites():
            for i, arbor in enumerate(morphology.apical_dendrites):

                # Get the apical dendrite result
                result = self.result.apical_dendrites_result[i]

                # Update the corresponding analysis variable
                self.update_analysis_variable(
                    prefix=arbor.tag, result=result, context=context)

        # Basal dendrites
        if morphology.has_basal_dendrites():
            for i, arbor in enumerate(morphology.basal_dendrites):

                # Get the result of this basal dendrite
                result = self.result.basal_dendrites_result[i]

                # Update the corresponding analysis variable
                self.update_analysis_variable(
                    prefix=arbor.tag, result=result, context=context)

        # Axons
        if morphology.has_axons():
            for i, arbor in enumerate(morphology.axons):

                # Get the axon result
                result = self.result.axons_result[i]

                # Update the corresponding analysis variable
                self.update_analysis_variable(
                    prefix=arbor.tag, result=result, context=context)

    ################################################################################################
    # @get_analysis_results_string
    ################################################################################################
    def get_analysis_results_string(self,
                                    morphology):
        """Gets the results of all the analysis in a string to get exported to a file.

        :param morphology:
            A given morphology to analyze.
        :return:
            A string with all the analysis results.
        """

        results_string = '- %s \n' % self.variable

        # Morphology
        results_string += self.get_analysis_result_string(
            prefix='Morphology', result=self.result.morphology_result) + '\n'

        # Apical dendrites
        if morphology.has_apical_dendrites():
            for i, arbor in enumerate(morphology.apical_dendrites):

                # Get the apical dendrite result
                result = self.result.apical_dendrites_result[i]
                results_string += self.get_analysis_result_string(
                    prefix=arbor.tag, result=result) + '\n'

        # Basal dendrites
        if morphology.has_basal_dendrites():
            for i, arbor in enumerate(morphology.basal_dendrites):

                # Get the result of this basal dendrite
                result = self.result.basal_dendrites_result[i]
                results_string += self.get_analysis_result_string(
                    prefix=arbor.tag, result=result) + '\n'

        # Axons
        if morphology.has_axons():
            for i, arbor in enumerate(morphology.axons):

                # Get the axon result
                result = self.result.axons_result[i]

                results_string += self.get_analysis_result_string(
                    prefix=arbor.tag, result=result) + '\n'

        # Return the final string
        return results_string

    ################################################################################################
    # @apply_per_arbor_analysis_kernel
    ################################################################################################
    def apply_per_arbor_analysis_kernel(self,
                                        morphology,
                                        context):
        """Applies the analysis kernels 'per-arbor' on the entire morphology.

        :param morphology:
            A given morphology to analyze.
        :param context:
            Blender context for the results to appear in the user interface.
        """

        if self.kernel is not None:

            # Get the result from applying the kernel on the entire morphology skeleton
            self.result = self.kernel(morphology)

            # Update the variables
            if context is not None:
                self.update_analysis_variables(morphology=morphology, context=context)

    ################################################################################################
    # @apply_global_analysis_kernel
    ################################################################################################
    def apply_global_analysis_kernel(self,
                                     morphology,
                                     context):
        """Applies the global analysis kernels and updates the results.

        :param morphology:
            A given morphology to analyze.
        :param context:
            Blender context for the results to appear in the user interface.
        """

        if self.kernel is not None:

            # Get the result from applying the kernel on the entire morphology skeleton
            self.result = self.kernel(morphology)

            # Update the variables
            if context is not None:
                setattr(context.scene, '%s' % self.variable, self.result)

    ################################################################################################
    # @write_analysis_results_to_string
    ################################################################################################
    def write_analysis_results_to_string(self,
                                         morphology):
        """Applies the analysis kernels on the entire morphology.

        :param morphology:
            A given morphology to analyze.
        """

        # Analysis results
        analysis_results_string = ''

        # Ensure that there is a valid kernel
        if self.kernel is not None:

            # Get the result from applying the kernel on the entire morphology skeleton
            self.result = self.kernel(morphology)

            # Get the analysis results string
            analysis_results_string += '%s \n' % self.get_analysis_results_string(morphology)

        # Return the string
        return analysis_results_string
