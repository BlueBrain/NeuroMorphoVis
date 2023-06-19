####################################################################################################
# Copyright (c) 2016 - 2022, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
# @add_soma_coloring_option
####################################################################################################
def add_soma_coloring_option(layout,
                             scene,
                             options):
    """Adds the coloring options of the soma. The soma coloring options are always added except for
    homogeneous coloring scheme.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Soma color option
    soma_color_row = layout.row()
    soma_color_row.prop(scene, 'NMV_SomaColor')

    # Make sure to build the soma, otherwise disable the wor
    if not scene.NMV_BuildSoma:
        soma_color_row.enabled = False

    # Pass options from UI to system
    options.shading.morphology_soma_color = Vector((scene.NMV_SomaColor.r,
                                                    scene.NMV_SomaColor.g,
                                                    scene.NMV_SomaColor.b))


####################################################################################################
# @add_axons_coloring_options
####################################################################################################
def add_axons_coloring_options(layout,
                               scene,
                               options):
    """Adds the coloring options of the axons.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """
    # The axon must be present
    if nmv.interface.ui_morphology.has_axons():

        # Axon color option
        axons_color_row = layout.row()
        axons_color_row.prop(scene, 'NMV_AxonColor')

        # Make sure that the user want to visualize the axons
        if not scene.NMV_BuildAxon:
            axons_color_row.enabled = False

        # Pass options from UI to system
        options.shading.morphology_axons_color = Vector((
            scene.NMV_AxonColor.r, scene.NMV_AxonColor.g, scene.NMV_AxonColor.b))


####################################################################################################
# @add_basal_dendrites_coloring_options
####################################################################################################
def add_basal_dendrites_coloring_options(layout,
                                         scene,
                                         options):
    """Adds the coloring options of the basal dendrites.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # The morphology must have basal dendrites
    if nmv.interface.ui_morphology.has_basal_dendrites():

        # Basal dendrites color option
        basal_dendrites_color_row = layout.row()
        basal_dendrites_color_row.prop(scene, 'NMV_BasalDendritesColor')

        # Make sure that the user want to visualize the basal dendrites
        if not scene.NMV_BuildBasalDendrites:
            basal_dendrites_color_row.enabled = False

        # Pass options from UI to system
        options.shading.morphology_basal_dendrites_color = Vector((
            scene.NMV_BasalDendritesColor.r,
            scene.NMV_BasalDendritesColor.g,
            scene.NMV_BasalDendritesColor.b))


####################################################################################################
# @add_apical_dendrites_coloring_options
####################################################################################################
def add_apical_dendrites_coloring_options(layout,
                                          scene,
                                          options):
    """Adds the coloring options of the apical dendrites.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """
    # The morphology must have apical dendrites
    if nmv.interface.ui_morphology.has_apical_dendrites():

        # Apical dendrite color option
        apical_dendrites_color_row = layout.row()
        apical_dendrites_color_row.prop(scene, 'NMV_ApicalDendriteColor')

        # Make sure that the user want to visualize the apical dendrites
        if not scene.NMV_BuildApicalDendrite:
            apical_dendrites_color_row.enabled = False

        # Pass options from UI to system
        options.shading.morphology_apical_dendrites_color = Vector((
            scene.NMV_ApicalDendriteColor.r,
            scene.NMV_ApicalDendriteColor.g,
            scene.NMV_ApicalDendriteColor.b))


####################################################################################################
# @add_articulation_coloring_options
####################################################################################################
def add_endfeet_coloring_options(layout,
                                 scene,
                                 options):
    """Adds the coloring options of the endfeet in case of loaded astrocytes.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Endfeet color option
    endfeet_color_row = layout.row()
    endfeet_color_row.prop(scene, 'NMV_EndfeetColor')

    # Pass options from UI to system
    options.shading.morphology_endfeet_color = Vector((
        scene.NMV_EndfeetColor.r,
        scene.NMV_EndfeetColor.g,
        scene.NMV_EndfeetColor.b))


####################################################################################################
# @add_articulation_coloring_options
####################################################################################################
def add_articulation_coloring_options(layout,
                                      scene,
                                      options):
    """Adds the coloring options of the articulations in case of articulated sections mode.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Articulation color option
    articulation_color_row = layout.row()
    articulation_color_row.prop(scene, 'NMV_ArticulationColor')

    # Pass options from UI to system
    options.shading.morphology_articulation_color = Vector((
        scene.NMV_ArticulationColor.r,
        scene.NMV_ArticulationColor.g,
        scene.NMV_ArticulationColor.b))


####################################################################################################
# @add_default_coloring_option
####################################################################################################
def add_default_coloring_option(layout,
                                scene,
                                options):
    """Adds to the UI the single arbor color elements.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Soma color option
    add_soma_coloring_option(layout=layout, scene=scene, options=options)

    # The morphology must be loaded to be able to draw these options
    if nmv.interface.ui_morphology is not None:

        # Axons color option
        add_axons_coloring_options(layout=layout, scene=scene, options=options)

        # Basal dendrites color option
        add_basal_dendrites_coloring_options(layout=layout, scene=scene, options=options)

        # Apical dendrites color option
        add_apical_dendrites_coloring_options(layout=layout, scene=scene, options=options)

        # Articulation color option
        technique = scene.NMV_MorphologyReconstructionTechnique
        if technique == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
            add_articulation_coloring_options(layout=layout, scene=scene, options=options)

        # Endfeet color option
        if nmv.interface.ui_morphology.has_endfeet():
            add_endfeet_coloring_options(layout=layout, scene=scene, options=options)

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
# @add_homogeneous_color_option
####################################################################################################
def add_homogeneous_color_option(layout,
                                 scene,
                                 options):
    """Adds to the UI the homogeneous color elements.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # The homogeneous color of the morphology
    color_row = layout.row()
    color_row.prop(scene, 'NMV_MorphologyColor')
    color = scene.NMV_MorphologyColor
    options.shading.morphology_soma_color = Vector((color.r, color.g, color.b))
    options.shading.morphology_axons_color = Vector((color.r, color.g, color.b))
    options.shading.morphology_basal_dendrites_color = Vector((color.r, color.g, color.b))
    options.shading.morphology_apical_dendrites_color = Vector((color.r, color.g, color.b))
    options.shading.morphology_articulation_color = Vector((color.r, color.g, color.b))
    options.shading.morphology_endfeet_color = Vector((color.r, color.g, color.b))


####################################################################################################
# @add_alternating_colors_option
####################################################################################################
def add_alternating_colors_option(layout,
                                  scene,
                                  options):
    """Adds alternating coloring options. Simply two colors where we can see different patterns in
    the morphology.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Soma options
    add_soma_coloring_option(layout=layout, scene=scene, options=options)

    # Color 1
    color_1_row = layout.row()
    color_1_row.prop(scene, 'NMV_MorphologyColor1')
    options.shading.morphology_alternating_color_1 = scene.NMV_MorphologyColor1

    # Color 2
    color_2_row = layout.row()
    color_2_row.prop(scene, 'NMV_MorphologyColor2')
    options.shading.morphology_alternating_color_2 = scene.NMV_MorphologyColor2

    # Articulation color option
    technique = scene.NMV_MorphologyReconstructionTechnique
    if technique == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
        add_articulation_coloring_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @add_colormap_options
####################################################################################################
def add_colormap_options(layout,
                         scene,
                         options):
    """Adds the coloring options that gives extra components to assign a colormap to the morphology.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Color map
    color_map_row = layout.row()
    color_map_row.label(text='Color Map:')
    color_map_row.prop(scene, 'NMV_ColorMap')
    color_map_row.prop(scene, 'NMV_InvertColorMap')

    # Clear the color map passed to VMV if it is full
    if len(nmv.interface.ui_options.shading.morphology_colormap_list) > 0:
        nmv.interface.ui_options.shading.morphology_colormap_list.clear()

    # Soma options
    add_soma_coloring_option(layout=layout, scene=scene, options=options)

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
# @add_per_section_color_coding_options
####################################################################################################
def add_per_section_color_coding_options(layout,
                                         scene,
                                         options):
    """Adds the coloring options of the per-section coloring scheme.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Set the color coding scheme
    nmv.interface.ui_options.shading.morphology_coloring_scheme = \
        scene.NMV_PerSectionColorCodingBasis

    # Default coloring scheme
    if scene.NMV_PerSectionColorCodingBasis == nmv.enums.ColorCoding.DEFAULT_SCHEME:
        add_default_coloring_option(layout=layout, scene=scene, options=options)

    # Homogeneous color
    elif scene.NMV_PerSectionColorCodingBasis == nmv.enums.ColorCoding.HOMOGENEOUS_COLOR:
        add_homogeneous_color_option(layout=layout, scene=scene, options=options)

    # Alternating colors
    elif scene.NMV_PerSectionColorCodingBasis == nmv.enums.ColorCoding.ALTERNATING_COLORS:
        add_alternating_colors_option(layout=layout, scene=scene, options=options)

    # Using a colormap
    else:
        add_colormap_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @add_per_segment_color_coding_options
####################################################################################################
def add_per_segment_color_coding_options(layout,
                                         scene,
                                         options):
    """Adds the coloring options of the per-segment coloring scheme.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Color coding scheme
    nmv.interface.ui_options.shading.morphology_coloring_scheme = \
        scene.NMV_PerSegmentColorCodingBasis

    # Single arbor color
    if scene.NMV_PerSegmentColorCodingBasis == nmv.enums.ColorCoding.DEFAULT_SCHEME:
        add_default_coloring_option(layout=layout, scene=scene, options=options)

    # Homogeneous color
    elif scene.NMV_PerSegmentColorCodingBasis == nmv.enums.ColorCoding.HOMOGENEOUS_COLOR:
        add_homogeneous_color_option(layout=layout, scene=scene, options=options)

    # Alternating colors
    elif scene.NMV_PerSegmentColorCodingBasis == nmv.enums.ColorCoding.ALTERNATING_COLORS:
        add_alternating_colors_option(layout=layout, scene=scene, options=options)

    # Using a colormap
    else:
        add_colormap_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @add_color_options
####################################################################################################
def add_color_options(layout,
                      scene,
                      options):
    """Morphology coloring options.

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
    morphology_material_row.label(text='Shading:')
    morphology_material_row.prop(scene, 'NMV_MorphologyMaterial')
    options.shading.morphology_material = scene.NMV_MorphologyMaterial

    # Per-section color coding
    color_coding_row = layout.row()

    method = options.morphology.reconstruction_method

    # Each section is rendered independently
    if method == nmv.enums.Skeleton.Method.DISCONNECTED_SECTIONS or \
       method == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS or  \
       method == nmv.enums.Skeleton.Method.PROGRESSIVE:
        color_coding_row.label(text='Color Coding:')
        color_coding_row.prop(scene, 'NMV_PerSectionColorCodingBasis')
        add_per_section_color_coding_options(layout, scene, options)

    # Each segment is rendered independently
    elif method == nmv.enums.Skeleton.Method.DISCONNECTED_SEGMENTS:
        color_coding_row.label(text='Color Coding:')
        color_coding_row.prop(scene, 'NMV_PerSegmentColorCodingBasis')
        add_per_segment_color_coding_options(layout, scene, options)

    # The arbor is rendered in one piece as a set of connected sections in whatever format
    elif method == nmv.enums.Skeleton.Method.CONNECTED_SECTIONS or  \
         method == nmv.enums.Skeleton.Method.SAMPLES or             \
         method == nmv.enums.Skeleton.Method.DENDROGRAM:
        add_default_coloring_option(layout, scene, options)
