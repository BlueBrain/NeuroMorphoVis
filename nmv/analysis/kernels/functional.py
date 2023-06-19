####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Internal imports
import nmv.analysis


####################################################################################################
# @apply_analysis_operation_to_arbor
####################################################################################################
def apply_analysis_operation_to_arbor(*args):
    """Apply a given function/filter/operation to a given arbor recursively.

    :param args:
        Arguments list, where the first argument is always the root section of the arbor and the
        second argument is the function of the operation/filter that will be applied
        and the rest of the arguments are those that will be passed to the function itself.
    """

    # The section is the first argument
    section = args[0]

    # If the section is None
    if section is None:

        # Simply return
        return

    # The operation is the second argument
    operation = args[1]

    # Construct the root section arguments list, add the section and ignore the operation
    section_args = [section]
    for i in range(2, len(args)):
        section_args.append(args[i])

    # Apply the operation/filter to the first section of the arbor
    operation(*section_args)

    # Ensure that the section has valid children
    if section.children is not None:

        # Apply the operation/filter to the children of the arbors
        for child in section.children:

            # Construct the child section arguments list, add the child and add the operation
            section_args = [child]
            for i in range(1, len(args)):
                section_args.append(args[i])

            # Validate the rest of the skeleton of the arbor
            apply_analysis_operation_to_arbor(*section_args)


####################################################################################################
# @apply_kernel_to_morphology_to_collect_distributions
####################################################################################################
def apply_kernel_to_morphology_to_collect_distributions(*args):

    # A structure to contain the analysis results of the entire morphology
    analysis_result = nmv.analysis.MorphologyAnalysisResult()

    # The morphology is the first argument
    morphology = args[0]

    # The kernel (or analysis function) is the second argument
    kernel = args[1]

    # Apical dendrite, if any
    if morphology.has_apical_dendrites():

        # Create an empty list to collect the analysis data
        analysis_result.apical_dendrites_result = list()

        # Dendrite by dendrite
        for arbor in morphology.apical_dendrites:

            # Construct arbor arguments list, not that the arbor is the first argument in the list
            arbor_args = [arbor]
            for i in range(2, len(args)):
                arbor_args.append(args[i])

            # Apply the kernel to the arbor and append the result
            analysis_result.apical_dendrites_result.extend(kernel(*arbor_args))

    # Basal dendrites
    if morphology.has_basal_dendrites():

        # Create an empty list to collect the resulting data
        analysis_result.basal_dendrites_result = list()

        # Dendrite by dendrite
        for arbor in morphology.basal_dendrites:

            # Construct arbor arguments list, not that the arbor is the first argument in the list
            arbor_args = [arbor]
            for i in range(2, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            analysis_result.basal_dendrites_result.extend(kernel(*arbor_args))

    # Axons
    if morphology.has_axons():

        # Create an empty list to collect the resulting data
        analysis_result.axons_result = list()

        # Axon by axon, if any
        for arbor in morphology.axons:

            # Construct arbor arguments list, not that the arbor is the first argument in the list
            arbor_args = [arbor]
            for i in range(2, len(args)):
                arbor_args.append(args[i])

            # Apply the kernel to the arbor
            analysis_result.axons_result.extend(kernel(*arbor_args))

    # Return the structure that contains the analysis result
    return analysis_result


####################################################################################################
# @apply_analysis_operation_to_morphology
####################################################################################################
def apply_analysis_operation_to_morphology(*args):
    """Apply a given function/filter/operation to a given morphology object including all of its
    arbors recursively.

    :param args:
        Arguments list, where the first argument is always the morphology and the second argument
        is the function of the operation/filter that will be applied and the rest of the arguments
        are those that will be passed to the function.
    """

    # A structure to contain the analysis results of the entire morphology
    analysis_result = nmv.analysis.MorphologyAnalysisResult()

    # The morphology is the first argument
    morphology = args[0]

    # The analysis function (or kernel) is the second argument
    analysis_function = args[1]

    # Apical dendrite
    if morphology.has_apical_dendrites():

        # Create an empty list to collect the resulting data
        analysis_result.apical_dendrites_result = list()

        # Dendrite by dendrite
        for arbor in morphology.apical_dendrites:

            # Construct arbor arguments list
            arbor_args = [arbor]
            for i in range(2, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            analysis_result.apical_dendrites_result.append(analysis_function(*arbor_args))

    # Basal dendrites
    if morphology.has_basal_dendrites():

        # Create an empty list to collect the resulting data
        analysis_result.basal_dendrites_result = list()

        # Dendrite by dendrite
        for arbor in morphology.basal_dendrites:

            # Construct arbor arguments list
            arbor_args = [arbor]
            for i in range(2, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            analysis_result.basal_dendrites_result.append(analysis_function(*arbor_args))

    # Axons
    if morphology.has_axons():

        # Create an empty list to collect the resulting data
        analysis_result.axons_result = list()

        # Dendrite by dendrite
        for arbor in morphology.axons:

            # Construct arbor arguments list
            arbor_args = [arbor]
            for i in range(2, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            analysis_result.axons_result.append(analysis_function(*arbor_args))

    # Return the structure that contains the analysis result
    return analysis_result
