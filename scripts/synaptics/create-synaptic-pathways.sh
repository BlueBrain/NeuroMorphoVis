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
# BLENDER='/gpfs/bbp.cscs.ch/project/proj3/resources/blender/bluebrain-blender-2.81/blender-neuromorphovis/blender'

# Circuit config
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200731/CircuitConfig'

# A file
SYNAPTIC_PAIRS_FILE='/blender/neuromorphovis-blender-2.82/blender-neuromorphovis/2.82/scripts/addons/neuromorphovis/scripts/synaptics/sample-pairs.txt'
SYNAPTIC_PAIRS_FILE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptic-pathways-data/L5_TTPC-pairs.txt'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptic-pathways/trial-2-04.10.2020'
OUTPUT_DIRECTORY='/ssd1/scratch/synaptic-pathways'

# Color
PRE_NEURON_COLOR='255_204_203'
POST_NEURON_COLOR='173_216_230'
SYNAPSE_COLOR='255_255_0'

# Synapse size
SYNAPSE_SIZE='8.0'

# Base image resolution
IMAGE_RESOLUTION='4000'

# The background image the frames will get blended to
BACKGROUND_IMAGE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptic-pathways-data/background.png'
BACKGROUND_IMAGE='/ssd1/scratch/background.png'

####################################################################################################
echo 'CREATING SYNAPTOME ...'
$BLENDER -b --verbose 0 --python create-synaptic-pathways.py --                                     \
    --circuit-config=$CIRCUIT_CONFIG                                                                \
    --synaptic-pairs-file=$SYNAPTIC_PAIRS_FILE                                                      \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --pre-neuron-color=$PRE_NEURON_COLOR                                                            \
    --post-neuron-color=$POST_NEURON_COLOR                                                          \
    --synapse-color=$SYNAPSE_COLOR                                                                  \
    --image-resolution=$IMAGE_RESOLUTION                                                            \
    --synapse-size=$SYNAPSE_SIZE                                                                    \
    --background-image=$BACKGROUND_IMAGE                                                            \
    $BOOL_ARGS

echo 'SYNAPTOME DONE ...'

