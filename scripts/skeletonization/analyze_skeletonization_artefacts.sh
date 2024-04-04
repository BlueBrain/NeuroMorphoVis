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

# Input mesh
INPUT_MESH='/abdellah2/microns-explorer/testing-scripts/input/864691136422909743.obj'
INPUT_MESH='/ssd2/skeletonization-project/sample-meshes-1/864691134832191490.obj'

# The file that contains the terminals of the spines
SPINES_TERMINALS_FILE='/ssd2/skeletonization-project/spine-extraction/output/dir-9/skeletonization-debugging/864691134832191490/864691134832191490-spine-terminals.nodes'

CENTER_LINES_FILE='/ssd2/skeletonization-project/spine-extraction/output/dir-9/skeletonization-debugging/864691134832191490/864691134832191490.branches'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/ssd2/skeletonization-project/sample-1-results'

# Scale factors
X_SCALE=0.001
Y_SCALE=0.001
Z_SCALE=0.001

# Export Blender scenes
EXPORT_BLENDER_SCENE='yes'

#####################################################################################################
BOOL_ARGS=''
if [ "$EXPORT_BLENDER_SCENE" == "yes" ];
    then BOOL_ARGS+=' --export-blend-file '; fi

####################################################################################################
echo 'RENDER MESH ...'
$BLENDER -b --verbose 0 --python analyze_skeletonization_artefacts.py --                            \
    --mesh=$INPUT_MESH                                                                              \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --x-scale=$X_SCALE --y-scale=$Y_SCALE --z-scale=$Z_SCALE                                        \
    --spines-terminals-file=$SPINES_TERMINALS_FILE                                                  \
    --center-lines-file=$CENTER_LINES_FILE                                                          \
    $BOOL_ARGS

echo 'DONE ...'
