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
from mathutils import Vector

# Internal imports
import nmv
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
    skeleton_row.label(text='Morphology Skeleton:', icon='POSE_DATA')

    # Build soma options
    build_soma_row = layout.row()
    build_soma_row.label('Soma:')
    build_soma_row.prop(scene, 'BuildSoma', expand=True)

    # Pass options from UI to system
    options.morphology.soma_representation = scene.BuildSoma

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
    options.morphology.ignore_axon = not scene.BuildAxon
    options.morphology.axon_branch_order = scene.AxonBranchingLevel

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
    options.morphology.ignore_basal_dendrites = not scene.BuildBasalDendrites
    options.morphology.basal_dendrites_branch_order = scene.BasalDendritesBranchingLevel

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
    options.morphology.ignore_apical_dendrite = not scene.BuildApicalDendrite
    options.morphology.apical_dendrite_branch_order = scene.ApicalDendriteBranchingLevel


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
        Context scene.
    :param options:
        System options.
    """

    # Reconstruction options
    reconstruction_options_row = layout.row()
    reconstruction_options_row.label(text='Reconstruction Options:', icon='OUTLINER_OB_EMPTY')

    # Morphology reconstruction techniques option
    morphology_reconstruction_row = layout.row()
    morphology_reconstruction_row.prop(
        scene, 'MorphologyReconstructionTechnique', icon='FORCE_CURVE')

    # Pass options from UI to system
    options.morphology.reconstruction_method = scene.MorphologyReconstructionTechnique

    # Reconstruction technique
    technique = scene.MorphologyReconstructionTechnique
    if technique == nmv.enums.Skeletonization.Method.CONNECTED_SECTION_REPAIRED or \
       technique == nmv.enums.Skeletonization.Method.CONNECTED_SECTION_ORIGINAL or \
       technique == nmv.enums.Skeletonization.Method.DISCONNECTED_SKELETON_REPAIRED or \
       technique == nmv.enums.Skeletonization.Method.DISCONNECTED_SKELETON_ORIGINAL:

        # Morphology reconstruction techniques option
        skeleton_style_row = layout.row()
        skeleton_style_row.prop(scene, 'ArborsStyle', icon='WPAINT_HLT')

        # Pass options from UI to system
        options.morphology.arbor_style = scene.ArborsStyle

        # Morphology branching
        branching_row = layout.row()
        branching_row.label('Branching:')
        branching_row.prop(scene, 'MorphologyBranching', expand=True)

        # Pass options from UI to system
        options.morphology.branching = scene.MorphologyBranching

        # Morphology branching
        arbor_to_soma_connection_row = layout.row()
        arbor_to_soma_connection_row.prop(scene, 'SomaConnectionToRoot')

        # Pass options from UI to system
        options.morphology.arbors_to_soma_connection = scene.SomaConnectionToRoot

    # Arbor quality option
    arbor_quality_row = layout.row()
    arbor_quality_row.label(text='Arbor Quality:')
    arbor_quality_row.prop(scene, 'ArborQuality')

    # Pass options from UI to system
    options.morphology.bevel_object_sides = scene.ArborQuality

    # Sections diameters option
    sections_radii_row = layout.row()
    sections_radii_row.prop(scene, 'SectionsRadii', icon='SURFACE_NCURVE')

    # Radii as specified in the morphology file
    if scene.SectionsRadii == nmv.enums.Skeletonization.ArborsRadii.AS_SPECIFIED:

        # Pass options from UI to system

        options.morphology.arbors_radii = nmv.enums.Skeletonization.ArborsRadii.AS_SPECIFIED

        options.morphology.scale_sections_radii = False
        options.morphology.unify_sections_radii = False
        options.morphology.sections_radii_scale = 1.0

    # Fixed diameter
    elif scene.SectionsRadii == nmv.enums.Skeletonization.ArborsRadii.FIXED:

        fixed_diameter_row = layout.row()
        fixed_diameter_row.label(text='Fixed Radius Value:')
        fixed_diameter_row.prop(scene, 'FixedRadiusValue')

        options.morphology.arbors_radii = nmv.enums.Skeletonization.ArborsRadii.FIXED

        # Pass options from UI to system
        options.morphology.scale_sections_radii = False
        options.morphology.unify_sections_radii = True
        options.morphology.sections_fixed_radii_value = scene.FixedRadiusValue

    # Scaled diameter
    elif scene.SectionsRadii == nmv.enums.Skeletonization.ArborsRadii.SCALED:

        scaled_diameter_row = layout.row()
        scaled_diameter_row.label(text='Radius Scale Factor:')
        scaled_diameter_row.prop(scene, 'RadiusScaleValue')

        options.morphology.arbors_radii = nmv.enums.Skeletonization.ArborsRadii.SCALED

        # Pass options from UI to system
        options.morphology.unify_sections_radii = False
        options.morphology.scale_sections_radii = True
        options.morphology.sections_radii_scale = scene.RadiusScaleValue

    # Filtered
    elif scene.SectionsRadii == nmv.enums.Skeletonization.ArborsRadii.FILTERED:

        filtered_diameter_row = layout.row()
        filtered_diameter_row.label(text='Radius Threshold:')
        filtered_diameter_row.prop(scene, 'FilteredRadiusThreshold')

        # Pass options from UI to system
        options.morphology.unify_sections_radii = False
        options.morphology.scale_sections_radii = True
        options.morphology.arbors_radii = nmv.enums.Skeletonization.ArborsRadii.FILTERED
        options.morphology.threshold_radius = scene.FilteredRadiusThreshold
    else:
        nmv.logger.log('ERROR')


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
    morphology_material_row.prop(scene, 'MorphologyMaterial')

    # Pass options from UI to system
    options.morphology.material = scene.MorphologyMaterial

    color_by_part_row = layout.row()
    color_by_part_row.prop(scene, 'ColorArborByPart')
    color_bw_row = color_by_part_row.column()
    color_bw_row.prop(scene, 'ColorArborBlackAndWhite')
    color_bw_row.enabled = False

    # Assign different colors to each part of the skeleton by part
    if scene.ColorArborByPart:
        options.morphology.axon_color = Vector((-1, 0, 0))
        options.morphology.basal_dendrites_color = Vector((-1, 0, 0))
        options.morphology.apical_dendrites_color = Vector((-1, 0, 0))
        color_bw_row.enabled = True

        # Render in black and white
        if scene.ColorArborBlackAndWhite:
            options.morphology.axon_color = Vector((0, -1, 0))
            options.morphology.basal_dendrites_color = Vector((0, -1, 0))
            options.morphology.apical_dendrites_color = Vector((0, -1, 0))

    # One color per component
    else:

        # Homogeneous morphology coloring
        homogeneous_color_row = layout.row()
        homogeneous_color_row.prop(scene, 'MorphologyHomogeneousColor')

        # If the homogeneous color flag is set
        if scene.MorphologyHomogeneousColor:

            neuron_color_row = layout.row()
            neuron_color_row.prop(scene, 'NeuronMorphologyColor')

            # Pass options from UI to system
            color = scene.NeuronMorphologyColor
            options.morphology.soma_color = Vector((color.r, color.g, color.b))
            options.morphology.axon_color = Vector((color.r, color.g, color.b))
            options.morphology.basal_dendrites_color = Vector((color.r, color.g, color.b))
            options.morphology.apical_dendrites_color = Vector((color.r, color.g, color.b))
            options.morphology.articulation_color = Vector((color.r, color.g, color.b))
        else:

            # Soma color option
            soma_color_row = layout.row()
            soma_color_row.prop(scene, 'SomaColor')
            if not scene.BuildSoma:
                soma_color_row.enabled = False

            # Pass options from UI to system
            soma_color_value = Vector((scene.SomaColor.r, scene.SomaColor.g, scene.SomaColor.b))
            options.morphology.soma_color = soma_color_value

            # Axon color option
            axon_color_row = layout.row()
            axon_color_row.prop(scene, 'AxonColor')
            if not scene.BuildAxon or scene.ColorArborByPart:
                axon_color_row.enabled = False

            # Pass options from UI to system
            axon_color_value = Vector((scene.AxonColor.r, scene.AxonColor.g, scene.AxonColor.b))
            options.morphology.axon_color = axon_color_value

            # Basal dendrites color option
            basal_dendrites_color_row = layout.row()
            basal_dendrites_color_row.prop(scene, 'BasalDendritesColor')
            if not scene.BuildBasalDendrites or scene.ColorArborByPart:
                basal_dendrites_color_row.enabled = False

            # Pass options from UI to system
            color = scene.BasalDendritesColor
            basal_dendrites_color_value = Vector((color.r, color.g, color.b))
            options.morphology.basal_dendrites_color = basal_dendrites_color_value

            # Apical dendrite color option
            apical_dendrites_color_row = layout.row()
            apical_dendrites_color_row.prop(scene, 'ApicalDendriteColor')
            if not scene.BuildApicalDendrite or scene.ColorArborByPart:
                apical_dendrites_color_row.enabled = False

            # Pass options from UI to system
            color = scene.ApicalDendriteColor
            apical_dendrites_color_value = Vector((color.r, color.g, color.b))
            options.morphology.apical_dendrites_color = apical_dendrites_color_value

            # Articulation color option
            technique = scene.MorphologyReconstructionTechnique
            if technique == nmv.enums.Skeletonization.Method.ARTICULATED_SECTIONS:
                articulation_color_row = layout.row()
                articulation_color_row.prop(scene, 'ArticulationColor')

                # Pass options from UI to system
                color = scene.ArticulationColor
                articulation_color_value = Vector((color.r, color.g, color.b))
                options.morphology.articulation_color = articulation_color_value


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
        Context scene.
    :param options:
        System options.
    """

    # Quick rendering options
    quick_rendering_row = layout.row()
    quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')

    # Rendering view
    rendering_view_row = layout.row()
    rendering_view_row.prop(scene, 'MorphologyRenderingView', expand=True)

    # Close up view
    if scene.MorphologyRenderingView == nmv.enums.Skeletonization.Rendering.View.CLOSE_UP_VIEW:

        # Rendering close up option
        render_close_up_row = layout.row()
        render_close_up_row.prop(scene, 'MorphologyCloseUpDimensions')

        # Frame resolution option
        frame_resolution_row = layout.row()
        frame_resolution_row.label(text='Frame Resolution:')
        frame_resolution_row.prop(scene, 'MorphologyFrameResolution')
        frame_resolution_row.enabled = True

    # Full morphology view
    else:

        # Rendering type
        rendering_type_row = layout.row()
        rendering_type_row.prop(scene, 'RenderingType', expand=True)

        # Render at a specific resolution
        if scene.RenderingType == nmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION:

            # Frame resolution option
            frame_resolution_row = layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(scene, 'MorphologyFrameResolution')
            frame_resolution_row.enabled = True

        # Otherwise, render to scale
        else:

            # Scale factor option
            scale_factor_row = layout.row()
            scale_factor_row.label(text='Resolution Scale:')
            scale_factor_row.prop(scene, 'MorphologyFrameScaleFactor')
            scale_factor_row.enabled = True

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
    save_morphology_buttons_column.operator('save_morphology.blend', icon='OUTLINER_OB_META')
    save_morphology_buttons_column.operator('save_morphology.swc', icon='GROUP_VERTEX')
    save_morphology_buttons_column.operator('save_morphology.segments', icon='GROUP_VERTEX')
    save_morphology_buttons_column.enabled = True
