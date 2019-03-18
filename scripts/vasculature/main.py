####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
import os, sys, ntpath, h5py

# Blender imports
import bpy
from mathutils import Vector

# NeuroMorphoVis imports
import nmv
import nmv.mesh
import nmv.scene

# Internal imports
project_space = ntpath.basename(os.path.dirname(os.path.realpath(__file__)))
project_path = os.path.dirname(os.path.realpath(__file__)).replace(project_space, '')
sys.path.append(project_path)

import vasculature_loader
import vasculature_skeletonizer


####################################################################################################
# @reconstruct_vasculature
####################################################################################################
def reconstruct_vasculature():

    # Clear the scene
    nmv.scene.ops.clear_scene()

    # Vasculature path
    vasculature_morphology = '/data/morphologies/vasculature/vasculature-datas-set-2.h5'
    #vasculature_morphology = '/computer/data/vasculature.h5'
    #vasculature_morphology = '/data/vasculature/vasculature.h5'

    # Load the morphology
    loader = vasculature_loader.VasculatureLoader(vasculature_morphology)

    # Skeletonize the morphology
    skeletonizer = vasculature_skeletonizer.VasculatureSkeletonizer(
        points_list=loader.points_list, segments_list=loader.segments_list,
        sections_list=loader.sections_list, connections_list=loader.connections_list)
    skeletonizer.skeletonize()

    # Get the roots
    print('Roots: %d' % len(skeletonizer.roots))

    # Data
    print('STATUS: Skeleton reconstruction Done !')


reconstruct_vasculature()

