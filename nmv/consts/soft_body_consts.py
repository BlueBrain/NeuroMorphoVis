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
# @SoftBody
####################################################################################################
class SoftBody:
    """Soft body constants"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Gravity value
    GRAVITY = 0.0

    # Max value for the goal
    GOAL_MAX = 0.1

    # Min value for the goal
    GOAL_MIN = 0.7

    # Default value for the goal
    GOAL_DEFAULT = 0.5

    # Default value for the subdivision
    SUBDIVISIONS_DEFAULT = 5

    # Default value for the number of steps
    SIMULATION_STEPS_DEFAULT = 100

    # Default value for stiffness
    STIFFNESS_DEFAULT = 0.1

    # Initial soma radius scale factor
    SOMA_SCALE_FACTOR = 0.5
