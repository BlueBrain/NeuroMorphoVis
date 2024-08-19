####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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

####################################################################################################
# @mesh_reveal
####################################################################################################
def mesh_reveal():
    bpy.ops.mesh.reveal()


####################################################################################################
# @mesh_select_all
####################################################################################################
def mesh_select_all():
    bpy.ops.mesh.select_all(action='SELECT')


####################################################################################################
# @mesh_deselect_all
####################################################################################################
def mesh_deselect_all():
    bpy.ops.mesh.select_all(action='DESELECT')


####################################################################################################
# @mesh_remove_doubles
####################################################################################################
def mesh_remove_doubles(threshold=0.0001):
    bpy.ops.mesh.remove_doubles(threshold=threshold)


####################################################################################################
# @mesh_delete_lose
####################################################################################################
def mesh_delete_lose(use_verts=True, use_edges=True, use_faces=True):
    bpy.ops.mesh.delete_loose(use_verts=use_verts, use_edges=use_edges, use_faces=use_faces)


####################################################################################################
# @mesh_select_interior_faces
####################################################################################################
def mesh_select_interior_faces():
    bpy.ops.mesh.select_interior_faces()


####################################################################################################
# @mesh_dissolve_degenerate
####################################################################################################
def mesh_dissolve_degenerate(threshold):
    bpy.ops.mesh.dissolve_degenerate(threshold=threshold)


####################################################################################################
# @mesh_normals_make_consistent
####################################################################################################
def mesh_normals_make_consistent():
    bpy.ops.mesh.normals_make_consistent()


####################################################################################################
# @mesh_fill_holes
####################################################################################################
def mesh_fill_holes(sides):
    bpy.ops.mesh.fill_holes(sides=sides)


####################################################################################################
# @mesh_delete_selected_vertices
####################################################################################################
def mesh_delete_selected_vertices():
    bpy.ops.mesh.delete(type='VERT')


####################################################################################################
# @mesh_delete_selected_faces
####################################################################################################
def mesh_delete_selected_faces():
    bpy.ops.mesh.delete(type='FACE')


####################################################################################################
# @mesh_extrude_region_move
####################################################################################################
def mesh_extrude_region_move(delta):
    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region={"mirror": False},
        TRANSFORM_OT_translate={"value": delta})

####################################################################################################
# @mesh_subdivide
####################################################################################################
def mesh_subdivide(number_cuts,
                   smoothness=0):
    bpy.ops.mesh.subdivide(number_cuts=number_cuts, smoothness=smoothness)


####################################################################################################
# @mesh_edge_face_add
####################################################################################################
def mesh_edge_face_add():
    bpy.ops.mesh.edge_face_add()


