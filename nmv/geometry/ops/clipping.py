####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

import mathutils
import bpy
import bmesh


####################################################################################################
# @clip_curve_object
####################################################################################################
def clip_curve_object(curve_object, pmin, pmax):
    
    # Must be a curve 
    if curve_object.type != 'CURVE':
        return 
    
    def in_bounds(p):
        return all(pmin[i] <= p[i] <= pmax[i] for i in range(3))
    
    # Ensure that the bounds are vectors, not tuples 
    pmin = mathutils.Vector(pmin)
    pmax = mathutils.Vector(pmax)
    
    # Get the data 
    curve_data = curve_object.data
    splines_to_replace = []
    
    # Validate the splines 
    for spline in curve_data.splines:
        if spline.type != 'POLY':
            continue
        
        # Keep both co and radius
        filtered_points = [
            (p.co.copy(), p.radius) for p in spline.points if in_bounds(p.co.xyz)]

        if len(filtered_points) < 2:
            splines_to_replace.append((spline, None))
        else:
            splines_to_replace.append((spline, filtered_points))
    
    # Replace old splines
    for spline, points in splines_to_replace:
        curve_data.splines.remove(spline)
        if points is None:
            continue

        new_spline = curve_data.splines.new('POLY')
        new_spline.points.add(len(points) - 1)
        for i, (co, radius) in enumerate(points):
            new_spline.points[i].co = (co.x, co.y, co.z, 1.0)
            new_spline.points[i].radius = radius


####################################################################################################
# @clip_mesh_object
####################################################################################################
def clip_mesh_object(mesh_object, pmin, pmax):
    
    # Must be a mesh 
    if mesh_object.type != 'MESH':
        return 
    # Ensure that the bounds are vectors, not tuples 
    pmin = mathutils.Vector(pmin)
    pmax = mathutils.Vector(pmax)

    def in_bounds(v):
        return all(pmin[i] <= v.co[i] <= pmax[i] for i in range(3))

    # Enter edit mode with BMesh for safe in-place editing
    bpy.context.view_layer.objects.active = mesh_object
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(mesh_object.data)
    
    # Tag vertices that are outside bounds
    for v in bm.verts:
        v.tag = not in_bounds(v)

    # Delete faces where any vertex is tagged (outside bounds)
    faces_to_delete = [f for f in bm.faces if any(v.tag for v in f.verts)]
    bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')

    # Delete now-unused vertices that are tagged
    unused_verts = [v for v in bm.verts if v.tag and len(v.link_faces) == 0]
    bmesh.ops.delete(bm, geom=unused_verts, context='VERTS')

    # Update and exit edit mode
    bmesh.update_edit_mesh(mesh_object.data)
    bpy.ops.object.mode_set(mode='OBJECT')


####################################################################################################
# @clip_mesh_object
####################################################################################################
def clip_objects(objects, pmin, pmax):
    
    for i_object in objects: 
        if i_object.type == 'CURVE':
            clip_curve_object(i_object, pmin, pmax)
        elif i_object.type == 'MESH':
            clip_mesh_object(i_object, pmin, pmax)
        else:
            continue # Skip unsupported object types