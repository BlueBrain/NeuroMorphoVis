####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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

import random
import nmv.mesh
import nmv.scene
import nmv.shading


####################################################################################################
# @split_mesh_object_into_partitions
####################################################################################################
def split_mesh_object_into_partitions(mesh_object,
                                      color_partitions=True):

    # Get all the partitions
    partitions = nmv.mesh.split_partitions_into_multiple_mesh_objects(mesh_object)

    # Color every partition with a random color
    if color_partitions:
        for i in range(len(partitions)):
            red = random.randint(0, 255) / 255.0
            green = random.randint(0, 255) / 255.0
            blue = random.randint(0, 255) / 255.0
            color = (red, green, blue)
            material = nmv.shading.create_flat_material('Material %d' % i,  color)
            nmv.shading.set_material_to_object(partitions[i], material)

    print("The mesh contains [%d] partitions" % len(partitions))

    # Return a list of partitions
    return partitions
