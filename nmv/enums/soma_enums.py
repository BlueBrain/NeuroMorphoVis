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

    ################################################################################################
    # @Profile
    ################################################################################################
    class Profile:
        """Profile enumerators
        """

        # Use the profile points only
        PROFILE_POINTS_ONLY = 'SOMA_PROFILE_BASED_ON_PROFILE_POINTS_ONLY'

        # Use the arbors
        ARBORS_ONLY = 'SOMA_PROFILE_BASED_ON_ARBORS_ONLY'

        # Use the arbors and the profile points
        COMBINED = 'SOMA_PROFILE_BASED_ON_ARBORS_AND_PROFILE_POINTS'

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
                Soma profile argument.
            :return:
                Soma reconstruction method enumerator.
            """

            # Arbors only
            if argument == 'arbors':
                return Soma.Profile.ARBORS_ONLY

            # Profile points only
            elif argument == 'profile':
                return Soma.Profile.PROFILE_POINTS_ONLY

            elif argument == 'combined':
                return Soma.Profile.COMBINED

            # Arbors only by default
            else:
                return Soma.Profile.ARBORS_ONLY

    ################################################################################################
    # @ReconstructionMethod
    ################################################################################################
    class ReconstructionMethod:
        """Soma reconstruction method enumerators
        """

        # Use soft body physics
        SOFT_BODY_PHYSICS = 'SOMA_RECONSTRUCTION_METHOD_SOFT_BODY_PHYSICS'

        # Use meta balls
        META_BALLS = 'SOMA_RECONSTRUCTION_METHOD_META_BALLS'

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
                Reconstruction argument.
            :return:
                Soma reconstruction method enumerator.
            """

            # Arbors only
            if argument == 'softbody':
                return Soma.ReconstructionMethod.SOFT_BODY_PHYSICS

            # Profile points only
            elif argument == 'metaballs':
                return Soma.ReconstructionMethod.META_BALLS

            # MetaBalls only by default
            else:
                return Soma.ReconstructionMethod.META_BALLS

