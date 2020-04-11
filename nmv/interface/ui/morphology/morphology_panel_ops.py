####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
from mathutils import Vector

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @set_skeleton_options
####################################################################################################
def set_skeleton_options(layout,
                         scene,
                         options):
    """Morphology skeleton options.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Morphology skeleton options
    skeleton_row = layout.row()
    skeleton_row.label(text='Morphology Skeleton:', icon='QUESTION')

    # Build soma options
    build_soma_row = layout.row()
    build_soma_row.label(text='Soma:')
    build_soma_row.prop(scene, 'NMV_BuildSoma')

    # Pass options from UI to system
    options.morphology.soma_representation = scene.NMV_BuildSoma

    # The morphology must be loaded to be able to draw these options
    if nmv.interface.ui_morphology is not None:

        # Build axon options
        if nmv.interface.ui_morphology.has_axons():
            axon_row = layout.row()
            axon_row.prop(scene, 'NMV_BuildAxon')
            axon_level_row = axon_row.column()
            axon_level_row.prop(scene, 'NMV_AxonBranchingLevel')

            if not scene.NMV_BuildAxon:
                axon_level_row.enabled = False
            else:
                axon_level_row.enabled = True

            # Pass options from UI to system
            options.morphology.ignore_axons = not scene.NMV_BuildAxon
            options.morphology.axon_branch_order = scene.NMV_AxonBranchingLevel

        # Build basal dendrites options
        if nmv.interface.ui_morphology.has_basal_dendrites():
            basal_dendrites_row = layout.row()
            basal_dendrites_row.prop(scene, 'NMV_BuildBasalDendrites')
            basal_dendrites_level_row = basal_dendrites_row.column()
            basal_dendrites_level_row.prop(scene, 'NMV_BasalDendritesBranchingLevel')
            if not scene.NMV_BuildBasalDendrites:
                basal_dendrites_level_row.enabled = False
            else:
                basal_dendrites_level_row.enabled = True

            # Pass options from UI to system
            options.morphology.ignore_basal_dendrites = not scene.NMV_BuildBasalDendrites
            options.morphology.basal_dendrites_branch_order = scene.NMV_BasalDendritesBranchingLevel

        # Build apical dendrite option
        if nmv.interface.ui_morphology.has_apical_dendrites():
            apical_dendrite_row = layout.row()
            apical_dendrite_row.prop(scene, 'NMV_BuildApicalDendrite')
            apical_dendrite_level_row = apical_dendrite_row.column()
            apical_dendrite_level_row.prop(scene, 'NMV_ApicalDendriteBranchingLevel')

            if not scene.NMV_BuildApicalDendrite:
                apical_dendrite_level_row.enabled = False
            else:
                apical_dendrite_level_row.enabled = True

            # Pass options from UI to system
            options.morphology.ignore_apical_dendrites = not scene.NMV_BuildApicalDendrite
            options.morphology.apical_dendrite_branch_order = scene.NMV_ApicalDendriteBranchingLevel

    # Only a simple demo UI
    else:

        # Axons
        axon_row = layout.row()
        axon_row.prop(scene, 'NMV_BuildAxon')
        axon_level_row = axon_row.column()
        axon_level_row.prop(scene, 'NMV_AxonBranchingLevel')

        # Basal dendrites
        basal_dendrites_row = layout.row()
        basal_dendrites_row.prop(scene, 'NMV_BuildBasalDendrites')
        basal_dendrites_level_row = basal_dendrites_row.column()
        basal_dendrites_level_row.prop(scene, 'NMV_BasalDendritesBranchingLevel')

        # Apical Dendrites
        apical_dendrite_row = layout.row()
        apical_dendrite_row.prop(scene, 'NMV_BuildApicalDendrite')
        apical_dendrite_level_row = apical_dendrite_row.column()
        apical_dendrite_level_row.prop(scene, 'NMV_ApicalDendriteBranchingLevel')


####################################################################################################
# set_reconstruction_options
####################################################################################################
def set_reconstruction_options(layout,
                               scene,
                               options):
    """Morphology reconstruction options.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.NMV_
    :param options:
        System options.
    """

    # Reconstruction options
    reconstruction_options_row = layout.row()
    reconstruction_options_row.label(text='Reconstruction Options:', icon='OUTLINER_OB_EMPTY')

    # Morphology reconstruction techniques option
    morphology_reconstruction_row = layout.row()
    morphology_reconstruction_row.prop(
        scene, 'NMV_MorphologyReconstructionTechnique', icon='FORCE_CURVE')
    options.morphology.reconstruction_method = scene.NMV_MorphologyReconstructionTechnique

    # Connected sections only options
    if scene.NMV_MorphologyReconstructionTechnique == nmv.enums.Skeleton.Method.CONNECTED_SECTIONS:

        # Skeleton style
        skeleton_style_row = layout.row()
        skeleton_style_row.label(text='Skeleton Style:')
        skeleton_style_row.prop(scene, 'NMV_ArborsStyle', icon='WPAINT_HLT')
        options.morphology.arbor_style = scene.NMV_ArborsStyle

        # Morphology branching
        branching_row = layout.row()
        branching_row.label(text='Branching:')
        branching_row.prop(scene, 'NMV_MorphologyBranching', expand=True)
        options.morphology.branching = scene.NMV_MorphologyBranching

    # Connection to somata
    arbor_to_soma_connection_row = layout.row()
    arbor_to_soma_connection_row.label(text='Arbors to Soma:')
    arbor_to_soma_connection_row.prop(scene, 'NMV_SomaConnectionToRoot')
    options.morphology.arbors_to_soma_connection = scene.NMV_SomaConnectionToRoot

    # Sections resampling
    resampling_row = layout.row()
    resampling_row.label(text='Resampling:')
    resampling_row.prop(scene, 'NMV_MorphologyResampling')
    options.morphology.resampling_method = scene.NMV_MorphologyResampling

    # If Fixed Step resampling method is selected, add the sampling step
    if scene.NMV_MorphologyResampling == nmv.enums.Skeleton.Resampling.FIXED_STEP:
        resampling_step_row = layout.row()
        resampling_step_row.label(text='Resampling Step:')
        resampling_step_row.prop(scene, 'NMV_MorphologyResamplingStep')
        options.morphology.resampling_step = scene.NMV_MorphologyResamplingStep

    # Sections diameters option
    sections_radii_row = layout.row()
    sections_radii_row.label(text='Arbors Radii:')
    sections_radii_row.prop(scene, 'NMV_SectionsRadii', icon='SURFACE_NCURVE')

    # Radii as specified in the morphology file
    if scene.NMV_SectionsRadii == nmv.enums.Skeleton.Radii.ORIGINAL:
        options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.ORIGINAL
        options.morphology.scale_sections_radii = False
        options.morphology.unify_sections_radii = False
        options.morphology.sections_radii_scale = 1.0

    # Unified diameter
    elif scene.NMV_SectionsRadii == nmv.enums.Skeleton.Radii.UNIFIED:
        fixed_diameter_row = layout.row()
        fixed_diameter_row.label(text='Fixed Radius Value:')
        fixed_diameter_row.prop(scene, 'NMV_UnifiedRadiusValue')
        options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.UNIFIED
        options.morphology.scale_sections_radii = False
        options.morphology.unify_sections_radii = True
        options.morphology.samples_unified_radii_value = scene.NMV_UnifiedRadiusValue

    # Unified diameter per arbor type
    elif scene.NMV_SectionsRadii == nmv.enums.Skeleton.Radii.UNIFIED_PER_ARBOR_TYPE:
        options.morphology.arbors_radii = \
            nmv.enums.Skeleton.Radii.UNIFIED_PER_ARBOR_TYPE
        options.morphology.scale_sections_radii = False
        options.morphology.unify_sections_radii = True

        if nmv.interface.ui_morphology.has_axons():
            axon_radius_row = layout.row()
            axon_radius_row.label(text='Axon Radius:')
            axon_radius_row.prop(scene, 'NMV_AxonUnifiedRadiusValue')
            options.morphology.axon_samples_unified_radii_value = scene.NMV_AxonUnifiedRadiusValue

        if nmv.interface.ui_morphology.has_apical_dendrites():
            apical_dendrite_radius_row = layout.row()
            apical_dendrite_radius_row.label(text='Apical Dendrite Radius:')
            apical_dendrite_radius_row.prop(scene, 'NMV_ApicalDendriteUnifiedRadiusValue')
            options.morphology.apical_dendrite_samples_unified_radii_value = \
                scene.NMV_ApicalDendriteUnifiedRadiusValue

        if nmv.interface.ui_morphology.has_basal_dendrites():
            basal_dendrites_radius_row = layout.row()
            basal_dendrites_radius_row.label(text='Basal Dendrites Radius:')
            basal_dendrites_radius_row.prop(scene, 'NMV_BasalDendritesUnifiedRadiusValue')
            options.morphology.basal_dendrites_samples_unified_radii_value = \
                scene.NMV_BasalDendritesUnifiedRadiusValue

    # Scaled diameter
    elif scene.NMV_SectionsRadii == nmv.enums.Skeleton.Radii.SCALED:
        scaled_diameter_row = layout.row()
        scaled_diameter_row.label(text='Radius Scale Factor:')
        scaled_diameter_row.prop(scene, 'NMV_RadiusScaleValue')
        options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.SCALED
        options.morphology.unify_sections_radii = False
        options.morphology.scale_sections_radii = True
        options.morphology.sections_radii_scale = scene.NMV_RadiusScaleValue

    # Filtered
    elif scene.NMV_SectionsRadii == nmv.enums.Skeleton.Radii.FILTERED:
        filtered_diameter_row = layout.row()
        filtered_diameter_row.label(text='Radius Threshold:')
        filtered_diameter_row.prop(scene, 'NMV_FilteredRadiusThreshold')
        options.morphology.unify_sections_radii = False
        options.morphology.scale_sections_radii = True
        options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.FILTERED
        options.morphology.threshold_radius = scene.NMV_FilteredRadiusThreshold
    else:
        nmv.logger.log('ERROR')

    # Arbor quality option
    arbor_quality_row = layout.row()
    arbor_quality_row.label(text='Arbor Quality:')
    arbor_quality_row.prop(scene, 'NMV_ArborQuality')
    options.morphology.bevel_object_sides = scene.NMV_ArborQuality


####################################################################################################
# set_color_options
####################################################################################################
def set_color_options(layout,
                      scene,
                      options):
    """Morphology color options.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Color parameters
    arbors_colors_row = layout.row()
    arbors_colors_row.label(text='Morphology Colors:', icon='COLOR')

    # Morphology material
    morphology_material_row = layout.row()
    morphology_material_row.prop(scene, 'NMV_MorphologyMaterial')
    options.shading.morphology_material = scene.NMV_MorphologyMaterial

    color_by_part_row = layout.row()
    color_by_part_row.prop(scene, 'NMV_ColorArborByPart')
    color_bw_row = color_by_part_row.column()
    color_bw_row.prop(scene, 'NMV_ColorArborBlackAndWhite')
    color_bw_row.enabled = False

    # Assign different colors to each part of the skeleton by part
    if scene.NMV_ColorArborByPart:
        options.shading.morphology_axons_color = Vector((-1, 0, 0))
        options.shading.morphology_basal_dendrites_color = Vector((-1, 0, 0))
        options.shading.morphology_apical_dendrites_color = Vector((-1, 0, 0))
        color_bw_row.enabled = True

        # Render in black and white
        if scene.NMV_ColorArborBlackAndWhite:
            options.shading.morphology_axons_color = Vector((0, -1, 0))
            options.shading.morphology_basal_dendrites_color = Vector((0, -1, 0))
            options.shading.morphology_apical_dendrites_color = Vector((0, -1, 0))

    # One color per component
    else:

        # Homogeneous morphology coloring
        homogeneous_color_row = layout.row()
        homogeneous_color_row.prop(scene, 'NMV_MorphologyHomogeneousColor')

        # If the homogeneous color flag is set
        if scene.NMV_MorphologyHomogeneousColor:

            neuron_color_row = layout.row()
            neuron_color_row.prop(scene, 'NMV_NeuronMorphologyColor')
            color = scene.NMV_NeuronMorphologyColor
            options.shading.morphology_soma_color = Vector((color.r, color.g, color.b))
            options.shading.morphology_axons_color = Vector((color.r, color.g, color.b))
            options.shading.morphology_basal_dendrites_color = Vector((color.r, color.g, color.b))
            options.shading.morphology_apical_dendrites_color = Vector((color.r, color.g, color.b))
            options.shading.morphology_articulation_color = Vector((color.r, color.g, color.b))
        else:

            # Soma color option
            soma_color_row = layout.row()
            soma_color_row.prop(scene, 'NMV_SomaColor')
            if not scene.NMV_BuildSoma:
                soma_color_row.enabled = False

            # Pass options from UI to system
            soma_color_value = Vector((scene.NMV_SomaColor.r,
                                       scene.NMV_SomaColor.g,
                                       scene.NMV_SomaColor.b))
            options.shading.morphology_soma_color = soma_color_value

            # The morphology must be loaded to be able to draw these options
            if nmv.interface.ui_morphology is not None:

                # Axon color option
                if nmv.interface.ui_morphology.has_axons():
                    axons_color_row = layout.row()
                    axons_color_row.prop(scene, 'NMV_AxonColor')
                    if not scene.NMV_BuildAxon or scene.NMV_ColorArborByPart:
                        axons_color_row.enabled = False

                    # Pass options from UI to system
                    axons_color_value = Vector((scene.NMV_AxonColor.r,
                                               scene.NMV_AxonColor.g,
                                               scene.NMV_AxonColor.b))
                    options.shading.morphology_axons_color = axons_color_value

                # Basal dendrites color option
                if nmv.interface.ui_morphology.has_basal_dendrites():
                    basal_dendrites_color_row = layout.row()
                    basal_dendrites_color_row.prop(scene, 'NMV_BasalDendritesColor')
                    if not scene.NMV_BuildBasalDendrites or scene.NMV_ColorArborByPart:
                        basal_dendrites_color_row.enabled = False

                    # Pass options from UI to system
                    color = scene.NMV_BasalDendritesColor
                    basal_dendrites_color_value = Vector((color.r, color.g, color.b))
                    options.shading.morphology_basal_dendrites_color = basal_dendrites_color_value

                # Apical dendrite color option
                if nmv.interface.ui_morphology.has_apical_dendrites():
                    apical_dendrites_color_row = layout.row()
                    apical_dendrites_color_row.prop(scene, 'NMV_ApicalDendriteColor')
                    if not scene.NMV_BuildApicalDendrite or scene.NMV_ColorArborByPart:
                        apical_dendrites_color_row.enabled = False

                    # Pass options from UI to system
                    color = scene.NMV_ApicalDendriteColor
                    apical_dendrites_color_value = Vector((color.r, color.g, color.b))
                    options.shading.morphology_apical_dendrites_color = apical_dendrites_color_value

                # Articulation color option
                technique = scene.NMV_MorphologyReconstructionTechnique
                if technique == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
                    articulation_color_row = layout.row()
                    articulation_color_row.prop(scene, 'NMV_ArticulationColor')

                    # Pass options from UI to system
                    color = scene.NMV_ArticulationColor
                    articulation_color_value = Vector((color.r, color.g, color.b))
                    options.shading.morphology_articulation_color = articulation_color_value

            # Only a simple UI
            else:

                # Axons
                axons_color_row = layout.row()
                axons_color_row.prop(scene, 'NMV_AxonColor')

                # Apical dendrites
                basal_dendrites_color_row = layout.row()
                basal_dendrites_color_row.prop(scene, 'NMV_BasalDendritesColor')

                # Apical dendrites
                apical_dendrites_color_row = layout.row()
                apical_dendrites_color_row.prop(scene, 'NMV_ApicalDendriteColor')

                # Articulation color option
                articulation_color_row = layout.row()
                articulation_color_row.prop(scene, 'NMV_ArticulationColor')


####################################################################################################
# set_rendering_options
####################################################################################################
def set_rendering_options(layout,
                          scene,
                          options):
    """Morphology rendering options.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.NMV_
    :param options:
        System options.
    """

    # Quick rendering options
    quick_rendering_row = layout.row()
    quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')

    # Rendering view
    rendering_view_row = layout.row()
    rendering_view_row.prop(scene, 'NMV_MorphologyRenderingView', expand=True)

    # Close up view
    if scene.NMV_MorphologyRenderingView == nmv.enums.Rendering.View.CLOSE_UP:

        # Rendering close up option
        render_close_up_row = layout.row()
        render_close_up_row.prop(scene, 'NMV_MorphologyCloseUpDimensions')

        # Frame resolution option
        frame_resolution_row = layout.row()
        frame_resolution_row.label(text='Frame Resolution:')
        frame_resolution_row.prop(scene, 'NMV_MorphologyFrameResolution')
        frame_resolution_row.enabled = True

    # Full morphology view
    else:

        # Rendering type
        rendering_type_row = layout.row()
        rendering_type_row.prop(scene, 'NMV_RenderingType', expand=True)

        # Render at a specific resolution
        if scene.NMV_RenderingType == nmv.enums.Rendering.Resolution.FIXED:

            # Frame resolution option
            frame_resolution_row = layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(scene, 'NMV_MorphologyFrameResolution')
            frame_resolution_row.enabled = True

        # Otherwise, render to scale
        else:

            # Scale factor option
            scale_factor_row = layout.row()
            scale_factor_row.prop(scene, 'NMV_MorphologyFrameScaleFactor')
            scale_factor_row.enabled = True

    # Image extension
    image_extension_row = layout.row()
    image_extension_row.label(text='Image Format:')
    image_extension_row.prop(scene, 'NMV_MorphologyImageFormat')
    nmv.interface.ui_options.morphology.image_format = scene.NMV_MorphologyImageFormat

    # Render view buttons
    render_view_row = layout.row()
    render_view_row.label(text='Render View:', icon='RESTRICT_RENDER_OFF')
    render_view_buttons_row = layout.row(align=True)
    render_view_buttons_row.operator('nmv.render_morphology_front', icon='AXIS_FRONT')
    render_view_buttons_row.operator('nmv.render_morphology_side', icon='AXIS_SIDE')
    render_view_buttons_row.operator('nmv.render_morphology_top', icon='AXIS_TOP')
    render_view_buttons_row.enabled = True

    # Render animations buttons
    render_animation_row = layout.row()
    render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
    render_animations_buttons_row = layout.row(align=True)
    render_animations_buttons_row.operator('nmv.render_morphology_360', icon='FORCE_MAGNETIC')
    render_animations_buttons_row.operator('nmv.render_morphology_progressive', icon='FORCE_HARMONIC')
    render_animations_buttons_row.enabled = True

    # Progress bar
    progress_bar_row = layout.row()
    progress_bar_row.prop(scene, 'NMV_MorphologyRenderingProgress')
    progress_bar_row.enabled = False


####################################################################################################
# set_export_options
####################################################################################################
def set_export_options(layout,
                       scene,
                       options):
    """Morphology export options.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Saving morphology options
    save_morphology_row = layout.row()
    save_morphology_row.label(text='Save Morphology As:', icon='MESH_UVSPHERE')

    # Saving morphology buttons
    save_morphology_buttons_column = layout.column(align=True)
    save_morphology_buttons_column.operator('nmv.save_morphology_blend', icon='OUTLINER_OB_META')
    save_morphology_buttons_column.operator('nmv.save_morphology_swc', icon='GROUP_VERTEX')
    save_morphology_buttons_column.operator('nmv.save_morphology_segments', icon='GROUP_VERTEX')
    save_morphology_buttons_column.enabled = True
