####################################################################################################
# Copyright (c) 2023, EPFL / Blue Brain Project
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

# Internal imports
import nmv.bmeshi
import nmv.enums
import nmv.geometry
import nmv.mesh
import nmv.shading


####################################################################################################
# @create_color_coded_synapses_particle_system
####################################################################################################
def create_color_coded_synapses_particle_system(circuit,
                                                synapse_groups,
                                                synapse_radius=2,
                                                synapses_percentage=100,
                                                inverted_transformation=None,
                                                material_type=nmv.enums.Shader.LAMBERT_WARD):
    """Creates a color-coded mesh for a given list of synapses.

    :param circuit:
        BBP circuit.
    :param synapse_groups:
        An object of the SynapseGroup class containing the name of the group, its synapses IDs list
        and the color of the group in a Vector((R, G, B)) format.
    :param synapse_radius:
        The radius of the synapse in microns. By default, this value if 2.
    :param synapses_percentage:
        The percentage of the shown synapses.
    :param inverted_transformation:
        The inverse transformation to transform the synapses to the origin. If this is None, the
        synapses where will be located in the circuit global coordinates.
    :param material_type:
        The type of the material used to shade the resulting mesh.
    :return:
        A reference to the created synapse group particle system.
    """

    # For every group in the synapse list, create a mesh and color code it.
    for synapse_group in synapse_groups:

        # The post-synaptic position
        positions = circuit.get_post_synaptic_synapse_positions(
            synapse_ids_list=synapse_group.synapses_ids_list)

        # Update the positions taking into consideration the transformation
        for j in range(len(positions)):
            position = Vector((positions[j][0], positions[j][1], positions[j][2]))
            if inverted_transformation is not None:
                position = inverted_transformation @ position
            positions[j] = position

        # Create the material
        material = nmv.shading.create_material(
            name=synapse_group.name, color=synapse_group.color, material_type=material_type)

        # Sample the list
        number_synapses = int(len(positions) * synapses_percentage / 100.0)
        positions = random.sample(positions, number_synapses)

        # Create the vertices mesh
        vertices_mesh = nmv.bmeshi.convert_bmesh_to_mesh(
            bmesh_object=nmv.bmeshi.create_vertices(locations=positions), name=synapse_group.name)

        nmv.shading.set_material_to_object(mesh_object=vertices_mesh, material_reference=material)

        # Create the particle system
        return nmv.geometry.create_particle_system_for_vertices(
            mesh_object=vertices_mesh, name=synapse_group.name, vertex_radius=synapse_radius,
            material=material)
