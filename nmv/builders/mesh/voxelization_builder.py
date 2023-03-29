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

        # Statistics
        self.profiling_statistics = 'VoxelizationBuilder Profiling Stats.: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'VoxelizationBuilder Mesh: \n'

        # Verify the connectivity of the arbors to the soma
        nmv.skeleton.verify_arbors_connectivity_to_soma(morphology=self.morphology)

    ################################################################################################
    # @build_proxy_mesh_using_articulated_sections_builder
    ################################################################################################
    def build_proxy_mesh_using_articulated_sections_builder(self):

        # Adjust the options to force the articulated sections method
        self.options.morphology.reconstruction_method = \
            nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS

        # Adjust the options to use the soma-generation method of the mesh toolbox
        self.options.morphology.soma_representation = self.options.mesh.soma_type

        # Create the morphology builder and generate the morphology skeleton
        morphology_builder = nmv.builders.DisconnectedSectionsBuilder(
            morphology=self.morphology, options=self.options)

        # Generate a list of objects (currently morphologies)
        objects = morphology_builder.draw_morphology_skeleton()

        # Convert the morphologies into meshes
        for i_object in objects:
            nmv.scene.convert_object_to_mesh(scene_object=i_object)

        # Join all the objects into a single mesh object
        mesh_object = nmv.scene.join_objects(scene_objects=objects)

        # Apply the voxelization-based re-meshing modifier to create a new mesh
        nmv.mesh.apply_voxelization_remeshing_modifier(
            mesh_object=mesh_object, voxel_size=0.15)

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):
        self.build_proxy_mesh_using_articulated_sections_builder()


