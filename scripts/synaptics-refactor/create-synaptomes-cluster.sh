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
BLENDER=$PWD'/../../../../../../blender'

# Individual synaptome script
SYNAPTOME_SCRIPT=$PWD/'create-synaptome.py'

# Circuit config
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200731/CircuitConfig'
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig.pre-fixL3'

# Neuron GID
# Synaptic file
REGION='S1DZO'
#REGION='S1DZ'
#REGION='S1FL_Column'
#REGION='S1HL_Column'
#REGION='S1J_Column'
#REGION='S1Sh'
#REGION='S1Tr'
#REGION='S1ULp'
GID_LIST='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptomes-data/iteration_2/cvs-files/gids/'$REGION'.gids'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/hdd1/projects-data/11.25.2020-synaptomes-with-spines'
OUTPUT_DIRECTORY='/hdd1/projects-data/2021.01.13-synaptomes-final/mtypes'
OUTPUT_DIRECTORY='/hdd1/projects-data/2021.01.13-synaptomes-final/excitatory_inhibitory'
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome'
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-2-26.02.2021'
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-7-09.03.2020'
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-9-10.03.2021/'$REGION

# Color-map file
COLOR_MAP_FILE=$PWD'/data/ColorMap'

# The background image the frames will get blended to
BACKGROUND_IMAGE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptomes-data/backgrounds/background_1900x1080.png'

# Show excitatory and inhibitory synapses, yes or no
SHOW_EXC_INH='no'

# Neuron color
NEURON_COLOR='255_255_255'

# Synapse percentage
SYNAPSE_PERCENTAGE='50'

# Synapse size
SYNAPSE_SIZE='2.0'

# Close-up view size
CLOSE_UP_SIZE='30'

# Base full view resolution
FULL_VIEW_RESOLUTION='2000'

# Base close-up resolution
CLOSE_UP_RESOLUTION='2000'

# Render 360 movies
RENDER_MOVIES='yes'

# Render static frames
RENDER_FRAMES='no'

# Number of jobs per core
NUMBER_OF_JOBS_PER_CORE=25

# User name, must be given to query slurm
USER_NAME='abdellah'

#####################################################################################################
BOOL_ARGS=''
if [ "$SHOW_EXC_INH" == "yes" ];
    then BOOL_ARGS+=' --show-exc-inh '; fi
if [ "$RENDER_MOVIES" == "yes" ];
    then BOOL_ARGS+=' --render-movies '; fi
if [ "$RENDER_FRAMES" == "yes" ];
    then BOOL_ARGS+=' --render-frames '; fi

####################################################################################################
$BLENDER -b --verbose 0 --python create-synaptomes-cluster.py --                                    \
    --synaptome-script=$SYNAPTOME_SCRIPT                                                            \
    --circuit-config=$CIRCUIT_CONFIG                                                                \
    --gid-list=$GID_LIST                                                                            \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --color-map=$COLOR_MAP_FILE                                                                     \
    --neuron-color=$NEURON_COLOR                                                                    \
    --full-view-resolution=$FULL_VIEW_RESOLUTION                                                    \
    --close-up-resolution=$CLOSE_UP_RESOLUTION                                                      \
    --synapse-percentage=$SYNAPSE_PERCENTAGE                                                        \
    --synapse-size=$SYNAPSE_SIZE                                                                    \
    --close-up-size=$CLOSE_UP_SIZE                                                                  \
    --background-image=$BACKGROUND_IMAGE                                                            \
    --number-jobs-per-core=$NUMBER_OF_JOBS_PER_CORE                                                 \
    --user-name=$USER_NAME                                                                          \
    $BOOL_ARGS
