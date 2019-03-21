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
import copy, math

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
        self.morphology = morphology

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

    def build_arbor(self,
                    arbor,
                    caps,
                    bevel_object,
                    max_branching_order,
                    name,
                    material):

        #arbor_poly_line_objects = nmv.skeleton.ops.draw_connected_sections_poly_lines(
        #    arbor=arbor, max_branching_level=max_branching_order, bevel_object=bevel_object,
        #    caps=caps)

        # A list that will contain all the poly-lines gathered from traversing the arbor tree with
        # depth-first traversal
        arbor_poly_lines_data = list()

        # Construct the poly-lines
        nmv.skeleton.ops.get_connected_sections_poly_line_recursively(
            section=arbor, poly_lines_data=arbor_poly_lines_data,
            max_branching_level=max_branching_order)

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


    ################################################################################################
    # @build_arbors
    ################################################################################################
    def build_arbors(self,
                     bevel_object,
                     caps,
                     roots_connection=False):
        """
        Builds the arbors of the neuron as tubes and AT THE END converts them into meshes.
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
        """

        # Axon
        if self.morphology.axon is not None:
            if not self.options.morphology.ignore_axon:
                nmv.logger.log('\t * Axon')

                self.build_arbor(
                    arbor=self.morphology.axon, caps=caps, bevel_object=bevel_object,
                    max_branching_order=self.options.morphology.axon_branch_order,
                    name=nmv.consts.Arbors.AXON_PREFIX, material=self.axon_materials[0])

        # Draw the apical dendrite, if exists
        if self.morphology.apical_dendrite is not None:
            if not self.options.morphology.ignore_apical_dendrite:
                nmv.logger.log('\t * Apical dendrite')

                self.build_arbor(
                    arbor=self.morphology.apical_dendrite, caps=caps, bevel_object=bevel_object,
                    max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                    name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                    material=self.apical_dendrites_materials[0])

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
                        material=self.basal_dendrites_materials[0])

    ################################################################################################
    # @connect_arbors_to_soma
    ################################################################################################
    def connect_arbors_to_soma(self):
        """
        Connects the root section of a given arbor to the soma at its initial segment.
        This function checks if the arbor mesh is 'logically' connected to the soma or not,
        following to the initial validation steps that determines if the arbor has a valid
        connection point to the soma or not.
        If the arbor is 'logically' connected to the soma, this function returns immediately.
        The arbor is a Section object, see Section() @ section.py.

        :return:
        """

        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:

            # Connecting apical dendrite
            if not self.options.morphology.ignore_apical_dendrite:

                # There is an apical dendrite
                if self.morphology.apical_dendrite is not None:
                    nmv.logger.log('\t * Apical dendrite')
                    nmv.skeleton.ops.connect_arbor_to_soma(
                        self.soma_mesh, self.morphology.apical_dendrite)

            # Connecting basal dendrites
            if not self.options.morphology.ignore_basal_dendrites:

                if self.morphology.dendrites is not None:

                    # Do it dendrite by dendrite
                    for i, basal_dendrite in enumerate(self.morphology.dendrites):
                        nmv.logger.log('\t * Dendrite [%d]' % i)
                        nmv.skeleton.ops.connect_arbor_to_soma(self.soma_mesh, basal_dendrite)

            # Connecting axon
            if not self.options.morphology.ignore_axon:
                nmv.logger.log('\t * Axon')
                nmv.skeleton.ops.connect_arbor_to_soma(self.soma_mesh, self.morphology.axon)

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
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_SOMA
        else:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN

        # Create the arbors using this 16-side bevel object and CLOSED caps (no smoothing required)
        self.build_arbors(bevel_object=bevel_object, caps=True, roots_connection=roots_connection)

        # Delete the bevel object
        nmv.scene.ops.delete_object_in_scene(bevel_object)

        # Smooth and close the faces of the apical dendrites meshes
        #for mesh in arbors_meshes:

        #    # Close the edges
        #    nmv.mesh.ops.close_open_faces(mesh)

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
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_SOMA
        else:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN

        # Create the arbors using this 4-side bevel object and OPEN caps (for smoothing)
        self.build_arbors(bevel_object=bevel_object, caps=True)

        # Delete the bevel object
        nmv.scene.ops.delete_object_in_scene(bevel_object)

        # Smooth and close the faces of the apical dendrites meshes
        #for mesh in arbors_meshes:

            # Smooth
            #nmv.mesh.ops.smooth_object(mesh_object=mesh, level=2)

            # Close the edges
            #nmv.mesh.ops.close_open_faces(mesh)

    ################################################################################################
    # @reconstruct_arbors_meshes
    ################################################################################################
    def reconstruct_arbors_meshes(self):
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
    # @reconstruct_soma_mesh
    ################################################################################################
    def reconstruct_soma_mesh(self):
        """Reconstruct the mesh of the soma.

        NOTE: To improve the performance of the soft body physics simulation, reconstruct the
        soma profile before the arbors, such that the scene is almost empty.

        NOTE: If the soma is requested to be connected to the initial segments of the arbors,
        we must use a high number of subdivisions to make smooth connections that look nice,
        but if the arbors are connected to the soma origin, then we can use less subdivisions
        since the soma will not be connected to the arbor at all.
        """

        # If the soma is connected to the root arbors
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            soma_builder_object = nmv.builders.SomaBuilder(
                morphology=self.morphology, options=self.options)

        # Otherwise, ignore
        else:
            soma_builder_object = nmv.builders.SomaBuilder(
                morphology=self.morphology,
                options=self.options)

        # Reconstruct the soma mesh
        self.soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

        # Apply the shader to the reconstructed soma mesh
        nmv.shading.set_material_to_object(self.soma_mesh, self.soma_materials[0])

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
        self.verify_morphology_skeleton()

        # Apply skeleton-based operation, if required, to slightly modify the morphology skeleton
        nmv.builders.common.modify_morphology_skeleton(builder=self)

        # Build the soma
        # self.reconstruct_soma_mesh()

        # Build the arbors
        self.reconstruct_arbors_meshes()

        # Connect the arbors to the soma
        # self.connect_arbors_to_soma()

        # Modifying mesh surface
        # self.modify_mesh_surface()

        # Decimation
        # self.decimate_neuron_mesh()

        # Adding spines
        # self.add_spines()

        # Report
        nmv.logger.header('Mesh Reconstruction Done!')

