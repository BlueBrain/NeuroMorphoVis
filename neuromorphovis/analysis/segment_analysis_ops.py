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

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.skeleton


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
# @compute_segments_length
####################################################################################################
def compute_segments_length_with_annotations(section,
                                             segments_length_list):
    """Computes the length of each segment along the given section and annotate the result with the
    data of the segments for extended analysis. The results are appends the to the given list.

    :param section:
        A given section to be analyzed.
    :param segments_length_list:
        The list where the computed lengths will be appended to.
    """

    # Iterate over each segment in the section
    for i in range(len(section.samples) - 1):

        # Retrieve the points along each segment on the section
        point_0 = section.samples[i].point
        point_1 = section.samples[i + 1].point

        # Compute the segment length
        segment_length = (point_1 - point_0).length

        #


        # Append it to the list
        segments_length_list.append(segment_length)
