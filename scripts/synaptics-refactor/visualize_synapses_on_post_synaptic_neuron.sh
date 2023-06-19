#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Blender executable, adjust it to match the executable located on macOS or Linux
BLENDER=$PWD/../../../../../../blender

# Circuit config
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig'

# The GID of the post synaptic neuron
NEURON_GID='3774248'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/home/abdellah/Desktop/clean-scripts/output'

# Color-map file
SYNAPSES_JSON_FILE='/home/abdellah/Desktop/clean-scripts/output/3774248.synapses'

# Neuron color
NEURON_COLOR='255_255_255'

# Synapse size
SYNAPSE_SIZE='1.0'

# Base image resolution
IMAGE_RESOLUTION='5000'


#####################################################################################################
BOOL_ARGS=''
if [ "$SHOW_EXC_INH" == "yes" ];
    then BOOL_ARGS+=' --show-exc-inh '; fi
if [ "$RENDER_MOVIES" == "yes" ];
    then BOOL_ARGS+=' --render-movies '; fi
if [ "$RENDER_FRAMES" == "yes" ];
    then BOOL_ARGS+=' --render-frames '; fi

####################################################################################################
$BLENDER -b --verbose 0 --python visualize_synapses_on_post_synaptic_neuron.py --                   \
    --circuit-config=$CIRCUIT_CONFIG                                                                \
    --gid=$NEURON_GID                                                                               \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --synapses-file=$SYNAPSES_JSON_FILE                                                             \
    --neuron-color=$NEURON_COLOR                                                                    \
    --synapse-radius=$SYNAPSE_SIZE                                                                    \
    --image-resolution=$IMAGE_RESOLUTION                                                            \
    $BOOL_ARGS

