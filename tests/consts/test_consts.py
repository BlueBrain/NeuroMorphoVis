####################################################################################################
# Copyright (c) 2016 - 2022, EPFL / Blue Brain Project
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

# System imports 
import unittest
import os
import sys 
sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))

# Blender imports 
from mathutils import Vector 

# Internal imports 
import nmv.consts


####################################################################################################
# @ColorConstsTesting
####################################################################################################
class ConstsTesting(unittest.TestCase):

    def test_color_consts(self):
        self.assertEqual(nmv.consts.Color.RED, Vector((1.0, 0.0, 0.0)))
        self.assertEqual(nmv.consts.Color.GREEN, Vector((0.0, 1.0, 0.0)))
        self.assertEqual(nmv.consts.Color.BLUE,  Vector((0.0, 0.0, 1.0)))
        self.assertEqual(nmv.consts.Color.WHITE, Vector((1.0, 1.0, 1.0)))
        self.assertEqual(nmv.consts.Color.VERY_WHITE, Vector((10.0, 10.0, 10.0)))
        self.assertEqual(nmv.consts.Color.GRAY, Vector((0.5, 0.5, 0.5)))
        self.assertEqual(nmv.consts.Color.GREYSH, Vector((0.9, 0.9, 0.9)))
        self.assertEqual(nmv.consts.Color.MATT_BLACK, Vector((0.1, 0.1, 0.1)))
        self.assertEqual(nmv.consts.Color.BLACK, Vector((0.0, 0.0, 0.0)))
        self.assertEqual(nmv.consts.Color.COLORMAP_RESOLUTION, 16)

    def test_dendrogram_consts(self):
        self.assertEqual(nmv.consts.Dendrogram.DELTA_SCALE_FACTOR, 8.0)
        self.assertEqual(nmv.consts.Dendrogram.ARBOR_CONST_RADIUS, 1.0)
        
    def test_math_consts(self):
        self.assertEqual(nmv.consts.Math.INFINITY, 1e30)
        self.assertEqual(nmv.consts.Math.MINUS_INFINITY, -1e30)
        self.assertEqual(nmv.consts.Math.EPSILON, 0.99)
        self.assertEqual(nmv.consts.Math.LITTLE_EPSILON, 1e-5)
        self.assertEqual(nmv.consts.Math.ORIGIN, Vector((0.0, 0.0, 0.0)))
        self.assertEqual(nmv.consts.Math.X_AXIS, Vector((1.0, 0.0, 0.0)))
        self.assertEqual(nmv.consts.Math.Y_AXIS, Vector((0.0, 1.0, 0.0)))
        self.assertEqual(nmv.consts.Math.Z_AXIS, Vector((0.0, 0.0, 1.0)))
        self.assertEqual(nmv.consts.Math.INDEX_OUT_OF_RANGE, -1)

    def test_softbody_consts(self):
        self.assertEqual(nmv.consts.SoftBody.GRAVITY, 0.0)
        self.assertEqual(nmv.consts.SoftBody.GOAL_MAX, 0.1)
        self.assertEqual(nmv.consts.SoftBody.GOAL_MIN, 0.7)
        self.assertEqual(nmv.consts.SoftBody.GOAL_DEFAULT, 0.5)
        self.assertEqual(nmv.consts.SoftBody.SUBDIVISIONS_DEFAULT, 5)
        self.assertEqual(nmv.consts.SoftBody.SIMULATION_STEPS_DEFAULT, 100)
        self.assertEqual(nmv.consts.SoftBody.STIFFNESS_DEFAULT, 0.1)
        self.assertEqual(nmv.consts.SoftBody.SOMA_SCALE_FACTOR, 0.5)

    def test_spines_consts(self):
        self.assertEqual(nmv.consts.Spines.MIN_SCALE_FACTOR, 0.5)
        self.assertEqual(nmv.consts.Spines.MAX_SCALE_FACTOR, 1.25)

    def test_suffix_consts(self):
        self.assertIs(nmv.consts.Suffix.SOMA_FRONT, '_soma_front')
        self.assertIs(nmv.consts.Suffix.SOMA_SIDE, '_soma_side')
        self.assertIs(nmv.consts.Suffix.SOMA_TOP, '_soma_top')
        self.assertIs(nmv.consts.Suffix.SOMA_360, '_soma_360')
        self.assertIs(nmv.consts.Suffix.SOMA_PROGRESSIVE, '_soma_progressive')
        self.assertIs(nmv.consts.Suffix.MORPHOLOGY, '_morphology')
        self.assertIs(nmv.consts.Suffix.MORPHOLOGY_FRONT, '_morphology_front')
        self.assertIs(nmv.consts.Suffix.MORPHOLOGY_SIDE, '_morphology_side')
        self.assertIs(nmv.consts.Suffix.MORPHOLOGY_TOP, '_morphology_top')
        self.assertIs(nmv.consts.Suffix.MORPHOLOGY_360, '_morphology_360')
        self.assertIs(nmv.consts.Suffix.MORPHOLOGY_PROGRESSIVE, '_morphology_progressive')
        self.assertIs(nmv.consts.Suffix.MESH_FRONT, '_mesh_front')
        self.assertIs(nmv.consts.Suffix.MESH_SIDE, '_mesh_side')
        self.assertIs(nmv.consts.Suffix.MESH_TOP, '_mesh_top')
        self.assertIs(nmv.consts.Suffix.MESH_360, '_mesh_360')
        self.assertIs(nmv.consts.Suffix.FIXED_RADIUS, '_fixed_radius')