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
# @Camera
####################################################################################################
class Camera:
    """Camera enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @View
    ################################################################################################
    class View:
        """Camera view enumerator
        """

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
            """Return the camera view enumerator.

            :param argument:
                Input argument.
            :return:
                Camera view enumerator.
            """

            # Front
            if argument == 'front':
                return Camera.View.FRONT

            # Side
            elif argument == 'side':
                return Camera.View.SIDE

            # Top
            elif argument == 'top':
                return Camera.View.TOP

            # Front for 360 rendering
            elif argument == 'front-360':
                return Camera.View.FRONT_360

            # Default, use the front view
            else:
                return Camera.View.FRONT

        # Front view
        FRONT = 'FRONT'

        # Side view
        SIDE = 'SIDE'

        # Top view
        TOP = 'TOP'

        # 360
        FRONT_360 = 'FRONT_360_VIEW'

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # Front
            if argument == 'front':
                return Camera.View.FRONT

            # Side
            elif argument == 'side':
                return Camera.View.SIDE

            # Top
            elif argument == 'top':
                return Camera.View.TOP

            # 360 from front view
            elif argument == '360':
                return Camera.View.FRONT_360

            # By default, use the front view
            else:
                return Camera.View.FRONT

    ################################################################################################
    # @Projection
    ################################################################################################
    class Projection:
        """Camera projection enumerator
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        # Orthographic
        ORTHOGRAPHIC = 'ORTHOGRAPHIC_VIEW'

        # Perspective
        PERSPECTIVE = 'PERSPECTIVE_VIEW'

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # Orthographic
            if argument == 'orthographic':
                return Camera.Projection.ORTHOGRAPHIC

            # Perspective
            elif argument == 'perspective':
                return Camera.Projection.PERSPECTIVE

            # By default, use orthographic
            else:
                return Camera.Projection.ORTHOGRAPHIC

