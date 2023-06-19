#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig'
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig_base'
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig.pre-fixL3'
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig_h5'
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj55/iavarone/releases/simulations/2019-11-21_GJs_newCT/CT_flickmulti_multiseed_1550fbr/ct_flick0/seed121877/BlueConfig'
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig_TC_WM'
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj112/circuits/CA1/20211110-BioM/BlueConfig'

# A file
SYNAPTIC_PAIRS_FILE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptic-pathways-data/L5_TTPC-pairs.txt'
SYNAPTIC_PAIRS_FILE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptic-pathways-data/iteration_2/S1DZO_pairs.gids'
SYNAPTIC_PAIRS_FILE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptic-pathways-data/sample-pairs.txt'
SYNAPTIC_PAIRS_FILE='/ssd2/projects-data/2022.01.07-neuron-pairs/pairs.gids'
SYNAPTIC_PAIRS_FILE='/ssd2/projects-data/2022.02.10-neuron-pairs/pairs.gids'
SYNAPTIC_PAIRS_FILE='/abdellah2/projects-data/2022.09.06-synaptics-sscx/L5_NBC-to-L5_TPC:A/L5_NBC-to-L5_TPC:A'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptic-pathways/trial-6-25.02.2021'
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptic-pathways/trial-7-11.10.2021'
OUTPUT_DIRECTORY='/ssd2/projects-data/2022.01.07-neuron-pairs/output'
OUTPUT_DIRECTORY='/ssd2/projects-data/2022.02.10-neuron-pairs/output'
OUTPUT_DIRECTORY='/abdellah2/projects-data/2022.09.06-synaptics-sscx/L5_NBC-to-L5_TPC:A/'
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj3/projects-data/2022.10.03-hippocampul-synaptics'

# Color
PRE_NEURON_COLOR='255_204_203'
POST_NEURON_COLOR='173_216_230'
SYNAPSE_COLOR='255_255_0'

PRE_NEURON_COLOR=''
POST_NEURON_COLOR=''

# Synapse size
SYNAPSE_SIZE='8.0'

# Base image resolution
IMAGE_RESOLUTION='4000'

# The background image the frames will get blended to
BACKGROUND_IMAGE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptomes-data/backgrounds/background_1900x1080.png'

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

