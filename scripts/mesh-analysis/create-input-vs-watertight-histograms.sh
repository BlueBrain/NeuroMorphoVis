#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2021, EPFL / Blue Brain Project
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
BLENDER=$PWD/../../../../../../blender

# Input directory
INPUT_DIRECTORY='/ssd2/ultraliser/2021.10.29-eyewire-h5-meshes/pyramidals/meshes/scaled'
INPUT_DIRECTORY='/ssd2/microns/janelia-flyem-hemibrain/large'
INPUT_DIRECTORY='/ssd2/microns/h01-data/l3_neuron_spiny_stellate/scaled'
INPUT_DIRECTORY='/ssd2/ultraliser/kaust/astrocyte-4'
INPUT_DIRECTORY='/ssd2/ultraliser/kaust/selected-meshes-for-analysis/astrocytes-er'
INPUT_DIRECTORY='/ssd2/ultraliser-figures/microns-pyramidal/input/meshes'

# Output directory
OUTPUT_DIRECTORY='/ssd2/ultraliser-figures/microns-pyramidal/input/analysis'

# ultraMes2Mesh executable
ULTRA_MESH2MESH='ultraMesh2Mesh'

# Voxel resolution
VOXELS_PER_MICRON=5

# Mesh scale
MESH_SCALE=1

# Statistics are ready
STATS_READY='no'

#####################################################################################################
BOOL_ARGS=''
if [ "$STATS_READY" == "yes" ];
    then BOOL_ARGS+=' --stats-ready '; fi

####################################################################################################
echo 'RUNNING ...'
$BLENDER -b --verbose 0 --python create-input-vs-watertight-histograms.py --                        \
    --input-directory=$INPUT_DIRECTORY                                                              \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --ultraMesh2Mesh=$ULTRA_MESH2MESH                                                               \
    --mesh-scale=$MESH_SCALE                                                                        \
    --voxels-per-micron=$VOXELS_PER_MICRON                                                          \
    $BOOL_ARGS

echo 'DONE ...'

