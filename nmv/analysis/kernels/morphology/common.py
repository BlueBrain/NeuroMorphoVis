####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
# @get_morphology_maximum_branching_order_from_analysis_results
####################################################################################################
def get_morphology_maximum_branching_order_from_analysis_results(analysis_result):
    """Computes the maximum branching order of the morphology based on the actual computed
    values from the analysis.

    :param analysis_result:
        The resulting data from a certain analysis procedure.
    :return:
        The maximum branching order of the morphology.
    """

    maximum_branching_order = 0

    # Apical dendrite
    if analysis_result.apical_dendrites_result is not None:
        for apical_dendrite_result in analysis_result.apical_dendrites_result:
            if len(apical_dendrite_result) > maximum_branching_order:
                maximum_branching_order = len(apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            if len(basal_dendrite_result) > maximum_branching_order:
                maximum_branching_order = len(basal_dendrite_result)

    # Axon
    if analysis_result.axons_result is not None:
        for axon_result in analysis_result.axons_result:
            if len(axon_result) > maximum_branching_order:
                maximum_branching_order = len(axon_result)

    # Return the maximum branching order
    return maximum_branching_order


####################################################################################################
# @compute_total_distribution_of_morphology
####################################################################################################
def compute_total_distribution_of_morphology(analysis_result):
    """Computes the total result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # Aggregate result of the entire morphology will be computed later
    maximum_branching_order = \
        get_morphology_maximum_branching_order_from_analysis_results(analysis_result)
    analysis_result.morphology_result = list()
    for i in range(maximum_branching_order):
        analysis_result.morphology_result.append([i + 1, 0])

    # Apical dendrite
    if analysis_result.apical_dendrites_result is not None:
        for item in analysis_result.apical_dendrites_result:
            analysis_result.morphology_result[item[0] - 1][1] += item[1]

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            for item in basal_dendrite_result:
                analysis_result.morphology_result[item[0] - 1][1] += item[1]

    # Axon
    if analysis_result.axons_result is not None:
        for item in analysis_result.axons_result:
            analysis_result.morphology_result[item[0] - 1][1] += item[1]


####################################################################################################
# @compute_total_analysis_result_of_morphology
####################################################################################################
def compute_total_analysis_result_of_morphology(analysis_result):
    """Computes the total result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # Aggregate result of the entire morphology will be computed later
    analysis_result.morphology_result = 0

    # Apical dendrite
    if analysis_result.apical_dendrites_result is not None:
        for result in analysis_result.apical_dendrites_result:
            analysis_result.morphology_result += result

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for result in analysis_result.basal_dendrites_result:
            analysis_result.morphology_result += result

    # Axon
    if analysis_result.axons_result is not None:
        for result in analysis_result.axons_result:
            analysis_result.morphology_result += result


####################################################################################################
# @compile_analysis_result_for_morphology
####################################################################################################
def compile_analysis_result_for_morphology(analysis_result):

    analysis_result.morphology_result = list()

    if analysis_result.apical_dendrites_result is not None:
        for result in analysis_result.apical_dendrites_result:
            analysis_result.morphology_result.append(result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for result in analysis_result.basal_dendrites_result:
            analysis_result.morphology_result.append(result)

        # Axon
    if analysis_result.axons_result is not None:
        for result in analysis_result.axons_result:
            analysis_result.morphology_result.append(result)


####################################################################################################
# @compute_minimum_analysis_result_of_morphology
####################################################################################################
def compute_minimum_analysis_result_of_morphology(analysis_result):
    """Computes the minimum result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrites_result is not None:
        for apical_dendrite_result in analysis_result.apical_dendrites_result:
            all_arbors_results.append(apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axons_result is not None:
        for axon_result in analysis_result.axons_result:
            all_arbors_results.append(axon_result)

    # Update the morphology result
    analysis_result.morphology_result = min(all_arbors_results)


####################################################################################################
# @compute_minimum_analysis_result_of_morphology_and_ignore_zero
####################################################################################################
def compute_minimum_analysis_result_of_morphology_and_ignore_zero(analysis_result):
    """Computes the minimum result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors. This function ignores the zero and picks a minimum value above
    it.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrites_result is not None:
        for apical_dendrite_result in analysis_result.apical_dendrites_result:
            all_arbors_results.append(apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axons_result is not None:
        for axon_result in analysis_result.axons_result:
            all_arbors_results.append(axon_result)

    # Remove zeros from the list
    if 0 in all_arbors_results:
        all_arbors_results.remove(0)

    # Update the morphology result
    analysis_result.morphology_result = min(all_arbors_results)


####################################################################################################
# @compute_maximum_analysis_result_of_morphology
####################################################################################################
def compute_maximum_analysis_result_of_morphology(analysis_result):
    """Computes the maximum result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrites_result is not None:
        for apical_dendrite_result in analysis_result.apical_dendrites_result:
            all_arbors_results.append(apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axons_result is not None:
        for axon_result in analysis_result.axons_result:
            all_arbors_results.append(axon_result)

    # Update the morphology result
    analysis_result.morphology_result = max(all_arbors_results)


####################################################################################################
# @compute_average_analysis_result_of_morphology
####################################################################################################
def compute_average_analysis_result_of_morphology(analysis_result):
    """Computes the average result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrites_result is not None:
        for apical_dendrite_result in analysis_result.apical_dendrites_result:
            all_arbors_results.append(apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axons_result is not None:
        for axon_result in analysis_result.axons_result:
            all_arbors_results.append(axon_result)

    # Update the morphology result
    analysis_result.morphology_result = 0
    for result in all_arbors_results:
        analysis_result.morphology_result += result
    analysis_result.morphology_result /= len(all_arbors_results)
    analysis_result.morphology_result = analysis_result.morphology_result


####################################################################################################
# @compute_average_analysis_result_of_morphology_and_ignore_zero
####################################################################################################
def compute_average_analysis_result_of_morphology_and_ignore_zero(analysis_result):
    """Computes the average result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors. This function ignores the zero-valued data from the computations.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrites_result is not None:
        for apical_dendrite_result in analysis_result.apical_dendrites_result:
            all_arbors_results.append(apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axons_result is not None:
        for axon_result in analysis_result.axons_result:
            all_arbors_results.append(axon_result)

    # Remove zeros from the list
    if 0 in all_arbors_results:
        all_arbors_results.remove(0)

    # Update the morphology result
    analysis_result.morphology_result = 0
    for result in all_arbors_results:
        analysis_result.morphology_result += result
    analysis_result.morphology_result /= len(all_arbors_results)


####################################################################################################
# @invoke_kernel
####################################################################################################
def invoke_kernel(morphology,
                  kernel,
                  aggregation_function):
    """Invoke the analysis kernel on the morphology and return the analysis result.

    :param morphology:
        A given morphology skeleton to analyze.
    :param kernel:
        Analysis kernel that will be applied on the morphology.
    :param aggregation_function:
        The function that will aggregate the entire morphology analysis result from the
        individual arbors, for example minimum, maximum, average or total.
    :return:
        The analysis results as an @MorphologyAnalysisResult structure.
    """

    # Apply the analysis operation to the morphology
    analysis_result = nmv.analysis.apply_analysis_operation_to_morphology(*[morphology, kernel])

    # Update the aggregate morphology result from the arbors
    aggregation_function(analysis_result)

    # Return the analysis result of the entire morphology
    return analysis_result


####################################################################################################
# @compile_data
####################################################################################################
def compile_data(morphology,
                 kernel):
    """Invoke the analysis kernel on the morphology and return the distribution in a form of list.

    :param morphology:
        A given morphology skeleton to analyze.
    :param kernel:
        Analysis kernel that will be applied on the morphology.
    :return:
        The analysis distribution as lists. The format of these lists are only known within the
        section function and the morphology function.
    """

    # Apply the analysis operation to the morphology and return the resulting lists
    return nmv.analysis.apply_analysis_operation_to_morphology(*[morphology, kernel])
