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
import math
import os

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.mesh
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities


####################################################################################################
# @UnionBuilder
####################################################################################################
class UnionBuilder:
    """Mesh builder that creates watertight meshes using Blender union operators"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology skeleton to reconstruct its mesh.
        :param options:
            Loaded options from NeuroMorphoVis.
        """

        # Morphology
        self.morphology = copy.deepcopy(morphology)

        # Loaded options from NeuroMorphoVis
        self.options = options

        # A list of the materials of the soma
        self.soma_materials = None

        # A list of the materials of the axon
        self.axon_materials = None

        # A list of the materials of the basal dendrites
        self.basal_dendrites_materials = None

        # A list of the materials of the apical dendrite
        self.apical_dendrites_materials = None

        # A reference to the reconstructed soma mesh
        self.soma_mesh = None

        # Statistics
        self.profiling_statistics = 'UnionBuilder Profiles: \n'

        # Stats. about the morphology
        self.morphology_statistics = 'Morphology: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'UnionBuilder Mesh: \n'

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

        # Label the primary and secondary sections based on angles, and if does not work use
        # the radii as a fallback
        try:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_angles])
        except ValueError:
            nmv.logger.info('Labeling branches based on radii as a fallback')
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_radii])

    ################################################################################################
    # @build_arbor
    ################################################################################################
    @staticmethod
    def build_arbor(arbor,
                    caps,
                    bevel_object,
                    max_branching_order,
                    name,
                    material,
                    connection_to_soma,
                    soft):
        """Builds the arbor.

        :param arbor:
            The root section of the neurite.
        :param caps:
            Caps flag, True or False.
        :param bevel_object:
            A bevel object used to shape the arbor.
        :param max_branching_order:
            Maximum branching order.
        :param name:
            Arbor name.
        :param material:
            The material that will be applied to the arbor mesh.
        :param connection_to_soma:
            A flag to check if the arbor is connected to the soma or not.
        :param soft:
            A flag to indicate that it is a soft arbor.
        """

        # A list that will contain all the poly-lines gathered from traversing the arbor tree with
        # depth-first traversal
        arbor_poly_lines_data = list()

        # Construct the poly-lines
        nmv.skeleton.ops.get_connected_sections_poly_line_recursively(
            section=arbor, poly_lines_data=arbor_poly_lines_data,
            max_branching_level=max_branching_order)

        # If the arbor not connected to the soma, then add a point at the origin
        if not connection_to_soma:

            # Add an auxiliary point at the origin
            arbor_poly_lines_data[0][0].insert(0, [(0, 0, 0, 1), arbor.samples[0].radius])

        # A list that will contain all the drawn poly-lines to be able to access them later,
        # although we can access them by name
        arbor_poly_line_objects = list()

        # For each poly-line in the list, draw it
        for i, poly_line_data in enumerate(arbor_poly_lines_data):

            # Draw the section, and append the result to the objects list
            arbor_poly_line_objects.append(nmv.skeleton.ops.draw_section_from_poly_line_data(
                data=poly_line_data[0], name=poly_line_data[1], bevel_object=bevel_object,
                caps=False if i == 0 else caps))

        # Convert the section object (poly-lines or tubes) into meshes
        for arbor_poly_line_object in arbor_poly_line_objects:
            nmv.scene.ops.convert_object_to_mesh(arbor_poly_line_object)

        # Union all the mesh objects into a single object
        arbor.mesh = nmv.mesh.ops.union_mesh_objects_in_list(arbor_poly_line_objects)

        # Rename the mesh
        arbor.mesh.name = name

        # Assign the material to the reconstructed arbor mesh
        nmv.shading.set_material_to_object(arbor.mesh, material)

        # Update the UV mapping
        nmv.shading.adjust_material_uv(arbor.mesh)

        # Close the edges only if not connected to soma

        # If soft arbors are required, smooth the mesh before closing the faces
        if soft:
            nmv.mesh.ops.smooth_object(mesh_object=arbor.mesh, level=2)

        # Close the caps
        nmv.mesh.ops.close_open_faces(arbor.mesh)

    ################################################################################################
    # @build_union_arbors
    ################################################################################################
    def build_union_arbors(self,
                           bevel_object,
                           caps,
                           connection_to_soma,
                           soft):
        """
        Builds the arbors of the neuron as tubes and AT THE END converts them into meshes.
        If you convert them during the building, the scene is getting crowded and the process is
        getting exponentially slower.

        :param bevel_object:
            A given bevel object to scale the section at the different samples.
        :param caps:
            A flag to indicate whether the drawn sections are closed or not.
        :param connection_to_soma:
            A flag to connect (for soma disconnected more) or disconnect (for soma bridging mode)
            the arbor to the soma origin.
            If this flag is set to True, this means that the arbor will be extended to the soma
            origin and the branch will not be physically connected to the soma as a single mesh.
            If the flag is set to False, the arbor will only have a bridging connection that
            would allow us later to connect it to the nearest face on the soma create a
            watertight mesh.
        """

        # Axon
        if self.morphology.axon is not None:
            if not self.options.morphology.ignore_axon:
                nmv.logger.log('\t * Axon')

                self.build_arbor(
                    arbor=self.morphology.axon, caps=caps, bevel_object=bevel_object,
                    max_branching_order=self.options.morphology.axon_branch_order,
                    name=nmv.consts.Arbors.AXON_PREFIX, material=self.axon_materials[0],
                    connection_to_soma=connection_to_soma, soft=soft)

        # Draw the apical dendrite, if exists
        if self.morphology.apical_dendrite is not None:
            if not self.options.morphology.ignore_apical_dendrite:
                nmv.logger.log('\t * Apical dendrite')

                self.build_arbor(
                    arbor=self.morphology.apical_dendrite, caps=caps, bevel_object=bevel_object,
                    max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                    name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                    material=self.apical_dendrites_materials[0],
                    connection_to_soma=connection_to_soma, soft=soft)

        # Draw the basal dendrites
        if self.morphology.dendrites is not None:
            if not self.options.morphology.ignore_basal_dendrites:

                # Do it dendrite by dendrite
                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.log('\t * Dendrite [%d]' % i)

                    # Draw the basal dendrites as a set connected sections
                    basal_dendrite_prefix = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)

                    self.build_arbor(
                        arbor=basal_dendrite, caps=caps, bevel_object=bevel_object,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        name=basal_dendrite_prefix,
                        material=self.basal_dendrites_materials[0],
                        connection_to_soma=connection_to_soma, soft=soft)

    ################################################################################################
    # @build_hard_edges_arbors
    ################################################################################################
    def build_hard_edges_arbors(self):
        """Reconstruct the meshes of the arbors of the neuron with HARD edges.
        """

        # Create a bevel object that will be used to create the mesh
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, vertices=16, name='hard_edges_arbors_bevel')

        # If the meshes of the arbors are 'welded' into the soma, then do NOT connect them to the
        #  soma origin, otherwise extend the arbors to the origin
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            connection_to_soma = True
        else:
            connection_to_soma = False

        # Create the arbors using this 16-side bevel object and CLOSED caps (no smoothing required)
        self.build_union_arbors(bevel_object=bevel_object, caps=True,
                                connection_to_soma=connection_to_soma, soft=False)

        # Delete the bevel object
        nmv.scene.ops.delete_object_in_scene(bevel_object)

    ################################################################################################
    # @build_soft_edges_arbors
    ################################################################################################
    def build_soft_edges_arbors(self):
        """Reconstruct the meshes of the arbors of the neuron with SOFT edges.
        """
        # Create a bevel object that will be used to create the mesh with 4 sides only
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0 * math.sqrt(2), vertices=4, name='soft_edges_arbors_bevel')

        # If the meshes of the arbors are 'welded' into the soma, then do NOT connect them to the
        #  soma origin, otherwise extend the arbors to the origin
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            connection_to_soma = True
        else:
            connection_to_soma = False

        # Create the arbors using this 4-side bevel object and OPEN caps (for smoothing)
        self.build_union_arbors(bevel_object=bevel_object, caps=True,
                                connection_to_soma=connection_to_soma, soft=True)

        # Delete the bevel object
        nmv.scene.ops.delete_object_in_scene(bevel_object)

    ################################################################################################
    # @reconstruct_arbors_meshes
    ################################################################################################
    def build_arbors(self):
        """Reconstruct the arbors.

        # There are two techniques for reconstructing the mesh. The first uses sharp edges without
        # any smoothing, and in this case, we will use a bevel object having 16 or 32 vertices.
        # The other method creates a smoothed mesh with soft edges. In this method, we will use a
        # simplified bevel object with only 'four' vertices and smooth it later using vertices
        # smoothing to make 'sexy curves' for the mesh that reflect realistic arbors.
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
        """Reconstructs the mesh.
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
        result, stats = nmv.utilities.profile_function(self.build_arbors)
        self.profiling_statistics += stats

        # Connect to the soma
        result, stats = nmv.utilities.profile_function(nmv.builders.connect_arbors_to_soma, self)
        self.profiling_statistics += stats

        # Tessellation
        result, stats = nmv.utilities.profile_function(nmv.builders.decimate_neuron_mesh, self)
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
        nmv.builders.write_statistics_to_file(builder=self, tag='union')

