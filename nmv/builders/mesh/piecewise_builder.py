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
import random, os, copy

# Blender imports
import bpy

# Internal modules
import nmv
import nmv.bbox
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.geometry
import nmv.mesh
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities
import nmv.rendering


####################################################################################################
# @PiecewiseBuilder
####################################################################################################
class PiecewiseBuilder:
    """Mesh builder that creates piecewise watertight meshes"""

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

        # A list of the colors/materials of the apical dendrites
        self.apical_dendrites_materials = None

        # A list of the colors/materials of the spines
        self.spines_materials = None

        # A reference to the reconstructed soma mesh
        self.soma_mesh = None

        # A list of the reconstructed meshes of the apical dendrites
        self.apical_dendrites_meshes = list()

        # A list of the reconstructed meshes of the basal dendrites
        self.basal_dendrites_meshes = list()

        # A list of the reconstructed meshes of the axon
        self.axon_meshes = list()

        # Statistics
        self.profiling_statistics = 'PiecewiseBuilder Profiles: \n'

        # Stats. about the morphology
        self.morphology_statistics = 'Morphology: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'PiecewiseBuilder Mesh: \n'

    ################################################################################################
    # @verify_morphology_skeleton
    ################################################################################################
    def verify_morphology_skeleton(self):
        """Verifies and repairs the morphology if the contain any artifacts that would potentially
        affect the reconstruction quality of the mesh.

        NOTE: The filters or operations performed in this builder are only specific to it. Other
        builders might apply a different set of filters.
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
    # @build_arbors
    ################################################################################################
    def build_arbors(self,
                     bevel_object,
                     caps,
                     roots_connection):
        """Builds the arbors of the neuron as tubes and AT THE END converts them into meshes.
        If you convert them during the building, the scene is getting crowded and the process is
        getting exponentially slower.

        :param bevel_object:
            A given bevel object to scale the section at the different samples.
        :param caps:
            A flag to indicate whether the drawn sections are closed or not.
        :param roots_connection:
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

        # Draw the apical dendrite if not ignored
        if not self.options.morphology.ignore_apical_dendrite:

            # Draw the apical dendrite, if exists
            if self.morphology.apical_dendrite is not None:

                # Draw the apical dendrite as a set connected sections
                nmv.logger.info('Apical dendrite')
                nmv.skeleton.ops.draw_connected_sections(
                    section=self.morphology.apical_dendrite,
                    max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                    name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                    material_list=self.apical_dendrites_materials,
                    bevel_object=bevel_object,
                    repair_morphology=True,
                    caps=caps,
                    sections_objects=self.apical_dendrites_meshes,
                    roots_connection=roots_connection)

                # Ensure that apical dendrite objects were reconstructed
                if len(self.apical_dendrites_meshes) > 0:

                    # Add a reference to the mesh object
                    self.morphology.apical_dendrite.mesh = self.apical_dendrites_meshes[0]

                    # Convert the section object (tubes) into meshes
                    for arbor_object in self.apical_dendrites_meshes:
                        nmv.scene.ops.convert_object_to_mesh(arbor_object)

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Ensure tha existence of basal dendrites
            if self.morphology.dendrites is not None:

                # Do it dendrite by dendrite
                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.info('Dendrite [%d]' % i)

                    basal_dendrite_objects = []

                    # Draw the basal dendrites as a set connected sections
                    basal_dendrite_prefix = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)
                    nmv.skeleton.ops.draw_connected_sections(
                        section=basal_dendrite,
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                        name=basal_dendrite_prefix,
                        material_list=self.basal_dendrites_materials,
                        bevel_object=bevel_object,
                        repair_morphology=True,
                        caps=caps,
                        sections_objects=basal_dendrite_objects,
                        roots_connection=roots_connection)

                    # Ensure that basal dendrite objects were reconstructed
                    if len(basal_dendrite_objects) > 0:

                        # Add a reference to the mesh object
                        self.morphology.dendrites[i].mesh = basal_dendrite_objects[0]

                        # Add the sections (tubes) of the basal dendrite to the list
                        self.basal_dendrites_meshes.extend(basal_dendrite_objects)

                        # Convert the section object (tubes) into meshes
                        for arbor_object in basal_dendrite_objects:
                            nmv.scene.ops.convert_object_to_mesh(arbor_object)

        # Draw the axon as a set connected sections
        if not self.options.morphology.ignore_axon:

            # Ensure tha existence of basal dendrites
            if self.morphology.axon is not None:
                nmv.logger.info('Axon')

                # Draw the axon as a set connected sections
                nmv.skeleton.ops.draw_connected_sections(
                    section=self.morphology.axon,
                    max_branching_level=self.options.morphology.axon_branch_order,
                    name=nmv.consts.Arbors.AXON_PREFIX,
                    material_list=self.axon_materials,
                    bevel_object=bevel_object,
                    repair_morphology=True,
                    caps=caps,
                    sections_objects=self.axon_meshes,
                    roots_connection=roots_connection)

                # Ensure that axon objects were reconstructed
                if len(self.axon_meshes) > 0:

                    # Add a reference to the mesh object
                    self.morphology.axon.mesh = self.axon_meshes[0]

                    # Convert the section object (tubes) into meshes
                    for arbor_object in self.axon_meshes:
                        nmv.scene.ops.convert_object_to_mesh(arbor_object)

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
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_SOMA
        else:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN

        # Create the arbors using this 16-side bevel object and CLOSED caps (no smoothing required)
        self.build_arbors(bevel_object=bevel_object, caps=True, roots_connection=roots_connection)

        # Close the caps of the apical dendrites meshes
        for arbor_object in self.apical_dendrites_meshes:
            nmv.mesh.close_open_faces(arbor_object)

        # Close the caps of the basal dendrites meshes
        for arbor_object in self.basal_dendrites_meshes:
            nmv.mesh.close_open_faces(arbor_object)

        # Close the caps of the axon meshes
        for arbor_object in self.axon_meshes:
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
        bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=4, name='arbors_bevel')

        # If the meshes of the arbors are 'welded' into the soma, then do NOT connect them to the
        #  soma origin, otherwise extend the arbors to the origin
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_SOMA
        else:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN

        # Create the arbors using this 4-side bevel object and OPEN caps (for smoothing)
        self.build_arbors(bevel_object=bevel_object, caps=False, roots_connection=roots_connection)

        # Smooth and close the faces of the apical dendrites meshes
        for mesh in self.apical_dendrites_meshes:
            nmv.mesh.ops.smooth_object_vertices(mesh_object=mesh, level=2)

        # Smooth and close the faces of the basal dendrites meshes
        for mesh in self.basal_dendrites_meshes:
            nmv.mesh.ops.smooth_object_vertices(mesh_object=mesh, level=2)

        # Smooth and close the faces of the axon meshes
        for mesh in self.axon_meshes:
            nmv.mesh.ops.smooth_object_vertices(mesh_object=mesh, level=2)

        # Delete the bevel object
        nmv.scene.ops.delete_object_in_scene(bevel_object)

    ################################################################################################
    # @reconstruct_arbors_meshes
    ################################################################################################
    def reconstruct_arbors_meshes(self):
        """Reconstruct the arbors.

        There are two techniques for reconstructing the mesh. The first uses sharp edges without
        any smoothing, and in this case, we will use a bevel object having 16 or 32 vertices.
        The other method creates a smoothed mesh with soft edges. In this method, we will use a
        simplified bevel object with only 'four' vertices and smooth it later using vertices
        smoothing to make 'sexy curves' for the mesh that reflect realistic arbors.
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

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):
        """Reconstructs the neuronal mesh as a set of piecewise-watertight meshes.

        The meshes are logically connected, but the different branches are intersecting,
        so they can be used perfectly for voxelization purposes, but they cannot be used for
        surface rendering with 'transparency'. For this purpose, we recommend to use the skinning
        builder.
        """

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        nmv.builders.create_skeleton_materials(builder=self)

        # Verify and repair the morphology, if required
        result, stats = nmv.utilities.profile_function(self.verify_morphology_skeleton)
        self.profiling_statistics += stats

        # Apply skeleton - based operation, if required, to slightly modify the skeleton
        result, stats = nmv.utilities.profile_function(
            nmv.builders.modify_morphology_skeleton, self)
        self.profiling_statistics += stats

        # Build the soma, with the default parameters
        result, stats = nmv.utilities.profile_function(nmv.builders.reconstruct_soma_mesh, self)
        self.profiling_statistics += stats

        # Build the arbors
        result, stats = nmv.utilities.profile_function(self.reconstruct_arbors_meshes)
        self.profiling_statistics += stats

        # Connect to the soma
        result, stats = nmv.utilities.profile_function(nmv.builders.connect_arbors_to_soma, self)
        self.profiling_statistics += stats

        # Tessellation
        result, stats = nmv.utilities.profile_function(nmv.builders.decimate_neuron_mesh, self)
        self.profiling_statistics += stats

        # Surface roughness
        result, stats = nmv.utilities.profile_function(
            nmv.builders.add_surface_noise_to_arbor, self)
        self.profiling_statistics += stats

        # Add the spines
        result, stats = nmv.utilities.profile_function(nmv.builders.add_spines_to_surface, self)
        self.profiling_statistics += stats

        # Join all the objects into a single object
        result, stats = nmv.utilities.profile_function(
            nmv.builders.join_mesh_object_into_single_object, self)
        self.profiling_statistics += stats

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
        nmv.builders.write_statistics_to_file(builder=self, tag='piecewise')
