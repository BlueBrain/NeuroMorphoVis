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

# Colormap file
# (optional, if not provided, the default colormap will be used)
COLORMAP_FILE='None'

# Image resolution 
IMAGE_RESOLUTION=2048

# Rendering view, options are 'front', 'side', 'top', and 'all' 
RENDERING_VIEW='front'

# Output directory 
OUTPUT_DIRECTORY='/data/circuits/cns-circuit/v2/renderings/'

# Orient the circuit upwards where the up vector is the Y axis, 'yes' or 'no'
ORIENT_CIRCUIT_UPWARDS='yes'

# Unify branch radii, 'yes' or 'no'
UNIFY_BRANCH_RADII='yes'

# Render a close-up of the circuit based on the somata positions, 'yes' or 'no'
RENDER_CLOSEUP='yes'

# Export the final mesh in a .BLEND file, 'yes' or 'no'
SAVE_BLENDER_SCENE='yes'

####################################################################################################
BOOL_ARGS=''
if [ "$SAVE_BLENDER_SCENE" == 'yes' ];
    then BOOL_ARGS+=' --save-blender-scene '; fi

if [ "$RENDER_CLOSEUP" == 'yes' ];
    then BOOL_ARGS+=' --render-closeup '; fi

if [ "$UNIFY_BRANCH_RADII" == 'yes' ];
    then BOOL_ARGS+=' --unify-branch-radii '; fi

if [ "$ORIENT_CIRCUIT_UPWARDS" == 'yes' ];
    then BOOL_ARGS+=' --orient-circuit-upwards '; fi


####################################################################################################
# NOTE: This is the command line and you can run it directly in a terminal. 
$BLENDER -b --verbose 0 --python circuit-renderer.py -- \
    --circuit-config="$CIRCUIT_CONFIG" \
    --population="$POPULATION" \
    --output-directory="$OUTPUT_DIRECTORY" \
    --image-resolution="$IMAGE_RESOLUTION" \
    --rendering-view="$RENDERING_VIEW" \
    --colormap-file="$COLORMAP_FILE" \
    $BOOL_ARGS
####################################################################################################

