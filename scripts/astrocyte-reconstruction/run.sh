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
BLENDER='$PWD/../../../../../../blender'

# Output directory 
OUTPUT_DIRECTORY='/projects-data/2021.01.14-astrocytes-generation'
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj3/projects-data/2021.01.15-synthetic-astrocytes-meshes'

# Circuit
CIRCUIT='/projects/astrocytes-circuit/20200930'
CIRCUIT='/gpfs/bbp.cscs.ch/project/proj62/scratch/ngv_circuits/20200701'
CIRCUIT='/gpfs/bbp.cscs.ch/project/proj62/scratch/ngv_circuits/20201027_full_sonata_origin'

# Soma style, 'metaball' or 'softbody'
SOMA_STYLE='metaball'

# A list of GIDs, if this is defined the GIDS_FILE is ignored, and if set to '0' the file is used
GIDS_RANGE='1-100'

# GIDs file (a file contains a list of GIDs of the astrocytes to be reconstructed separated by space)
GIDS_FILE=$PWD/gids

# Meshes type, for simulation/visualization/both
MESH_TYPE='both'

# Create optimized meshes
CREATE_OPTIMIZED='yes'

# ultraCleanMesh executable
ULTRA_CLEAN_MESH_EXECUTABLE='/gpfs/bbp.cscs.ch/project/proj3/development/Ultraliser/build/bin/ultraCleanMesh'
# ULTRA_CLEAN_MESH_EXECUTABLE='ultraCleanMesh'

# Execution, serial or parallel
EXECUTION='parallel'

# Number of cores parallel processing 
NUMBER_CORES=15

# Decimation factor (range: 0.5 - 0.01) to reduce the number of polygons in the mesh that is
# generated for the visualization purposes.
DECIMATION_FACTOR='0.05'

# Export the final mesh in a .OBJ file, 'yes' or 'no'
EXPORT_OBJ='yes'

# Export the final mesh in a .BLEND file, 'yes' or 'no'
EXPORT_BLEND='no'

####################################################################################################
BOOL_ARGS=''
if [ "$EXPORT_OBJ" == 'yes' ];
    then BOOL_ARGS+=' --export-obj '; fi
if [ "$EXPORT_BLEND" == "yes" ];
    then BOOL_ARGS+=' --export-blend '; fi
if [ "$CREATE_OPTIMIZED" == "yes" ];
    then BOOL_ARGS+=' --create-optimized '; fi

####################################################################################################
$PWD/../../../../../python/bin/python3.7m run.py                                                    \
    --blender-executable=$BLENDER                                                                   \
    --gids-file=$GIDS_FILE                                                                          \
    --gids-range=$GIDS_RANGE                                                                        \
    --soma-style=$SOMA_STYLE                                                                        \
    --execution=$EXECUTION                                                                          \
    --circuit-path=$CIRCUIT                                                                         \
    --mesh-type=$MESH_TYPE                                                                          \
    --ultra-clean-mesh-executable=$ULTRA_CLEAN_MESH_EXECUTABLE                                      \
    --decimation-factor=$DECIMATION_FACTOR                                                          \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --number-cores=$NUMBER_CORES                                                                    \
    $BOOL_ARGS
