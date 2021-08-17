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

import math


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

    # Add the stats. to the morphology skeleton to be used later in any operation
    section.stats.volume = section_volume

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


####################################################################################################
# @compute_section_volume_from_segments
####################################################################################################
def compute_segments_volumes_in_section(section,
                                        segments_volumes):
    """Computes the volume of a section from its segments.

    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its volume.
    :param segments_volumes:
        A list to collect the resulting data.
    """

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:
        return

    # Integrate the volume between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the data of the samples along each segment on the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius

        # Compute the segment volume and append to the total section volume
        segment_volume = (1.0 / 3.0) * math.pi * (p0 - p1).length * (r0 * r0 + r0 * r1 + r1 * r1)

        # Append to the list
        segments_volumes.append(segment_volume)
