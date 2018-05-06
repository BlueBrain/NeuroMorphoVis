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
import sys, os

# Blender imports
import bpy
from bpy.props import EnumProperty
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import BoolProperty
from bpy.props import FloatVectorProperty
from mathutils import Vector

# Append the modules path to the system paths to be able to load the internal python modules
sys.path.append("%s/../modules" % os.path.dirname(os.path.realpath(__file__)))

# Internal imports
import bounding_box
import consts
import camera_ops
import enumerators
import file_ops
import exporters
import rendering_ops
import skeleton_builder
import scene_ops
import morphology_loader
import ui_interface
import time_line


# A global reference to the reconstructed morphology objects.
# This reference is used to link the operations in the other panels in the add-on with this panel.
reconstructed_morphology_objects = None

####################################################################################################
# @update_bounding_box_panel
####################################################################################################
def update_bounding_box_panel(scene, bbox):
    """
    Update the bounding box panel.
    :param scene: Input scene.
    :param bbox: Bounding box.
    """

    # PMin
    scene.BBoxPMinX = bbox.p_min[0]
    scene.BBoxPMinY = bbox.p_min[1]
    scene.BBoxPMinZ = bbox.p_min[2]

    # PMax
    scene.BBoxPMaxX = bbox.p_max[0]
    scene.BBoxPMaxY = bbox.p_max[1]
    scene.BBoxPMaxZ = bbox.p_max[2]

    # Center
    scene.BBoxCenterX = bbox.center[0]
    scene.BBoxCenterY = bbox.center[1]
    scene.BBoxCenterZ = bbox.center[2]

    # Bounds
    scene.BoundsX = bbox.bounds[0]
    scene.BoundsY = bbox.bounds[1]
    scene.BoundsZ = bbox.bounds[2]


####################################################################################################
# @MorphologyOptions
####################################################################################################
class MorphologyOptions(bpy.types.Panel):
    """Morphology reconstruction options"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Morphology Options'
    bl_context = 'objectmode'
    bl_category = 'NeuroMorphoVis'

    ################################################################################################
    # Panel options
    ################################################################################################
    # Build soma
    bpy.types.Scene.BuildSoma = EnumProperty(
        items=[(enumerators.__soma_ignore__,
                'Ignore',
                'Ignore soma reconstruction'),
               (enumerators.__soma_sphere__,
                'Sphere',
                'Represent the soma by a sphere'),
               (enumerators.__soma_soft_body__,
                'Profile',
                'Reconstruct a 3D profile of the soma')],
        name='Soma', default=enumerators.__soma_sphere__)

    # Build axon
    bpy.types.Scene.BuildAxon = BoolProperty(
        name="Build Axon",
        description="Select this flag to reconstruct the axon",
        default=True)

    # Axon branching level
    bpy.types.Scene.AxonBranchingLevel = IntProperty(
        name="Branching Level",
        description="Branching level for the axon",
        default=100, min=1, max=100)

    # Build basal dendrites
    bpy.types.Scene.BuildBasalDendrites = BoolProperty(
        name="Build Basal Dendrites",
        description="Select this flag to reconstruct the basal dendrites",
        default=True)

    # Basal dendrites branching level
    bpy.types.Scene.BasalDendritesBranchingLevel = IntProperty(
        name="Branching Level",
        description="Branching level for the basal dendrites",
        default=100, min=1, max=100)

    # Build apical dendrite
    bpy.types.Scene.BuildApicalDendrite = BoolProperty(
        name="Build Apical Dendrites",
        description="Select this flag to reconstruct the apical dendrite (if exists)",
        default=True)

    # Apical dendrite branching level
    bpy.types.Scene.ApicalDendriteBranchingLevel = IntProperty(
        name="Branching Level",
        description="Branching level for the apical dendrite",
        default=100, min=1, max=100)

    # Draw bounding box
    bpy.types.Scene.DrawBoundingBox = BoolProperty(
        name="Draw Bounding Box",
        description="Draws the bounding box of the morphology",
        default=False)

    # Display bounding box info
    bpy.types.Scene.DisplayBoundingBox = BoolProperty(
        name="Display Bounding Box Info",
        description="Displays the bounding box of the morphology",
        default=False)

    # Bounding box data
    bpy.types.Scene.BBoxPMinX = FloatProperty(name="X", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxPMinY = FloatProperty(name="Y", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxPMinZ = FloatProperty(name="Z", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxPMaxX = FloatProperty(name="X", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxPMaxY = FloatProperty(name="Y", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxPMaxZ = FloatProperty(name="Z", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxCenterX = FloatProperty(name="X", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxCenterY = FloatProperty(name="Y", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxCenterZ = FloatProperty(name="Z", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BoundsX = FloatProperty(name="X", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BoundsY = FloatProperty(name="Y", min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BoundsZ = FloatProperty(name="Z", min=-1e10, max=1e10, subtype='FACTOR')

    # Morphology material
    bpy.types.Scene.MorphologyMaterial = EnumProperty(
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

    # Color arbor by part
    bpy.types.Scene.ColorArborByPart = BoolProperty(
        name="Color Arbor By Part",
        description="Each component of the arbor will be assigned a different color",
        default=False)

    # Color arbor using black and white alternatives
    bpy.types.Scene.ColorArborBlackAndWhite = BoolProperty(
        name="Black / White",
        description="Each component of the arbor will be assigned a either black or white",
        default=False)

    # Soma color
    bpy.types.Scene.SomaColor = FloatVectorProperty(
        name="Soma Color",
        subtype='COLOR', default=enumerators.__soma_color__, min=0.0, max=1.0,
        description="The color of the reconstructed soma")

    # Axon color
    bpy.types.Scene.AxonColor = FloatVectorProperty(
        name="Axon Color",
        subtype='COLOR', default=enumerators.__axon_color__, min=0.0, max=1.0,
        description="The color of the reconstructed axon")

    # Basal dendrites color
    bpy.types.Scene.BasalDendritesColor = FloatVectorProperty(
        name="Basal Dendrites  Color",
        subtype='COLOR', default=enumerators.__basal_dendrites_color__, min=0.0, max=1.0,
        description="The color of the reconstructed basal dendrites")

    # Apical dendrite color
    bpy.types.Scene.ApicalDendriteColor = FloatVectorProperty(
        name="Apical Dendrite Color",
        subtype='COLOR', default=enumerators.__apical_dendrites_color__, min=0.0, max=1.0,
        description="The color of the reconstructed apical dendrite")

    # Articulation color
    bpy.types.Scene.ArticulationColor = FloatVectorProperty(
        name="Articulation Color",
        subtype='COLOR', default=enumerators.__articulation_color__, min=0.0, max=1.0,
        description="The color of the articulations in the Articulated Section mode")

    # Reconstruction method
    bpy.types.Scene.MorphologyReconstructionTechnique = EnumProperty(
        items=[(enumerators.__method_disconnected_skeleton__,
                'Disconnected Skeleton (Original)',
                "The skeleton is disconnected at the branching points"),
               (enumerators.__method_disconnected_skeleton_resampled__,
                'Disconnected Skeleton (Resampled)',
                "The skeleton is disconnected at the branching points and resampled"),
               (enumerators.__method_disconnected_segments__,
                'Disconnected Segments',
                "Each segment is an independent object (this approach is time consuming)"),
               (enumerators.__method_disconnected_sections__,
                'Disconnected Sections',
                "Each section is an independent object"),
               (enumerators.__method_articulated_sections__,
                'Articulated Sections',
                "Each section is an independent object, but connected with a pivot"),
               (enumerators.__method_connected_sections__,
                'Connected Sections (Original)',
                "The sections of a single arbor are connected together"),
               (enumerators.__method_connected_sections_repaired__,
                'Connected Sections (Repaired)',
                "The morphology is repaired and fully reconstructed ")],
        name="Method",
        default=enumerators.__method_connected_sections_repaired__)

    # Branching, is it based on angles or radii
    bpy.types.Scene.MorphologyBranching = EnumProperty(
        items=[(enumerators.__branching_angles__,
                'Angles',
                'Make the branching based on the angles at branching points'),
               (enumerators.__branching_radii__,
                'Radii',
                'Make the branching based on the radii of the children at the branching points')],
        name='Branching Style',
        default=enumerators.__branching_angles__)

    # Connect to soma if the connected method is used
    bpy.types.Scene.ConnectToSoma = BoolProperty(
        name="Connect to Soma",
        description="Connect the arbors to the soma",
        default=True)

    # Arbor quality
    bpy.types.Scene.ArborQuality = IntProperty(
        name="Sides",
        description="Number of vertices of the cross-section of each segment along the arbor",
        default=16, min=4, max=128)

    # Section radius
    bpy.types.Scene.SectionsRadii = EnumProperty(
        items=[(enumerators.__sections__radii__as_specified__,
                'As Specified in Morphology',
                "Use the cross-sectional radii reported in the morphology file"),
               (enumerators.__sections__radii__at_fixed_scale__,
                'At a Fixed Diameter',
                "Set all the arbors to a fixed radius"),
               (enumerators.__sections__radii__with_scale_factor__,
                'With Scale Factor',
                "Scale all the arbors using a specified scale factor")],
        name="Sections Radii",
        default=enumerators.__sections__radii__as_specified__)

    # Fixed section radius value
    bpy.types.Scene.FixedRadiusValue = FloatProperty(
        name="Value (micron)",
        description="The value of the radius in microns between (0.05 and 5.0) microns",
        default=1.0, min=0.05, max=5.0)

    # Global radius scale value
    bpy.types.Scene.RadiusScaleValue= FloatProperty(
        name="Scale",
        description="A scale factor for scaling the radii of the arbors between (0.01 and 5.0)",
        default=1.0, min=0.01, max=5.0)

    # Rendering type
    bpy.types.Scene.RenderingType = EnumProperty(
        items=[(enumerators.__rendering_full_view__,
                'Fixed Resolution',
                'Renders a full view of the morphology'),
               (enumerators.__rendering_to_scale__,
                'To Scale',
                'Renders an image of the full view at the right scale in (um)'),
               (enumerators.__rendering_close_up__,
                'Close Up',
                'Renders a close up image the focuses on the soma')],
        name='Frame Type', default=enumerators.__rendering_full_view__)

    # Rendering extent
    bpy.types.Scene.RenderingExtent = EnumProperty(
        items=[(enumerators.__rendering_whole_morphology__,
                'Whole Morphology',
                'Renders a view that considers all the morphology components'),
               (enumerators.__rendering_selected_components__,
                'Selected Arbors',
                'Renders a view that considers only the built morphology components')],
        name='Frame Type', default=enumerators.__rendering_whole_morphology__)

    # Frame resolution
    bpy.types.Scene.MorphologyFrameResolution = IntProperty(
        name="Resolution", default=512, min=128, max=1024 * 10,
        description="The resolution of the image generated from rendering the morphology")

    # Frame scale factor 'for rendering to scale option '
    bpy.types.Scene.MorphologyFrameScaleFactor = FloatProperty(
        name="Scale", default=1.0, min=1.0, max=100.0,
        description="The scale factor for rendering a morphology to scale")

    # Morphology close up dimensions
    bpy.types.Scene.MorphologyCloseUpDimensions = FloatProperty(
        name="Dimensions",
        default=20, min=5, max=100,
        description="The dimensions of the view that will be rendered in microns")

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """
        Draws the panel.

        :param context: Panel context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Get a reference to the scene
        scene = context.scene

        # Morphology skeleton options
        skeleton_row = layout.row()
        skeleton_row.label(text='Morphology Skeleton:', icon='POSE_DATA')

        # Build soma options
        build_soma_row = layout.row()
        build_soma_row.label('Soma:')
        build_soma_row.prop(scene, 'BuildSoma', expand=True)

        # Pass options from UI to system
        ui_interface.options.morphology.soma_representation = scene.BuildSoma

        # Build axon options
        axon_row = layout.row()
        axon_row.prop(scene, 'BuildAxon')
        axon_level_row = axon_row.column()
        axon_level_row.prop(scene, 'AxonBranchingLevel')
        if not scene.BuildAxon:
            axon_level_row.enabled = False
        else:
            axon_level_row.enabled = True

        # Pass options from UI to system
        ui_interface.options.morphology.ignore_axon = not scene.BuildAxon
        ui_interface.options.morphology.axon_branch_order = scene.AxonBranchingLevel

        # Build basal dendrites options
        basal_dendrites_row = layout.row()
        basal_dendrites_row.prop(scene, 'BuildBasalDendrites')
        basal_dendrites_level_row = basal_dendrites_row.column()
        basal_dendrites_level_row.prop(scene, 'BasalDendritesBranchingLevel')
        if not scene.BuildBasalDendrites:
            basal_dendrites_level_row.enabled = False
        else:
            basal_dendrites_level_row.enabled = True

        # Pass options from UI to system
        ui_interface.options.morphology.ignore_basal_dendrites = not scene.BuildBasalDendrites
        ui_interface.options.morphology.basal_dendrites_branch_order = \
            scene.BasalDendritesBranchingLevel

        # Build apical dendrite option
        apical_dendrite_row = layout.row()
        apical_dendrite_row.prop(scene, 'BuildApicalDendrite')
        apical_dendrite_level_row = apical_dendrite_row.column()
        apical_dendrite_level_row.prop(scene, 'ApicalDendriteBranchingLevel')
        if not scene.BuildApicalDendrite:
            apical_dendrite_level_row.enabled = False
        else:
            apical_dendrite_level_row.enabled = True

        # Pass options from UI to system
        ui_interface.options.morphology.ignore_apical_dendrite = not scene.BuildApicalDendrite
        ui_interface.options.morphology.apical_dendrite_branch_order = \
            scene.ApicalDendriteBranchingLevel

        # Bounding box options
        bounding_box_row = layout.row()
        bounding_box_row.label(text='Morphology Bounding Box:', icon='BORDER_RECT')

        # Draw bounding box option
        draw_bounding_box_row = layout.row()
        draw_bounding_box_row.prop(scene, 'DrawBoundingBox')

        # Display bounding box option
        display_bounding_box_row = layout.row()
        display_bounding_box_row.prop(scene, 'DisplayBoundingBox')

        # if globals.objects.loaded_morphology_object is not None:
        # TODO: Fix globals
        if scene.DisplayBoundingBox:
            bounding_box_p_row = layout.row()
            bounding_box_p_min_row = bounding_box_p_row.column(align=True)
            bounding_box_p_min_row.label(text='PMin:')
            bounding_box_p_min_row.prop(scene, 'BBoxPMinX')
            bounding_box_p_min_row.prop(scene, 'BBoxPMinY')
            bounding_box_p_min_row.prop(scene, 'BBoxPMinZ')
            bounding_box_p_min_row.enabled = False

            bounding_box_p_max_row = bounding_box_p_row.column(align=True)
            bounding_box_p_max_row.label(text='PMax:')
            bounding_box_p_max_row.prop(scene, 'BBoxPMaxX')
            bounding_box_p_max_row.prop(scene, 'BBoxPMaxY')
            bounding_box_p_max_row.prop(scene, 'BBoxPMaxZ')
            bounding_box_p_max_row.enabled = False

            bounding_box_data_row = layout.row()
            bounding_box_center_row = bounding_box_data_row.column(align=True)
            bounding_box_center_row.label(text='Center:')
            bounding_box_center_row.prop(scene, 'BBoxCenterX')
            bounding_box_center_row.prop(scene, 'BBoxCenterY')
            bounding_box_center_row.prop(scene, 'BBoxCenterZ')
            bounding_box_center_row.enabled = False

            bounding_box_bounds_row = bounding_box_data_row.column(align=True)
            bounding_box_bounds_row.label(text='Bounds:')
            bounding_box_bounds_row.prop(scene, 'BoundsX')
            bounding_box_bounds_row.prop(scene, 'BoundsY')
            bounding_box_bounds_row.prop(scene, 'BoundsZ')
            bounding_box_bounds_row.enabled = False

        # Reconstruction options
        reconstruction_options_row = layout.row()
        reconstruction_options_row.label(text='Reconstruction Options:', icon='OUTLINER_OB_EMPTY')

        # Morphology reconstruction techniques option
        morphology_reconstruction_row = layout.row()
        morphology_reconstruction_row.prop(
            scene, 'MorphologyReconstructionTechnique', icon='FORCE_CURVE')

        # Pass options from UI to system
        ui_interface.options.morphology.reconstruction_method = \
            scene.MorphologyReconstructionTechnique

        # Connect to the soma option
        reconstruction_technique = scene.MorphologyReconstructionTechnique
        if reconstruction_technique == enumerators.__method_connected_sections_repaired__ \
            or reconstruction_technique == enumerators.__method_connected_sections__\
            or reconstruction_technique == enumerators.__method_disconnected_skeleton__ \
            or reconstruction_technique == enumerators.__method_disconnected_skeleton_resampled__:

            # Morphology branching
            branching_row = layout.row()
            branching_row.label('Branching:')
            branching_row.prop(scene, 'MorphologyBranching', expand=True)

            # Pass options from UI to system
            ui_interface.options.morphology.branching = scene.MorphologyBranching

            connect_to_soma_row = layout.row()
            connect_to_soma_row.prop(scene, 'ConnectToSoma')

            # Pass options from UI to system
            ui_interface.options.morphology.connect_to_soma = scene.ConnectToSoma

        # Arbor quality option
        arbor_quality_row = layout.row()
        arbor_quality_row.label(text='Arbor Quality:')
        arbor_quality_row.prop(scene, 'ArborQuality')

        # Pass options from UI to system
        ui_interface.options.morphology.bevel_object_sides = scene.ArborQuality

        # Sections diameters option
        sections_radii_row = layout.row()
        sections_radii_row.prop(scene, 'SectionsRadii', icon='SURFACE_NCURVE')

        # Radii as specified in the morphology file
        if scene.SectionsRadii == enumerators.__sections__radii__as_specified__:

            # Pass options from UI to system
            ui_interface.options.morphology.scale_sections_radii = False
            ui_interface.options.morphology.unify_sections_radii = False
            ui_interface.options.morphology.sections_radii_scale = 1.0

        # Fixed diameter
        if scene.SectionsRadii == enumerators.__sections__radii__at_fixed_scale__:

            fixed_diameter_row = layout.row()
            fixed_diameter_row.label(text='Fixed Radius Value:')
            fixed_diameter_row.prop(scene, 'FixedRadiusValue')

            # Pass options from UI to system
            ui_interface.options.morphology.scale_sections_radii = False
            ui_interface.options.morphology.unify_sections_radii = True
            ui_interface.options.morphology.sections_fixed_radii_value = scene.FixedRadiusValue

        # Scaled diameter
        if scene.SectionsRadii == enumerators.__sections__radii__with_scale_factor__:

            scaled_diameter_row = layout.row()
            scaled_diameter_row.label(text='Radius Scale Factor:')
            scaled_diameter_row.prop(scene, 'RadiusScaleValue')

            # Pass options from UI to system
            ui_interface.options.morphology.unify_sections_radii = False
            ui_interface.options.morphology.scale_sections_radii = True
            ui_interface.options.morphology.sections_radii_scale = scene.RadiusScaleValue

        # Color parameters
        arbors_colors_row = layout.row()
        arbors_colors_row.label(text='Morphology Colors:', icon='COLOR')

        # Morphology material
        morphology_material_row = layout.row()
        morphology_material_row.prop(scene, 'MorphologyMaterial')

        # Pass options from UI to system
        ui_interface.options.morphology.material = scene.MorphologyMaterial

        color_by_part_row = layout.row()
        color_by_part_row.prop(scene, 'ColorArborByPart')
        color_bw_row = color_by_part_row.column()
        color_bw_row.prop(scene, 'ColorArborBlackAndWhite')
        color_bw_row.enabled = False

        # Soma color option
        soma_color_row = layout.row()
        soma_color_row.prop(scene, 'SomaColor')
        if not scene.BuildSoma:
            soma_color_row.enabled = False

        # Pass options from UI to system
        soma_color_value = Vector((scene.SomaColor.r, scene.SomaColor.g, scene.SomaColor.b))
        ui_interface.options.morphology.soma_color = soma_color_value

        # Axon color option
        axon_color_row = layout.row()
        axon_color_row.prop(scene, 'AxonColor')
        if not scene.BuildAxon or scene.ColorArborByPart:
            axon_color_row.enabled = False

        # Pass options from UI to system
        axon_color_value = Vector((scene.AxonColor.r, scene.AxonColor.g, scene.AxonColor.b))
        ui_interface.options.morphology.axon_color = axon_color_value

        # Basal dendrites color option
        basal_dendrites_color_row = layout.row()
        basal_dendrites_color_row.prop(scene, 'BasalDendritesColor')
        if not scene.BuildBasalDendrites or scene.ColorArborByPart:
            basal_dendrites_color_row.enabled = False

        # Pass options from UI to system
        color = scene.BasalDendritesColor
        basal_dendrites_color_value = Vector((color.r, color.g, color.b))
        ui_interface.options.morphology.basal_dendrites_color = basal_dendrites_color_value

        # Apical dendrite color option
        apical_dendrites_color_row = layout.row()
        apical_dendrites_color_row.prop(scene, 'ApicalDendriteColor')
        if not scene.BuildApicalDendrite or scene.ColorArborByPart:
            apical_dendrites_color_row.enabled = False

        # Pass options from UI to system
        color = scene.ApicalDendriteColor
        apical_dendrites_color_value = Vector((color.r, color.g, color.b))
        ui_interface.options.morphology.apical_dendrites_color = apical_dendrites_color_value

        # Articulation color option
        if scene.MorphologyReconstructionTechnique == enumerators.__method_articulated_sections__:
            articulation_color_row = layout.row()
            articulation_color_row.prop(scene, 'ArticulationColor')

            # Pass options from UI to system
            color = scene.ArticulationColor
            articulation_color_value = Vector((color.r, color.g, color.b))
            ui_interface.options.morphology.articulation_color = articulation_color_value

        if scene.ColorArborByPart:
            ui_interface.options.morphology.axon_color = Vector((-1, 0, 0))
            ui_interface.options.morphology.basal_dendrites_color = Vector((-1, 0, 0))
            ui_interface.options.morphology.apical_dendrites_color = Vector((-1, 0, 0))
            color_bw_row.enabled = True

            if scene.ColorArborBlackAndWhite:
                ui_interface.options.morphology.axon_color = Vector((0, -1, 0))
                ui_interface.options.morphology.basal_dendrites_color = Vector((0, -1, 0))
                ui_interface.options.morphology.apical_dendrites_color = Vector((0, -1, 0))

        # Morphology quick reconstruction options
        quick_reconstruction_row = layout.row()
        quick_reconstruction_row.label(text='Quick Reconstruction:', icon='PARTICLE_POINT')

        # Morphology reconstruction button
        reconstruct_morphology_button_row = layout.row()
        reconstruct_morphology_button_row.operator('reconstruct.morphology', icon='RNA_ADD')
        if scene.InputSource == 'h5_swc_file' or scene.InputSource == 'circuit_gid':
            reconstruct_morphology_button_row.enabled = True
        else:
            reconstruct_morphology_button_row.enabled = False

        # Quick rendering options
        quick_rendering_row = layout.row()
        quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')

        # Rendering type
        rendering_type_row = layout.row()
        rendering_type_row.prop(scene, 'RenderingType', expand=True)

        # Add the rendering extent for the full view or to-scale rendering modes
        if scene.RenderingType == enumerators.__rendering_full_view__ or \
                        scene.RenderingType == enumerators.__rendering_to_scale__:

            # Rendering extent
            rendering_extent_row = layout.row()
            rendering_extent_row.prop(scene, 'RenderingExtent', expand=True)

        if scene.RenderingType == enumerators.__rendering_full_view__ or \
           scene.RenderingType == enumerators.__rendering_close_up__:

            # Frame resolution option
            frame_resolution_row = layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(scene, 'MorphologyFrameResolution')
            frame_resolution_row.enabled = True

        if scene.RenderingType == enumerators.__rendering_to_scale__:

            # Scale factor option
            scale_factor_row = layout.row()
            scale_factor_row.label(text='Resolution Scale:')
            scale_factor_row.prop(scene, 'MorphologyFrameScaleFactor')
            scale_factor_row.enabled = True

        if scene.RenderingType == enumerators.__rendering_close_up__:

            # Render close up option
            render_close_up_row = layout.row()
            render_close_up_row.prop(scene, 'MorphologyCloseUpDimensions')

        # Render view buttons
        render_view_row = layout.row()
        render_view_row.label(text='Render View:', icon='RESTRICT_RENDER_OFF')
        render_view_buttons_row = layout.row(align=True)
        render_view_buttons_row.operator('render_morphology.front', icon='AXIS_FRONT')
        render_view_buttons_row.operator('render_morphology.side', icon='AXIS_SIDE')
        render_view_buttons_row.operator('render_morphology.top', icon='AXIS_TOP')
        render_view_buttons_row.enabled = True

        # Render animations buttons
        render_animation_row = layout.row()
        render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
        render_animations_buttons_row = layout.row(align=True)
        render_animations_buttons_row.operator('render_morphology.360', icon='FORCE_MAGNETIC')
        render_animations_buttons_row.operator('render_morphology.progressive', icon='FORCE_HARMONIC')
        render_animations_buttons_row.enabled = True

        # Saving morphology options
        save_morphology_row = layout.row()
        save_morphology_row.label(text='Save Morphology As:', icon='MESH_UVSPHERE')

        # Saving morphology buttons
        save_morphology_buttons_column = layout.column(align=True)
        save_morphology_buttons_column.operator('save_morphology.blend', icon='OUTLINER_OB_META')
        save_morphology_buttons_column.enabled = True


####################################################################################################
# ReconstructMorphologyOperator
####################################################################################################
class ReconstructMorphologyOperator(bpy.types.Operator):
    """Morphology reconstruction operator"""

    # Operator parameters
    bl_idname = "reconstruct.morphology"
    bl_label = "Reconstruct Morphology"

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
    # @load_morphology
    ################################################################################################
    def execute(self,
                context):
        """
        Execute the operator.

        :param context: Context.
        :return: 'FINISHED'
        """

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # Load the morphology
        self.load_morphology(scene=context.scene)

        # Create a skeletonizer object to build the morphology skeleton
        morphology_skeleton_builder = skeleton_builder.SkeletonBuilder(
            ui_interface.morphology, ui_interface.options)

        # Draw the morphology skeleton
        morphology_skeleton_objects = morphology_skeleton_builder.draw_morphology_skeleton()

        # Update the global reference
        global reconstructed_morphology_objects
        reconstructed_morphology_objects = morphology_skeleton_objects

        # Draw the bounding box of the morphology
        # if scene.DrawBoundingBox:
        #    bounding_box.draw_bounding_box(globals.objects.loaded_morphology_object.bounding_box,
        #                                   name='morphology_bounding_box')


        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphologyFront
####################################################################################################
class RenderMorphologyFront(bpy.types.Operator):
    """Render front view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "render_morphology.front"
    bl_label = "Front"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
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
        self.report({'INFO'}, 'Morphology Rendering ... Wait')

        # Render a full view
        if scene.RenderingType == enumerators.__rendering_full_view__:
            rendering_ops.render_full_view(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_morphology' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MorphologyFrameResolution,
                camera_view='FRONT')

        if scene.RenderingType == enumerators.__rendering_to_scale__:
            rendering_ops.render_full_view_to_scale(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_morphology_to_scale' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_scale_factor=scene.MorphologyFrameScaleFactor,
                camera_view='FRONT')

        # Render a close up of the morphology
        if scene.RenderingType == enumerators.__rendering_close_up__:
            rendering_ops.render_close_up(
                image_name='%s_morphology' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MorphologyFrameResolution,
                camera_view='FRONT',
                close_up_dimension=scene.MorphologyCloseUpDimensions)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Rendering Morphology Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphologySide
####################################################################################################
class RenderMorphologySide(bpy.types.Operator):
    """Render side view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "render_morphology.side"
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
        self.report({'INFO'}, 'Morphology Rendering ... Wait')

        # Render a full view
        if scene.RenderingType == enumerators.__rendering_full_view__:
            rendering_ops.render_full_view(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_morphology' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MorphologyFrameResolution,
                camera_view='SIDE')

        if scene.RenderingType == enumerators.__rendering_to_scale__:
            rendering_ops.render_full_view_to_scale(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_morphology_to_scale' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_scale_factor=scene.MorphologyFrameScaleFactor,
                camera_view='SIDE')

        # Render a close up of the morphology
        if scene.RenderingType == enumerators.__rendering_close_up__:
            rendering_ops.render_close_up(
                image_name='%s_morphology' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MorphologyFrameResolution,
                camera_view='SIDE',
                close_up_dimension=scene.MorphologyCloseUpDimensions)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Rendering Morphology Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphologyTop
####################################################################################################
class RenderMorphologyTop(bpy.types.Operator):
    """Render top view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "render_morphology.top"
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
        self.report({'INFO'}, 'Morphology Rendering ... Wait')

        # Render a full view
        if scene.RenderingType == enumerators.__rendering_full_view__:
            rendering_ops.render_full_view(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_morphology' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MorphologyFrameResolution,
                camera_view='TOP')

        if scene.RenderingType == enumerators.__rendering_to_scale__:
            rendering_ops.render_full_view_to_scale(
                view_bounding_box=ui_interface.morphology.bounding_box,
                image_name='%s_morphology_to_scale' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_scale_factor=scene.MorphologyFrameScaleFactor,
                camera_view='TOP')

        # Render a close up of the morphology
        if scene.RenderingType == enumerators.__rendering_close_up__:
            rendering_ops.render_close_up(
                image_name='%s_morphology' % ui_interface.options.morphology.label,
                image_output_directory=ui_interface.options.output.images_directory,
                image_base_resolution=scene.MorphologyFrameResolution,
                camera_view='TOP',
                close_up_dimension=scene.MorphologyCloseUpDimensions)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Rendering Morphology Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @RenderMorphology360
####################################################################################################
class RenderMorphology360(bpy.types.Operator):
    """Render a 360 view of the reconstructed morphology"""

    # Operator parameters
    bl_idname = "render_morphology.360"
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
            global reconstructed_morphology_objects
            rendering_ops.render_frame_at_angle(
                scene_objects=reconstructed_morphology_objects,
                camera=self.camera_360,
                angle=self.timer_limits,
                frame_name=frame_name)

            # Update the progress shell
            time_line.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            context.scene.SomaRenderingProgress = int(100 * self.timer_limits / 360.0)

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
        self.camera_360 = camera_ops.create_camera(
            view_bounding_box=bounding_box_360,
            image_base_resolution=scene.MorphologyFrameResolution)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_morphology_360' % (
            ui_interface.options.output.sequences_directory,
            ui_interface.options.morphology.label)
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
# @RenderMorphologyProgressive
####################################################################################################
class RenderMorphologyProgressive(bpy.types.Operator):
    """Render a progressive sequence of the reconstruction procedure (time-consuming)"""

    # Operator parameters
    bl_idname = "render_morphology.progressive"
    bl_label = "Progressive"

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

        # Create the sequences directory if it does not exist
        if not file_ops.path_exists(ui_interface.options.output.sequences_directory):
            file_ops.clean_and_create_directory(ui_interface.options.output.sequences_directory)

        # Clear the scene
        nmv.scene.ops.clear_scene()

        # NOTE: To render a progressive reconstruction sequence, this requires setting the
        # morphology progressive rendering flag to True and then passing the ui_interface.options
        # to the morphology builder and disabling it after the rendering
        ui_interface.options.morphology.render_progressive = True

        # Create a skeleton builder object
        morphology_builder = skeleton_builder.SkeletonBuilder(
            ui_interface.morphology, ui_interface.options)

        # Reconstruct the morphology
        morphology_skeleton_objects = morphology_builder.draw_morphology_skeleton()

        # Setting the progressive rendering flag to False (default value)
        ui_interface.options.morphology.render_progressive = False

        # Report the process termination in the UI
        self.report({'INFO'}, 'Morphology Rendering Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @SaveSomaMeshBlend
####################################################################################################
class SaveMorphologyBLEND(bpy.types.Operator):
    """Save the reconstructed morphology in a blender file"""

    # Operator parameters
    bl_idname = "save_morphology.blend"
    bl_label = "Blender Format (.blend)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
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

        # Export the reconstructed morphology as an .blend file
        # NOTE: Since we don't have meshes, then the mesh_object argument will be set to None and
        # the exported blender file will contain all the morphology objects.
        exporters.export_object_to_blend_file(mesh_object=None,
            output_directory=ui_interface.options.output.meshes_directory,
            output_file_name=ui_interface.morphology.label)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Soma reconstruction panel
    bpy.utils.register_class(MorphologyOptions)

    # Soma reconstruction operator
    bpy.utils.register_class(ReconstructMorphologyOperator)

    # Morphology rendering
    bpy.utils.register_class(RenderMorphologyFront)
    bpy.utils.register_class(RenderMorphologySide)
    bpy.utils.register_class(RenderMorphologyTop)
    bpy.utils.register_class(RenderMorphology360)
    bpy.utils.register_class(RenderMorphologyProgressive)

    # Saving morphology
    bpy.utils.register_class(SaveMorphologyBLEND)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Morphology reconstruction panel
    bpy.utils.unregister_class(MorphologyOptions)

    # Morphology reconstruction operator
    bpy.utils.unregister_class(ReconstructMorphologyOperator)

    # Morphology rendering
    bpy.utils.unregister_class(RenderMorphologyTop)
    bpy.utils.unregister_class(RenderMorphologySide)
    bpy.utils.unregister_class(RenderMorphologyFront)
    bpy.utils.unregister_class(RenderMorphology360)
    bpy.utils.unregister_class(RenderMorphologyProgressive)

    # Saving morphology
    bpy.utils.unregister_class(SaveMorphologyBLEND)
