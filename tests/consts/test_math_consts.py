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
# @MathConstsTesting
####################################################################################################
class MathConstsTesting(unittest.TestCase):

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