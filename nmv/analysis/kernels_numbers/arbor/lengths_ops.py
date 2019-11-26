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

# Internal imports
import nmv
import nmv.analysis
import nmv.skeleton


####################################################################################################
# @compute_arbor_total_length
####################################################################################################
def compute_total_length_of_arbor(arbor):
    """Computes the total length of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The total length of the arbor in um.
    """

    # A list that will contains the lengths of all the sections along the arbor
    sections_lengths = list()

    # Compute the length of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_lengths,
          sections_lengths])

    # Total arbor length
    arbor_total_length = 0.0

    # Iterate and sum up all the sections lengths
    for length in sections_lengths:

        # Add to the arbor length
        arbor_total_length += length

    # Return the total section length
    return arbor_total_length


####################################################################################################
# @compute_segments_lengths_of_arbor
####################################################################################################
def compute_segments_lengths_of_arbor(arbor):
    """Computes an array that contains the lengths of all the segments along the arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        An array that contains the lengths of all the segments along the arbor.
    """

    # A list that will contains the lengths of all the segments along the arbor
    segments_lengths = list()

    # Compute the length of each segment individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_segments_lengths,
          segments_lengths])

    # Return the list
    return segments_lengths


####################################################################################################
# @compute_minimum_segment_length_of_arbor
####################################################################################################
def compute_minimum_segment_length_of_arbor(arbor):
    """Computes the minimum segment length along the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The minimum segment length of the given arbor.
    """

    # Get all the segments lengths
    segments_lengths = compute_segments_lengths_of_arbor(arbor)

    # Return the minimum
    return min(segments_lengths)


####################################################################################################
# @compute_maximum_segment_length_of_arbor
####################################################################################################
def compute_maximum_segment_length_of_arbor(arbor):
    """Computes the maximum segment length along the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The maximum segment length of the given arbor.
    """

    # Get all the segments lengths
    segments_lengths = compute_segments_lengths_of_arbor(arbor)

    # Return the maximum
    return max(segments_lengths)


####################################################################################################
# @compute_average_segment_length_of_arbor
####################################################################################################
def compute_average_segment_length_of_arbor(arbor):
    """Computes the average segment length along the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The average segment length of the given arbor.
    """

    # Get all the segments lengths
    segments_lengths = compute_segments_lengths_of_arbor(arbor)

    # Total length
    total_length = 0.0

    # Iterate and sum up all the segments lengths
    for length in segments_lengths:

        # Add to the arbor length
        total_length += length

    # Return the average segment length by normalizing the total one
    return total_length / len(segments_lengths)


####################################################################################################
# @compute_number_zero_length_segments_of_arbor
####################################################################################################
def compute_number_zero_length_segments_of_arbor(arbor):
    """Computes the number of zero-length segments of a given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The number of zero-length segments of the given arbor.
    """

    # Get all the segments lengths
    segments_lengths = compute_segments_lengths_of_arbor(arbor)

    # Number of zero-length segments
    zero_length_segments = 0

    # Check the length of each segment
    for segment_length in segments_lengths:

        # If the segment length is zero
        if segment_length < 1e-5:

            # Increment the count
            zero_length_segments += 1

    # Return the number of zero-length segments
    return zero_length_segments


####################################################################################################
# @compute_sections_lengths_of_arbor
####################################################################################################
def compute_sections_lengths_of_arbor(arbor):
    """Computes an array that contains the lengths of all the sections along the arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        An array that contains the lengths of all the sections along the arbor.
    """

    # A list that will contains the lengths of all the sections along the arbor
    sections_lengths = list()

    # Compute the length of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_lengths,
          sections_lengths])

    # Return the list
    return sections_lengths


####################################################################################################
# @compute_minimum_section_length_of_arbor
####################################################################################################
def compute_minimum_section_length_of_arbor(arbor):
    """Computes the minimum section length along the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The minimum section length of the given arbor
    """

    # Get all the sections lengths
    sections_lengths = compute_sections_lengths_of_arbor(arbor)

    # Return the minimum
    return min(sections_lengths)


####################################################################################################
# @compute_maximum_section_length_of_arbor
####################################################################################################
def compute_maximum_section_length_of_arbor(arbor):
    """Computes the maximum section length along the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The maximum section length of the given arbor
    """

    # Get all the sections lengths
    sections_lengths = compute_sections_lengths_of_arbor(arbor)

    # Return the minimum
    return max(sections_lengths)


####################################################################################################
# @compute_average_section_length_of_arbor
####################################################################################################
def compute_average_section_length_of_arbor(arbor):
    """Computes the average section length along the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The average section length of the given arbor
    """

    # Get all the sections lengths
    sections_lengths = compute_sections_lengths_of_arbor(arbor)

    # Total arbor length
    arbor_total_length = 0.0

    # Iterate and sum up all the sections lengths
    for length in sections_lengths:

        # Add to the arbor length
        arbor_total_length += length

    # Return the average section length by normalizing the total one
    return arbor_total_length / len(sections_lengths)


####################################################################################################
# @compute_number_of_short_sections_of_arbor
####################################################################################################
def compute_number_of_short_sections_of_arbor(arbor):
    """Computes an array that contains the lengths of all the sections along the arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        An array that contains the lengths of all the sections along the arbor.
    """

    # A list that will contains the lengths of all the sections along the arbor
    short_sections = list()

    # Compute the length of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.identify_short_sections,
          short_sections])

    # Return the number of short sections
    return len(short_sections)
