####################################################################################################
# Copyright (c) 2016 - 2021, EPFL / Blue Brain Project
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
# @SectionStats
####################################################################################################
class SectionStats:

    def __init__(self):

        # Number of samples in the section
        self.number_samples = None

        # Number of segments in the section
        self.number_segments = None

        # The length of the section
        self.length = None

        # The length of the shortest segment in the section
        self.minimum_segment_length = None

        # The length of the longest segment in the section
        self.maximum_segment_length = None

        # The average segment length in the section
        self.average_segment_length = None

        # Average section radius
        self.average_radius = None
        
        # The total surface are of the section
        self.surface_area = None

        # The surface area of the smallest segment in the section
        self.minimum_segment_surface_are = None

        # The surface area of the largest segment in the section
        self.maximum_segment_surface_area = None

        # The average segment surface area in the section
        self.average_segment_surface_area = None

        # The total volume of the section
        self.volume = None

        # The volume of the smallest segment in the section
        self.minimum_segment_volume = None

        # The volume of the largest segment in the section
        self.maximum_segment_volume = None

        # The average segment volume in the section
        self.average_segment_volume = None


