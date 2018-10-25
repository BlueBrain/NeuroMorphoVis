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

import neuromorphovis as nmv
import neuromorphovis.analysis
import neuromorphovis.skeleton


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