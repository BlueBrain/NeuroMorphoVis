#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
BLENDER='/gpfs/bbp.cscs.ch/project/proj3/research/nmv/neuromorphovis-blender-2.79b-linux-x86_64/blender'

# Rendering configuration file
RENDERING_CONFIGURATION='/gpfs/bbp.cscs.ch/project/proj3/research/nmv/projects/soma-rainbow/targets/RANDOM_BOX_mc2_Column_50.00p.config'

# The input directory where the meshes exist
MESHES_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj3/research/nmv/projects/soma-rainbow/neurons-meshes/morphologies'

## Input type
# Use ['blend'] if the neurons are stored in .blend files
# Use ['ply'] if the neurons are stored in .ply meshes
# Use ['obj'] if the neurons are stored in .obj meshes.
INPUT_TYPE='blend'

# The output directory where the scene and images will be generated
OUTPUT_DIRECTORY='/gpfs/bbp.cscs.ch/project/proj3/research/nmv/projects/soma-rainbow/rendering'

# Style file
STYLE_FILE='/gpfs/bbp.cscs.ch/project/proj3/research/nmv/projects/soma-rainbow/styles/style.config'

# Projection, orthographic or perspective
PROJECTION='orthographic'

# Number of samples
NUMBER_SAMPLES=32

# Base image resolution
IMAGE_RESOLUTION=10000

# Use spheres for representative rendering
USE_SPHERES='no'

# Transform the neurons to their local positions
TRANSFORM_NEURONS='yes'

# Prefix
PREFIX='rainbow'

################################################################################
BOOL_ARGS=''
if [ "$USE_SPHERES" == "yes" ];
    then BOOL_ARGS+=' --use-spheres'; fi
if [ "$TRANSFORM_NEURONS" == "yes" ];
    then BOOL_ARGS+=' --transform'; fi

####################################################################################################
echo 'RENDERING ...'
$BLENDER -b --verbose 0 --python soma-rainbow.py --                                                \
    --config=$RENDERING_CONFIGURATION                                                              \
    --input-directory=$MESHES_DIRECTORY                                                            \
    --input-type=$INPUT_TYPE                                                                       \
    --output-directory=$OUTPUT_DIRECTORY                                                           \
    --resolution=$IMAGE_RESOLUTION                                                                 \
    --style-file=$STYLE_FILE                                                                       \
    --projection=$PROJECTION                                                                       \
    --prefix=$PREFIX                                                                               \
    --spp=$NUMBER_SAMPLES                                                                          \
    $BOOL_ARGS

echo 'RENDERING DONE ...'

