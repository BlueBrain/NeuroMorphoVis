#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Input mesh
INPUT_MESH='/projects-data/2020.12.25-remeshing/input-meshes/nuclei/nucleus-1.obj'
INPUT_MESH='/projects-data/2020.12.25-remeshing/input-meshes/cow-simple.obj'

# Output directory
OUTPUT_DIRECTORY='/projects-data/2020.12.25-remeshing/output-meshes'

# Decimation factor (range: 0.5 - 0.01) to reduce the number of polygons in the mesh that is
# generated for the visualization purposes.
DECIMATION_FACTOR='0.1'

# Export the final mesh in a .OBJ file, 'yes' or 'no'
EXPORT_OBJ='yes'

# Export the final mesh in a .BLEND file, 'yes' or 'no'
EXPORT_BLEND='yes'

####################################################################################################
BOOL_ARGS=''
if [ "$EXPORT_OBJ" == 'yes' ];
    then BOOL_ARGS+=' --export-obj '; fi
if [ "$EXPORT_BLEND" == "yes" ];
    then BOOL_ARGS+=' --export-blend '; fi

####################################################################################################
$BLENDER -b --verbose 0 --python run.py --                                                         \
    --input-mesh=$INPUT_MESH                                                                        \
    --decimation-factor=$DECIMATION_FACTOR                                                          \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    $BOOL_ARGS
