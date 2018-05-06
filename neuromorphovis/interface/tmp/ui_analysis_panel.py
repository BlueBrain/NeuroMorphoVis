"""ui_analysis_panel.py:
    Morphology analysis panel.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2017, Blue Brain Project / EPFL"
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# System imports
import sys, os

# Blender imports
import bpy
from mathutils import Vector
from bpy.props import (IntProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty,
                       FloatVectorProperty)

####################################################################################################
# @VolumeOptions
####################################################################################################
class AnalysisOptions(bpy.types.Panel):
    """Analysis options"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Morphology Analysis'
    bl_context = 'objectmode'
    bl_category = 'NeuroMorphoVis'

    # Number of samples per section
    bpy.types.Scene.AnalyzeNumberSamplesPerSection = BoolProperty(
        name="Samples Per Section",
        description="Analyze the distribution of number of samples per section",
        default=True)

    # Number of segments per section
    bpy.types.Scene.AnalyzeNumberSegmentsPerSection = BoolProperty(
        name="Segments Per Section",
        description="Analyze the distribution of number of segments per section",
        default=True)

    # Number of sections per arbor
    bpy.types.Scene.AnalyzeNumberSectionsPerArbor = BoolProperty(
        name="Sections Per Arbor",
        description="Analyze the distribution of number of sections per arbor",
        default=True)

    # Branching angles
    bpy.types.Scene.AnalyzeBranchingAngles = BoolProperty(
        name="Branching Angles",
        description="Analyze the distribution of the angles at the branching points",
        default=True)

    # Branching radii
    bpy.types.Scene.AnalyzeBranchingRadii = BoolProperty(
        name="Branching Radii",
        description="Analyze the distribution of the radii at the branching points",
        default=True)

    # Short sections
    bpy.types.Scene.AnalyzeShortSections = BoolProperty(
        name="Short Sections",
        description="Detect the number of short sections",
        default=True)

    # Duplicate samples
    bpy.types.Scene.AnalyzeDuplicateSamples = BoolProperty(
        name="Duplicate Samples",
        description="Detect the duplicate samples that are extremely close along the section",
        default=True)

    # Disconnected axons from soma
    bpy.types.Scene.AnalyzeDisconnectedAxons = BoolProperty(
        name="Disconnected Axons",
        description="Detect when the axon is disconnected from the soma",
        default=True)

    # Branches with negative samples
    bpy.types.Scene.AnalyzeBranchesWithNegativeSamples = BoolProperty(
        name="Branches With Negative Samples",
        description="Detect when the section is intersecting with the soma",
        default=True)

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """
        Draws the panel.

        :param context: Panel context.
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Get a reference to the scene
        scene = context.scene

        # Number of samples per section
        number_samples_per_section_row = layout.row()
        number_samples_per_section_row.prop(scene, 'AnalyzeNumberSamplesPerSection')

        # Number of segments per section
        number_segments_per_section_row = layout.row()
        number_segments_per_section_row.prop(scene, 'AnalyzeNumberSegmentsPerSection')

        # Number of sections per arbor
        number_sections_per_arbor_row = layout.row()
        number_sections_per_arbor_row.prop(scene, 'AnalyzeNumberSectionsPerArbor')

        # Branching angles
        branching_angles_row = layout.row()
        branching_angles_row.prop(scene, 'AnalyzeBranchingAngles')

        # Branching radii
        branching_radii_row = layout.row()
        branching_radii_row.prop(scene, 'AnalyzeBranchingRadii')

        # Short sections
        short_sections_row = layout.row()
        short_sections_row.prop(scene, 'AnalyzeShortSections')

        # Duplicate samples
        duplicate_samples_row = layout.row()
        duplicate_samples_row.prop(scene, 'AnalyzeDuplicateSamples')

        # Disconnected axons
        disconnected_axons_row = layout.row()
        disconnected_axons_row.prop(scene, 'AnalyzeDisconnectedAxons')

        # Branches with negative samples
        negative_samples_row = layout.row()
        negative_samples_row.prop(scene, 'AnalyzeBranchesWithNegativeSamples')

        # Morphology analysis button
        analyze_morphology_column = layout.column(align=True)
        analyze_morphology_column.operator('analyze.morphology', icon='MESH_DATA')


####################################################################################################
# @SaveSomaMeshBlend
####################################################################################################
class AnalyzeMorphology(bpy.types.Operator):
    """Analyze the morphology skeleton, detect the artifacts and report them"""

    # Operator parameters
    bl_idname = "analyze.morphology"
    bl_label = "Analyze Morphology"

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


        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """
    Registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.register_class(AnalysisOptions)

    # Morphology analysis button
    bpy.utils.register_class(AnalyzeMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """
    Un-registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.unregister_class(AnalysisOptions)

    # Morphology analysis button
    bpy.utils.unregister_class(AnalyzeMorphology)
