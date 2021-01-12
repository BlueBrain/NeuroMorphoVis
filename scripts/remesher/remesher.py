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
import nmv.physics
import nmv.options


####################################################################################################
# @AstroMetaBuilder
####################################################################################################
class MetaBuilderRemesher:
    """Remesher based on a particle-systems and Metaballs to create high fidelity meshes that can
    be connected to surfaces in a clean and simple way"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 input_mesh):
        """Constructor

        :param input_mesh:
            A given mesh to get remeshed.
        """

        # Morphology
        self.input_mesh = input_mesh

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
    # @build_proxy_mesh_with_particle_simulation
    ################################################################################################
    def build_proxy_mesh_with_particle_simulation(self):
        """Build the proxy mesh with the particle simulation
        """

        # Select the input mesh
        nmv.scene.select_object(scene_object=self.input_mesh)

        # Run the particles simulation remesher
        mesher = nmv.physics.ParticleRemesher(resolution=20, mask_resolution=20)
        stepper = mesher.run(mesh_object=self.input_mesh, context=bpy.context, interactive=True)

        for i in range(1000000):
            finished = next(stepper)
            if finished:
                break

    ################################################################################################
    # @build_meta_field_with_meta_balls
    ################################################################################################
    def build_meta_field_with_meta_balls(self):
        """Builds the meta filed with meta balls
        """

        # Build the soma profile from the soft-body mesh
        for face in self.input_mesh.data.polygons:

            # Add a new meta element
            meta_element = self.meta_skeleton.elements.new()

            # Compute the largest radius in the triangle, but since we re-mesh the soma, we will
            # get almost equi-sides faces
            radius = nmv.mesh.get_largest_radius_in_face(
                mesh_object=self.input_mesh, face_index=face.index)

            # Compute the radius of the meta-element by trial-and-error
            meta_element.radius = radius * 2 * self.magic_scale_factor

            if meta_element.radius < self.smallest_radius:
                self.smallest_radius = meta_element.radius

            # Update its coordinates
            meta_element.co = face.center - (face.normal * radius * self.magic_scale_factor)

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

        # Make sure that the mesh is located at the centroid
        self.meta_mesh.location = self.input_mesh.location

        # Link the meta object to the scene
        nmv.scene.link_object_to_scene(self.meta_mesh)

        # Initial resolution of the meta skeleton, this will get updated later in the finalization
        self.meta_skeleton.resolution = 1.0
        nmv.logger.info('Meta Resolution [%f]' % self.meta_skeleton.resolution)

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
        self.meta_mesh = bpy.context.scene.objects[self.input_mesh.name + '.001']

        # Set the mesh to be the active one
        nmv.scene.set_active_object(self.meta_mesh)

        # Convert it to a mesh from meta-balls
        nmv.logger.info('Converting the Meta-object to a Mesh')
        bpy.ops.object.convert(target='MESH')

        nmv.logger.info('Labeling')
        self.meta_mesh = bpy.context.scene.objects[0]
        self.meta_mesh.name = self.input_mesh.name + '_reconstructed'

        # Re-select it again to be able to perform post-processing operations in it
        nmv.scene.select_object(self.meta_mesh)

        # Set the mesh to be the active one
        nmv.scene.set_active_object(self.meta_mesh)
        
        # Remove the small partitions
        nmv.logger.info('Removing Partitions')
        nmv.mesh.remove_small_partitions(self.meta_mesh)

        # Clean the mesh object and remove the non-manifold edges
        nmv.logger.info('Cleaning Mesh Non-manifold Edges & Vertices')
        nmv.mesh.clean_mesh_object(self.meta_mesh)

        # Remove the small partitions
        nmv.logger.info('Removing Partitions')
        nmv.mesh.remove_small_partitions(self.meta_mesh)

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):
        """Reconstructs the neuronal mesh using meta objects.
        """

        self.build_proxy_mesh_with_particle_simulation()

        # Initialize the meta object
        result, stats = nmv.utilities.profile_function(
            self.initialize_meta_object,  self.input_mesh.name)
        self.profiling_statistics += stats

        self.build_meta_field_with_meta_balls()

        # Finalize the meta object and construct a solid object
        result, stats = nmv.utilities.profile_function(self.finalize_meta_object)
        self.profiling_statistics += stats

        # Report
        nmv.logger.header('Mesh Reconstruction Done!')
        nmv.logger.log(self.profiling_statistics)

        # Return the reconstructed mesh
        return self.meta_mesh
