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
