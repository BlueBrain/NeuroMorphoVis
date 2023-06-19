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
import nmv.mesh


####################################################################################################
# @MeshObjectTesting
####################################################################################################
class MeshObjectTesting(unittest.TestCase):

    def test_create_plane(self):
        mesh_object = nmv.mesh.create_plane(
            size=1, location=Vector((0.0, 0.0, 0.0)), name='plane')
        self.assertEqual(mesh_object.name, 'plane')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(len(mesh_object.data.vertices), 4)
        self.assertEqual(len(mesh_object.data.edges), 4)
        self.assertEqual(len(mesh_object.data.polygons), 1)
        self.assertEqual(mesh_object.data.polygons[0].area, 1.0)
        self.assertEqual(mesh_object.data.polygons[0].index, 0)
        self.assertEqual(mesh_object.data.polygons[0].center, Vector((0.0, 0.0, 0.0)))
        self.assertEqual(mesh_object.data.polygons[0].normal, Vector((0.0, 0.0, 1.0)))
        self.assertEqual(mesh_object.data.vertices[0].index, 0)
        self.assertEqual(mesh_object.data.vertices[1].index, 1)
        self.assertEqual(mesh_object.data.vertices[2].index, 2)
        self.assertEqual(mesh_object.data.vertices[3].index, 3)
        self.assertEqual(mesh_object.data.vertices[0].co, Vector((-0.5, -0.5, 0.0)))
        self.assertEqual(mesh_object.data.vertices[1].co, Vector((0.5, -0.5, 0.0)))
        self.assertEqual(mesh_object.data.vertices[2].co, Vector((-0.5, 0.5, 0.0)))
        self.assertEqual(mesh_object.data.vertices[3].co, Vector((0.5, 0.5, 0.0)))

    def test_create_ico_sphere(self):
        mesh_object = nmv.mesh.create_ico_sphere(
            radius=1, location=Vector((0.0, 0.0, 0.0)), subdivisions=1, name='ico_sphere')
        self.assertEqual(mesh_object.name, 'ico_sphere')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(len(mesh_object.data.vertices), 12)
        self.assertEqual(len(mesh_object.data.edges), 30)
        self.assertEqual(len(mesh_object.data.polygons), 20)

    def test_create_uv_sphere(self):
        mesh_object = nmv.mesh.create_uv_sphere(
            radius=1, location=(0, 0, 0), subdivisions=32, name='uv_sphere')
        self.assertEqual(mesh_object.name, 'uv_sphere')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(len(mesh_object.data.vertices), 482)
        self.assertEqual(len(mesh_object.data.edges), 992)
        self.assertEqual(len(mesh_object.data.polygons), 512)

    def test_create_circle(self):
        mesh_object = nmv.mesh.create_circle(
            radius=1, location=(0, 0, 0), vertices=4, caps=True, name='circle')
        self.assertEqual(mesh_object.name, 'circle')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(len(mesh_object.data.vertices), 4)
        self.assertEqual(len(mesh_object.data.edges), 4)
        self.assertEqual(len(mesh_object.data.polygons), 1)
        self.assertEqual(mesh_object.data.polygons[0].area, 2.0)
        self.assertEqual(mesh_object.data.polygons[0].index, 0)
        # self.assertEqual(mesh_object.data.polygons[0].center, Vector((0.0, 0.0, 0.0)))
        self.assertEqual(mesh_object.data.polygons[0].normal, Vector((0.0, 0.0, 1.0)))
    

    def test_create_bezier_circle(self):
        mesh_object = nmv.mesh.create_bezier_circle(
            radius=1, resolution=4, location=(0, 0, 0), name='bezier_circle')
        self.assertEqual(mesh_object.name, 'bezier_circle')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(mesh_object.type, 'CURVE')

    def test_create_cube(self):
        mesh_object = nmv.mesh.create_cube(radius=1, location=(0, 0, 0), name='cube')
        self.assertEqual(mesh_object.name, 'cube')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(len(mesh_object.data.vertices), 8)
        self.assertEqual(len(mesh_object.data.edges), 12)
        self.assertEqual(len(mesh_object.data.polygons), 6)

    def test_create_mesh_from_raw_data(self):
        verts = [Vector((-0.5, -0.5, 0.0)), Vector((0.5, -0.5, 0.0)), 
                 Vector((-0.5, 0.5, 0.0)), Vector((0.5, 0.5, 0.0))]
        faces = [[0, 1, 2, 3]]
        mesh_object = nmv.mesh.create_mesh_from_raw_data(
            verts, faces, edges=[], name='plane', collection_name="Collection")
        self.assertEqual(mesh_object.name, 'plane')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(len(mesh_object.data.vertices), 4)
        self.assertEqual(len(mesh_object.data.edges), 4)
        self.assertEqual(len(mesh_object.data.polygons), 1)
