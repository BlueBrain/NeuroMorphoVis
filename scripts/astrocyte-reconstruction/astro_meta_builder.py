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
# @AstroMetaBuilder
####################################################################################################
class AstroMetaBuilder:
    """Mesh builder that creates high quality meshes with nice bifurcations based on meta objects
       for the astrocytes"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 soma_centroid,
                 soma_radius,
                 end_feet_proxy_meshes=None,
                 end_feet_thicknesses=None):
        """Constructor

        :param morphology:
            A given astrocyte morphology.
        :param soma_centroid:
            The center of the astrocyte soma.
        :param soma_radius:
            The radius of the astrocyte soma.
        :param end_feet_proxy_meshes:
            A list of the end-feet proxy meshes that will be used to create the actual end-feet.
        :param end_feet_thicknesses:
            A list of the end-feet thicknesses that will be used to create the actual end-feet.
        """

        # Morphology
        self.morphology = copy.deepcopy(morphology)

        # Soma centroid
        self.soma_centroid = soma_centroid

        # Soma radius
        self.soma_radius = soma_radius

        # End feet proxy meshes
        self.end_feet_proxy_meshes = end_feet_proxy_meshes

        # End feet thicknesses
        self.end_feet_thicknesses = end_feet_thicknesses

        # Meta object skeleton, used to build the skeleton of the morphology
        self.meta_skeleton = None

        # Meta object mesh, used to build the mesh of the morphology
        self.meta_mesh = None

        # A scale factor that was figured out by trial and error to correct the scaling of the radii
        self.magic_scale_factor = 1.575

        # The smallest detected radius while building the model, to be used for meta-ball resolution
        self.smallest_radius = 1e5

        # Statistics
        self.profiling_statistics = '\tMetaBuilder Profiles: \n'

        # Stats. about the morphology
        self.morphology_statistics = 'Morphology: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'MetaBuilder Mesh: \n'

        # Collect the error
        self.radii_error = list()

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

            radius_0 = samples[i].radius
            radius_1 = samples[i + 1].radius

            if radius_0 < 0.1:
                self.radii_error.append(1.0 - radius_0)
                radius_0 = 0.1

            if radius_1 < 0.1:
                radius_1 = 0.1

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
                          max_branching_order=1000):
        """Extrude the given arbor section by section recursively using meta objects.

        :param root:
            The root of a given section.
        :param max_branching_order:
            The maximum branching order set by the user to terminate the recursive call.
        """

        if root is None:
            return

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
        nmv.logger.header('Building Arbors')

        # Draw the apical dendrite, if exists
        if self.morphology.apical_dendrites is not None:
            for i, apical_dendrite in enumerate(self.morphology.apical_dendrites):
                nmv.logger.info('Apical Dendrite [%d]' % i)
                self.create_meta_arbor(root=apical_dendrite)

        # Draw the basal dendrites, if exist
        if self.morphology.basal_dendrites is not None:
            for i, basal_dendrite in enumerate(self.morphology.basal_dendrites):
                nmv.logger.info('Basal Dendrite [%d]' % i)
                self.create_meta_arbor(root=basal_dendrite)

        # Draw the axon, if exist
        if self.morphology.axons is not None:
            for i, axon in enumerate(self.morphology.axons):
                nmv.logger.info('Axon [%d]' % i)
                self.create_meta_arbor(root=axon)

    ################################################################################################
    # @build_endfeet
    ################################################################################################
    def build_endfeet(self):

        for i, mesh in enumerate(self.end_feet_proxy_meshes):

            vertex_list = list()
            for v in mesh.vertices:
                vertex_list.append(v.co)

            # Vertex list
            for v in vertex_list:

                # Add the meta element
                meta_element = self.meta_skeleton.elements.new()

                # Set its radius
                meta_element.radius = self.end_feet_thicknesses[i]

                if self.end_feet_thicknesses[i] < self.smallest_radius:
                    self.smallest_radius = self.end_feet_thicknesses[i]

                    # Update its coordinates
                meta_element.co = v

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

        # Create a new meta object that reflects the reconstructed mesh at the end of the operation
        self.meta_mesh = bpy.data.objects.new(name, self.meta_skeleton)

        # Get a reference to the scene
        scene = bpy.context.scene

        # Link the meta object to the scene
        nmv.scene.link_object_to_scene(self.meta_mesh)

        # Initial resolution of the meta skeleton, this will get updated later in the finalization
        self.meta_skeleton.resolution = 1.0
        nmv.logger.info('Meta Resolution [%f]' % self.meta_skeleton.resolution)

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

        # Assume that from the soma center towards the first point along the arbor is a segment
        self.create_meta_segment(
            p1=self.soma_centroid,
            p2=arbor.samples[0].point,
            r1=self.soma_radius,
            r2=arbor.samples[0].radius * self.magic_scale_factor)

    ################################################################################################
    # @build_soma_from_meta_objects
    ################################################################################################
    def build_soma_from_meta_objects(self):

        # Header
        nmv.logger.header('Building Soma from Meta Objects')

        # The apical dendrite must be valid
        if self.morphology.apical_dendrites is not None:
            for i, apical_dendrite in enumerate(self.morphology.apical_dendrites):
                nmv.logger.info('Dendrite [%d]' % i)
                self.emanate_soma_towards_arbor(arbor=apical_dendrite)

        if self.morphology.basal_dendrites is not None:
            for i, basal_dendrite in enumerate(self.morphology.basal_dendrites):
                nmv.logger.info('Dendrite [%d]' % i)
                self.emanate_soma_towards_arbor(arbor=basal_dendrite)

        # The axon must be valid
        if self.morphology.axons is not None:
            for i, axon in enumerate(self.morphology.axons):
                nmv.logger.info('Axon [%d]' % i)
                self.emanate_soma_towards_arbor(arbor=axon)

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
        self.meta_mesh = bpy.context.scene.objects[self.morphology.label]

        # Set the mesh to be the active one
        nmv.scene.set_active_object(self.meta_mesh)

        # Convert it to a mesh from meta-balls
        bpy.ops.object.convert(target='MESH')

        self.meta_mesh = bpy.context.scene.objects[0]
        self.meta_mesh.name = self.morphology.label

        # Re-select it again to be able to perform post-processing operations in it
        nmv.scene.select_object(self.meta_mesh)

        # Set the mesh to be the active one
        nmv.scene.set_active_object(self.meta_mesh)

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

        # Initialize the meta object
        result, stats = nmv.utilities.profile_function(
            self.initialize_meta_object, self.morphology.label)
        self.profiling_statistics += stats

        # Build the soma
        result, stats = nmv.utilities.profile_function(self.build_soma_from_meta_objects)
        self.profiling_statistics += stats

        # Build the arbors
        result, stats = nmv.utilities.profile_function(self.build_arbors)
        self.profiling_statistics += stats

        result, stats = nmv.utilities.profile_function(self.build_endfeet)
        self.profiling_statistics += stats

        # Finalize the meta object and construct a solid object
        result, stats = nmv.utilities.profile_function(self.finalize_meta_object)
        self.profiling_statistics += stats

        # Report
        nmv.logger.header('Mesh Reconstruction Done!')
        nmv.logger.log(self.profiling_statistics)

        # Return the reconstructed mesh
        return self.meta_mesh
