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
INPUT_DIRECTORY='/ssd2/ultraliser-figures/microns-pyramidal'
INPUT_DIRECTORY='/ssd2/ultraliser-figures/kaust-ngv-datasets/selected-meshes-for-analysis/neurons-astrocytes-pericytes-microglia-blood-vessels/input/meshes/pericytes/output/meshes'
#INPUT_DIRECTORY='/ssd2/ultraliser-figures/kaust-ngv-datasets/selected-meshes-for-analysis/neurons-astrocytes-pericytes-microglia-blood-vessels/output/meshes'
INPUT_DIRECTORY='/ssd2/ultraliser-figures/kaust-ngv-datasets/selected-meshes-for-analysis/astrocytes-er/output/meshes'
INPUT_DIRECTORY='/ssd2/ultraliser-figures/kaust-ngv-datasets/selected-meshes-for-analysis/mitochondria/input'


INPUT_DIRECTORY='/ssd2/ultraliser-figures/kaust-ngv-datasets/selected-meshes-for-analysis/mitochondria/'


# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/ssd2/ultraliser-figures/microns-pyramidal/output-rendering'
OUTPUT_DIRECTORY='/ssd2/ultraliser-figures/kaust-ngv-datasets/selected-meshes-for-analysis/neurons-astrocytes-pericytes-microglia-blood-vessels/input/meshes/pericytes/output/renderings'
#OUTPUT_DIRECTORY='/ssd2/ultraliser-figures/kaust-ngv-datasets/selected-meshes-for-analysis/neurons-astrocytes-pericytes-microglia-blood-vessels/output/rendering-output'
OUTPUT_DIRECTORY='/ssd2/ultraliser-figures/kaust-ngv-datasets/selected-meshes-for-analysis/astrocytes-er/output/renderings'
OUTPUT_DIRECTORY='/ssd2/ultraliser-figures/kaust-ngv-datasets/selected-meshes-for-analysis/mitochondria/input/renderings'


OUTPUT_DIRECTORY=$INPUT_DIRECTORY'/renderings'

# Mesh color
MESH_COLOR='0.9_0.125_0.150'

MESH_COLOR_IN='0.92118373_0.60184659_0.45048789'
MESH_COLOR_OUT='0.71837612_0.24102046_0.41863486'
MESH_COLOR=$MESH_COLOR_IN

# Camera view: front, side, top
CAMERA_VIEW='front'

# Render wireframe
RENDER_WIREFRAME='yes'

# Wireframe thickness (w.r.t pixel size)
WIREFRAME_THICKNESS='1.25'

# Base image resolution
IMAGE_RESOLUTION='5000'

# Export Blender scenes
EXPORT_BLENDER_SCENE='yes'

# Render artistic image, yes or no
RENDER_ARTISTIC='no'

#####################################################################################################
BOOL_ARGS=''
if [ "$EXPORT_BLENDER_SCENE" == "yes" ];
    then BOOL_ARGS+=' --export-blend '; fi
if [ "$RENDER_WIREFRAME" == "yes" ];
    then BOOL_ARGS+=' --wireframe '; fi
if [ "$ARTISTIC" == "yes" ];
    then BOOL_ARGS+=' --artistic '; fi
####################################################################################################
echo 'RENDER MESH ...'
$BLENDER -b --verbose 0 --python render-meshes.py --                                                \
    --input-directory=$INPUT_DIRECTORY                                                              \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --mesh-color=$MESH_COLOR                                                                        \
    --resolution=$IMAGE_RESOLUTION                                                                  \
    --wireframe-thickness=$WIREFRAME_THICKNESS                                                      \
    --camera-view=$CAMERA_VIEW                                                                      \
    $BOOL_ARGS
echo 'DONE ...'
