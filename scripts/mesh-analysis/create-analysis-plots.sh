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
#INPUT_DIRECTORY='/ssd2/papers-in-progress/kaust/input-meshes'
#INPUT_DIRECTORY='/ssd2/papers-in-progress/microglia/astrocytes/meshes'
INPUT_DIRECTORY='/ssd2/papers-in-progress/kaust/grouped-meshes/validated/meshes'
INPUT_DIRECTORY='/ssd2/ultraliser-stats-figures/astrocytes/output/meshes'


# The output directory where the scene and images will be generated
#OUTPUT_DIRECTORY='/ssd2/papers-in-progress/kaust/20.10.2021'
#OUTPUT_DIRECTORY='/ssd2/papers-in-progress/microglia/astrocytes/meshes'
#OUTPUT_DIRECTORY='/ssd2/papers-in-progress/kaust/grouped-meshes/validated/meshes/analysis'

#INPUT_DIRECTORY='/ssd2/ultraliser-stats-figures/axons/output-factors/watertight'


INPUT_DIRECTORY='/home/abdellah/display-meshes'
OUTPUT_DIRECTORY='/home/abdellah/display-meshes/output'

# Render artistic image, yes or no
RENDER_ARTISTIC='no'

# Mesh color
MESH_COLOR='0.9_0.125_0.150'

# Wireframe thickness
WIREFRAME_THICKNESS='0.25'

# Base image resolution
IMAGE_RESOLUTION='6000'

# Export Blender scenes
EXPORT_BLENDER_SCENE='no'

# ultraQualityChecker executable
QUALITY_CHECKER_EXECUTABLE='ultraMeshQualityChecker'

# Mesh scale
MESH_SCALE=0.001

#####################################################################################################
BOOL_ARGS=''
if [ "$EXPORT_BLENDER_SCENE" == "yes" ];
    then BOOL_ARGS+=' --export-blend '; fi
if [ "$RENDER_ARTISTIC" == "yes" ];
    then BOOL_ARGS+=' --render-artistic '; fi
####################################################################################################
echo 'CREATING MESH RENDERING ...'
$BLENDER -b --verbose 0 --python create-analysis-plots.py --                                        \
    --input-directory=$INPUT_DIRECTORY                                                              \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --mesh-color=$MESH_COLOR                                                                        \
    --resolution=$IMAGE_RESOLUTION                                                                  \
    --wireframe-thickness=$WIREFRAME_THICKNESS                                                      \
    --quality-checker-executable=$QUALITY_CHECKER_EXECUTABLE                                        \
    --mesh-scale=$MESH_SCALE                                                                        \
    $BOOL_ARGS


echo 'DONE ...'

