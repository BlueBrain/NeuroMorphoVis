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

import nmv
import nmv.analysis
import nmv.skeleton


####################################################################################################
# @compute_number_of_samples_of_arbor
####################################################################################################
def compute_number_of_samples_of_arbor(arbor):
    """Computes the total number of samples along the given arbor.

    Note that we use the number of segments to account for the number of samples to avoid
    double-counting the branching points.

    :param arbor:
        A given arbor to analyze.
    :return
        Total number of samples of the arbor.
    """

    # A list that will contain the number of samples per section
    sections_number_samples = list()

    # Compute the number of segments of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_number_of_segments_per_section,
          sections_number_samples])

    # Total number of samples
    total_number_samples = 0

    # Iterate and sum up
    for section_number_samples in sections_number_samples:

        # Add to the total number of samples
        total_number_samples += section_number_samples

    # Add the root sample that is not considered a bifurcation point
    total_number_samples += 1

    # Return the total number of samples of the given arbor
    return total_number_samples


####################################################################################################
# @compute_number_of_samples_of_arbor_distributions
####################################################################################################
def compute_number_of_samples_of_arbor_distributions(arbor):
    """Computes the total number of samples along the given arbor with respect to different
    branching orders.

    :param arbor:
        A given arbor to analyze.
    :return
        Total number of samples of the arbor w.r.t the branching order.
    """

    # A list that will be filled with the results recursively
    analysis_data = list()

    # Compute the number of segments of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_number_of_samples_per_section_distributions,
          analysis_data])

    # Aggregate the results
    aggregate_analysis_data = nmv.analysis.add_distributions(analysis_data)

    # Return the final aggregate data
    return aggregate_analysis_data


####################################################################################################
# @compute_number_of_samples_of_arbor
####################################################################################################
def compute_total_number_of_zero_radii_samples_of_arbor(arbor):
    """Computes the total number of samples that have zero-radii along the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Total number of samples of the arbor.
    """

    # A list that will contain the number of samples per section
    sections_number_zero_radii_samples = list()

    # Compute the number of segments of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_number_of_zero_radius_samples_per_section,
          sections_number_zero_radii_samples])

    # Total number of samples
    total_number_zero_radii_samples = 0

    # Iterate and sum up
    for section_number_zero_radii_samples in sections_number_zero_radii_samples:

        # Add to the total number of samples
        total_number_zero_radii_samples += section_number_zero_radii_samples

    # Return the total number of samples of the given arbor
    return total_number_zero_radii_samples


####################################################################################################
# @compute_minimum_samples_count_of_arbor
####################################################################################################
def compute_minimum_samples_count_of_arbor(arbor):
    """Computes the least number of samples found on a section that belongs to the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Least number of samples of a section along the arbor.
    """

    # A list that will contain the number of samples per section
    sections_number_samples = list()

    # Compute the number of segments of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_number_of_samples_per_section,
          sections_number_samples])

    # Return the minimum number of samples
    if len(sections_number_samples) > 0:
        return min(sections_number_samples)
    else:
        return 0


####################################################################################################
# @compute_minimum_samples_count_of_arbor
####################################################################################################
def compute_first_sample_distance_to_soma(arbor):
    """Computes the distance from the first sample along the arbor to the soma origin.

    :param arbor:
        A given arbor to analyze.
    :return
        The distance from the first sample along the arbor to the soma origin.
    """

    # No arbor
    if arbor is None:
        return 0

    if len(arbor.samples) > 0:
        return arbor.samples[0].point.length
    else:
        return 0




####################################################################################################
# @compute_maximum_samples_count_of_arbor
####################################################################################################
def compute_maximum_samples_count_of_arbor(arbor):
    """Computes the largest number of samples found on a section that belongs to the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Largest number of samples of a section along the arbor.
    """

    # A list that will contain the number of samples per section
    sections_number_samples = list()

    # Compute the number of segments of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_number_of_samples_per_section,
          sections_number_samples])

    # Return the minimum number of samples
    if len(sections_number_samples) > 0:
        return max(sections_number_samples)
    else:
        return 0


####################################################################################################
# @compute_average_number_samples_per_section_of_arbor
####################################################################################################
def compute_average_number_samples_per_section_of_arbor(arbor):
    """Computes the average number of samples per section of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Average number of samples per section along the gievn arbor.
    """

    # A list that will contain the number of samples per section
    sections_number_samples = list()

    # Compute the number of segments of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_number_of_samples_per_section,
          sections_number_samples])

    # Total number of samples
    total_number_samples = 0

    # At least one element
    if len(sections_number_samples) == 0:
        return 0

    # Iterate and sum up
    for section_number_samples in sections_number_samples:

        # Add to the total number of samples
        total_number_samples += section_number_samples

    # Return the average number of samples per section
    return int(total_number_samples * 1.0 / len(sections_number_samples))


####################################################################################################
# @compute_number_of_zero_radius_samples_per_section_of_arbor
####################################################################################################
def compute_number_of_zero_radius_samples_per_section_of_arbor(arbor):
    """Computes the total number of zero-radius samples per section of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Number of zero-radius samples along the given arbor.
    """

    # A list that will contain the number of samples per section
    sections_number_zero_radius_samples = list()

    # Compute the number of segments of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_number_of_zero_radius_samples_per_section,
          sections_number_zero_radius_samples])

    # Total number of samples
    total_number_zero_radius_samples = 0

    # Iterate and sum up
    for section_number_zero_radius_samples in sections_number_zero_radius_samples:

        # Add to the total number of samples
        total_number_zero_radius_samples += section_number_zero_radius_samples

    # Return the average number of samples per section
    return total_number_zero_radius_samples


####################################################################################################
# @compute_partition_asymmetry_per_section_of_arbor
####################################################################################################
def compute_partition_asymmetry_per_section_of_arbor(arbor):
    """Computes the total number of zero-radius samples per section of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Number of zero-radius samples along the given arbor.
    """

    # A list that will contain the values per section
    sections_partition_asymmetry = list()

    # Compute the value of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_section_partition_asymmetry,
          sections_partition_asymmetry])

    # Return the list that contains all the values
    return sections_partition_asymmetry


####################################################################################################
# @compute_minimum_partition_asymmetry_of_arbor
####################################################################################################
def compute_minimum_partition_asymmetry_of_arbor(arbor):
    """Computes the minimum partition asymmetry of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Minimum partition asymmetry of the given arbor.
    """

    # Result
    partition_asymmetry = compute_partition_asymmetry_per_section_of_arbor(arbor)

    # Return the minimum
    if len(partition_asymmetry) > 0:
        return min(partition_asymmetry)
    else:
        return 0


####################################################################################################
# @compute_maximum_partition_asymmetry_of_arbor
####################################################################################################
def compute_maximum_partition_asymmetry_of_arbor(arbor):
    """Computes the maximum partition asymmetry of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Maximum partition asymmetry of the given arbor.
    """

    # Result
    partition_asymmetry = compute_partition_asymmetry_per_section_of_arbor(arbor)

    # Return the maximum
    if len(partition_asymmetry) > 0:
        return max(partition_asymmetry)
    else:
        return 0


####################################################################################################
# @compute_average_partition_asymmetry_of_arbor
####################################################################################################
def compute_average_partition_asymmetry_of_arbor(arbor):
    """Computes the average partition asymmetry of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Average partition asymmetry of the given arbor.
    """

    # Return the average
    partition_asymmetry = compute_partition_asymmetry_per_section_of_arbor(arbor)

    if len(partition_asymmetry) > 0:
        return sum(partition_asymmetry) / (1.0 * len(partition_asymmetry))
    else:
        return 0.0


####################################################################################################
# @compute_minimum_sample_radius_of_arbor
####################################################################################################
def compute_minimum_sample_radius_of_arbor(arbor):
    """Computes the minimum sample radius of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Minimum sample radius along the given arbor.
    """

    # A list that will contain the radii of all the samples along a given section
    sections_samples_radii = list()

    # Append the radii of the samples to the list
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_minimum_sample_radius_per_section,
          sections_samples_radii])

    # Return the minimum sample radius
    if len(sections_samples_radii) > 0:
        return min(sections_samples_radii)
    else:
        return 0.0


####################################################################################################
# @compute_minimum_daughter_ratio_of_arbor
####################################################################################################
def compute_minimum_daughter_ratio_of_arbor(arbor):

    # A list that will contain the radii of all the samples along a given section
    data_list = list()

    # Append the radii of the samples to the list
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_daughter_ratio,
          data_list])

    # The data list must have at least one element
    if len(data_list) > 0:
        return min(data_list)
    else:
        return 0.0


####################################################################################################
# @compute_maximum_daughter_ratio_of_arbor
####################################################################################################
def compute_maximum_daughter_ratio_of_arbor(arbor):

    # A list that will contain the radii of all the samples along a given section
    data_list = list()

    # Append the radii of the samples to the list
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_daughter_ratio,
          data_list])

    # The data list must have at least one element
    if len(data_list) > 0:
        return max(data_list)
    else:
        return 0.0


####################################################################################################
# @compute_average_daughter_ratio_of_arbor
####################################################################################################
def compute_average_daughter_ratio_of_arbor(arbor):

    # A list that will contain the radii of all the samples along a given section
    data_list = list()

    # Append the radii of the samples to the list
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_daughter_ratio,
          data_list])

    # The data list must have at least one element
    if len(data_list) > 0:
        return sum(data_list) / len(data_list)
    else:
        return 0.0


####################################################################################################
# @compute_minimum_parent_daughter_ratio_of_arbor
####################################################################################################
def compute_minimum_parent_daughter_ratio_of_arbor(arbor):

    # A list that will contain the radii of all the samples along a given section
    data_list = list()

    # Append the radii of the samples to the list
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_parent_daughter_ratios,
          data_list])

    # The data list must have at least one element
    if len(data_list) > 0:
        return min(data_list)
    else:
        return 0.0


####################################################################################################
# @compute_maximum_parent_daughter_ratio_of_arbor
####################################################################################################
def compute_maximum_parent_daughter_ratio_of_arbor(arbor):

    # A list that will contain the radii of all the samples along a given section
    data_list = list()

    # Append the radii of the samples to the list
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_parent_daughter_ratios,
          data_list])

    # The data list must have at least one element
    if len(data_list) > 0:
        return max(data_list)
    else:
        return 0.0


####################################################################################################
# @compute_average_parent_daughter_ratio_of_arbor
####################################################################################################
def compute_average_parent_daughter_ratio_of_arbor(arbor):

    # A list that will contain the radii of all the samples along a given section
    data_list = list()

    # Append the radii of the samples to the list
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_parent_daughter_ratios,
          data_list])

    # The data list must have at least one element
    if len(data_list) > 0:
        return sum(data_list) / len(data_list)
    else:
        return 0.0


####################################################################################################
# @compute_maximum_sample_radius_of_arbor
####################################################################################################
def compute_maximum_sample_radius_of_arbor(arbor):
    """Computes the maximum sample radius of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Maximum sample radius along the given arbor.
    """

    # A list that will contain the radii of all the samples along a given section
    sections_samples_radii = list()

    # Append the radii of the samples to the list
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_maximum_sample_radius_per_section,
          sections_samples_radii])

    # Return the maximum sample radius
    if len(sections_samples_radii) > 0:
        return max(sections_samples_radii)
    else:
        return 0.0


####################################################################################################
# @compute_average_sample_radius_of_arbor
####################################################################################################
def compute_average_sample_radius_of_arbor(arbor):
    """Computes the average sample radius of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Average sample radius along the given arbor.
    """

    # A list that will contain the radii of all the samples along a given section
    sections_samples_radii = list()

    # Append the radii of the samples to the list
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_average_sample_radius_per_section,
          sections_samples_radii])

    # Return the maximum sample radius
    if len(sections_samples_radii) > 0:
        return (1.0 * sum(sections_samples_radii)) / len(sections_samples_radii)
    else:
        return 0.0


####################################################################################################
# @get_samples_radii_of_arbor
####################################################################################################
def get_samples_radii_of_arbor(arbor):
    """Gets a list of the radii of all the samples of a given arbor.

    :param arbor:
        A given arbor to get analyzed.
    :return
        A list of the radii of the samples .
    """

    # A list that will contain the analysis data
    arbor_samples_radii = list()

    # Analyse
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.get_samples_radii_of_section,
          arbor_samples_radii])

    # Return the list
    return arbor_samples_radii


####################################################################################################
# @get_number_of_samples_per_section_of_arbor
####################################################################################################
def get_number_of_samples_per_section_of_arbor(arbor):
    """Gets a list of the number of samples per section of a given arbor.

    :param arbor:
        A given arbor to get analyzed.
    :return
        A list of the radii of the samples.
    """

    # A list that will contain the analysis data
    arbor_number_of_samples_per_section = list()

    # Analyse
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.get_number_of_samples_per_section_of_section,
          arbor_number_of_samples_per_section])

    # Return the list
    return arbor_number_of_samples_per_section
