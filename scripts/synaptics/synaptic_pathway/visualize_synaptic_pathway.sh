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

# Blender executable, adjust it to match the executable located on macOS or Linux
BLENDER=$PWD/../../../../../../../blender

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj3/projects-data/synaptics/ex-4'
OUTPUT_DIRECTORY='/abdellah2/scratch/spines'

# BBP circuit config
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig'
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig_h5'

# The GID of the pre- and post-synaptic neurons
PRE_SYNAPTIC_NEURON_GID='961928'
POST_SYNAPTIC_NEURON_GID='3793945'

# If this variable is set to yes, we will use the UNIFIED_NEURON_RADIUS value for all the branches
UNIFY_BRANCHES_RADII='no'

# A constant value for the radius of the neuron branches. This value will be ignore if
# UNIFY_BRANCHES_RADII is set to yes
UNIFIED_NEURON_RADIUS='1.0'

# The colors of the pre- and post-synaptic neurons
PRE_SYNAPTIC_DENDRITES_COLOR='#c23bd4' # 194, 59, 212
PRE_SYNAPTIC_AXONS_COLOR='#3b76d4' # 59, 118, 212
POST_SYNAPTIC_DENDRITES_COLOR='#00ffaa' # 194, 59, 212
POST_SYNAPTIC_AXONS_COLOR='#ff00aa' # 212, 59, 79

# The color of the shared synapses
SYNAPSES_COLOR='#ff00aa'

# A given fixed radius for the synapses, it is represented as a symbolic sphere
SYNAPSE_RADIUS='2.0'

# Base resolution of the rendered image
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
$BLENDER -b --verbose 0 --python visualize_synaptic_pathway.py --                                   \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --circuit-config=$CIRCUIT_CONFIG                                                                \
    --pre-synaptic-neuron-gid=$PRE_SYNAPTIC_NEURON_GID                                              \
    --post-synaptic-neuron-gid=$POST_SYNAPTIC_NEURON_GID                                            \
    --pre-synaptic-dendrites-color=$PRE_SYNAPTIC_DENDRITES_COLOR                                    \
    --pre-synaptic-axons-color=$PRE_SYNAPTIC_AXONS_COLOR                                            \
    --post-synaptic-dendrites-color=$POST_SYNAPTIC_DENDRITES_COLOR                                  \
    --post-synaptic-axons-color=$POST_SYNAPTIC_AXONS_COLOR                                          \
    --unified-branches-radius=$UNIFIED_NEURON_RADIUS                                                \
    --synapses-color=$SYNAPSES_COLOR                                                                \
    --synapse-radius=$SYNAPSE_RADIUS                                                                \
    --image-resolution=$IMAGE_RESOLUTION                                                            \
    $BOOL_ARGS