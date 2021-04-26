####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
import time

# Blender imports
import bpy

# Internal modules
import nmv.builders
import nmv.bmeshi
import nmv.consts
import nmv.enums
import nmv.geometry
import nmv.mesh
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities


####################################################################################################
# @ExtrusionBuilder
####################################################################################################
class SkinningBuilder:
    """Mesh builder that creates accurate and nice meshes using skinning. The reconstructed meshes
    are not guaranteed to be watertight, but they look very nice if you need to use transparency."""

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
        self.axons_materials = None

        # A list of the colors/materials of the basal dendrites
        self.basal_dendrites_materials = None

        # A list of the colors/materials of the apical dendrite
        self.apical_dendrites_materials = None

        # A list of the colors/materials of the spines
        self.spines_materials = None

        # A reference to the reconstructed soma mesh
        self.soma_mesh = None

        # A reference to the reconstructed spines mesh
        self.spines_mesh = None

        # A list of all the meshes created by the builder
        self.neuron_meshes = list()

        # Statistics
        self.profiling_statistics = 'SkinningBuilder Mesh Stats.: \n'

        # Stats. about the morphology
        self.morphology_statistics = 'Morphology: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'SkinningBuilder Mesh: \n'

        # Total extrusion time
        self.extrusion_time = 0

        # Total subdivision time
        self.subdivision_time = 0

        # Total time to apply the skin modifier
        self.skin_modifier_time = 0

        # Total time to update the radii
        self.update_radii_time = 0

        # Conversion from bmesh to mesh time
        self.mesh_conversion_time = 0

        # Smooth shade the surface
        self.smooth_shading_time = 0

        # Modifier creation time
        self.creating_modifier_time = 0

        # Reindexing time
        self.reindexing_time = 0

        # Verify the connectivity of the arbors to the soma
        nmv.skeleton.verify_arbors_connectivity_to_soma(morphology=self.morphology)

    ################################################################################################
    # @update_morphology_skeleton
    ################################################################################################
    def update_morphology_skeleton(self):
        """Verifies and repairs the morphology if the contain any artifacts that would potentially
        affect the reconstruction quality of the mesh.

        NOTE: The filters or operations performed in this builder are only specific to it. Other
        builders might apply a different set of filters.
        """

        # Verify and repair the morphology, if required
        nmv.builders.mesh.update_morphology_skeleton(builder=self)

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

        :param arbor_bmesh_object:
            The bmesh object of the arbor.
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
                          arbor_name,
                          arbor_material,
                          connected_to_soma=False):
        """Creates a mesh of the given arbor recursively.

        :param arbor:
            A given arbor.
        :param max_branching_order:
            The maximum branching order of the arbor.
        :param arbor_name:
            The name of the arbor.
        :param arbor_material:
            The material or the arbor.
        :param connected_to_soma:
            If the arbor is connected to soma or not, by default False.
        :return:
            A reference to the created mesh object.
        """

        # If the arbor is connected to soma, then start at the initial segment of the arbor
        if connected_to_soma:

            # Initially, this index is set to TWO and incremented later, sample zero is reserved to
            # the auxiliary sample that is added at the soma, and the first sample to the point that
            # is added right before the arbor starts
            samples_global_arbor_index = [1]
            nmv.builders.update_samples_indices_per_arbor(
                arbor, samples_global_arbor_index, max_branching_order)

            # Add an auxiliary sample just before the arbor starts
            auxiliary_point = arbor.samples[0].point - 0.01 * arbor.samples[0].point.normalized()

            # Create the initial vertex of the arbor skeleton at the auxiliary point
            arbor_bmesh_object = nmv.bmeshi.create_vertex(location=auxiliary_point)

            # Extrude towards the first sample from the auxiliary point
            nmv.bmeshi.ops.extrude_vertex_towards_point(
                arbor_bmesh_object, 0, arbor.samples[0].point)

        # Otherwise, add a little auxiliary sample and start from it
        else:

            # Initially, this index is set to TWO and incremented later, sample zero is reserved to
            # the auxiliary sample that is added at the soma, and the first sample to the point that
            # is added right before the arbor starts
            reindexing_time = time.time()
            samples_global_arbor_index = [2]
            nmv.builders.update_samples_indices_per_arbor(
                arbor, samples_global_arbor_index, max_branching_order)
            self.reindexing_time += time.time() - reindexing_time

            # If the arbor is not far from soma, then connect it to the origin
            if not arbor.far_from_soma:
                arbor_bmesh_object = nmv.bmeshi.create_vertex()

                # Add an auxiliary sample just before the arbor starts
                auxiliary_point = arbor.samples[0].point - 0.01 * arbor.samples[
                    0].point.normalized()

            else:
                arbor_bmesh_object = nmv.bmeshi.create_vertex(location=arbor.samples[0].point)

                # Add an auxiliary sample just after the arbor starts
                auxiliary_point = arbor.samples[0].point + 0.01 * arbor.samples[
                    0].point.normalized()

            # Extrude to the auxiliary sample
            nmv.bmeshi.ops.extrude_vertex_towards_point(arbor_bmesh_object, 0, auxiliary_point)

            # Extrude towards the first sample
            nmv.bmeshi.ops.extrude_vertex_towards_point(
                arbor_bmesh_object, 1, arbor.samples[0].point)

        # Extrude arbor mesh using the skinning method using a temporary radius with a bmesh
        extrusion_time = time.time()
        self.extrude_arbor(arbor_bmesh_object, arbor, max_branching_order)
        self.extrusion_time += time.time() - extrusion_time

        # Convert the bmesh to a mesh object
        mesh_conversion_time = time.time()
        arbor_mesh = nmv.bmeshi.convert_bmesh_to_mesh(arbor_bmesh_object, arbor_name)
        self.mesh_conversion_time += time.time() - mesh_conversion_time

        # Apply a skin modifier create the membrane of the skeleton
        creating_modifier_time = time.time()
        arbor_mesh.modifiers.new(name="Skin", type='SKIN')
        self.creating_modifier_time += time.time() - creating_modifier_time

        # Activate the arbor mesh
        nmv.scene.set_active_object(arbor_mesh)

        # Get a reference to the vertex
        vertex = arbor_mesh.data.skin_vertices[0].data[0]

        # Update the radius of the vertex
        vertex.radius = arbor.samples[0].radius, arbor.samples[0].radius

        # Get a reference to the vertex
        vertex = arbor_mesh.data.skin_vertices[0].data[1]

        # Update the radius of the vertex
        vertex.radius = arbor.samples[0].radius, arbor.samples[0].radius

        # Update the radii of the arbor using the fast method before applying the skinning modifier
        update_radii_time = time.time()
        self.update_arbor_samples_radii(
            arbor_mesh=arbor_mesh, root=arbor, max_branching_order=max_branching_order)
        self.update_radii_time += time.time() - update_radii_time

        # Apply the modifier
        skin_modifier_time = time.time()

        if nmv.utilities.is_blender_290():
            bpy.ops.object.modifier_apply(modifier="Skin")
        else:
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Skin")
        self.skin_modifier_time += time.time() - skin_modifier_time

        # Assign the material to the reconstructed arbor mesh
        nmv.shading.set_material_to_object(arbor_mesh, arbor_material)

        # Remove the first face, before the smoothing operation if connected to the soma
        if connected_to_soma:

            # Remove the first face
            nmv.mesh.ops.remove_first_face_of_quad_mesh_object(arbor_mesh)

            # Smooth the mesh object
            subdivision_time = time.time()
            nmv.mesh.smooth_object(mesh_object=arbor_mesh, level=2)
            self.subdivision_time += time.time() - subdivision_time

            # Close the removed face
            nmv.mesh.ops.close_open_faces(mesh_object=arbor_mesh)

        # Otherwise, apply directly the smoothing operation
        else:

            # Smooth the mesh object
            subdivision_time = time.time()
            nmv.mesh.smooth_object(mesh_object=arbor_mesh, level=2)
            self.subdivision_time += time.time() - subdivision_time

        # Further smoothing, only with shading
        smooth_shading_time = time.time()
        nmv.mesh.shade_smooth_object(arbor_mesh)
        self.smooth_shading_time += time.time() - smooth_shading_time

        # Update the UV mapping
        nmv.shading.adjust_material_uv(arbor_mesh)

        # Return a reference to the arbor mesh
        return arbor_mesh

    ################################################################################################
    # @build_arbors
    ################################################################################################
    def build_arbors(self,
                     connected_to_soma=False):
        """Builds the arbors of the neuron as tubes and AT THE END converts them into meshes.
        If you convert them during the building, the scene is getting crowded and the process is
        getting exponentially slower.

        :param connected_to_soma:
            If the arbor is connected to soma or not, by default False.
        """

        # Header
        nmv.logger.info('Building arbors')

        # Apical dendrites
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for i, arbor in enumerate(self.morphology.apical_dendrites):

                    # Create the mesh
                    nmv.logger.detail(arbor.label)
                    arbor_mesh = self.create_arbor_mesh(
                        arbor=arbor,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        arbor_name=arbor.label,
                        arbor_material=self.apical_dendrites_materials[0],
                        connected_to_soma=connected_to_soma)

                    # Add a reference to the mesh object
                    self.morphology.apical_dendrites[i].mesh = arbor_mesh
                    self.neuron_meshes.append(arbor_mesh)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for i, arbor in enumerate(self.morphology.basal_dendrites):

                    # Create the mesh
                    nmv.logger.detail(arbor.label)
                    arbor_mesh = self.create_arbor_mesh(
                        arbor=arbor,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        arbor_name=arbor.label,
                        arbor_material=self.basal_dendrites_materials[0],
                        connected_to_soma=connected_to_soma)

                    # Add a reference to the mesh object
                    self.morphology.basal_dendrites[i].mesh = arbor_mesh
                    self.neuron_meshes.append(arbor_mesh)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for i, arbor in enumerate(self.morphology.axons):

                    # Create the axon mesh
                    nmv.logger.detail(arbor.label)
                    arbor_mesh = self.create_arbor_mesh(
                        arbor=arbor,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        arbor_name=arbor.label,
                        arbor_material=self.axons_materials[0],
                        connected_to_soma=connected_to_soma)

                    # Add a reference to the mesh object
                    self.morphology.axons[i].mesh = arbor_mesh
                    self.neuron_meshes.append(arbor_mesh)

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):
        """Reconstructs the neuronal mesh using the skinning modifiers in Blender.
        """

        nmv.logger.header('Building Mesh: SkinningBuilder')

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        nmv.builders.create_skeleton_materials(builder=self)

        # Verify and repair the morphology, if required
        result, stats = nmv.utilities.profile_function(
            nmv.builders.mesh.update_morphology_skeleton, self)
        self.profiling_statistics += stats

        # Verify the connectivity of the arbors to the soma to filter the disconnected arbors,
        # for example, an axon that is emanating from a dendrite or two intersecting dendrites
        nmv.skeleton.ops.verify_arbors_connectivity_to_soma(self.morphology)

        # Build the soma, with the default parameters
        result, stats = nmv.utilities.profile_function(nmv.builders.reconstruct_soma_mesh, self)
        self.profiling_statistics += stats

        # Build the arbors and connect them to the soma
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:

            # Build the arbors
            result, stats = nmv.utilities.profile_function(self.build_arbors, True)
            self.profiling_statistics += stats

            # Connect to the soma
            result, stats = nmv.utilities.profile_function(
                nmv.builders.connect_arbors_to_soma, self)
            self.profiling_statistics += stats

        # Build the arbors only without any connection to the soma
        else:
            # Build the arbors
            result, stats = nmv.utilities.profile_function(self.build_arbors, False)
            self.profiling_statistics += stats

        # Details about the arbors building
        self.profiling_statistics += '\t* Stats. @%s: [%.3f]\n' % ('extrusion',
                                                                   self.extrusion_time)
        # Details about the arbors building
        self.profiling_statistics += '\t* Stats. @%s: [%.3f]\n' % ('subdivision',
                                                                   self.subdivision_time)

        # Details about the arbors building
        self.profiling_statistics += '\t* Stats. @%s: [%.3f]\n' % ('skin_modifier',
                                                                   self.skin_modifier_time)

        # Details about the arbors building
        self.profiling_statistics += '\t* Stats. @%s: [%.3f]\n' % ('update_radii',
                                                                   self.update_radii_time)

        # Details about the arbors building
        self.profiling_statistics += '\t* Stats. @%s: [%.3f]\n' % ('mesh_conversion',
                                                                   self.mesh_conversion_time)

        # Details about the arbors building
        self.profiling_statistics += '\t* Stats. @%s: [%.3f]\n' % ('reindexing',
                                                                   self.reindexing_time)

        # Details about the arbors building
        self.profiling_statistics += '\t* Stats. @%s: [%.3f]\n' % ('smooth_shading',
                                                                   self.smooth_shading_time)

        # Details about the arbors building
        self.profiling_statistics += '\t* Stats. @%s: [%.3f]\n' % ('creating_modifier',
                                                                   self.creating_modifier_time)

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
        neuron_mesh, stats = nmv.utilities.profile_function(
            nmv.builders.join_mesh_object_into_single_object, self)
        self.profiling_statistics += stats

        # Transform to the global coordinates, if required
        result, stats = nmv.utilities.profile_function(
            nmv.builders.transform_to_global_coordinates, self)
        self.profiling_statistics += stats

        # Collect the stats. of the mesh
        result, stats = nmv.utilities.profile_function(nmv.builders.collect_mesh_stats, self)
        self.profiling_statistics += stats

        # Done
        nmv.logger.statistics(self.profiling_statistics)

        # Write the stats to file
        nmv.builders.write_statistics_to_file(builder=self, tag='skinning')

        # Return a reference to the neuron mesh if joint
        return neuron_mesh
