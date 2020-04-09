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
# @Skeleton
####################################################################################################
class Skeleton:
    """Skeleton enumerators
    """

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Method
    ################################################################################################
    class Method:

        # Connect the original sections without repairing any artifacts in the morphology
        CONNECTED_SECTIONS = 'SKELETON_CONNECTED_SECTION'

        # Disconnect the sections and draw each of them as an independent object
        DISCONNECTED_SECTIONS = 'SKELETON_DISCONNECTED_SECTIONS'

        # Progressive reconstruction of the morphology
        PROGRESSIVE = 'SKELETON_PROGRESSIVE'

        # Connected skeleton where all the skeleton lines will be connected together in a one object
        CONNECTED_SKELETON = 'SKELETON_CONNECTED_SKELETON'

        # Samples
        SAMPLES = 'SKELETON_SAMPLES'

        # Similar to DISCONNECTED_SECTIONS, and add an articulation sphere to connect the sections
        ARTICULATED_SECTIONS = 'SKELETON_ARTICULATED_SECTIONS'

        # Disconnect the segments and draw each of them as an independent object
        DISCONNECTED_SEGMENTS = 'SKELETON_DISCONNECTED_SEGMENTS'

        # Dendrogram mode
        DENDROGRAM = 'SKELETON_DENDROGRAM'

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
                return Skeleton.Method.DISCONNECTED_SEGMENTS

            # Connected sections
            elif argument == 'samples':
                return Skeleton.Method.SAMPLES

            # Connected sections
            elif argument == 'progressive':
                return Skeleton.Method.PROGRESSIVE

            # Disconnected sections
            elif argument == 'disconnected-sections':
                return Skeleton.Method.DISCONNECTED_SECTIONS

            # Articulated sections
            elif argument == 'articulated-sections':
                return Skeleton.Method.ARTICULATED_SECTIONS

            # Connected sections
            elif argument == 'connected-sections':
                return Skeleton.Method.CONNECTED_SECTIONS

            # Dendrogram
            elif argument == 'dendrogram':
                return Skeleton.Method.DENDROGRAM

            # Default
            else:
                return Skeleton.Method.DISCONNECTED_SECTIONS

    ################################################################################################
    # @Style
    ################################################################################################
    class Style:
        """The style of the skeleton enumerators
        """

        # Use the original morphology skeleton
        ORIGINAL = 'SKELETON_STYLE_ORIGINAL'

        # Project the skeleton to XY plane
        PLANAR = 'SKELETON_STYLE_PLANAR'

        # Create a tapered morphology skeleton
        TAPERED = 'SKELETON_STYLE_TAPERED'

        # Create a zigzagged morphology skeleton
        ZIGZAG = 'SKELETON_STYLE_ZIGZAG'

        # Project the skeleton to XY plane and make it zigzag
        PLANAR_ZIGZAG = 'SKELETON_STYLE_PLANAR_ZIGZAG'

        # Create a zigzagged and tapered morphology skeleton
        TAPERED_ZIGZAG = 'SKELETON_STYLE_TAPERED_ZIGZAG'

        # Simplified
        SIMPLIFIED = 'SKELETON_STYLE_SIMPLIFIED'

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
                return Skeleton.Style.ORIGINAL

            elif argument == 'planar':
                return Skeleton.Style.PLANAR

            # Tapered
            elif argument == 'tapered':
                return Skeleton.Style.TAPERED

            # Zigzag
            elif argument == 'zigzag':
                return Skeleton.Style.ZIGZAG

            # Tapered zigzag
            elif argument == 'tapered-zigzag':
                return Skeleton.Style.TAPERED_ZIGZAG

            elif argument == 'planar-zigzag':
                return Skeleton.Style.PLANAR_ZIGZAG

            # Tapered zigzag
            elif argument == 'simplified':
                return Skeleton.Style.SIMPLIFIED

            # By default use the original skeleton
            else:
                return Skeleton.Style.ORIGINAL

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
                return Skeleton.Branching.ANGLES

            # Radii
            elif argument == 'radii':
                return Skeleton.Branching.RADII

            # By default angles
            else:
                return Skeleton.Branching.ANGLES

    ################################################################################################
    # @Resampling
    ################################################################################################
    class Resampling:
        """Resampling method
        """

        # Do not resample the section
        NONE = 'RESAMPLING_NONE'

        # Adaptive relaxed resampling (samples do NOT touch each other)
        ADAPTIVE_RELAXED = 'RESAMPLING_ADAPTIVE_RELAXED'

        # Adaptive packed resampling (samples overlap as if we PACK the resampled section)
        ADAPTIVE_PACKED = 'RESAMPLING_ADAPTIVE_PACKED'

        # Resample the section at a fixed step
        FIXED_STEP = 'RESAMPLING_FIXED_STEP'

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

            # None
            if argument == 'none':
                return Skeleton.Resampling.NONE

            # Adaptive relaxed
            elif argument == 'adaptive-relaxed':
                return Skeleton.Resampling.ADAPTIVE_RELAXED

            # Adaptive packed
            elif argument == 'adaptive-packed':
                return Skeleton.Resampling.ADAPTIVE_PACKED

            # Fixed step
            elif argument == 'fixed':
                return Skeleton.Resampling.FIXED_STEP

            # By default none
            else:
                return Skeleton.Resampling.NONE

    ################################################################################################
    # @ArborsRadii
    ################################################################################################
    class ArborsRadii:
        """Radii of the samples along the arbors
        """

        # Use the original radii that were reported in the morphology file
        ORIGINAL = 'ARBORS_RADII_ORIGINAL'

        # Set the radii of all the samples in the morphology to a unified value given by the user
        UNIFIED = 'ARBORS_RADII_UNIFIED'

        # Set the radii of all the samples in a given arbor type to a unified value given by users
        UNIFIED_PER_ARBOR_TYPE = 'ARBORS_RADII_UNIFIED_PER_ARBOR_TYPE'

        # Scale the radii of the samples in the entire morphology using a user-defined scale factor
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
                return Skeleton.ArborsRadii.ORIGINAL

            # Scaled
            elif argument == 'scaled':
                return Skeleton.ArborsRadii.SCALED

            # Fixed
            elif argument == 'fixed':
                return Skeleton.ArborsRadii.UNIFIED

            # Filtered
            elif argument == 'filtered':
                return Skeleton.ArborsRadii.FILTERED

            # By default, as specified in the morphology file
            else:
                return Skeleton.ArborsRadii.ORIGINAL

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
                    return Skeleton.Rendering.View.CLOSE_UP_VIEW

                # Mid-shot view
                elif argument == 'mid-shot':
                    return Skeleton.Rendering.View.MID_SHOT_VIEW

                # Wide-shot view
                elif argument == 'wide-shot':
                    return Skeleton.Rendering.View.WIDE_SHOT_VIEW

                # By default use the wide shot view
                else:
                    return Skeleton.Rendering.View.WIDE_SHOT_VIEW

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
                    return Skeleton.Rendering.Resolution.TO_SCALE

                # Fixed resolution
                elif argument == 'fixed':
                    return Skeleton.Rendering.Resolution.FIXED_RESOLUTION

                # By default render at the specified resolution
                else:
                    return Skeleton.Rendering.Resolution.FIXED_RESOLUTION
