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


class SegmentData:

    def __init__(self):
        index = 0
        type = 0
        length = 0.0
        analytical_surface_area = 0.0
        geometric_surface_area = 0.0
        analytical_volume = 0.0
        geometrical_volume = 0.0

    def to_string(self):
        pass


class SectionData:

    def __init__(self):
        index = 0
        type = 0
        length = 0.0
        surface_area = 0.0
        volume = 0.0

    def to_string(self):
        pass


class NeuriteData:

    def __init__(self):
        index = 0
        type = 0
        length = 0.0
        surface_area = 0.0
        volume = 0.0

    def to_string(self):
        pass

class MorphologyData:

    def __init__(self):
        pass



def analyze_segment(section, segments_data_list):




    pass

def analyze_section(section, sections_data_list):
    pass
