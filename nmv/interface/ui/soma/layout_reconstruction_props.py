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

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @draw_morphology_reconstruction_header
####################################################################################################
def draw_soma_reconstruction_header(layout):

    row = layout.row()
    row.label(text='Reconstruction Options', icon='OUTLINER_OB_EMPTY')


####################################################################################################
# @draw_soma_reconstruction_technique_option
####################################################################################################
def draw_soma_reconstruction_technique_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_SomaReconstructionMethod', icon='FORCE_CURVE')
    options.soma.method = scene.NMV_SomaReconstructionMethod


####################################################################################################
# @draw_meta_ball_soma_resolution_option
####################################################################################################
def draw_meta_ball_soma_resolution_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_SomaMetaBallResolution')
    options.soma.meta_ball_resolution = scene.NMV_SomaMetaBallResolution


####################################################################################################
# @draw_meta_ball_soma_options
####################################################################################################
def draw_meta_ball_soma_options(layout, scene, options):

    draw_meta_ball_soma_resolution_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_soma_profile_options
####################################################################################################
def draw_soma_profile_options(layout, scene, options, morphology):

    row = layout.row()
    if len(morphology.soma.profile_points) > 0:
        row.prop(scene, 'NMV_SomaProfile')
        options.soma.profile = scene.NMV_SomaProfile
    else:
        row.prop(scene, 'NMV_SomaArborsOnlyProfile')
        options.soma.profile = scene.NMV_SomaArborsOnlyProfile


####################################################################################################
# @draw_simulation_steps_option
####################################################################################################
def draw_simulation_steps_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_SimulationSteps')
    options.soma.simulation_steps = scene.NMV_SimulationSteps


####################################################################################################
# @draw_soft_body_stiffness_option
####################################################################################################
def draw_soft_body_stiffness_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_Stiffness')
    options.soma.stiffness = scene.NMV_Stiffness


####################################################################################################
# @draw_soma_radius_scale_factor
####################################################################################################
def draw_soma_radius_scale_factor(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_SomaRadiusScaleFactor')
    options.soma.radius_scale_factor = scene.NMV_SomaRadiusScaleFactor


####################################################################################################
# @draw_ico_sphere_subdivision_level_option
####################################################################################################
def draw_ico_sphere_subdivision_level_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_SubdivisionLevel')
    options.soma.subdivision_level = scene.NMV_SubdivisionLevel


####################################################################################################
# @draw_soft_body_soma_options
####################################################################################################
def draw_soft_body_soma_options(layout, scene, options, morphology):

    draw_soma_profile_options(layout=layout, scene=scene, options=options, morphology=morphology)
    draw_simulation_steps_option(layout=layout, scene=scene, options=options)
    draw_soft_body_stiffness_option(layout=layout, scene=scene, options=options)
    draw_soma_radius_scale_factor(layout=layout, scene=scene, options=options)
    draw_ico_sphere_subdivision_level_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_hybrid_soma_options
####################################################################################################
def draw_hybrid_soma_options(layout, scene, options, morphology):

    draw_soma_profile_options(layout=layout, scene=scene, options=options, morphology=morphology)
    draw_simulation_steps_option(layout=layout, scene=scene, options=options)
    draw_soft_body_stiffness_option(layout=layout, scene=scene, options=options)
    draw_soma_radius_scale_factor(layout=layout, scene=scene, options=options)
    draw_ico_sphere_subdivision_level_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_soma_reconstruction_button
####################################################################################################
def draw_soma_reconstruction_button(layout, scene, options):

    row = layout.row(align=True)
    row.operator('nmv.reconstruct_soma', icon='FORCE_LENNARDJONES')

    # Soma simulation progress bar
    if options.soma.method == nmv.enums.Soma.Representation.SOFT_BODY:
        row = layout.row()
        row.prop(scene, 'NMV_SomaSimulationProgress')
        row.enabled = False

    if nmv.interface.ui_soma_reconstructed:
        row = layout.row()
        row.prop(scene, 'NMV_SomaReconstructionTime')
        row.enabled = False


####################################################################################################
# @draw_morphology_reconstruction_options
####################################################################################################
def draw_soma_reconstruction_options(panel, scene, options, morphology):

    draw_soma_reconstruction_header(layout=panel.layout)
    draw_soma_reconstruction_technique_option(layout=panel.layout, scene=scene, options=options)

    if options.soma.method == nmv.enums.Soma.Representation.META_BALLS:
        draw_meta_ball_soma_options(
            layout=panel.layout, scene=scene, options=options)
    elif options.soma.method == nmv.enums.Soma.Representation.SOFT_BODY:
        draw_soft_body_soma_options(
            layout=panel.layout, scene=scene, options=options, morphology=morphology)
    elif options.soma.method == nmv.enums.Soma.Representation.HYBRID:
        draw_hybrid_soma_options(
            layout=panel.layout, scene=scene, options=options, morphology=morphology)
    else:
        nmv.logger.log('UI_ERROR: draw_soma_reconstruction_options')

