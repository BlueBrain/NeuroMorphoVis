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
import sys, os, imp

# Blender imports
import bpy
from mathutils import Vector
from bpy.props import EnumProperty
from bpy.props import FloatProperty
from bpy.props import FloatVectorProperty
from bpy.props import BoolProperty

# Append the modules path to the system paths to be able to load the internal python modules
sys.path.append("%s/../modules" % os.path.dirname(os.path.realpath(__file__)))

# Options and Enumerators
#import bounding_box
#import camera_ops
#import consts
#import enumerators
#import exporters
#import file_ops
#import morphology_loader
#import piecewise_mesh_builder
#import rendering_ops
#import scene_ops
#import time_line
#import ui_interface
#import bridging_mesh_builder
#import mesh_ops
#import union_mesh_builder


import neuromorphovis as nmv
import neuromorphovis.bbox
import neuromorphovis.builders
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.file
import neuromorphovis.mesh
import neuromorphovis.scene
import neuromorphovis.utilities




##  A global reference to the reconstructed neuron mesh.
# This reference is used to link the operations in the other panels in the add-on with this panel.
reconstructed_neuron_mesh = None

# A global reference to the list of meshes that compose a disconnected neuron
# This reference is used to link the operations in the other panels in the add-on with this panel.
reconstructed_neuron_meshes = None



####################################################################################################
# @MeshOptions
####################################################################################################
class MeshOptions(bpy.types.Panel):
    """MeshOptions class"""

    # Panel options
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Mesh Options'
    bl_context = 'objectmode'
    bl_category = 'NeuroMorphoVis'

    # Meshing technique
    bpy.types.Scene.MeshingTechnique = EnumProperty(
        items=[(enumerators.__meshing_technique_piecewise__,
                'Piecewise Watertight',
                'Piecewise watertight meshes for each component'),
               (enumerators.__meshing_technique_bridging__,
                'Bridging (Watertight)',
                'Create a mesh using the bridging method'),
               (enumerators.__meshing_technique_union__,
                'Union (Watertight)',
                'Create a mesh using the union method')
               ],
        name='Method',
        default=enumerators.__meshing_technique_union__)

    # Is the soma connected to the first order branches or not !
    bpy.types.Scene.MeshSomaConnection = EnumProperty(
        items=[(enumerators.__meshing_soma_connected__,
                'Connected',
                'Connect the soma mesh to the arbors'),
               (enumerators.__meshing_soma_disconnected__,
                'Disconnected',
                'Create the soma as a separate mesh and do not connect it to the arbors')],
        name='Soma Connection',
        default=enumerators.__meshing_soma_disconnected__)

    # Edges, hard or smooth
    bpy.types.Scene.MeshSmoothing = EnumProperty(
        items=[(enumerators.__meshing_hard_edges__,
                'Original',
                'Make the edges between the segments hard'),
               (enumerators.__meshing_smooth_edges__,
                'Smooth',
                'Make the edges between the segments soft')],
        name='Edges',
        default=enumerators.__meshing_smooth_edges__)

    # Branching, is it based on angles or radii
    bpy.types.Scene.MeshBranching = EnumProperty(
        items=[(enumerators.__branching_angles__,
                'Angles',
                'Make the branching based on the angles at branching points'),
               (enumerators.__branching_radii__,
                'Radii',
                'Make the branching based on the radii of the children at the branching points')],
        name='Branching Style',
        default=enumerators.__branching_angles__)

    # Are the mesh objects connected or disconnected.
    bpy.types.Scene.MeshObjectsConnection = EnumProperty(
        items=[(enumerators.__meshing_objects_connected__,
                'Connected',
                'Connect all the objects of the mesh into one piece'),
               (enumerators.__meshing_objects_disconnected__,
                'Disconnected',
                'Keep the different mesh objects of the neuron into separate pieces')],
        name='Mesh Objects',
        default=enumerators.__meshing_objects_disconnected__)

    # Is the output model for reality or beauty
    bpy.types.Scene.MeshModel = EnumProperty(
        items=[(enumerators.__meshing_model_reality__,
                'Rough',
                'Create a mesh that looks like a real neuron reconstructed from microscope'),
               (enumerators.__meshing_model_beauty__,
                'Smooth',
                'Create a mesh that has smooth surface for visualization')],
        name='Model',
        default=enumerators.__meshing_model_beauty__)

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
        items=[(enumerators.__rendering_lambert__,
                'Lambert',
                "Use a Lambert shader"),
               (enumerators.__rendering_super_electron_light__,
                'Super Electron Light',
                "Use Highly Detailed Light Electron Shader"),
               (enumerators.__rendering_super_electron_dark__,
                'Super Electron Dark',
                "Use Highly Detailed Dark Electron Shader"),
               (enumerators.__rendering_electron_light__,
                'Electron Light',
                "Use Light Electron shader"),
               (enumerators.__rendering_electron_dark__,
                'Electron Dark',
                "Use Dark Electron shader"),
               (enumerators.__rendering_shadow__,
                'Shadow',
                "Use Shadows Shader"),
               (enumerators.__rendering_flat__,
                'Flat',
                "Use Flat Shader")],
        name="Material",
        default=enumerators.__rendering_lambert__)

    # Use single color for the all the objects in the mesh
    bpy.types.Scene.MeshHomogeneousColor = BoolProperty(
        name="Homogeneous Color",
        description="Use a single color for rendering all the objects of the mesh",
        default=True)

    # A homogeneous color for all the objects of the mesh
    bpy.types.Scene.NeuronMeshColor = FloatVectorProperty(
        name="Mesh Color", subtype='COLOR', default=(1.0, 0.0, 0.0), min=0.0, max=1.0,
        description="The homogeneous color of the reconstructed mesh")

    # The color of the reconstructed soma mesh
    bpy.types.Scene.SomaMeshColor = FloatVectorProperty(name="Soma Color", subtype='COLOR',
        default=(1.0, 0.0, 0.0), min=0.0, max=1.0,
        description="The color of the reconstructed soma mesh")

    # The color of the reconstructed axon mesh
    bpy.types.Scene.AxonMeshColor = FloatVectorProperty(name="Axon Color", subtype='COLOR',
        default=(0.0, 1.0, 0.0), min=0.0, max=1.0,
        description="The color of the reconstructed axon mesh")

    # The color of the reconstructed basal dendrites meshes
    bpy.types.Scene.BasalDendritesMeshColor = FloatVectorProperty(name="Basal Dendrites Color",
        subtype='COLOR', default=(0.0, 0.0, 1.0), min=0.0, max=1.0,
        description="The color of the reconstructed basal dendrites")

    # The color of the reconstructed apical dendrite meshe
    bpy.types.Scene.ApicalDendriteMeshColor = FloatVectorProperty(name="Apical Dendrite Color",
        subtype='COLOR', default=(1.0, 1.0, 0.0), min=0.0, max=1.0,
        description="The color of the reconstructed apical dendrite")

    # Rendering type
    bpy.types.Scene.MeshRenderingType = EnumProperty(
        items=[(enumerators.__rendering_full_view__,
                'Fixed Resolution',
                'Renders a full view of the morphology'),
               (enumerators.__rendering_to_scale__,
                'To Scale',
                'Renders an image of the full view at the right scale in (nm)'),
               (enumerators.__rendering_close_up__,
                'Close Up',
                'Renders a close up image the focuses on the soma')],
        name='Frame Type',
        default=enumerators.__rendering_full_view__)

    # Rendering extent
    bpy.types.Scene.MeshRenderingExtent = EnumProperty(
        items=[(enumerators.__rendering_whole_morphology__,
                'Whole Morphology',
                'Renders a view that considers all the neuron arbors'),
               (enumerators.__rendering_selected_components__,
                'Selected Arbors',
                'Renders a view that considers only the built neuron arbors')],
        name='Frame Type', default=enumerators.__rendering_whole_morphology__)

    # Mesh frame resolution
    bpy.types.Scene.MeshFrameResolution = IntProperty(
        name='Resolution',
        description='The resolution of the image generated from rendering the mesh',
        default=512, min=128, max=1024 * 10)

    # Frame scale factor 'for rendering to scale option '
    bpy.types.Scene.MeshFrameScaleFactor = FloatProperty(
        name="Scale", default=1.0, min=1.0, max=100.0,
        description="The scale factor for rendering a mesh to scale")

    # Mesh rendering close up dimensions
    bpy.types.Scene.MeshCloseUpDimensions = FloatProperty(
        name='Dimensions',
        description='The dimensions of the view that will be rendered in microns',
        default=20, min=5, max=100,)

    # Soma rendering progress bar
    bpy.types.Scene.NeuronMeshRenderingProgress = IntProperty(
        name="Rendering Progress",
        default=0, min=0, max=100, subtype='PERCENTAGE')

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """
        Draw the panel.

        :param context: Panel context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Get a reference to the scene
        scene = context.scene

        # Meshing method parameters
        meshing_method_row = layout.row()
        meshing_method_row.prop(scene, 'MeshingTechnique', icon='OUTLINER_OB_EMPTY')

        # Pass options from UI to system
        ui_interface.options.mesh.meshing_technique = scene.MeshingTechnique

        # Mesh model
        mesh_surface_row = layout.row()
        mesh_surface_row.label('Surface:')
        mesh_surface_row.prop(scene, 'MeshModel', expand=True)

        # Pass options from UI to system
        ui_interface.options.mesh.surface = scene.MeshModel

        if scene.MeshModel == enumerators.__meshing_model_beauty__:

            # Soma connection
            soma_connection_row = layout.row()
            soma_connection_row.label('Soma:')
            soma_connection_row.prop(scene, 'MeshSomaConnection', expand=True)

            # Pass options from UI to system
            ui_interface.options.mesh.soma_connection = scene.MeshSomaConnection

            # Mesh objects connection
            neuron_objects_connection_row = layout.row()
            neuron_objects_connection_row.label('Mesh Objects:')
            neuron_objects_connection_row.prop(scene, 'MeshObjectsConnection', expand=True)

            # Pass options from UI to system
            ui_interface.options.mesh.neuron_objects_connection = scene.MeshObjectsConnection

            # Mesh branching
            branching_row = layout.row()
            branching_row.label('Branching:')
            branching_row.prop(scene, 'MeshBranching', expand=True)

            # Pass options from UI to system
            ui_interface.options.mesh.branching = scene.MeshBranching

            # Add the vertex smoothing option only for the piecewise meshing
            if scene.MeshingTechnique == enumerators.__meshing_technique_piecewise__:

                # Smoothing
                smoothing_row = layout.row()
                smoothing_row.label('Branch Path:')
                smoothing_row.prop(scene, 'MeshSmoothing', expand=True)

                # Pass options from UI to system
                ui_interface.options.mesh.edges = scene.MeshSmoothing

            # Tessellation parameters
            tess_level_row = layout.row()
            tess_level_row.prop(scene, 'TessellateMesh')
            tess_level_column = tess_level_row.column()
            tess_level_column.prop(scene, 'MeshTessellationLevel')
            if not scene.TessellateMesh:
                ui_interface.options.mesh.tessellation_level = 1.0 # To disable the tessellation
                tess_level_column.enabled = False

            # Pass options from UI to system
            ui_interface.options.mesh.tessellate_mesh = scene.TessellateMesh
            ui_interface.options.mesh.tessellation_level = scene.MeshTessellationLevel

        # Update the dfault parameters to the rough
        else:

            # Pass options from UI to system
            ui_interface.options.mesh.neuron_objects_connection = \
                enumerators.__meshing_objects_connected__
            ui_interface.options.mesh.soma_connection = enumerators.__meshing_soma_connected__
            ui_interface.options.mesh.edges = enumerators.__meshing_smooth_edges__


        # Coloring parameters
        colors_row = layout.row()
        colors_row.label(text='Colors & Materials:', icon='COLOR')

        # Mesh material
        mesh_material_row = layout.row()
        mesh_material_row.prop(scene, 'MeshMaterial')

        # Pass options from UI to system
        ui_interface.options.mesh.material = scene.MeshMaterial

        # Homogeneous mesh coloring
        homogeneous_color_row = layout.row()
        homogeneous_color_row.prop(scene, 'MeshHomogeneousColor')

        # If the homogeneous color flag is set
        if scene.MeshHomogeneousColor:
            neuron_color_row = layout.row()
            neuron_color_row.prop(scene, 'NeuronMeshColor')

            # Pass options from UI to system
            ui_interface.options.mesh.soma_color = \
                Vector((scene.NeuronMeshColor.r, scene.NeuronMeshColor.g, scene.NeuronMeshColor.b))
            ui_interface.options.mesh.axon_color = \
                Vector((scene.NeuronMeshColor.r, scene.NeuronMeshColor.g, scene.NeuronMeshColor.b))
            ui_interface.options.mesh.basal_dendrites_color = \
                Vector((scene.NeuronMeshColor.r, scene.NeuronMeshColor.g, scene.NeuronMeshColor.b))
            ui_interface.options.mesh.apical_dendrites_color = \
                Vector((scene.NeuronMeshColor.r, scene.NeuronMeshColor.g, scene.NeuronMeshColor.b))

        # Different colors
        else:
            soma_color_row = layout.row()
            soma_color_row.prop(scene, 'SomaMeshColor')
            axon_color_row = layout.row()
            axon_color_row.prop(scene, 'AxonMeshColor')
            basal_dendrites_color_row = layout.row()
            basal_dendrites_color_row.prop(scene, 'BasalDendritesMeshColor')
            apical_dendrites_color_row = layout.row()
            apical_dendrites_color_row.prop(scene, 'ApicalDendriteMeshColor')

            # Pass options from UI to system
            ui_interface.options.mesh.soma_color = Vector(
                (scene.SomaMeshColor.r, scene.SomaMeshColor.g, scene.SomaMeshColor.b))
            ui_interface.options.mesh.axon_color = Vector(
                (scene.AxonMeshColor.r, scene.AxonMeshColor.g, scene.AxonMeshColor.b))
            ui_interface.options.mesh.basal_dendrites_color = \
                Vector((scene.BasalDendritesMeshColor.r, scene.BasalDendritesMeshColor.g,
                        scene.BasalDendritesMeshColor.b))
            ui_interface.options.mesh.apical_dendrites_color = \
                Vector((scene.ApicalDendriteMeshColor.r, scene.ApicalDendriteMeshColor.g,
                        scene.ApicalDendriteMeshColor.b))

        # Mesh reconstruction options
        mesh_reconstruction_row = layout.row()
        mesh_reconstruction_row.operator('reconstruct.neuron_mesh', icon='MESH_DATA')

        # Rendering options
        quick_rendering_row = layout.row()
        quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')

        # Rendering type
        rendering_type_row = layout.row()
        rendering_type_row.prop(scene, 'MeshRenderingType', expand=True)

        # Rendering extent
        rendering_extent_row = layout.row()
        rendering_extent_row.prop(scene, 'MeshRenderingExtent', expand=True)

        frame_resolution_row = None
        scale_factor_row = None
        render_close_up_row = None

        if scene.MeshRenderingType == enumerators.__rendering_full_view__ or \
           scene.MeshRenderingType == enumerators.__rendering_close_up__:

            # Frame resolution option
            frame_resolution_row = layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(scene, 'MeshFrameResolution')
            frame_resolution_row.enabled = True

        if scene.MeshRenderingType == enumerators.__rendering_to_scale__:

            # Scale factor option
            scale_factor_row = layout.row()
            scale_factor_row.label(text='Resolution Scale:')
            scale_factor_row.prop(scene, 'MeshFrameScaleFactor')
            scale_factor_row.enabled = True

        if scene.MeshRenderingType == enumerators.__rendering_close_up__:

            # Render close up option
            render_close_up_row = layout.row()
            render_close_up_row.prop(scene, 'MeshCloseUpDimensions')

        # Rendering view
        render_view_row = layout.row()
        render_view_row.label(text='Render View:', icon='RESTRICT_RENDER_OFF')
        render_view_buttons_row = layout.row(align=True)
        render_view_buttons_row.operator('render_mesh.front', icon='AXIS_FRONT')
        render_view_buttons_row.operator('render_mesh.side', icon='AXIS_SIDE')
        render_view_buttons_row.operator('render_mesh.top', icon='AXIS_TOP')
        render_view_buttons_row.enabled = True

        render_animation_row = layout.row()
        render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
        render_animations_buttons_row = layout.row(align=True)
        render_animations_buttons_row.operator('render_mesh.360', icon='FORCE_MAGNETIC')
        render_animations_buttons_row.enabled = True

        # Soma rendering progress bar
        neuron_mesh_rendering_progress_row = layout.row()
        neuron_mesh_rendering_progress_row.prop(scene, 'NeuronMeshRenderingProgress')
        neuron_mesh_rendering_progress_row.enabled = False

        # Saving meshes parameters
        save_neuron_mesh_row = layout.row()
        save_neuron_mesh_row.label(text='Save Neuron Mesh As:', icon='MESH_UVSPHERE')

        save_neuron_mesh_buttons_column = layout.column(align=True)
        save_neuron_mesh_buttons_column.operator('save_neuron_mesh.obj', icon='MESH_DATA')
        save_neuron_mesh_buttons_column.operator('save_neuron_mesh.ply', icon='GROUP_VERTEX')
        save_neuron_mesh_buttons_column.operator('save_neuron_mesh.stl', icon='RETOPO')
        save_neuron_mesh_buttons_column.operator('save_neuron_mesh.blend', icon='OUTLINER_OB_META')
        save_neuron_mesh_buttons_column.enabled = True

        # If no given data, then disable some buttons
        global reconstructed_neuron_mesh
        global reconstructed_neuron_meshes

        if nmv.scene.ops.is_object_in_scene(reconstructed_neuron_mesh) or \
                not nmv.scene.ops.is_it_null(reconstructed_neuron_meshes):
            rendering_type_row.enabled = True

            if frame_resolution_row is not None:
                frame_resolution_row.enabled = True

            if scale_factor_row is not None:
                scale_factor_row.enabled = True

            if render_close_up_row is not None:
                render_close_up_row.enabled = True

            render_view_buttons_row.enabled = True
            render_animations_buttons_row.enabled = True
            save_neuron_mesh_buttons_column.enabled = True
        else:
            rendering_type_row.enabled = False
            if frame_resolution_row is not None:
                frame_resolution_row.enabled = False

            if scale_factor_row is not None:
                scale_factor_row.enabled = False

            if render_close_up_row is not None:
                render_close_up_row.enabled = False

            render_view_buttons_row.enabled = False
            render_animations_buttons_row.enabled = False
            save_neuron_mesh_buttons_column.enabled = False


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
    def load_morphology(self, scene):
        """
        Loads the morphology from file.

        :param scene: Scene.
        """

        # Read the data from a given morphology file either in .h5 or .swc formats
        if bpy.context.scene.InputSource == enumerators.__input_h5_swc_file__:

            # Pass options from UI to system
            ui_interface.options.morphology.morphology_file_path = scene.MorphologyFile

            # Update the morphology label
            ui_interface.options.morphology.label = file_ops.get_file_name_from_path(
                scene.MorphologyFile)

            # Load the morphology from the file
            loading_flag, morphology_object = morphology_loader.load_from_file(
                options=ui_interface.options)

            # Verify the loading operation
            if loading_flag:

                # Update the morphology
                ui_interface.morphology = morphology_object

            # Otherwise, report an ERROR
            else:
                self.report({'ERROR'}, 'Invalid Morphology File')

        # Read the data from a specific gid in a given circuit
        elif bpy.context.scene.InputSource == enumerators.__input_circuit_gid__:

            # Pass options from UI to system
            ui_interface.options.morphology.blue_config = scene.CircuitFile
            ui_interface.options.morphology.gid = scene.Gid

            # Update the morphology label
            ui_interface.options.morphology.label = 'neuron_' + str(scene.Gid)

            # Load the morphology from the circuit
            loading_flag, morphology_object = morphology_loader.load_from_circuit(
                options=ui_interface.options)

            # Verify the loading operation
            if loading_flag:

                # Update the morphology
                ui_interface.morphology = morphology_object

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
        self.load_morphology(scene=context.scene)

        # Create a mesh builder object
        mesh_builder=None
        if ui_interface.options.mesh.meshing_technique == enumerators.__meshing_technique_piecewise__:
            mesh_builder = piecewise_mesh_builder.PiecewiseBuilder(
                morphology=ui_interface.morphology, options=ui_interface.options)
        elif ui_interface.options.mesh.meshing_technique == enumerators.__meshing_technique_bridging__:
            mesh_builder = bridging_mesh_builder.BridgingBuilder(
                morphology=ui_interface.morphology, options=ui_interface.options)
        elif ui_interface.options.mesh.meshing_technique == enumerators.__meshing_technique_union__:
            mesh_builder = union_mesh_builder.UnionBuilder(
                morphology=ui_interface.morphology, options=ui_interface.options)
        else:
            nmv.logger.log('ERROR: unknown method')

        # Reconstruct the mesh
        #global reconstructed_neuron_mesh
        #global reconstructed_neuron_meshes
        #reconstructed_neuron_mesh, reconstructed_neuron_meshes = mesh_builder.reconstruct_mesh()
        mesh_builder.reconstruct_mesh()

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
        """
        Execute the operator.

        :param context: Context.
        :return: 'FINISHED'
        """

        # Get a reference to the scene
        scene = context.scene

        # Ensure that there is a valid directory where the images will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.images_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.images_directory)

        # Report the process starting in the UI
        self.report({'INFO'}, 'Mesh Rendering ... Wait')

        # Render a full view
        if scene.MeshRenderingType == enumerators.__rendering_full_view__:
            rendering_ops.render_full_view(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_mesh' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MeshFrameResolution,
                camera_view='FRONT')

        # Render mesh to scale
        if scene.MeshRenderingType == enumerators.__rendering_to_scale__:
            rendering_ops.render_full_view_to_scale(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_mesh_to_scale' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_scale_factor=scene.MeshFrameScaleFactor,
                camera_view='FRONT')

        # Render a close up of the mesh
        if scene.MeshRenderingType == enumerators.__rendering_close_up__:
            rendering_ops.render_close_up(
                image_name='%s_mesh' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MeshFrameResolution,
                camera_view='FRONT',
                close_up_dimension=scene.MeshCloseUpDimensions)

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
        """
        Execute the operator.

        :param context: Context.
        :return: 'FINISHED'
        """

        # Get a reference to the scene
        scene = context.scene

        # Ensure that there is a valid directory where the images will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.images_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.images_directory)

        # Report the process starting in the UI
        self.report({'INFO'}, 'Mesh Rendering ... Wait')

        # Render a full view
        if scene.MeshRenderingType == enumerators.__rendering_full_view__:
            rendering_ops.render_full_view(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_mesh' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MeshFrameResolution,
                camera_view='SIDE')

        # Render mesh to scale
        if scene.MeshRenderingType == enumerators.__rendering_to_scale__:
            rendering_ops.render_full_view_to_scale(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_mesh_to_scale' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_scale_factor=scene.MeshFrameScaleFactor,
                camera_view='SIDE')

        # Render a close up of the mesh
        if scene.MeshRenderingType == enumerators.__rendering_close_up__:
            rendering_ops.render_close_up(
                image_name='%s_mesh_to_scale' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MeshFrameResolution,
                camera_view='SIDE',
                close_up_dimension=scene.MeshCloseUpDimensions)

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
        """
        Execute the operator.

        :param context: Context.
        :return: 'FINISHED'
        """

        # Get a reference to the scene
        scene = context.scene

        # Ensure that there is a valid directory where the images will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.images_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.images_directory)

        # Report the process starting in the UI
        self.report({'INFO'}, 'Mesh Rendering ... Wait')

        # Render a full view
        if scene.MeshRenderingType == enumerators.__rendering_full_view__:
            rendering_ops.render_full_view(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_mesh' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MeshFrameResolution,
                camera_view='TOP')

        # Render mesh to scale
        if scene.MeshRenderingType == enumerators.__rendering_to_scale__:
            rendering_ops.render_full_view_to_scale(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_mesh' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_scale_factor=scene.MeshFrameScaleFactor,
                camera_view='TOP')

        # Render a close up of the mesh
        if scene.MeshRenderingType == enumerators.__rendering_close_up__:
            rendering_ops.render_close_up(
                image_name='%s_mesh' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MeshFrameResolution,
                camera_view='TOP',
                close_up_dimension=scene.MeshCloseUpDimensions)

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

    # Camera parameters
    camera_360 = None

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
            frame_name = '%s/frame_%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Render a frame
            global reconstructed_neuron_mesh
            global reconstructed_neuron_meshes

            # If we have the mesh as a single object, then render it directly
            if reconstructed_neuron_mesh is not None:
                rendering_ops.render_frame_at_angle(
                    scene_objects=[reconstructed_neuron_mesh],
                    camera=self.camera_360,
                    angle=self.timer_limits,
                    frame_name=frame_name)

            # Otherwise, group the meshes into a single mesh and then render it
            else:
                if reconstructed_neuron_meshes is not None:

                    # Group the neuron meshes into a single neuron
                    neuron_mesh = mesh_ops.join_mesh_objects(reconstructed_neuron_meshes, 'neuron')

                    # Render the neuron
                    rendering_ops.render_frame_at_angle(
                        scene_objects=[neuron_mesh],
                        camera=self.camera_360,
                        angle=self.timer_limits,
                        frame_name=frame_name)

            # Update the progress shell
            time_line.show_progress('Rendering', self.timer_limits, 360)

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
        """
        Execute the operator.

        :param context: Panel context.
        """

        # Get a reference to the scene
        scene = context.scene

        # Ensure that there is a valid directory where the images will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.sequences_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.sequences_directory)

        # Compute the 360 bounding box
        bounding_box_360 = bounding_box.compute_360_bounding_box(
            ui_interface.morphology.bounding_box, ui_interface.morphology.soma.centroid)

        # Create the camera
        self.camera_360 = camera_ops.create_camera(view_bounding_box=bounding_box_360,
            image_base_resolution=scene.MorphologyFrameResolution)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_mesh_360' % (
            ui_interface.options.output.sequences_directory, ui_interface.options.morphology.label)
        file_ops.clean_and_create_directory(self.output_directory)

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

        # Delete the camera
        nmv.scene.ops.delete_list_objects([self.camera_360])

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @SaveNeuronMeshOBJ
####################################################################################################
class SaveNeuronMeshOBJ(bpy.types.Operator):
    """zSave the neuron mesh in OBJ file"""

    # Operator parameters
    bl_idname = "save_neuron_mesh.obj"
    bl_label = "Wavefront (.obj)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Executes the operator

        Keyword arguments:
        :param context: Operator context.
        :return: {'FINISHED'}
        """

        # Ensure that there is a valid directory where the meshes will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.meshes_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.meshes_directory)

        # Address the global variable
        global reconstructed_neuron_mesh
        global reconstructed_neuron_meshes

        # If we have the mesh as a single object, then render it directly
        if reconstructed_neuron_mesh is not None:

            # Export the selected soma mesh as an .obj file
            exporters.export_object_to_obj_file(
                mesh_object=reconstructed_neuron_mesh,
                output_directory=ui_interface.options.output.meshes_directory,
                output_file_name=ui_interface.morphology.label)

        # Otherwise, group the meshes into a single mesh and then render it
        else:
            if reconstructed_neuron_meshes is not None:

                # Group the neuron meshes into a single neuron
                neuron_mesh = mesh_ops.join_mesh_objects(reconstructed_neuron_meshes, 'neuron')

                # Export the selected soma mesh as an .obj file
                exporters.export_object_to_obj_file(
                    mesh_object=neuron_mesh,
                    output_directory=ui_interface.options.output.meshes_directory,
                    output_file_name=ui_interface.morphology.label)

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

        Keyword arguments:
        :param context: Operator context.
        :return: {'FINISHED'}
        """

        # Ensure that there is a valid directory where the meshes will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.meshes_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.meshes_directory)

        # Address the global variable
        global reconstructed_neuron_mesh

        # Export the selected soma mesh as a .ply file
        exporters.export_object_to_ply_file(
            mesh_object=reconstructed_neuron_mesh,
            output_directory=ui_interface.options.output.meshes_directory,
            output_file_name=ui_interface.morphology.label)

        # Address the global variable
        global reconstructed_neuron_mesh
        global reconstructed_neuron_meshes

        # If we have the mesh as a single object, then export it directly
        if reconstructed_neuron_mesh is not None:

            # Export the selected soma mesh as a .ply file
            exporters.export_object_to_ply_file(
                mesh_object=reconstructed_neuron_mesh,
                output_directory=ui_interface.options.output.meshes_directory,
                output_file_name=ui_interface.morphology.label)

        # Otherwise, group the meshes into a single mesh and then export it
        else:
            if reconstructed_neuron_meshes is not None:
                # Group the neuron meshes into a single neuron
                neuron_mesh = mesh_ops.join_mesh_objects(reconstructed_neuron_meshes, 'neuron')

                # Export the selected soma mesh as a .ply file
                exporters.export_object_to_ply_file(
                    mesh_object=neuron_mesh,
                    output_directory=ui_interface.options.output.meshes_directory,
                    output_file_name=ui_interface.morphology.label)

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
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.meshes_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.meshes_directory)

        # Address the global variable
        global reconstructed_neuron_mesh
        global reconstructed_neuron_meshes

        # If we have the mesh as a single object, then export it directly
        if reconstructed_neuron_mesh is not None:

            # Export the selected soma mesh as a .stl file
            exporters.export_object_to_stl_file(
                mesh_object=reconstructed_neuron_mesh,
                output_directory=ui_interface.options.output.meshes_directory,
                output_file_name=ui_interface.morphology.label)

        # Otherwise, group the meshes into a single mesh and then export it
        else:
            if reconstructed_neuron_meshes is not None:

                # Group the neuron meshes into a single neuron
                neuron_mesh = mesh_ops.join_mesh_objects(reconstructed_neuron_meshes, 'neuron')

                # Export the selected soma mesh as a .stl file
                exporters.export_object_to_stl_file(
                    mesh_object=neuron_mesh,
                    output_directory=ui_interface.options.output.meshes_directory,
                    output_file_name=ui_interface.morphology.label)

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

        Keyword arguments:
        :param context: Operator context.
        :return: {'FINISHED'}
        """


        # Ensure that there is a valid directory where the meshes will be written to
        if ui_interface.options.output.output_directory is None:
            self.report({'ERROR'}, nmv.consts.__msg_path_not_set__)
            return {'FINISHED'}

        if not file_ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.__msg_invalid_output_path__)
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.meshes_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.meshes_directory)

        # Address the global variable
        global reconstructed_neuron_mesh

        # Export the selected soma mesh as an .blend file
        exporters.export_object_to_blend_file(
            mesh_object=reconstructed_neuron_mesh,
            output_directory=ui_interface.options.output.meshes_directory,
            output_file_name=ui_interface.morphology.label)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Mesh reconstruction panel
    bpy.utils.register_class(MeshOptions)

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
    """Un-registers all the classes in this panel"""

    # Mesh reconstruction panel
    bpy.utils.unregister_class(MeshOptions)

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