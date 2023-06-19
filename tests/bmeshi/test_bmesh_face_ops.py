####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import unittest
import os
import sys 
sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))

# Blender imports 
from mathutils import Vector 

# Internal imports 
import nmv.bmeshi


####################################################################################################
# @BmeshFaceOpsTesting
####################################################################################################
class BmeshFaceOpsTesting(unittest.TestCase):

    def test_get_face_from_index(self):
        bmesh_object = nmv.bmeshi.create_cube()
        bmesh_object.verts.ensure_lookup_table()
        self.assertTrue(bmesh_object.is_valid)

        face = nmv.bmeshi.get_face_from_index(bmesh_object=bmesh_object, face_index=0)
        self.assertTrue(face.is_valid)
        self.assertEqual(face.index, 0)
        self.assertEqual(len(face.verts), 4)
        self.assertEqual(len(face.edges), 4)
        self.assertEqual(face.normal, Vector((-1.0, -0.0, 0.0)))
        self.assertEqual(face.calc_area(), 1.0)
        self.assertEqual(face.calc_center_bounds(), Vector((-0.5, 0.0, 0.0)))
        self.assertEqual(face.calc_center_median(), Vector((-0.5, 0.0, 0.0)))
        self.assertEqual(face.calc_center_median_weighted(), Vector((-0.5, 0.0, 0.0)))
        self.assertEqual(face.calc_perimeter(), 4.0)
        self.assertEqual(face.calc_tangent_edge(), Vector((0.0, 1.0, 0.0)))
        self.assertEqual(face.calc_tangent_edge_diagonal(), Vector((0.0, 0.0, -1.0)))
        self.assertEqual(face.calc_tangent_edge_pair(), Vector((0.0, 0.0, -2.0)))
        self.assertEqual(face.calc_tangent_vert_diagonal(), 
            Vector((0.0, -0.7071067690849304, -0.7071067690849304)))

    def test_get_nearest_face_index(self):
        bmesh_object = nmv.bmeshi.create_cube()
        bmesh_object.verts.ensure_lookup_table()
        self.assertTrue(bmesh_object.is_valid)

        face_index = nmv.bmeshi.get_nearest_face_index(
            bmesh_object=bmesh_object, point=Vector((-0.55, 0.0, 0.0)))
        self.assertEqual(face_index, 0)

    def test_get_nearest_vertex_index_to_point(self):
        bmesh_object = nmv.bmeshi.create_cube()
        bmesh_object.verts.ensure_lookup_table()
        self.assertTrue(bmesh_object.is_valid)

        vertex_index = nmv.bmeshi.get_nearest_vertex_index_to_point(
            bmesh_object=bmesh_object, point=Vector((-0.45, -0.5, -0.65)))
        self.assertEqual(vertex_index, 0)
        
        vertex_index = nmv.bmeshi.get_nearest_vertex_index_to_point(
            bmesh_object=bmesh_object, point=Vector((0.45, 0.5, 0.65)))
        self.assertEqual(vertex_index, 7)

    def test_get_nearest_face_index_from_list(self):
        bmesh_object = nmv.bmeshi.create_cube()
        self.assertTrue(bmesh_object.is_valid)
        bmesh_object.verts.ensure_lookup_table()
        bmesh_object.faces.ensure_lookup_table()
        
        faces_indices_list = [0, 1, 2, 3, 4, 5]
        face_index = nmv.bmeshi.get_nearest_face_index_from_list(
            bmesh_object=bmesh_object, point=Vector((0.45, 0.5, 0.65)), faces_indices=faces_indices_list)
        self.assertEqual(face_index, 5)