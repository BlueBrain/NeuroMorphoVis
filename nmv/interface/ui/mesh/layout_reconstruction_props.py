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
    row.label(text='Soma')
    row.prop(scene, 'NMV_MeshingSomaType', expand=True)
    options.mesh.soma_type = scene.NMV_MeshingSomaType


####################################################################################################
# @draw_meta_soma_option
####################################################################################################
def draw_meta_soma_option(layout, scene, options):

    row = layout.row()
    row.label(text='Soma')
    row.prop(scene, 'NMV_MeshingMetaSoma', expand=True)
    options.mesh.soma_type = scene.NMV_MeshingMetaSoma


####################################################################################################
# @draw_meshing_technique_option
####################################################################################################
def draw_mesh_smoothing_option(layout, scene, options):

    row = layout.row()
    row.label(text='Edges')
    row.prop(scene, 'NMV_MeshSmoothing', expand=True)
    options.mesh.edges = scene.NMV_MeshSmoothing


def draw_mesh_surface_roughness_option(layout, scene, options):

    row = layout.row()
    row.label(text='Surface:')
    row.prop(scene, 'NMV_SurfaceRoughness', expand=True)
    options.mesh.surface = scene.NMV_SurfaceRoughness

def draw_mesh_connectivity_options(layout, scene, options):

    row = layout.row()
    row.label(text='Skeleton Objects:')
    row.prop(scene, 'NMV_MeshObjectsConnection', expand=True)
    options.mesh.neuron_objects_connection = scene.NMV_MeshObjectsConnection


def draw_piecewise_watertight_meshing_options(layout, scene, options):

    draw_soma_type_option(layout=layout, scene=scene, options=options)
    draw_mesh_connectivity_options(layout=layout, scene=scene, options=options)


def draw_voxelization_meshing_options(layout, scene, options):

    draw_soma_type_option(layout=layout, scene=scene, options=options)
    draw_mesh_surface_roughness_option(layout=layout, scene=scene, options=options)


def draw_skinning_meshing_options(layout, scene, options):

    draw_soma_type_option(layout=layout, scene=scene, options=options)
    draw_mesh_connectivity_options(layout=layout, scene=scene, options=options)
    draw_mesh_surface_roughness_option(layout=layout, scene=scene, options=options)


def draw_union_operators_meshing_options(layout, scene, options):

    draw_meta_soma_option(layout=layout, scene=scene, options=options)
    draw_mesh_surface_roughness_option(layout=layout, scene=scene, options=options)


def draw_meta_objects_meshing_options(layout, scene, options):

    draw_meta_soma_option(layout=layout, scene=scene, options=options)
    draw_mesh_surface_roughness_option(layout=layout, scene=scene, options=options)


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

