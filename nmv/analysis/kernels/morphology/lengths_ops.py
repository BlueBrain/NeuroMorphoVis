####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# Internal imports
import nmv.analysis


####################################################################################################
# @kernel_total_length
####################################################################################################
def kernel_total_length(morphology):
    """Analyse the total length aspects the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_length_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_section_length
####################################################################################################
def kernel_minimum_section_length(morphology):
    """Find the minimum section length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_section_length_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=analysis_results.basal_dendrites_result,
        apical_dendrites_list=analysis_results.apical_dendrites_result,
        axons_list=analysis_results.axons_result)

    # Store the result in the morphology
    morphology.stats.minimum_section_length = min(combined_results)

    # Return the analysis results
    return analysis_results


####################################################################################################
# @kernel_maximum_section_length
####################################################################################################
def kernel_maximum_section_length(morphology):
    """Find the maximum section length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_section_length_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=analysis_results.basal_dendrites_result,
        apical_dendrites_list=analysis_results.apical_dendrites_result,
        axons_list=analysis_results.axons_result)

    # Store the result in the morphology
    morphology.stats.maximum_section_length = max(combined_results)

    # Return the analysis results
    return analysis_results


####################################################################################################
# @kernel_average_section_length
####################################################################################################
def kernel_average_section_length(morphology):
    """Find the average section length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_average_section_length_of_arbor,
                                      nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_segment_length
####################################################################################################
def kernel_minimum_segment_length(morphology):
    """Find the minimum segment length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_segment_length_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=analysis_results.basal_dendrites_result,
        apical_dendrites_list=analysis_results.apical_dendrites_result,
        axons_list=analysis_results.axons_result)

    # Store the result in the morphology
    morphology.stats.minimum_segment_length = min(combined_results)

    # Return the analysis results
    return analysis_results


####################################################################################################
# @kernel_maximum_segment_length
####################################################################################################
def kernel_maximum_segment_length(morphology):
    """Find the maximum segment length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_segment_length_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=analysis_results.basal_dendrites_result,
        apical_dendrites_list=analysis_results.apical_dendrites_result,
        axons_list=analysis_results.axons_result)

    # Store the result in the morphology
    morphology.stats.maximum_segment_length = max(combined_results)

    # Return the analysis results
    return analysis_results


####################################################################################################
# @kernel_average_segment_length
####################################################################################################
def kernel_average_segment_length(morphology):
    """Find the average segment length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_average_segment_length_of_arbor,
                                      nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_zero_length_segments
####################################################################################################
def kernel_zero_length_segments(morphology):
    """Find the number of zero-length segments of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_number_zero_length_segments_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_short_sections
####################################################################################################
def kernel_short_sections(morphology):
    """Find the number of the short sections of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_number_of_short_sections_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_contraction
####################################################################################################
def kernel_minimum_contraction(morphology):
    """Find the minimum contraction ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_minimum_section_contraction_of_arbor,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_contraction
####################################################################################################
def kernel_maximum_contraction(morphology):
    """Find the maximum contraction ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_section_contraction_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_contraction
####################################################################################################
def kernel_average_contraction(morphology):
    """Find the average contraction ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_average_section_contraction_of_arbor,
                                      nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_burke_taper
####################################################################################################
def kernel_minimum_burke_taper(morphology):
    """Find the minimum Burke taper of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_minimum_burke_taper_of_arbor,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_hillman_taper
####################################################################################################
def kernel_minimum_hillman_taper(morphology):
    """Find the minimum Hillman taper of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_minimum_hillman_taper_of_arbor,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_burke_taper
####################################################################################################
def kernel_maximum_burke_taper(morphology):
    """Find the maximum Burke taper of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_burke_taper_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_hillman_taper
####################################################################################################
def kernel_maximum_hillman_taper(morphology):
    """Find the maximum Hillman taper of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_hillman_taper_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_burke_taper
####################################################################################################
def kernel_average_burke_taper(morphology):
    """Find the average Burke taper of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_average_burke_taper_of_arbor,
                                      nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_hillman_taper
####################################################################################################
def kernel_average_hillman_taper(morphology):
    """Find the average Hillman taper of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_average_hillman_taper_of_arbor,
                                      nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @compute_distribution_segments_length_of_morphology
####################################################################################################
def compute_distribution_segments_length_of_morphology(morphology):

    # Apply the kernel
    analysis_result = nmv.analysis.apply_kernel_to_morphology_to_collect_distributions(
        *[morphology,
          nmv.analysis.compute_distribution_segments_length_per_arbor])

    # Compile the list for the entire morphology
    nmv.analysis.compile_analysis_result_for_morphology(analysis_result)

    # Return the results
    return analysis_result

