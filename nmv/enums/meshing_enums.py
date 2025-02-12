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
# @Meshing
####################################################################################################
class Meshing:
    """Meshing enumerators"""

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Technique
    ################################################################################################
    class Technique:
        """Meshing techniques enumerators"""

        # Piecewise watertight meshing
        PIECEWISE_WATERTIGHT = 'MESHING_TECHNIQUE_PIECEWISE_WATERTIGHT'

        # Using voxelization-based re-meshing
        VOXELIZATION = 'MESHING_TECHNIQUE_VOXELIZATION'

        # Union-operator based meshing
        UNION = 'MESHING_TECHNIQUE_UNION'

        # Skinning modifier-based meshing
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
            """Get the meshing technique enumerator from a string
            :param argument:
                The string to get the meshing technique from.
            :return:
                The meshing technique enumerator.
            """

            if argument == 'piecewise-watertight':
                return Meshing.Technique.PIECEWISE_WATERTIGHT
            elif argument == 'voxelization':
                return Meshing.Technique.VOXELIZATION
            elif argument == 'union':
                return Meshing.Technique.UNION
            elif argument == 'skinning':
                return Meshing.Technique.SKINNING
            elif argument == 'meta-balls':
                return Meshing.Technique.META_OBJECTS
            else:
                return Meshing.Technique.PIECEWISE_WATERTIGHT

        ############################################################################################
        # A list of all the available meshing techniques in NeuroMorphoVis to be displayed in the UI
        ############################################################################################
        MESHING_TECHNIQUE_ITEMS = [

            (PIECEWISE_WATERTIGHT,
             'Piecewise Watertight',
             'This approach (Abdellah et al., 2017) creates a piecewise watertight mesh that is '
             'composed of multiple mesh objects, where each object is a watertight component. '
             'This method is used to reconstruct high fidelity volumes from the generated meshes'),

            (VOXELIZATION,
             'Voxelization',
             'This approach creates a watertight mesh using voxelization-based remeshing in '
             'Blender 3.0 and later'),

            (SKINNING,
             'Skinning',
             'Skinning (Abdellah et al., 2019) uses the skin modifier to reconstruct the branches. '
             'This approach is guaranteed to reconstruct a nice looking branching compared to the '
             'other methods and also guarantees the fidelity of the mesh, but it does not '
             'guarantee watertightness. This technique is used when you need meshes for '
             'visualization with transparency'),

            (UNION,
             'Union',
             'This method uses the union boolean operator to join the different branches together '
             'in a single mesh. It is not guaranteed to generate a watertight or even a valid '
             'mesh, although it works in 90% of the cases, (Abdellah et al., 2022)'),

            (META_OBJECTS,
             'MetaBalls',
             'Creates watertight mesh models using MetaBalls. This approach is extremely slow if '
             'the axons are included in the meshing process, so it is always recommended to use '
             'first order branching for the axons when using this technique')
        ]

    ################################################################################################
    # @TopologyTessellation
    ################################################################################################
    class TopologyTessellation:
        """The topology tessellation method."""

        # Use the re-tessellation of the voxel remesher
        VOXEL_REMESHER = 'TOPOLOGY_TESSELLATION_VOXEL_REMESHER'

        # Use the tessellation of the omesh, if available
        OMESH_TESSELLATION = 'TOPOLOGY_TESSELLATION_OMESH'

        # None
        NO_TESSELLATION = 'TOPOLOGY_TESSELLATION_NONE'

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
            """Get the topology tessellation enumerator from a string
            :param argument:
                The string to get the topology tessellation from.
            :return:
                The topology tessellation enumerator.
            """

            if argument == 'voxel-remesher':
                return Meshing.TopologyTessellation.VOXEL_REMESHER
            elif argument == 'omesh':
                return Meshing.TopologyTessellation.OMESH_TESSELLATION
            elif argument == 'none':
                return Meshing.TopologyTessellation.NO_TESSELLATION
            else:
                return Meshing.TopologyTessellation.NO_TESSELLATION

        ############################################################################################
        # A list of all the available tessellation options in NeuroMorphoVis to be displayed in the UI
        ############################################################################################
        TOPOLOGY_TESSELLATION_ITEMS = [

            (VOXEL_REMESHER,
             'Voxel Remesher Tessellation',
             'This approach  uses the adaptive meshing of the Voxel remesh modifier. It is '
             'relatively faster than than the omesh'),

            (OMESH_TESSELLATION,
             'OMesh Tessellation',
             'This approach uses the OMesh library to re-tessellate the mesh.'),

            (NO_TESSELLATION,
             'Ignore',
             'Ignore re-tessellating the mesh.')
        ]

    ################################################################################################
    # @Proxy
    ################################################################################################
    class Proxy:
        """The method used to create the proxy meshes for the voxelization-based re-meshing."""

        # Use the articulated sections morphology builder
        ARTICULATED_SECTIONS = 'PROXY_ARTICULATED_SECTIONS'

        # Use the connected sections morphology builder
        CONNECTED_SECTIONS = 'PROXY_CONNECTED_SECTIONS'

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
            """Get the proxy meshes method enumerator from a string
            :param argument:
                The string to get the proxy meshes method from.
            :return:
                The proxy meshes method enumerator.
            """

            if argument == 'articulated-sections':
                return Meshing.Proxy.ARTICULATED_SECTIONS
            elif argument == 'connected-sections':
                return Meshing.Proxy.CONNECTED_SECTIONS
            else:
                return Meshing.Proxy.ARTICULATED_SECTIONS

        ############################################################################################
        # A list of all the available proxy options in NeuroMorphoVis to be displayed in the UI
        ############################################################################################
        PROXY_MESHES_METHODS = [

            (ARTICULATED_SECTIONS,
             'Articulated Sections',
             'Use the articulated sections morphology builder to build the proxy mesh that is '
             'used later to construct the final mesh. The articulated sections builder builds '
             'every section in the morphology independently and then adds spheres at the terminal '
             'points of every section to make a continuation of the path from the parent sections '
             'to the child ones.'),

            (CONNECTED_SECTIONS,
             'Connected Sections',
             'Use the connected sections morphology building style to build the proxy mesh that is '
             'used later to construct the final mesh. This method constructs a single mesh for a '
             'full path from a root node to a leaf one. This method is more robust than the '
             'Articulated Sections.')
        ]

    ################################################################################################
    # @PiecewiseFilling
    ################################################################################################
    class PiecewiseFilling:
        """The filling of the piecewise meshing."""

        # Fill the skeleton using one mesh per path from a root to a leaf section
        PATHS = 'PIECEWISE_FILLING_PATHS'

        # Fill the skeleton using sections and articulations at the bifurcation points
        SECTIONS = 'PIECEWISE_FILLING_SECTIONS'

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
            """Get the piecewise filling enumerator from a string
            :param argument:
                The string to get the piecewise filling from.
            :return:
                The piecewise filling enumerator.
            """

            # Paths
            if argument == 'paths':
                return Meshing.PiecewiseFilling.PATHS

            # Sections
            elif argument == 'sections':
                return Meshing.PiecewiseFilling.SECTIONS

            # By default, use the paths
            else:
                return Meshing.PiecewiseFilling.PATHS

    ################################################################################################
    # @Technique
    ################################################################################################
    class SomaConnection:
        """Soma connection to the arbors."""

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
            """Get the soma connection enumerator from a string
            :param argument:
                The string to get the soma connection from.
            :return:
                The soma connection enumerator.
            """

            # Soma is connected to the arbors
            if argument == 'connected':
                return Meshing.SomaConnection.CONNECTED

            # Soma is disconnected from the arbors
            elif argument == 'disconnected':
                return Meshing.SomaConnection.DISCONNECTED

            # By default, use the soma disconnected mode
            else:
                return Meshing.SomaConnection.DISCONNECTED

    ################################################################################################
    # @ArborsConnection
    ################################################################################################
    class ObjectsConnection:
        """Objects connected to each others via joint operation"""

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
            """Get the objects connection enumerator from a string
            :param argument:
                The string to get the objects connection from.
            :return:
                The objects connection enumerator.
            """

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
        """Arbors edges enumerators"""

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
    # @Model
    ################################################################################################
    class Surface:
        """Reconstructed model quality, is it realistic quality or beauty."""

        # Smooth surface
        SMOOTH = 'SURFACE_SMOOTH'

        # Add noise to the surface to make it rough
        ROUGH = 'SURFACE_ROUGH'

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
            """Get the surface quality enumerator from a string
            :param argument:
                The string to get the surface quality from.
            :return:
                The surface quality enumerator.
            """ 

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
    # @UnionMeshing
    ################################################################################################
    class UnionMeshing:
        """Union meshing technique options."""

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
        """Spines options."""

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        ############################################################################################
        # @Source
        ############################################################################################
        class Source:
            """Spines source."""

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
            """Spines quality."""

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
                """Get the spines quality enumerator from a string
                :param argument:
                    The string to get the spines quality from.
                :return:
                    The spines quality enumerator.
                """

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
        """Nucleus options."""

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
            """Nucleus mesh quality"""

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
                """Get the nucleus quality enumerator from a string
                :param argument:
                    The string to get the nucleus quality from.
                :return:
                    The nucleus quality enumerator.
                """

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
        """The file format of the exported meshes."""

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

        ############################################################################################
        # A list of all the export formats to be displayed in the UI
        ############################################################################################
        FORMATS_ITEMS = [

            # PLY format
            (PLY, 'Stanford (.ply)', 'Export the mesh to a .ply file'),

            # OBJ format
            (OBJ, 'Wavefront (.obj)', 'Export the mesh to a .obj file'),

            # STL format
            (STL, 'Stereolithography CAD (.stl)', 'Export the mesh to an .stl file'),

            # BLEND format
            (BLEND, 'Blender File (.blend)', 'Export the mesh as a .blend file')
        ]
