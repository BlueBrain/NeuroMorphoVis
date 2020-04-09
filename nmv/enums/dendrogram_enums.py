####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
# @Dendrogram
####################################################################################################
class Dendrogram:
    """Dendrogram enumerators
    """

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Method
    ################################################################################################
    class Radius:

        # Draw the dendrogram with a fixed radius
        FIXED = 'DENDROGRAM_FIXED_RADIUS'

        # Draw the dendrogram with a varying radii to see the frequency of the tapering
        VARYING = 'DENDROGRAM_VARYING_RADIUS'

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # Fixed radius
            if argument == 'fixed':
                return Dendrogram.Radius.FIXED

            # Varying radius
            elif argument == 'varying':
                return Dendrogram.Radius.VARYING

            # Default
            else:
                return Dendrogram.Radius.FIXED
