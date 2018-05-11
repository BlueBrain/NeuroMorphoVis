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
import neuromorphovis as nmv
import neuromorphovis.bbox
import neuromorphovis.consts
import neuromorphovis.builders
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.file
import neuromorphovis.interface
import neuromorphovis.mesh
import neuromorphovis.rendering
import neuromorphovis.scene
import neuromorphovis.skeleton
import neuromorphovis.utilities


####################################################################################################
# @MeshPanel
####################################################################################################
class MeshPanel(bpy.types.Panel):
    """MeshPanel class"""

    # Panel options
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Mesh Toolbox'
    bl_context = 'objectmode'
    bl_category = 'NeuroMorphoVis'

    # Shown / Hidden rows
    # A list of rows that will be activated or deactivated based on availability of the mesh
    shown_hidden_rows = list()

    # Meshing technique
    bpy.types.Scene.MeshingTechnique = EnumProperty(
        items=[(nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT,
                'Piecewise Watertight',
                'Extended piecewise watertight meshing with some flexibility to adapt the options'),
               (nmv.enums.Meshing.Technique.BRIDGING,
                'Bridging (Watertight)',
                'Create a mesh using the bridging method'),
               (nmv.enums.Meshing.Technique.UNION,
                'Union (Watertight)',
                'Create a mesh using the union method')],
        name='Method',
        default=nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT)

    # Is the soma connected to the first order branches or not !
    bpy.types.Scene.MeshSomaConnection = EnumProperty(
        items=[(nmv.enums.Meshing.SomaConnection.CONNECTED,
                'Connected',
                'Connect the soma mesh to the arbors'),
               (nmv.enums.Meshing.SomaConnection.DISCONNECTED,
                'Disconnected',
                'Create the soma as a separate mesh and do not connect it to the arbors')],
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
                'Original',
                'Make the edges between the segments hard'),
               (nmv.enums.Meshing.Edges.SMOOTH,
                'Smooth',
                'Make the edges between the segments soft')],
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

    # Rendering view
    bpy.types.Scene.Spines = EnumProperty(
        items=[(nmv.enums.Meshing.Spines.IGNORE,
                'Ignore',
                'The spines are ignored'),
               (nmv.enums.Meshing.Spines.DISCONNECTED,
                'Disconnected',
                'The spines are generated but disconnected from the neuron mesh'),
               (nmv.enums.Meshing.Spines.INTEGRATED,
                'Integrated',
                'The spines are integrated as part of the neuron mesh')],
                name='Spines', default=nmv.enums.Meshing.Spines.IGNORE)

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

    bpy.types.Scene.MeshMaterial = EnumProperty(
        items=nmv.enums.Shading.MATERIAL_ITEMS,
        name="Material",
        default=nmv.enums.Shading.LAMBERT_WARD)

    # Use single color for the all the objects in the mesh
    bpy.types.Scene.MeshHomogeneousColor = BoolProperty(
        name="Homogeneous Color",
        description="Use a single color for rendering all the objects of the mesh",
        default=True)

    # A homogeneous color for all the objects of the mesh
    bpy.types.Scene.NeuronMeshColor = FloatVectorProperty(
        name="Mesh Color", subtype='COLOR',
        default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
        description="The homogeneous color of the reconstructed mesh")

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
        name='View', default=nmv.enums.Meshing.Rendering.View.WIDE_SHOT_VIEW)

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

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel

        :param context:
            Rendering context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Meshing method parameters
        meshing_method_row = layout.row()
        meshing_method_row.prop(context.scene, 'MeshingTechnique', icon='OUTLINER_OB_EMPTY')

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.meshing_technique = context.scene.MeshingTechnique

        if context.scene.MeshingTechnique == nmv.enums.Meshing.Technique.UNION:
            skeleton_row = layout.row()
            skeleton_row.label('Skeleton:')
            skeleton_row.prop(context.scene, 'UnionMethodSkeleton', expand=True)

            # Pass options from UI to system
            nmv.interface.ui_options.mesh.skeleton_shape = context.scene.UnionMethodSkeleton

        # Surface roughness
        mesh_surface_row = layout.row()
        mesh_surface_row.label('Surface:')
        mesh_surface_row.prop(context.scene, 'SurfaceRoughness', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.surface = context.scene.SurfaceRoughness

        # Edges
        mesh_edges_row = layout.row()
        mesh_edges_row.label('Edges:')
        mesh_edges_row.prop(context.scene, 'MeshSmoothing', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.edges = context.scene.MeshSmoothing

        # Soma connection
        soma_connection_row = layout.row()
        soma_connection_row.label('Soma:')
        soma_connection_row.prop(context.scene, 'MeshSomaConnection', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.soma_connection = context.scene.MeshSomaConnection

        # Mesh objects connection
        neuron_objects_connection_row = layout.row()
        neuron_objects_connection_row.label('Mesh Objects:')
        neuron_objects_connection_row.prop(context.scene, 'MeshObjectsConnection', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.neuron_objects_connection = \
            context.scene.MeshObjectsConnection

        # Mesh branching
        branching_row = layout.row()
        branching_row.label('Branching:')
        branching_row.prop(context.scene, 'MeshBranching', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.branching = context.scene.MeshBranching

        # Spines
        spines_row = layout.row()
        spines_row.label('Spines:')
        spines_row.prop(context.scene, 'Spines', expand=True)

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.spine_objects = context.scene.Spines

        # Ignore the spines row if no circuit is given
        if context.scene.InputSource == nmv.enums.Input.H5_SWC_FILE:
            spines_row.enabled = False
            nmv.interface.ui_options.mesh.spine_objects = nmv.enums.Meshing.Spines.IGNORE

        # Tessellation parameters
        tess_level_row = layout.row()
        tess_level_row.prop(context.scene, 'TessellateMesh')
        tess_level_column = tess_level_row.column()
        tess_level_column.prop(context.scene, 'MeshTessellationLevel')
        if not context.scene.TessellateMesh:
            nmv.interface.ui_options.mesh.tessellation_level = 1.0  # To disable the tessellation
            tess_level_column.enabled = False

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.tessellate_mesh = context.scene.TessellateMesh
        nmv.interface.ui_options.mesh.tessellation_level = context.scene.MeshTessellationLevel

        # Coloring parameters
        colors_row = layout.row()
        colors_row.label(text='Colors & Materials:', icon='COLOR')

        # Mesh material
        mesh_material_row = layout.row()
        mesh_material_row.prop(context.scene, 'MeshMaterial')

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.material = context.scene.MeshMaterial

        # Homogeneous mesh coloring
        homogeneous_color_row = layout.row()
        homogeneous_color_row.prop(context.scene, 'MeshHomogeneousColor')

        # If the homogeneous color flag is set
        if context.scene.MeshHomogeneousColor:
            neuron_color_row = layout.row()
            neuron_color_row.prop(context.scene, 'NeuronMeshColor')

            # Pass options from UI to system
            nmv.interface.ui_options.mesh.soma_color = Vector((context.scene.NeuronMeshColor.r,
                                                               context.scene.NeuronMeshColor.g,
                                                               context.scene.NeuronMeshColor.b))
            nmv.interface.ui_options.mesh.axon_color = Vector((context.scene.NeuronMeshColor.r,
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

        # Mesh reconstruction options
        mesh_reconstruction_row = layout.row()
        mesh_reconstruction_row.operator('reconstruct.neuron_mesh', icon='MESH_DATA')

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
            if context.scene.MeshRenderingResolution == \
                    nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

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

        # Saving meshes parameters
        save_neuron_mesh_row = layout.row()
        save_neuron_mesh_row.label(text='Save Neuron Mesh As:', icon='MESH_UVSPHERE')
        self.shown_hidden_rows.append(save_neuron_mesh_row)

        save_neuron_mesh_buttons_column = layout.column(align=True)
        save_neuron_mesh_buttons_column.operator('save_neuron_mesh.obj', icon='MESH_DATA')
        save_neuron_mesh_buttons_column.operator('save_neuron_mesh.ply', icon='GROUP_VERTEX')
        save_neuron_mesh_buttons_column.operator('save_neuron_mesh.stl', icon='RETOPO')
        save_neuron_mesh_buttons_column.operator('save_neuron_mesh.blend', icon='OUTLINER_OB_META')
        save_neuron_mesh_buttons_column.enabled = True
        self.shown_hidden_rows.append(save_neuron_mesh_buttons_column)


####################################################################################################
# @ReconstructNeuronMesh
####################################################################################################
class ReconstructNeuronMesh(bpy.types.Operator):
    """Reconstructs the mesh of the neuron"""

    # Operator parameters
    bl_idname = "reconstruct.neuron_mesh"
    bl_label = "Reconstruct"

    ################################################################################################
    # @load_morphology
    ################################################################################################
    def load_morphology(self, current_scene):
        """
        Loads the morphology from file.

        :param current_scene: Scene.
        """

        # Read the data from a given morphology file either in .h5 or .swc formats
        if bpy.context.scene.InputSource == nmv.enums.Input.H5_SWC_FILE:

            # Pass options from UI to system
            nmv.interface.ui_options.morphology.morphology_file_path = current_scene.MorphologyFile

            # Update the morphology label
            nmv.interface.ui_options.morphology.label = nmv.file.ops.get_file_name_from_path(
                current_scene.MorphologyFile)

            # Load the morphology from the file
            loading_flag, morphology_object = nmv.file.readers.read_morphology_from_file(
                options=nmv.interface.ui_options)

            # Verify the loading operation
            if loading_flag:

                # Update the morphology
                nmv.interface.ui_morphology = morphology_object

            # Otherwise, report an ERROR
            else:
                self.report({'ERROR'}, 'Invalid Morphology File')

        # Read the data from a specific gid in a given circuit
        elif bpy.context.scene.InputSource == nmv.enums.Input.CIRCUIT_GID:

            # Pass options from UI to system
            nmv.interface.ui_options.morphology.blue_config = current_scene.CircuitFile
            nmv.interface.ui_options.morphology.gid = current_scene.Gid

            # Update the morphology label
            nmv.interface.ui_options.morphology.label = 'neuron_' + str(current_scene.Gid)

            # Load the morphology from the circuit
            loading_flag, morphology_object = \
                nmv.file.readers.BBPReader.load_morphology_from_circuit(
                    blue_config=nmv.interface.ui_options.morphology.blue_config,
                    gid=nmv.interface.ui_options.morphology.gid)

            # Verify the loading operation
            if loading_flag:

                # Update the morphology
                nmv.interface.ui_morphology = morphology_object

            # Otherwise, report an ERROR
            else:

                self.report({'ERROR'}, 'Cannot Load Morphology from Circuit')

        else:

            # Report an invalid input source
            self.report({'ERROR'}, 'Invalid Input Source')


    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Executes the operator

        Keyword arguments:
        :param context: Operator context.
        :return: {'FINISHED'}
        """

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology
        self.load_morphology(current_scene=context.scene)

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
    def execute(self, context):
        """Execute the operator

        :param context:
            Rendering Context.
        :return:
            'FINISHED'
        """

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

        # Report the process starting in the UI
        self.report({'INFO'}, 'Mesh Rendering ... Wait')

        # A reference to the bounding box that will be used for the rendering
        rendering_bbox = None

        # Compute the bounding box for a close up view
        if context.scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            rendering_bbox = nmv.bbox.compute_unified_extent_bounding_box(
                extent=context.scene.MeshCloseUpSize)

        # Compute the bounding box for a mid-shot view
        elif context.scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            rendering_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Compute the bounding box for the wide-shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            rendering_bbox = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=nmv.interface.ui_morphology)

        # Stretch the bounding box by few microns
        rendering_bbox.extend_bbox(delta=nmv.consts.Image.GAP_DELTA)

        # Render at a specific resolution
        if context.scene.MeshRenderingResolution == \
                nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

            # Render the image
            nmv.rendering.NeuronMeshRenderer.render(
                bounding_box=rendering_bbox,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=context.scene.MeshFrameResolution,
                image_name='MESH_FRONT_%s' % nmv.interface.ui_options.morphology.label,
                image_directory=nmv.interface.ui_options.io.images_directory,
                keep_camera_in_scene=context.scene.KeepMeshCameras)

        # Render at a specific scale factor
        else:

            # Render the image
            nmv.rendering.NeuronMeshRenderer.render_to_scale(
                bounding_box=rendering_bbox,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_scale_factor=context.scene.MeshFrameScaleFactor,
                image_name='MESH_FRONT_%s' % nmv.interface.ui_options.morphology.label,
                image_directory=nmv.interface.ui_options.io.images_directory,
                keep_camera_in_scene=context.scene.KeepMeshCameras)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Mesh Rendering Done')

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

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

        # Report the process starting in the UI
        self.report({'INFO'}, 'Mesh Rendering ... Wait')

        # A reference to the bounding box that will be used for the rendering
        bounding_box = None

        # Compute the bounding box for a close up view
        if context.scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
                extent=context.scene.MeshCloseUpSize)

        # Compute the bounding box for a mid shot view
        elif context.scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Compute the bounding box for the wide shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=nmv.interface.ui_morphology)

        # Render at a specific resolution
        if context.scene.MeshRenderingResolution == \
                nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

            # Render the image
            nmv.rendering.NeuronMeshRenderer.render(
                bounding_box=bounding_box,
                camera_view=nmv.enums.Camera.View.SIDE,
                image_resolution=context.scene.MeshFrameResolution,
                image_name='MESH_SIDE_%s' % nmv.interface.ui_options.morphology.label,
                image_directory=nmv.interface.ui_options.io.images_directory,
                keep_camera_in_scene=context.scene.KeepMeshCameras)

        # Render at a specific scale factor
        else:

            # Render the image
            nmv.rendering.NeuronMeshRenderer.render_to_scale(
                bounding_box=bounding_box,
                camera_view=nmv.enums.Camera.View.SIDE,
                image_scale_factor=context.scene.MeshFrameScaleFactor,
                image_name='MESH_SIDE_%s' % nmv.interface.ui_options.morphology.label,
                image_directory=nmv.interface.ui_options.io.images_directory,
                keep_camera_in_scene=context.scene.KeepMeshCameras)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Mesh Rendering Done')

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

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.images_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.images_directory)

        # Report the process starting in the UI
        self.report({'INFO'}, 'Mesh Rendering ... Wait')

        # A reference to the bounding box that will be used for the rendering
        bounding_box = None

        # Compute the bounding box for a close up view
        if context.scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            bounding_box = nmv.bbox.compute_unified_extent_bounding_box(
                extent=context.scene.MeshCloseUpSize)

        # Compute the bounding box for a mid shot view
        elif context.scene.MeshRenderingView == nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Compute the bounding box for the wide shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
                morphology=nmv.interface.ui_morphology)

        # Render at a specific resolution
        if context.scene.MeshRenderingResolution == \
                nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

            # Render the image
            nmv.rendering.NeuronMeshRenderer.render(
                bounding_box=bounding_box,
                camera_view=nmv.enums.Camera.View.TOP,
                image_resolution=context.scene.MeshFrameResolution,
                image_name='MESH_TOP_%s' % nmv.interface.ui_options.morphology.label,
                image_directory=nmv.interface.ui_options.io.images_directory,
                keep_camera_in_scene=context.scene.KeepMeshCameras)

        # Render at a specific scale factor
        else:

            # Render the image
            nmv.rendering.NeuronMeshRenderer.render_to_scale(
                bounding_box=bounding_box,
                camera_view=nmv.enums.Camera.View.TOP,
                image_scale_factor=context.scene.MeshFrameScaleFactor,
                image_name='MESH_TOP_%s' % nmv.interface.ui_options.morphology.label,
                image_directory=nmv.interface.ui_options.io.images_directory,
                keep_camera_in_scene=context.scene.KeepMeshCameras)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Mesh Rendering Done')

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

    # 360 bounding box
    bounding_box_360 = None

    # Output data
    output_directory = None

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self, context, event):
        """
        Threading and non-blocking handling.

        :param context: Panel context.
        :param event: A given event for the panel.
        """

        # Get a reference to the scene
        scene = context.scene

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
                nmv.rendering.NeuronMeshRenderer.render_at_angle(
                    mesh_objects=nmv.interface.ui_reconstructed_mesh,
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=nmv.enums.Camera.View.FRONT_360,
                    image_resolution=context.scene.MeshFrameResolution,
                    image_name=image_name)

            # Render at a specific scale factor
            else:

                # Render the image
                nmv.rendering.NeuronMeshRenderer.render_at_angle_to_scale(
                    mesh_objects=nmv.interface.ui_reconstructed_mesh,
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

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.sequences_directory)

        # A reference to the bounding box that will be used for the rendering
        rendering_bbox = None

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
# @SaveNeuronMeshOBJ
####################################################################################################
class SaveNeuronMeshOBJ(bpy.types.Operator):
    """Save the neuron mesh in OBJ file"""

    # Operator parameters
    bl_idname = "save_neuron_mesh.obj"
    bl_label = "Wavefront (.obj)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Executes the operator

        :param context:
            Rendering context.
        :return:
            'FINISHED'.
        """

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # If the nmv.interface.ui_reconstructed_mesh list is empty, then skip the operation
        if len(nmv.interface.ui_reconstructed_mesh) == 0:
            self.report({'ERROR'}, 'Reconstruct a Neuron Mesh to Export it!')
            return {'FINISHED'}

        # If the mesh is already a single object,
        elif len(nmv.interface.ui_reconstructed_mesh) == 1:

            # Export the mesh object as an .OBJ  file
            nmv.file.export_object_to_obj_file(
                mesh_object=nmv.interface.ui_reconstructed_mesh[0],
                output_directory=nmv.interface.ui_options.io.meshes_directory,
                output_file_name=nmv.interface.ui_morphology.label)

        # Otherwise, join all the mesh objects into a single object and export it
        else:

            # Join all the mesh objects into a single object
            mesh_object = nmv.mesh.ops.join_mesh_objects(
                mesh_list=nmv.interface.ui_reconstructed_mesh,
                name=nmv.interface.ui_morphology.label)

            # Export the mesh object as an .OBJ  file
            nmv.file.export_object_to_obj_file(
                mesh_object=mesh_object,
                output_directory=nmv.interface.ui_options.io.meshes_directory,
                output_file_name=nmv.interface.ui_morphology.label)

        return {'FINISHED'}


####################################################################################################
# @SaveNeuronMeshPLY
####################################################################################################
class SaveNeuronMeshPLY(bpy.types.Operator):
    """Save the neuron mesh in PLY file"""

    # Operator parameters
    bl_idname = "save_neuron_mesh.ply"
    bl_label = "Stanford (.ply)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Executes the operator

        :param context:
            Operator context.
        :return:
            'FINISHED'.
        """

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # If the nmv.interface.ui_reconstructed_mesh list is empty, then skip the operation
        if len(nmv.interface.ui_reconstructed_mesh) == 0:
            self.report({'ERROR'}, 'Reconstruct a Neuron Mesh to Export it!')
            return {'FINISHED'}

        # If the mesh is already a single object,
        elif len(nmv.interface.ui_reconstructed_mesh) == 1:

            # Export the mesh object as an .OBJ  file
            nmv.file.export_object_to_ply_file(
                mesh_object=nmv.interface.ui_reconstructed_mesh[0],
                output_directory=nmv.interface.ui_options.io.meshes_directory,
                output_file_name=nmv.interface.ui_morphology.label)

        # Otherwise, join all the mesh objects into a single object and export it
        else:

            # Join all the mesh objects into a single object
            mesh_object = nmv.mesh.ops.join_mesh_objects(
                mesh_list=nmv.interface.ui_reconstructed_mesh,
                name=nmv.interface.ui_morphology.label)

            # Export the mesh object as an .PLY  file
            nmv.file.export_object_to_ply_file(
                mesh_object=mesh_object,
                output_directory=nmv.interface.ui_options.io.meshes_directory,
                output_file_name=nmv.interface.ui_morphology.label)

        return {'FINISHED'}


####################################################################################################
# @SaveNeuronMeshSTL
####################################################################################################
class SaveNeuronMeshSTL(bpy.types.Operator):
    """Save the neuron mesh in STL file"""

    # Operator parameters
    bl_idname = "save_neuron_mesh.stl"
    bl_label = "Stereolithography CAD (.stl)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """
        Executes the operator.

        :param context: Operator context.
        :return: {'FINISHED'}
        """

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # If the nmv.interface.ui_reconstructed_mesh list is empty, then skip the operation
        if len(nmv.interface.ui_reconstructed_mesh) == 0:
            self.report({'ERROR'}, 'Reconstruct a Neuron Mesh to Export it!')
            return {'FINISHED'}

        # If the mesh is already a single object,
        elif len(nmv.interface.ui_reconstructed_mesh) == 1:

            # Export the mesh object as an .OBJ  file
            nmv.file.export_object_to_stl_file(
                mesh_object=nmv.interface.ui_reconstructed_mesh[0],
                output_directory=nmv.interface.ui_options.io.meshes_directory,
                output_file_name=nmv.interface.ui_morphology.label)

        # Otherwise, join all the mesh objects into a single object and export it
        else:

            # Join all the mesh objects into a single object
            mesh_object = nmv.mesh.ops.join_mesh_objects(
                mesh_list=nmv.interface.ui_reconstructed_mesh,
                name=nmv.interface.ui_morphology.label)

            # Export the mesh object as an .STL  file
            nmv.file.export_object_to_stl_file(
                mesh_object=mesh_object,
                output_directory=nmv.interface.ui_options.io.meshes_directory,
                output_file_name=nmv.interface.ui_morphology.label)

        return {'FINISHED'}


####################################################################################################
# @SaveNeuronMeshBLEND
####################################################################################################
class SaveNeuronMeshBLEND(bpy.types.Operator):
    """Save the neuron mesh in BLEND file"""

    # Operator parameters
    bl_idname = "save_neuron_mesh.blend"
    bl_label = "Blender Format (.blend)"

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

        # Ensure that there is a valid directory where the meshes will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Export the neuron mesh as an .BLEND file
        # NOTE: Use None to the mesh object to export every thing in the scene
        nmv.file.export_object_to_blend_file(
            mesh_object=None,
            output_directory=nmv.interface.ui_options.io.meshes_directory,
            output_file_name=nmv.interface.ui_morphology.label)

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
    bpy.utils.register_class(SaveNeuronMeshOBJ)
    bpy.utils.register_class(SaveNeuronMeshPLY)
    bpy.utils.register_class(SaveNeuronMeshSTL)
    bpy.utils.register_class(SaveNeuronMeshBLEND)


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
    bpy.utils.unregister_class(RenderMeshFront)
    bpy.utils.unregister_class(RenderMeshSide)
    bpy.utils.unregister_class(RenderMeshTop)
    bpy.utils.unregister_class(RenderMesh360)

    # Neuron mesh saving operators
    bpy.utils.unregister_class(SaveNeuronMeshOBJ)
    bpy.utils.unregister_class(SaveNeuronMeshPLY)
    bpy.utils.unregister_class(SaveNeuronMeshSTL)
    bpy.utils.unregister_class(SaveNeuronMeshBLEND)