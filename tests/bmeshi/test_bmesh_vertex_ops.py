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
import unittest
import os
import sys 
sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))

# Blender imports 
from mathutils import Vector 

# Internal imports 
import nmv.bmeshi


####################################################################################################
# @BmeshVertexOpsTesting
####################################################################################################
class BmeshVertexOpsTesting(unittest.TestCase):

    def test_get_vertex_from_index(self):
        bmesh_object = nmv.bmeshi.create_vertex()
        bmesh_object.verts.ensure_lookup_table()
        self.assertTrue(bmesh_object.is_valid)

        vertex = nmv.bmeshi.get_vertex_from_index(bmesh_object=bmesh_object, vertex_index=0)
        self.assertTrue(vertex.is_valid)
        self.assertFalse(vertex.is_boundary)
        self.assertFalse(vertex.is_manifold)
        self.assertEqual(vertex.index, 0)
        self.assertEqual(vertex.co, Vector((0.0, 0.0, 0.0)))

    def test_extrude_vertex_towards_point(self):
        bmesh_object = nmv.bmeshi.create_vertex()
        bmesh_object.verts.ensure_lookup_table()
        self.assertTrue(bmesh_object.is_valid)

        target_point = Vector((1.0, 1.0, 1.0))
        extruded_vertex = nmv.bmeshi.extrude_vertex_towards_point(bmesh_object, index=0, point=target_point)  
        self.assertTrue(extruded_vertex.is_valid)
        self.assertFalse(extruded_vertex.is_boundary)
        self.assertFalse(extruded_vertex.is_manifold)
        self.assertEqual(extruded_vertex.index, 1)
        self.assertEqual(extruded_vertex.co, target_point)
