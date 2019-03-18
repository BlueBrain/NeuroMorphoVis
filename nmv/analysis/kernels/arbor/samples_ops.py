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

import nmv
import nmv.analysis
import nmv.skeleton


####################################################################################################
# @compute_total_number_samples_of_arbor
####################################################################################################
def compute_total_number_samples_of_arbor(arbor):
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
# @compute_total_number_samples_of_arbor
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
          nmv.analysis.compute_number_of_zero_radii_samples_per_section,
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
    return min(sections_number_samples)


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
    return max(sections_number_samples)


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
    return min(sections_samples_radii)


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
    return max(sections_samples_radii)


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
    return (1.0 * sum(sections_samples_radii)) / len(sections_samples_radii)


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
        A list of the radii of the samples .
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







def compute_distribution_number_samples_per_section_of_arbor(arbor):

    # A list that will contain the number of samples per section
    data_list = list()

    # Compute the number of segments of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_distribution_number_of_samples_per_section,
          data_list])
