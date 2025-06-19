#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2025, Open Brain Institute
# Author(s): Marwan Abdellah <marwan.abdellah@openbraininstitute.org>
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
CIRCUIT_CONFIG='/data/circuits/cns-circuit/v2/N_10__selection1__swc/circuit_config.json'

# Population name
POPULATION='S1nonbarrel_neurons'

# Colormap to use for the rendering, options are: 
# 'tab10', 'tab20', 'viridis', 'plasma', 'inferno', 'magma', 'cividis'
# If you want to use a custom colormap, set COLORMAP_FILE to the path of the colormap file
# and set COLORMAP to 'custom'
COLORMAP='custom'


# Colormap file (optional, if not provided, the default colormaps will be used)
COLORMAP_FILE='/home/abdellah/Downloads/colors_tab10.txt'

# Image resolution 
IMAGE_RESOLUTION=3000

# Output directory 
OUTPUT_DIRECTORY='/data/circuits/cns-circuit/v2/renderings/v3-19.06.2025'

####################################################################################################
# Create the full image  
echo "Rendering the full circuit image:"
$BLENDER -b --verbose 0 --python circuit-renderer.py -- \
    --circuit-config="$CIRCUIT_CONFIG" \
    --population="$POPULATION" \
    --output-directory="$OUTPUT_DIRECTORY" \
    --image-resolution="$IMAGE_RESOLUTION" \
    --colormap-file="$COLORMAP_FILE" \
    --colormap-palette="$COLORMAP" \
    --unified-branch-radius=1.0 \
    --orient-circuit-upwards --square-aspect-ratio

# Create the close-up image
echo "Rendering the close-up circuit image:"
$BLENDER -b --verbose 0 --python circuit-renderer.py -- \
    --circuit-config="$CIRCUIT_CONFIG" \
    --population="$POPULATION" \
    --output-directory="$OUTPUT_DIRECTORY" \
    --image-resolution="$IMAGE_RESOLUTION" \
    --colormap-file="$COLORMAP_FILE" \
    --colormap-palette="$COLORMAP" \
    --unified-branch-radius=0.0 \
    --render-closeup --render-shadows --render-outlines --transparent-background \
    --orient-circuit-upwards --square-aspect-ratio

# Compose the two images 
python3 compose-images.py --images-directory="$OUTPUT_DIRECTORY" --closeup-ratio=0.35