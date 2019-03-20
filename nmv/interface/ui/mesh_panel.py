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

# System imports
import sys

# Blender imports
import bpy
from mathutils import Vector
from bpy.props import EnumProperty
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import FloatVectorProperty
from bpy.props import BoolProperty

# Internal imports
import nmv
import nmv.bbox
import nmv.consts
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.mesh
import nmv.rendering
import nmv.scene
import nmv.skeleton
import nmv.utilities


####################################################################################################
# @MeshPanel
####################################################################################################
class MeshPanel(bpy.types.Panel):
    """MeshPanel class"""

    # Panel options
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Mesh Toolbox'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    # Shown / Hidden rows
    # A list of rows that will be activated or deactivated based on availability of the mesh
    shown_hidden_rows = list()

    # Meshing technique
    bpy.types.Scene.SkeletonizationTechnique = EnumProperty(
        items=[(nmv.enums.Meshing.Skeleton.ORIGINAL,
                'Original',
                'Use the original morphology skeleton'),
               (nmv.enums.Meshing.Skeleton.TAPERED,
                'Tapered',
                'Create a tapered morphology skeleton (artistic)'),
               (nmv.enums.Meshing.Skeleton.ZIGZAG,
                'Zigzag',
                'Create a zigzagged skeleton (artistic)'),
               (nmv.enums.Meshing.Skeleton.TAPERED_ZIGZAG,
                'Tapered Zigzag',
                'Create a zigzagged and tapered skeleton (artistic)')],
        name='Skeleton', default=nmv.enums.Meshing.Skeleton.ORIGINAL)

    # Meshing technique
    bpy.types.Scene.MeshingTechnique = EnumProperty(
        items=[(nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT,
                'Piecewise Watertight',
                'Extended piecewise watertight meshing with some flexibility to adapt the options'),
               (nmv.enums.Meshing.Technique.SKINNING,
                'Skinning',
                'Skinning'),
               (nmv.enums.Meshing.Technique.UNION,
                'Union',
                'Union'),
               (nmv.enums.Meshing.Technique.META_OBJECTS,
                'Meta Objects',
                'Creates watertight mesh models using meta balls, but it could be slower than'
                ' the other methods')],
        name='Meshing Method', default=nmv.enums.Meshing.Technique.SKINNING)

    # Is the soma connected to the first order branches or not !
    bpy.types.Scene.SomaArborsConnection = EnumProperty(
        items=[(nmv.enums.Meshing.SomaConnection.CONNECTED,
                'Connected',
                'Connect the soma mesh to the arbors to make a nice mesh that can be used for any'
                'type of visualization that involves transparency'),
               (nmv.enums.Meshing.SomaConnection.DISCONNECTED,
                'Disconnected',
                'Create the soma as a separate mesh and do not connect it to the arbors. This '
                'option is used to guarantee surface smoothing when a volume is reconstructed '
                'from the resulting mesh, but cannot be used for surface transparency')],
        name='Soma Connection',
        default=nmv.enums.Meshing.SomaConnection.DISCONNECTED)

    # The skeleton of the union-based meshing algorithm
    bpy.types.Scene.UnionMethodSkeleton= EnumProperty(
        items=[(nmv.enums.Meshing.UnionMeshing.QUAD_SKELETON,
                'Quad',
                'Use a quad skeleton for the union meshing algorithm'),
               (nmv.enums.Meshing.UnionMeshing.CIRCULAR_SKELETON,
                'Circle',
                'Use a circular skeleton for the union meshing algorithm')],
        name='Skeleton',
        default=nmv.enums.Meshing.UnionMeshing.QUAD_SKELETON)

    # Edges, hard or smooth
    bpy.types.Scene.MeshSmoothing = EnumProperty(
        items=[(nmv.enums.Meshing.Edges.HARD,
                'Sharp',
                'Make the edges between the segments sharp and hard'),
               (nmv.enums.Meshing.Edges.SMOOTH,
                'Curvy',
                'Make the edges between the segments soft and curvy')],
        name='Edges',
        default=nmv.enums.Meshing.Edges.HARD)

    # Branching, is it based on angles or radii
    bpy.types.Scene.MeshBranching = EnumProperty(
        items=[(nmv.enums.Meshing.Branching.ANGLES,
                'Angles',
                'Make the branching based on the angles at branching points'),
               (nmv.enums.Meshing.Branching.RADII,
                'Radii',
                'Make the branching based on the radii of the children at the branching points')],
        name='Branching Method',
        default=nmv.enums.Meshing.Branching.ANGLES)

    # Are the mesh objects connected or disconnected.
    bpy.types.Scene.MeshObjectsConnection = EnumProperty(
        items=[(nmv.enums.Meshing.ObjectsConnection.CONNECTED,
                'Connected',
                'Connect all the objects of the mesh into one piece'),
               (nmv.enums.Meshing.ObjectsConnection.DISCONNECTED,
                'Disconnected',
                'Keep the different mesh objects of the neuron into separate pieces')],
        name='Mesh Objects',
        default=nmv.enums.Meshing.ObjectsConnection.DISCONNECTED)

    # Is the output model for reality or beauty
    bpy.types.Scene.SurfaceRoughness = EnumProperty(
        items=[(nmv.enums.Meshing.Surface.ROUGH,
                'Rough',
                'Create a mesh that looks like a real neuron reconstructed from microscope'),
               (nmv.enums.Meshing.Surface.SMOOTH,
                'Smooth',
                'Create a mesh that has smooth surface for visualization')],
        name='Model',
        default=nmv.enums.Meshing.Surface.SMOOTH)

    # Spine sources can be random or from a BBP circuit
    bpy.types.Scene.SpinesSourceCircuit= EnumProperty(
        items=[(nmv.enums.Meshing.Spines.Source.IGNORE,
                'Ignore',
                'Ignore creating the spines'),
               (nmv.enums.Meshing.Spines.Source.RANDOM,
                'Random',
                'The spines are generated randomly'),
               (nmv.enums.Meshing.Spines.Source.CIRCUIT,
                'Circuit',
                'The spines are generated following a BBP circuit'),],
        name='Spines Source',
        default=nmv.enums.Meshing.Spines.Source.IGNORE)

    # Spine sources are only random
    bpy.types.Scene.SpinesSourceRandom = EnumProperty(
        items=[(nmv.enums.Meshing.Spines.Source.IGNORE,
                'Ignore',
                'Ignore creating the spines'),
               (nmv.enums.Meshing.Spines.Source.RANDOM,
                'Random',
                'The spines are generated randomly')],
        name='Spines Source',
        default=nmv.enums.Meshing.Spines.Source.IGNORE)

    # Spine meshes quality
    bpy.types.Scene.SpineMeshQuality = EnumProperty(
        items=[(nmv.enums.Meshing.Spines.Quality.LQ,
                'Low',
                'Load low quality meshes'),
               (nmv.enums.Meshing.Spines.Quality.HQ,
                'High',
                'Load high quality meshes')],
        name='Spines Quality',
        default=nmv.enums.Meshing.Spines.Quality.LQ)

    # Nucleus
    bpy.types.Scene.Nucleus = EnumProperty(
        items=[(nmv.enums.Meshing.Nucleus.IGNORE,
                'Ignore',
                'The nucleus is ignored'),
               (nmv.enums.Meshing.Nucleus.INTEGRATED,
                'Integrated',
                'The nucleus is integrated')],
        name='Nucleus',
        default=nmv.enums.Meshing.Nucleus.IGNORE)

    # Nucleus mesh quality
    bpy.types.Scene.NucleusMeshQuality = EnumProperty(
        items=[(nmv.enums.Meshing.Nucleus.Quality.LQ,
                'Low',
                'Low quality nucleus mesh'),
               (nmv.enums.Meshing.Nucleus.Quality.HQ,
                'High',
                'High quality nucleus mesh')],
        name='Nucleus Mesh Quality',
        default=nmv.enums.Meshing.Nucleus.Quality.LQ)

    # Fix artifacts flag
    bpy.types.Scene.FixMorphologyArtifacts = BoolProperty(
        name='Fix Morphology Artifacts',
        description='Fixes the morphology artifacts during the mesh reconstruction process',
        default=True)

    # Mesh tessellation flag
    bpy.types.Scene.TessellateMesh = BoolProperty(
        name='Tessellation',
        description='Tessellate the reconstructed mesh to reduce the geometry complexity',
        default=False)

    # Mesh tessellation level
    bpy.types.Scene.MeshTessellationLevel = FloatProperty(
        name='Factor',
        description='Mesh tessellation level (between 0.1 and 1.0)',
        default=1.0, min=0.1, max=1.0)

    # Random spines percentage
    bpy.types.Scene.RandomSpinesPercentage = FloatProperty(
        name='Percentage',
        description='The percentage of the random spines along the dendrites (1 - 100)',
        default=50, min=1.0, max=100.0)

    bpy.types.Scene.MeshMaterial = EnumProperty(
        items=nmv.enums.Shading.MATERIAL_ITEMS,
        name="Material",
        default=nmv.enums.Shading.LAMBERT_WARD)

    # Use single color for the all the objects in the mesh
    bpy.types.Scene.MeshHomogeneousColor = BoolProperty(
        name="Homogeneous Color",
        description="Use a single color for rendering all the objects of the mesh",
        default=False)

    # A homogeneous color for all the objects of the mesh (membrane and spines)
    bpy.types.Scene.NeuronMeshColor = FloatVectorProperty(
        name="Membrane Color", subtype='COLOR',
        default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
        description="The homogeneous color of the reconstructed mesh membrane")

    # The color of the reconstructed soma mesh
    bpy.types.Scene.SomaMeshColor = FloatVectorProperty(
        name="Soma Color", subtype='COLOR',
        default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
        description="The color of the reconstructed soma mesh")

    # The color of the reconstructed axon mesh
    bpy.types.Scene.AxonMeshColor = FloatVectorProperty(
        name="Axon Color", subtype='COLOR',
        default=nmv.enums.Color.AXONS, min=0.0, max=1.0,
        description="The color of the reconstructed axon mesh")

    # The color of the reconstructed basal dendrites meshes
    bpy.types.Scene.BasalDendritesMeshColor = FloatVectorProperty(
        name="Basal Dendrites Color", subtype='COLOR',
        default=nmv.enums.Color.BASAL_DENDRITES, min=0.0, max=1.0,
        description="The color of the reconstructed basal dendrites")

    # The color of the reconstructed apical dendrite meshes
    bpy.types.Scene.ApicalDendriteMeshColor = FloatVectorProperty(
        name="Apical Dendrite Color", subtype='COLOR',
        default=nmv.enums.Color.APICAL_DENDRITES, min=0.0, max=1.0,
        description="The color of the reconstructed apical dendrite")

    # The color of the spines meshes
    bpy.types.Scene.SpinesMeshColor = FloatVectorProperty(
        name="Spines Color", subtype='COLOR',
        default=nmv.enums.Color.SPINES, min=0.0, max=1.0,
        description="The color of the spines")

    # The color of the nucleus mesh
    bpy.types.Scene.NucleusMeshColor = FloatVectorProperty(
        name="Nucleus Color", subtype='COLOR',
        default=nmv.enums.Color.NUCLEI, min=0.0, max=1.0,
        description="The color of the nucleus")

    # Rendering resolution
    bpy.types.Scene.MeshRenderingResolution = EnumProperty(
        items=[(nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION,
                'Fixed',
                'Renders an image of the mesh at a specific resolution'),
               (nmv.enums.Meshing.Rendering.Resolution.TO_SCALE,
                'To Scale',
                'Renders an image of the mesh at factor of the exact scale in (um)')],
        name='Type',
        default=nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION)

    # Rendering view
    bpy.types.Scene.MeshRenderingView = EnumProperty(
        items=[(nmv.enums.Meshing.Rendering.View.WIDE_SHOT_VIEW,
                'Wide Shot',
                'Renders an image of the full view'),
               (nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW,
                'Mid Shot',
                'Renders an image of the reconstructed arbors only'),
               (nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW,
                'Close Up',
                'Renders a close up image the focuses on the soma')],
        name='View', default=nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW)

    # Keep cameras
    bpy.types.Scene.KeepMeshCameras = BoolProperty(
        name="Keep Cameras & Lights in Scene",
        description="Keep the cameras in the scene to be used later if this file is saved",
        default=False)

    # Image resolution
    bpy.types.Scene.MeshFrameResolution = IntProperty(
        name='Resolution',
        description='The resolution of the image generated from rendering the mesh',
        default=512, min=128, max=1024 * 10)

    # Frame scale factor 'for rendering to scale option '
    bpy.types.Scene.MeshFrameScaleFactor = FloatProperty(
        name="Scale", default=1.0, min=1.0, max=100.0,
        description="The scale factor for rendering a mesh to scale")

    # Mesh rendering close up size
    bpy.types.Scene.MeshCloseUpSize = FloatProperty(
        name='Size',
        description='The size of the view that will be rendered in microns',
        default=20, min=5, max=100,)

    # Soma rendering progress bar
    bpy.types.Scene.NeuronMeshRenderingProgress = IntProperty(
        name="Rendering Progress",
        default=0, min=0, max=100, subtype='PERCENTAGE')

    # Individual components export flag
    bpy.types.Scene.ExportIndividuals = BoolProperty(
        name='Export Components',
        description='Export each component of the neuron as a separate mesh. This feature is '
                    'important to label reconstructions with machine learning applications.',
        default=False)

    # Exported mesh file formats
    bpy.types.Scene.ExportedMeshFormat = bpy.props.EnumProperty(
        items=[(nmv.enums.Meshing.ExportFormat.PLY,
                'Stanford (.ply)',
                'Export the mesh to a .ply file'),
               (nmv.enums.Meshing.ExportFormat.OBJ,
                'Wavefront (.obj)',
                'Export the mesh to a .obj file'),
               (nmv.enums.Meshing.ExportFormat.STL,
                'Stereolithography CAD (.stl)',
                'Export the mesh to an .stl file'),
               (nmv.enums.Meshing.ExportFormat.OFF,
                'Object File Format (.off)',
                'Export the mesh to an .off file'),
               (nmv.enums.Meshing.ExportFormat.BLEND,
                'Blender File (.blend)',
                'Export the mesh as a .blend file')],
        name='Format', default=nmv.enums.Meshing.ExportFormat.PLY)

    ################################################################################################
    # @draw_skinning_meshing_options
    ################################################################################################
    def draw_skinning_meshing_options(self,
                                      context):
        """Draws the options when the skinning meshing technique is selected.

        :param context:
            Panel context.
        """

        # Surface roughness
        if nmv.interface.ui_options.mesh.edges == nmv.enums.Meshing.Edges.SMOOTH:
            mesh_surface_row = self.layout.row()
            mesh_surface_row.label('Surface:')
            mesh_surface_row.prop(context.scene, 'SurfaceRoughness', expand=True)
            nmv.interface.ui_options.mesh.surface = context.scene.SurfaceRoughness
        else:
            nmv.interface.ui_options.mesh.surface = nmv.enums.Meshing.Surface.SMOOTH

        # Soma connection
        soma_connection_row = self.layout.row()
        soma_connection_row.label('Soma:')
        soma_connection_row.prop(context.scene, 'SomaArborsConnection', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.soma_connection = context.scene.SomaArborsConnection

        # Tessellation parameters
        tess_level_row = self.layout.row()
        tess_level_row.prop(context.scene, 'TessellateMesh')
        tess_level_column = tess_level_row.column()
        tess_level_column.prop(context.scene, 'MeshTessellationLevel')
        if not context.scene.TessellateMesh:
            # Use 1.0 to disable the tessellation
            nmv.interface.ui_options.mesh.tessellation_level = 1.0
            tess_level_column.enabled = False

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.tessellate_mesh = context.scene.TessellateMesh
        nmv.interface.ui_options.mesh.tessellation_level = context.scene.MeshTessellationLevel

    ################################################################################################
    # @draw_meta_objects_meshing_options
    ################################################################################################
    def draw_meta_objects_meshing_options(self,
                                          context):
        """Draws the options when the meta objects meshing technique is selected.

        :param context:
            Panel context.
        """

        # Surface roughness
        mesh_surface_row = self.layout.row()
        mesh_surface_row.label('Surface:')
        mesh_surface_row.prop(context.scene, 'SurfaceRoughness', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.surface = context.scene.SurfaceRoughness

        # Tessellation parameters
        tess_level_row = self.layout.row()
        tess_level_row.prop(context.scene, 'TessellateMesh')
        tess_level_column = tess_level_row.column()
        tess_level_column.prop(context.scene, 'MeshTessellationLevel')
        if not context.scene.TessellateMesh:
            nmv.interface.ui_options.mesh.tessellation_level = 1.0  # To disable the tessellation
            tess_level_column.enabled = False

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.tessellate_mesh = context.scene.TessellateMesh
        nmv.interface.ui_options.mesh.tessellation_level = context.scene.MeshTessellationLevel

    ################################################################################################
    # @draw_union_meshing_options
    ################################################################################################
    def draw_union_meshing_options(self,
                                   context):
        """Draws the options when the union meshing technique is selected.

        :param context:
            Panel context.
        """

        # Surface roughness
        mesh_surface_row = self.layout.row()
        mesh_surface_row.label('Surface:')
        mesh_surface_row.prop(context.scene, 'SurfaceRoughness', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.surface = context.scene.SurfaceRoughness

        # Edges
        mesh_edges_row = self.layout.row()
        mesh_edges_row.label('Edges:')
        mesh_edges_row.prop(context.scene, 'MeshSmoothing', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.edges = context.scene.MeshSmoothing

        # Soma connection
        soma_connection_row = self.layout.row()
        soma_connection_row.label('Soma:')
        soma_connection_row.prop(context.scene, 'SomaArborsConnection', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.soma_connection = context.scene.SomaArborsConnection

        # Tessellation parameters
        tess_level_row = self.layout.row()
        tess_level_row.prop(context.scene, 'TessellateMesh')
        tess_level_column = tess_level_row.column()
        tess_level_column.prop(context.scene, 'MeshTessellationLevel')
        if not context.scene.TessellateMesh:
            nmv.interface.ui_options.mesh.tessellation_level = 1.0  # To disable the tessellation
            tess_level_column.enabled = False

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.tessellate_mesh = context.scene.TessellateMesh
        nmv.interface.ui_options.mesh.tessellation_level = context.scene.MeshTessellationLevel

    ################################################################################################
    # @draw_piece_wise_meshing_options
    ################################################################################################
    def draw_piece_wise_meshing_options(self,
                                        context):
        """Draws the options when the Meta Objects meshing technique is selected.

        :param context:
            Panel context.
        """

        # Edges
        mesh_edges_row = self.layout.row()
        mesh_edges_row.label('Edges:')
        mesh_edges_row.prop(context.scene, 'MeshSmoothing', expand=True)
        nmv.interface.ui_options.mesh.edges = context.scene.MeshSmoothing

        # Surface roughness
        if nmv.interface.ui_options.mesh.edges == nmv.enums.Meshing.Edges.SMOOTH:
            mesh_surface_row = self.layout.row()
            mesh_surface_row.label('Surface:')
            mesh_surface_row.prop(context.scene, 'SurfaceRoughness', expand=True)
            nmv.interface.ui_options.mesh.surface = context.scene.SurfaceRoughness
        else:
            nmv.interface.ui_options.mesh.surface = nmv.enums.Meshing.Surface.SMOOTH

        # Soma connection
        soma_connection_row = self.layout.row()
        soma_connection_row.label('Soma:')
        soma_connection_row.prop(context.scene, 'SomaArborsConnection', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.soma_connection = context.scene.SomaArborsConnection

        # Mesh objects connection
        neuron_objects_connection_row = self.layout.row()
        neuron_objects_connection_row.label('Skeleton Objects:')
        neuron_objects_connection_row.prop(context.scene, 'MeshObjectsConnection', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.neuron_objects_connection = \
            context.scene.MeshObjectsConnection

        # Mesh branching
        branching_row = self.layout.row()
        branching_row.label('Branching:')
        branching_row.prop(context.scene, 'MeshBranching', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.branching = context.scene.MeshBranching

        # Tessellation parameters
        tess_level_row = self.layout.row()
        tess_level_row.prop(context.scene, 'TessellateMesh')
        tess_level_column = tess_level_row.column()
        tess_level_column.prop(context.scene, 'MeshTessellationLevel')
        if not context.scene.TessellateMesh:
            nmv.interface.ui_options.mesh.tessellation_level = 1.0  # To disable the tessellation
            tess_level_column.enabled = False

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.tessellate_mesh = context.scene.TessellateMesh
        nmv.interface.ui_options.mesh.tessellation_level = context.scene.MeshTessellationLevel

    ################################################################################################
    # @draw_meshing_options
    ################################################################################################
    def draw_meshing_options(self,
                             context):
        """Draw the options of the meshing.

        :param context:
            Panel context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Skeleton meshing options
        skeleton_meshing_options_row = layout.row()
        skeleton_meshing_options_row.label(text='Meshing Options:', icon='SURFACE_DATA')

        # Which meshing technique to use
        meshing_method_row = layout.row()
        meshing_method_row.prop(context.scene, 'MeshingTechnique', icon='OUTLINER_OB_EMPTY')
        nmv.interface.ui_options.mesh.meshing_technique = context.scene.MeshingTechnique

        # Which skeletonization technique to use
        skeletonization_row = layout.row()
        skeletonization_row.prop(context.scene, 'SkeletonizationTechnique', icon='CURVE_BEZCURVE')
        nmv.interface.ui_options.mesh.skeletonization = context.scene.SkeletonizationTechnique

        # Draw the meshing options
        if context.scene.MeshingTechnique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
            self.draw_piece_wise_meshing_options(context)
        elif context.scene.MeshingTechnique == nmv.enums.Meshing.Technique.META_OBJECTS:
            self.draw_meta_objects_meshing_options(context)
        elif context.scene.MeshingTechnique == nmv.enums.Meshing.Technique.SKINNING:
            self.draw_skinning_meshing_options(context)
        elif context.scene.MeshingTechnique == nmv.enums.Meshing.Technique.UNION:
            self.draw_union_meshing_options(context)

    ################################################################################################
    # @draw_spines_options
    ################################################################################################
    def draw_spines_options(self,
                            context):
        """Draw the spines options.

        :param context:
            Panel context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Spines meshing options
        spines_meshing_options_row = layout.row()
        spines_meshing_options_row.label(text='Spine Options:', icon='MOD_WAVE')

        # Spines
        spines_row = layout.row()
        spines_row.label('Source:')

        # If you are reading from a BBP circuit
        if context.scene.InputSource == nmv.enums.Input.CIRCUIT_GID:
            spines_row.prop(context.scene, 'SpinesSourceCircuit', expand=True)

            # Pass options from UI to system
            nmv.interface.ui_options.mesh.spines = context.scene.SpinesSourceCircuit

        # Otherwise, it is only random
        else:
            spines_row.prop(context.scene, 'SpinesSourceRandom', expand=True)

            # Pass options from UI to system
            nmv.interface.ui_options.mesh.spines = context.scene.SpinesSourceRandom

        # If the spines are not ignored
        if nmv.interface.ui_options.mesh.spines != nmv.enums.Meshing.Spines.Source.IGNORE:

            # Spines quality
            spines_quality_row = layout.row()
            spines_quality_row.label('Quality:')
            spines_quality_row.prop(context.scene, 'SpineMeshQuality', expand=True)

            # Pass options from UI to system
            nmv.interface.ui_options.mesh.spines_mesh_quality = context.scene.SpineMeshQuality

            # Percentage in case of random spines
            if nmv.interface.ui_options.mesh.spines == nmv.enums.Meshing.Spines.Source.RANDOM:

                # Random percentage
                spines_percentage_row = layout.row()
                spines_percentage_row.label('Percentage:')
                spines_percentage_row.prop(context.scene, 'RandomSpinesPercentage')

                # Pass options from UI to system
                nmv.interface.ui_options.mesh.random_spines_percentage = \
                    context.scene.RandomSpinesPercentage

    ################################################################################################
    # @draw_color_options
    ################################################################################################
    def draw_color_options(self, context):
        """Draw the coloring options.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Coloring parameters
        colors_row = layout.row()
        colors_row.label(text='Colors & Materials:', icon='COLOR')

        # Mesh material
        mesh_material_row = layout.row()
        mesh_material_row.prop(context.scene, 'MeshMaterial')

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.material = context.scene.MeshMaterial

        # Draw the meshing options
        if context.scene.MeshingTechnique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT or \
           context.scene.MeshingTechnique == nmv.enums.Meshing.Technique.UNION or \
           context.scene.MeshingTechnique == nmv.enums.Meshing.Technique.SKINNING:

            # Homogeneous mesh coloring
            homogeneous_color_row = layout.row()
            homogeneous_color_row.prop(context.scene, 'MeshHomogeneousColor')

            # If the homogeneous color flag is set
            if context.scene.MeshHomogeneousColor:
                neuron_color_row = layout.row()
                neuron_color_row.prop(context.scene, 'NeuronMeshColor')

                # Pass options from UI to system
                nmv.interface.ui_options.mesh.soma_color = \
                    Vector((context.scene.NeuronMeshColor.r,
                            context.scene.NeuronMeshColor.g,
                            context.scene.NeuronMeshColor.b))

                nmv.interface.ui_options.mesh.axon_color = \
                    Vector((context.scene.NeuronMeshColor.r,
                            context.scene.NeuronMeshColor.g,
                            context.scene.NeuronMeshColor.b))

                nmv.interface.ui_options.mesh.basal_dendrites_color = \
                    Vector((context.scene.NeuronMeshColor.r,
                            context.scene.NeuronMeshColor.g,
                            context.scene.NeuronMeshColor.b))

                nmv.interface.ui_options.mesh.apical_dendrites_color = \
                    Vector((context.scene.NeuronMeshColor.r,
                            context.scene.NeuronMeshColor.g,
                            context.scene.NeuronMeshColor.b))

                nmv.interface.ui_options.mesh.spines_color = \
                    Vector((context.scene.NeuronMeshColor.r,
                            context.scene.NeuronMeshColor.g,
                            context.scene.NeuronMeshColor.b))

            # Different colors
            else:
                soma_color_row = layout.row()
                soma_color_row.prop(context.scene, 'SomaMeshColor')

                axon_color_row = layout.row()
                axon_color_row.prop(context.scene, 'AxonMeshColor')

                basal_dendrites_color_row = layout.row()
                basal_dendrites_color_row.prop(context.scene, 'BasalDendritesMeshColor')

                apical_dendrites_color_row = layout.row()
                apical_dendrites_color_row.prop(context.scene, 'ApicalDendriteMeshColor')

                spines_color_row = layout.row()
                spines_color_row.prop(context.scene, 'SpinesMeshColor')

                # Pass options from UI to system
                nmv.interface.ui_options.mesh.soma_color = \
                    Vector((context.scene.SomaMeshColor.r,
                            context.scene.SomaMeshColor.g,
                            context.scene.SomaMeshColor.b))

                nmv.interface.ui_options.mesh.axon_color = \
                    Vector((context.scene.AxonMeshColor.r,
                            context.scene.AxonMeshColor.g,
                            context.scene.AxonMeshColor.b))

                nmv.interface.ui_options.mesh.basal_dendrites_color = \
                    Vector((context.scene.BasalDendritesMeshColor.r,
                            context.scene.BasalDendritesMeshColor.g,
                            context.scene.BasalDendritesMeshColor.b))

                nmv.interface.ui_options.mesh.apical_dendrites_color = \
                    Vector((context.scene.ApicalDendriteMeshColor.r,
                            context.scene.ApicalDendriteMeshColor.g,
                            context.scene.ApicalDendriteMeshColor.b))

                nmv.interface.ui_options.mesh.spines_color = \
                    Vector((context.scene.SpinesMeshColor.r,
                            context.scene.SpinesMeshColor.g,
                            context.scene.SpinesMeshColor.b))

        elif context.scene.MeshingTechnique == nmv.enums.Meshing.Technique.META_OBJECTS:

            neuron_color_row = layout.row()
            neuron_color_row.prop(context.scene, 'NeuronMeshColor')

            # Pass options from UI to system
            nmv.interface.ui_options.mesh.soma_color = \
                Vector((context.scene.NeuronMeshColor.r,
                        context.scene.NeuronMeshColor.g,
                        context.scene.NeuronMeshColor.b))

            nmv.interface.ui_options.mesh.axon_color = \
                Vector((context.scene.NeuronMeshColor.r,
                        context.scene.NeuronMeshColor.g,
                        context.scene.NeuronMeshColor.b))

            nmv.interface.ui_options.mesh.basal_dendrites_color = \
                Vector((context.scene.NeuronMeshColor.r,
                        context.scene.NeuronMeshColor.g,
                        context.scene.NeuronMeshColor.b))

            nmv.interface.ui_options.mesh.apical_dendrites_color = \
                Vector((context.scene.NeuronMeshColor.r,
                        context.scene.NeuronMeshColor.g,
                        context.scene.NeuronMeshColor.b))

            nmv.interface.ui_options.mesh.spines_color = \
                Vector((context.scene.NeuronMeshColor.r,
                        context.scene.NeuronMeshColor.g,
                        context.scene.NeuronMeshColor.b))

        # Add nucleus color option if they are not ignored
        if context.scene.Nucleus != nmv.enums.Meshing.Nucleus.IGNORE:

            nucleus_color_row = layout.row()
            nucleus_color_row.prop(context.scene, 'NucleusMeshColor')

            nmv.interface.ui_options.mesh.nucleus_color = Vector((
            context.scene.NucleusMeshColor.r, context.scene.NucleusMeshColor.g,
            context.scene.NucleusMeshColor.b))

    ################################################################################################
    # @draw_mesh_reconstruction_button
    ################################################################################################
    def draw_mesh_reconstruction_button(self,
                                        context):
        """Draw the mesh reconstruction button.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Mesh quick reconstruction options
        quick_reconstruction_row = layout.row()
        quick_reconstruction_row.label(text='Quick Reconstruction:', icon='PARTICLE_POINT')

        # Mesh reconstruction options
        mesh_reconstruction_row = layout.row()
        mesh_reconstruction_row.operator('reconstruct.neuron_mesh', icon='MESH_DATA')

    ################################################################################################
    # @draw_rendering_options
    ################################################################################################
    def draw_rendering_options(self,
                               context):
        """Draw the rendering options.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Rendering options
        quick_rendering_row = layout.row()
        quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')
        self.shown_hidden_rows.append(quick_rendering_row)

        # Rendering view
        rendering_view_row = layout.row()
        rendering_view_row.label('View:')
        rendering_view_row.prop(context.scene, 'MeshRenderingView', expand=True)
        self.shown_hidden_rows.append(rendering_view_row)

        # Add the close up size option
        if context.scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

            # Close up size option
            close_up_size_row = layout.row()
            close_up_size_row.label(text='Close Up Size:')
            close_up_size_row.prop(context.scene, 'MeshCloseUpSize')
            close_up_size_row.enabled = True
            self.shown_hidden_rows.append(close_up_size_row)

            # Frame resolution option (only for the close up mode)
            frame_resolution_row = layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(context.scene, 'MeshFrameResolution')
            frame_resolution_row.enabled = True
            self.shown_hidden_rows.append(frame_resolution_row)

        # Otherwise, render the Mid and Wide shot modes
        else:

            # Rendering resolution
            rendering_resolution_row = layout.row()
            rendering_resolution_row.label('Resolution:')
            rendering_resolution_row.prop(context.scene, 'MeshRenderingResolution', expand=True)
            self.shown_hidden_rows.append(rendering_resolution_row)

            # Add the frame resolution option
            if context.scene.MeshRenderingResolution == nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

                # Frame resolution option (only for the close up mode)
                frame_resolution_row = layout.row()
                frame_resolution_row.label(text='Frame Resolution:')
                frame_resolution_row.prop(context.scene, 'MeshFrameResolution')
                frame_resolution_row.enabled = True
                self.shown_hidden_rows.append(frame_resolution_row)

            # Otherwise, add the scale factor option
            else:

                # Scale factor option
                scale_factor_row = layout.row()
                scale_factor_row.label(text='Resolution Scale:')
                scale_factor_row.prop(context.scene, 'MeshFrameScaleFactor')
                scale_factor_row.enabled = True
                self.shown_hidden_rows.append(scale_factor_row)

        # Keep the cameras used for the rendering in the scene
        keep_cameras_row = layout.row()
        keep_cameras_row.prop(context.scene, 'KeepMeshCameras')
        keep_cameras_row.enabled = False

        # Rendering view
        render_view_row = layout.row()
        render_view_row.label(text='Render View:', icon='RESTRICT_RENDER_OFF')
        render_view_buttons_row = layout.row(align=True)
        render_view_buttons_row.operator('render_mesh.front', icon='AXIS_FRONT')
        render_view_buttons_row.operator('render_mesh.side', icon='AXIS_SIDE')
        render_view_buttons_row.operator('render_mesh.top', icon='AXIS_TOP')
        render_view_buttons_row.enabled = True
        self.shown_hidden_rows.append(render_view_buttons_row)

        render_animation_row = layout.row()
        render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
        render_animations_buttons_row = layout.row(align=True)
        render_animations_buttons_row.operator('render_mesh.360', icon='FORCE_MAGNETIC')
        render_animations_buttons_row.enabled = True
        self.shown_hidden_rows.append(render_animations_buttons_row)

        # Soma rendering progress bar
        neuron_mesh_rendering_progress_row = layout.row()
        neuron_mesh_rendering_progress_row.prop(context.scene, 'NeuronMeshRenderingProgress')
        neuron_mesh_rendering_progress_row.enabled = False
        self.shown_hidden_rows.append(neuron_mesh_rendering_progress_row)

    ################################################################################################
    # @draw_mesh_export_options
    ################################################################################################
    def draw_mesh_export_options(self,
                                 context):
        """Draw the mesh export options.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Saving meshes parameters
        save_neuron_mesh_row = layout.row()
        save_neuron_mesh_row.label(text='Export Neuron Mesh:', icon='MESH_UVSPHERE')

        export_format = layout.row()
        export_format.prop(context.scene, 'ExportedMeshFormat', icon='GROUP_VERTEX')

        if not context.scene.ExportedMeshFormat == nmv.enums.Meshing.ExportFormat.BLEND:
            if context.scene.MeshingTechnique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
                export_individual_row = layout.row()
                export_individual_row.prop(context.scene, 'ExportIndividuals')

        # Save button
        save_neuron_mesh_buttons_column = layout.column(align=True)
        save_neuron_mesh_buttons_column.operator('export.neuron_mesh', icon='MESH_DATA')
        save_neuron_mesh_buttons_column.enabled = True
        self.shown_hidden_rows.append(save_neuron_mesh_buttons_column)

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel

        :param context:
            Rendering context.
        """

        # Meshing options
        self.draw_meshing_options(context)

        # Spine options
        self.draw_spines_options(context)

        # Color options
        self.draw_color_options(context)

        # Mesh reconstruction button
        self.draw_mesh_reconstruction_button(context)

        # Rendering options
        self.draw_rendering_options(context)

        # Mesh export options
        self.draw_mesh_export_options(context)


####################################################################################################
# @ReconstructNeuronMesh
####################################################################################################
class ReconstructNeuronMesh(bpy.types.Operator):
    """Reconstructs the mesh of the neuron"""

    # Operator parameters
    bl_idname = "reconstruct.neuron_mesh"
    bl_label = "Reconstruct Mesh"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Executes the operator

        Keyword arguments:
        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Meshing technique
        meshing_technique = nmv.interface.ui_options.mesh.meshing_technique

        # Piece-wise watertight meshing
        if meshing_technique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:

            # Create the mesh builder
            mesh_builder = nmv.builders.PiecewiseBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

            # Reconstruct the mesh
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Bridging
        elif meshing_technique == nmv.enums.Meshing.Technique.BRIDGING:

            # Create the mesh builder
            mesh_builder = nmv.builders.BridgingBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

            # Reconstruct the mesh
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Union
        elif meshing_technique == nmv.enums.Meshing.Technique.UNION:

            # Create the mesh builder
            mesh_builder = nmv.builders.UnionBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

            # Reconstruct the mesh
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Extrusion
        elif meshing_technique == nmv.enums.Meshing.Technique.EXTRUSION:

            # Create the mesh builder
            mesh_builder = nmv.builders.ExtrusionBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

            # Reconstruct the mesh
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        elif meshing_technique == nmv.enums.Meshing.Technique.SKINNING:

            # Create the mesh builder
            mesh_builder = nmv.builders.SkinningBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

            # Reconstruct the mesh
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        elif meshing_technique == nmv.enums.Meshing.Technique.META_OBJECTS:

            # Create the mesh builder
            mesh_builder = nmv.builders.MetaBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

            # Reconstruct the mesh
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        else:

            # Invalid method
            self.report({'ERROR'}, 'Invalid Meshing Technique')

        return {'FINISHED'}


####################################################################################################
# @RenderMeshFront
####################################################################################################
class RenderMeshFront(bpy.types.Operator):
    """Render front view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "render_mesh.front"
    bl_label = "Front"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator

        :param context:
            Rendering Context.
        :return:
            'FINISHED'
        """

        # Render the image
        nmv.interface.ui.render_mesh_image(self, context.scene, nmv.enums.Camera.View.FRONT)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMeshSide
####################################################################################################
class RenderMeshSide(bpy.types.Operator):
    """Render side view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "render_mesh.side"
    bl_label = "Side"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator

        :param context:
            Rendering context.
        :return:
            'FINISHED'
        """

        # Render the image
        nmv.interface.ui.render_mesh_image(self, context.scene, nmv.enums.Camera.View.SIDE)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMeshTop
####################################################################################################
class RenderMeshTop(bpy.types.Operator):
    """Render top view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "render_mesh.top"
    bl_label = "Top"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator

        :param context:
            Rendering context.
        :return:
            'FINISHED'.
        """

        # Render the image
        nmv.interface.ui.render_mesh_image(self, context.scene, nmv.enums.Camera.View.TOP)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMesh360
####################################################################################################
class RenderMesh360(bpy.types.Operator):
    """Render a 360 view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "render_mesh.360"
    bl_label = "360"

    # Timer parameters
    event_timer = None
    timer_limits = bpy.props.IntProperty(default=0)

    # Collect a list of the scene objects (meshes) to be rendered before starting the rendering loop
    scene_objects = list()

    # 360 bounding box
    bounding_box_360 = None

    # Output data
    output_directory = None

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self,
              context,
              event):
        """Threading and non-blocking handling.

        :param context:
            Panel context.
        :param event:
            A given event for the panel.
        """

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > 360:

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel context
            self.cancel(context)

            # Done
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Set the frame name
            image_name = '%s/%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Render at a specific resolution
            if context.scene.MeshRenderingResolution == \
                    nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

                # Render the image
                nmv.rendering.renderer.render_at_angle(
                    scene_objects=self.scene_objects,
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=nmv.enums.Camera.View.FRONT_360,
                    image_resolution=context.scene.MeshFrameResolution,
                    image_name=image_name)

            # Render at a specific scale factor
            else:

                # Render the image
                nmv.rendering.NeuronMeshRenderer.render_at_angle_to_scale(
                    mesh_objects=self.scene_objects,
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=nmv.enums.Camera.View.FRONT_360,
                    image_scale_factor=context.scene.MeshFrameScaleFactor,
                    image_name=image_name)

            # Update the progress shell
            nmv.utilities.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            context.scene.NeuronMeshRenderingProgress = int(100 * self.timer_limits / 360.0)

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator

        :param context:
            Panel context.
        """

        # If no morphology is loaded, report it
        if nmv.interface.ui_morphology is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Validate the output directory
        nmv.interface.ui.validate_output_directory(
            panel_object=self, context_scene=context.scene)

        # Get a list of all the meshes in the scene
        self.scene_objects = nmv.scene.get_list_of_meshes_in_scene()

        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.sequences_directory)

        # Compute the bounding box for a close up view
        if context.scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            rendering_bbox = nmv.bbox.compute_unified_extent_bounding_box(
                extent=context.scene.MeshCloseUpSize)

        # Compute the bounding box for a mid shot view
        elif context.scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            rendering_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Compute the bounding box for the wide shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            rendering_bbox = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=nmv.interface.ui_morphology)

        # Compute a 360 bounding box to fit the arbors
        self.bounding_box_360 = nmv.bbox.compute_360_bounding_box(
            rendering_bbox, nmv.interface.ui_morphology.soma.centroid)

        # Stretch the bounding box by few microns
        self.bounding_box_360.extend_bbox(delta=nmv.consts.Image.GAP_DELTA)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_mesh_360' % (
            nmv.interface.ui_options.io.sequences_directory,
            nmv.interface.ui_options.morphology.label)
        nmv.file.ops.clean_and_create_directory(self.output_directory)

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        self.event_timer = wm.event_timer_add(time_step=0.01, window=context.window)
        wm.modal_handler_add(self)

        # Done
        return {'RUNNING_MODAL'}

    ################################################################################################
    # @cancel
    ################################################################################################
    def cancel(self, context):
        """
        Cancel the panel processing and return to the interaction mode.

        :param context: Panel context.
        """

        # Multi-threading
        wm = context.window_manager
        wm.event_timer_remove(self.event_timer)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Morphology Rendering Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @SaveNeuronMeshBLEND
####################################################################################################
class ExportMesh(bpy.types.Operator):
    """Export neuron mesh"""

    # Operator parameters
    bl_idname = "export.neuron_mesh"
    bl_label = "Export"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Executes the operator

        :param context:
            Rendering context.
        :return:
            'FINISHED'
        """

        # If no morphology is loaded, report it
        if nmv.interface.ui_morphology is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Validate the output directory
        nmv.interface.ui.validate_output_directory(panel_object=self, context_scene=context.scene)

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Get a list of all the meshes in the scene
        mesh_objects = nmv.scene.get_list_of_meshes_in_scene()

        # Export
        nmv.file.export_mesh_objects_to_file(mesh_objects,
                                             nmv.interface.ui_options.io.meshes_directory,
                                             nmv.interface.ui_morphology.label,
                                             context.scene.ExportedMeshFormat,
                                             context.scene.ExportIndividuals)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Register all the classes in this panel"""

    # Mesh reconstruction panel
    bpy.utils.register_class(MeshPanel)

    # Mesh reconstruction button
    bpy.utils.register_class(ReconstructNeuronMesh)

    # Mesh rendering
    bpy.utils.register_class(RenderMeshFront)
    bpy.utils.register_class(RenderMeshSide)
    bpy.utils.register_class(RenderMeshTop)
    bpy.utils.register_class(RenderMesh360)

    # Neuron mesh saving operators
    bpy.utils.register_class(ExportMesh)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-register all the classes in this panel"""

    # Mesh reconstruction panel
    bpy.utils.unregister_class(MeshPanel)

    # Mesh reconstruction button
    bpy.utils.unregister_class(ReconstructNeuronMesh)

    # Mesh rendering
    bpy.utils.unregister_class(ExportMesh)

    # Neuron mesh saving operators
    bpy.utils.unregister_class(ExportMesh)

