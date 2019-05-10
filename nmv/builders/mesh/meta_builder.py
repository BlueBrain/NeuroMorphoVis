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

# Syetsm imports
import copy, os

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
        self.morphology = copy.deepcopy(morphology)

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

        # Meta object skeleton, used to build the skeleton of the morphology
        self.meta_skeleton = None

        # Meta object mesh, used to build the mesh of the morphology
        self.meta_mesh = None

        # A scale factor that was figured out by trial and error to correct the scaling of the radii
        self.magic_scale_factor = 1.575

        # The smallest detected radius while building the model, to be used for meta-ball resolution
        self.smallest_radius = 1e5

        # Statistics
        self.profiling_statistics = 'MetaBuilder Profiles: \n'

        # Stats. about the morphology
        self.morphology_statistics = 'Morphology: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'MetaBuilder Mesh: \n'

    ################################################################################################
    # @verify_morphology_skeleton
    ################################################################################################
    def verify_morphology_skeleton(self):
        """Verifies and repairs the morphology if the contain any artifacts that would potentially
        affect the reconstruction quality of the mesh.
        """

        # Remove the internal samples, or the samples that intersect the soma at the first
        # section and each arbor
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.ops.remove_samples_inside_soma])

        # Verify the connectivity of the arbors to the soma to filter the disconnected arbors,
        # for example, an axon that is emanating from a dendrite or two intersecting dendrites
        nmv.skeleton.ops.update_arbors_connection_to_soma(self.morphology)

        # Label the primary and secondary sections based on angles
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology,
              nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_angles])

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
        """

        # Header
        nmv.logger.header('Building Arbors')

        # Draw the apical dendrite, if exists
        if not self.options.morphology.ignore_apical_dendrite:
            if self.morphology.apical_dendrite is not None:
                nmv.logger.info('Apical Dendrite')
                self.create_meta_arbor(
                    root=self.morphology.apical_dendrite,
                    max_branching_order=self.options.morphology.apical_dendrite_branch_order)

        # Draw the basal dendrites, if exist
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.dendrites is not None:
                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.info('Dendrite [%d]' % i)
                    self.create_meta_arbor(
                        root=basal_dendrite,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order)

        # Draw the axon, if exist
        if not self.options.morphology.ignore_axon:
            if self.morphology.axon is not None:
                nmv.logger.info('Axon')
                self.create_meta_arbor(
                    root=self.morphology.axon,
                    max_branching_order=self.options.morphology.axon_branch_order)

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
        scene.objects.link(self.meta_mesh)

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

        # The arbor must be connected to the soma
        if arbor.connected_to_soma:

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

        if self.morphology.dendrites is not None:

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
        """

        # Header
        nmv.logger.header('Meshing the Meta Object')

        # Deselect all objects
        nmv.scene.ops.deselect_all()

        # Update the resolution
        self.meta_skeleton.resolution = self.smallest_radius * 2.0
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
        self.meta_mesh.select = True

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

        # Verify and repair the morphology, if required
        result, stats = nmv.utilities.profile_function(self.verify_morphology_skeleton)
        self.profiling_statistics += stats

        # Apply skeleton-based operation, if required, to slightly modify the skeleton
        result, stats = nmv.utilities.profile_function(
            nmv.builders.common.modify_morphology_skeleton, self)
        self.profiling_statistics += stats

        # Initialize the meta object
        result, stats = nmv.utilities.profile_function(
            self.initialize_meta_object, self.options.morphology.label)
        self.profiling_statistics += stats

        # Build the soma
        result, stats = nmv.utilities.profile_function(self.build_soma_from_meta_objects)
        self.profiling_statistics += stats

        # Build the arbors
        # TODO: Adding the spines should be part of the meshing using the spine morphologies
        result, stats = nmv.utilities.profile_function(self.build_arbors)
        self.profiling_statistics += stats

        # Finalize the meta object and construct a solid object
        result, stats = nmv.utilities.profile_function(self.finalize_meta_object)
        self.profiling_statistics += stats

        # Tessellation
        result, stats = nmv.utilities.profile_function(
            nmv.builders.common.decimate_neuron_mesh, self)
        self.profiling_statistics += stats

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        nmv.builders.common.create_skeleton_materials(builder=self)

        # Assign the material to the mesh
        self.assign_material_to_mesh()

        # Transform to the global coordinates, if required
        result, stats = nmv.utilities.profile_function(
            nmv.builders.transform_to_global_coordinates, self)
        self.profiling_statistics += stats

        # Collect the stats. of the mesh
        result, stats = nmv.utilities.profile_function(nmv.builders.collect_mesh_stats, self)
        self.profiling_statistics += stats

        # Report
        nmv.logger.header('Mesh Reconstruction Done!')
        nmv.logger.log(self.profiling_statistics)

        # Write the stats to file
        nmv.builders.write_statistics_to_file(builder=self, tag='meta')
