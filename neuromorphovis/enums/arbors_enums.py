####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


####################################################################################################
# @Soma
####################################################################################################
class Arbors:
    """Arbors enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Radii
    ################################################################################################
    class Radii:
        """Arbors radii enumerators
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        # Set the radii of the arbors as specified in the morphology file
        AS_SPECIFIED = 'ARBORS_RADII_AS_SPECIFIED'

        # Set the radii of the arbors to a fixed value
        FIXED = 'ARBORS_RADII_FIXED'

        # Scale the radii of the arbors using a constant factor
        SCALED = 'ARBORS_RADII_SCALED'

        # Filter sections with radii smaller than a threshold value given
        FILTERED = 'ARBORS_RADII_FILTERED'

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # Fixed radii arbors
            if argument == 'fixed':
                return Arbors.Radii.FIXED

            # Scaled radii
            elif argument == 'scaled':
                return Arbors.Radii.SCALED

            # Scaled radii
            elif argument == 'filtered':
                return Arbors.Radii.SCALED

            # By default, use the original skeleton radii as specified in the morphology
            else:
                return Arbors.Radii.AS_SPECIFIED
