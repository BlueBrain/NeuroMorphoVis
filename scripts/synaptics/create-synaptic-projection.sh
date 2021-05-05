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

# Circuit config
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj112/circuits/CA1/20200820/CircuitConfig'

# Post synaptic neurons GIDs, a list separate by '_'
GIDS='1681_408231'

# Projection
PROJECTION='SC'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/hdd1/projects-data/2021.05.05-synapse-projections'

# Neuron color
NEURON_COLOR='0_0_0'

# Neuron color
SYNAPSE_COLOR='255_255_0'

# Synapse percentage
SYNAPSE_PERCENTAGE='50'

# Synapse size
SYNAPSE_SIZE='2.0'

# Base full view resolution
IMAGE_RESOLUTION='4000'


####################################################################################################
echo 'CREATING SYNAPTOME ...'
$BLENDER -b --verbose 0 --python create-synaptic-projection.py --                                   \
    --circuit-config=$CIRCUIT_CONFIG                                                                \
    --gids=$GIDS                                                                                    \
    --projection=$PROJECTION                                                                        \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --neuron-color=$NEURON_COLOR                                                                    \
    --synapse-color=$SYNAPSE_COLOR                                                                  \
    --image-resolution=$IMAGE_RESOLUTION                                                            \
    --synapse-percentage=$SYNAPSE_PERCENTAGE                                                        \
    --synapse-size=$SYNAPSE_SIZE                                                                    \

echo 'SYNAPTOME DONE ...'

