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

# If no configuration file is provided, then report it and exit
if [ $# -eq 0 ]
	then echo "No configuration file is provided, EXITING!"; exit
fi

# Source the input configuration file to use the parameters 
echo "Using the configuration file [$1]"
source $1

#####################################################################################################
BOOL_ARGS=''
if [ "$RECONSTRUCT_MORPHOLOGY_SKELETON" == "yes" ];
    then BOOL_ARGS+=' --reconstruct-morphology-skeleton '; fi
if [ "$IGNORE_AXON" == "yes" ];
    then BOOL_ARGS+=' --ignore-axon '; fi
if [ "$IGNORE_BASAL_DENDRITES" == "yes" ];
    then BOOL_ARGS+=' --ignore-basal-dendrites '; fi
if [ "$IGNORE_APICAL_DENDRITES" == "yes" ];
    then BOOL_ARGS+=' --ignore-apical-dendrites '; fi
if [ "$RECONSTRUCT_SOMA_MESH" == "yes" ];
    then BOOL_ARGS+=' --reconstruct-soma-mesh '; fi
if [ "$RECONSTRUCT_NEURON_MESH" == "yes" ];
    then BOOL_ARGS+=' --reconstruct-neuron-mesh '; fi
if [ "$CONNECT_SOMA_MESH_TO_ARBORS" == "yes" ];
    then BOOL_ARGS+=' --connect-soma-arbors'; fi
if [ "$CONNECT_NEURON_OBJECTS_INTO_SINGLE_MESH" == "yes" ];
    then BOOL_ARGS+=' --joint-neuron-meshes'; fi
####################################################################################################
# Rendering parameters
if [ "$RENDER_SOMA_SKELETON" == "yes" ];
    then BOOL_ARGS+=' --render-soma-skeleton '; fi
if [ "$RENDER_SOMA_MESH" == "yes" ];
    then BOOL_ARGS+=' --render-soma-mesh '; fi
if [ "$RENDER_SOMA_MESH_PROGRESSIVE" == "yes" ];
    then BOOL_ARGS+=' --render-soma-mesh-progressive '; fi
if [ "$RENDER_SOMA_MESH_360" == "yes" ];
    then BOOL_ARGS+=' --render-soma-mesh-360 '; fi
if [ "$RENDER_NEURON_MORPHOLOGY" == "yes" ];
    then BOOL_ARGS+=' --render-neuron-morphology '; fi
if [ "$RENDER_NEURON_MORPHOLOGY_360" == "yes" ];
    then BOOL_ARGS+=' --render-neuron-morphology-360 '; fi
if [ "$RENDER_NEURON_MORPHOLOGY_PROGRESSIVE" == "yes" ];
    then BOOL_ARGS+=' --render-neuron-morphology-progressive '; fi
if [ "$RENDER_NEURON_MESH" == "yes" ];
    then BOOL_ARGS+=' --render-neuron-mesh '; fi
if [ "$RENDER_NEURON_MESH_360" == "yes" ];
    then BOOL_ARGS+=' --render-neuron-mesh-360 '; fi
if [ "$RENDER_TO_SCALE" == "yes" ];
    then BOOL_ARGS+=' --render-to-scale '; fi
####################################################################################################
# Mesh parameters
if [ "$GLOBAL_COORDINATES" == "yes" ];
    then BOOL_ARGS+=' --global-coordinates '; fi
if [ "$ADD_NUCLEUS" == "yes" ];
    then BOOL_ARGS+=' --add-nucleus '; fi
####################################################################################################
# Export morphology
if [ "$EXPORT_NEURON_MORPHOLOGY_H5" == "yes" ];
    then BOOL_ARGS+=' --export-morphology-h5'; fi
if [ "$EXPORT_NEURON_MORPHOLOGY_SWC" == "yes" ];
    then BOOL_ARGS+=' --export-morphology-swc'; fi
if [ "$EXPORT_NEURON_MORPHOLOGY_BLEND" == "yes" ];
    then BOOL_ARGS+=' --export-morphology-blend '; fi
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
    python2.7 neuromorphovis.py                                                                     \
    --blender=$BLENDER_EXECUTABLE                                                                   \
    --input=$INPUT                                                                                  \
    --blue-config=$BLUE_CONFIG                                                                      \
    --gid=$GID                                                                                      \
    --target=$TARGET                                                                                \
    --morphology-file=$MORPHOLOGY_FILE                                                              \
    --morphology-directory=$MORPHOLOGY_DIRECTORY                                                    \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --morphology-reconstruction-algorithm=$MORPHOLOGY_RECONSTRUCTION_ALGORITHM                      \
    --morphology-skeleton=$SKELETON                                                                 \
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
    --random-spines-percentage=$RANDOM_SPINES_PERCENTAGE                                            \
    --soma-color=$SOMA_COLOR                                                                        \
    --axon-color=$AXON_COLOR                                                                        \
    --apical-dendrites-color=$APICAL_DENDRITE_COLOR                                                 \
    --basal-dendrites-color=$BASAL_DENDRITES_COLOR                                                  \
    --spines-color=$SPINES_COLOR                                                                    \
    --nucleus-color=$NUCLEUS_COLOR                                                                  \
    --sections-radii=$SET_SECTION_RADII                                                             \
    --radii-scale-factor=$RADII_SCALE_FACTOR                                                        \
    --fixed-section-radius=$FIXED_SECTION_RADIUS                                                    \
    --bevel-sides=$SECTION_BEVEL_SIDES                                                              \
    --camera-view=$CAMERA_VIEW                                                                      \
    --rendering-view=$RENDERING_VIEW                                                                \
    --full-view-resolution=$FULL_VIEW_FRAME_RESOLUTION                                              \
    --resolution-scale-factor=$FULL_VIEW_SCALE_FACTOR                                               \
    --close-up-resolution=$CLOSE_UP_FRAME_RESOLUTION                                                \
    --close-up-dimensions=$CLOSE_UP_VIEW_DIMENSIONS                                                 \
    --shader=$SHADER                                                                                \
    --execution-node=$EXECUTION_NODE                                                                \
    --tessellation-level=$TESSELLATION_LEVEL                                                        \
    --number-cores=$NUMBER_CORES                                                                    \
    $BOOL_ARGS

echo -e "\nDONE ... NeuroMorphoVis \n"
####################################################################################################
