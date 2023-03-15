#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=1
#SBATCH --mem=128000
#SBATCH --time=16:00:00
#SBATCH --partition=prod
#SBATCH --job-name="synaptome"
#SBATCH --constraint=volta
#SBATCH --account=proj3
#SBATCH --output=/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-4-08.03.2020/stdout-vgl
#SBATCH --error=/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-4-08.03.2020/stderr-vgl
#sbatch --startx
#sbatch --x11

# Blender executable
BLENDER=$PWD/../../../../../../blender

# Circuit config
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200731/CircuitConfig'
CIRCUIT_CONFIG='/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig.pre-fixL3'

# Neuron GID
GIDS_FILE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptomes-data/iteration_2/cvs-files/gids/S1DZ.gids'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome'
OUTPUT_DIRECTORY='/hdd1/projects-data/11.25.2020-synaptomes-with-spines'
OUTPUT_DIRECTORY='/hdd1/projects-data/2021.01.13-synaptomes-final/mtypes'
OUTPUT_DIRECTORY='/hdd1/projects-data/2021.01.13-synaptomes-final/excitatory_inhibitory'
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-2-26.02.2021'
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-4-08.03.2020'

# Show excitatory and inhibitory synapses, yes or no
SHOW_EXC_INH='no'

# Color-map file
COLOR_MAP_FILE=$PWD'/data/ColorMap'

# Neuron color
NEURON_COLOR='255_255_255'

# Synapse percentage
SYNAPSE_PERCENTAGE='100'

# Synapse size
SYNAPSE_SIZE='2.0'

# Close-up view size
CLOSEUP_SIZE='50'

# Base full view resolution
FULL_VIEW_RESOLUTION='2000'

# Base close-up resolution
CLOSEUP_RESOLUTION='1000'

# The background image the frames will get blended to
BACKGROUND_IMAGE='/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptomes-data/backgrounds/background_1900x1080.png'

# Execution, serial or parallel
EXECUTION='serial'

# Number of parallel cores
NUMBER_PARALLEL_CORES='10'

#####################################################################################################
BOOL_ARGS=''
if [ "$SHOW_EXC_INH" == "yes" ];
    then BOOL_ARGS+=' --show-exc-inh '; fi
#####################################################################################################


nvidia-smi
module load unstable
module load virtualgl/2.5.2

#DISPLAY=:5 glxspheres64


#module load unstable
#module load virtualgl/2.5.2

####################################################################################################
#/usr/bin/X

#xdpyinfo | grep version
#DISPLAY=:5 glxgears

echo 'CREATING SYNAPTOMES ...';
DISPLAY=:5 $PWD/../../../../../python/bin/python3.7m create-synaptomes.py                 \
    --blender-executable=$BLENDER                                                                   \
    --circuit-config=$CIRCUIT_CONFIG                                                                \
    --gids-file=$GIDS_FILE                                                                          \
    --execution=$EXECUTION                                                                          \
    --number-parallel-cores=$NUMBER_PARALLEL_CORES                                                  \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --color-map=$COLOR_MAP_FILE                                                                     \
    --neuron-color=$NEURON_COLOR                                                                    \
    --full-view-resolution=$FULL_VIEW_RESOLUTION                                                    \
    --close-up-resolution=$CLOSEUP_RESOLUTION                                                      \
    --synapse-percentage=$SYNAPSE_PERCENTAGE                                                        \
    --synapse-size=$SYNAPSE_SIZE                                                                    \
    --close-up-size=$CLOSEUP_SIZE                                                                  \
    --background-image=$BACKGROUND_IMAGE                                                            \
    $BOOL_ARGS;
