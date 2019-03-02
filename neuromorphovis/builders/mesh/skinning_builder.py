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
import random, copy, sys

# Blender imports
import bpy

# Internal modules
import neuromorphovis as nmv
import neuromorphovis.builders
import neuromorphovis.bmeshi
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.geometry
import neuromorphovis.mesh
import neuromorphovis.shading
import neuromorphovis.skeleton
import neuromorphovis.scene
import neuromorphovis.utilities

import bmesh
from random import uniform
import mathutils


####################################################################################################
# @ExtrusionBuilder
####################################################################################################
class SkinningBuilder:
    """Mesh builder that creates accurate and nice meshes using skinning and extrusion"""

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
        self.morphology = morphology

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
        self.spines_colors = None

        # A reference to the reconstructed soma mesh
        self.reconstructed_soma_mesh = None

        # A reference to the reconstructed spines mesh
        self.spines_mesh = None

        # A parameter to track the current branching order on each arbor
        # NOTE: This parameter must get reset when you start working on a new arbor
        self.branching_order = 0

        # A list of all the meshes that are reconstructed on a piecewise basis and correspond to
        # the different components of the neuron including soma, arbors and the spines as well
        self.reconstructed_neuron_meshes = list()

    ################################################################################################
    # @update_section_samples_radii
    ################################################################################################
    @staticmethod
    def update_section_samples_radii(arbor_mesh,
                                     section):
        """Update the radii of the samples along a given section.

        :param arbor_mesh:
            The mesh of the arbor.
        :param section:
            A given section to update the radii of its samples.
        """

        # Make sure to include the first sample of the root section
        if section.is_root():
            starting_index = 0
        else:
            starting_index = 1

        # Sample by sample along the section
        for i in range(starting_index, len(section.samples)):

            # Get the sample radius
            radius = section.samples[i].radius

            # Get a reference to the vertex
            vertex = arbor_mesh.data.skin_vertices[0].data[section.samples[i].arbor_idx]

            # Update the radius of the vertex
            vertex.radius = radius, radius

    ################################################################################################
    # @update_arbor_samples_radii
    ################################################################################################
    def update_arbor_samples_radii(self,
                                   arbor_mesh,
                                   root,
                                   max_branching_order):
        """Updates the radii of the samples of the entire arbor to match reality from the
        temporary ones that were given before.

        :param arbor_mesh:
            The mesh of the arbor that will be updated.
        :param root:
            The root section of the arbor.
        :param max_branching_order:
            The maximum branching order set by the user to terminate the recursive call.
        """

        # Do not proceed if the branching order limit is hit
        if root.branching_order > max_branching_order:
            return

        # Set the radius of a given section
        self.update_section_samples_radii(arbor_mesh, root)

        # Update the radii of the samples of the children recursively
        for child in root.children:
            self.update_arbor_samples_radii(arbor_mesh, child, max_branching_order)

    ################################################################################################
    # @extrude_section
    ################################################################################################
    @staticmethod
    def extrude_section(arbor_bmesh_object,
                        section):
        """Extrudes the section along its samples starting from the first one to the last one.

        Note that the mesh to be extruded is already selected and there is no need to pass it.

        :param arbor_bmesh_object:
            The bmesh object of the given arbor.
        :param section:
            A given section to extrude a mesh around it.
        """

        # Extrude segment by segment
        for i in range(len(section.samples) - 1):

            nmv.bmeshi.ops.extrude_vertex_towards_point(
                arbor_bmesh_object, section.samples[i].arbor_idx, section.samples[i + 1].point)

    ################################################################################################
    # @create_root_point_mesh
    ################################################################################################
    def extrude_arbor(self,
                      arbor_bmesh_object,
                      root,
                      max_branching_order):
        """Extrude the given arbor section by section recursively.

        :param root:
            The root of a given section.
        :param max_branching_order:
            The maximum branching order set by the user to terminate the recursive call.
        """

        # Do not proceed if the branching order limit is hit
        if root.branching_order > max_branching_order:
            return

        # Extrude the section
        self.extrude_section(arbor_bmesh_object, root)

        # Extrude the children sections recursively
        for child in root.children:
            self.extrude_arbor(arbor_bmesh_object, child, max_branching_order)

    ################################################################################################
    # @create_arbor_mesh
    ################################################################################################
    def create_arbor_mesh(self,
                          arbor,
                          max_branching_order,
                          arbor_name):
        """Creates a mesh of the given arbor recursively.

        :param arbor:
            A given arbor.
        :param max_branching_order:
            The maximum branching order of the arbor.
        :param arbor_name:
            The name of the arbor.
        :return:
            A reference to the created mesh object.
        """

        # Initially, this index is set to ONE and incremented later, sample zero is reserved to
        # the auxiliary sample that is added at the soma
        samples_global_arbor_index = [1]
        nmv.builders.update_samples_indices_per_arbor(
            arbor, samples_global_arbor_index, max_branching_order)

        # Create the initial vertex of the arbor skeleton
        arbor_bmesh_object = nmv.bmeshi.create_vertex()

        # Extrude to the first sample along the arbor
        nmv.bmeshi.ops.extrude_vertex_towards_point(arbor_bmesh_object, 0, arbor.samples[0].point)

        # Extrude arbor mesh using the skinning method using a temporary radius with a bmesh
        self.extrude_arbor(arbor_bmesh_object, arbor, max_branching_order)

        # Convert the bmesh to a mesh object
        arbor_mesh = nmv.bmeshi.convert_bmesh_to_mesh(arbor_bmesh_object, arbor_name)

        # Apply a skin modifier create the membrane of the skeleton
        arbor_mesh.modifiers.new(name="Skin", type='SKIN')

        # Activate the arbor mesh
        nmv.scene.set_active_object(arbor_mesh)

        # Update the radii of the arbor using the fast method before applying the skinning modifier
        self.update_arbor_samples_radii(
            arbor_mesh=arbor_mesh, root=arbor, max_branching_order=max_branching_order)

        # Apply the modifier
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Skin")

        # Smooth the mesh object
        nmv.mesh.smooth_object(mesh_object=arbor_mesh, level=2)

        # Further smoothing, only with shading
        nmv.mesh.shade_smooth_object(arbor_mesh)

        # Return a reference to the arbor mesh
        return arbor_mesh

    ################################################################################################
    # @build_arbors
    ################################################################################################
    def build_arbors(self):
        """Builds the arbors of the neuron as tubes and AT THE END converts them into meshes.
        If you convert them during the building, the scene is getting crowded and the process is
        getting exponentially slower.

        :return:
            A list of all the individual meshes of the arbors.
        """

        # Header
        nmv.logger.header('Building Arbors')

        # Apply the morphology reformation filters if requested before creating the arbors

        # Taper the sections if requested
        if self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED or \
                self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED_ZIGZAG:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.taper_section])

        # Zigzag the sections if required
        if self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.ZIGZAG or \
                self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED_ZIGZAG:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.zigzag_section])

        # Create a list that keeps references to the meshes of all the connected pieces of the
        # arbors of the mesh.
        arbors_objects = []

        # Draw the apical dendrite, if exists
        if not self.options.morphology.ignore_apical_dendrite:
            nmv.logger.info('Apical dendrite')

            # Create the apical dendrite mesh
            if self.morphology.apical_dendrite is not None:
                arbor_mesh = self.create_arbor_mesh(
                    arbor=self.morphology.apical_dendrite,
                    max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                    arbor_name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX)

                # Apply the material to the reconstructed arbor
                nmv.shading.set_material_to_object(arbor_mesh,
                                                   self.apical_dendrite_materials[0])

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Do it dendrite by dendrite
            for i, basal_dendrite in enumerate(self.morphology.dendrites):
                # Create the basal dendrite meshes
                nmv.logger.info('Dendrite [%d]' % i)
                arbor_mesh = self.create_arbor_mesh(
                    arbor=basal_dendrite,
                    max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                    arbor_name='%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i))

                # Apply the material to the reconstructed arbor
                nmv.shading.set_material_to_object(arbor_mesh,
                                                   self.basal_dendrites_materials[0])

        # Draw the axon as a set connected sections
        if not self.options.morphology.ignore_axon:

            # Ensure tha existence of basal dendrites
            if self.morphology.axon is not None:
                nmv.logger.info('Axon')

                # Create the axon mesh
                arbor_mesh = self.create_arbor_mesh(
                    arbor=self.morphology.axon,
                    max_branching_order=self.options.morphology.axon_branch_order,
                    arbor_name=nmv.consts.Arbors.AXON_PREFIX)

                # Apply the material to the reconstructed arbor
                nmv.shading.set_material_to_object(arbor_mesh,
                                                   self.axon_materials[0])

        # Return the list of meshes
        return arbors_objects

    ################################################################################################
    # @connect_arbors_to_soma
    ################################################################################################
    def connect_arbors_to_soma(self):
        """Connects the root section of a given arbor to the soma at its initial segment.

        This function checks if the arbor mesh is 'logically' connected to the soma or not,
        following to the initial validation steps that determines if the arbor has a valid
        connection point to the soma or not.
        If the arbor is 'logically' connected to the soma, this function returns immediately.
        The arbor is a Section object, see Section() @ section.py.
        """

        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            nmv.logger.header('Connecting arbors to soma')

            # Connecting apical dendrite
            if not self.options.morphology.ignore_apical_dendrite:

                # There is an apical dendrite
                if self.morphology.apical_dendrite is not None:
                    nmv.logger.detail('Apical dendrite')
                    nmv.skeleton.ops.connect_arbor_to_soma(
                        self.reconstructed_soma_mesh, self.morphology.apical_dendrite)

            # Connecting basal dendrites
            if not self.options.morphology.ignore_basal_dendrites:

                # Do it dendrite by dendrite
                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.detail('Dendrite [%d]' % i)
                    nmv.skeleton.ops.connect_arbor_to_soma(
                        self.reconstructed_soma_mesh, basal_dendrite)

            # Connecting axon
            if not self.options.morphology.ignore_axon:
                nmv.logger.detail('Axon')
                nmv.skeleton.ops.connect_arbor_to_soma(
                    self.reconstructed_soma_mesh, self.morphology.axon)

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
        self.reconstructed_soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

        # Apply the shader to the reconstructed soma mesh
        nmv.shading.set_material_to_object(self.reconstructed_soma_mesh, self.soma_materials[0])

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):
        """Reconstructs the neuronal mesh as a set of piecewise-watertight meshes.
        The meshes are logically connected, but the different branches are intersecting,
        so they can be used perfectly for voxelization purposes, but they cannot be used for
        surface rendering with 'transparency'.
        """

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        nmv.builders.create_skeleton_materials(builder=self)

        # Build the soma
        self.reconstruct_soma_mesh()

        # Build the arbors
        # self.reconstruct_arbors_meshes()
        self.build_arbors()

        nmv.logger.header('Done!')

        return self.reconstructed_neuron_meshes