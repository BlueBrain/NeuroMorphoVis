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

# System imports
import random
import os
import sys

# Internal imports
import_paths = ['core']
for import_path in import_paths:
    sys.path.append(('%s/%s' % (os.path.dirname(os.path.realpath(__file__)), import_path)))

import circuit_data

# BBP imports
import bluepy
from bluepy.v2 import Circuit

# Blender
from mathutils import Vector, Matrix

# Internal imports
import nmv.bbox
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.geometry
import nmv.options
import nmv.mesh
import nmv.rendering
import nmv.scene
import nmv.shading
import nmv.utilities


####################################################################################################
# @create_synapses_mesh
####################################################################################################
def create_synapses_mesh(circuit,
                         gid,
                         synapse_size,
                         synapse_percentage,
                         inverted_transformation,
                         color_map_materials):
    """Creates a mesh of all the synapses

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param synapse_size:
        The size of the synapses.
    :param synapse_percentage:
        The percentage of the syanpses to be drawn.
    :param inverted_transformation:
        The inverted transformation that will take the synapses to the origin.
    :param color_map_materials:
        A dictionary of all the mtype materials.
    :return:
        A reference to the created synapse mesh.
    """

    spine_meshes = nmv.file.load_spines(nmv.consts.Paths.SPINES_MESHES_LQ_DIRECTORY)

    # Get the IDs of the afferent synapses of a given GID
    afferent_synapses_ids = circuit.connectome.afferent_synapses(gid)

    # Get the synapse type
    synapse_types = circuit.connectome.synapse_properties(
        afferent_synapses_ids, [bluepy.v2.enums.Synapse.TYPE]).values

    # Get the positions of the incoming synapses at the post synaptic side
    post_synaptic_positions = circuit.connectome.synapse_positions(
        afferent_synapses_ids, 'post', 'center').values.tolist()
    pre_synaptic_positions = circuit.connectome.synapse_positions(
        afferent_synapses_ids, 'pre', 'contour').values.tolist()

    # Get the GIDs of the pre-synaptic cells
    pre_gids = circuit.connectome.synapse_properties(
        afferent_synapses_ids, [bluepy.v2.enums.Synapse.PRE_GID]).values
    pre_synaptic_gids = [gid[0] for gid in pre_gids]

    # Get the pre-synaptic mtypes
    pre_synaptic_mtypes = circuit.cells.get(pre_synaptic_gids)['mtype'].values.tolist()

    # We need the color and the position to draw the synaptome
    synapse_objects = list()
    synapse_groups = list()

    x = list()
    # Do it for all the synapses
    for i in range(len(post_synaptic_positions)):

        # Show progress
        nmv.utilities.time_line.show_iteration_progress('Synapses', i, len(post_synaptic_positions))

        # Random selection
        if synapse_percentage < random.uniform(0, 100):
            continue

        # Material, only for afferent synapses, efferent ones should be create as spheres
        if not (pre_synaptic_mtypes[i] in color_map_materials):
            continue

        # Inhibitory synapse
        if synapse_types[i] < 100:

            # Post-synaptic position
            post_synaptic_position = Vector((post_synaptic_positions[i][0],
                                             post_synaptic_positions[i][1],
                                             post_synaptic_positions[i][2]))
            post_synaptic_position = inverted_transformation @ post_synaptic_position

            # A synapse sphere object
            spine_object = nmv.geometry.create_ico_sphere(
                radius=synapse_size, location=post_synaptic_position, subdivisions=3,
                name='synapse_%d' % i)

            # Material
            material = color_map_materials['INH']
            nmv.shading.set_material_to_object(mesh_object=spine_object,
                                               material_reference=material)
        # Excitatory
        else:

            material = color_map_materials[pre_synaptic_mtypes[i]]

            # Pre-synaptic position
            pre_synaptic_position = Vector((pre_synaptic_positions[i][0],
                                            pre_synaptic_positions[i][1],
                                            pre_synaptic_positions[i][2]))
            pre_synaptic_position = inverted_transformation @ pre_synaptic_position

            # Post-synaptic position
            post_synaptic_position = Vector((post_synaptic_positions[i][0],
                                             post_synaptic_positions[i][1],
                                             post_synaptic_positions[i][2]))
            post_synaptic_position = inverted_transformation @ post_synaptic_position

            # Select a random spine from the spines list
            spine_template = random.choice(spine_meshes)

            # Get a copy of the template and update it
            spine_object = nmv.scene.ops.duplicate_object(spine_template, i, link_to_scene=True)

            # Get the spine extent
            spine_extent = (post_synaptic_position - pre_synaptic_position).length

            # Scale the spine
            nmv.scene.ops.scale_object_uniformly(spine_object, synapse_size * 2)

            # Translate the spine to the post synaptic position
            nmv.scene.ops.set_object_location(spine_object, post_synaptic_position)

            # Rotate the spine towards the pre-synaptic point
            # We assume that the normal is heading towards to -Z axis for computing the rotation
            nmv.scene.ops.rotate_object_towards_target(
                spine_object, Vector((0, 0, -1)), pre_synaptic_position)

            # Material
            nmv.shading.set_material_to_object(mesh_object=spine_object,
                                               material_reference=material)

        # Add the sphere to the group
        synapse_objects.append(spine_object)

        # Group every 100 objects into a single group
        if i % 50 == 0:

            # Join the meshes into a group
            synapse_group = nmv.mesh.join_mesh_objects(
                mesh_list=synapse_objects, name='group_%d' % (i % 100))

            # Add the group to the list
            synapse_groups.append(synapse_group)

            # Clear the object list
            synapse_objects.clear()

    # Join the meshes into a group
    synapse_group = nmv.mesh.join_mesh_objects(
        mesh_list=synapse_objects, name='group_%d' % (i % 100))

    # Add the group to the list
    synapse_groups.append(synapse_group)

    # Done
    nmv.utilities.time_line.show_iteration_progress(
        'Synapses', len(post_synaptic_positions), len(post_synaptic_positions), done=True)

    # Join the meshes into a group
    synapses_mesh = nmv.mesh.join_mesh_objects(mesh_list=synapse_groups, name='synapses')

    # Return a reference to the synapse mesh
    return synapses_mesh


####################################################################################################
# @create_neuron_mesh
####################################################################################################
def create_neuron_mesh(circuit,
                       gid,
                       neuron_material):
    """Creates the mesh of the neuron.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param neuron_color:
        The color of the neuron in a RGB Vector((R, G, B)) format
    :return:
    """
    # Get the morphology file path from its GID
    # We must ensure that the GID is integer, that's why the cast is there
    h5_morphology_path = circuit.morph.get_filepath(int(gid))

    # Use the H5 morphology loader to load this file
    # Don't center the morphology, as it is assumed to be cleared and reviewed by the team
    h5_reader = nmv.file.H5Reader(h5_file=h5_morphology_path, center_morphology=False)
    morphology = h5_reader.read_file()

    # Adjust the label to be set according to the GID not the morphology label
    morphology.label = str(gid)

    # Create default NMV options
    nmv_options = nmv.options.NeuroMorphoVisOptions()
    nmv_options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.UNIFIED
    nmv_options.morphology.samples_unified_radii_value = 1.0
    nmv_options.shading.mesh_material = nmv.enums.shading_enums.Shader.FLAT

    # Create a meta balls meshing builder
    meta_builder = nmv.builders.MetaBuilder(morphology=morphology, options=nmv_options)

    # Create the neuron mesh
    neuron_mesh = meta_builder.reconstruct_mesh()

    # Add the material top the reconstructed mesh
    nmv.shading.set_material_to_object(mesh_object=neuron_mesh, material_reference=neuron_material)

    # Return a reference to the neuron mesh
    return neuron_mesh


####################################################################################################
# @create_synaptome
####################################################################################################
def create_synaptome(circuit_config,
                     gid,
                     synapse_size,
                     synapse_percentage,
                     synaptome_color_map_materials,
                     neuron_material):

    # Loading a circuit
    circuit = Circuit(circuit_config)

    # Get the cell transformation matrix
    transformation = circuit_data.get_cell_transformation(circuit=circuit, gid=gid)

    # Invert the transformation matrix
    inverted_transformation = transformation.inverted()

    # Neuron mtype
    mtype = circuit.cells.get(gid).mtype

    # Create neuron mesh
    neuron_mesh = create_neuron_mesh(circuit=circuit, gid=gid,
                                     neuron_material=neuron_material)

    # Create synapse mesh
    synapses_mesh = create_synapses_mesh(circuit=circuit, gid=gid,
                                         synapse_size=synapse_size,
                                         synapse_percentage=synapse_percentage,
                                         inverted_transformation=inverted_transformation,
                                         color_map_materials=synaptome_color_map_materials)

    # Merge
    synaptome_mesh = nmv.mesh.join_mesh_objects(
        mesh_list=[neuron_mesh, synapses_mesh], name='synaptome_%s_%d' % (mtype, gid))

    # Returns a reference to the synaptome mesh
    return synaptome_mesh
