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
BLENDER=$PWD/../../../../../../blender

# Circuit config
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200731/CircuitConfig'

# Neuron GID
NEURON_GID='956172'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome'
OUTPUT_DIRECTORY='/hdd1/projects-data/11.25.2020-synaptomes-with-spines'
OUTPUT_DIRECTORY='/hdd1/projects-data/2021.01.12-synaptomes-final'


# Color-map file
COLOR_MAP_FILE=$PWD'/data/ColorMap'

# Neuron color
NEURON_COLOR='255_255_255'

# Synapse percentage
SYNAPSE_PERCENTAGE='100'

# Synapse size
SYNAPSE_SIZE='2.0'

# Close-up view size
CLOSE_UP_SIZE='50'

# Base full view resolution
FULL_VIEW_RESOLUTION='2000'

# Base close-up resolution
CLOSE_UP_RESOLUTION='4000'

# The background image the frames will get blended to
BACKGROUND_IMAGE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptomes-data/backgrounds/background_1900x1080.png'

# 360 frames directory
ROTATION_360_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptomes-data/360s/1'

####################################################################################################
echo 'CREATING SYNAPTOME ...'
$BLENDER -b --verbose 0 --python create-synaptome.py --                                             \
    --circuit-config=$CIRCUIT_CONFIG                                                                \
    --gid=$NEURON_GID                                                                               \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --color-map=$COLOR_MAP_FILE                                                                     \
    --neuron-color=$NEURON_COLOR                                                                    \
    --full-view-resolution=$FULL_VIEW_RESOLUTION                                                    \
    --close-up-resolution=$CLOSE_UP_RESOLUTION                                                      \
    --synapse-percentage=$SYNAPSE_PERCENTAGE                                                        \
    --synapse-size=$SYNAPSE_SIZE                                                                    \
    --close-up-size=$CLOSE_UP_SIZE                                                                  \
    --background-image=$BACKGROUND_IMAGE                                                            \
    --rotation-360-directory=$ROTATION_360_DIRECTORY                                                \
    $BOOL_ARGS

echo 'SYNAPTOME DONE ...'

