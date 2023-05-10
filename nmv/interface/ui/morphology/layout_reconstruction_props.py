####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# Internal imports
import nmv.consts
import nmv.enums
import nmv.bbp
import nmv.scene


####################################################################################################
# @draw_morphology_reconstruction_header
####################################################################################################
def draw_morphology_reconstruction_header(layout):

    row = layout.row()
    row.label(text='Reconstruction Options', icon='OUTLINER_OB_EMPTY')


####################################################################################################
# @draw_morphology_reconstruction_technique_option
####################################################################################################
def draw_morphology_reconstruction_technique_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_MorphologyReconstructionTechnique', icon='FORCE_CURVE')
    options.morphology.reconstruction_method = scene.NMV_MorphologyReconstructionTechnique


####################################################################################################
# @draw_arbor_style_option
####################################################################################################
def draw_arbor_style_option(layout, scene, options):

    row = layout.row()
    row.label(text='Arbor Style')
    row.prop(scene, 'NMV_ArborsStyle', icon='WPAINT_HLT')
    options.morphology.arbor_style = scene.NMV_ArborsStyle


####################################################################################################
# @draw_branching_option
####################################################################################################
def draw_branching_option(layout, scene, options):

    row = layout.row()
    row.label(text='Branching')
    row.prop(scene, 'NMV_MorphologyBranching', expand=True)
    options.morphology.branching = scene.NMV_MorphologyBranching


####################################################################################################
# @draw_arbor_to_soma_connection_option
####################################################################################################
def draw_arbor_to_soma_connection_option(layout, scene, options):

    row = layout.row()
    row.label(text='Arbors to Soma Connection')
    row.prop(scene, 'NMV_SomaConnectionToRoot')
    options.morphology.arbors_to_soma_connection = scene.NMV_SomaConnectionToRoot


####################################################################################################
# @draw_dendrogram_type_option
####################################################################################################
def draw_dendrogram_type_option(layout, scene, options):

    row = layout.row()
    row.label(text='Dendrogram Type')
    row.prop(scene, 'NMV_DendrogramType', expand=True)
    options.morphology.dendrogram_type = scene.NMV_DendrogramType


####################################################################################################
# @draw_arbors_radii_option
####################################################################################################
def draw_arbors_radii_option(layout, scene, options):

    row = layout.row()
    row.label(text='Arbors Radii:')
    row.prop(scene, 'NMV_SectionsRadii', icon='SURFACE_NCURVE')
    options.morphology.arbors_radii = scene.NMV_SectionsRadii


####################################################################################################
# @draw_original_arbors_radii_option
####################################################################################################
def draw_original_arbors_radii_option(layout, scene, options):

    options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.ORIGINAL
    options.morphology.scale_sections_radii = False
    options.morphology.unify_sections_radii = False
    options.morphology.sections_radii_scale = 1.0


####################################################################################################
# @draw_unified_radii_option
####################################################################################################
def draw_unified_radii_option(layout, scene, options):

    row = layout.row()
    row.label(text='Fixed Radius Value:')
    row.prop(scene, 'NMV_UnifiedRadiusValue')

    options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.UNIFIED
    options.morphology.scale_sections_radii = False
    options.morphology.unify_sections_radii = True
    options.morphology.samples_unified_radii_value = scene.NMV_UnifiedRadiusValue


####################################################################################################
# @draw_unified_radii_per_arbor_option
####################################################################################################
def draw_unified_radii_per_arbor_option(layout, scene, options, morphology):

    options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.UNIFIED_PER_ARBOR_TYPE
    options.morphology.scale_sections_radii = False
    options.morphology.unify_sections_radii = True

    if morphology.has_axons():
        axons_row = layout.row()
        axons_row.label(text='Axons Radius:')
        axons_row.prop(scene, 'NMV_AxonUnifiedRadiusValue')
        options.morphology.axon_samples_unified_radii_value = scene.NMV_AxonUnifiedRadiusValue

    if morphology.has_apical_dendrites():
        apicals_row = layout.row()
        apicals_row.label(text='Apical Dendrites Radius:')
        apicals_row.prop(scene, 'NMV_ApicalDendriteUnifiedRadiusValue')
        options.morphology.apical_dendrite_samples_unified_radii_value = \
            scene.NMV_ApicalDendriteUnifiedRadiusValue

    if morphology.has_basal_dendrites():
        basals_row = layout.row()
        basals_row.label(text='Basal Dendrites Radius:')
        basals_row.prop(scene, 'NMV_BasalDendritesUnifiedRadiusValue')
        options.morphology.basal_dendrites_samples_unified_radii_value = \
            scene.NMV_BasalDendritesUnifiedRadiusValue


####################################################################################################
# @draw_scaled_radii_option
####################################################################################################
def draw_scaled_radii_option(layout, scene, options):

    row = layout.row()
    row.label(text='Radius Scale Factor:')
    row.prop(scene, 'NMV_RadiusScaleValue')

    # Affirm
    options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.SCALED
    options.morphology.unify_sections_radii = False
    options.morphology.scale_sections_radii = True
    options.morphology.sections_radii_scale = scene.NMV_RadiusScaleValue


####################################################################################################
# @draw_filtered_radii_option
####################################################################################################
def draw_filtered_radii_option(layout, scene, options):

    minimum_row = layout.row()
    minimum_row.label(text='Minimum Radius:')
    minimum_row.prop(scene, 'NMV_MinimumRadiusThreshold')

    maximum_row = layout.row()
    maximum_row.label(text='Maximum Radius:')
    maximum_row.prop(scene, 'NMV_MaximumRadiusThreshold')

    # Affirm
    options.morphology.unify_sections_radii = False
    options.morphology.scale_sections_radii = False
    options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.FILTERED
    options.morphology.minimum_threshold_radius = scene.NMV_MinimumRadiusThreshold
    options.morphology.maximum_threshold_radius = scene.NMV_MaximumRadiusThreshold


####################################################################################################
# @draw_arbors_radii_options
####################################################################################################
def draw_arbors_radii_options(layout, scene, options, morphology):

    draw_arbors_radii_option(layout=layout, scene=scene, options=options)
    if options.morphology.arbors_radii == nmv.enums.Skeleton.Radii.ORIGINAL:
        draw_original_arbors_radii_option(layout=layout, scene=scene, options=options)

    elif options.morphology.arbors_radii == nmv.enums.Skeleton.Radii.UNIFIED:
        draw_unified_radii_option(layout=layout, scene=scene, options=options)

    elif options.morphology.arbors_radii == nmv.enums.Skeleton.Radii.UNIFIED_PER_ARBOR_TYPE:
        draw_unified_radii_per_arbor_option(
            layout=layout, scene=scene, options=options, morphology=morphology)

    elif options.morphology.arbors_radii == nmv.enums.Skeleton.Radii.SCALED:
        draw_scaled_radii_option(layout=layout, scene=scene, options=options)

    elif options.morphology.arbors_radii == nmv.enums.Skeleton.Radii.FILTERED:
        draw_filtered_radii_option(layout=layout, scene=scene, options=options)

    else:
        nmv.logger.log('UI_ERROR: draw_arbors_radii_options')


####################################################################################################
# @draw_arbor_quality_option
####################################################################################################
def draw_arbor_quality_option(layout, scene, options):

    row = layout.row()
    row.label(text='Arbor Quality:')
    row.prop(scene, 'NMV_ArborQuality')
    options.morphology.bevel_object_sides = scene.NMV_ArborQuality


####################################################################################################
# @draw_morphology_resampling_method_option
####################################################################################################
def draw_morphology_resampling_method_option(layout, scene, options):

    row = layout.row()
    row.label(text='Resampling')
    row.prop(scene, 'NMV_MorphologyResampling')
    options.morphology.resampling_method = scene.NMV_MorphologyResampling


####################################################################################################
# @draw_fixed_resampling_step_option
####################################################################################################
def draw_fixed_resampling_step_option(layout, scene, options):

    row = layout.row()
    row.label(text='Resampling Step')
    row.prop(scene, 'NMV_MorphologyResamplingStep')
    options.morphology.resampling_step = scene.NMV_MorphologyResamplingStep


####################################################################################################
# @draw_morphology_resampling_options
####################################################################################################
def draw_morphology_resampling_options(layout, scene, options):

    draw_morphology_resampling_method_option(layout=layout, scene=scene, options=options)
    if options.morphology.resampling_method == nmv.enums.Skeleton.Resampling.FIXED_STEP:
        draw_fixed_resampling_step_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_disconnected_segments_options
####################################################################################################
def draw_disconnected_segments_options(layout, scene, options, morphology):

    draw_morphology_resampling_options(layout=layout, scene=scene, options=options)
    draw_arbors_radii_options(layout=layout, scene=scene, options=options, morphology=morphology)
    draw_arbor_quality_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_disconnected_sections_options
####################################################################################################
def draw_disconnected_sections_options(layout, scene, options, morphology):

    draw_morphology_resampling_options(layout=layout, scene=scene, options=options)
    draw_arbors_radii_options(layout=layout, scene=scene, options=options, morphology=morphology)
    draw_arbor_quality_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_samples_options
####################################################################################################
def draw_samples_options(layout, scene, options, morphology):

    draw_morphology_resampling_options(layout=layout, scene=scene, options=options)
    draw_arbors_radii_options(layout=layout, scene=scene, options=options, morphology=morphology)


####################################################################################################
# @draw_progressive_options
####################################################################################################
def draw_progressive_options(layout, scene, options, morphology):

    draw_morphology_resampling_options(layout=layout, scene=scene, options=options)
    draw_arbors_radii_options(layout=layout, scene=scene, options=options, morphology=morphology)
    draw_arbor_quality_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_articulated_sections_options
####################################################################################################
def draw_articulated_sections_options(layout, scene, options, morphology):

    draw_morphology_resampling_options(layout=layout, scene=scene, options=options)
    draw_arbors_radii_options(layout=layout, scene=scene, options=options, morphology=morphology)
    draw_arbor_quality_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_connected_sections_options
####################################################################################################
def draw_connected_sections_options(layout, scene, options, morphology):

    draw_arbor_style_option(layout=layout, scene=scene, options=options)
    draw_branching_option(layout=layout, scene=scene, options=options)
    draw_arbor_to_soma_connection_option(layout=layout, scene=scene, options=options)
    draw_morphology_resampling_options(layout=layout, scene=scene, options=options)
    draw_arbors_radii_options(layout=layout, scene=scene, options=options, morphology=morphology)
    draw_arbor_quality_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_dendrogram_options
####################################################################################################
def draw_dendrogram_options(layout, scene, options):

    draw_dendrogram_type_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_morphology_reconstruction_options
####################################################################################################
def draw_morphology_reconstruction_options(layout, scene, options, morphology):

    draw_morphology_reconstruction_header(layout=layout)
    draw_morphology_reconstruction_technique_option(layout=layout, scene=scene, options=options)

    method = options.morphology.reconstruction_method
    if method == nmv.enums.Skeleton.Method.CONNECTED_SECTIONS:
        draw_connected_sections_options(
            layout=layout, scene=scene, options=options, morphology=morphology)

    elif method == nmv.enums.Skeleton.Method.DISCONNECTED_SECTIONS:
        draw_disconnected_sections_options(
            layout=layout, scene=scene, options=options, morphology=morphology)

    elif method == nmv.enums.Skeleton.Method.DISCONNECTED_SEGMENTS:
        draw_disconnected_segments_options(
            layout=layout, scene=scene, options=options, morphology=morphology)

    elif method == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
        draw_articulated_sections_options(
            layout=layout, scene=scene, options=options, morphology=morphology)

    elif method == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
        draw_articulated_sections_options(
            layout=layout, scene=scene, options=options, morphology=morphology)

    elif method == nmv.enums.Skeleton.Method.PROGRESSIVE:
        draw_progressive_options(
            layout=layout, scene=scene, options=options, morphology=morphology)

    elif method == nmv.enums.Skeleton.Method.SAMPLES:
        draw_samples_options(
            layout=layout, scene=scene, options=options, morphology=morphology)

    elif method == nmv.enums.Skeleton.Method.DENDROGRAM:
        draw_dendrogram_options(layout=layout, scene=scene, options=options)

    else:
        nmv.logger.log('UI_ERROR: draw_morphology_reconstruction_options')



