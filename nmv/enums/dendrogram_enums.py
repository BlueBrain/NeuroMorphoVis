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
# @Dendrogram
####################################################################################################
class Dendrogram:
    """Dendrogram enumerators"""

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Type
    ################################################################################################
    class Type:
        """Dendrogram type enumerators"""

        # Draw a simplified dendrogram with a fixed radius at all the samples
        SIMPLIFIED = 'DENDROGRAM_SIMPLIFIED'

        # Draw a detailed dendrogram with varying radii to see the frequency of the tapering
        DETAILED = 'DENDROGRAM_DETAILED'

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
            """Get the dendrogram type enumerator from a string

            :param argument:
                The string to get the dendrogram type from.
            :return:
                The dendrogram type enumerator.
            """ 

            # Fixed radius
            if argument == 'simplified':
                return Dendrogram.Type.SIMPLIFIED

            # Varying radius
            elif argument == 'detailed':
                return Dendrogram.Type.DETAILED

            # Default
            else:
                return Dendrogram.Type.SIMPLIFIED
