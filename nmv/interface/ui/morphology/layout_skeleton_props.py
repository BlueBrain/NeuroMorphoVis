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


####################################################################################################
# @draw_morphology_skeleton_display_header
####################################################################################################
def draw_morphology_skeleton_display_header(layout):

    row = layout.row()
    row.label(text='Morphology Skeleton Display Options', icon='QUESTION')


####################################################################################################
# @draw_soma_building_option
####################################################################################################
def draw_soma_building_option(layout, scene, options):

    row = layout.row()
    row.label(text='Display Soma As')
    row.prop(scene, 'NMV_BuildSoma')
    options.morphology.soma_representation = scene.NMV_BuildSoma


####################################################################################################
# @draw_axons_building_option
####################################################################################################
def draw_axons_building_option(layout, scene, options, morphology):

    if morphology.has_axons():
        axon_row = layout.row()
        axon_row.prop(scene, 'NMV_BuildAxon')
        axon_order_row = axon_row.column()
        axon_order_row.prop(scene, 'NMV_AxonsBranchingOrder')
        axon_order_row.enabled = True if scene.NMV_BuildAxon else False
        options.morphology.ignore_axons = not scene.NMV_BuildAxon
        options.morphology.axon_branch_order = scene.NMV_AxonsBranchingOrder


####################################################################################################
# @draw_basal_dendrites_building_option
####################################################################################################
def draw_basal_dendrites_building_option(layout, scene, options, morphology):

    if morphology.has_basal_dendrites():
        basal_dendrites_row = layout.row()
        basal_dendrites_row.prop(scene, 'NMV_BuildBasalDendrites')
        basal_dendrites_order_row = basal_dendrites_row.column()
        basal_dendrites_order_row.prop(scene, 'NMV_BasalDendritesBranchingOrder')
        basal_dendrites_order_row.enabled = True if scene.NMV_BuildBasalDendrites else False
        options.morphology.ignore_basal_dendrites = not scene.NMV_BuildBasalDendrites
        options.morphology.basal_dendrites_branch_order = scene.NMV_BasalDendritesBranchingOrder


####################################################################################################
# @draw_apical_dendrites_building_option
####################################################################################################
def draw_apical_dendrites_building_option(layout, scene, options, morphology):

    if morphology.has_apical_dendrites():
        apical_dendrites_row = layout.row()
        apical_dendrites_row.prop(scene, 'NMV_BuildApicalDendrite')
        apical_dendrites_order_row = apical_dendrites_row.column()
        apical_dendrites_order_row.prop(scene, 'NMV_ApicalDendritesBranchingOrder')
        apical_dendrites_order_row.enabled = True if scene.NMV_BuildApicalDendrite else False
        options.morphology.ignore_apical_dendrites = not scene.NMV_BuildApicalDendrite
        options.morphology.apical_dendrite_branch_order = scene.NMV_ApicalDendritesBranchingOrder


####################################################################################################
# @draw_demo_options
####################################################################################################
def draw_demo_options(layout, scene):

    # Axons
    axons_row = layout.row()
    axons_row.prop(scene, 'NMV_BuildAxon')
    axons_order_row = axons_row.column()
    axons_order_row.prop(scene, 'NMV_AxonsBranchingOrder')

    # Basal dendrites
    basal_dendrites_row = layout.row()
    basal_dendrites_row.prop(scene, 'NMV_BuildBasalDendrites')
    basal_dendrites_order_row = basal_dendrites_row.column()
    basal_dendrites_order_row.prop(scene, 'NMV_BasalDendritesBranchingOrder')

    # Apical Dendrites
    apical_dendrites_row = layout.row()
    apical_dendrites_row.prop(scene, 'NMV_BuildApicalDendrite')
    apical_dendrites_order_row = apical_dendrites_row.column()
    apical_dendrites_order_row.prop(scene, 'NMV_ApicalDendritesBranchingOrder')


####################################################################################################
# @draw_morphology_skeleton_display_options
####################################################################################################
def draw_morphology_skeleton_display_options(layout, scene, options, morphology):

    draw_morphology_skeleton_display_header(layout=layout)
    draw_soma_building_option(layout=layout, scene=scene, options=options)

    # The morphology must be loaded to be able to draw these options, otherwise draw a demo
    if morphology is not None:
        draw_axons_building_option(
            layout=layout, scene=scene, options=options, morphology=morphology)

        draw_basal_dendrites_building_option(
            layout=layout, scene=scene, options=options, morphology=morphology)

        draw_apical_dendrites_building_option(
            layout=layout, scene=scene, options=options, morphology=morphology)
    else:
        draw_demo_options(layout=layout, scene=scene)
    layout.separator()


