####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
from mathutils import Vector, Matrix

# Internal modules
from .base import MeshBuilderBase
import nmv.builders
import nmv.enums
import nmv.mesh
import nmv.shading
import nmv.skeleton
import nmv.utilities
import nmv.scene
import nmv.geometry
import nmv.physics


####################################################################################################
# @MetaBuilder
####################################################################################################
class MetaBuilder(MeshBuilderBase):
    """Mesh builder that creates high quality meshes with nice bifurcations based on meta objects.

    This builder is inspired by the SWC Mesher written by Bob Kuczewski, Oliver Ernst from the
    MCell team. The code is available on Github at [https://github.com/mcellteam/swc_mesher].
    This code is subject to the GPL license based on the original Blender license.
    For further information refer to this page [https://www.blender.org/about/license/].
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options,
                 ignore_watertightness=False):
        """Constructor

        :param morphology:
            A given morphology skeleton to create the mesh for.
        :param options:
            Loaded options from NeuroMorphoVis.
        """

        # Initialize the parent with the common parameters
        MeshBuilderBase.__init__(self, morphology, options)

        # Ignore watertightness
        self.ignore_watertightness = ignore_watertightness

        # Meta object skeleton, used to build the skeleton of the morphology
        self.meta_skeleton = None

        # Meta object mesh, used to build the mesh of the morphology
        self.meta_mesh = None

        # A scale factor that was figured out by trial-and-error to correct the scaling of the radii
        # The results are validated by computing the Hausdorff distance.
        self.magic_scale_factor = 1.575 * 1.025

        # A scale factor that was figured by trial-and-error to correct the scaling of the somata
        # reconstructed from the soft-body meshes
        self.soma_scaling_factor = 1.5

        # The smallest detected radius while building the model, to be used for meta-ball resolution
        self.smallest_radius = 1e5

        # Statistics
        self.profiling_statistics = 'MetaBuilder Profiling Stats.: \n'

        # Stats. about the morphology
        self.morphology_statistics = 'Morphology: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'MetaBuilder Mesh: \n'

        # A list to collect the error in radii
        self.radii_error = list()

        # A temporary label for the mesh
        self.label = 'meta_mesh'

    ################################################################################################
    # @update_morphology_skeleton
    ################################################################################################
    def update_morphology_skeleton(self):
        """Verifies and repairs the morphology if the contain any artifacts that would potentially
        affect the reconstruction quality of the mesh.
        """

        # Remove the internal samples, or the samples that intersect the soma at the first
        # section and each arbor
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.ops.remove_samples_inside_soma])

        # Verify the connectivity of the arbors to the soma to filter the disconnected arbors,
        # for example, an axon that is emanating from a dendrite or two intersecting dendrites
        nmv.skeleton.verify_arbors_connectivity_to_soma(self.morphology)

        # Resample the sections of the morphology skeleton
        self.resample_skeleton_sections()

        # Radii
        nmv.skeleton.update_arbors_radii(
            morphology=self.morphology, morphology_options=self.options.morphology)

        # Update the style of the arbors
        nmv.skeleton.ops.update_arbors_style(
            morphology=self.morphology, arbor_style=self.options.morphology.arbor_style)

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
        i = 0
        while travelled_distance < segment_length:

            # Make a meta ball (or sphere) at this point
            meta_element = self.meta_skeleton.elements.new()

            # Set its radius
            if i == 0:
                meta_element.radius = r * 0.90
            else:
                meta_element.radius = r

            # Update its coordinates
            meta_element.co = (x, y, z)

            # Proceed to the next point
            travelled_distance += 0.5 * r

            r = r1 + (travelled_distance * dr / segment_length)

            # Get the next point
            x = p1[0] + (travelled_distance * dx / segment_length)
            y = p1[1] + (travelled_distance * dy / segment_length)
            z = p1[2] + (travelled_distance * dz / segment_length)

            i += 1

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

            # Get the radii
            radius_0 = samples[i].radius
            radius_1 = samples[i + 1].radius

            # Limit the radii to 100 nano-meters
            if radius_0 < 0.1:
                self.radii_error.append(0.1 - radius_0)
                radius_0 = 0.1
            if radius_1 < 0.1:
                self.radii_error.append(0.1 - radius_1)
                radius_1 = 0.1

            # Adjust the radii
            if radius_0 < self.smallest_radius:
                self.smallest_radius = radius_0
            if radius_1 < self.smallest_radius:
                self.smallest_radius = radius_1

            # Create the meta segment
            self.create_meta_segment(
                p1=samples[i].point,
                p2=samples[i + 1].point,
                r1=radius_0 * self.magic_scale_factor,
                r2=radius_1 * self.magic_scale_factor)

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
        """

        # Header
        nmv.logger.info('Building arbors')

        # Apical Dendrites
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.create_meta_arbor(
                        root=arbor,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.create_meta_arbor(
                        root=arbor,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    self.create_meta_arbor(
                        root=arbor,
                        max_branching_order=self.options.morphology.axon_branch_order)

    ################################################################################################
    # @build_endfeet
    ################################################################################################
    def build_endfeet(self):

        # Construct the meta-object from the endfeet
        for endfoot in self.morphology.endfeet:

            # Create the resampled surface patch
            patch = endfoot.create_resampled_surface_patch()

            # Prepare the vertex list
            vertex_list = list()
            for v in patch.data.vertices:
                vertex_list.append(v.co)

            # NOTE: For the moment, get the average thickness
            thickness = endfoot.compute_average_thickness()

            # Construct the elements
            for v in vertex_list:

                # Add the meta element
                meta_element = self.meta_skeleton.elements.new()

                # Set its radius
                meta_element.radius = thickness

                # Verify the thickness
                if thickness < self.smallest_radius:
                    self.smallest_radius = thickness

                # Update its coordinates
                meta_element.co = v

            # Delete the patch
            nmv.scene.delete_object_in_scene(patch)

    ################################################################################################
    # @initialize_meta_object
    ################################################################################################
    def initialize_meta_object(self,
                               name):
        """Constructs and initialize a new meta object that will be the basis of the mesh.

        :param name:
            Meta-object name.
        """

        # Header
        nmv.logger.header('Creating the Meta Object')

        # Create a new meta skeleton that will be used to reconstruct the skeleton frame
        self.meta_skeleton = bpy.data.metaballs.new(name)

        # Create a new meta-object that reflects the reconstructed mesh at the end of the operation
        self.meta_mesh = bpy.data.objects.new(name, self.meta_skeleton)

        # Link the meta-object to the scene
        nmv.scene.link_object_to_scene(self.meta_mesh)

        # Initial resolution of the meta skeleton, this will get updated later in the finalization
        self.meta_skeleton.resolution = 1.0
        nmv.logger.info('Meta Resolution [%f]' % self.meta_skeleton.resolution)

    ################################################################################################
    # @emanate_soma_towards_arbor
    ################################################################################################
    def emanate_soma_towards_arbor(self,
                                   arbor,
                                   soma_smallest_radius=None):
        """Extends the space of the soma towards the given arbor to make a shape that is not sphere.

        NOTE: The arbor must be connected to the soma to apply this operation, otherwise it
        is ignored.

        :param arbor:
            A given arbor to emanate the soma towards.
        :param soma_smallest_radius:
            The smallest radius to be assigned to the first point at the origin. By default is None.
            This means it is assigned to the auto-value detected by NeuroMorphoVis.
        """

        # The arbor must NOT be far from the soma to emanate towards it
        if not arbor.far_from_soma:

            # Assume that from the soma center towards the first point along the arbor is a segment
            p1 = Vector((self.morphology.soma.centroid[0], 
                         self.morphology.soma.centroid[1], 
                         self.morphology.soma.centroid[2]))
            p2 = arbor.samples[0].point

            # Starting radius
            r1 = self.morphology.soma.smallest_radius
            if soma_smallest_radius is not None:
                r1 = soma_smallest_radius

            # Add the meta segment to the object 
            self.create_meta_segment(
                p1=p1,
                p2=p2,
                r1=r1,
                r2=arbor.samples[0].radius * self.magic_scale_factor)

    ################################################################################################
    # @build_soma_from_meta_objects
    ################################################################################################
    def build_soma_from_meta_objects(self):
        """Builds the soma from meta-objects ONLY.
        """

        # Header
        nmv.logger.info('Building soma from Meta Objects')

        # Verify the proximity of the arbors to the soma
        nmv.skeleton.verify_arbors_connectivity_to_soma(morphology=self.morphology)

        # Get a list of valid arbors where we can pull the sphere towards without being intersecting
        valid_arbors = nmv.skeleton.get_connected_arbors_to_soma_after_verification(
            morphology=self.morphology, soma_center=self.morphology.soma.centroid,
            soma_radius=self.morphology.soma.smallest_radius)

        # Re-classify the arbors to be able to deal with the selectivity
        valid_apical_dendrites = list()
        valid_basal_dendrites = list()
        valid_axons = list()

        for arbor in valid_arbors:
            if arbor.is_axon():
                valid_axons.append(arbor)
            elif arbor.is_apical_dendrite():
                valid_apical_dendrites.append(arbor)
            else:
                valid_basal_dendrites.append(arbor)

        # Emanate towards the apical dendrites, if exist
        if self.morphology.has_apical_dendrites():
            if not self.options.morphology.ignore_apical_dendrites:
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.emanate_soma_towards_arbor(arbor=arbor)

        # Emanate towards basal dendrites, if exist
        if self.morphology.has_basal_dendrites():
            if not self.options.morphology.ignore_basal_dendrites:
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.emanate_soma_towards_arbor(arbor=arbor)

        # Emanate towards axons, if exist
        if self.morphology.has_axons():
            if not self.options.morphology.ignore_axons:
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    self.emanate_soma_towards_arbor(arbor=arbor)

    ################################################################################################
    # @build_soma_from_soft_body
    ################################################################################################
    def build_soma_from_soft_body_mesh(self):
        """Builds the soma profile in the meta skeleton based on a soma that is reconstructed with
        the with soft-body algorithm.
        """

        # Use the SomaSoftBodyBuilder to reconstruct the soma
        soft_body_soma_builder = nmv.builders.SomaSoftBodyBuilder(morphology=self.morphology,
                                                                  options=self.options)

        # Construct the soft-body-based soma and avoid adding noise to the profile
        soft_body_soma = soft_body_soma_builder.reconstruct_soma_mesh(
            apply_shader=False, add_noise_to_surface=False)

        # Run the particle simulation re-mesher
        mesher = nmv.physics.ParticleRemesher()
        stepper = mesher.run(mesh_object=soft_body_soma, context=bpy.context, interactive=True)

        for i in range(1000000):
            finished = next(stepper)
            if finished:
                break

        # Remove the faces that are located around the initial segment
        valid_arbors = soft_body_soma_builder.remove_faces_within_arbor_initial_segment(
            soft_body_soma)

        # For every valid arbor
        for arbor in valid_arbors:

            # Construct a meta-element at the initial sample of each arbor
            meta_element = self.meta_skeleton.elements.new()
            meta_element.radius = arbor.samples[0].radius * self.magic_scale_factor * 1.0
            meta_element.co = arbor.samples[0].point

        # Build the soma profile from the soft-body mesh
        for face in soft_body_soma.data.polygons:

            # Add a new meta element
            meta_element = self.meta_skeleton.elements.new()

            # Compute the largest radius in the triangle, but since we re-mesh the soma, we will
            # get almost equi-sides faces
            radius = nmv.mesh.get_largest_radius_in_face(
                mesh_object=soft_body_soma, face_index=face.index)

            # Compute the radius of the meta-element by trial-and-error
            meta_element.radius = radius * self.magic_scale_factor

            if meta_element.radius < self.smallest_radius:
                self.smallest_radius = meta_element.radius

            # Update its coordinates
            meta_element.co = face.center - (face.normal * radius * self.soma_scaling_factor)

        # Delete the mesh
        nmv.scene.delete_object_in_scene(scene_object=soft_body_soma)

        # Return a reference to the valid arbors that are connected to the soma
        return valid_arbors

    ################################################################################################
    # @build_spines
    ################################################################################################
    def build_random_spines(self):
        """Builds integrated spines into the neuron meta-object that will be meshed and will be
        part of the neuron mesh.
        """

        # Header
        nmv.logger.info('Integrating spines')

        # Create the spine builder
        spines_builder = nmv.builders.RandomSpineBuilderFromMorphology(
            morphology=self.morphology, options=self.options)

        # Basal dendrites
        if self.morphology.has_basal_dendrites():
            if not self.options.morphology.ignore_basal_dendrites:
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)

                    spine_sections = spines_builder.get_spine_morphologies_for_arbor(
                        arbor=arbor,
                        number_spines_per_micron=self.options.mesh.number_spines_per_micron,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order)

                    # Construct the samples from segments
                    for spine_section in spine_sections:
                        self.create_meta_section(spine_section)

        # Apical dendrites
        if self.morphology.has_basal_dendrites():
            if not self.options.morphology.ignore_basal_dendrites:
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)

                    spine_sections = spines_builder.get_spine_morphologies_for_arbor(
                        arbor=arbor, number_spines_per_micron=2,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order)

                    # Construct the samples from segments
                    for spine_section in spine_sections:
                        self.create_meta_section(spine_section)

        # Clean the unwanted data from the spines builder
        spines_builder.clean_unwanted_data()

    def build_circuit_spines(self):
        return

    def build_spines(self):
        if self.options.mesh.spines == nmv.enums.Meshing.Spines.Source.CIRCUIT:
            nmv.logger.info('Adding Spines from a BBP Circuit')
            self.build_circuit_spines()
        elif self.options.mesh.spines == nmv.enums.Meshing.Spines.Source.RANDOM:
            self.build_random_spines()
        else:
            return

    ################################################################################################
    # @finalize_meta_object
    ################################################################################################
    def finalize_meta_object(self):
        """Converts the meta object to a mesh and get it ready for export or visualization.
        """

        # Header
        nmv.logger.header('Meshing the Meta Object')

        # Deselect all objects
        nmv.scene.ops.deselect_all()

        # Update the resolution
        self.meta_skeleton.resolution = self.smallest_radius
        nmv.logger.info('Meta Resolution [%f]' % self.meta_skeleton.resolution)

        # Select the mesh
        self.meta_mesh = bpy.context.scene.objects[self.label]

        # Set the mesh to be the active one
        nmv.scene.set_active_object(self.meta_mesh)

        # Convert it to a mesh from meta-balls
        nmv.logger.info('Converting the Meta-object to a Mesh (Patience Please!)')
        bpy.ops.object.convert(target='MESH')

        # Update the label of the reconstructed mesh
        self.meta_mesh = bpy.context.scene.objects[0]
        self.meta_mesh.name = self.morphology.label

        # Re-select it again to be able to perform post-processing operations in it
        nmv.scene.select_object(self.meta_mesh)

        # Set the mesh to be the active one
        nmv.scene.set_active_object(self.meta_mesh)

        # Clean the mesh object and remove the non-manifold edges
        if not self.ignore_watertightness:
            nmv.logger.info('Cleaning Mesh Non-manifold Edges & Vertices')
            nmv.mesh.clean_mesh_object(self.meta_mesh)

        # Remove the islands (or small partitions from the mesh) and smooth it to look nice
        if self.options.mesh.soma_type == nmv.enums.Soma.Representation.SOFT_BODY:

            # Remove the small partitions
            nmv.logger.info('Removing Partitions')
            nmv.mesh.remove_small_partitions(self.meta_mesh)

            # Decimate
            nmv.logger.info('Decimating the Mesh')
            nmv.mesh.decimate_mesh_object(self.meta_mesh, decimation_ratio=0.25)

            # Smooth vertices to remove any sphere-like shapes
            nmv.logger.info('Smoothing the Mesh')
            nmv.mesh.smooth_object_vertices(self.meta_mesh, level=5)

    ################################################################################################
    # @add_surface_roughness
    ################################################################################################
    def add_surface_roughness(self):
        """Adds roughness to the surface of the mesh, compatible with the MetaBuilder.
        """

        # Ensure that the surface is rough
        if self.options.mesh.surface == nmv.enums.Meshing.Surface.ROUGH:

            # Decimate the neuron according to the meta resolution
            if self.meta_skeleton.resolution < 1.0:
                nmv.mesh.ops.decimate_mesh_object(mesh_object=self.meta_mesh,
                                                  decimation_ratio=self.meta_skeleton.resolution)

            # Add the surface distortion map
            nmv.mesh.add_surface_noise_to_mesh_using_displacement_modifier(
                mesh_object=self.meta_mesh, strength=1.0)

            nmv.mesh.ops.decimate_mesh_object(mesh_object=self.meta_mesh,
                                              decimation_ratio=0.25)

            nmv.mesh.ops.smooth_object(mesh_object=self.meta_mesh, level=1)

    ################################################################################################
    # @assign_material_to_mesh
    ################################################################################################
    def assign_material_to_mesh(self):

        # Deselect all objects
        nmv.scene.ops.deselect_all()

        # Activate the mesh object
        nmv.scene.set_active_object(self.meta_mesh)

        # Assign the material to the selected mesh
        nmv.shading.set_material_to_object(self.meta_mesh, self.soma_materials[0])

        # Update the UV mapping
        nmv.shading.adjust_material_uv(self.meta_mesh)

        # Activate the mesh object
        nmv.scene.set_active_object(self.meta_mesh)

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):
        """Reconstructs the neuronal mesh using meta objects.
        """

        nmv.logger.header('Building Mesh: MetaBuilder')

        # Verify and repair the morphology, if required
        result, stats = nmv.utilities.profile_function(self.update_morphology_skeleton)
        self.profiling_statistics += stats

        # Initialize the meta object
        # Note that self.label should be replaced by self.options.morphology.label
        result, stats = nmv.utilities.profile_function(
            self.initialize_meta_object, self.label)
        self.profiling_statistics += stats

        if self.options.mesh.soma_type == nmv.enums.Soma.Representation.SOFT_BODY:
            soma_building_function = self.build_soma_from_soft_body_mesh
        else:
            soma_building_function = self.build_soma_from_meta_objects

        # Build the soma
        result, stats = nmv.utilities.profile_function(soma_building_function)
        self.profiling_statistics += stats

        # Build the arbors
        result, stats = nmv.utilities.profile_function(self.build_arbors)
        self.profiling_statistics += stats
        
        # Building the endfeet 
        result, stats = nmv.utilities.profile_function(self.build_endfeet)
        self.profiling_statistics += stats

        # Building the spines from morphologies
        result, stats = nmv.utilities.profile_function(self.build_spines)
        self.profiling_statistics += stats

        # Finalize the meta object and construct a solid object
        result, stats = nmv.utilities.profile_function(self.finalize_meta_object)
        self.profiling_statistics += stats

        # Surface roughness
        result, stats = nmv.utilities.profile_function(self.add_surface_roughness)
        self.profiling_statistics += stats

        # Tessellation
        result, stats = nmv.utilities.profile_function(self.decimate_neuron_mesh)

        # Clean the mesh object and remove the non-manifold edges
        if not self.ignore_watertightness:
            nmv.logger.info('Cleaning Mesh Non-manifold Edges & Vertices')
            nmv.mesh.clean_mesh_object(self.meta_mesh)
            self.profiling_statistics += stats

        # Update the center of the mesh to the soma
        nmv.mesh.set_mesh_origin(
            mesh_object=self.meta_mesh, coordinate=self.morphology.soma.centroid)

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        self.create_skeleton_materials()

        # Assign the material to the mesh
        self.assign_material_to_mesh()

        # Transform to the global coordinates, if required
        result, stats = nmv.utilities.profile_function(self.transform_to_global_coordinates)
        self.profiling_statistics += stats

        # Collect the stats. of the mesh
        result, stats = nmv.utilities.profile_function(self.collect_mesh_stats)
        self.profiling_statistics += stats

        # Report
        nmv.logger.statistics_overall(self.profiling_statistics)

        # Write the stats to file
        self.write_statistics_to_file(tag='meta')

        # Create a new collection from the created objects of the mesh
        nmv.utilities.create_collection_with_objects(
            name='Mesh %s' % self.morphology.label, objects_list=[self.meta_mesh])

        # Return a reference to the reconstructed mesh
        return self.meta_mesh
