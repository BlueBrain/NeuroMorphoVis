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
BLENDER=$PWD/../../../../../../blender

# The mesh that will be analyzed
MESH=''

# The directory where the results will be written
OUTPUT_DIRECTORY=''

####################################################################################################
echo 'ANALYZING MESH ...'

$BLENDER -b --verbose 0 --python analyze-mesh.py                                                                                   \
    --blender=$BLENDER                                                                              \
    --mesh=$MESH                                                                          \
    --output-directory=$OUTPUT_DIRECTORY

echo 'ANALYSIS DONE ...'

