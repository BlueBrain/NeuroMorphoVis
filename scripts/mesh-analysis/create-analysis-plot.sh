#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2021, EPFL / Blue Brain Project
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
BLENDER=$PWD/../../../../../../blender

# Input mesh
INPUT_MESH='/ssd2/ultraliser-figures/microns-pyramidal/2.obj'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/ssd2/ultraliser-figures/microns-pyramidal/output'

# Render artistic image, yes or no
RENDER_ARTISTIC='yes'

# Mesh color
MESH_COLOR='0.9_0.125_0.150'

# Wireframe thickness
WIREFRAME_THICKNESS='0.075'

# Base image resolution
IMAGE_RESOLUTION='5000'

# Export Blender scenes
EXPORT_BLENDER_SCENE='yes'

# ultraQualityChecker executable
QUALITY_CHECKER_EXECUTABLE='ultraMeshQualityChecker '

#####################################################################################################
BOOL_ARGS=''
if [ "$EXPORT_BLENDER_SCENE" == "yes" ];
    then BOOL_ARGS+=' --export-blend '; fi
if [ "$ARTISTIC" == "yes" ];
    then BOOL_ARGS+=' --artistic '; fi
####################################################################################################
echo 'CREATING MESH RENDERING ...'
$BLENDER -b --verbose 0 --python create-analysis-plot.py --                                         \
    --input-mesh=$INPUT_MESH                                                                        \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --mesh-color=$MESH_COLOR                                                                        \
    --resolution=$IMAGE_RESOLUTION                                                                  \
    --wireframe-thickness=$WIREFRAME_THICKNESS                                                      \
    --quality-checker-executable=$QUALITY_CHECKER_EXECUTABLE                                        \
    $BOOL_ARGS

echo 'DONE ...'

