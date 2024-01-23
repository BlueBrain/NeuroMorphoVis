#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2024, EPFL / Blue Brain Project
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

# Input directory
INPUT_DIRECTORY='/ssd2/biovis2024-data/nmv-output-aspiny/meshes'
INPUT_MESH='3512410.obj'

# Output directory
OUTPUT_DIRECTORY='/ssd2/biovis2024-data/nmv-output-aspiny/watertight_meshes'
OUTPUT_DIRECTORY='/hdd1/biovis-24-zenodo/verify/'


INPUT_DIRECTORY='/hdd1/biovis-24-zenodo/mtypes/L23_LBC/'
INPUT_MESH='L23_LBC.stl'
OUTPUT_DIRECTORY='/hdd1/biovis-24-zenodo/mtypes/L23_LBC/'

#####################################################################################################
BOOL_ARGS=' '

####################################################################################################
echo 'RUNNING ...'
$BLENDER -b --verbose 0 --python optimize_mesh.py --                                                \
    --input-directory=$INPUT_DIRECTORY                                                              \
    --input-mesh=$INPUT_MESH                                                                        \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    $BOOL_ARGS

echo 'DONE ...'

