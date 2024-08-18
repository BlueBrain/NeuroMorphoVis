####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
# @Image
####################################################################################################
class Image:
    """Image constants"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Minimum image resolution (for sliders)
    MIN_RESOLUTION = 256

    # Maximum image resolution (for sliders)
    MAX_RESOLUTION = 10240

    # Default full view resolution
    FULL_VIEW_RESOLUTION = 1024

    # Default close up view resolution
    CLOSEUP_RESOLUTION = 1024

    # Default close up dimensions (in microns)
    CLOSEUP_DIMENSIONS = 20

    # The bounding box increment that will clean the edges around the images
    GAP_DELTA = 5.0

    # Default image resolution
    DEFAULT_RESOLUTION = 1024

    # Default value for the image scale factor
    DEFAULT_IMAGE_SCALE_FACTOR = 1.0

    # Default samples per pixels
    DEFAULT_SPP = 8

    # Flat samples per pixels
    FLAT_SPP = 2
