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

# System imports
import math


####################################################################################################
# @compute_number_of_samples_per_section
####################################################################################################
def compute_number_of_samples_per_section(section,
                                          analysis_data):
    """Computes the number of samples of a given section.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    analysis_data.append(len(section.samples))


####################################################################################################
# @compute_number_of_segments_per_section
####################################################################################################
def compute_number_of_segments_per_section(section,
                                           analysis_data):
    """Computes the number of segments of a given section.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    analysis_data.append(len(section.samples) - 1)


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
# @compute_section_surface_area_from_segments
####################################################################################################
def compute_section_surface_area_from_segments(section):
    """Computes the surface area of a section from its segments.
    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its surface area.
    :return:
        Section total surface area in square microns.
    """

    # Section surface area
    section_surface_area = 0.0

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Return 0
        return section_surface_area

    # Integrate the surface area between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the data of the samples along each segment on the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius

        # Compute the segment lateral area
        segment_length = (p0 - p1).length
        r_sum = r0 + r1
        r_diff = r0 - r1
        segment_lateral_area = math.pi * r_sum * math.sqrt((r_diff * r_diff) + segment_length)

        # Compute the segment surface area and append it to the total section surface area
        section_surface_area += segment_lateral_area + math.pi * ((r0 * r0) + (r1 * r1))

    # Return the section surface area
    return section_surface_area


####################################################################################################
# @compute_sections_surface_areas_from_segments
####################################################################################################
def compute_sections_surface_areas_from_segments(section,
                                                 sections_surface_areas):

    """Computes the surface areas of all the sections along a given neurite or arbor.

    :param section:
        A given section to compute its surface area.
    :param sections_surface_areas:
        A list to collect the resulting data.
    """

    # Compute section surface area
    section_surface_area = compute_section_surface_area_from_segments(section=section)

    # Append the computed surface area to the list
    sections_surface_areas.append(section_surface_area)


####################################################################################################
# @compute_section_volume_from_segments
####################################################################################################
def compute_section_volume_from_segments(section):
    """Computes the volume of a section from its segments.

    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its volume.
    :return:
        Section total volume in cube microns.
    """

    # Section volume
    section_volume = 0.0

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Return 0
        return section_volume

    # Integrate the volume between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the data of the samples along each segment on the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius

        # Compute the segment volume and append to the total section volume
        section_volume += (1.0 / 3.0) * math.pi * (p0 - p1).length * (r0 * r0 + r0 * r1 + r1 * r1)

    # Return the section volume
    return section_volume


####################################################################################################
# @compute_sections_volumes_from_segments
####################################################################################################
def compute_sections_volumes_from_segments(section,
                                           sections_volumes):

    """Computes the volumes of all the sections along a given neurite or arbor.

    :param section:
        A given section to compute its surface area.
    :param sections_volumes:
        A list to collect the resulting data.
    """

    # Compute section surface area
    section_volume = compute_section_volume_from_segments(section=section)

    # Append the computed surface area to the list
    sections_volumes.append(section_volume)
