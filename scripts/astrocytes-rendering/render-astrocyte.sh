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

# Input directory
INPUT_DIRECTORY='/hdd1/projects-data/2021.01.13-astrocyte-meshes-samples-for-rendering/input/skinned'

# Astrocyte mesh
ASTROCYTES_LIST='/hdd1/projects-data/2021.01.13-astrocyte-meshes-samples-for-rendering/input/astrocytes'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/hdd1/projects-data/2021.01.13-astrocyte-meshes-samples-for-rendering/output'

# Consider the optimized version
CONSIDER_OPTIMIZED='yes'

# Mesh color
WIREFRAME_MESH_COLOR='255_128_10'

# Wireframe thickness
WIREFRAME_THICKNESS='0.05'

# Base image resolution
IMAGE_RESOLUTION='2000'

# Export Blender scenes
EXPORT_BLENDER_SCENE='yes'

#####################################################################################################
BOOL_ARGS=''
if [ "$EXPORT_BLENDER_SCENE" == "yes" ];
    then BOOL_ARGS+=' --export-blend '; fi
if [ "$CONSIDER_OPTIMIZED" == "yes" ];
    then BOOL_ARGS+=' --consider-optimized '; fi
####################################################################################################
echo 'CREATING ASTROCYTE RENDERING ...'
$BLENDER -b --verbose 0 --python render-astrocyte.py --                                             \
    --astrocytes-list=$ASTROCYTES_LIST                                                              \
    --input-directory=$INPUT_DIRECTORY                                                              \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --astrocyte-color=$WIREFRAME_MESH_COLOR                                                         \
    --resolution=$IMAGE_RESOLUTION                                                                  \
    --wireframe-thickness=$WIREFRAME_THICKNESS                                                      \
    $BOOL_ARGS

echo 'SYNAPTOME DONE ...'

