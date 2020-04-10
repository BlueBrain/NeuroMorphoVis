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
# @Rendering
####################################################################################################
class Rendering:
    """Rendering options
    """

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @View
    ################################################################################################
    class View:
        """Rendering view options
        """

        # Close up view
        CLOSE_UP = 'RENDERING_CLOSE_UP_VIEW'

        # The view will include the reconstructed arbors only
        MID_SHOT = 'RENDERING_MID_SHORT_VIEW'

        # Full view
        WIDE_SHOT = 'RENDERING_WIDE_SHOT_VIEW'

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

            # Close up view
            if argument == 'close-up':
                return Rendering.View.CLOSE_UP

            # Mid-shot view
            elif argument == 'mid-shot':
                return Rendering.View.MID_SHOT

            # Wide-shot view
            elif argument == 'wide-shot':
                return Rendering.View.WIDE_SHOT

            # By default use the wide shot view
            else:
                return Rendering.View.WIDE_SHOT

    ################################################################################################
    # @Resolution
    ################################################################################################
    class Resolution:
        """Rendering resolution options
        """

        # Rendering to scale (for figures)
        TO_SCALE = 'RENDER_TO_SCALE'

        # Rendering based on a user defined resolution
        FIXED= 'RENDER_FIXED_RESOLUTION'

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

            # To scale
            if argument == 'to-scale':
                return Rendering.Resolution.TO_SCALE

            # Fixed resolution
            elif argument == 'fixed':
                return Rendering.Resolution.FIXED

            # By default render at the specified resolution
            else:
                return Rendering.Resolution.FIXED