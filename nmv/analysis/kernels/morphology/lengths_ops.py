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

# Internal imports
import nmv
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

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_minimum_section_length_of_arbor,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


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

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_section_length_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


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

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_minimum_segment_length_of_arbor,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


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

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_segment_length_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


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
# @kernel_average_segment_length
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
# @kernel_average_segment_length
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
# @kernel_sections_length_range_distribution
####################################################################################################
def kernel_total_arbor_length_distribution(morphology,
                                           options,
                                           figure_title,
                                           figure_axis_label,
                                           figure_label):

    # Get the results
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_total_length_of_arbor,
        nmv.analysis.compute_total_analysis_result_of_morphology)

    # Plot the distribution
    nmv.analysis.plot_per_arbor_distribution(analysis_results=analysis_results,
                                             morphology=morphology,
                                             options=options,
                                             figure_name=figure_label,
                                             x_label=figure_axis_label,
                                             title=figure_title,
                                             add_percentage=True)


####################################################################################################
# @kernel_sections_length_range_distribution
####################################################################################################
def kernel_sections_length_range_distribution(morphology,
                                              options,
                                              figure_title,
                                              figure_axis_label,
                                              figure_label):
    """Computes and plots the range of section lengths across the morphology along the different
    arbors.

    :param morphology:
        A given morphology skeleton to analyse.
    :param options:
        System options.
    """

    # Minimum
    minimum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_section_length_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Average
    average_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_section_length_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)

    # Maximum
    maximum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_section_length_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Plot
    nmv.analysis.plot_min_avg_max_per_arbor_distribution(
        minimum_results=minimum_results,
        maximum_results=maximum_results,
        average_results=average_results,
        morphology=morphology,
        options=options,
        figure_name=figure_label,
        x_label=figure_axis_label,
        title=figure_title)


####################################################################################################
# @kernel_segment_length_range_distribution
####################################################################################################
def kernel_segment_length_range_distribution(morphology,
                                             options,
                                             figure_title,
                                             figure_axis_label,
                                             figure_label):
    """Computes and plots the range of section lengths across the morphology along the different
    arbors.

    :param morphology:
        A given morphology skeleton to analyse.
    :param options:
        System options.
    """

    # Minimum
    minimum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_segment_length_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Average
    average_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_segment_length_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)

    # Maximum
    maximum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_segment_length_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Plot
    nmv.analysis.plot_min_avg_max_per_arbor_distribution(
        minimum_results=minimum_results,
        maximum_results=maximum_results,
        average_results=average_results,
        morphology=morphology,
        options=options,
        figure_name=figure_label,
        x_label=figure_axis_label,
        title=figure_title)



####################################################################################################
# @kernel_segments_length_range_distribution
####################################################################################################
def kernel_segments_length_range_distribution(morphology,
                                              options,
                                              figure_title,
                                              figure_axis_label,
                                              figure_label):
    """Computes and plots the range of section lengths across the morphology along the different
    arbors.

    :param morphology:
        A given morphology skeleton to analyse.
    :param options:
        System options.
    """

    # Minimum
    minimum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_segment_length_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Average
    average_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_segment_length_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)

    # Maximum
    maximum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_segment_length_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Plot
    nmv.analysis.plot_min_avg_max_per_arbor_distribution(
        minimum_results=minimum_results,
        maximum_results=maximum_results,
        average_results=average_results,
        morphology=morphology,
        options=options,
        figure_name=figure_label,
        x_label=figure_axis_label,
        title=figure_title)
