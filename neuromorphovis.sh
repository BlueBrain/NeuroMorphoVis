#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# If no configuration file is provided, then report it and exit
if [ $# -eq 0 ]
	then echo "No configuration file is provided, EXITING!"; exit
fi

# Source the input configuration file to use the parameters 
echo "Using the configuration file [$1]"
source $1

#####################################################################################################
BOOL_ARGS=''
#####################################################################################################
# Ignoring Branches
if [ "$IGNORE_AXON" == "yes" ];
    then BOOL_ARGS+=' --ignore-axons '; fi
if [ "$IGNORE_BASAL_DENDRITES" == "yes" ];
    then BOOL_ARGS+=' --ignore-basal-dendrites '; fi
if [ "$IGNORE_APICAL_DENDRITES" == "yes" ];
    then BOOL_ARGS+=' --ignore-apical-dendrites '; fi
if [ "$CONNECT_SOMA_MESH_TO_ARBORS" == "yes" ];
    then BOOL_ARGS+=' --connect-soma-arbors'; fi
####################################################################################################
# Rendering parameters
if [ "$RENDER_SOMA_IMAGE" == "yes" ];
    then BOOL_ARGS+=' --render-soma-mesh '; fi
if [ "$RENDER_SOMA_PROGRESSIVE_SEQUENCE" == "yes" ];
    then BOOL_ARGS+=' --render-soma-mesh-progressive '; fi
if [ "$RENDER_SOMA_360_SEQUENCE" == "yes" ];
    then BOOL_ARGS+=' --render-soma-mesh-360 '; fi
if [ "$RENDER_NEURON_MORPHOLOGY_IMAGE" == "yes" ];
    then BOOL_ARGS+=' --render-neuron-morphology '; fi
if [ "$RENDER_NEURON_MORPHOLOGY_360_SEQUENCE" == "yes" ];
    then BOOL_ARGS+=' --render-neuron-morphology-360 '; fi
if [ "$RENDER_NEURON_MORPHOLOGY_PROGRESSIVE_SEQUENCE" == "yes" ];
    then BOOL_ARGS+=' --render-neuron-morphology-progressive '; fi
if [ "$RENDER_NEURON_MESH_IMAGE" == "yes" ];
    then BOOL_ARGS+=' --render-neuron-mesh '; fi
if [ "$RENDER_NEURON_MESH_360_SEQUENCE" == "yes" ];
    then BOOL_ARGS+=' --render-neuron-mesh-360 '; fi
if [ "$RENDER_IMAGES_TO_SCALE" == "yes" ];
    then BOOL_ARGS+=' --render-to-scale '; fi
if [ "$RENDER_SCALE_BAR" == "yes" ];
    then BOOL_ARGS+=' --render-scale-bar '; fi
####################################################################################################
# Morphology positioning parameters
if [ "$GLOBAL_COORDINATES" == "yes" ];
    then BOOL_ARGS+=' --global-coordinates '; fi
if [ "$ADD_NUCLEUS" == "yes" ];
    then BOOL_ARGS+=' --add-nucleus '; fi
####################################################################################################
# Export morphology
if [ "$EXPORT_NEURON_MORPHOLOGY_SWC" == "yes" ];
    then BOOL_ARGS+=' --export-morphology-swc'; fi
if [ "$EXPORT_NEURON_MORPHOLOGY_BLEND" == "yes" ];
    then BOOL_ARGS+=' --export-morphology-blend '; fi
if [ "#EXPORT_NEURON_MORPHOLOGY_SEGMENTS" == "yes" ];
    then BOOL_ARGS+=' --export-morphology-segments'; fi
####################################################################################################
# Export soma mesh
if [ "$EXPORT_SOMA_MESH_PLY" == "yes" ];
    then BOOL_ARGS+=' --export-soma-mesh-ply '; fi
if [ "$EXPORT_SOMA_MESH_OBJ" == "yes" ];
    then BOOL_ARGS+=' --export-soma-mesh-obj '; fi
if [ "$EXPORT_SOMA_MESH_STL" == "yes" ];
    then BOOL_ARGS+=' --export-soma-mesh-stl '; fi
if [ "$EXPORT_SOMA_MESH_BLEND" == "yes" ];
    then BOOL_ARGS+=' --export-soma-mesh-blend '; fi
####################################################################################################
# Export neuron mesh
if [ "$EXPORT_NEURON_MESH_PLY" == "yes" ];
    then BOOL_ARGS+=' --export-neuron-mesh-ply '; fi
if [ "$EXPORT_NEURON_MESH_OBJ" == "yes" ];
    then BOOL_ARGS+=' --export-neuron-mesh-obj '; fi
if [ "$EXPORT_NEURON_MESH_STL" == "yes" ];
    then BOOL_ARGS+=' --export-neuron-mesh-stl '; fi
if [ "$EXPORT_NEURON_MESH_BLEND" == "yes" ];
    then BOOL_ARGS+=' --export-neuron-mesh-blend '; fi
if [ "$EXPORT_INDIVIDUALS" == "yes" ];
    then BOOL_ARGS+=' --export-individuals '; fi
####################################################################################################
# Morphology analysis
if [ "$ANALYZE_MORPHOLOGY_SKELETON" == "yes" ];
    then BOOL_ARGS+=' --analyze-morphology '; fi

####################################################################################################
# echo 'FLAGS:' $BOOL_ARGS
echo -e "\nRUNNING ... NeuroMorphoVis \n"
    ../../../python/bin/python3.7m neuromorphovis.py                                                \
    --blender=$BLENDER_EXECUTABLE                                                                   \
    --input=$INPUT                                                                                  \
    --blue-config=$BLUE_CONFIG                                                                      \
    --gid=$GID                                                                                      \
    --target=$TARGET                                                                                \
    --morphology-file=$MORPHOLOGY_FILE                                                              \
    --morphology-directory=$MORPHOLOGY_DIRECTORY                                                    \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --morphology-reconstruction-algorithm=$MORPHOLOGY_RECONSTRUCTION_ALGORITHM                      \
    --morphology-skeleton-style=$SKELETON_STYLE                                                     \
    --morphology-color-coding=$MORPHOLOGY_COLOR_CODING_SCHEME                                       \
    --morphology-colormap=$MORPHOLOGY_COLORMAP                                                      \
    --meshing-algorithm=$MESHING_TECHNIQUE                                                          \
    --axon-branching-order=$MAX_AXON_BRANCHING_ORDER                                                \
    --basal-dendrites-branching-order=$MAX_BASAL_DENDRITES_BRANCHING_ORDER                          \
    --apical-dendrites-branching-order=$MAX_APICAL_DENDRITES_BRANCHING_ORDER                        \
    --soma-representation=$SOMA_REPRESENTATION                                                      \
    --soma-stiffness=$SOMA_STIFFNESS                                                                \
    --soma-subdivision-level=$SOMA_SUBDIVISION_LEVEL                                                \
    --edges=$EDGES                                                                                  \
    --surface=$SURFACE                                                                              \
    --spines=$SPINES                                                                                \
    --spines-quality=SPINES_QUALITY                                                                 \
    --number-spines-per-micron=$NUMBER_SPINES_PER_MICRON                                            \
    --soma-color=$SOMA_COLOR                                                                        \
    --axons-color=$AXON_COLOR                                                                       \
    --apical-dendrites-color=$APICAL_DENDRITE_COLOR                                                 \
    --basal-dendrites-color=$BASAL_DENDRITES_COLOR                                                  \
    --spines-color=$SPINES_COLOR                                                                    \
    --nucleus-color=$NUCLEUS_COLOR                                                                  \
    --samples-radii=$SAMPLES_RADII                                                                  \
    --radii-scale-factor=$RADII_SCALE_FACTOR                                                        \
    --unified-morphology-radius=$UNIFIED_SAMPLES_RADIUS                                             \
    --axon-radius=$AXON_RADIUS                                                                      \
    --apical-dendrites-radius=$APICAL_DENDRITES_RADIUS                                              \
    --basal-dendrites-radius=$BASAL_DENDRITES_RADIUS                                                \
    --bevel-sides=$SECTION_BEVEL_SIDES                                                              \
    --camera-view=$CAMERA_VIEW                                                                      \
    --rendering-view=$RENDERING_VIEW                                                                \
    --frame-resolution=$FRAME_RESOLUTION                                                            \
    --resolution-scale-factor=$RESOLUTION_SCALE_FACTOR                                              \
    --close-up-dimensions=$CLOSEUP_VIEW_DIMENSIONS                                                 \
    --image-file-format=$IMAGE_FILE_FORMAT                                                          \
    --shader=$SHADER                                                                                \
    --execution-node=$EXECUTION_NODE                                                                \
    --tessellation-level=$TESSELLATION_LEVEL                                                        \
    $BOOL_ARGS

echo -e "\nDONE ... NeuroMorphoVis \n"
####################################################################################################
