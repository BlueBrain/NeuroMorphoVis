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

# Internal modules
from .base import MeshBuilderBase
import nmv.builders
import nmv.enums
import nmv.mesh
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities


####################################################################################################
# @VoxelizationBuilder
####################################################################################################
class VoxelizationBuilder(MeshBuilderBase):
    """Mesh builder that creates watertight meshes using voxelization.
    Notes:
        - This builder works with Blender 3.0 and beyond.
        - The meshes produced by this builder are watertight.
    """

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

        # Initialize the parent with the common parameters
        MeshBuilderBase.__init__(self, morphology, options)

        # A reference to the reconstructed soma mesh
        self.soma_mesh = None

        # A list of the reconstructed meshes of the apical dendrites
        self.apical_dendrites_meshes = list()

        # A list of the reconstructed meshes of the basal dendrites
        self.basal_dendrites_meshes = list()

        # A list of the reconstructed meshes of the axon
        self.axons_meshes = list()

        # A list of the endfeet meshes, if exist
        self.endfeet_meshes = list()

        # A reference to the reconstructed mesh
        self.mesh = None

        # Statistics
        self.profiling_statistics = 'VoxelizationBuilder Profiling Stats.: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'VoxelizationBuilder Mesh: \n'

        # Verify the connectivity of the arbors to the soma
        nmv.skeleton.verify_arbors_connectivity_to_soma(morphology=self.morphology)

    ################################################################################################
    # @assign_material_to_mesh
    ################################################################################################
    def assign_material_to_mesh(self):

        self.create_skeleton_materials()

        # Deselect all objects
        nmv.scene.ops.deselect_all()

        # Activate the mesh object
        nmv.scene.set_active_object(self.mesh)

        # Assign the material to the selected mesh
        nmv.shading.set_material_to_object(self.mesh, self.soma_materials[0])

        # Update the UV mapping
        nmv.shading.adjust_material_uv(self.mesh)

        # Activate the mesh object
        nmv.scene.set_active_object(self.mesh)

    ################################################################################################
    # @build_proxy_mesh_using_articulated_sections_builder
    ################################################################################################
    def build_proxy_mesh_using_articulated_sections_builder(self):

        # Adjust the options to force the articulated sections method
        self.options.morphology.reconstruction_method = \
            nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS

        # Adjust the options to use the soma-generation method of the mesh toolbox
        self.options.morphology.soma_representation = self.options.mesh.soma_type

        # Adjust the minimum radius to 0.1 to avoid discontinuities
        nmv.skeleton.set_smallest_sample_radius_to_value(
            morphology=self.morphology, smallest_radius=0.1)

        # Create the morphology builder and generate the morphology skeleton
        morphology_builder = nmv.builders.DisconnectedSectionsBuilder(
            morphology=self.morphology, options=self.options)

        # Generate a list of objects (currently morphologies)
        objects = morphology_builder.draw_morphology_skeleton()

        # Convert the morphologies into meshes, if not meshes
        for i_object in objects:
            nmv.scene.convert_object_to_mesh(scene_object=i_object)

        # Join all the objects into a single mesh object
        self.mesh = nmv.scene.join_objects(scene_objects=objects)

    ################################################################################################
    # @remesh_with_voxelization_modifier
    ################################################################################################
    def remesh_with_voxelization_modifier(self):
        """Apply the voxelization-based re-meshing modifier to create a new mesh."""

        # Apply the modifier
        nmv.mesh.apply_voxelization_remeshing_modifier(
            mesh_object=self.mesh, voxel_size=0.1)

    ################################################################################################
    # @adjust_mesh_origin
    ################################################################################################
    def adjust_mesh_origin(self):
        """Adjusts the origin of the mesh to be located at the soma."""

        pass


    ################################################################################################
    # @post_process_mesh
    ################################################################################################
    def post_process_mesh(self):
        """Post-processes the resulting mesh to create a clean one"""

        nmv.logger.info('Post processing')

        # Remove doubles
        # nmv.mesh.remove_doubles(mesh_object=self.mesh, distance=0.01)

        # Smooth vertices to remove any sphere-like shapes
        nmv.mesh.smooth_object_vertices(self.mesh, level=5)

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):

        nmv.logger.header('Building Mesh: VoxelizationBuilder')

        # Verify and repair the morphology, if required
        result, stats = nmv.utilities.profile_function(self.update_morphology_skeleton)
        self.profiling_statistics += stats

        result, stats = nmv.utilities.profile_function(
            self.build_proxy_mesh_using_articulated_sections_builder)
        self.profiling_statistics += stats

        # Voxelization modifier
        result, stats = nmv.utilities.profile_function(self.remesh_with_voxelization_modifier)
        self.profiling_statistics += stats

        # Adjust the origin of the mesh
        result, stats = nmv.utilities.profile_function(self.post_process_mesh)
        self.profiling_statistics += stats

        # Assign the material to the mesh
        result, stats = nmv.utilities.profile_function(self.assign_material_to_mesh)
        self.profiling_statistics += stats

        # Adjust the origin of the mesh
        result, stats = nmv.utilities.profile_function(self.adjust_mesh_origin)
        self.profiling_statistics += stats

        # Collect the stats. of the mesh
        result, stats = nmv.utilities.profile_function(self.collect_mesh_stats)
        self.profiling_statistics += stats

        # Report
        nmv.logger.statistics(self.profiling_statistics)

        # Write the stats to file
        self.write_statistics_to_file(tag='voxelization')

        # Create a new collection from the created objects of the mesh
        nmv.utilities.create_collection_with_objects(
            name='Mesh %s' % self.morphology.label, objects_list=[self.mesh])


