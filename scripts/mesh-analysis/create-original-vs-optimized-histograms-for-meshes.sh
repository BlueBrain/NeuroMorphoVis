#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2021, EPFL / Blue Brain Project
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

INPUT_DIRECTORY='/ssd2/biovis2024-data/nmv-output-aspiny/'
OUTPUT_DIRECTORY='/ssd2/biovis2024-data/nmv-output-aspiny/analysis'

# ultraQualityChecker executable
QUALITY_CHECKER_EXECUTABLE='ultraMeshQualityChecker'

# The numer of parallel cores used to run the script
NUM_CORES=6

#####################################################################################################
BOOL_ARGS=''
if [ "$STATS_READY" == "yes" ];
    then BOOL_ARGS+=' --stats-ready '; fi

####################################################################################################
echo 'RUNNING ...'
$BLENDER -b --verbose 0 --python create-original-vs-optimized-histograms-for-meshes.py --           \
    --blender-executable=$BLENDER                                                                   \
    --input-directory=$INPUT_DIRECTORY                                                              \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --quality-checker-executable=$QUALITY_CHECKER_EXECUTABLE                                        \
    --num-cores=$NUM_CORES

echo 'DONE ...'

