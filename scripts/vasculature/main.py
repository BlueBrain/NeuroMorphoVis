####################################################################################################
# Copyright (c) 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# System imports
import os, sys, ntpath, h5py

# Blender imports
import bpy
from mathutils import Vector

# NeuroMorphoVis imports
import neuromorphovis as nmv
import neuromorphovis.mesh
import neuromorphovis.scene

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

    # Load the morphology
    loader = vasculature_loader.VasculatureLoader(vasculature_morphology)

    # Skeletonize the morphology
    skeletonizer = vasculature_skeletonizer.VasculatureSkeletonizer(
        points_list=loader.points_list, segments_list=loader.segments_list,
        sections_list=loader.sections_list, connections_list=loader.connections_list)
    skeletonizer.skeletonize()


    print('to be done')


reconstruct_vasculature()

