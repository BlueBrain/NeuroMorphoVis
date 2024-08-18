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


####################################################################################################
# @MorphologyStats
####################################################################################################
class MorphologyStats:

    def __init__(self):

        # The total number of samples in the entire morphology
        self.number_samples = None

        # The number of samples in the section that has the least samples in the morphology
        self.minimum_number_samples_in_section = None

        # The number of samples in the section that has the most samples in the morphology
        self.maximum_number_samples_in_section = None

        # The total number of sections in the morphology
        self.number_sections = None

        # The total length of the entire morphology
        self.length = None

        # The length of the shortest section in the morphology
        self.minimum_section_length = None

        # The length of the longest section in the morphology
        self.maximum_section_length = None

        # The average section length in the morphology
        self.average_section_length = None

        # The length of the shortest segment in the morphology
        self.minimum_segment_length = None

        # The length of the longest segment in the morphology
        self.maximum_segment_length = None

        # The average segment length in the morphology
        self.average_segment_length = None

        # The surface area of the smallest section in the morphology
        self.minimum_section_surface_area = None

        # The surface area of the largest section in the morphology
        self.maximum_section_surface_area = None

        # The surface area of the smallest segment in the morphology
        self.minimum_segment_surface_area = None

        # The surface area of the largest segment in the morphology
        self.maximum_segment_surface_area = None

        # The volume of the smallest section in the morphology
        self.minimum_section_volume = None

        # The volume of the largest section in the morphology
        self.maximum_section_volume = None

        # The volume of the smallest segment in the morphology
        self.minimum_segment_volume = None

        # The volume of the largest segment in the morphology
        self.maximum_segment_volume = None

        # The total surface area of the entire morphology
        self.surface_area = None

        # The total volume of the entire morphology
        self.volume = None

        # The maximum path distance along the entire morphology
        self.maximum_path_distance = None

        # The maximum Euclidean distance along the entire morphology
        self.maximum_euclidean_distance = None


