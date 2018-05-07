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

# Blender imports
import bpy
from mathutils import Vector
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import FloatVectorProperty

import neuromorphovis as nmv


####################################################################################################
# @NeuroRender
####################################################################################################
class NeuroRender(bpy.types.Panel):
    """NeuroRender panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'NeuroRender'
    bl_context = 'objectmode'
    bl_category = 'NeuroRender'

    # Number of samples per section
    bpy.types.Scene.AnalyzeNumberSamplesPerSection = BoolProperty(
        name="# Samples / Section",
        description="Analyze the number of samples per section",
        default=True)

    # Number of segments per section
    bpy.types.Scene.AnalyzeNumberSegmentsPerSection = BoolProperty(
        name="# Segments / Section",
        description="Analyze the number of segments per section",
        default=True)

    # Number of sections per arbor
    bpy.types.Scene.AnalyzeNumberSectionsPerArbor = BoolProperty(
        name="# Sections / Arbor",
        description="Analyze the number of sections per arbor",
        default=True)

    # Branching angles
    bpy.types.Scene.AnalyzeNumberChildrenPerSection = BoolProperty(
        name="# Children / Section",
        description="Analyze the number of children per section", default=True)

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

    # Sections lengths
    bpy.types.Scene.AnalyzeSectionsLength = BoolProperty(
        name="Sections Length",
        description="Analyze the distribution of the lengths of the sections",
        default=True)

    # Sections radii
    bpy.types.Scene.AnalyzeSectionsRadii = BoolProperty(
        name="Sections Radii",
        description="Analyze the distribution of the radii of the samples along the sections",
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
    def draw(self,
             context):
        """Draw the panel

        :param context:
            Rendering context
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Number of samples per section
        number_samples_per_section_row = layout.row()
        number_samples_per_section_row.prop(context.scene, 'AnalyzeNumberSamplesPerSection')

        # Number of segments per section
        number_segments_per_section_row = layout.row()
        number_segments_per_section_row.prop(context.scene, 'AnalyzeNumberSegmentsPerSection')

        # Number of sections per arbor
        number_sections_per_arbor_row = layout.row()
        number_sections_per_arbor_row.prop(context.scene, 'AnalyzeNumberSectionsPerArbor')

        # Branching angles
        branching_angles_row = layout.row()
        branching_angles_row.prop(context.scene, 'AnalyzeBranchingAngles')

        # Branching radii
        branching_radii_row = layout.row()
        branching_radii_row.prop(context.scene, 'AnalyzeBranchingRadii')

        # Sections lengths
        sections_length_row = layout.row()
        sections_length_row.prop(context.scene, 'AnalyzeSectionsLength')

        # Sections radii
        sections_radii_row = layout.row()
        sections_radii_row.prop(context.scene, 'AnalyzeSectionsRadii')

        # Short sections
        short_sections_row = layout.row()
        short_sections_row.prop(context.scene, 'AnalyzeShortSections')

        # Duplicate samples
        duplicate_samples_row = layout.row()
        duplicate_samples_row.prop(context.scene, 'AnalyzeDuplicateSamples')

        # Disconnected axons
        disconnected_axons_row = layout.row()
        disconnected_axons_row.prop(context.scene, 'AnalyzeDisconnectedAxons')

        # Branches with negative samples
        negative_samples_row = layout.row()
        negative_samples_row.prop(context.scene, 'AnalyzeBranchesWithNegativeSamples')

        # Morphology analysis button
        analyze_morphology_column = layout.column(align=True)
        analyze_morphology_column.operator('analyze.morphology', icon='MESH_DATA')



####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """
    Registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.register_class(NeuroRender)

    # Morphology analysis button
    #bpy.utils.register_class(AnalyzeMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """
    Un-registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.unregister_class(NeuroRender)

    # Morphology analysis button
    #bpy.utils.unregister_class(AnalyzeMorphology)
