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
# @Skeletonization
####################################################################################################
class Skeletonization:
    """Skeletonization enumerators
    """

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Skeleton
    ################################################################################################
    class Skeleton:
        """Skeletonization
        """

        # Use the original morphology skeleton
        ORIGINAL = 'MESHING_SKELETON_ORIGINAL'

        # Create a tapered morphology skeleton
        TAPERED = 'MESHING_SKELETON_TAPERED'

        # Create a zigzagged morphology skeleton
        ZIGZAG = 'MESHING_SKELETON_ZIGZAG'

        # Create a zigzagged and ta[ered morphology skeleton
        TAPERED_ZIGZAG = 'MESHING_SKELETON_TAPERED_ZIGZAG'

        # Simplified
        SIMPLIFIED = 'MESHING_SKELETON_SIMPLIFIED'

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

            # Original
            if argument == 'original':
                return Skeletonization.Skeleton.ORIGINAL

            # Tapered
            elif argument == 'tapered':
                return Skeletonization.Skeleton.TAPERED

            # Zigzag
            elif argument == 'zigzag':
                return Skeletonization.Skeleton.ZIGZAG

            # Tapered zigzag
            elif argument == 'tapered-zigzag':
                return Skeletonization.Skeleton.TAPERED_ZIGZAG

            # Tapered zigzag
            elif argument == 'simplified':
                return Skeletonization.Skeleton.SIMPLIFIED

            # By default use the original skeleton
            else:
                return Skeletonization.Skeleton.ORIGINAL

    ################################################################################################
    # @Method
    ################################################################################################
    class Method:

        # Connect the original sections without repairing any artifacts in the morphology
        CONNECTED_SECTION_ORIGINAL = 'SKELETONIZATION_CONNECTED_SECTION_ORIGINAL'

        # Connect the original sections after repairing the artifacts in the morphology
        CONNECTED_SECTION_REPAIRED = 'SKELETONIZATION_CONNECTED_SECTION_REPAIRED'

        # Disconnect the sections and draw each of them as an independent object
        DISCONNECTED_SECTIONS = 'SKELETONIZATION_DISCONNECTED_SECTIONS'

        # Samples
        SAMPLES = 'SKELETONIZATION_SAMPLES'

        # Similar to DISCONNECTED_SECTIONS, and add an articulation sphere to connect the sections
        ARTICULATED_SECTIONS = 'SKELETONIZATION_ARTICULATED_SECTIONS'

        # Disconnect the segments and draw each of them as an independent object
        DISCONNECTED_SEGMENTS = 'SKELETONIZATION_DISCONNECTED_SEGMENTS'

        # Draw the skeleton and disconnect the secondary branching arbors using original morphology
        DISCONNECTED_SKELETON_ORIGINAL = 'SKELETONIZATION_DISCONNECTED_SKELETON_ORIGINAL'

        # Draw the skeleton and disconnect the secondary branches after repairing the arbors
        DISCONNECTED_SKELETON_REPAIRED = 'SKELETONIZATION_DISCONNECTED_SKELETON_REPAIRED'

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

            # Disconnected segments
            if argument == 'disconnected-segments':
                return Skeletonization.Method.DISCONNECTED_SEGMENTS

                # Connected sections
            elif argument == 'samples':
                return Skeletonization.Method.SAMPLES

            # Disconnected sections
            elif argument == 'disconnected-sections':
                return Skeletonization.Method.DISCONNECTED_SECTIONS

            # Articulated sections
            elif argument == 'articulated-sections':
                return Skeletonization.Method.ARTICULATED_SECTIONS

            # Connected sections
            elif argument == 'connected-sections':
                return Skeletonization.Method.CONNECTED_SECTION_ORIGINAL

            # Connected sections
            elif argument == 'connected-sections-repaired':
                return Skeletonization.Method.CONNECTED_SECTION_REPAIRED

            # Default
            else:
                return Skeletonization.Method.CONNECTED_SECTION_ORIGINAL

    ################################################################################################
    # @Branching
    ################################################################################################
    class Branching:
        """Branching method
        """

        # Make the branching based on the angles between the branches
        ANGLES = 'ANGLE_BASED_BRANCHING'

        # Make the branching based in the radii between the branches
        RADII = 'RADII_BASED_BRANCHING'

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

            # Angles
            if argument == 'radii':
                return Skeletonization.Branching.ANGLES

            # Radii
            elif argument == 'radii':
                return Skeletonization.Branching.RADII

            # By default angles
            else:
                return Skeletonization.Branching.ANGLES

    ################################################################################################
    # @ArborsRadii
    ################################################################################################
    class ArborsRadii:
        """Radii of the samples along the arbors
        """

        # Set the radii of the arbors as specified in the morphology file
        AS_SPECIFIED = 'ARBORS_RADII_AS_SPECIFIED'

        # Set the radii of the arbors to a fixed value
        FIXED = 'ARBORS_RADII_FIXED'

        # Scale the radii of the arbors using a constant factor
        SCALED = 'ARBORS_RADII_SCALED'

        # Filter the radii at a given threshold radius
        FILTERED = 'ARBORS_RADII_FILTERED'

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

            # As specified in the morphology file
            if argument == 'default':
                return Skeletonization.ArborsRadii.AS_SPECIFIED

            # Scaled
            elif argument == 'scaled':
                return Skeletonization.ArborsRadii.SCALED

            # Fixed
            elif argument == 'fixed':
                return Skeletonization.ArborsRadii.FIXED

            # Filtered
            elif argument == 'filtered':
                return Skeletonization.ArborsRadii.FILTERED

            # By default, as specified in the morphology file
            else:
                return Skeletonization.ArborsRadii.AS_SPECIFIED

    ################################################################################################
    # @Rendering
    ################################################################################################
    class Rendering:
        """Rendering options
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        ########################################################################################
        # @View
        ########################################################################################
        class View:
            """Rendering view options
            """

            # Close up view
            CLOSE_UP_VIEW = 'RENDERING_SKELETON_CLOSE_UP_VIEW'

            # The view will include the reconstructed arbors only
            MID_SHOT_VIEW = 'RENDERING_SKELETON_MID_SHORT_VIEW'

            # Full morphology view
            WIDE_SHOT_VIEW = 'RENDERING_SKELETON_WIDE_SHOT_VIEW'

            ####################################################################################
            # @__init__
            ####################################################################################
            def __init__(self):
                pass

            ####################################################################################
            # @get_enum
            ####################################################################################
            @staticmethod
            def get_enum(argument):

                # Close up view
                if argument == 'close-up':
                    return Skeletonization.Rendering.View.CLOSE_UP_VIEW

                # Mid-shot view
                elif argument == 'mid-shot':
                    return Skeletonization.Rendering.View.MID_SHOT_VIEW

                # Wide-shot view
                elif argument == 'wide-shot':
                    return Skeletonization.Rendering.View.WIDE_SHOT_VIEW

                # By default use the wide shot view
                else:
                    return Skeletonization.Rendering.View.WIDE_SHOT_VIEW

        ########################################################################################
        # @Resolution
        ########################################################################################
        class Resolution:
            """Rendering resolution options
            """

            # Rendering to scale (for figures)
            TO_SCALE = 'RENDER_SKELETON_TO_SCALE'

            # Rendering based on a user defined resolution
            FIXED_RESOLUTION = 'RENDER_SKELETON_FIXED_RESOLUTION'

            ########################################################################################
            # @__init__
            ########################################################################################
            def __init__(self):
                pass

            ########################################################################################
            # @get_enum
            ########################################################################################
            @staticmethod
            def get_enum(argument):

                # To scale
                if argument == 'to-scale':
                    return Skeletonization.Rendering.Resolution.TO_SCALE

                # Fixed resolution
                elif argument == 'fixed':
                    return Skeletonization.Rendering.Resolution.FIXED_RESOLUTION

                # By default render at the specified resolution
                else:
                    return Skeletonization.Rendering.Resolution.FIXED_RESOLUTION
