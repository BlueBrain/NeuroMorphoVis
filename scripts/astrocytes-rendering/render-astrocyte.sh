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
#INPUT_DIRECTORY='/hdd1/projects-data/2021.01.13-astrocyte-meshes-samples-for-rendering/input/optimized'
INPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj3/projects-data/2021.01.14-synthetic-astrocytes-meshes/simulation'

# Astrocyte mesh
#ASTROCYTES_LIST='/hdd1/projects-data/2021.01.13-astrocyte-meshes-samples-for-rendering/input/astrocytes'
ASTROCYTES_LIST='/gpfs/bbp.cscs.ch/project/proj3/projects-data/2021.01.14-synthetic-astrocytes-meshes/astrocyte-list'

# The output directory where the scene and images will be generated
#OUTPUT_DIRECTORY='/hdd1/projects-data/2021.01.13-astrocyte-meshes-samples-for-rendering/output'
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj3/projects-data/2021.01.14-synthetic-astrocytes-meshes/analysis'

# Render artistic image, yes or no
RENDER_ARTISTIC='no'

# Mesh color
SKINNED_MESH_COLOR='0.9_0.125_0.150'
OPTIMIZED_MESH_COLOR='0.015_0.275_0.950'

# Wireframe thickness
WIREFRAME_THICKNESS='0.075'

# Base image resolution
IMAGE_RESOLUTION='2000'

# Export Blender scenes
EXPORT_BLENDER_SCENE='yes'

# ultraQualityChecker executable
QUALITY_CHECKER_EXECUTABLE='/gpfs/bbp.cscs.ch/project/proj3/development/Ultraliser/build/bin/ultraMeshQualityChecker'

#####################################################################################################
BOOL_ARGS=''
if [ "$EXPORT_BLENDER_SCENE" == "yes" ];
    then BOOL_ARGS+=' --export-blend '; fi
if [ "$ARTISTIC" == "yes" ];
    then BOOL_ARGS+=' --artistic '; fi
####################################################################################################
echo 'CREATING ASTROCYTE RENDERING ...'
$BLENDER -b --verbose 0 --python render-astrocyte.py --                                             \
    --astrocytes-list=$ASTROCYTES_LIST                                                              \
    --input-directory=$INPUT_DIRECTORY                                                              \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --skinned-mesh-color=$SKINNED_MESH_COLOR                                                        \
    --optimized-mesh-color=$OPTIMIZED_MESH_COLOR                                                    \
    --resolution=$IMAGE_RESOLUTION                                                                  \
    --wireframe-thickness=$WIREFRAME_THICKNESS                                                      \
    --quality-checker-executable=$QUALITY_CHECKER_EXECUTABLE                                        \
    $BOOL_ARGS

echo 'SYNAPTOME DONE ...'

