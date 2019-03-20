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


################################################################################################
# @create_materials
################################################################################################
def create_materials(builder,
                     name,
                     color):
    """Creates just two materials of the mesh on the input parameters of the user.

    :param builder:
        The builder object.
    :param name:
        The name of the material/color.
    :param color:
        The code of the given colors.
    :return:
        A list of two elements (different or same colors) where we can apply later to the drawn
        sections or segments.
    """

    # A list of the created materials
    materials_list = []

    for i in range(2):

        # Create the material
        material = nmv.shading.create_material(name='%s_color_%d' % (name, i), color=color,
                                               material_type=builder.options.mesh.material)

        # Append the material to the materials list
        materials_list.append(material)

    # Return the list
    return materials_list


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
    builder.soma_materials = create_materials(
        builder=builder, name='soma_skeleton', color=builder.options.mesh.soma_color)

    # Axon
    builder.axon_materials = create_materials(
        builder=builder, name='axon_skeleton', color=builder.options.mesh.axon_color)

    # Basal dendrites
    builder.basal_dendrites_materials = create_materials(
        builder=builder, name='basal_dendrites_skeleton',
        color=builder.options.mesh.basal_dendrites_color)

    # Apical dendrite
    builder.apical_dendrites_materials = create_materials(
        builder=builder, name='apical_dendrite_skeleton',
        color=builder.options.mesh.apical_dendrites_color)

    # Spines
    builder.spines_materials = create_materials(
        builder=builder, name='spines', color=builder.options.mesh.spines_color)

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

            # Otherwise, add the object to the list
            else:

                if 'Apical' in scene_object.name or \
                   'Basal' in scene_object.name or \
                   'Axon' in scene_object.name or \
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

    nmv.logger.header('UV mapping')

    # Do it mesh by mesh
    for i, mesh_object in enumerate(mesh_objects):

        # Adjust the size
        nmv.shading.adjust_material_uv(mesh_object, size=texspace_size)

        # Show the progress
        nmv.utilities.show_progress(
            '* Adjusting the UV mapping', float(i), float(len(mesh_objects)))

    # Show the progress
    nmv.utilities.show_progress('* Adjusting the UV mapping', 0, 0, done=True)


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
        nmv.logger.header('Decimating the neuron')

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
    """

    if builder.options.mesh.surface == nmv.enums.Meshing.Surface.ROUGH:
        nmv.logger.header('Adding surface roughness to arbors')

        # Get a list of all the meshes of the reconstructed arbors



        # Join all the mesh objects (except the spines) of the neuron into a single mesh object
        nmv.logger.info('Joining meshes')
        neuron_meshes = list()
        for scene_object in bpy.context.scene.objects:

            # Only for meshes
            if scene_object.type == 'MESH':

                # Exclude the spines
                if 'spin' in scene_object.name:
                    continue

                # Otherwise, add the object to the list
                else:
                    neuron_meshes.append(scene_object)

        # Join all the objects into a single neuron mesh
        neuron_mesh = nmv.mesh.ops.join_mesh_objects(
            mesh_list=neuron_meshes,
            name='%s_mesh_proxy' % builder.options.morphology.label)

        # The soma is already reconstructed with high number of subdivisions for accuracy,
        # and the arbors are reconstructed with minimal number of samples that is sufficient to
        # make them smooth. Therefore, we must add the noise around the soma and its connections
        # to the arbors (the stable extent) with a different amplitude.
        stable_extent_center, stable_extent_radius = nmv.skeleton.ops.get_stable_soma_extent(
            builder.morphology)

        # Apply the noise addition filter
        nmv.logger.info('Adding noise')
        for i in range(len(neuron_mesh.data.vertices)):
            vertex = neuron_mesh.data.vertices[i]
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

        # Decimate and smooth for getting the bumps
        nmv.logger.info('Smoothing')

        # Deselect all the vertices
        nmv.mesh.ops.deselect_all_vertices(mesh_object=neuron_mesh)

        # Decimate each mesh object
        nmv.mesh.ops.decimate_mesh_object(mesh_object=neuron_mesh, decimation_ratio=0.5)

        # Smooth each mesh object
        nmv.mesh.ops.smooth_object(mesh_object=neuron_mesh, level=1)

def add_spines(self):
    # Add spines
    spines_objects = None
    if self.options.mesh.spines == nmv.enums.Meshing.Spines.Source.CIRCUIT:
        nmv.logger.header('Adding circuit spines')
        spines_objects = nmv.builders.build_circuit_spines(
            morphology=self.morphology, blue_config=self.options.morphology.blue_config,
            gid=self.options.morphology.gid, material=self.spines_materials[0])

    # Random spines
    elif self.options.mesh.spines == nmv.enums.Meshing.Spines.Source.RANDOM:
        nmv.logger.header('Adding random spines')
        spines_builder = nmv.builders.RandomSpineBuilder(
            morphology=self.morphology, options=self.options)
        spines_objects = spines_builder.add_spines_to_morphology()

    # Otherwise ignore spines
    else:
        return

    # Join the spine objects into a single mesh
    spine_mesh_name = '%s_spines' % self.options.morphology.label
    self.spines_mesh = nmv.mesh.join_mesh_objects(spines_objects, spine_mesh_name)






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





################################################################################################
# @joint_neuron_meshes_into_single_mesh
################################################################################################
def join_neuron_meshes_into_single_mesh(soma_meshes_list=None,
                                        apical_dendrite_meshes_list=None,
                                        basal_dendrites_meshes_list=None,
                                        axon_meshes_list=None,
                                        spines_meshes_list=None,
                                        label='MESH'):
    """Join all the given meshes into a single mesh.

    NOTE: The best approach to perform this operation is to compile a list with the contents of
    all the other lists and then merge this list.

    :param soma_meshes_list:
        A list of all the meshes created for the soma.
    :param apical_dendrite_meshes_list:
        A list of all the meshes created for the apical dendrites.
    :param basal_dendrites_meshes_list:
        A list of all the meshes created for the basal dendrites .
    :param axon_meshes_list:
        A list of all the meshes created for the axon.
    :param spines_meshes_list:
        A list of all the meshes created for the spines.
    :param label:
        The label of the joint mesh object.
    :return:
        A reference to the joint mesh object.
    """

    # A list of the individual mesh objects
    individual_mesh_objects = list()

    # Append the soma meshes
    if soma_meshes_list is not None:
        for mesh in soma_meshes_list:
            individual_mesh_objects.append(mesh)

    # Append the apical dendrites meshes
    if soma_meshes_list is not None:
        for mesh in apical_dendrite_meshes_list:
            individual_mesh_objects.extend(mesh)

    # Append the basal dendrites meshes
    if soma_meshes_list is not None:
        for mesh in basal_dendrites_meshes_list:
            individual_mesh_objects.extend(mesh)

    # Append the axon meshes
    if soma_meshes_list is not None:
        for mesh in axon_meshes_list:
            individual_mesh_objects.extend(mesh)

    # Append the spines meshes
    if soma_meshes_list is not None:
        for mesh in spines_meshes_list:
            individual_mesh_objects.extend(mesh)

    # Joint all the objects
    joint_mesh_object = nmv.mesh.ops.join_mesh_objects(
        mesh_list=individual_mesh_objects, name=label)

    # Return a reference go the joint mesh object
    return joint_mesh_object
