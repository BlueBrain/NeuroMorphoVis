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
import copy

# Blender imports
import bpy, mathutils

# Internal modules
import nmv
import nmv.builders
import nmv.enums
import nmv.mesh
import nmv.shading
import nmv.skeleton
import nmv.utilities
import nmv.scene


####################################################################################################
# @MetaBuilder
####################################################################################################
class MetaBuilder:
    """Mesh builder that creates high quality meshes with nice bifurcations based on meta objects"""

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

        # A parameter to track the current branching order on each arbor
        # NOTE: This parameter must get reset when you start working on a new arbor
        self.branching_order = 0

        # A list of all the meshes that are reconstructed on a piecewise basis and correspond to
        # the different components of the neuron including soma, arbors and the spines as well
        self.reconstructed_neuron_meshes = list()

        # Meta object skeleton, used to build the skeleton of the morphology
        self.meta_skeleton = None

        # Meta object mesh, used to build the mesh of the morphology
        self.meta_mesh = None

        # A scale factor that was figured out by trial and error to correct the scaling of the radii
        self.magic_scale_factor = 1.575

        # The smallest detected radius while building the model, to be used for meta-ball resolution
        self.smallest_radius = 10.0

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
        # sharp edges, we do NOT need to re-sample the morphology skeleton. However, if the smooth
        # edges option is selected, the arbors must be re-sampled to avoid any meshing artifacts
        # after applying the vertex smoothing filter. The re-sampling filter for the moment
        # re-samples the morphology sections at 2.5 microns, however this can be improved later
        # by adding an algorithm that re-samples the section based on its radii.
        if self.options.mesh.edges == nmv.enums.Meshing.Edges.SMOOTH:

            # Apply the re-sampling filter on the whole morphology skeleton
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
    # @create_meta_segment
    ################################################################################################
    def create_meta_segment(self, p1, p2, r1, r2):
        """Constructs a segment that is composed of two points with a meta object.

        :param p1:
            First point coordinate.
        :param p2:
            Second point coordinate.
        :param r1:
            First point radius.
        :param r2:
            Second point radius.
        """

        # Segment vector
        segment = p2 - p1
        segment_length = segment.length

        # Make sure that the segment length is not zero
        # TODO: Verify this when the radii are greater than the distance
        if segment_length < 0.001:
            return

        # Verify the radii, or fix them
        if r1 < 0.001 * segment_length:
            r1 = 0.001 * segment_length
        if r2 < 0.001 * segment_length:
            r2 = 0.001 * segment_length

        # Compute the deltas between the first and last points along the segments
        dr = r2 - r1
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dz = p2[2] - p1[2]

        # Keep track on the distance traveled along the segment while building, initially 0
        travelled_distance = 0.0

        # Local points, initially at the first point
        r = r1
        x = p1[0]
        y = p1[1]
        z = p1[2]

        # Construct the meta elements along the segment
        while travelled_distance < segment_length:

            # Make a meta ball (or sphere) at this point
            meta_element = self.meta_skeleton.elements.new()

            # Set its radius
            # TODO: Find a solution to compensate the connection points
            meta_element.radius = r

            # Update its coordinates
            meta_element.co = (x, y, z)

            # Proceed to the second point
            travelled_distance += r / 2

            r = r1 + (travelled_distance * dr / segment_length)

            # Get the next point
            x = p1[0] + (travelled_distance * dx / segment_length)
            y = p1[1] + (travelled_distance * dy / segment_length)
            z = p1[2] + (travelled_distance * dz / segment_length)

    ################################################################################################
    # @create_meta_section
    ################################################################################################
    def create_meta_section(self,
                            section):
        """Create a section with meta objects.

        :param section:
            A given section to extrude a mesh around it.
        """

        # Get the list of samples
        samples = section.samples

        # Ensure that the section has at least two samples, otherwise it will give an error
        if len(samples) < 2:
            return

        # Proceed segment by segment
        for i in range(len(samples) - 1):

            if samples[i].radius < self.smallest_radius:
                self.smallest_radius = samples[i].radius

            # Create the meta segment
            self.create_meta_segment(
                p1=samples[i].point,
                p2=samples[i + 1].point,
                r1=samples[i].radius * self.magic_scale_factor,
                r2=samples[i + 1].radius * self.magic_scale_factor)

    ################################################################################################
    # @create_meta_arbor
    ################################################################################################
    def create_meta_arbor(self,
                          root,
                          max_branching_order):
        """Extrude the given arbor section by section recursively using meta objects.

        :param root:
            The root of a given section.
        :param max_branching_order:
            The maximum branching order set by the user to terminate the recursive call.
        """

        # Do not proceed if the branching order limit is hit
        if root.branching_order > max_branching_order:
            return

        # Create the section
        self.create_meta_section(root)

        # Create the children sections recursively
        for child in root.children:
            self.create_meta_arbor(child, max_branching_order)

    ################################################################################################
    # @build_arbors
    ################################################################################################
    def build_arbors(self):
        """Builds the arbors of the neuron as tubes and AT THE END converts them into meshes.
        If you convert them during the building, the scene is getting crowded and the process is
        getting exponentially slower.

        :return:
            A list of all the individual meshes of the arbors.
        """

        # Header
        nmv.logger.header('Building Arbors')

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

        # Draw the apical dendrite, if exists
        if not self.options.morphology.ignore_apical_dendrite:
            nmv.logger.info('Apical dendrite')

            # Create the apical dendrite mesh
            if self.morphology.apical_dendrite is not None:

                self.create_meta_arbor(
                    root=self.morphology.apical_dendrite,
                    max_branching_order=self.options.morphology.apical_dendrite_branch_order)

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Do it dendrite by dendrite
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                # Create the basal dendrite meshes
                nmv.logger.info('Dendrite [%d]' % i)
                self.create_meta_arbor(
                    root=basal_dendrite,
                    max_branching_order=self.options.morphology.basal_dendrites_branch_order)

        # Draw the axon as a set connected sections
        if not self.options.morphology.ignore_axon:
            nmv.logger.info('Axon')

            # Create the apical dendrite mesh
            if self.morphology.axon is not None:

                # Create the axon mesh
                self.create_meta_arbor(
                    root=self.morphology.axon,
                    max_branching_order=self.options.morphology.axon_branch_order)

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
    # @initialize_meta_object
    ################################################################################################
    def initialize_meta_object(self,
                               name):
        """Constructs and initialize a new meta object that will be the basis of the mesh.

        :param name:
            Meta-object name.
        :return:
            A reference to the meta object
        """

        # Create a new meta skeleton that will be used to reconstruct the skeleton frame
        self.meta_skeleton = bpy.data.metaballs.new(name)

        # Create a new meta object that reflects the reconstructed mesh at the end of the operation
        self.meta_mesh = bpy.data.objects.new(name, self.meta_skeleton)

        # Get a reference to the scene
        scene = bpy.context.scene

        # Link the meta object to the scene
        scene.objects.link(self.meta_mesh)

        # Update the resolution of the meta skeleton
        # TODO: Get these parameters from the user interface
        self.meta_skeleton.resolution = 1.0

    ################################################################################################
    # @emanate_soma_towards_arbor
    ################################################################################################
    def emanate_soma_towards_arbor(self,
                                   arbor):
        """Extends the space of the soma towards the given arbor to make a shape that is not sphere.

        :param arbor:
            A given arbor to emanate the soma towards.
        """

        # Assume that from the soma center towards the first point along the arbor is a segment
        self.create_meta_segment(
            p1=self.morphology.soma.centroid,
            p2=arbor.samples[0].point,
            r1=self.morphology.soma.mean_radius,
            r2=arbor.samples[0].radius * self.magic_scale_factor)

    ################################################################################################
    # @build_soma_from_meta_objects
    ################################################################################################
    def build_soma_from_meta_objects(self):

        # Header
        nmv.logger.header('Building Soma from Meta Objects')

        # Emanate towards the apical dendrite, if exists
        if not self.options.morphology.ignore_apical_dendrite:
            nmv.logger.info('Apical dendrite')

            # The apical dendrite must be valid
            if self.morphology.apical_dendrite is not None:
                self.emanate_soma_towards_arbor(arbor=self.morphology.apical_dendrite)

        # Emanate towards basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Do it dendrite by dendrite
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                # Basal dendrites
                nmv.logger.info('Dendrite [%d]' % i)
                self.emanate_soma_towards_arbor(arbor=basal_dendrite)

        # Emanate towards the axon, if exists
        if not self.options.morphology.ignore_apical_dendrite:
            nmv.logger.info('Axon')

            # The axon must be valid
            if self.morphology.axon is not None:
                self.emanate_soma_towards_arbor(arbor=self.morphology.axon)

    ################################################################################################
    # @finalize_meta_object
    ################################################################################################
    def finalize_meta_object(self):
        """Converts the meta object to a mesh and get it ready for export or visualization.

        :return:
        """

        # Header
        nmv.logger.header('Meshing the Meta Object')

        # Deselect all objects
        nmv.scene.ops.deselect_all()

        # Update the resolution
        self.meta_skeleton.resolution = self.smallest_radius

        # Select the mesh
        self.meta_mesh = bpy.context.scene.objects[self.morphology.label]
        self.meta_mesh.select = True

        bpy.context.scene.objects.active = self.meta_mesh

        # Convert it to a mesh from meta-balls
        bpy.ops.object.convert(target='MESH')

        self.meta_mesh = bpy.context.scene.objects[self.morphology.label + '.001']
        self.meta_mesh.name = self.morphology.label

        # Re-select it again to be able to perform post-processing operations in it
        self.meta_mesh.select = True

        bpy.context.scene.objects.active = self.meta_mesh

    ################################################################################################
    # @assign_material_to_mesh
    ################################################################################################
    def assign_material_to_mesh(self):

        # Deselect all objects
        nmv.scene.ops.deselect_all()

        # Activate the mesh object
        bpy.context.scene.objects.active = self.meta_mesh

        # Adjusting the texture space, before assigning the material
        bpy.context.object.data.use_auto_texspace = False
        bpy.context.object.data.texspace_size[0] = 5
        bpy.context.object.data.texspace_size[1] = 5
        bpy.context.object.data.texspace_size[2] = 5

        # Assign the material to the selected mesh
        nmv.shading.set_material_to_object(self.meta_mesh, self.soma_materials[0])

        # Activate the mesh object
        self.meta_mesh.select = True
        bpy.context.scene.objects.active = self.meta_mesh

    ################################################################################################
    # @transform_to_global_coordinates
    ################################################################################################
    def transform_to_global_coordinates(self):
        """Transform the neuron membrane to the global coordinates.

        NOTE: Spine transformation is already implemented by the spine builder, and therefore
        this function applies only to the arbors and the soma.
        """

        # Transform the neuron object to the global coordinates
        nmv.logger.header('Transforming to global coordinates')
        nmv.skeleton.ops.transform_to_global_coordinates(
            mesh_object=self.meta_mesh, blue_config=self.options.morphology.blue_config,
            gid=self.options.morphology.gid)

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):
        """Reconstructs the neuronal mesh using meta objects.
        """

        # Verify and repair the morphology
        # self.verify_and_repair_morphology()

        # Initialize the meta object
        self.initialize_meta_object(name=self.options.morphology.label)

        # Build the soma
        self.build_soma_from_meta_objects()

        # Build the arbors
        self.build_arbors()

        # Finalize the meta object and construct a solid object
        self.finalize_meta_object()

        # We can here create the materials at the end to avoid any issues
        self.create_skeleton_materials()

        # Assign the material to the mesh
        self.assign_material_to_mesh()

        # Transform the mesh to the global coordinates
        if self.options.mesh.global_coordinates:
            self.transform_to_global_coordinates()

        # Mission done
        nmv.logger.header('Done!')

        # Return a reference to the created mesh
        return self.meta_mesh



        # Adding surface roughness
        # self.add_surface_noise()

        # Decimation
        self.decimate_neuron_mesh()


        #
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



        return self.reconstructed_neuron_meshes