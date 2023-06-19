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
# @kernel_total_number_sections
####################################################################################################
def kernel_total_number_sections(morphology):
    """Compute the total number of sections of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_number_of_sections_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_total_number_bifurcations
####################################################################################################
def kernel_total_number_bifurcations(morphology):
    """Compute the total number of bifurcations of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_number_of_bifurcations_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_total_number_trifurcations
####################################################################################################
def kernel_total_number_trifurcations(morphology):
    """Compute the total number of bifurcations of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_number_of_trifurcations_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_total_number_terminal_tips
####################################################################################################
def kernel_total_number_terminal_tips(morphology):
    """Compute the total number of terminal tips of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_number_of_terminal_tips_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_total_number_terminal_segments
####################################################################################################
def kernel_total_number_terminal_segments(morphology):
    """Compute the total number of terminal segments of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_total_number_of_terminal_segments_of_arbor,
        nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_path_distance
####################################################################################################
def kernel_maximum_path_distance(morphology):
    """Computes the maximum path distance from the soma along all the arbors till their last sample.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_path_distance_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=analysis_results.basal_dendrites_result,
        apical_dendrites_list=analysis_results.apical_dendrites_result,
        axons_list=analysis_results.axons_result)

    # Store the result in the morphology
    morphology.stats.maximum_path_distance = max(combined_results)

    # Return the analysis results
    return analysis_results


####################################################################################################
# @kernel_maximum_euclidean_distance
####################################################################################################
def kernel_maximum_euclidean_distance(morphology):
    """Computes the maximum Euclidean distance from the soma along all the arbors till their last
    sample.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_euclidean_distance_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=analysis_results.basal_dendrites_result,
        apical_dendrites_list=analysis_results.apical_dendrites_result,
        axons_list=analysis_results.axons_result)

    # Store the result in the morphology
    morphology.stats.maximum_euclidean_distance = max(combined_results)

    # Return the analysis results
    return analysis_results


####################################################################################################
# @kernel_maximum_branching_order
####################################################################################################
def kernel_maximum_branching_order(morphology):
    """Computes the maximum branching order of the morphology per arbor.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Apply the kernel
    result = nmv.analysis.invoke_kernel(morphology,
                                        nmv.analysis.compute_maximum_branching_order_of_arbor,
                                        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Axon
    if result.axons_result is not None:
        for i in range(len(result.axons_result)):
            morphology.axons[i].maximum_branching_order = result.axons_result[i]

    # Apical dendrite
    if result.apical_dendrites_result is not None:
        for i in range(len(result.apical_dendrites_result)):
            morphology.apical_dendrites[i].maximum_branching_order = \
                result.apical_dendrites_result[i]

    # Basal dendrites
    if result.basal_dendrites_result is not None:
        for i in range(len(result.basal_dendrites_result)):
            morphology.basal_dendrites[i].maximum_branching_order = result.basal_dendrites_result[i]

    # Pass the analysis results to the morphology
    morphology.maximum_branching_order = result

    # Return the final result
    return result
