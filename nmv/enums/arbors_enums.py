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

            # By default, use the original skeleton radii as specified in the morphology
            else:
                return Arbors.Radii.AS_SPECIFIED

    ################################################################################################
    # @Roots
    ################################################################################################
    class Roots:
        """The status of the roots of the arbors
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        # The arbors are disconnected from the soma
        DISCONNECTED_FROM_SOMA = 'ARBORS_ROOTS_DISCONNECTED_FROM_SOMA'

        # The arbors are connected to the soma if they are primary with no intersection
        CONNECTED_TO_SOMA = 'ARBORS_ROOTS_CONNECTED_TO_SOMA'

        # The arbors are connected to the origin (0, 0, 0) if they are primary
        CONNECTED_TO_ORIGIN = 'ARBORS_ROOTS_CONNECTED_TO_ORIGIN'

        # All the arbors are connected to the origin even if some of them are not physically
        # connected to the soma. This mode is used for piecewise meshing
        ALL_CONNECTED_TO_ORIGIN = 'ARBORS_ROOTS_ALL_CONNECTED_TO_ORIGIN'

    ################################################################################################
    # @Style
    ################################################################################################
    class Style:
        """Arbors style enumerators
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        # Original as reported in the morphology
        ORIGINAL = 'ARBORS_STYLE_ORIGINAL'

        # Tapered (from thick to thin branches)
        TAPERED = 'ARBORS_STYLE_TAPERED'

        # Zigzag
        ZIGZAG = 'ARBORS_STYLE_ZIGZAG'

        # Tapered and zigzagged
        TAPERED_ZIGZAG = 'ARBORS_STYLE_TAPER_ZIGZAG'

        # Projected on the XY plane @Z=0
        PROJECTED = 'ARBORS_STYLE_PROJECTED'

        # Bumpy, for meshing only
        BUMPY = 'ARBORS_STYLE_BUMPY'

        # Bumpy and zigzagged, for meshing only
        BUMPY_ZIGZAG = 'ARBORS_STYLE_BUMPY_ZIGZAG'

        # Straight, only connects the first and the last two samples of a section
        STRAIGHT = 'ARBORS_STYLE_STRAIGHT'

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # Fixed radii arbors
            if argument == 'tapered':
                return Arbors.Style.TAPERED

            # Use the zigzag style
            elif argument == 'zigzag':
                return Arbors.Style.ZIGZAG

            # Use the tapered-zigzag style
            elif argument == 'tapered-zigzag':
                return Arbors.Style.TAPERED_ZIGZAG

            # Use the projected style
            elif argument == 'projected':
                return Arbors.Style.PROJECTED

            # Use the bumpy style
            elif argument == 'bumpy':
                return Arbors.Style.BUMPY

            # Use the bumpy-zigzag style
            elif argument == 'bumpy-zigzag':
                return Arbors.Style.BUMPY_ZIGZAG

            # By default, use the original style
            else:
                return Arbors.Style.ORIGINAL

        ############################################################################################
        # A list of all the available styles in NeuroMorphoVis for morphology reconstruction
        ############################################################################################
        MORPHOLOGY_STYLE_ITEMS = [
            (ORIGINAL,
             'Original',
             'Draw the arbors as described in the morphology file'),
            (TAPERED,
             'Tapered',
             'Draw the sections as tapered cylinders (artistic)'),
            (ZIGZAG,
             'Zigzag',
             'Draw the sections as wiggled zigzag lines (artistic)'),
            (TAPERED_ZIGZAG,
             'Tapered-Zigzag',
             'Draw the sections as tapered and wiggled zigzag tubes (artistic)'),
            (STRAIGHT,
             'Straight',
             'Represent each section by a single segment that connects its terminals (artistic)')
        ]


