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

# System imports 
import unittest
import os
import sys 
sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))

# Blender imports 
from mathutils import Vector 

# Internal imports 
import nmv.bmeshi
import input_data

####################################################################################################
# @BmeshObjectsTesting
####################################################################################################
class BmeshObjectsTesting(unittest.TestCase):

    def test_create_vertex(self):
        for location in input_data.get_exact_locations():
            bmesh_object = nmv.bmeshi.create_vertex(location=location)
            bmesh_object.verts.ensure_lookup_table()
            
            self.assertTrue(bmesh_object.is_valid)
            self.assertEqual(bmesh_object.verts[0].co, location)
            self.assertEqual(len(bmesh_object.verts), 1)
            self.assertEqual(len(bmesh_object.faces), 0)
        
    def test_create_uv_sphere(self):
        for location in input_data.get_exact_locations():
            bmesh_object = nmv.bmeshi.create_uv_sphere(location=location)
            bmesh_object.verts.ensure_lookup_table()

            self.assertTrue(bmesh_object.is_valid)
            self.assertEqual(len(bmesh_object.verts), 92)
            self.assertEqual(len(bmesh_object.faces), 100)

    def test_create_ico_sphere(self):
        for location in input_data.get_exact_locations():
            bmesh_object = nmv.bmeshi.create_ico_sphere(location=location)
            bmesh_object.verts.ensure_lookup_table()

            self.assertTrue(bmesh_object.is_valid)
            self.assertEqual(len(bmesh_object.verts), 12)
            self.assertEqual(len(bmesh_object.faces), 20)

    def test_create_circle(self):
        for location in input_data.get_exact_locations():
            bmesh_object = nmv.bmeshi.create_circle(location=location)
            bmesh_object.verts.ensure_lookup_table()

            self.assertTrue(bmesh_object.is_valid)
            self.assertEqual(len(bmesh_object.verts), 4)
            self.assertEqual(len(bmesh_object.faces), 1)

    def test_create_cube(self):
        for location in input_data.get_exact_locations():
            bmesh_object = nmv.bmeshi.create_cube(location=location)
            bmesh_object.verts.ensure_lookup_table()

            self.assertTrue(bmesh_object.is_valid)
            self.assertEqual(len(bmesh_object.verts), 8)
            self.assertEqual(len(bmesh_object.faces), 6)