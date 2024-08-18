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
# @create_partitions_materials
####################################################################################################
def create_partitions_materials(number_materials):

    # Load the base materials
    base_flat_opaque_material = nmv.shading.create_flat_material_cycles(
        name='Partition Material Base', transparent=False)
    base_flat_transparent_material = nmv.shading.create_flat_material_cycles(
        name='Partition Material Base', transparent=True)
    # Create 100 materials and randomly chose from them
    materials_pair = list()
    for i in range(number_materials):
        red = random.randint(0, 255) / 255.0
        green = random.randint(0, 255) / 255.0
        blue = random.randint(0, 255) / 255.0
        color = (red, green, blue)

        # Create the opaque material
        flat_opaque_material = nmv.shading.duplicate_flat_material_cycles(
            input_material=base_flat_opaque_material,
            name='Partition Material %d' % i, color=color)

        # Create the transparent material
        flat_transparent_material = nmv.shading.duplicate_flat_material_cycles(
            input_material=base_flat_transparent_material,
            name='Partition Material %d - Transparent' % i, color=color)

        # Create the materials pair and add it to the list
        materials_pair.append([flat_opaque_material, flat_transparent_material])

    # Return the list
    return materials_pair


####################################################################################################
# @assign_materials_to_partitions
####################################################################################################
def assign_materials_to_partitions(mesh_partitions,
                                   materials_pairs,
                                   assign_transparent=False):

    for i in range(len(mesh_partitions)):
        material_index = i % len(materials_pairs)
        materials_pair = materials_pairs[material_index]
        material = materials_pair[1] if assign_transparent else materials_pair[0]
        nmv.shading.set_material_to_object(mesh_partitions[i], material)



####################################################################################################
# @split_mesh_object_into_partitions
####################################################################################################
def split_mesh_object_into_partitions(mesh_object,
                                      color_partitions=True):
    """Splits the input mesh object into multiple partitions and color each partition with a
    random color.

    @param mesh_object:
        A given mesh object.
    @param color_partitions:
        If this flag is set, each partition will be randomly colored.
    @return:
        A list containing references to each partition as a single mesh object.
    """

    # Get all the partitions
    partitions = nmv.mesh.split_partitions_into_multiple_mesh_objects(mesh_object)
    print("The mesh contains [%d] partitions" % len(partitions))

    # Return a list of partitions
    return partitions
