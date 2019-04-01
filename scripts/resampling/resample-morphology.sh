#!/usr/bin/env bash
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

# Blender executable
BLENDER='/bbp/bbp-blender-packages/blender-2.79b-linux-glibc219-x86_64/blender'

# The input directory where the meshes exist
INPUT_MORPHOLOGY='/bbp/projects/2019-resampling-morphologies/input/000061cbfa9d8d7bc26c4a2c73614e61.h5'

# Output directory 
OUTPUT_DIRECTORY='/bbp/projects/2019-resampling-morphologies/output'

####################################################################################################
$BLENDER -b --verbose 0 --python resample-morphology.py --                                         \
    --morphology=$INPUT_MORPHOLOGY                                                            	   \
    --output-directory=$OUTPUT_DIRECTORY                                                           
    

