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
import numpy
import random
from tqdm import tqdm

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.bmeshi
import nmv.enums
import nmv.mesh
import nmv.geometry
import nmv.shading
import nmv.utilities


####################################################################################################
# @create_synapses_mesh_using_spheres
####################################################################################################
def create_synapses_mesh_using_spheres(positions,
                                       synapse_radius,
                                       mesh_name='synapses',
                                       sphere_subdivisions=1):
    """Creates an aggregate mesh for all the synapses given in the positions array.
    Note that this function might take quite some time to create all the synapses due to the
    limitations of Python and Blender.

    :param positions:
        A list of Vectors containing the XYZ coordinates of the synapses.
    :param synapse_radius:
        The unified radius of all the synapses in microns.
    :param mesh_name:
        The name of the resulting mesh.
    :param sphere_subdivisions:
        The number of subdivisions of the spheres. By default, it is 2.
    :return:
        A reference to the created synapse mesh.
    """

    # NOTE: We create two lists, one to collect objects per iteration and another to collect the
    # aggregated objects to end up with a single mesh object that can be shaded later in an easy way
    all_synapse_objects = list()
    per_iteration_synapse_objects = list()

    for i in range(len(positions)):

        # Create a sphere representing the synapse and append it to the list
        #synapse_symbolic_sphere = nmv.geometry.create_ico_sphere(
        #    radius=synapse_radius, location=positions[i], subdivisions=sphere_subdivisions,
        #    name='synapse_%d' % i)
        synapse_symbolic_sphere = nmv.geometry.create_vertex_mesh(location=positions[i],name='a')
        per_iteration_synapse_objects.append(synapse_symbolic_sphere)

        # NOTE: To reduce to overhead of the number of objects in the scene, we group every few
        # objects into a single object
        if i % 100 == 0:
            all_synapse_objects.append(nmv.mesh.join_mesh_objects(
                mesh_list=per_iteration_synapse_objects, name='group_%d' % (i % 100)))

            # Clear the per-iteration list
            per_iteration_synapse_objects.clear()

    # If the per-iteration list still have some synapses, append them
    if len(per_iteration_synapse_objects) == 0:
        pass
    elif len(per_iteration_synapse_objects) == 1:
        all_synapse_objects.append(per_iteration_synapse_objects[0])
    else:
        all_synapse_objects.append(nmv.mesh.join_mesh_objects(
            mesh_list=per_iteration_synapse_objects, name='group_n'))

    # Join all the synapse objects into a single mesh
    all_synapse_objects = nmv.mesh.join_mesh_objects(mesh_list=all_synapse_objects,
                                                     name=mesh_name)
    # Return a reference to the collected synapses
    return all_synapse_objects


####################################################################################################
# @create_color_coded_synapses_mesh
####################################################################################################
def create_color_coded_synapses_mesh(circuit,
                                     synapse_groups,
                                     synapse_radius=4,
                                     inverted_transformation=None,
                                     material_type=nmv.enums.Shader.LAMBERT_WARD):
    """Creates a color-coded mesh for a given list of synapses.

    :param circuit:
        BBP circuit.
    :param synapse_groups:
        An object of the SynapseGroup class containing the name of the group, its synapses IDs list
        and the color of the group in a Vector((R, G, B)) format.
    :param synapse_radius:
        The radius of the synapse in microns. By default, this value if 4.
    :param inverted_transformation:
        The inverse transformation to transform the synapses to the origin. If this is None, the
        synapses where will be located in the circuit global coordinates.
    :param material_type:
        The type of the material used to shade the resulting mesh.
    :return:
        A reference to the created mesh.
    """

    # For every group in the synapse list, create a mesh and color code it.
    for synapse_group in tqdm(synapse_groups):

        # The post-synaptic position
        positions = circuit.connectome.synapse_positions(
            numpy.array(synapse_group.synapses_ids_list), 'post', 'center').values.tolist()

        # Update the positions taking into consideration the transformation
        for j in range(len(positions)):
            position = Vector((positions[j][0], positions[j][1], positions[j][2]))
            if inverted_transformation is not None:
                position = inverted_transformation @ position
            positions[j] = position

        # Create the corresponding synapses mesh
        synapse_group_mesh = create_synapses_mesh_using_spheres(
            positions=positions, synapse_radius=synapse_radius, mesh_name=synapse_group.name)

        # Create the corresponding shader
        material = nmv.shading.create_material(
            name=synapse_group.name, color=synapse_group.color, material_type=material_type)
        nmv.shading.set_material_to_object(
            mesh_object=synapse_group_mesh, material_reference=material)


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
        A reference to the created mesh.
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
        synapse_group_particle_system = nmv.geometry.create_particle_system_for_vertices(
            mesh_object=vertices_mesh, name=synapse_group.name, vertex_radius=synapse_radius,
            material=material)




