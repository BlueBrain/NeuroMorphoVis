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

# Output directory 
OUTPUT_DIRECTORY='/projects/astrocytes-circuit/astrocytes-meshes/generated'

# Circuit
CIRCUIT='/ssd1/projects/astrocytes-circuit/20200930'

# A list of GIDs, if this is defined the GIDS_FILE is ignored
GIDS_RANGE='1-5'

# GIDs file (a file contains a list of GIDs of the astrocytes to be reconstructed separated by space)
GIDS_FILE='/blender/neuromorphovis-blender-2.82/blender-neuromorphovis/2.82/scripts/addons/neuromorphovis/scripts/astrocyte-reconstruction/gids'

# Execution, serial or parallel
EXECUTION='parallel'

# Decimation factor (range: 1.0 - 0.01) to reduce the number of polygons in the mesh
DECIMATION_FACTOR=0.1

####################################################################################################
python3 run.py                                                                                      \
    --blender-executable=$BLENDER                                                                   \
    --gids-file=$GIDS_FILE                                                                          \
    --gids-range=$GIDS_RANGE                                                                        \
    --execution=$EXECUTION                                                                          \
    --circuit-path=$CIRCUIT                                                                         \
    --decimation-factor=$DECIMATION_FACTOR                                                          \
    --output-directory=$OUTPUT_DIRECTORY
    

