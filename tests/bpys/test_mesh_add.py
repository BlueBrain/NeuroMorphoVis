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
import nmv.bpys
import nmv.consts

####################################################################################################
# @bpyMeshAddTesting
####################################################################################################
class bpyMeshAddTesting(unittest.TestCase):

    ################################################################################################
    # @test_add_plane_mesh
    ################################################################################################
    def test_add_plane_mesh(self):
        nmv.bpys.add_plane_mesh()
        mesh_object = nmv.bpys.get_active_object()
        self.assertEqual(mesh_object.name, 'Plane')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(mesh_object.location, Vector((0.0, 0.0, 0.0)))
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
        nmv.bpys.delete_selected_object()

    ################################################################################################
    # @test_add_ico_sphere_mesh
    ################################################################################################
    def test_add_ico_sphere_mesh(self):
        nmv.bpys.add_ico_sphere_mesh()
        mesh_object = nmv.bpys.get_active_object()
        self.assertEqual(mesh_object.name, 'Icosphere')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(mesh_object.location, Vector((0.0, 0.0, 0.0)))
        self.assertEqual(len(mesh_object.data.vertices), 42)
        self.assertEqual(len(mesh_object.data.edges), 120)
        self.assertEqual(len(mesh_object.data.polygons), 80)
        nmv.bpys.delete_selected_object()

    ################################################################################################
    # @test_add_uv_sphere_mesh
    ################################################################################################
    def test_add_uv_sphere_mesh(self):
        nmv.bpys.add_uv_sphere_mesh()
        mesh_object = nmv.bpys.get_active_object()
        self.assertEqual(mesh_object.name, 'Sphere')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(mesh_object.location, Vector((0.0, 0.0, 0.0)))
        self.assertEqual(len(mesh_object.data.vertices), 242)
        self.assertEqual(len(mesh_object.data.edges), 496)
        self.assertEqual(len(mesh_object.data.polygons), 256)
        nmv.bpys.delete_selected_object()

    ################################################################################################
    # @test_add_circle_mesh
    ################################################################################################
    def test_add_circle_mesh(self):
        nmv.bpys.add_circle_mesh()
        mesh_object = nmv.bpys.get_active_object()
        self.assertEqual(mesh_object.name, 'Circle')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(mesh_object.location, Vector((0.0, 0.0, 0.0)))
        self.assertEqual(len(mesh_object.data.vertices), 8)
        self.assertEqual(len(mesh_object.data.edges), 8)
        self.assertEqual(len(mesh_object.data.polygons), 0)
        nmv.bpys.delete_selected_object()

    ################################################################################################
    # @test_add_cube_mesh
    ################################################################################################
    def test_add_cube_mesh(self):
        nmv.bpys.add_cube_mesh()
        mesh_object = nmv.bpys.get_active_object()
        self.assertEqual(mesh_object.name, 'Cube')
        self.assertFalse(mesh_object.data.is_editmode)
        self.assertEqual(mesh_object.location, Vector((0.0, 0.0, 0.0)))
        self.assertEqual(len(mesh_object.data.vertices), 8)
        self.assertEqual(len(mesh_object.data.edges), 12)
        self.assertEqual(len(mesh_object.data.polygons), 6)
        nmv.bpys.delete_selected_object()