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
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.file
import neuromorphovis.interface
import neuromorphovis.skeleton





class Feature:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 variable,
                 name,
                 type='Float',
                 unit='NONE'):
        """Constructor

        :param variable:
            Feature variable name.
        :param name:
            Feature name.
        :param unit:
            Feature unit.
        """

        self.variable = variable
        self.name = name
        self.type = type
        self.unit = unit



morphology_features_list = [
    Feature(variable='MorphologyNeuritesLength', name='Neurites Length', unit='LENGTH'),
    Feature(variable='MorphologyNeuritesSurfaceArea', name='Neurites Surface Area', unit='AREA'),
    Feature(variable='MorphologyNeuritesVolume', name='Neurites Volume', unit='VOLUME'),

]

neurite_features_list = [
    Feature(variable='TotalLength', name='Total Length', unit='NONE'),
    Feature(variable='Length', name='Length', unit='LENGTH'),
    Feature(variable='AvgLengthPerSection', name='Avg. Length / Section', unit='LENGTH'),
    Feature(variable='AvgLengthPerSegment', name='Avg. Length / Segment', unit='LENGTH'),
    Feature(variable='SurfaceArea', name='Surface Area', unit='AREA'),
    Feature(variable='AvgSurfaceAreaPerSection', name='Avg. Surface Area / Section', unit='AREA'),
    Feature(variable='AvgSurfaceAreaPerSegment', name='Avg. Surface Area / Segment', unit='AREA'),
    Feature(variable='Volume', name='Volume', unit='VOLUME'),
    Feature(variable='AvgVolumePerSection', name='Avg. Volume / Section', unit='VOLUME'),
    Feature(variable='AvgVolumePerSegment', name='Avg. Volume / Segment', unit='VOLUME'),
    Feature(variable='NumberBifurcations', name='# Bifurcations', type='Int'),
    Feature(variable='NumberTrifurcations', name='# Trifurcations', type='Int'),
    Feature(variable='NumberSections', name='# Sections', type='Int'),
    Feature(variable='NumberSections', name='# Segments', type='Int'),
]



soma_features_list = [
    Feature(variable='SomaMinRadius', name='Min. Radius', unit='LENGTH'),
    Feature(variable='SomaMaxRadius', name='Max. Radius', unit='LENGTH'),
    Feature(variable='SomaAvgRadius', name='Avg. Radius', unit='LENGTH'),
    Feature(variable='SomaSurfaceArea', name='Surface Area', unit='AREA'),
    Feature(variable='SomaVolume', name='Volume', unit='VOLUME')

]






####################################################################################################
# @AnalysisPanel
####################################################################################################
class AnalysisPanel(bpy.types.Panel):
    """Analysis panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Morphology Analysis'
    bl_context = 'objectmode'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

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

    # Sections volumes
    bpy.types.Scene.SectionsVolumes = BoolProperty(
        name="Sections Volumes",
        description="Compute the distribution of sections volumes",
        default=True)

    # Segments volumes
    bpy.types.Scene.SegmentsVolumes = BoolProperty(
        name="Segments Volumes",
        description="Compute the distribution of sections volumes",
        default=True)

    # Sections surface areas
    bpy.types.Scene.SectionsSurfaceAreas = BoolProperty(
        name="Sections Surface Areas",
        description="Compute the distribution of sections volumes",
        default=True)

    # Segments surface areas
    bpy.types.Scene.SegmentsSurfaceAreas = BoolProperty(
        name="Segments Surface Areas",
        description="Compute the distribution of sections volumes",
        default=True)

    # Duplicate samples
    bpy.types.Scene.AnalyzeDuplicateSamples = BoolProperty(
        name="Duplicate Samples",
        description="Detect the duplicate samples that are extremely close along the section",
        default=True)

    # Disconnected axons from soma
    bpy.types.Scene.AnalyzeDisconnectedAxons = BoolProperty(
        name="Disconnected Axons",
        description="De[tect when the axon is disconnected from the soma",
        default=True)

    # Branches with negative samples
    bpy.types.Scene.AnalyzeBranchesWithNegativeSamples = BoolProperty(
        name="Branches With Negative Samples",
        description="Detect when the section is intersecting with the soma",
        default=True)

    for neurite in ['Axon', 'ApicalDendrite', 'BasalDendrite0']:
        for feature in neurite_features_list:
            if feature.type == 'Int':
                setattr(bpy.types.Scene, '%s%s' % (neurite, feature.variable),
                        IntProperty(name=feature.name, min=0, max=1))
            elif feature.type == 'Float':
                setattr(bpy.types.Scene, '%s%s' % (neurite, feature.variable),
                        FloatProperty(name=feature.name,
                                      min=-1e10, max=1e10, unit=feature.unit))
            else:
                pass


    #bpy.types.Scene.AxonTotalLength = \
    #    FloatProperty(name="", min=-1e10, max=1e10, subtype='NONE', options={'ANIMATABLE'})

    #FloatProperty(name="", min=-1e10, max=1e10, subtype='FACTOR', options={'ANIMATABLE'})

    # bpy.types.Scene.BBoxPMinX = FloatProperty(name="X", min=-1e10, max=1e10, subtype='FACTOR')







    file_path = StringProperty(name="File", subtype="FILE_PATH")

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




        # Segments surface area
        segments_surface_area_row = layout.row()
        segments_surface_area_row.prop(context.scene, 'SegmentsSurfaceAreas')

        # Sections surface area
        sections_surface_area_row = layout.row()
        sections_surface_area_row.prop(context.scene, 'SectionsSurfaceAreas')

        # Segments volumes
        segments_volume_row = layout.row()
        segments_volume_row.prop(context.scene, 'SegmentsVolumes')

        # Sections volumes
        sections_volume_row = layout.row()
        sections_volume_row.prop(context.scene, 'SectionsVolumes')

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

        box = layout.box()
        row = box.column()

        bounding_box_p_row = layout.row()
        bounding_box_p_min_row = bounding_box_p_row.column(align=True)
        bounding_box_p_min_row.label(text='Axon:')
        for feature in neurite_features_list:
            bounding_box_p_min_row.prop(context.scene, 'Axon%s' % feature.variable)
        bounding_box_p_min_row.enabled = False

        bounding_box_p_row = layout.row()
        bounding_box_p_min_row = bounding_box_p_row.column(align=True)
        bounding_box_p_min_row.label(text='Apical Dendrite:')
        for feature in neurite_features_list:
            bounding_box_p_min_row.prop(context.scene, 'ApicalDendrite%s' % feature.variable)
        bounding_box_p_min_row.enabled = False

        """
        
        axon_column = layout.box()
        axon_column.prop(context.scene, 'AnalyzeBranchesWithNegativeSamples')
        x_row = axon_column.row(align=True)
        x_row.label(text='Total Length')
        x_row.prop(context.scene, 'AxonTotalLength')
        axon_column.prop(context.scene, 'AxonTotalLength')
        axon_column.prop(context.scene, 'AxonTotalLength')
        # axon_column.enabled = False

        row = layout.row()
        row.label(text='Total Length')
        row.prop(context.scene, 'AxonTotalLength')
        """

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
        """Execute the operator.

        :param context:
            Rendering context
        :return:
            'FINISHED'
        """

        # context.scene.A = 25.4

        # Ensure that there is a valid directory where the images will be written to
        if nmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        nmv.logger.log(context.scene.OutputDirectory)
        if not nmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the analysis directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.analysis_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.analysis_directory)

        # Load the morphology file
        nmv.interface.ui.load_morphology(self, context.scene)

        # All set of filter we support
        analysis_filters = [
            [context.scene.AnalyzeNumberSamplesPerSection,
             nmv.skeleton.ops.analyze_number_of_samples_per_section,
             'NUMBER_SAMPLES_PER_SECTION'],
            [context.scene.AnalyzeNumberSegmentsPerSection,
             nmv.skeleton.ops.analyze_number_of_segments_per_section,
             'NUMBER_SEGMENTS_PER_SECTION'],
            [context.scene.AnalyzeNumberChildrenPerSection,
             nmv.skeleton.ops.analyze_number_of_children_per_section,
             'NUMBER_CHILDREN_PER_SECTION'],
            [context.scene.AnalyzeBranchingAngles,
             nmv.skeleton.ops.analyze_branching_angles_per_section,
             'BRANCHING_ANGLES'],
            [context.scene.AnalyzeBranchingRadii,
             nmv.skeleton.ops.analyze_branching_radii_per_section,
             'BRANCHING_RADII'],
            [context.scene.AnalyzeSectionsLength,
             nmv.skeleton.ops.analyze_section_length,
             'SECTIONS_LENGTH'],
            [context.scene.AnalyzeShortSections,
             nmv.skeleton.ops.analyze_short_sections,
             'SHORT_SECTIONS'],
            [context.scene.AnalyzeSectionsRadii,
             nmv.skeleton.ops.analyze_section_radii,
             'SECTIONS_RADII']
        ]

        # Apply the analysis filters
        for analysis_filter in analysis_filters:

            # UI flag
            filter_flag = analysis_filter[0]

            # Filter function
            filter_function = analysis_filter[1]

            # Filter prefix
            filter_prefix = analysis_filter[2]

            # If the filter flag is set, apply the filter on the morphology
            if filter_flag:

                # Create a list to collect the analysis data
                analysis_data = list()

                # Analyze the morphology
                nmv.skeleton.ops.apply_operation_to_morphology(
                    *[nmv.interface.ui_morphology,
                      filter_function,
                      analysis_data])

                # Write the analysis report
                report_file = '%s/%s_%s.analysis' % (nmv.interface.ui_options.io.analysis_directory,
                                                     nmv.interface.ui_morphology.label,
                                                     filter_prefix)
                nmv.file.write_list_string_to_file(analysis_data, report_file)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.register_class(AnalysisPanel)

    # Morphology analysis button
    bpy.utils.register_class(AnalyzeMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.unregister_class(AnalysisPanel)

    # Morphology analysis button
    bpy.utils.unregister_class(AnalyzeMorphology)
