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
from mathutils import Vector

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @draw_mesh_colors_header
####################################################################################################
def draw_mesh_colors_header(layout):

    row = layout.row()
    row.label(text='Mesh Colors', icon='COLOR')


####################################################################################################
# @draw_mesh_shading_option
####################################################################################################
def draw_mesh_shading_option(layout, scene, options):

    row = layout.row()
    row.label(text='Shading')
    row.prop(scene, 'NMV_MeshMaterial')
    options.shading.mesh_material = scene.NMV_MeshMaterial



####################################################################################################
# @draw_soma_color_option
####################################################################################################
def draw_soma_color_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_SomaColor')
    rgb = scene.NMV_SomaColor
    options.shading.mesh_soma_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_axons_color_option
####################################################################################################
def draw_axons_color_option(layout, scene, options, morphology):

    if morphology.has_axons():
        row = layout.row()
        row.prop(scene, 'NMV_AxonColor')
        rgb = scene.NMV_AxonColor
        options.shading.mesh_axons_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_basal_dendrites_color_option
####################################################################################################
def draw_basal_dendrites_color_option(layout, scene, options, morphology):

    if morphology.has_basal_dendrites():
        row = layout.row()
        row.prop(scene, 'NMV_BasalDendritesColor')
        rgb = scene.NMV_BasalDendritesColor
        options.shading.mesh_basal_dendrites_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_apical_dendrites_color_option
####################################################################################################
def draw_apical_dendrites_color_option(layout, scene, options, morphology):

    if morphology.has_apical_dendrites():
        row = layout.row()
        row.prop(scene, 'NMV_ApicalDendriteColor')
        rgb = scene.NMV_ApicalDendriteColor
        options.shading.mesh_apical_dendrites_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_apical_dendrites_color_option
####################################################################################################
def draw_spines_color_option(layout, scene, options, morphology):

    if options.mesh.spines != nmv.enums.Meshing.Spines.Source.IGNORE:
        row = layout.row()
        row.prop(scene, 'NMV_SpinesMeshColor')
        rgb = scene.NMV_ApicalDendriteColor
        options.shading.mesh_spines_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_endfeet_color_option
####################################################################################################
def draw_endfeet_color_option(layout, scene, options, morphology):

    if morphology.has_endfeet():
        row = layout.row()
        row.prop(scene, 'NMV_EndfeetMeshColor')
        rgb = scene.NMV_EndfeetColor
        options.shading.mesh_endfeet_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_mesh_demo_color_options
####################################################################################################
def draw_mesh_demo_color_options(layout, scene, options):

    # Axons
    axons_color_row = layout.row()
    axons_color_row.prop(scene, 'NMV_AxonColor')

    # Apical dendrites
    basal_dendrites_color_row = layout.row()
    basal_dendrites_color_row.prop(scene, 'NMV_BasalDendritesColor')

    # Apical dendrites
    apical_dendrites_color_row = layout.row()
    apical_dendrites_color_row.prop(scene, 'NMV_ApicalDendriteColor')


####################################################################################################
# @draw_multi_component_mesh_color_options
####################################################################################################
def draw_multi_component_mesh_color_options(layout, scene, options, morphology):

    draw_soma_color_option(layout=layout, scene=scene, options=options)

    draw_axons_color_option(
        layout=layout, scene=scene, options=options, morphology=morphology)
    draw_basal_dendrites_color_option(
        layout=layout, scene=scene, options=options, morphology=morphology)
    draw_apical_dendrites_color_option(
        layout=layout, scene=scene, options=options, morphology=morphology)
    draw_spines_color_option(
        layout=layout, scene=scene, options=options, morphology=morphology)
    draw_endfeet_color_option(
        layout=layout, scene=scene, options=options, morphology=morphology)


####################################################################################################
# @draw_multi_component_mesh_color_options
####################################################################################################
def draw_single_component_mesh_color_options(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_NeuronMeshColor')
    rgb = scene.NMV_NeuronMeshColor
    options.shading.mesh_axons_color = Vector((rgb.r, rgb.g, rgb.b))

    # Affirm
    options.shading.mesh_soma_color = Vector((rgb.r, rgb.g, rgb.b))
    options.shading.mesh_axons_color = Vector((rgb.r, rgb.g, rgb.b))
    options.shading.mesh_basal_dendrites_color = Vector((rgb.r, rgb.g, rgb.b))
    options.shading.mesh_apical_dendrites_color = Vector((rgb.r, rgb.g, rgb.b))
    options.shading.mesh_spines_color = Vector((rgb.r, rgb.g, rgb.b))


####################################################################################################
# @draw_mesh_color_options
####################################################################################################
def draw_mesh_color_options(layout, scene, options, morphology):

    draw_mesh_colors_header(layout=layout)

    # The morphology must be loaded to be able to draw these options, otherwise draw demo
    if morphology is not None:

        draw_mesh_shading_option(layout=layout, scene=scene, options=options)

        if options.mesh.meshing_technique == nmv.enums.Meshing.Technique.WATERTIGHT:
            draw_single_component_mesh_color_options(
                layout=layout, scene=scene, options=options)
        elif options.mesh.meshing_technique == nmv.enums.Meshing.Technique.UNION:
            draw_single_component_mesh_color_options(
                layout=layout, scene=scene, options=options)
        elif options.mesh.meshing_technique == nmv.enums.Meshing.Technique.META_OBJECTS:
            draw_single_component_mesh_color_options(
                layout=layout, scene=scene, options=options)
        elif options.mesh.meshing_technique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
            draw_multi_component_mesh_color_options(
                layout=layout, scene=scene, options=options, morphology=morphology)
        elif options.mesh.meshing_technique == nmv.enums.Meshing.Technique.SKINNING:
            draw_multi_component_mesh_color_options(
                layout=layout, scene=scene, options=options, morphology=morphology)
        else:
            nmv.logger.log('UI_ERROR: draw_mesh_color_options')

    else:
        draw_mesh_demo_color_options(layout=layout, scene=scene, options=options)
