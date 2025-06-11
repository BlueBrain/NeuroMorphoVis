#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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

# libSonata Circuit file 
CIRCUIT=''

# Population name
POPULATION=''

# Colormap file
# (optional, if not provided, the default colormap will be used)
COLORMAP_FILE=''

# Image resolution 
IMAGE_RESOLUTION=2048

# Rendering view, options are 'front', 'side', 'top', and 'all' 
RENDERING_VIEW='front'

# Output directory 
OUTPUT_DIRECTORY='/home/abdellah/neuromorphovis-output/analysis-glia/resampled'

# Export the final mesh in a .BLEND file, 'yes' or 'no'
SAVE_BLENDER_SCENE='yes'

####################################################################################################
BOOL_ARGS=''
if [ "$SAVE_BLENDER_SCENE" == 'yes' ];
    then BOOL_ARGS+=' --save-blender-scene '; fi


####################################################################################################
$BLENDER -b --verbose 0 --python circuit-renderer.py -- \
    --circuit="$CIRCUIT" \
    --population="$POPULATION" \
    --output-directory="$OUTPUT_DIRECTORY" \
    --image-resolution="$IMAGE_RESOLUTION" \
    --rendering-view="$RENDERING_VIEW" \
    --colormap-file="$COLORMAP_FILE" \
    $BOOL_ARGS
####################################################################################################

