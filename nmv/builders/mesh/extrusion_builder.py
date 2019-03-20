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
import nmv
import nmv.builders
import nmv.bmeshi
import nmv.consts
import nmv.enums
import nmv.geometry
import nmv.mesh
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities


####################################################################################################
# @ExtrusionBuilder
####################################################################################################
class ExtrusionBuilder:
    """Mesh builder that creates watertight meshes using extrusion"""

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

        # A list of the colors/materials of the apical dendrite
        self.apical_dendrite_materials = None

        # A list of the colors/materials of the spines
        self.spines_materials = None

        # A reference to the reconstructed soma mesh
        self.reconstructed_soma_mesh = None

        # A reference to the reconstructed spines mesh
        self.spines_mesh = None

        # A list of all the meshes that are reconstructed on a piecewise basis and correspond to
        # the different components of the neuron including soma, arbors and the spines as well
        self.reconstructed_neuron_meshes= list()

    ################################################################################################
    # @create_materials
    ################################################################################################
    def create_materials(self,
                         name,
                         color):
        """Creates just two materials of the mesh on the input parameters of the user.

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
            material = nmv.shading.create_material(
                name='%s_color_%d' % (name, i), color=color,
                material_type=self.options.mesh.material)

            # Append the material to the materials list
            materials_list.append(material)

        # Return the list
        return materials_list

    ################################################################################################
    # @create_skeleton_materials
    ################################################################################################
    def create_skeleton_materials(self):
        """Create the materials of the skeleton.
        """

        for material in bpy.data.materials:
            if 'soma_skeleton' in material.name or \
               'axon_skeleton' in material.name or \
               'basal_dendrites_skeleton' in material.name or \
               'apical_dendrite_skeleton' in material.name or \
               'spines' in material.name:
                material.user_clear()
                bpy.data.materials.remove(material)

        # Soma
        self.soma_materials = self.create_materials(
            name='soma_skeleton', color=self.options.mesh.soma_color)

        # Axon
        self.axon_materials = self.create_materials(
            name='axon_skeleton', color=self.options.mesh.axon_color)

        # Basal dendrites
        self.basal_dendrites_materials = self.create_materials(
            name='basal_dendrites_skeleton', color=self.options.mesh.basal_dendrites_color)

        # Apical dendrite
        self.apical_dendrite_materials = self.create_materials(
            name='apical_dendrite_skeleton', color=self.options.mesh.apical_dendrites_color)

        # Spines
        self.spines_materials = self.create_materials(
            name='spines', color=self.options.mesh.spines_color)

        # Create an illumination specific for the given material
        nmv.shading.create_material_specific_illumination(self.options.morphology.material)

    ################################################################################################
    # @verify_and_repair_morphology
    ################################################################################################
    def verify_and_repair_morphology(self):
        """Verifies and repairs the morphology if the contain any artifacts that would potentially
        affect the reconstruction quality of the mesh.
        """

        # Remove the internal samples, or the samples that intersect the soma at the first
        # section and each arbor
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.ops.remove_samples_inside_soma])

        # The arbors can be selected to be reconstructed with sharp edges or smooth ones. For the
        # sharp edges, we do NOT need to resample the morphology skeleton. However, if the smooth
        # edges option is selected, the arbors must be re-sampled to avoid any meshing artifacts
        # after applying the vertex smoothing filter. The resampling filter for the moment
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

    def create_extrusion_face(self, branch):

        # Compute the direction from the origin to the branching point
        connection_direction = branch.samples[0].point.normalized()

        # Compute the intersecting point on the soma and the difference between that on the soma
        # and that on the branch starting point
        connection_point_on_soma = connection_direction * 0.5 * self.morphology.soma.mean_radius

        # Compute the extrusion radius that will be applied on the soma_sphere
        scale_factor = 0.5 * self.morphology.soma.mean_radius / branch.samples[0].point.length
        extrusion_radius = branch.samples[0].radius * scale_factor

        # Create a reference circle for reshaping the connection cross section to a clean shape,
        # for instance a circle approximation
        connection_circle = nmv.bmeshi.create_circle(radius=branch.samples[0].radius * 2,
            location=branch.samples[0].point, vertices=4)

        # The connection rotation target is mandatory to point the connection circle to it, then
        # compute it and rotate the face towards it
        connection_rotation_target = connection_point_on_soma + connection_direction * 0.1
        nmv.bmeshi.ops.rotate_face_from_center_to_point(connection_circle, 0,
            connection_rotation_target)

        return connection_circle

    ################################################################################################
    # @build_arbors
    ################################################################################################
    def build_arbors(self,
                     bevel_object,
                     caps,
                     connect_to_soma_origin,
                     bridge_to_soma):
        """Builds the arbors of the neuron as tubes and AT THE END converts them into meshes.
        If you convert them during the building, the scene is getting crowded and the process is
        getting exponentially slower.

        :param bevel_object:
            A given bevel object to scale the section at the different samples.
        :param caps:
            A flag to indicate whether the drawn sections are closed or not.
        :param bridge_to_soma:
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

        # Apply the morphology reformation filters if requested before creating the arbors

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

        # Apply the resampling filter on the whole morphology skeleton
        #nmv.skeleton.ops.apply_operation_to_morphology(
        #    *[self.morphology, nmv.skeleton.ops.resample_sections, 1.0])

        

        # Draw the apical dendrite, if exists
        if not self.options.morphology.ignore_apical_dendrite:
            nmv.logger.info('Apical dendrite')

            if self.morphology.apical_dendrite is not None:

                # Create the extrusion object and move it near the first sample of the branch
                apical_dendrite_bmesh_object = self.create_extrusion_face(self.morphology.apical_dendrite)

                # Draw the apical dendrite as a set connected sections
                nmv.skeleton.ops.extrude_connected_sections(
                    section=copy.deepcopy(self.morphology.apical_dendrite),
                    section_objects=[apical_dendrite_bmesh_object],
                    max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                    name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                    material_list=self.apical_dendrite_materials,
                    bevel_object=bevel_object,
                    repair_morphology=True,
                    caps=caps)

                # Link it to the scene
                apical_dendrite_mesh = bpy.data.meshes.new('apical_dendrite_mesh')
                apical_dendrite_bmesh_object.to_mesh(apical_dendrite_mesh)

                # Create a blender object, link it to the scene
                apical_dendrite_mesh_object = bpy.data.objects.new('apical_dendrite', apical_dendrite_mesh)
                bpy.context.scene.objects.link(apical_dendrite_mesh_object)

                # Add a reference to the mesh object
                self.morphology.apical_dendrite.mesh = apical_dendrite_mesh_object

                # Add the mesh object
                arbors_objects.append(apical_dendrite_mesh_object)

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Do it dendrite by dendrite
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                nmv.logger.info('Dendrite [%d]' % i)

                # Create the extrusion object and move it near the first sample of the branch
                basal_dendrite_bmesh_object = self.create_extrusion_face(basal_dendrite)

                # Draw the apical dendrite as a set connected sections
                nmv.skeleton.ops.extrude_connected_sections(
                    section=copy.deepcopy(basal_dendrite),
                    section_objects=[basal_dendrite_bmesh_object],
                    max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                    name=nmv.consts.Arbors.BASAL_DENDRITES_PREFIX,
                    material_list=self.basal_dendrites_materials,
                    bevel_object=bevel_object,
                    repair_morphology=True,
                    caps=caps)

                # Link it to the scene
                basal_dendrite_mesh = bpy.data.meshes.new('dendrite_%d_mesh' % i)
                basal_dendrite_bmesh_object.to_mesh(basal_dendrite_mesh)

                # Create a blender object, link it to the scene
                basal_dendrite_mesh_object = bpy.data.objects.new('dendrite_%d' % i, basal_dendrite_mesh)
                bpy.context.scene.objects.link(basal_dendrite_mesh_object)

                # Add a reference to the mesh object
                self.morphology.dendrites[i].mesh = basal_dendrite_mesh_object

                # Add the sections (tubes) of the basal dendrite to the list
                arbors_objects.append(basal_dendrite_mesh_object)

        # Return the list of meshes
        return arbors_objects

        # Draw the axon as a set connected sections
        if not self.options.morphology.ignore_axon:
            nmv.logger.info('Axon')

            # Create the extrusion object and move it near the first sample of the branch
            axon_bmesh_object = self.create_extrusion_face(self.morphology.axon)

            # Draw the apical dendrite as a set connected sections
            nmv.skeleton.ops.extrude_connected_sections(
                section=copy.deepcopy(self.morphology.axon),
                section_objects=[axon_bmesh_object],
                max_branching_level=self.options.morphology.axon_branch_order,
                name=nmv.consts.Arbors.AXON_PREFIX,
                material_list=self.axon_materials,
                bevel_object=bevel_object,
                repair_morphology=True,
                caps=caps)

            # Link it to the scene
            axon_mesh = bpy.data.meshes.new('axon_mesh')
            axon_bmesh_object.to_mesh(axon_mesh)

            # Create a blender object, link it to the scene
            axon_mesh_object = bpy.data.objects.new('axon', axon_mesh)
            bpy.context.scene.objects.link(axon_mesh_object)

            # Add a reference to the mesh object
            self.morphology.axon.mesh = axon_mesh_object

            # Add the mesh object
            arbors_objects.append(axon_mesh_object)

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
                    nmv.skeleton.ops.connect_arbor_to_soma(
                        self.reconstructed_soma_mesh, self.morphology.apical_dendrite)

            # Connecting basal dendrites
            if not self.options.morphology.ignore_basal_dendrites:

                # Do it dendrite by dendrite
                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.detail('Dendrite [%d]' % i)
                    nmv.skeleton.ops.connect_arbor_to_soma(
                        self.reconstructed_soma_mesh, basal_dendrite)

            # Connecting axon
            if not self.options.morphology.ignore_axon:
                nmv.logger.detail('Axon')
                nmv.skeleton.ops.connect_arbor_to_soma(
                    self.reconstructed_soma_mesh, self.morphology.axon)

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
            bridge_to_soma = True
            connect_to_soma_origin = False
        else:
            bridge_to_soma = False
            connect_to_soma_origin = True

        # Create the arbors using this 16-side bevel object and CLOSED caps (no smoothing required)
        arbors_meshes = self.build_arbors(
            bevel_object=bevel_object, caps=True, connect_to_soma_origin=connect_to_soma_origin,
            bridge_to_soma=bridge_to_soma)

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
            bridge_to_soma = True
            connect_to_soma_origin = False
        else:
            bridge_to_soma = False
            connect_to_soma_origin = True

        # Create the arbors using this 4-side bevel object and OPEN caps (for smoothing)
        arbors_meshes = self.build_arbors(
            bevel_object=bevel_object, caps=False, connect_to_soma_origin=connect_to_soma_origin,
            bridge_to_soma=bridge_to_soma)

        # Smooth and close the faces in one step
        for mesh in arbors_meshes:
            nmv.mesh.ops.smooth_object_vertices(mesh_object=mesh, level=2)

            # Delete the bevel object
            nmv.scene.ops.delete_object_in_scene(bevel_object)

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
                name='%s_mesh_proxy' % self.options.morphology.label)

            # The soma is already reconstructed with high number of subdivisions for accuracy,
            # and the arbors are reconstructed with minimal number of samples that is sufficient to
            # make them smooth. Therefore, we must add the noise around the soma and its connections
            # to the arbors (the stable extent) with a different amplitude.
            stable_extent_center, stable_extent_radius = nmv.skeleton.ops.get_stable_soma_extent(
                self.morphology)

            # Apply the noise addition filter
            nmv.logger.info('Adding noise')
            for i in range(len(neuron_mesh.data.vertices)):
                vertex = neuron_mesh.data.vertices[i]
                if nmv.geometry.ops.is_point_inside_sphere(
                        stable_extent_center, stable_extent_radius, vertex.co):
                    if nmv.geometry.ops.is_point_inside_sphere(
                            stable_extent_center, self.morphology.soma.smallest_radius,
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
        self.reconstructed_soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

        # Apply the shader to the reconstructed soma mesh
        nmv.shading.set_material_to_object(self.reconstructed_soma_mesh, self.soma_materials[0])

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
        # self.reconstruct_soma_mesh()

        # Build the arbors
        self.reconstruct_arbors_meshes()

        # Connect the arbors to the soma
        self.connect_arbors_to_soma()

        # Adding surface roughness
        self.add_surface_noise()

        # Decimation
        self.decimate_neuron_mesh()

        # Adding spines
        self.add_spines()

        # Adding nucleus
        if self.options.mesh.nucleus == nmv.enums.Meshing.Nucleus.INTEGRATED:
            nmv.logger.header('Adding nucleus')
            nucleus_builder = nmv.builders.NucleusBuilder(
                morphology=self.morphology, options=self.options)
            nucleus_mesh = nucleus_builder.add_nucleus_inside_soma()

        # Compile a list of all the meshes in the scene, they account for the different mesh
        # objects of the neuron
        for scene_object in bpy.context.scene.objects:
            if scene_object.type == 'MESH':

                # Add the object to the list
                self.reconstructed_neuron_meshes.append(scene_object)

                # If the meshes are merged into a single object, we must override the texture values
                # Update the texture space of the created mesh
                scene_object.select = True
                bpy.context.scene.objects.active = scene_object
                bpy.context.object.data.use_auto_texspace = False
                bpy.context.object.data.texspace_size[0] = 5
                bpy.context.object.data.texspace_size[1] = 5
                bpy.context.object.data.texspace_size[2] = 5
                scene_object.select = False

        # Connecting all the mesh objects together in a single object
        if self.options.mesh.neuron_objects_connection == \
                nmv.enums.Meshing.ObjectsConnection.CONNECTED:

                nmv.logger.header('Connecting neurons objects')
                nmv.logger.info('Connecting neuron: [%s_mesh]' % self.options.morphology.label)

                # Group all the objects into a single mesh object after the decimation
                neuron_mesh = nmv.mesh.ops.join_mesh_objects(
                    mesh_list=self.reconstructed_neuron_meshes,
                    name='%s_mesh' % self.options.morphology.label)

                # Update the reconstructed_neuron_meshes list to a single object
                self.reconstructed_neuron_meshes = [neuron_mesh]

        # Transform the neuron object to the global coordinates
        if self.options.mesh.global_coordinates:
            nmv.logger.header('Transforming to global coordinates')

            for mesh_object in self.reconstructed_neuron_meshes:
                nmv.skeleton. ops.transform_to_global(
                    neuron_object=mesh_object,
                    blue_config=self.options.morphology.blue_config,
                    gid=self.options.morphology.gid)

        nmv.logger.header('Done!')

        return self.reconstructed_neuron_meshes
