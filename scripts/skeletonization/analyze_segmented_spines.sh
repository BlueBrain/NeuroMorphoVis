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

# Input morphology
MORPHOLOGY='/ssd2/skeletonization-project/spine-extraction/output/dir-9/morphologies/864691134832191490.swc'

# The directory of the meshes of the spines
SPINES_MESHES_DIRECTORY='/ssd2/skeletonization-project/spine-extraction/output/dir-9/spine-meshes/864691134832191490'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/ssd2/skeletonization-project/sample-1-results/artifacts'

# Scale factors
NEURON_MESH_X_SCALE=0.001
NEURON_MESH_Y_SCALE=0.001
NEURON_MESH_Z_SCALE=0.001

# Export Blender scenes
EXPORT_BLENDER_SCENE='yes'

#####################################################################################################
BOOL_ARGS=''
if [ "$EXPORT_BLENDER_SCENE" == "yes" ];
    then BOOL_ARGS+=' --export-blend-file '; fi

####################################################################################################
echo 'RENDER MESH ...'
$BLENDER -b --verbose 0 --python analyze_segmented_spines.py --                                     \
    --morphology=$MORPHOLOGY                                                                        \
    --spine-meshes-directory=$SPINES_MESHES_DIRECTORY                                               \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --x-scale=$NEURON_MESH_X_SCALE --y-scale=$NEURON_MESH_Y_SCALE --z-scale=$NEURON_MESH_Z_SCALE    \
    $BOOL_ARGS

echo 'DONE ...'
