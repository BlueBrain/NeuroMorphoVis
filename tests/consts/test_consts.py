####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
# @ConstsTesting
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
    
    def test_meshing_consts(self):
        self.assertEqual(nmv.consts.Meshing.MIN_TESSELLATION_LEVEL, 0.1)
        self.assertEqual(nmv.consts.Meshing.MAX_TESSELLATION_LEVEL, 1.0)
        self.assertEqual(nmv.consts.Meshing.BEVEL_OBJECT_SIDES, 16)
        self.assertEqual(nmv.consts.Meshing.NUMBER_SPINES_PER_MICRON, 2)
        self.assertEqual(nmv.consts.Meshing.PLY_EXTENSION, '.ply')
        self.assertEqual(nmv.consts.Meshing.OBJ_EXTENSION, '.obj')
        self.assertEqual(nmv.consts.Meshing.STL_EXTENSION, '.stl')
        self.assertEqual(nmv.consts.Meshing.BLEND_EXTENSION, '.blend')
        
    def test_metaball_consts(self):
        self.assertEqual(nmv.consts.MetaBall.SOMA_META_DEFAULT_RESOLUTION, 0.99)
        self.assertEqual(nmv.consts.MetaBall.META_DEFAULT_RESOLUTION, 0.99)

    def test_morphology_consts(self):
        self.assertEqual(nmv.consts.Morphology.ORIGIN_SAMPLE_RADIUS, 0.1)
        self.assertEqual(nmv.consts.Morphology.FIRST_SAMPLE_RADIUS, 0.1)
        self.assertEqual(nmv.consts.Morphology.LAST_SAMPLE_RADIUS, 0.05)
        self.assertEqual(nmv.consts.Morphology.FIRST_SAMPLE_RADIUS_SCALE_FACTOR, 0.5)
        self.assertEqual(nmv.consts.Morphology.LAST_SAMPLE_RADIUS_SCALE_FACTOR, 0.5)

    def test_simulation_consts(self):
        self.assertEqual(nmv.consts.Simulation.MIN_FRAME, 0)
        self.assertEqual(nmv.consts.Simulation.MAX_FRAME, 200)

    def test_skeleton_consts(self):
        self.assertEqual(nmv.consts.Skeleton.MAX_BRANCHING_ORDER, 1000)
        self.assertEqual(nmv.consts.Skeleton.AXON_DEFAULT_BRANCHING_ORDER, 2)
        self.assertEqual(nmv.consts.Skeleton.MAXIMUM_SOMA_RADIUS_REPORTED, 30)
        self.assertEqual(nmv.consts.Skeleton.SOMA_PREFIX, 'Soma')
        self.assertEqual(nmv.consts.Skeleton.AXON_PREFIX, 'Axon')
        self.assertEqual(nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX, 'BasalDendrite')
        self.assertEqual(nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX, 'ApicalDendrite')
        self.assertEqual(nmv.consts.Skeleton.SOMA_EXTRUSION_DELTA, 0.7)
        self.assertEqual(nmv.consts.Skeleton.ARBOR_EXTRUSION_DELTA, 0.2)
        self.assertEqual(nmv.consts.Skeleton.N_SAMPLES_ROOT_TO_ORIGIN, 5)
        self.assertEqual(nmv.consts.Skeleton.SWC_SAMPLE_INDEX_IDX, 0)
        self.assertEqual(nmv.consts.Skeleton.SWC_SAMPLE_TYPE_IDX, 1)
        self.assertEqual(nmv.consts.Skeleton.SWC_SAMPLE_X_COORDINATES_IDX, 2)
        self.assertEqual(nmv.consts.Skeleton.SWC_SAMPLE_Y_COORDINATES_IDX, 3)
        self.assertEqual(nmv.consts.Skeleton.SWC_SAMPLE_Z_COORDINATES_IDX, 4)
        self.assertEqual(nmv.consts.Skeleton.SWC_SAMPLE_RADIUS_IDX, 5)
        self.assertEqual(nmv.consts.Skeleton.SWC_SAMPLE_PARENT_INDEX_IDX, 6)
        self.assertEqual(nmv.consts.Skeleton.SWC_SAMPLE_PARENT_INDEX_IDX, 6)
        self.assertEqual(nmv.consts.Skeleton.SWC_NO_PARENT_SAMPLE_TYPE, -1)
        self.assertEqual(nmv.consts.Skeleton.SWC_UNDEFINED_SAMPLE_TYPE, 0)
        self.assertEqual(nmv.consts.Skeleton.SWC_SOMA_SAMPLE_TYPE, 1)
        self.assertEqual(nmv.consts.Skeleton.SWC_AXON_SAMPLE_TYPE, 2)
        self.assertEqual(nmv.consts.Skeleton.SWC_BASAL_DENDRITE_SAMPLE_TYPE, 3)
        self.assertEqual(nmv.consts.Skeleton.SWC_APICAL_DENDRITE_SAMPLE_TYPE, 4)
        self.assertEqual(nmv.consts.Skeleton.SWC_FORK_POINT_SAMPLE_TYPE, 5)
        self.assertEqual(nmv.consts.Skeleton.SWC_END_POINT_SAMPLE_TYPE, 6)
        self.assertEqual(nmv.consts.Skeleton.SWC_CUSTOM_SAMPLE_TYPE, 7)
        self.assertEqual(nmv.consts.Skeleton.H5_POINTS_DIRECTORY, '/points')
        self.assertEqual(nmv.consts.Skeleton.H5_STRUCTURE_DIRECTORY, '/structure')
        self.assertEqual(nmv.consts.Skeleton.H5_PERIMETERS_DIRECTORY, '/perimeters')
        self.assertEqual(nmv.consts.Skeleton.H5_ASTROCYTE_STRUCTURE_DIRECTORY, '/structure')
        self.assertEqual(nmv.consts.Skeleton.H5_ASTROCYTE_POINTS_DIRECTORY, '/points')
        self.assertEqual(nmv.consts.Skeleton.H5_ASTROCYTE_COORDINATES_DIRECTORY, '/coordinates')
        self.assertEqual(nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_VERTEX_INDEX_DIRECTORY, '/endfeet_vertex_indices')
        self.assertEqual(nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_VERTEX_DATA_DIRECTORY, '/endfeet_vertex_data')
        self.assertEqual(nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_TRIANGLES_INDEX_DIRECTORY, '/endfeet_triangle_indices')
        self.assertEqual(nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_TRIANGLES_DATA_DIRECTORY, '/endfeet_triangle_data')
        self.assertEqual(nmv.consts.Skeleton.H5_SAMPLE_X_COORDINATES_IDX, 0)
        self.assertEqual(nmv.consts.Skeleton.H5_SAMPLE_Y_COORDINATES_IDX, 1)
        self.assertEqual(nmv.consts.Skeleton.H5_SAMPLE_Z_COORDINATES_IDX, 2)
        self.assertEqual(nmv.consts.Skeleton.H5_SAMPLE_RADIUS_IDX, 3)
        self.assertEqual(nmv.consts.Skeleton.H5_AXON_SECTION_TYPE, 2)
        self.assertEqual(nmv.consts.Skeleton.H5_BASAL_DENDRITE_SECTION_TYPE, 3)
        self.assertEqual(nmv.consts.Skeleton.H5_APICAL_DENDRITE_SECTION_TYPE, 4)

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
        self.assertEqual(nmv.consts.Suffix.SOMA_FRONT, '_soma_front')
        self.assertEqual(nmv.consts.Suffix.SOMA_SIDE, '_soma_side')
        self.assertEqual(nmv.consts.Suffix.SOMA_TOP, '_soma_top')
        self.assertEqual(nmv.consts.Suffix.SOMA_360, '_soma_360')
        self.assertEqual(nmv.consts.Suffix.SOMA_PROGRESSIVE, '_soma_progressive')
        self.assertEqual(nmv.consts.Suffix.MORPHOLOGY, '_morphology')
        self.assertEqual(nmv.consts.Suffix.MORPHOLOGY_FRONT, '_morphology_front')
        self.assertEqual(nmv.consts.Suffix.MORPHOLOGY_SIDE, '_morphology_side')
        self.assertEqual(nmv.consts.Suffix.MORPHOLOGY_TOP, '_morphology_top')
        self.assertEqual(nmv.consts.Suffix.MORPHOLOGY_360, '_morphology_360')
        self.assertEqual(nmv.consts.Suffix.MORPHOLOGY_PROGRESSIVE, '_morphology_progressive')
        self.assertEqual(nmv.consts.Suffix.MESH_FRONT, '_mesh_front')
        self.assertEqual(nmv.consts.Suffix.MESH_SIDE, '_mesh_side')
        self.assertEqual(nmv.consts.Suffix.MESH_TOP, '_mesh_top')
        self.assertEqual(nmv.consts.Suffix.MESH_360, '_mesh_360')
        self.assertEqual(nmv.consts.Suffix.FIXED_RADIUS, '_fixed_radius')