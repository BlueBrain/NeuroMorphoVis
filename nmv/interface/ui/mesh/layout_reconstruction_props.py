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
# @draw_mesh_reconstruction_header
####################################################################################################
def draw_mesh_reconstruction_header(layout):

    row = layout.row()
    row.label(text='Mesh Reconstruction Options', icon='SURFACE_DATA')


####################################################################################################
# @draw_meshing_technique_option
####################################################################################################
def draw_meshing_technique_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_MeshingTechnique', icon='OUTLINER_OB_EMPTY')
    options.mesh.meshing_technique = scene.NMV_MeshingTechnique


####################################################################################################
# @draw_soma_type_option
####################################################################################################
def draw_soma_type_option(layout, scene, options):

    row = layout.row()
    row.label(text='Soma:')
    row.prop(scene, 'NMV_MeshingSomaType', expand=True)
    options.mesh.soma_type = scene.NMV_MeshingSomaType


####################################################################################################
# @draw_meta_soma_option
####################################################################################################
def draw_meta_soma_option(layout, scene, options):

    row = layout.row()
    row.label(text='Soma:')
    row.prop(scene, 'NMV_MeshingMetaSoma', expand=True)
    options.mesh.soma_type = scene.NMV_MeshingMetaSoma


####################################################################################################
# @draw_mesh_edges_option
####################################################################################################
def draw_mesh_edges_option(layout, scene, options):

    row = layout.row()
    row.label(text='Edges:')
    row.prop(scene, 'NMV_MeshSmoothing', expand=True)
    options.mesh.edges = scene.NMV_MeshSmoothing


####################################################################################################
# @draw_small_edges_removal_option
####################################################################################################
def draw_small_edges_removal_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_RemoveSmallEdges', expand=True)
    options.mesh.remove_small_edges = scene.NMV_RemoveSmallEdges


####################################################################################################
# @draw_mesh_surface_roughness_option
####################################################################################################
def draw_mesh_surface_roughness_option(layout, scene, options):

    row = layout.row()
    row.label(text='Surface:')
    row.prop(scene, 'NMV_SurfaceRoughness', expand=True)
    options.mesh.surface = scene.NMV_SurfaceRoughness


####################################################################################################
# @draw_mesh_connectivity_options
####################################################################################################
def draw_mesh_connectivity_options(layout, scene, options):

    row = layout.row()
    row.label(text='Mesh Objects:')
    row.prop(scene, 'NMV_MeshObjectsConnection', expand=True)
    options.mesh.neuron_objects_connection = scene.NMV_MeshObjectsConnection


####################################################################################################
# @draw_proxy_mesh_option
####################################################################################################
def draw_proxy_mesh_option(layout, scene, options):

    row = layout.row()
    row.label(text='Proxy Mesh')
    row.prop(scene, 'NMV_ProxyMeshes', expand=True)
    options.mesh.proxy_mesh_method = scene.NMV_ProxyMeshes


####################################################################################################
# @draw_tessellation_option
####################################################################################################
def draw_tessellation_option(layout, scene, options):

    tess_level_row = layout.row()
    tess_level_row.prop(scene, 'NMV_TessellateMesh')
    tess_level_column = tess_level_row.column()
    tess_level_column.prop(scene, 'NMV_MeshTessellationLevel')

    # Disable the tessellation
    if not scene.NMV_TessellateMesh:
        options.mesh.tessellate_mesh = False
        options.mesh.tessellation_level = 1.0
        tess_level_column.enabled = False
    else:
        options.mesh.tessellate_mesh = scene.NMV_TessellateMesh
        options.mesh.tessellation_level = scene.NMV_MeshTessellationLevel


####################################################################################################
# @draw_spine_options_header
####################################################################################################
def draw_spine_options_header(layout):

    row = layout.row()
    row.label(text='Spine Options', icon='MOD_WAVE')


####################################################################################################
# @draw_spines_source_option
####################################################################################################
def draw_spines_source_option(layout, scene, options):

    # If the input neuron is from a circuit, show the circuit options, otherwise use random spines
    row = layout.row()
    row.label(text='Source:')

    if scene.NMV_InputSource == nmv.enums.Input.CIRCUIT_GID:
        row.prop(scene, 'NMV_SpinesSourceCircuit', expand=True)
        options.mesh.spines = scene.NMV_SpinesSourceCircuit
    else:
        row.prop(scene, 'NMV_SpinesSourceRandom', expand=True)
        options.mesh.spines = scene.NMV_SpinesSourceRandom


####################################################################################################
# @draw_spines_percentage_option
####################################################################################################
def draw_spines_percentage_option(layout, scene, options):

    if options.mesh.spines == nmv.enums.Meshing.Spines.Source.RANDOM:
        row = layout.row()
        row.label(text='Random Density:')
        row.prop(scene, 'NMV_NumberSpinesPerMicron')
        options.mesh.number_spines_per_micron = scene.NMV_NumberSpinesPerMicron


####################################################################################################
# @draw_spines_options
####################################################################################################
def draw_spines_options(layout, scene, options):

    draw_spine_options_header(layout=layout)
    draw_spines_source_option(layout=layout, scene=scene, options=options)
    draw_spines_percentage_option(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_piecewise_watertight_meshing_options
####################################################################################################
def draw_piecewise_watertight_meshing_options(layout, scene, options):

    draw_soma_type_option(layout=layout, scene=scene, options=options)
    draw_mesh_connectivity_options(layout=layout, scene=scene, options=options)
    draw_tessellation_option(layout=layout, scene=scene, options=options)
    draw_spines_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_voxelization_meshing_options
####################################################################################################
def draw_voxelization_meshing_options(layout, scene, options):

    draw_soma_type_option(layout=layout, scene=scene, options=options)
    draw_proxy_mesh_option(layout=layout, scene=scene, options=options)
    draw_mesh_surface_roughness_option(layout=layout, scene=scene, options=options)
    draw_small_edges_removal_option(layout=layout, scene=scene, options=options)
    draw_spines_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_skinning_meshing_options
####################################################################################################
def draw_skinning_meshing_options(layout, scene, options):

    draw_soma_type_option(layout=layout, scene=scene, options=options)
    draw_mesh_connectivity_options(layout=layout, scene=scene, options=options)
    draw_mesh_surface_roughness_option(layout=layout, scene=scene, options=options)
    draw_tessellation_option(layout=layout, scene=scene, options=options)
    draw_spines_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_union_operators_meshing_options
####################################################################################################
def draw_union_operators_meshing_options(layout, scene, options):

    draw_meta_soma_option(layout=layout, scene=scene, options=options)
    draw_mesh_edges_option(layout=layout, scene=scene, options=options)
    draw_mesh_surface_roughness_option(layout=layout, scene=scene, options=options)
    draw_tessellation_option(layout=layout, scene=scene, options=options)
    draw_spines_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_meta_objects_meshing_options
####################################################################################################
def draw_meta_objects_meshing_options(layout, scene, options):

    draw_meta_soma_option(layout=layout, scene=scene, options=options)
    draw_mesh_surface_roughness_option(layout=layout, scene=scene, options=options)
    draw_small_edges_removal_option(layout=layout, scene=scene, options=options)
    draw_tessellation_option(layout=layout, scene=scene, options=options)
    draw_spines_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @draw_mesh_reconstruction_options
####################################################################################################
def draw_mesh_reconstruction_options(panel, scene, options, morphology):

    draw_mesh_reconstruction_header(layout=panel.layout)
    draw_meshing_technique_option(layout=panel.layout, scene=scene, options=options)

    if options.mesh.meshing_technique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
        draw_piecewise_watertight_meshing_options(layout=panel.layout, scene=scene, options=options)

    elif options.mesh.meshing_technique == nmv.enums.Meshing.Technique.VOXELIZATION:
        draw_voxelization_meshing_options(layout=panel.layout, scene=scene, options=options)

    elif options.mesh.meshing_technique == nmv.enums.Meshing.Technique.SKINNING:
        draw_skinning_meshing_options(layout=panel.layout, scene=scene, options=options)

    elif options.mesh.meshing_technique == nmv.enums.Meshing.Technique.UNION:
        draw_union_operators_meshing_options(layout=panel.layout, scene=scene, options=options)

    elif options.mesh.meshing_technique == nmv.enums.Meshing.Technique.META_OBJECTS:
        draw_meta_objects_meshing_options(layout=panel.layout, scene=scene, options=options)

    else:
        nmv.logger.log('UI_ERROR: draw_mesh_reconstruction_options')

