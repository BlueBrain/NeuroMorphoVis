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


####################################################################################################
# @compute_segments_lengths
####################################################################################################
def compute_segments_lengths(section,
                             segments_lengths):
    """Computes the lengths of all the segments along a given neurite or arbor.

     :param section:
        A given section to compute its length.
    :param segments_lengths:
        A list to collect the resulting data.
    """

    # Iterate over each segment in the section
    for i in range(len(section.samples) - 1):

        # Retrieve the points along each segment on the section
        point_0 = section.samples[i].point
        point_1 = section.samples[i + 1].point

        # Compute the segment length
        segment_length = (point_1 - point_0).length

        # Append it to the list
        segments_lengths.append(segment_length)


####################################################################################################
# @compute_section_length
####################################################################################################
def compute_section_length(section):
    """
    Computes the length of a given section.
    NOTE: This function returns a meaningful value for the roots sections, ONLY when the negative
    samples are removed from the branch, otherwise, the contribution of the negative samples
    will be integrated. The negative samples are those located closer to the origin of the soma
    than the first samples of the section.

    :param section:
        A given section to compute its length.
    :return:
        Section total length in microns.
    """

    # Section length
    section_length = 0.0

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Return 0
        return section_length

    # Integrate the distance between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the points along each segment on the section
        point_0 = section.samples[i].point
        point_1 = section.samples[i + 1].point

        # Update the section length
        section_length += (point_1 - point_0).length

    # Return the section length
    return section_length


####################################################################################################
# @compute_sections_lengths
####################################################################################################
def compute_sections_lengths(section,
                             sections_lengths):
    """Computes the lengths of all the sections along a given neurite or arbor.

    :param section:
        A given section to compute its length.
    :param sections_lengths:
        A list to collect the resulting data.
    """

    # Compute section length
    section_length = compute_section_length(section=section)

    # Append the length to the list
    sections_lengths.append(section_length)


####################################################################################################
# @identify_short_sections
####################################################################################################
def identify_short_sections(section,
                            short_sections):
    """Analyze the short sections, which have their length shorter than the sum of their
    initial and final diameters.

    :param section:
        A given section to get analyzed.
    :param short_sections:
        A list to collect the resulting analysis data.
    """

    # Only applies if the section has more than two samples
    if len(section.samples) > 1:

        # Compute the sum of the diameters of the first and last samples
        diameters_sum = (section.samples[0].radius + section.samples[-1].radius) * 2

        # Compute section length
        section_length = compute_section_length(section=section)

        # If the sum is smaller than the section length, then report it as an issue
        if section_length < diameters_sum:

            # Update the list
            analysis_string = 'Section[%s : %d] : Length[Current : %f, Minimal : %f]' % (
                section.get_type_string(), section.id, section_length, diameters_sum)
            short_sections.append(analysis_string)