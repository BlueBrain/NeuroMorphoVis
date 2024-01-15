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

INPUT_DIRECTORY='/home/abdellah/display-meshes'
OUTPUT_DIRECTORY='/home/abdellah/display-meshes/output'

# ultraQualityChecker executable
QUALITY_CHECKER_EXECUTABLE='ultraMeshQualityChecker'

#####################################################################################################
BOOL_ARGS=''
if [ "$STATS_READY" == "yes" ];
    then BOOL_ARGS+=' --stats-ready '; fi

####################################################################################################
echo 'RUNNING ...'
$BLENDER -b --verbose 0 --python create-original-vs-optimized-histograms.py --                        \
    --input-directory=$INPUT_DIRECTORY                                                              \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --quality-checker-executable=$QUALITY_CHECKER_EXECUTABLE

echo 'DONE ...'

