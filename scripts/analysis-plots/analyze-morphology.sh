#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Blender executable
BLENDER=$PWD/../../../../../../blender

# The input directory where the meshes exist
INPUT_MORPHOLOGY='/scratch/analysis/morphology/C010398B-I4_cor_-_Scale_x1.000_y1.050_z1.000_-_Clone_5.h5'
#INPUT_MORPHOLOGY='/scratch/analysis/morphology/KO-1DIV-TTc.CNG.swc'
# Output directory
OUTPUT_DIRECTORY='/scratch/analysis/output'

####################################################################################################
$BLENDER -b --verbose 0 --python analyze-morphology.py --                                          \
    --morphology=$INPUT_MORPHOLOGY                                                            	   \
    --output-directory=$OUTPUT_DIRECTORY


