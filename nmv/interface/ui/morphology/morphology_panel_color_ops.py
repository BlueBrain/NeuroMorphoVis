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

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @draw_soma_color_option
####################################################################################################
def draw_soma_color_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_SomaColor')
    row.enabled = True if scene.NMV_BuildSoma else False
    rgb = scene.NMV_SomaColor
    options.shading.morphology_soma_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_axons_color_option
####################################################################################################
def draw_axons_color_option(layout, scene, options, morphology):

    if morphology.has_axons():
        row = layout.row()
        row.prop(scene, 'NMV_AxonColor')
        row.enabled = True if scene.NMV_BuildAxon else False
        rgb = scene.NMV_AxonColor
        options.shading.morphology_axons_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_basal_dendrites_color_option
####################################################################################################
def draw_basal_dendrites_color_option(layout, scene, options, morphology):

    if morphology.has_basal_dendrites():
        row = layout.row()
        row.prop(scene, 'NMV_BasalDendritesColor')
        row.enabled = True if scene.NMV_BuildBasalDendrites else False
        rgb = scene.NMV_BasalDendritesColor
        options.shading.morphology_basal_dendrites_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_apical_dendrites_color_option
####################################################################################################
def draw_apical_dendrites_color_option(layout, scene, options, morphology):

    if morphology.has_apical_dendrites():
        row = layout.row()
        row.prop(scene, 'NMV_ApicalDendriteColor')
        row.enabled = True if scene.NMV_BuildApicalDendrite else False
        rgb = scene.NMV_ApicalDendriteColor
        options.shading.morphology_apical_dendrites_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_endfeet_color_option
####################################################################################################
def draw_endfeet_color_option(layout, scene, options, morphology):

    row = layout.row()
    row.prop(scene, 'NMV_EndfeetColor')
    rgb = scene.NMV_EndfeetColor
    options.shading.morphology_endfeet_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_articulation_color_option
####################################################################################################
def draw_articulation_color_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_ArticulationColor')
    rgb = scene.NMV_ArticulationColor
    options.shading.morphology_articulation_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_morphology_demo_color_options
####################################################################################################
def draw_morphology_demo_color_options(layout, scene, options):

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
# @draw_default_morphology_color_options
####################################################################################################
def draw_default_morphology_color_options(layout, scene, options, morphology):

    # Soma color option
    draw_soma_color_option(layout=layout, scene=scene, options=options)

    # The morphology must be loaded to be able to draw these options, otherwise draw demo
    if morphology is not None:
        draw_axons_color_option(
            layout=layout, scene=scene, options=options, morphology=morphology)
        draw_basal_dendrites_color_option(
            layout=layout, scene=scene, options=options, morphology=morphology)
        draw_apical_dendrites_color_option(
            layout=layout, scene=scene, options=options, morphology=morphology)

        # Technique-specific options
        technique = scene.NMV_MorphologyReconstructionTechnique
        if technique == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
            draw_articulation_color_option(layout=layout, scene=scene, options=options)

        # Is the loaded morphology has any endfeet, i.e. astrocytes
        if nmv.interface.ui_morphology.has_endfeet():
            draw_endfeet_color_option(
                layout=layout, scene=scene, options=options, morphology=morphology)
    else:
        draw_morphology_demo_color_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_homogeneous_color_option
####################################################################################################
def draw_homogeneous_color_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_MorphologyColor')
    rgb = scene.NMV_MorphologyColor
    homogeneous_color = Vector((rgb.r, rgb.g, rgb.b))
    options.shading.morphology_soma_color = homogeneous_color
    options.shading.morphology_axons_color = homogeneous_color
    options.shading.morphology_basal_dendrites_color = homogeneous_color
    options.shading.morphology_apical_dendrites_color = homogeneous_color
    options.shading.morphology_articulation_color = homogeneous_color
    options.shading.morphology_endfeet_color = homogeneous_color


####################################################################################################
# @draw_alternating_colors_option
####################################################################################################
def draw_alternating_colors_option(layout, scene, options):

    draw_soma_color_option(layout=layout, scene=scene, options=options)

    # Color 1
    row_1 = layout.row()
    row_1.prop(scene, 'NMV_MorphologyColor1')
    options.shading.morphology_alternating_color_1 = scene.NMV_MorphologyColor1

    # Color 2
    row_2 = layout.row()
    row_2.prop(scene, 'NMV_MorphologyColor2')
    options.shading.morphology_alternating_color_2 = scene.NMV_MorphologyColor2

    # Technique-specific options
    technique = scene.NMV_MorphologyReconstructionTechnique
    if technique == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
        draw_articulation_color_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_colormap_options
####################################################################################################
def draw_colormap_options(layout, scene, options):

    # Color map
    color_map_row = layout.row()
    color_map_row.label(text='Color Map')
    color_map_row.prop(scene, 'NMV_ColorMap')
    color_map_row.prop(scene, 'NMV_InvertColorMap')

    # Clear the color map passed to VMV if it is full
    if len(nmv.interface.ui_options.shading.morphology_colormap_list) > 0:
        nmv.interface.ui_options.shading.morphology_colormap_list.clear()

    # Soma
    draw_soma_color_option(layout=layout, scene=scene, options=options)

    # Fill list of colors
    for i in range(nmv.consts.Color.COLORMAP_RESOLUTION):

        # Add the colormap element to the UI
        colors = layout.row()
        colormap_element = colors.column()
        colormap_element.prop(scene, 'NMV_Color%d' % i)

        # Colormap range values
        values = colors.row()
        values.prop(scene, 'NMV_R0_Value%d' % i)
        values.prop(scene, 'NMV_R1_Value%d' % i)
        values.enabled = False

        # Get the color value from the panel
        color = getattr(scene, 'NMV_Color%d' % i)
        nmv.interface.ui_options.shading.morphology_colormap_list.append(color)


####################################################################################################
# @draw_per_section_color_coding_options
####################################################################################################
def draw_per_section_color_coding_options(layout, scene, options, morphology):

    row = layout.row()
    row.label(text='Color Coding')
    row.prop(scene, 'NMV_PerSectionColorCodingBasis')
    options.shading.morphology_coloring_scheme = scene.NMV_PerSectionColorCodingBasis

    if options.shading.morphology_coloring_scheme == nmv.enums.ColorCoding.DEFAULT_SCHEME:
        draw_default_morphology_color_options(
            layout=layout, scene=scene, options=options, morphology=morphology)
    elif options.shading.morphology_coloring_scheme == nmv.enums.ColorCoding.HOMOGENEOUS_COLOR:
        draw_homogeneous_color_option(layout=layout, scene=scene, options=options)
    elif options.shading.morphology_coloring_scheme == nmv.enums.ColorCoding.ALTERNATING_COLORS:
        draw_alternating_colors_option(layout=layout, scene=scene, options=options)
    else:
        draw_colormap_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_per_segment_color_coding_options
####################################################################################################
def draw_per_segment_color_coding_options(layout, scene, options, morphology):

    row = layout.row()
    row.label(text='Color Coding')
    row.prop(scene, 'NMV_PerSegmentColorCodingBasis')
    options.shading.morphology_coloring_scheme = scene.NMV_PerSegmentColorCodingBasis

    if options.shading.morphology_coloring_scheme == nmv.enums.ColorCoding.DEFAULT_SCHEME:
        draw_default_morphology_color_options(
            layout=layout, scene=scene, options=options, morphology=morphology)
    elif options.shading.morphology_coloring_scheme == nmv.enums.ColorCoding.HOMOGENEOUS_COLOR:
        draw_homogeneous_color_option(layout=layout, scene=scene, options=options)
    elif options.shading.morphology_coloring_scheme == nmv.enums.ColorCoding.ALTERNATING_COLORS:
        draw_alternating_colors_option(layout=layout, scene=scene, options=options)
    else:
        draw_colormap_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_morphology_colors_header
####################################################################################################
def draw_morphology_colors_header(layout):

    row = layout.row()
    row.label(text='Morphology Colors', icon='COLOR')


####################################################################################################
# @draw_morphology_shading_option
####################################################################################################
def draw_morphology_shading_option(layout, scene, options):

    row = layout.row()
    row.label(text='Shading')
    row.prop(scene, 'NMV_MorphologyMaterial')
    options.shading.morphology_material = scene.NMV_MorphologyMaterial


####################################################################################################
# @draw_morphology_color_options
####################################################################################################
def draw_morphology_color_options(layout, scene, options, morphology):

    draw_morphology_colors_header(layout=layout)
    draw_morphology_shading_option(layout=layout, scene=scene, options=options)

    method = options.morphology.reconstruction_method

    # Each SECTION has a different color
    if method == nmv.enums.Skeleton.Method.DISCONNECTED_SECTIONS:
        draw_per_section_color_coding_options(
            layout=layout, scene=scene, options=options, morphology=morphology)
    elif method == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
        draw_per_section_color_coding_options(
            layout=layout, scene=scene, options=options, morphology=morphology)
    elif method == nmv.enums.Skeleton.Method.PROGRESSIVE:
        draw_per_section_color_coding_options(
            layout=layout, scene=scene, options=options, morphology=morphology)

    # Each SEGMENT has a different color
    elif method == nmv.enums.Skeleton.Method.DISCONNECTED_SEGMENTS:
        draw_per_segment_color_coding_options(
            layout=layout, scene=scene, options=options, morphology=morphology)

    # Every ARBOR has a different color
    elif method == nmv.enums.Skeleton.Method.CONNECTED_SECTIONS:
        draw_default_morphology_color_options(
            layout=layout, scene=scene, options=options, morphology=morphology)
    elif method == nmv.enums.Skeleton.Method.SAMPLES:
        draw_default_morphology_color_options(
            layout=layout, scene=scene, options=options, morphology=morphology)
    elif method == nmv.enums.Skeleton.Method.DENDROGRAM:
        draw_default_morphology_color_options(
            layout=layout, scene=scene, options=options, morphology=morphology)
    else:
        nmv.logger.log('UI_ERROR: add_morphology_color_options')

    layout.separator()
