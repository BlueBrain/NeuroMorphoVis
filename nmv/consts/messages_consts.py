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
# Messages
####################################################################################################
class Messages:
    """Messages
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Output directory not set
    PATH_NOT_SET = "Output directory is not set, update it in the Input / Output Data panel"

    # Invalid output path
    INVALID_OUTPUT_PATH = "Invalid output directory, update it in the Input / Output Data panel"

    # Invalid view
    INVALID_RENDERING_VIEW = "Invalid rendering view"

    # Spaces
    SPACES = '                                                                                     '

