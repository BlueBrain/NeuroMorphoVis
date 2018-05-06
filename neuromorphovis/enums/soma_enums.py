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
class Soma:
    """Soma enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Representation
    ################################################################################################
    class Representation:
        """Soma representation enumerators
        """

        # Ignore the representation of the soma
        IGNORE = 'SOMA_IGNORE_REPRESENTATION'

        # Use a symbolic representation, sphere
        SPHERE = 'SOMA_SYMBOLIC_SPHERE'

        # Reconstruct a realistic mesh to reflect the three-dimensional contour of the soma
        REALISTIC = 'SOMA_REALISTIC_MESH'

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        ############################################################################################
        # @__init__
        ############################################################################################
        @staticmethod
        def get_enum(argument):
            """Gets the enumerator from the argument directly.

            :param argument:
                Representation argument.
            :return:
                Soma representation enumerator.
            """

            # Ignore the representation of the soma
            if argument == 'ignore':
                return Soma.Representation.IGNORE

            # Sphere representation
            elif argument == 'sphere':
                return Soma.Representation.SPHERE

            # Realistic profile
            else:
                return Soma.Representation.REALISTIC


