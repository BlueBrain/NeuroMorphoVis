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
# @Geometry
####################################################################################################
class Geometry:
    """Geometry constants.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Scale bar main edge size (in blender units)
    SCALE_BAR_MAIN_EDGE_SIZE = 0.15

    # Scale bar center edge size (in blender units)
    SCALE_BAR_CENTER_EDGE_SIZE = 0.075

    # Scale bar negative shift for alignment
    SCALE_BAR_NEGATIVE_SHIFT = 0.05

    # Scale bar thickness (in blender units)
    SCALE_BAR_THICKNESS = 0.025
