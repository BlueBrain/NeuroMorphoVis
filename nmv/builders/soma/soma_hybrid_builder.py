####################################################################################################
# Copyright (c) 2016 - 2021, EPFL / Blue Brain Project
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
import copy

# Blender imports
import bpy
from mathutils import Vector

import nmv.bmeshi
import nmv.consts
import nmv.enums
import nmv.mesh
import nmv.physics
import nmv.scene
import nmv.shading
import nmv.skeleton
import nmv.utilities
import nmv.options


####################################################################################################
# @SomaHybridBuilder
####################################################################################################
class SomaHybridBuilder:
    """Soma reconstruction using a hybrid method that combines the soft-body physics and Metaballs.
    The somata reconstructed with this builder are high fidelity, but the soma defintion must have
    valid data, otherwise it will create weird somatic surface.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology.
        :param options:
            System options.
        """

        # Morphology
        self.morphology = morphology

        # All the options of the project (an instance of MeshyOptions)
        self.options = options

        # Meta object skeleton, used to build the skeleton of the soma before making it a mesh
        self.meta_skeleton = None

        # Meta object mesh, used to build the mesh of the soma
        self.meta_mesh = None

        # A scale factor that was figured out by trial and error to correct the scaling of the radii
        self.magic_scale_factor = 1.575

        # A scale factor that was figured by trial-and-error to correct the scaling of the somata
        # reconstructed from the soft-body meshes
        self.soma_scaling_factor = 1.5

        # The smallest detected radius while building the model, to be used for meta-ball resolution
        self.smallest_radius = 10.0

        # Set the initial soma radius to half of its mean radius
        self.initial_soma_radius = morphology.soma.smallest_radius

        # Ensure the connection between the arbors and the soma
        nmv.skeleton.ops.verify_arbors_connectivity_to_soma(self.morphology)

    ################################################################################################
    # @initialize_meta_object
    ################################################################################################
    def initialize_meta_object(self,
                               name):
        """Constructs and initialize a new meta object that will be the basis of the mesh.

        :param name:
            Meta-object name.
        """

        nmv.logger.info('Initialization')

        # Create a new meta skeleton that will be used to reconstruct the skeleton frame
        self.meta_skeleton = bpy.data.metaballs.new(name)

        # Create a new meta object that reflects the reconstructed mesh at the end of the operation
        self.meta_mesh = bpy.data.objects.new(name, self.meta_skeleton)

        # Adjust the location of the meta_mesh
        self.meta_mesh.location = self.morphology.soma.centroid

        # Link the meta object to the scene
        nmv.scene.link_object_to_scene(self.meta_mesh)

        # Initial resolution of the meta skeleton, this will get updated later in the finalization
        self.meta_skeleton.resolution = 1.0
        nmv.logger.detail('Meta resolution [%f]' % self.meta_skeleton.resolution)

    ################################################################################################
    # @finalize_meta_object
    ################################################################################################
    def finalize_meta_object(self,
                             name):
        """Converts the meta object to a mesh and get it ready for export or visualization.
        """

        # Header
        nmv.logger.info('Converting soma profile to a mesh')

        # Deselect all objects
        nmv.scene.ops.deselect_all()

        # Update the resolution
        self.meta_skeleton.resolution = self.smallest_radius
        nmv.logger.detail('Meta resolution [%f]' % self.meta_skeleton.resolution)

        # Select the mesh
        self.meta_mesh = bpy.context.scene.objects[name]

        # Set the mesh to be the active one
        nmv.scene.set_active_object(self.meta_mesh)

        # Convert it to a mesh from meta-balls
        bpy.ops.object.convert(target='MESH')

        # Deselect all objects
        nmv.scene.deselect_all()

        # Select the soma object
        # Note the conversion from the meta object to the mesh object adds automatically '.001'
        # to the object name, therefore we must rename it
        self.meta_mesh = bpy.context.scene.objects['%s.001' % name]
        self.meta_mesh.name = name

        # Re-select it again to be able to perform post-processing operations in it
        nmv.scene.select_object(self.meta_mesh)

        # Set the mesh to be the active one
        nmv.scene.set_active_object(self.meta_mesh)

        # Decimate the mesh a little bit
        nmv.mesh.decimate_mesh_object(mesh_object=self.meta_mesh, decimation_ratio=0.25)

    ################################################################################################
    # @assign_material_to_mesh
    ################################################################################################
    def assign_material_to_mesh(self):

        # Create the soma material and assign it to the ico-sphere
        soma_material = nmv.shading.create_material(
            name='soma_material', color=self.options.shading.soma_color,
            material_type=self.options.shading.soma_material)

        # Create an illumination specific for the given material
        nmv.shading.create_material_specific_illumination(self.options.shading.soma_material)

        # Deselect all objects
        nmv.scene.ops.deselect_all()

        # Activate the mesh object
        nmv.scene.set_active_object(self.meta_mesh)

        # Assign the material to the selected mesh
        nmv.shading.set_material_to_object(self.meta_mesh, soma_material)

        # Update the UV mapping
        nmv.shading.adjust_material_uv(self.meta_mesh)

        # Activate the mesh object
        nmv.scene.set_active_object(self.meta_mesh)

    ################################################################################################
    # @add_noise_to_soma_surface
    ################################################################################################
    def add_noise_to_soma_surface(self,
                                  delta=0.5):
        """Add some random noise of the soma surface to make it a little bit realistic.

        :param delta:
            The noise delta, by default 0.25.
        """

        nmv.logger.info('Adding random noise')

        # Decimation
        nmv.mesh.decimate_mesh_object(mesh_object=self.meta_mesh, decimation_ratio=0.5)

        # Adding perturbations
        for i in range(len(self.meta_mesh.data.vertices)):
            vertex = self.meta_mesh.data.vertices[i]
            vertex.select = True
            vertex.co = vertex.co + (vertex.normal * random.uniform(-delta / 2.0, delta / 2.0))
            vertex.select = False

        # Smoothing
        nmv.mesh.smooth_object(mesh_object=self.meta_mesh, level=2)

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
        while travelled_distance < segment_length:

            # Make a meta ball (or sphere) at this point
            meta_element = self.meta_skeleton.elements.new()

            # Set its radius
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
    # @emanate_soma_towards_arbor
    ################################################################################################
    def emanate_soma_towards_arbor(self,
                                   arbor):
        """Extends the space of the soma towards the given arbor to make a shape that is not sphere.

        NOTE: The arbor must be connected to the soma to apply this operation, otherwise it
        is ignored.

        :param arbor:
            A given arbor to emanate the soma towards.
        """

        # The arbor must NOT be far from the soma
        if not arbor.far_from_soma:

            # Assume that from the soma center towards the first point along the arbor is a segment
            p1 = Vector((self.morphology.soma.centroid[0],
                         self.morphology.soma.centroid[1],
                         self.morphology.soma.centroid[2]))
            p2 = arbor.samples[0].point

            # Assume that from the soma center towards the first point along the arbor is a segment
            self.create_meta_segment(
                p1=p1,
                p2=p2,
                r1=self.morphology.soma.smallest_radius,
                r2=arbor.samples[0].radius * self.magic_scale_factor)

    ################################################################################################
    # @emanate_towards_the_branches
    ################################################################################################
    def emanate_towards_the_branches(self):
        """Emanates the soma towards the branches.
        """

        # Header
        nmv.logger.info('Extruding towards arbors')

        # Verify the proximity of the arbors to the soma
        nmv.skeleton.verify_arbors_connectivity_to_soma(morphology=self.morphology)

        # Get a list of valid arbors where we can pull the sphere towards without being intersecting
        valid_arbors = nmv.skeleton.get_connected_arbors_to_soma_after_verification(
            morphology=self.morphology, soma_radius=self.initial_soma_radius)

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
                for arbor in valid_apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.emanate_soma_towards_arbor(arbor=arbor)

        # Emanate towards basal dendrites, if exist
        if self.morphology.has_basal_dendrites():
            if not self.options.morphology.ignore_basal_dendrites:
                for arbor in valid_basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.emanate_soma_towards_arbor(arbor=arbor)

        # Emanate towards axons, if exist
        if self.morphology.has_axons():
            if not self.options.morphology.ignore_axons:
                for arbor in valid_axons:
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

        # Run the particles simulation re-mesher
        particle_remeshes = nmv.physics.ParticleRemesher()
        stepper = particle_remeshes.run(mesh_object=soft_body_soma,
                                        context=bpy.context, interactive=True)

        # Iterate
        for i in range(1000000):
            finished = next(stepper)

            # If the finished state was over, go ahead and break
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
        for i, face in enumerate(soft_body_soma.data.polygons):

            # Add a new meta element
            meta_element = self.meta_skeleton.elements.new()

            # Compute the largest radius in the triangle, but since we re-mesh the soma, we will
            # get almost equi-sides faces
            radius = nmv.mesh.get_largest_radius_in_face(
                mesh_object=soft_body_soma, face_index=face.index)

            # Compute the radius of the meta-element by trial-and-error
            meta_element.radius = radius * 2 * self.magic_scale_factor

            if meta_element.radius < self.smallest_radius:
                self.smallest_radius = meta_element.radius

            # Update its coordinates
            meta_element.co = face.center - (face.normal * radius * self.soma_scaling_factor)

        # Delete the mesh
        nmv.scene.delete_object_in_scene(scene_object=soft_body_soma)

        # Return a reference to the valid arbors that are connected to the soma
        return valid_arbors

    ################################################################################################
    # @reconstruct_soma_mesh
    ################################################################################################
    def reconstruct_soma_mesh(self,
                              apply_shader=True,
                              add_noise_to_surface=False):
        """Reconstructs the mesh of the soma of the neuron in a single step.

        :param apply_shader:
            Apply the given soma shader in the configuration. This flag will be set to False when
            the soma is created in another builder such as the skeleton builder or the piecewise
            mesh builder.
        :param add_noise_to_surface:
            Adds noise to the surface of the soma to make it much more realistic.
        :return:
            A reference to the reconstructed mesh of the soma.
        """

        # Header
        nmv.logger.header('Soma reconstruction with MetaBalls')

        # Initialize the MetaObject before emanating towards the branches
        self.initialize_meta_object(name=nmv.consts.Skeleton.SOMA_PREFIX)

        # Emanate the basic sphere towards the branches
        valid_arbors = self.build_soma_from_soft_body_mesh()

        # Update the meta object and convert it to a mesh
        self.finalize_meta_object(name=nmv.consts.Skeleton.SOMA_PREFIX)

        # Remove the internal partition
        nmv.mesh.remove_small_partitions(mesh_object=self.meta_mesh)

        # Smooth the mesh surface, the level (13) was obtained by trial and error
        nmv.mesh.smooth_object_vertices(mesh_object=self.meta_mesh, level=15)

        # Assign the material to the reconstructed mesh
        if apply_shader:
            self.assign_material_to_mesh()

        # A dd a little bit of noise
        if add_noise_to_surface:
            self.add_noise_to_soma_surface()

        # Return a reference to the reconstructed mesh
        return self.meta_mesh

    ################################################################################################
    # @get_soma_profile
    ################################################################################################
    def get_soma_profile(self):
        """Returns the profile of the soma as a list of coordinates.

        :return:
            The profile of the soma as a list of coordinates.
        """

        # Initialize the MetaObject before emanating towards the branches
        self.initialize_meta_object(name='SomaProfile')

        # Emanate the basic sphere towards the branches
        self.build_soma_from_soft_body_mesh()

        # Update the meta object and convert it to a mesh
        self.finalize_meta_object(name='SomaProfile')

        # List of vertices
        vertices = copy.deepcopy(nmv.mesh.get_vertices_in_object(self.meta_mesh))

        # delete the soma
        nmv.scene.delete_object_in_scene(self.meta_mesh)

        # Return the vertices list
        return vertices
