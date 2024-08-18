####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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
import nmv.consts
import nmv.analysis
import nmv.utilities


####################################################################################################
# @kernel_total_number_samples
####################################################################################################
def kernel_total_number_samples(morphology):
    """Analyse the total number of samples of the given morphology.

    This analysis accounts for the number of samples of each individual arbor or neurite of the
    morphology and the total number of samples of the entire morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_number_of_samples_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_number_samples_per_section
####################################################################################################
def kernel_minimum_number_samples_per_section(morphology):
    """Analyses the minimum number of samples per section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_samples_count_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=analysis_results.basal_dendrites_result,
        apical_dendrites_list=analysis_results.apical_dendrites_result,
        axons_list=analysis_results.axons_result)

    # Store the result in the morphology
    morphology.stats.minimum_number_samples_in_section = min(combined_results)

    # Return the analysis results
    return analysis_results


####################################################################################################
# @kernel_maximum_number_samples_per_section
####################################################################################################
def kernel_maximum_number_samples_per_section(morphology):
    """Analyses the maximum number of samples per section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_samples_count_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=analysis_results.basal_dendrites_result,
        apical_dendrites_list=analysis_results.apical_dendrites_result,
        axons_list=analysis_results.axons_result)

    # Store the result in the morphology
    morphology.stats.maximum_number_samples_in_section = max(combined_results)

    # Return the analysis results
    return analysis_results


####################################################################################################
# @kernel_average_number_samples_per_section
####################################################################################################
def kernel_average_number_samples_per_section(morphology):
    """Analyses the average number of samples per section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_number_samples_per_section_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_number_samples_per_micron_per_section
####################################################################################################
def kernel_average_number_samples_per_micron_per_section(morphology):
    """Analyses the average number of samples per micron per section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_number_samples_per_micron_of_arbor_distributions,
        nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_sampling_distance_per_section
####################################################################################################
def kernel_average_sampling_distance_per_section(morphology):
    """Analyses the average sampling distance section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_sampling_distance_arbor_distributions,
        nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_distance_from_initial_sample_to_origin
####################################################################################################
def kernel_distance_from_initial_sample_to_origin(morphology):
    """Computes the distance between the first sample along the arbor and the soma.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_first_sample_distance_to_soma,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_number_zero_radius_samples
####################################################################################################
def kernel_number_zero_radius_samples(morphology):
    """Find the number of zero-radii samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_number_of_zero_radius_samples_per_section_of_arbor,
        nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_sample_radius
####################################################################################################
def kernel_minimum_sample_radius(morphology):
    """Find the minimum radius of the samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_sample_radius_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=analysis_results.basal_dendrites_result,
        apical_dendrites_list=analysis_results.apical_dendrites_result,
        axons_list=analysis_results.axons_result)

    # Store the result in the morphology
    morphology.stats.minimum_sample_radius = min(combined_results)

    # Return the analysis results
    return analysis_results


####################################################################################################
# @kernel_maximum_sample_radius
####################################################################################################
def kernel_maximum_sample_radius(morphology):
    """Find the minimum radius of the samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Run the analysis kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_sample_radius_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Compile all the results into a single list to store the resulting values and annotate
    # the morphology skeleton
    combined_results = nmv.analysis.combine_results_into_single_list(
        basal_dendrites_list=analysis_results.basal_dendrites_result,
        apical_dendrites_list=analysis_results.apical_dendrites_result,
        axons_list=analysis_results.axons_result)

    # Store the result in the morphology
    morphology.stats.maximum_sample_radius = max(combined_results)

    # Return the analysis results
    return analysis_results


####################################################################################################
# @kernel_average_sample_radius
####################################################################################################
def kernel_average_sample_radius(morphology):
    """Find the average radius of the samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_sample_radius_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_daughter_ratio
####################################################################################################
def kernel_minimum_daughter_ratio(morphology):
    """Find the minimum daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_daughter_ratio_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_maximum_daughter_ratio
####################################################################################################
def kernel_maximum_daughter_ratio(morphology):
    """Find the maximum daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_daughter_ratio_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_daughter_ratio
####################################################################################################
def kernel_average_daughter_ratio(morphology):
    """Find the average daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_daughter_ratio_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_minimum_parent_daughter_ratio
####################################################################################################
def kernel_minimum_parent_daughter_ratio(morphology):
    """Find the minimum daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_parent_daughter_ratio_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_maximum_parent_daughter_ratio
####################################################################################################
def kernel_maximum_parent_daughter_ratio(morphology):
    """Find the maximum daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_parent_daughter_ratio_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_parent_daughter_ratio
####################################################################################################
def kernel_average_parent_daughter_ratio(morphology):
    """Find the average daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_parent_daughter_ratio_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_minimum_partition_asymmetry
####################################################################################################
def kernel_minimum_partition_asymmetry(morphology):
    """Find the minimum partition asymmetry of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_partition_asymmetry_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_partition_asymmetry
####################################################################################################
def kernel_maximum_partition_asymmetry(morphology):
    """Find the maximum partition asymmetry of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_partition_asymmetry_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_partition_asymmetry
####################################################################################################
def kernel_average_partition_asymmetry(morphology):
    """Find the average partition asymmetry of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_partition_asymmetry_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @compute_distribution_number_of_samples_of_morphology
####################################################################################################
def compute_distribution_number_of_samples_of_morphology(morphology):

    # Apply the kernel
    analysis_result = nmv.analysis.apply_kernel_to_morphology_to_collect_distributions(
        *[morphology,
          nmv.analysis.compute_distribution_number_of_samples_per_arbor])

    # Compile the list for the entire morphology
    nmv.analysis.compile_analysis_result_for_morphology(analysis_result)

    # Return the results
    return analysis_result


####################################################################################################
# @compute_distribution_samples_radii_of_morphology
####################################################################################################
def compute_distribution_samples_radii_of_morphology(morphology):

    # Apply the kernel
    analysis_result = nmv.analysis.apply_kernel_to_morphology_to_collect_distributions(
        *[morphology,
          nmv.analysis.compute_distribution_samples_radii_per_arbor])

    # Compile the list for the entire morphology
    nmv.analysis.compile_analysis_result_for_morphology(analysis_result)

    # Return the results
    return analysis_result


