####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
        - If the mesh optimization library (omesh) is available, the final mesh will be optimized.
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
        MeshBuilderBase.__init__(self, morphology, options, 'voxelization')

        # Voxelization resolution use for the re-meshing modifier
        self.voxelization_resolution = 0.1

        # Statistics
        self.profiling_statistics = 'VoxelizationBuilder Profiling Stats.: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'VoxelizationBuilder Mesh: \n'

    ################################################################################################
    # @confirm_single_or_multiple_mesh_objects
    ################################################################################################
    def confirm_single_or_multiple_mesh_objects(self):
        """The resulting mesh from this builder is always contained in a single object."""

        self.result_is_single_object_mesh = True

    ################################################################################################
    # @resample_skeleton_adaptive_relaxed
    ################################################################################################
    def resample_skeleton_adaptive_relaxed(self):
        """Resamples the morphology skeleton using the adaptive relaxed method."""

        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.resample_section_adaptively_relaxed])

    ################################################################################################
    # @initialize_builder
    ################################################################################################
    def initialize_builder(self):
        """Initializes the different parameters/options of the builder required for building."""

        # Create the materials of the morphology skeleton
        self.create_skeleton_materials()

        # Is it a single object or multiple objects
        self.confirm_single_or_multiple_mesh_objects()

        # Modify the morphology skeleton, if required
        self.modify_morphology_skeleton()

        # Remove the internal samples of the arbors that are located within the soma extent
        self.remove_arbors_samples_inside_soma()

        # Resample the morphology skeleton using the adaptive relaxed method
        # self.resample_skeleton_adaptive_relaxed()

        # Verify the connectivity of the arbors to the soma
        nmv.skeleton.verify_arbors_connectivity_to_soma(morphology=self.morphology)

        # Computes the smallest radius of the morphology skeleton until the specified branch order
        smallest_radius = nmv.skeleton.get_smallest_sample_radius_of_trimmed_morphology(
            morphology=self.morphology,
            axon_branch_order=self.options.morphology.axon_branch_order,
            basal_dendrites_branch_order=self.options.morphology.basal_dendrites_branch_order,
            apical_dendrite_branch_order=self.options.morphology.apical_dendrite_branch_order)

        # Get the voxelization resolution
        if smallest_radius < 0.1:
            self.voxelization_resolution = 0.1 * 0.75
        else:
            self.voxelization_resolution = smallest_radius * 0.75

        # If the spines are loaded, use resolution 0.05
        if self.options.mesh.spines != nmv.enums.Meshing.Spines.Source.IGNORE:
            self.voxelization_resolution = 0.05

        nmv.logger.info('Voxelization Resolution [%f]' % self.voxelization_resolution)

        # Optimized meta-ball soma resolution for the voxelization modifier
        self.options.soma.meta_ball_resolution = self.voxelization_resolution

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
            morphology=self.morphology, smallest_radius=0.2)

        # Create the morphology builder and generate the morphology skeleton
        morphology_builder = nmv.builders.DisconnectedSectionsBuilder(
            morphology=self.morphology, options=self.options)

        # Generate a list of objects (currently morphologies)
        objects = morphology_builder.draw_morphology_skeleton()

        # Convert the morphologies into meshes, if not meshes
        for i_object in objects:
            nmv.scene.convert_object_to_mesh(scene_object=i_object)

        # Join all the objects into a single mesh object
        self.neuron_mesh = nmv.scene.join_objects(scene_objects=objects)

    ################################################################################################
    # @build_proxy_mesh_using_connected_sections_builder
    ################################################################################################
    def build_proxy_mesh_using_connected_sections_builder(self):

        # Adjust the minimum radius to 0.1 to avoid discontinuities
        nmv.skeleton.set_smallest_sample_radius_to_value(
            morphology=self.morphology, smallest_radius=0.2)

        # Create the proxy mesh builder and generate the morphology skeleton
        proxy_mesh_builder = nmv.builders.PiecewiseBuilder(
            morphology=self.morphology, options=self.options, this_is_proxy_mesh=True)

        # Reconstruct the proxy mesh
        self.neuron_mesh = proxy_mesh_builder.reconstruct_mesh()[0]

    ################################################################################################
    # @apply_voxelization_modifier
    ################################################################################################
    def apply_voxelization_modifier(self):
        """Apply the voxelization-based re-meshing modifier to create a new mesh."""

        # Consider the adaptivity
        topology = self.options.mesh.topology_tessellation
        if topology == nmv.enums.Meshing.TopologyTessellation.VOXEL_REMESHER:
            adaptivity = 0.25
        else:
            adaptivity = 0.0

        nmv.logger.info('Applying the voxelization finalization [Resolution: %f, Adaptivity %f]'
                        % (self.voxelization_resolution, adaptivity))

        # Apply the modifier
        nmv.mesh.apply_voxelization_remeshing_modifier(
            mesh_object=self.neuron_mesh, voxel_size=self.voxelization_resolution,
            adaptivity=adaptivity)

    ################################################################################################
    # @adjust_origin_to_soma_center
    ################################################################################################
    def adjust_origin_to_soma_center(self):
        nmv.mesh.set_mesh_origin(
            mesh_object=self.neuron_mesh, coordinate=self.morphology.soma.centroid)

    ################################################################################################
    # @build_proxy_mesh
    ################################################################################################
    def build_proxy_mesh(self):
        """Builds the proxy mesh that will be used for the voxelization"""

        # Ensure that we use a high quality cross-sectional bevel
        self.options.morphology.bevel_object_sides = 16
        if self.options.mesh.proxy_mesh_method == nmv.enums.Meshing.Proxy.CONNECTED_SECTIONS:
            return self.build_proxy_mesh_using_connected_sections_builder()
        else:
            return self.build_proxy_mesh_using_articulated_sections_builder()

    ################################################################################################
    # @finalize_mesh
    ################################################################################################
    def finalize_mesh(self):
        """Finalize the resulting mesh to create a clean one."""

        nmv.logger.info('Mesh finalization')

        # Create the soma material and assign it to the final object
        self.create_soma_materials()
        self.assign_material_to_single_object_mesh()

        # Adjust the origin of the mesh
        self.adjust_origin_to_soma_center()

        # Create a new collection from the created objects of the mesh
        nmv.utilities.create_collection_with_objects(
            name='Mesh %s' % self.morphology.label, objects_list=self.neuron_meshes)

    ################################################################################################
    # @clean_mesh
    ################################################################################################
    def clean_mesh(self):
        """Cleans the resulting mesh."""

        # Remove doubles
        if self.options.mesh.remove_small_edges:
            nmv.mesh.remove_doubles(mesh_object=self.neuron_mesh, distance=0.01)

        # Smooth vertices to remove any sphere-like shapes
        nmv.mesh.smooth_object_vertices(self.neuron_mesh, level=1)

    ################################################################################################
    # @add_surface_roughness
    ################################################################################################
    def add_surface_roughness(self):
        """Adds surface noise to the mesh to make it looking realistic as seen by microscopes."""

        if self.options.mesh.surface == nmv.enums.Meshing.Surface.ROUGH:
            nmv.logger.info('Adding surface noise')
            nmv.mesh.add_surface_noise_to_mesh_using_displacement_modifier(
                mesh_object=self.neuron_mesh, strength=1.5, noise_scale=1.5, noise_depth=2)

    ################################################################################################
    # @optimize_mesh
    ################################################################################################
    def optimize_mesh(self):
        """Optimizes the mesh surface using the OMesh (optimization mesh) library."""

        nmv.logger.info('Optimization')

        topology = self.options.mesh.topology_tessellation
        if topology == nmv.enums.Meshing.TopologyTessellation.VOXEL_REMESHER:
            self.neuron_mesh = nmv.mesh.optimize_mesh(
                mesh_object=self.neuron_mesh, coarse=False, smooth=True, delete_input_mesh=True)
            self.neuron_mesh = nmv.mesh.optimize_mesh(
                mesh_object=self.neuron_mesh, coarse=True, smooth=True, delete_input_mesh=True)
        elif topology == nmv.enums.Meshing.TopologyTessellation.OMESH_TESSELLATION:
            self.neuron_mesh = nmv.mesh.optimize_mesh(
                mesh_object=self.neuron_mesh, coarse=True, smooth=True, delete_input_mesh=True)
        else:
            pass


    def draw_sections(self):

        basal_dendrites_sections = self.morphology.get_basal_dendrites_sections_list()

        threshold = 0.4

        # Retrieve the 'safe' sections, which have minimum radius greater than the threshold
        thick_sections = list()
        thin_sections = list()
        for i_section in basal_dendrites_sections:
            if nmv.skeleton.compute_section_minimum_radius(section=i_section) > threshold:
                thick_sections.append(i_section)
            else:
                if nmv.skeleton.compute_section_average_radius(section=i_section) > threshold:
                    nmv.skeleton.adjust_section_radii_to_threshold(section=i_section, threshold=threshold)
                    thick_sections.append(i_section)
                else:
                    thin_sections.append(i_section)

        thick_geometry = list()
        for i_section in thick_sections:
            nmv.skeleton.resample_section_adaptively(section=i_section)
            skinned_mesh = nmv.skeleton.skin_section_into_mesh(section=i_section, smoothing_level=2)
            thick_geometry.append(skinned_mesh)
            articulations = nmv.skeleton.draw_articulation_samples(section=i_section)
            thick_geometry.extend(articulations)

        thick_mesh = nmv.mesh.join_mesh_objects(mesh_list=thick_geometry, name='ThickSections')
        nmv.mesh.add_surface_noise_to_mesh_using_displacement_modifier(mesh_object=thick_mesh, noise_scale=1.5)

        thin_geometry = list()
        for i_section in thin_sections:
            nmv.skeleton.resample_section_adaptively(section=i_section)
            skinned_mesh = nmv.skeleton.skin_section_into_mesh(section=i_section, smoothing_level=2)
            thin_geometry.append(skinned_mesh)
            articulations = nmv.skeleton.draw_articulation_samples(section=i_section)
            thin_geometry.extend(articulations)

        thin_mesh = nmv.mesh.join_mesh_objects(mesh_list=thin_geometry, name='ThinSections')

        self.neuron_meshes.append(thick_mesh)
        self.neuron_meshes.append(thin_mesh)


    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):

        nmv.logger.header('Building Mesh: VoxelizationBuilder')

        # Initialization
        result, stats = self.PROFILE(self.initialize_builder)
        self.profiling_statistics += stats

        # Build the soma
        result, stats = self.PROFILE(self.reconstruct_soma_mesh)
        self.profiling_statistics += stats

        self.draw_sections()

        # Add the spines
        result, stats = self.PROFILE(self.add_spines_to_surface)
        self.profiling_statistics += stats

        self.neuron_mesh = nmv.mesh.join_mesh_objects(self.neuron_meshes)

        #result, stats = self.PROFILE(self.build_proxy_mesh)
        #self.profiling_statistics += stats

        # Voxelization modifier
        result, stats = self.PROFILE(self.apply_voxelization_modifier)
        self.profiling_statistics += stats

        # Surface roughness
        result, stats = self.PROFILE(self.add_surface_roughness)
        self.profiling_statistics += stats

        # Mesh cleaning
        result, stats = self.PROFILE(self.clean_mesh)
        self.profiling_statistics += stats

        # Mesh optimization
        result, stats = self.PROFILE(self.optimize_mesh)
        self.profiling_statistics += stats

        self.neuron_meshes = [self.neuron_mesh]

        # Adjust the origin of the mesh
        result, stats = self.PROFILE(self.finalize_mesh)
        self.profiling_statistics += stats

        # Report the statistics of this builder
        self.report_builder_statistics()

        # This builder creates a single mesh object
        return [self.neuron_mesh]
