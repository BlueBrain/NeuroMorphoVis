####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# System imports
import copy

# Blender imports
import bpy
from bpy.props import BoolProperty

# Internal imports
import nmv.analysis
import nmv.builders
import nmv.scene
import nmv.enums
import nmv.consts


####################################################################################################
# @draw_morphology_label
####################################################################################################
def draw_morphology_label(layout, morphology):

    row = layout.row()
    row.label(text='Name: %s' % morphology.label)


####################################################################################################
# @draw_morphology_file_format
####################################################################################################
def draw_morphology_file_format(layout, morphology):

    row = layout.row()
    row.label(text='Format: %s' % morphology.file_format)


####################################################################################################
# @draw_load_morphology_for_analysis_message
####################################################################################################
def draw_load_morphology_for_analysis_message(layout):

    row = layout.row()
    row.label(text='Load Morphology to Get Analyzed!')


####################################################################################################
# @draw_export_analysis_header
####################################################################################################
def draw_export_analysis_header(layout):

    row = layout.row()
    row.label(text='Export Analysis Results', icon='MESH_UVSPHERE')


####################################################################################################
# @add_analysis_group_to_panel
####################################################################################################
def add_analysis_group_to_panel(prefix,
                                layout,
                                scene):
    """Adds the results of analysis of each arbor to the UI.

    :param prefix:
        The prefix 'in string format' that is used to tag or identify the arbor.
    :param layout:
        UI panel layout.
    :param scene:
        Blender scene.
    """

    # Create a column outline in the panel
    outline = layout.column()

    # Add the checkbox that was registered before to show/hide the group @register_group_checkbox
    outline.prop(scene, prefix)

    # If the checkbox is checked
    if getattr(scene, prefix):

        # Create a sub-column that aligns the analysis data from the original outline
        analysis_area = outline.column()

        # In case of showing the analysis results of the entire morphology, add the
        # results of the global analysis before the common ones
        if 'Morphology' in prefix:
            analysis_area.label(text='Soma')
            soma_area = analysis_area.column(align=True)
            for item in nmv.analysis.ui_soma_analysis_items:
                soma_area.prop(scene, '%s' % item.variable)

            analysis_area.label(text='Arbors')
            arbors_area = analysis_area.column(align=True)
            for item in nmv.analysis.ui_global_analysis_items:
                arbors_area.prop(scene, '%s' % item.variable)

        # Update the analysis area with all the filters, that are common
        for item in nmv.analysis.ui_per_arbor_analysis_items:
            analysis_area.prop(scene, '%s%s' % (prefix, item.variable))

        # Disable editing the analysis area
        analysis_area.enabled = False


####################################################################################################
# @add_analysis_groups_to_panel
####################################################################################################
def add_analysis_groups_to_panel(layout,
                                 scene,
                                 morphology):
    """Adds the results of the morphology analysis to the UI.

    :param morphology:
        Loaded morphology.
    :param layout:
        UI panel layout.
    :param scene:
        Blender scene.
    """

    # Bounding box information
    add_bounding_box_information_to_panel(morphology=morphology, layout=layout, scene=scene)

    # Morphology
    add_analysis_group_to_panel(prefix='Morphology', layout=layout, scene=scene)

    # Add the analysis results of the Apical Dendrites to the panel
    if morphology.has_apical_dendrites():
        for arbor in morphology.apical_dendrites:
            add_analysis_group_to_panel(prefix=arbor.tag, layout=layout, scene=scene)

    # Add the analysis results of the Basal Dendrites to the panel
    if morphology.basal_dendrites is not None:
        for arbor in morphology.basal_dendrites:
            add_analysis_group_to_panel(prefix=arbor.tag, layout=layout, scene=scene)

    # Add the analysis results of the Axons to the panel
    if morphology.has_axons():
        for arbor in morphology.axons:
            add_analysis_group_to_panel(prefix=arbor.tag, layout=layout, scene=scene)


####################################################################################################
# @add_bounding_box_information_to_panel
####################################################################################################
def add_bounding_box_information_to_panel(morphology,
                                          layout,
                                          scene):
    """Computes the bounding box information of the morphology and adds them to the analysis panel.

    :param morphology:
        The input morphology being analyzed.
    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    """

    # Draw the bounding box
    bounding_box_p_row = layout.row()
    bounding_box_p_min_row = bounding_box_p_row.column(align=True)
    bounding_box_p_min_row.label(text='BBox PMin:')
    bounding_box_p_min_row.prop(scene, 'NMV_BBoxPMinX')
    bounding_box_p_min_row.prop(scene, 'NMV_BBoxPMinY')
    bounding_box_p_min_row.prop(scene, 'NMV_BBoxPMinZ')
    bounding_box_p_min_row.enabled = False

    bounding_box_p_max_row = bounding_box_p_row.column(align=True)
    bounding_box_p_max_row.label(text='BBox PMax:')
    bounding_box_p_max_row.prop(scene, 'NMV_BBoxPMaxX')
    bounding_box_p_max_row.prop(scene, 'NMV_BBoxPMaxY')
    bounding_box_p_max_row.prop(scene, 'NMV_BBoxPMaxZ')
    bounding_box_p_max_row.enabled = False

    bounding_box_data_row = layout.row()
    bounding_box_center_row = bounding_box_data_row.column(align=True)
    bounding_box_center_row.label(text='BBox Center:')
    bounding_box_center_row.prop(scene, 'NMV_BBoxCenterX')
    bounding_box_center_row.prop(scene, 'NMV_BBoxCenterY')
    bounding_box_center_row.prop(scene, 'NMV_BBoxCenterZ')
    bounding_box_center_row.enabled = False

    bounding_box_bounds_row = bounding_box_data_row.column(align=True)
    bounding_box_bounds_row.label(text='BBox Bounds:')
    bounding_box_bounds_row.prop(scene, 'NMV_BoundsX')
    bounding_box_bounds_row.prop(scene, 'NMV_BoundsY')
    bounding_box_bounds_row.prop(scene, 'NMV_BoundsZ')
    bounding_box_bounds_row.enabled = False


####################################################################################################
# @draw_layout_props
####################################################################################################
def draw_layout_props(panel, scene, options, morphology):

    # The morphology must be loaded to the UI and analyzed to be able to draw the analysis
    # components based on its arbors count
    if morphology is not None:

        draw_morphology_label(layout=panel.layout, morphology=morphology)

        draw_morphology_file_format(layout=panel.layout, morphology=morphology)

        # If the morphology is analyzed, then add the results to the analysis panel
        add_analysis_groups_to_panel(layout=panel.layout, scene=scene, morphology=morphology)

        draw_export_analysis_header(layout=panel.layout)

        export_analysis_row = panel.layout.row()
        export_analysis_row.operator('nmv.export_analysis_results', icon='MESH_DATA')

        create_plots_row = panel.layout.row()
        create_plots_row.operator('nmv.create_neuron_card', icon='MESH_DATA')

        if nmv.interface.ui_morphology_analyzed:
            morphology_stats_row = panel.layout.row()
            morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')
            analysis_time_row = panel.layout.row()
            analysis_time_row.prop(scene, 'NMV_MorphologyAnalysisTime')
            analysis_time_row.enabled = False

    # Load a morphology file to get analyzed !
    else:
        draw_load_morphology_for_analysis_message(layout=panel.layout)