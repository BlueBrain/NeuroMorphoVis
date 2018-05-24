#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

# Blender executable
BLENDER='blender'

# Rendering configuration file
RENDERING_CONFIGURATION='/data/neurorender-data/sample.config'

# The input directory where the meshes exist
MESHES_DIRECTORY='/data/neurorender-data/meshes'

## Input type
# Use ['blend'] if the neurons are stored in .blend files
# Use ['ply'] if the neurons are stored in .ply meshes
# Use ['obj'] if the neurons are stored in .obj meshes.
INPUT_TYPE='blend'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/data/neurorender-data/output'

# Number of samples
NUMBER_SAMPLES=32

# Base image resolution
IMAGE_RESOLUTION=5000

# Prefix
PREFIX='scene'

################################################################################
BOOL_ARGS=''

####################################################################################################
echo 'RENDEING'
$BLENDER -b --verbose 0 --python neurorender.py --                                                 \
    --config=$RENDERING_CONFIGURATION                                                              \
    --input-directory=$MESHES_DIRECTORY                                                            \
    --input-type=$INPUT_TYPE                                                                       \
    --output-directory=$OUTPUT_DIRECTORY                                                           \
    --resolution=$IMAGE_RESOLUTION                                                                 \
    --prefix=$PREFIX                                                                               \
    --spp=$NUMBER_SAMPLES                                                                          \
    $BOOL_ARGS

echo 'RENDERING DONE ...'

