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
BLENDER=$PWD/../../../../../../../blender

# Circuit config
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig'

# The GID of the neuron
NEURON_GID='3774248'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj3/projects-data/synaptics/ex-1'

# The color of the neuron
NEURON_COLOR='#fffff0'

# The color of the excitatory synapses
EXC_SYNAPSES_COLOR='#ff0000	'

# The color of the inhibitory synapses
INH_SYNAPSES_COLOR='#0000ff'

# If this variable is set to yes, we will use the UNIFIED_NEURON_RADIUS value for all the branches
UNIFY_BRANCHES_RADII='yes'

# A constant value for the radius of the neuron branches. This value will be ignore if
# UNIFY_BRANCHES_RADII is set to yes
UNIFIED_NEURON_RADIUS='1.0'

# Synapse size
SYNAPSE_RADIUS='2.0'

# The percentage of the displayed synapses (from 0.1% - 100%)
SYNAPSE_PERCENTAGE='100'

# Base image resolution
IMAGE_RESOLUTION='5000'

# Save the rendering into a Blender file such that we can visualize the scene later interactively
SAVE_TO_BLEND_FILE='yes'

#####################################################################################################
BOOL_ARGS=''
if [ "$SAVE_TO_BLEND_FILE" == "yes" ];
    then BOOL_ARGS+=' --save-blend-file '; fi
if [ "$UNIFY_BRANCHES_RADII" == "yes" ];
    then BOOL_ARGS+=' --unify-branches-radii '; fi

####################################################################################################
$BLENDER -b --verbose 0 --python visualize_exc_inh_synapses_on_neuron.py --                         \
    --circuit-config=$CIRCUIT_CONFIG                                                                \
    --gid=$NEURON_GID                                                                               \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --neuron-color=$NEURON_COLOR                                                                    \
    --unified-branches-radius=$UNIFIED_NEURON_RADIUS                                                \
    --exc-synapses-color=$EXC_SYNAPSES_COLOR                                                        \
    --inh-synapses-color=$INH_SYNAPSES_COLOR                                                        \
    --synapse-radius=$SYNAPSE_RADIUS                                                                \
    --synapse-percentage=$SYNAPSE_PERCENTAGE                                                        \
    --image-resolution=$IMAGE_RESOLUTION                                                            \
    $BOOL_ARGS

