#!/usr/bin/env bash

# Blender executable
BLENDER='blender'

# Rendering configuration file
RENDERING_CONFIGURATION=''

# The input directory where the meshes exist
MESHES_DIRECTORY=''

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY=''

# Number of samples
NUMBER_SAMPLES=32

# Base image resolution
IMAGE_RESOLUTION=1024

# Prefix
PREFIX='scene'

################################################################################
BOOL_ARGS=''

####################################################################################################
$BLENDER -b --verbose 0 --python neurorender.py --                                                  \
    --config=$RENDERING_CONFIGURATION                                                               \
    --input=$MESHES_DIRECTORY                                                                       \
    --output=$OUTPUT_DIRECTORY                                                                      \
    --resolution=$IMAGE_RESOLUTION                                                                  \
    --prefix=$PREFIX                                                                                \
    --num-samples=$NUMBER_SAMPLES                                                                   \
    $BOOL_ARGS

echo  'Rendering done... '

