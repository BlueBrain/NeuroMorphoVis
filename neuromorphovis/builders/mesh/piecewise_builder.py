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
import random, copy

# Blender imports
import bpy

# Internal modules
import neuromorphovis as nmv
import neuromorphovis.bbox
import neuromorphovis.builders
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.geometry
import neuromorphovis.mesh
import neuromorphovis.shading
import neuromorphovis.skeleton
import neuromorphovis.scene
import neuromorphovis.utilities
import neuromorphovis.rendering


####################################################################################################
# @PiecewiseBuilder
####################################################################################################
class PiecewiseBuilder:
    """Mesh builder that creates piecewise watertight meshes"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology skeleton to create the mesh for.
        :param options:
            Loaded options from NeuroMorphoVis.
        """

        # Morphology
        self.morphology = morphology

        # Loaded options from NeuroMorphoVis
        self.options = options

        # A list of the colors/materials of the soma
        self.soma_materials = None

        # A list of the colors/materials of the axon
        self.axon_materials = None

        # A list of the colors/materials of the basal dendrites
        self.basal_dendrites_materials = None

        # A list of the colors/materials of the apical dendrites
        self.apical_dendrites_materials = None

        # A list of the colors/materials of the spines
        self.spines_materials = None

        # A reference to the reconstructed soma mesh
        self.soma_mesh = None

        # A list of the reconstructed meshes of the arbors
        self.arbors_meshes = list()

        # A reference to the reconstructed spines mesh (spines are grouped in a single mesh)
        self.spines_mesh = None

        self.spines_list = None

        # A mesh of the reconstructed nucleus
        self.nucleus_mesh = None

        # A reference to the reconstructed neuron mesh
        # NOTE: After the generation of the individual meshes of each component of the neuron,
        # these components are joint together into a single mesh and assigned to this variable
        self.neuron_mesh = None

    ################################################################################################
    # @create_materials
    ################################################################################################
    def create_homogeneous_materials(self,
                                     name,
                                     color):
        """Creates a material that will be applied on the surface of the mesh.

        :param name:
            The name of the material.
        :param color:
            The color of the material.
        :return:
            A reference to the created material.
        """

        # A list of materials
        materials = list()

        # Create the materials
        for i in range(2):
            material = nmv.shading.create_material(
                name='%s_%d' % (name, i), color=color, material_type=self.options.mesh.material)

            # Append the material to the list
            materials.append(material)

        # Return a reference to the created material
        return materials

    ################################################################################################
    # @create_skeleton_materials
    ################################################################################################
    def create_skeleton_materials(self):
        """Create the materials of the skeleton.
        """

        # Clear all the existing materials before to make the scene clean
        for material in bpy.data.materials:
            if 'soma_material' in material.name or \
               'axon_material' in material.name or \
               'basal_dendrites_material' in material.name or \
               'apical_dendrite_material' in material.name or \
               'spines_material' in material.name:
                material.user_clear()
                bpy.data.materials.remove(material)

        # Soma
        self.soma_materials = self.create_homogeneous_materials(
            name='soma_material', color=self.options.mesh.soma_color)

        # Axon
        self.axon_materials = self.create_homogeneous_materials(
            name='axon_material', color=self.options.mesh.axon_color)

        # Basal dendrites
        self.basal_dendrites_materials = self.create_homogeneous_materials(
            name='basal_dendrites_material', color=self.options.mesh.basal_dendrites_color)

        # Apical dendrite
        self.apical_dendrites_materials = self.create_homogeneous_materials(
            name='apical_dendrite_material', color=self.options.mesh.apical_dendrites_color)

        # Spines
        self.spines_materials = self.create_homogeneous_materials(
            name='spines_material', color=self.options.mesh.spines_color)

    ################################################################################################
    # @verify_and_repair_morphology
    ################################################################################################
    def verify_and_repair_morphology(self):
        """Verifies and repairs the morphology if the contain any artifacts that would potentially
        affect the reconstruction quality of the mesh.

        NOTE: The filters or operations performed in this builder are only specific to it. Other
        builders might apply a different set of filters.
        """

        # Remove the internal samples, or the samples that intersect the soma at the first
        # section and each arbor
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.ops.remove_samples_inside_soma])

        # The arbors can be selected to be reconstructed with sharp edges or smooth ones. For the
        # sharp edges, we do NOT need to re-sample the morphology skeleton. However, if the smooth
        # edges option is selected, the arbors must be re-sampled to avoid any meshing artifacts
        # after applying the vertex smoothing filter. The re-sampling filter for the moment
        # re-samples the morphology sections at 2.5 microns, however this can be improved later
        # by adding an algorithm that re-samples the section based on its radii.
        if self.options.mesh.edges == nmv.enums.Meshing.Edges.SMOOTH:

            # Apply the resampling filter on the whole morphology skeleton
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.resample_sections])

        # Verify the connectivity of the arbors to the soma to filter the disconnected arbors,
        # for example, an axon that is emanating from a dendrite or two intersecting dendrites
        nmv.skeleton.ops.update_arbors_connection_to_soma(self.morphology)

        # Primary and secondary branching
        if self.options.mesh.branching == nmv.enums.Meshing.Branching.ANGLES:

            # Label the primary and secondary sections based on angles
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_angles])

        else:

            # Label the primary and secondary sections based on radii
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_radii])

    ################################################################################################
    # @build_arbors
    ################################################################################################
    def build_arbors(self,
                     bevel_object,
                     caps,
                     roots_connection):
        """Builds the arbors of the neuron as tubes and AT THE END converts them into meshes.
        If you convert them during the building, the scene is getting crowded and the process is
        getting exponentially slower.

        :param bevel_object:
            A given bevel object to scale the section at the different samples.
        :param caps:
            A flag to indicate whether the drawn sections are closed or not.
        :param roots_connection:
            A flag to connect (for soma disconnected more) or disconnect (for soma bridging mode)
            the arbor to the soma origin.
            If this flag is set to True, this means that the arbor will be extended to the soma
            origin and the branch will not be physically connected to the soma as a single mesh.
            If the flag is set to False, the arbor will only have a bridging connection that
            would allow us later to connect it to the nearest face on the soma create a
            watertight mesh.
        :return:
            A list of all the individual meshes of the arbors.
        """

        # Taper the sections if requested
        if self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED or \
           self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED_ZIGZAG:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.taper_section])

        # Zigzag the sections if required
        if self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.ZIGZAG or \
           self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED_ZIGZAG:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.zigzag_section])

        # Create a list that keeps references to the meshes of all the connected pieces of the
        # arbors of the mesh.
        arbors_objects = []

        # Draw the apical dendrite, if exists
        if not self.options.morphology.ignore_apical_dendrite:
            nmv.logger.info('Apical dendrite')

            # Individual sections (tubes) of the apical dendrite
            apical_dendrite_objects = []

            if self.morphology.apical_dendrite is not None:

                # Draw the apical dendrite as a set connected sections
                nmv.skeleton.ops.draw_connected_sections(
                    section=copy.deepcopy(self.morphology.apical_dendrite),
                    max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                    name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                    material_list=self.apical_dendrites_materials,
                    bevel_object=bevel_object,
                    repair_morphology=True,
                    caps=caps,
                    sections_objects=apical_dendrite_objects,
                    roots_connection=roots_connection)

                # Ensure that apical dendrite objects were reconstructed
                if len(apical_dendrite_objects) > 0:

                    # Add a reference to the mesh object
                    self.morphology.apical_dendrite.mesh = apical_dendrite_objects[0]

                    # Add the sections (tubes) of the basal dendrites to the list
                    arbors_objects.extend(apical_dendrite_objects)

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Ensure tha existence of basal dendrites
            if self.morphology.dendrites is not None:

                # Do it dendrite by dendrite
                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.info('Dendrite [%d]' % i)

                    basal_dendrite_objects = []

                    # Draw the basal dendrites as a set connected sections
                    basal_dendrite_prefix = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)
                    nmv.skeleton.ops.draw_connected_sections(
                        section=copy.deepcopy(basal_dendrite),
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                        name=basal_dendrite_prefix,
                        material_list=self.basal_dendrites_materials,
                        bevel_object=bevel_object,
                        repair_morphology=True,
                        caps=caps,
                        sections_objects=basal_dendrite_objects,
                        roots_connection=roots_connection)

                    # Ensure that basal dendrite objects were reconstructed
                    if len(basal_dendrite_objects) > 0:

                        # Add a reference to the mesh object
                        self.morphology.dendrites[i].mesh = basal_dendrite_objects[0]

                        # Add the sections (tubes) of the basal dendrite to the list
                        arbors_objects.extend(basal_dendrite_objects)

        # Draw the axon as a set connected sections
        if not self.options.morphology.ignore_axon:

            # Ensure tha existence of basal dendrites
            if self.morphology.axon is not None:

                nmv.logger.info('Axon')

                # Individual sections (tubes) of the axon
                axon_objects = []

                # Draw the axon as a set connected sections
                nmv.skeleton.ops.draw_connected_sections(
                    section=copy.deepcopy(self.morphology.axon),
                    max_branching_level=self.options.morphology.axon_branch_order,
                    name=nmv.consts.Arbors.AXON_PREFIX,
                    material_list=self.axon_materials,
                    bevel_object=bevel_object,
                    repair_morphology=True,
                    caps=caps,
                    sections_objects=axon_objects,
                    roots_connection=roots_connection)

                # Ensure that axon objects were reconstructed
                if len(axon_objects) > 0:

                    # Add a reference to the mesh object
                    self.morphology.axon.mesh = axon_objects[0]

                    # Add the sections (tubes) of the axons to the list
                    arbors_objects.extend(axon_objects)

        # Convert the section object (tubes) into meshes
        for arbor_object in arbors_objects:
            nmv.scene.ops.convert_object_to_mesh(arbor_object)

        # Return the list of meshes
        return arbors_objects

    ################################################################################################
    # @connect_arbors_to_soma
    ################################################################################################
    def connect_arbors_to_soma(self):
        """Connects the root section of a given arbor to the soma at its initial segment.

        This function checks if the arbor mesh is 'logically' connected to the soma or not,
        following to the initial validation steps that determines if the arbor has a valid
        connection point to the soma or not.
        If the arbor is 'logically' connected to the soma, this function returns immediately.
        The arbor is a Section object, see Section() @ section.py.
        """

        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            nmv.logger.header('Connecting arbors to soma')

            # Connecting apical dendrite
            if not self.options.morphology.ignore_apical_dendrite:

                # There is an apical dendrite
                if self.morphology.apical_dendrite is not None:
                    nmv.logger.detail('Apical dendrite')
                    nmv.skeleton.ops.connect_arbor_to_soma(self.soma_mesh,
                                                           self.morphology.apical_dendrite)

            # Connecting basal dendrites
            if not self.options.morphology.ignore_basal_dendrites:

                # Ensure tha existence of basal dendrites
                if self.morphology.dendrites is not None:

                    # Do it dendrite by dendrite
                    for i, basal_dendrite in enumerate(self.morphology.dendrites):
                        nmv.logger.detail('Dendrite [%d]' % i)
                        nmv.skeleton.ops.connect_arbor_to_soma(self.soma_mesh, basal_dendrite)

            # Connecting axon
            if not self.options.morphology.ignore_axon:

                # Ensure tha existence of the axon
                if self.morphology.axon is not None:

                    nmv.logger.detail('Axon')
                    nmv.skeleton.ops.connect_arbor_to_soma(self.soma_mesh, self.morphology.axon)

    ################################################################################################
    # @adjust_texture_mapping
    ################################################################################################
    @staticmethod
    def adjust_texture_mapping(list_meshes,
                               texspace_size):
        """

        :param list_meshes:
        :param texspace_size:
        :return:
        """

        # Do it mesh by mesh
        for i, mesh_object in enumerate(list_meshes):

            # Update the texture space of the created meshes
            mesh_object.select = True
            bpy.context.object.data.use_auto_texspace = False
            bpy.context.object.data.texspace_size[0] = texspace_size
            bpy.context.object.data.texspace_size[1] = texspace_size
            bpy.context.object.data.texspace_size[2] = texspace_size

            # Show the progress
            nmv.utilities.show_progress(
                '\t * Decimating the mesh', float(i), float(len(list_meshes)))

    ################################################################################################
    # @decimate_neuron_mesh
    ################################################################################################
    def decimate_neuron_mesh(self):
        """Decimate the reconstructed neuron mesh.
        """

        nmv.logger.header('Decimating the mesh')

        if 0.05 < self.options.mesh.tessellation_level < 1.0:
            nmv.logger.info('Decimating the neuron')

            # Get a list of all the mesh objects (except the spines) of the neuron
            neuron_meshes = list()
            for scene_object in bpy.context.scene.objects:

                # Only for meshes
                if scene_object.type == 'MESH':

                    # Exclude the spines
                    if 'spine' in scene_object.name:
                        continue

                    # Otherwise, add the object to the list
                    else:
                        neuron_meshes.append(scene_object)

            # Do it mesh by mesh
            for i, object_mesh in enumerate(neuron_meshes):

                # Update the texture space of the created meshes
                object_mesh.select = True
                bpy.context.object.data.use_auto_texspace = False
                bpy.context.object.data.texspace_size[0] = 5
                bpy.context.object.data.texspace_size[1] = 5
                bpy.context.object.data.texspace_size[2] = 5

                # Skip the soma, if the soma is disconnected
                if 'soma' in object_mesh.name:
                    continue

                # Show the progress
                nmv.utilities.show_progress(
                    '\t * Decimating the mesh', float(i),float(len(neuron_meshes)))

                # Decimate each mesh object
                nmv.mesh.ops.decimate_mesh_object(
                    mesh_object=object_mesh, decimation_ratio=self.options.mesh.tessellation_level)

    ################################################################################################
    # @build_hard_edges_arbors
    ################################################################################################
    def build_hard_edges_arbors(self):
        """Reconstruct the meshes of the arbors of the neuron with HARD edges.
        """

        # Create a bevel object that will be used to create the mesh
        bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=16, name='arbors_bevel')

        # If the meshes of the arbors are 'welded' into the soma, then do NOT connect them to the
        #  soma origin, otherwise extend the arbors to the origin
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_SOMA
        else:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN

        # Create the arbors using this 16-side bevel object and CLOSED caps (no smoothing required)
        arbors_meshes = self.build_arbors(
            bevel_object=bevel_object, caps=True, roots_connection=roots_connection)

        # Close the caps
        for arbor_object in arbors_meshes:
            nmv.mesh.close_open_faces(arbor_object)

        # Delete the bevel object
        nmv.scene.ops.delete_object_in_scene(bevel_object)

    ################################################################################################
    # @build_soft_edges_arbors
    ################################################################################################
    def build_soft_edges_arbors(self):
        """Reconstruct the meshes of the arbors of the neuron with SOFT edges.
        """
        # Create a bevel object that will be used to create the mesh with 4 sides only
        bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=4, name='bevel')

        # If the meshes of the arbors are 'welded' into the soma, then do NOT connect them to the
        #  soma origin, otherwise extend the arbors to the origin
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_SOMA
        else:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN

        # Create the arbors using this 4-side bevel object and OPEN caps (for smoothing)
        arbors_meshes = self.build_arbors(
            bevel_object=bevel_object, caps=False, roots_connection=roots_connection)

        # Smooth and close the faces in one step
        for mesh in arbors_meshes:
            nmv.mesh.ops.smooth_object_vertices(mesh_object=mesh, level=2)

        # Delete the bevel object
        nmv.scene.ops.delete_object_in_scene(bevel_object)

    ################################################################################################
    # @add_surface_noise
    ################################################################################################
    def add_surface_noise(self):
        """Adds noise to the surface of the reconstructed mesh(es).

        NOTE: The surface mesh of the neuron is reconstructed as a set (or list) of meshes
        representing the soma, different arbors and spines. This operation will JOIN all the
        objects (except the spines) into a single object only to be able to apply it correctly.
        """

        if self.options.mesh.surface == nmv.enums.Meshing.Surface.ROUGH:
            nmv.logger.header('Adding surface roughness')

            # The soma is already reconstructed with high number of subdivisions for accuracy,
            # and the arbors are reconstructed with minimal number of samples that is sufficient to
            # make them smooth. Therefore, we must add the noise around the soma and its connections
            # to the arbors (the stable extent) with a different amplitude.
            stable_extent_center, stable_extent_radius = nmv.skeleton.ops.get_stable_soma_extent(
                self.morphology)

            # Apply the noise addition filter
            nmv.logger.info('Adding noise')
            for i in range(len(self.neuron_mesh.data.vertices)):
                vertex = self.neuron_mesh.data.vertices[i]
                if nmv.geometry.ops.is_point_inside_sphere(
                        stable_extent_center, stable_extent_radius, vertex.co):
                    if nmv.geometry.ops.is_point_inside_sphere(
                            stable_extent_center, self.morphology.soma.smallest_radius,
                            vertex.co):
                        vertex.select = True
                        vertex.co = vertex.co + (vertex.normal * random.uniform(0, 0.01))
                        vertex.select = False
                    else:
                        if 0.0 < random.uniform(0, 1.0) < 0.1:
                            vertex.select = True
                            vertex.co = vertex.co + (vertex.normal * random.uniform(-0.1, 0.2))
                            vertex.select = False
                else:

                    value = random.uniform(-0.25, 0.1)
                    if 0.0 < random.uniform(0, 1.0) < 0.045:
                        value += random.uniform(0.05, 0.1)
                    elif 0.045 < random.uniform(0, 1.0) < 0.06:
                        value += random.uniform(0.2, 0.5)
                    vertex.select = True
                    vertex.co = vertex.co + (vertex.normal * value)
                    vertex.select = False

            # Decimate and smooth for getting the bumps
            nmv.logger.info('Smoothing')

            # Deselect all the vertices
            nmv.mesh.ops.deselect_all_vertices(mesh_object=self.neuron_mesh)

            # Decimate each mesh object
            nmv.mesh.ops.decimate_mesh_object(mesh_object=self.neuron_mesh, decimation_ratio=0.25)

            # Smooth each mesh object
            nmv.mesh.ops.smooth_object(mesh_object=self.neuron_mesh, level=1)

    ################################################################################################
    # @reconstruct_soma_mesh
    ################################################################################################
    def reconstruct_soma_mesh(self):
        """Reconstruct the mesh of the soma.

        NOTE: To improve the performance of the soft body physics simulation, reconstruct the
        soma profile before the arbors, such that the scene is almost empty.

        NOTE: If the soma is requested to be connected to the initial segments of the arbors,
        we must use a high number of subdivisions to make smooth connections that look nice,
        but if the arbors are connected to the soma origin, then we can use less subdivisions
        since the soma will not be connected to the arbor at all.
        """

        # If the soma is connected to the root arbors
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            soma_builder_object = nmv.builders.SomaBuilder(
                morphology=self.morphology, options=self.options)

        # Otherwise, ignore
        else:
            soma_builder_object = nmv.builders.SomaBuilder(
                morphology=self.morphology,
                options=self.options)

        # Reconstruct the soma mesh
        self.soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

        # Apply the shader to the reconstructed soma mesh
        nmv.shading.set_material_to_object(self.soma_mesh, self.soma_materials[0])

    ################################################################################################
    # @reconstruct_arbors_meshes
    ################################################################################################
    def reconstruct_arbors_meshes(self):
        """Reconstruct the arbors.

        # There are two techniques for reconstructing the mesh. The first uses sharp edges without
        # any smoothing, and in this case, we will use a bevel object having 16 or 32 vertices.
        # The other method creates a smoothed mesh with soft edges. In this method, we will use a
        # simplified bevel object with only 'four' vertices and smooth it later using vertices
        # smoothing to make 'sexy curves' for the mesh that reflect realistic arbors.
        """

        nmv.logger.header('Building arbors')

        # Hard edges (less samples per branch)
        if self.options.mesh.edges == nmv.enums.Meshing.Edges.HARD:
            self.build_hard_edges_arbors()

        # Smooth edges (more samples per branch)
        elif self.options.mesh.edges == nmv.enums.Meshing.Edges.SMOOTH:
            self.build_soft_edges_arbors()

        else:
            nmv.logger.log('ERROR')

    ################################################################################################
    # @add_spines
    ################################################################################################
    def add_spines(self):
        """Add the spines to the neuron.
        """

        if self.options.mesh.spines == nmv.enums.Meshing.Spines.Source.CIRCUIT:
            spines_builder = nmv.builders.CircuitSpineBuilder(
                morphology=self.morphology, options=self.options)
            self.spines_mesh, self.spines_list = spines_builder.add_spines_to_morphology()

        # Random spines
        elif self.options.mesh.spines == nmv.enums.Meshing.Spines.Source.RANDOM:
            nmv.logger.header('Adding random spines')
            spines_builder = nmv.builders.RandomSpineBuilder(
                morphology=self.morphology, options=self.options)
            spines_objects = spines_builder.add_spines_to_morphology()

        # Otherwise ignore spines
        else:
            nmv.logger.log('Ignoring spines')

    ################################################################################################
    # @add_nucleus
    ################################################################################################
    def add_nucleus(self):
        """Add nucleus to the neuron.
        """

        # Adding nucleus
        if self.options.mesh.nucleus == nmv.enums.Meshing.Nucleus.INTEGRATED:
            nmv.logger.header('Adding nucleus')
            nucleus_builder = nmv.builders.NucleusBuilder(
                morphology=self.morphology, options=self.options)
            self.nucleus_mesh = nucleus_builder.add_nucleus_inside_soma()

    ################################################################################################
    # @transform_to_global_coordinates
    ################################################################################################
    def transform_to_global_coordinates(self):
        """Transform the neuron membrane to the global coordinates.

        NOTE: Spine transformation is already implemented by the spine builder, and therefore
        this function applies only to the arbors and the soma.
        """

        # Transform the neuron object to the global coordinates
        if self.options.mesh.global_coordinates:
            nmv.logger.header('Transforming to global coordinates')
            nmv.skeleton.ops.transform_to_global_coordinates(
                mesh_object=self.neuron_mesh, blue_config=self.options.morphology.blue_config,
                gid=self.options.morphology.gid)

    ################################################################################################
    # @joint_neuron_meshes_into_single_mesh
    ################################################################################################
    def join_neuron_meshes_into_single_mesh(self):
        """Join the individual mesh objects of the neuron into a single mesh object.
        """

        # A list of the individual mesh objects
        individual_mesh_objects = list()

        # Connecting all the objects together into a single object
        for scene_object in bpy.context.scene.objects:
            if scene_object.type == 'MESH':
                individual_mesh_objects.append(scene_object)

        # Joint all the objects
        self.neuron_mesh = nmv.mesh.ops.join_mesh_objects(
            mesh_list=individual_mesh_objects, name=self.options.morphology.label)

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):
        """Reconstructs the neuronal mesh as a set of piecewise-watertight meshes.

        The meshes are logically connected, but the different branches are intersecting,
        so they can be used perfectly for voxelization purposes, but they cannot be used for
        surface rendering with 'transparency'.
        """

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        self.create_skeleton_materials()

        # Verify and repair the morphology
        self.verify_and_repair_morphology()

        # Build the soma
        self.reconstruct_soma_mesh()

        # Build the arbors
        self.reconstruct_arbors_meshes()

        # Connect the arbors to the soma
        self.connect_arbors_to_soma()

        # Adding surface roughness
        # self.add_surface_noise()

        # Add nucleus
        # self.add_nucleus()

        # Decimation
        # self.decimate_neuron_mesh()



        # Group the objects of the neuron together
        self.join_neuron_meshes_into_single_mesh()

        # Adding spines
        self.add_spines()

        self.add_surface_noise()

        """
        # Adding noise finally based on the spines
        for i, spine in enumerate(self.spines_list):
            print(i)

            spine_post_position = spine.post_synaptic_position
            spine_pre_position = spine.pre_synaptic_position

            # get the nearest vertex to the spine
            vertex_index = nmv.mesh.ops.get_index_of_nearest_vertex_to_point(self.neuron_mesh,
                                                                             spine_post_position)

            vertex = self.neuron_mesh.data.vertices[vertex_index]
            vertex.co = vertex.co + vertex.normal * 4.0
            # pull the nearest vertex to the spine towards the pre-synaptic neuron
        """




        # Group the objects of the neuron together
        # self.join_neuron_meshes_into_single_mesh()





        # Transform to the global coordinates
        # self.transform_to_global_coordinates()

        # Adjust the texture coordinates of the mesh

        # Report
        nmv.logger.header('Mesh Reconstruction Done!')

        # Return a reference to the neuron mesh
        return self.neuron_mesh






        """
        # Compile a list of all the meshes in the scene, they account for the different mesh
        # objects of the neuron
        for scene_object in bpy.context.scene.objects:
            if scene_object.type == 'MESH':

                # Add the object to the list
                self.arbors_meshes.append(scene_object)

                # If the meshes are merged into a single object, we must override the texture values
                # Update the texture space of the created mesh
                scene_object.select = True
                bpy.context.scene.objects.active = scene_object
                bpy.context.object.data.use_auto_texspace = False
                bpy.context.object.data.texspace_size[0] = 1
                bpy.context.object.data.texspace_size[1] = 1
                bpy.context.object.data.texspace_size[2] = 1
                scene_object.select = False
        
        # Connecting all the mesh objects together in a single object
        if self.options.mesh.neuron_objects_connection == \
                nmv.enums.Meshing.ObjectsConnection.CONNECTED:

                nmv.logger.header('Connecting neurons objects')
                nmv.logger.info('Connecting neuron: [%s_mesh]' % self.options.morphology.label)

                # Group all the objects into a single mesh object after the decimation
                neuron_mesh = nmv.mesh.ops.join_mesh_objects(
                    mesh_list=self.arbors_meshes,
                    name='%s_mesh' % self.options.morphology.label)

                # Update the arbors_meshes list to a single object
                self.arbors_meshes = [neuron_mesh]
        """





