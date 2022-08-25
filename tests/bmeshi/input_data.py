####################################################################################################
# Copyright (c) 2016 - 2022, EPFL / Blue Brain Project
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

# System imports 
import random 

# Blender imports 
from mathutils import Vector 


####################################################################################################
# @get_exact_locations
####################################################################################################
def get_exact_locations():
    return [Vector((0.0, 0.0, 0.0)), 
            Vector((0.25, 0.25, 0.25)),
            Vector((0.5, 0.5, 0.5)),
            Vector((0.75, 0.75, 0.75)),
            Vector((1.0, 1.0, 1.0))]

####################################################################################################
# @get_random_locations
####################################################################################################
def get_random_locations(extent=5.0):
    random_locations = list()
    for i in range(5):
        x = random.uniform(-extent, extent)
        y = random.uniform(-extent, extent)
        z = random.uniform(-extent, extent)
        random_locations.append(Vector((x, y, z)))
    return random_locations
