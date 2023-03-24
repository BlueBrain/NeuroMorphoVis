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
GIDS='2080_14739_128625'

# Projection
PROJECTION='SC'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/abdellah2/projects-data/2023.03.24-synaptic-projections'

# Neuron color
NEURON_COLOR='1_1.0_1'
# NEURON_COLOR='0.0_1.0_0.0'

# Neuron color
SYNAPSE_COLOR='1.0_0.3_0.06'
# SYNAPSE_COLOR='1.0_0.0_0.0'

# Synapse percentage
SYNAPSE_PERCENTAGE='10'

# Synapse size
SYNAPSE_SIZE='1.5'

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

