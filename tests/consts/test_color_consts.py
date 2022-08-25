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
class ColorConstsTesting(unittest.TestCase):

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
        