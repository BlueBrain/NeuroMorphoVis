#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2024, EPFL / Blue Brain Project
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

# Blender executable
BLENDER=$PWD/../../../../../../blender

# Input directory
INPUT_DIRECTORY='/ssd2/biovis2024-data/nmv-output-aspiny/meshes'

# Output directory
OUTPUT_DIRECTORY='/ssd2/biovis2024-data/nmv-output-aspiny/self-intersections'

# Max. number of iterations
MAX_ITERATIONS=50

# Num. cores
NUM_CORES=10

#####################################################################################################
BOOL_ARGS=' '

####################################################################################################
echo 'RUNNING ...'
$BLENDER -b --verbose 0 --python count_self_intersections_for_meshes.py --                          \
    --blender-executable=$BLENDER                                                                   \
    --input-directory=$INPUT_DIRECTORY                                                              \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --max-iterations=$MAX_ITERATIONS                                                                \
    --num-cores=$NUM_CORES                                                                          \
    $BOOL_ARGS

echo 'DONE ...'

