####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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

# Blender imports
import bpy

# Internal imports
import nmv
import nmv.enums
import nmv.geometry
import nmv.mesh
import nmv.shading
import nmv.skeleton
import nmv.utilities


####################################################################################################
# @create_skeleton_materials
####################################################################################################
def create_skeleton_materials(builder):
    """Create the materials that will be used to shade the different object from a given builder.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    """

    # Delete the old materials
    for material in bpy.data.materials:
        if 'soma_skeleton' in material.name or              \
           'axon_skeleton' in material.name or              \
           'basal_dendrites_skeleton' in material.name or   \
           'apical_dendrite_skeleton' in material.name or   \
           'spines' in material.name:

            # Clear
            material.user_clear()

            # Remove
            bpy.data.materials.remove(material)

    # Soma
    builder.soma_materials = nmv.shading.create_materials(
        material_type=builder.options.mesh.material, name='soma_skeleton',
        color=builder.options.mesh.soma_color)

    # Axon
    builder.axon_materials = nmv.shading.create_materials(
        material_type=builder.options.mesh.material, name='axon_skeleton',
        color=builder.options.mesh.axon_color)

    # Basal dendrites
    builder.basal_dendrites_materials = nmv.shading.create_materials(
        material_type=builder.options.mesh.material, name='basal_dendrites_skeleton',
        color=builder.options.mesh.basal_dendrites_color)

    # Apical dendrite
    builder.apical_dendrites_materials = nmv.shading.create_materials(
        material_type=builder.options.mesh.material, name='apical_dendrite_skeleton',
        color=builder.options.mesh.apical_dendrites_color)

    # Spines
    builder.spines_materials = nmv.shading.create_materials(
        material_type=builder.options.mesh.material,
        name='spines', color=builder.options.mesh.spines_color)

    # Create an illumination specific for the given material
    nmv.shading.create_material_specific_illumination(builder.options.mesh.material)


####################################################################################################
# @modify_morphology_skeleton
####################################################################################################
def modify_morphology_skeleton(builder):
    """Modifies the morphology skeleton, if required. These modifications are generic and not
    specific to any builder. Specific modifications can be implemented as a function in the
    corresponding builder.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    """

    # Taper the sections if requested
    if builder.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED or \
       builder.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED_ZIGZAG:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[builder.morphology, nmv.skeleton.ops.taper_section])

    # Zigzag the sections if required
    if builder.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.ZIGZAG or \
       builder.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED_ZIGZAG:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[builder.morphology, nmv.skeleton.ops.zigzag_section])


####################################################################################################
# @reconstruct_soma_mesh
####################################################################################################
def reconstruct_soma_mesh(builder):
    """Reconstruct the mesh of the soma.

    NOTE: To improve the performance of the soft body physics simulation, reconstruct the
    soma profile before the arbors, such that the scene is almost empty.

    NOTE: If the soma is requested to be connected to the initial segments of the arbors,
    we must use a high number of subdivisions to make smooth connections that look nice,
    but if the arbors are connected to the soma origin, then we can use less subdivisions
    since the soma will not be connected to the arbor at all.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    """

    # If the soma is connected to the root arbors
    soma_builder_object = nmv.builders.SomaBuilder(
        morphology=builder.morphology, options=builder.options, irregular_subdivisions=True)

    # Reconstruct the soma mesh
    builder.soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

    # Apply the shader to the reconstructed soma mesh
    nmv.shading.set_material_to_object(builder.soma_mesh, builder.soma_materials[0])


####################################################################################################
# @get_neuron_mesh_objects
####################################################################################################
def get_neuron_mesh_objects(builder,
                            exclude_spines=False):
    """Gets a list of all the objects that belong to the neuron mesh. If all the objects are all
    connected into a single object, it will be returned as a single item in a list.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    :param exclude_spines:
        Exclude the spine meshes from this selection since they have a very special treatment.
    :return:
        A list of all the mesh objects that belong to the neuron
    """

    # Prepare the list
    neuron_mesh_objects = list()

    # Query the objects in the scene
    for scene_object in bpy.context.scene.objects:

        # Only select meshes
        if scene_object.type == 'MESH':

            # Exclude the spines
            if not exclude_spines:
                if 'spine' in scene_object.name:
                    neuron_mesh_objects.append(scene_object)

            if 'Apical' in scene_object.name or \
               'Basal' in scene_object.name or \
               'Axon' in scene_object.name or \
               'soma' in scene_object.name or \
                 builder.morphology.label in scene_object.name:
                neuron_mesh_objects.append(scene_object)

    # Return the list
    return neuron_mesh_objects


####################################################################################################
# @adjust_texture_mapping
####################################################################################################
def adjust_texture_mapping(mesh_objects,
                           texspace_size=5.0):
    """Adjusts the UV mapping of the meshes. This operation is recommended to be called after
    any mesh operation.

    :param mesh_objects:
        A list of meshes.
    :param texspace_size:
        Texture space size, by default 5.0.
    """

    nmv.logger.header('UV Mapping')

    # Do it mesh by mesh
    for i, mesh_object in enumerate(mesh_objects):

        # Adjust the size
        nmv.shading.adjust_material_uv(mesh_object, size=texspace_size)

        # Show the progress
        nmv.utilities.show_progress(
            '* Adjusting the UV mapping', float(i), float(len(mesh_objects)))

    # Show the progress
    nmv.utilities.show_progress('* Adjusting the UV mapping', 0, 0, done=True)


####################################################################################################
# @adjust_texture_mapping_of_all_meshes
####################################################################################################
def adjust_texture_mapping_of_all_meshes(builder, texspace_size=5.0):
    """Adjusts the UV mapping of the meshes. This operation is recommended to be called after
    any mesh operation.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.

    :param texspace_size:
        Texture space size, by default 5.0.
    """

    # Get a list of all the neurons in the scene
    mesh_objects = get_neuron_mesh_objects(builder=builder, exclude_spines=False)

    # Adjust the mapping of all the meshes
    adjust_texture_mapping(mesh_objects=mesh_objects, texspace_size=texspace_size)


####################################################################################################
# @connect_arbors_to_soma
####################################################################################################
def connect_arbors_to_soma(builder):
    """Connects the root section of a given arbor to the soma at its initial segment.

    This function checks if the arbor mesh is 'logically' connected to the soma or not,
    following to the initial validation steps that determines if the arbor has a valid
    connection point to the soma or not.
    If the arbor is 'logically' connected to the soma, this function returns immediately.
    The arbor is a Section object, see Section() @ section.py.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    """

    if builder.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
        nmv.logger.header('Connecting arbors to soma')

        # Connecting apical dendrite
        if not builder.options.morphology.ignore_apical_dendrite:

            # There is an apical dendrite
            if builder.morphology.apical_dendrite is not None:
                nmv.logger.info('Apical dendrite')
                nmv.skeleton.ops.connect_arbor_to_soma(builder.soma_mesh,
                                                       builder.morphology.apical_dendrite)

        # Connecting basal dendrites
        if not builder.options.morphology.ignore_basal_dendrites:

            # Create the apical dendrite mesh
            if builder.morphology.dendrites is not None:

                # Do it dendrite by dendrite
                for i, basal_dendrite in enumerate(builder.morphology.dendrites):
                    nmv.logger.info('Dendrite [%d]' % i)
                    nmv.skeleton.ops.connect_arbor_to_soma(builder.soma_mesh, basal_dendrite)

        # Connecting axon
        if not builder.options.morphology.ignore_axon:

            # Create the apical dendrite mesh
            if builder.morphology.axon is not None:
                nmv.logger.info('Axon')
                nmv.skeleton.ops.connect_arbor_to_soma(builder.soma_mesh, builder.morphology.axon)

    # Adjust the texture mapping after connecting the meshes together
    adjust_texture_mapping_of_all_meshes(builder=builder)


################################################################################################
# @decimate_neuron_mesh
################################################################################################
def decimate_neuron_mesh(builder):
    """Decimates the reconstructed neuron mesh.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    """

    # Ensure that the tessellation level is within range
    if 0.01 < builder.options.mesh.tessellation_level < 1.0:
        nmv.logger.header('Decimating Mesh')

        # Get neuron objects
        neuron_mesh_objects = get_neuron_mesh_objects(builder=builder, exclude_spines=True)

        # Do it mesh by mesh
        for i, neuron_mesh_object in enumerate(neuron_mesh_objects):

            # Show the progress
            nmv.utilities.show_progress(
                '* Decimating the mesh', float(i), float(len(neuron_mesh_objects)))

            # Decimate each mesh object
            nmv.mesh.ops.decimate_mesh_object(
                mesh_object=neuron_mesh_object,
                decimation_ratio=builder.options.mesh.tessellation_level)

        # Show the progress
        nmv.utilities.show_progress('* Decimating the mesh', 0, 0, done=True)

        # Adjust the texture mapping
        adjust_texture_mapping(neuron_mesh_objects)


####################################################################################################
# @add_surface_noise_to_arbor
####################################################################################################
def add_surface_noise_to_arbor(builder):
    """Adds noise to the surface of the arbors of the reconstructed mesh(es).

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    """

    if builder.options.mesh.surface == nmv.enums.Meshing.Surface.ROUGH:
        nmv.logger.header('Adding surface roughness to arbors')

        # Get a list of all the meshes of the reconstructed arbors
        mesh_objects = get_neuron_mesh_objects(builder=builder)

        # The soma is already reconstructed with high number of subdivisions for accuracy,
        # and the arbors are reconstructed with minimal number of samples that is sufficient to
        # make them smooth. Therefore, we must add the noise around the soma and its connections
        # to the arbors (the stable extent) with a different amplitude.
        stable_extent_center, stable_extent_radius = nmv.skeleton.ops.get_stable_soma_extent(
            builder.morphology)

        # Apply the operation to every mesh object in the list
        for mesh_object in mesh_objects:

            # Apply the noise addition filter
            for i in range(len(mesh_object.data.vertices)):
                vertex = mesh_object.data.vertices[i]
                if nmv.geometry.ops.is_point_inside_sphere(
                        stable_extent_center, stable_extent_radius, vertex.co):
                    if nmv.geometry.ops.is_point_inside_sphere(
                            stable_extent_center, builder.morphology.soma.smallest_radius,
                            vertex.co):
                        vertex.select = True
                        vertex.co = vertex.co + (vertex.normal * random.uniform(0, 0.1))
                        vertex.select = False
                    else:
                        if 0.0 < random.uniform(0, 1.0) < 0.1:
                            vertex.select = True
                            vertex.co = vertex.co + (vertex.normal * random.uniform(-0.1, 0.3))
                            vertex.select = False
                else:

                    value = random.uniform(-0.1, 0.1)
                    if 0.0 < random.uniform(0, 1.0) < 0.045:
                        value += random.uniform(0.05, 0.1)
                    elif 0.045 < random.uniform(0, 1.0) < 0.06:
                        value += random.uniform(0.2, 0.4)
                    vertex.select = True
                    vertex.co = vertex.co + (vertex.normal * value)
                    vertex.select = False

            # Deselect all the vertices
            nmv.mesh.ops.deselect_all_vertices(mesh_object=mesh_object)

            # Decimate each mesh object
            nmv.mesh.ops.decimate_mesh_object(mesh_object=mesh_object, decimation_ratio=0.5)

            # Smooth each mesh object
            nmv.mesh.ops.smooth_object(mesh_object=mesh_object, level=1)


####################################################################################################
# @add_spines_to_surface
####################################################################################################
def add_spines_to_surface(builder,
                          join_spine_meshes=False):
    """Adds spines meshes to the surface mesh of the neuron.

    NOTE: The spines will just be added to the surface, but they will not get merged to the surface
    with any union operator.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    :param join_spine_meshes:
        Join all the spines meshes into a single mesh object for simplicity.
    """

    # Build spines from a BBP circuit
    if builder.options.mesh.spines == nmv.enums.Meshing.Spines.Source.CIRCUIT:
        nmv.logger.header('Adding Spines from a BBP Circuit')
        spines_objects = nmv.builders.build_circuit_spines(
            morphology=builder.morphology, blue_config=builder.options.morphology.blue_config,
            gid=builder.options.morphology.gid, material=builder.spines_materials[0])

    # Just add some random spines for the look only
    elif builder.options.mesh.spines == nmv.enums.Meshing.Spines.Source.RANDOM:
        nmv.logger.header('Adding Random Spines')
        spines_builder = nmv.builders.RandomSpineBuilder(
            morphology=builder.morphology, options=builder.options)
        spines_objects = spines_builder.add_spines_to_morphology()

    # Otherwise ignore spines
    else:
        return

    # Join the spine objects into a single mesh, if required
    if join_spine_meshes:
        spine_mesh_name = '%s_spines' % builder.options.morphology.label
        nmv.mesh.join_mesh_objects(spines_objects, spine_mesh_name)


####################################################################################################
# @join_mesh_object_into_single_object
####################################################################################################
def join_mesh_object_into_single_object(builder):
    """Join all the mesh objects in the scene into a single mesh.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    :return:
        A reference to the joint mesh.
    """

    # Build spines from a BBP circuit
    if builder.options.mesh.neuron_objects_connection == \
       nmv.enums.Meshing.ObjectsConnection.CONNECTED:

        # Get a list of all the neuron mesh objects
        mesh_objects = get_neuron_mesh_objects(builder=builder)

        # Join them into a single object
        joint_mesh = nmv.mesh.join_mesh_objects(mesh_objects, builder.options.morphology.label)

        # Return a reference to the joint mesh object
        return joint_mesh


####################################################################################################
# @collect_morphology_stats
####################################################################################################
def collect_morphology_stats(builder):
    """Collects the stats. of the morphology skeleton.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    """

    nmv.logger.header('Collecting Morphology Stats.')

    builder.morphology_statistics += '\tSoma: ' + 'Found \n' \
        if builder.morphology.soma is not None else 'Not Found \n'
    if builder.morphology.apical_dendrite is not None:
        builder.morphology_statistics += '\tApical Dendrite: 1 \n'
    else:
        builder.morphology_statistics += '\tApical Dendrite: 0 \n'

    if builder.morphology.dendrites is not None:
        builder.morphology_statistics += '\tBasal Dendrites: %d \n' \
                                         % len(builder.morphology.dendrites)
    else:
        builder.morphology_statistics += '\t* Basal Dendrites: 0 \n'

    if builder.morphology.axon is not None:
        builder.morphology_statistics += '\tAxon: 1 \n'
    else:
        builder.morphology_statistics += '\tAxon: 0 \n'


####################################################################################################
# @collect_mesh_stats
####################################################################################################
def collect_mesh_stats(builder):
    """Collects the stats. of the reconstructed mesh.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    """

    nmv.logger.header('Collecting Mesh Stats.')

    # Get neuron objects
    neuron_mesh_objects = get_neuron_mesh_objects(builder=builder, exclude_spines=False)

    total_vertices = 0
    total_polygons = 0

    # Do it mesh by mesh
    for i, neuron_mesh_object in enumerate(neuron_mesh_objects):

        vertices = len(neuron_mesh_object.data.vertices)
        polygons = len(neuron_mesh_object.data.polygons)

        total_vertices += vertices
        total_polygons += polygons

        builder.mesh_statistics += '\t' + neuron_mesh_object.name + \
            ': Polygons [%d], ' % polygons + 'Vertices [%d] \n' % vertices

    builder.mesh_statistics += \
        '\tTotal : Polygons [%d], ' % total_polygons + 'Vertices [%d] \n' % total_vertices


####################################################################################################
# @write_statistics_to_file
####################################################################################################
def write_statistics_to_file(builder, tag):
    """Write the profiling stats. and also the mesh stats to file.

    :param tag:
        A label that will be used to tag the stats. file.
    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    """

    # Collect the morphology stats.
    collect_morphology_stats(builder)

    # Write the stats to file
    if builder.options.io.statistics_directory is None:
        output_directory = os.getcwd()
    else:
        output_directory = builder.options.io.statistics_directory
    stats_file = open('%s/%s-%s.stats' % (output_directory, builder.morphology.label, tag), 'w')

    stats_file.write(builder.morphology_statistics)
    stats_file.write('\n')
    stats_file.write(builder.profiling_statistics)
    stats_file.write('\n')
    stats_file.write(builder.mesh_statistics)

    stats_file.close()


####################################################################################################
# @transform_to_global_coordinates
####################################################################################################
def transform_to_global_coordinates(builder):
    """Transforms the neuron mesh to the global coordinates.

    NOTE: Spine transformation is already implemented by the spine builder, and therefore
    this function applies only to the arbors and the soma.

    :param builder:
        An object of the builder that is used to reconstruct the neuron mesh.
    """

    # Transform the neuron object to the global coordinates
    if builder.options.mesh.global_coordinates:
        
        # Make sure that a GID is selected 
        if builder.options.morphology.gid is None:
            return 

        nmv.logger.header('Transforming to global coordinates')
        
        # Get neuron objects
        neuron_mesh_objects = get_neuron_mesh_objects(builder=builder, exclude_spines=False)

        # Do it mesh by mesh
        for i, neuron_mesh_object in enumerate(neuron_mesh_objects):

            # Show the progress
            nmv.utilities.show_progress(
                '* Transforming to global coordinates', float(i), float(len(neuron_mesh_objects)))

            # Transforming to global coordinates 
            nmv.skeleton.ops.transform_to_global_coordinates(
                mesh_object=neuron_mesh_object, blue_config=builder.options.morphology.blue_config,
                gid=builder.options.morphology.gid)

        # Show the progress
        nmv.utilities.show_progress('* Decimating the mesh', 0, 0, done=True)


################################################################################################
# @update_samples_indices_per_arbor
################################################################################################
def update_samples_indices_per_arbor(section,
                                     index,
                                     max_branching_order):
    """Updates the global indices of all the samples along the given section.

    Note: This global index of the sample w.r.t to the arbor it belongs to.

    :param section:
        A given section to update the indices of its samples.
    :param index:
        A list that contains a single value that account for the index of the arbor.
        Note that we use this list as a trick to update the index value.
    :param max_branching_order:
        The maximum branching order of the arbor requested by the user.
    """

    # If the order goes beyond the maximum requested by the user, ignore the remaining samples
    if section.branching_order > max_branching_order:
        return

    # If the given section is root
    if section.is_root():

        # Update the arbor index of the first sample
        section.samples[0].arbor_idx = index[0]

        # Increment the index value
        index[0] += 1

    else:

        # The index of the root is basically the same as the index of the last sample of the
        # parent arbor
        section.samples[0].arbor_idx = section.parent.samples[-1].arbor_idx

    # Update the indices of the rest of the samples along the section
    for i in range(1, len(section.samples)):

        # Set the arbor index of the current sample
        section.samples[i].arbor_idx = index[0]

        # Increment the index
        index[0] += 1

    # Update the children sections recursively
    for child in section.children:
        update_samples_indices_per_arbor(child, index, max_branching_order)


################################################################################################
# @select_vertex
################################################################################################
def select_vertex(vertex_idx):
    """Selects a vertex along a morphology path using its index during the skinning process.

    :param vertex_idx:
        The index of the vertex that needs to be selected.
    """

    # Set the current mode to the object mode
    # bpy.ops.object.mode_set(mode='OBJECT')

    # Select the active object (that is supposed to be the arbor being created)
    obj = bpy.context.active_object

    # Switch to the edit mode
    # bpy.ops.object.mode_set(mode='EDIT')

    # Switch to the vertex mode
    bpy.ops.mesh.select_mode(type="VERT")

    # Deselect all the vertices
    bpy.ops.mesh.select_all(action='DESELECT')

    # Switch back to the object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Select the vertex
    obj.data.vertices[vertex_idx].select = True

    # Switch to the edit mode
    bpy.ops.object.mode_set(mode='EDIT')
