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
# Morphology
####################################################################################################
class Morphology:
    """Morphology constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # The radius of the sample located at the origin (auxiliary sample)
    ORIGIN_SAMPLE_RADIUS = 0.1

    # The radius of the first sample along a branch
    FIRST_SAMPLE_RADIUS = 0.1

    # The radius of the last sample along a branch
    LAST_SAMPLE_RADIUS = 0.05

    # The scale factor of the radius of the first sample along a branch
    FIRST_SAMPLE_RADIUS_SCALE_FACTOR = 0.5

    # The scale factor of the radius of the last sample along a branch
    LAST_SAMPLE_RADIUS_SCALE_FACTOR = 0.5
