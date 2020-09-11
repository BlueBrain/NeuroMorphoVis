#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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
BLENDER='/blender/neuromorphovis-blender-2.82/blender-neuromorphovis/blender'

# Circuit config
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200731/CircuitConfig'

# Neuron GID
NEURON_GID='956172'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/rendering-examples/example-2'
OUTPUT_DIRECTORY='/home/abdellah/Desktop/sample/example-2'

# Color-map file
COLOR_MAP_FILE=$PWD'/data/ColorMap'

# Neuron color
NEURON_COLOR='255_255_255'

# Synapse percentage
SYNAPSE_PERCENTAGE='25'

# Synapse size
SYNAPSE_SIZE='4.0'

# Base image resolution
IMAGE_RESOLUTION='2000'

# Base video resolution
VIDEO_RESOLUTION='500'

# The background image the frames will get blended to
BACKGROUND_IMAGE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptomes-data/background.png'
BACKGROUND_IMAGE='/home/abdellah/Desktop/sample/background.png'

# 360 frames directory
ROTATION_360_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptomes-data/360s/1'
ROTATION_360_DIRECTORY='/home/abdellah/Desktop/sample/360-1'

####################################################################################################
echo 'CREATING SYNAPTOME ...'
$BLENDER -b --verbose 0 --python create-synaptome.py --                                             \
    --circuit-config=$CIRCUIT_CONFIG                                                                \
    --gid=$NEURON_GID                                                                               \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --color-map=$COLOR_MAP_FILE                                                                     \
    --neuron-color=$NEURON_COLOR                                                                    \
    --image-resolution=$IMAGE_RESOLUTION                                                            \
    --video-resolution=$IMAGE_RESOLUTION                                                            \
    --synapse-percentage=$SYNAPSE_PERCENTAGE                                                        \
    --synapse-size=$SYNAPSE_SIZE                                                                    \
    --background-image=$BACKGROUND_IMAGE                                                            \
    --rotation-360-directory=$ROTATION_360_DIRECTORY                                                \
    $BOOL_ARGS

echo 'SYNAPTOME DONE ...'

