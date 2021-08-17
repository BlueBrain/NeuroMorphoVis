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

# System imports
import copy

# Internal imports
import nmv.analysis


####################################################################################################
# @kernel_total_surface_area
####################################################################################################
def kernel_total_surface_area(morphology):
    """Analyse the total surface area of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_arbor_total_surface_area,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_section_surface_area
####################################################################################################
def kernel_minimum_section_surface_area(morphology):
    """Find the minimum section surface area of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    sections_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_section_surface_area,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=sections_results.basal_dendrites_result,
        apical_dendrites_list=sections_results.apical_dendrites_result,
        axons_list=sections_results.axons_result)

    # Store the result in the morphology
    morphology.stats.minimum_section_surface_area = copy.deepcopy(min(combined_results))

    # NOTE: We will also compute the minimum segment surface area to complete the analysis
    segment_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_segment_surface_area,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=segment_results.basal_dendrites_result,
        apical_dendrites_list=segment_results.apical_dendrites_result,
        axons_list=segment_results.axons_result)

    # Store the result in the morphology
    morphology.stats.minimum_segment_surface_area = copy.deepcopy(min(combined_results))

    # Return the analysis results of the section
    return sections_results


####################################################################################################
# @kernel_maximum_section_surface_area
####################################################################################################
def kernel_maximum_section_surface_area(morphology):
    """Find the maximum section surface area of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    sections_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_section_surface_area,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=sections_results.basal_dendrites_result,
        apical_dendrites_list=sections_results.apical_dendrites_result,
        axons_list=sections_results.axons_result)

    # Store the result in the morphology
    morphology.stats.maximum_section_surface_area = copy.deepcopy(max(combined_results))

    # NOTE: We will also compute the minimum segment surface area to complete the analysis
    segment_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_segment_surface_area,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=segment_results.basal_dendrites_result,
        apical_dendrites_list=segment_results.apical_dendrites_result,
        axons_list=segment_results.axons_result)

    # Store the result in the morphology
    morphology.stats.maximum_segment_surface_area = copy.deepcopy(max(combined_results))

    # Return the analysis results
    return sections_results


####################################################################################################
# @kernel_average_section_surface_area
####################################################################################################
def kernel_average_section_surface_area(morphology):
    """Find the average section surface area of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_average_section_surface_area,
                                      nmv.analysis.compute_average_analysis_result_of_morphology)
