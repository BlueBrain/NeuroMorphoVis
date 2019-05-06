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
# @Meshing
####################################################################################################
class Meshing:
    """Meshing enumerators
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

        # Create a zigzagged and tapered morphology skeleton
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
                return Meshing.Skeleton.ORIGINAL

            # Tapered
            elif argument == 'tapered':
                return Meshing.Skeleton.TAPERED

            # Zigzag
            elif argument == 'zigzag':
                return Meshing.Skeleton.ZIGZAG

            # Tapered zigzag
            elif argument == 'tapered-zigzag':
                return Meshing.Skeleton.TAPERED_ZIGZAG

            # Tapered zigzag
            elif argument == 'simplified':
                return Meshing.Skeleton.SIMPLIFIED

            # By default use the original skeleton
            else:
                return Meshing.Skeleton.ORIGINAL

    ################################################################################################
    # @Technique
    ################################################################################################
    class Technique:
        """Meshing techniques
        """

        # Piecewise watertight meshing
        PIECEWISE_WATERTIGHT = 'MESHING_TECHNIQUE_PIECEWISE_WATERTIGHT'

        # Bridging meshing
        BRIDGING = 'MESHING_TECHNIQUE_BRIDGING'

        # Union meshing
        UNION = 'MESHING_TECHNIQUE_UNION'

        # Extrusion meshing
        EXTRUSION = 'MESHING_TECHNIQUE_EXTRUSION'

        # Skinning
        SKINNING = 'MESHING_TECHNIQUE_SKINNING'

        # Meta objects-based meshing
        META_OBJECTS = 'MESHING_TECHNIQUE_META_OBJECTS'

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

            # Piecewise-watertight
            if argument == 'piecewise-watertight':
                return Meshing.Technique.PIECEWISE_WATERTIGHT

            # Union
            elif argument == 'union':
                return Meshing.Technique.UNION

            # Bridging
            elif argument == 'bridging':
                return Meshing.Technique.BRIDGING

            # Extrusion
            elif argument == 'extrusion':
                return Meshing.Technique.EXTRUSION

            # Skinning
            elif argument == 'skinning':
                return Meshing.Technique.SKINNING

            # Meta objects
            elif argument == 'meta-balls':
                return Meshing.Technique.META_OBJECTS

            # By default use piecewise-watertight
            else:
                return Meshing.Technique.PIECEWISE_WATERTIGHT

    ################################################################################################
    # @Technique
    ################################################################################################
    class SomaConnection:
        """Soma connection to the arbors
        """

        # Connected
        CONNECTED = 'SOMA_CONNECTED_TO_ARBORS'

        # Disconnected
        DISCONNECTED = 'SOMA_DISCONNECTED_FROM_ARBORS'

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

            # Soma is connected to the arbors
            if argument == 'connected':
                return Meshing.SomaConnection.CONNECTED

            # Soma is disconnected from the arbors
            elif argument == 'disconnected':
                return Meshing.SomaConnection.DISCONNECTED

            # By default use the soma disconnected mode
            else:
                return Meshing.SomaConnection.DISCONNECTED

    ################################################################################################
    # @ArborsConnection
    ################################################################################################
    class ObjectsConnection:
        """Objects connected to each others via joint operation
        """

        # Connected
        CONNECTED = 'CONNECTED_OBJECTS'

        # Disconnected
        DISCONNECTED = 'DISCONNECTED_OBJECTS'

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

            # All the objects are connected to a single mesh object
            if argument == 'connected':
                return Meshing.ObjectsConnection.CONNECTED

            # The objects are disconnected from each others
            elif argument == 'disconnected':
                return Meshing.ObjectsConnection.DISCONNECTED

            # By default use the mesh objects are disconnected
            else:
                return Meshing.ObjectsConnection.DISCONNECTED

    ################################################################################################
    # @Edges
    ################################################################################################
    class Edges:
        """Arbors edges
        """

        # Smooth edges
        SMOOTH = 'ARBORS_SMOOTH_EDGES'

        # Hard edges
        HARD = 'ARBORS_HARD_EDGES'

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

            # Use smooth edges
            if argument == 'smooth':
                return Meshing.Edges.SMOOTH

            # Use hard edges
            elif argument == 'hard':
                return Meshing.Edges.HARD

            # By default use hard edges
            else:
                return Meshing.Edges.HARD

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

            # Angle
            if argument == 'angles':
                return Meshing.Branching.ANGLES

            # Radii
            elif argument == 'radii':
                return Meshing.Branching.RADII

            # By default return angles
            else:
                return Meshing.Branching.ANGLES

    ################################################################################################
    # @Model
    ################################################################################################
    class Surface:
        """Reconstructed model quality, is it realistic quality or beauty
        """

        # Smooth surface
        SMOOTH = 'SURFACE_ROUGH'

        # Add noise to the surface to make it rough
        ROUGH = 'SURFACE_SMOOTH'

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

            # Rough surface
            if argument == 'rough':
                return Meshing.Surface.ROUGH

            # Smooth surface
            elif argument == 'smooth':
                return Meshing.Surface.SMOOTH

            # By default construct a smooth surface
            else:
                return Meshing.Surface.SMOOTH

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
            CLOSE_UP_VIEW = 'RENDERING_MESH_CLOSE_UP_VIEW'

            # Full morphology view
            MID_SHOT_VIEW = 'RENDERING_MESH_MID_SHORT_VIEW'

            # Full morphology view
            WIDE_SHOT_VIEW = 'RENDERING_MESH_WIDE_SHOT_VIEW'

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
                    return Meshing.Rendering.View.CLOSE_UP_VIEW

                # Mid-shot view
                elif argument == 'mid-shot':
                    return Meshing.Rendering.View.MID_SHOT_VIEW

                # Wide-shot view
                elif argument == 'wide-shot':
                    return Meshing.Rendering.View.WIDE_SHOT_VIEW

                # By default use the mid-shot view
                else:
                    return Meshing.Rendering.View.MID_SHOT_VIEW

        ########################################################################################
        # @Resolution
        ########################################################################################
        class Resolution:
            """Rendering resolution options
            """

            # Rendering to scale (for figures)
            TO_SCALE = 'RENDER_MESH_TO_SCALE'

            # Rendering based on a user defined resolution
            FIXED_RESOLUTION = 'RENDER_MESH_FIXED_RESOLUTION'

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
                    return Meshing.Rendering.Resolution.TO_SCALE

                # Fixed resolution
                elif argument == 'fixed':
                    return Meshing.Rendering.Resolution.FIXED_RESOLUTION

                # By default render at the specified resolution
                else:
                    return Meshing.Rendering.Resolution.FIXED_RESOLUTION

    ################################################################################################
    # @UnionMeshing
    ################################################################################################
    class UnionMeshing:
        """Union meshing technique options
        """

        # Quad skeleton
        QUAD_SKELETON = 'UNION_QUAD_SKELETON'

        # Circular skeleton
        CIRCULAR_SKELETON = 'UNION_CIRCULAR_SKELETON'

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

    ################################################################################################
    # @Spines
    ################################################################################################
    class Spines:
        """Spines options
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        ############################################################################################
        # @Source
        ############################################################################################
        class Source:
            """Spines source
            """

            # Ignore spines
            IGNORE = 'IGNORE_SPINES'

            # Randomly generated spines
            RANDOM = 'RANDOM_SPINES'

            # Spines integrated in a BBP circuit
            CIRCUIT = 'CIRCUIT_SPINES'

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

                # Ignore spines
                if argument == 'random':
                    return Meshing.Spines.Source.RANDOM

                # Circuit spines
                elif argument == 'circuit':
                    return Meshing.Spines.Source.CIRCUIT

                # By default, ignore loading the spines
                else:
                    return Meshing.Spines.Source.IGNORE

        ############################################################################################
        # @__init__
        ############################################################################################
        class Quality:
            """Spines quality
            """

            # High quality
            HQ = 'SPINES_HQ'

            # Low quality
            LQ = 'SPINES_LQ'

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

                # High quality
                if argument == 'hq':
                    return Meshing.Spines.Quality.HQ

                # By default, use low quality spines
                else:
                    return Meshing.Spines.Quality.LQ

    ################################################################################################
    # @Nucleus
    ################################################################################################
    class Nucleus:
        """Nucleus options
        """

        # Ignore
        IGNORE = 'IGNORE_NUCLEUS'

        # Integrated
        INTEGRATED = 'INTEGRATED_NUCLEUS'

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        ############################################################################################
        # @__init__
        ############################################################################################
        class Quality:
            """Nucleus mesh quality
            """

            # High quality
            HQ = 'NUCLEUS_HQ'

            # Low quality
            LQ = 'NUCLEUS_LQ'

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

                # High quality
                if argument == 'hq':
                    return Meshing.Nucleus.Quality.HQ

                # By default, use low quality nucleus
                else:
                    return Meshing.Nucleus.Quality.LQ

    ################################################################################################
    # @ExportFormat
    ################################################################################################
    class ExportFormat:
        """The file format of the exported meshes
        """

        # .ply
        PLY = 'EXPORT_FORMAT_PLY'

        # .stl
        STL = 'EXPORT_FORMAT_STL'

        # .obj
        OBJ = 'EXPORT_FORMAT_OBJ'

        # .off
        OFF = 'EXPORT_FORMAT_OFF'

        # .blend
        BLEND = 'EXPORT_FORMAT_BLEND'

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass
