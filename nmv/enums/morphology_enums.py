####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
# @Morphology
####################################################################################################
class Morphology:
    """Morphology enumerators"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Format
    ################################################################################################
    class Format:
        """Morphology format enumerators"""

        # SWC format
        SWC = 'SWC_MORPHOLOGY_FORMAT'

        # H5 format
        H5 = 'H5_MORPHOLOGY_FORMAT'

        # ASCII format
        ASCII = 'ASCII_MORPHOLOGY_FORMAT'
