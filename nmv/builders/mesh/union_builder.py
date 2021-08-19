####################################################################################################
# Copyright (c) 2016 - 2021, EPFL / Blue Brain Project
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
import bpy

# Internal imports
from .base import MeshBuilderBase
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.mesh
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities
import nmv.geometry


####################################################################################################
# @UnionBuilder
####################################################################################################
class UnionBuilder(MeshBuilderBase):
    """This mesh builder creates low-tessellated meshes using the union operators."""

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

        # Initialize the parent with the common parameters
        MeshBuilderBase.__init__(self, morphology, options)

        # A reference to the reconstructed soma mesh, and potentially the neuron mesh after welding
        self.soma_mesh = None

        # Statistics
        self.profiling_statistics = 'UnionBuilder Profiling Stats.: \n'

        # Stats. about the morphology
        self.morphology_statistics = 'Morphology: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'UnionBuilder Mesh: \n'

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
                *[self.morphology, nmv.skeleton.ops.resample_section_at_fixed_step])
        else:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.resample_section_adaptively_relaxed])

        # Verify the connectivity of the arbors to the soma to filter the disconnected arbors,
        # for example, an axon that is emanating from a dendrite or two intersecting dendrites
        nmv.skeleton.ops.verify_arbors_connectivity_to_soma(self.morphology)

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
    def clean_union_operator_reconstructed_surface(mesh_object):

        # Subdivide mesh with level 1
        nmv.mesh.subdivide_mesh(mesh_object=mesh_object, level=1)

        # Remove doubles
        nmv.mesh.remove_doubles(mesh_object=mesh_object, distance=0.01)

        # Add light surface noise
        nmv.mesh.add_light_surface_noise(mesh_object=mesh_object)

        # Decimate the mesh
        nmv.mesh.decimate_mesh_object(mesh_object=mesh_object, decimation_ratio=0.2)

        # Remove doubles
        nmv.mesh.remove_doubles(mesh_object=mesh_object, distance=0.01)

        # Smooth the surface vertices
        nmv.mesh.smooth_object_vertices(mesh_object=mesh_object, level=5)

    ################################################################################################
    # @build_arbor
    ################################################################################################
    def build_arbor(self,
                    arbor,
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
        arbor_poly_lines = list()

        # Construct the poly-lines
        nmv.skeleton.ops.get_connected_sections_poly_lines_recursively(
            section=arbor, poly_lines=arbor_poly_lines, max_branching_order=max_branching_order)

        # If the arbor not connected to the soma, then add a point at the origin, only if the arbor
        # is actually connected to the soma
        if not connection_to_soma and not arbor.far_from_soma:

            # Add an auxiliary point at the origin to the first poly-line in the list
            arbor_poly_lines[0].samples.insert(0, [(0, 0, 0, 1), arbor.samples[0].radius])

        # A list that will contain all the drawn poly-lines to be able to access them later,
        # although we can access them by name
        arbor_poly_line_objects = list()

        # Indicate the curve style
        curve_style = 'POLY'
        if soft:
            curve_style = 'NURBS'

        # For each poly-line in the list, draw it
        for i, poly_line in enumerate(arbor_poly_lines):

            # Resample the poly-line adaptively to preserve the geometry
            nmv.geometry.resample_poly_line_adaptively_relaxed(poly_line=poly_line)

            # Draw the section, and append the result to the objects list
            arbor_poly_line_objects.append(nmv.skeleton.ops.draw_section_from_poly_line_data(
                data=poly_line.samples, name=poly_line.name, bevel_object=bevel_object,
                caps=False if i == 0 else caps, curve_style=curve_style))

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
        """Builds the arbors of the neuron as tubes and AT THE END converts them into meshes.
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
        :param soft:
            A flag indicating that the arbors will be smooth.
        """

        # Axons
        if self.morphology.has_axons():
            if not self.options.morphology.ignore_axons:
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    self.build_arbor(
                        arbor=arbor, caps=caps, bevel_object=bevel_object,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        name=arbor.label, material=self.axons_materials[0],
                        connection_to_soma=connection_to_soma, soft=soft)

        # Apical dendrites
        if self.morphology.has_apical_dendrites():
            if not self.options.morphology.ignore_apical_dendrites:
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.build_arbor(
                        arbor=arbor, caps=caps, bevel_object=bevel_object,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        name=arbor.label,
                        material=self.apical_dendrites_materials[0],
                        connection_to_soma=connection_to_soma, soft=soft)

        # Basal dendrites
        if self.morphology.has_basal_dendrites():
            if not self.options.morphology.ignore_basal_dendrites:
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.build_arbor(
                        arbor=arbor, caps=caps, bevel_object=bevel_object,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        name=arbor.label,
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
            radius=1.0, vertices=16, name='soft_edges_arbors_bevel')

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

        nmv.logger.header('Reconstructing arbors')
        self.build_hard_edges_arbors()
        return

        # Hard edges (less samples per branch)
        if self.options.mesh.edges == nmv.enums.Meshing.Edges.HARD:
            self.build_hard_edges_arbors()

        # Smooth edges (more samples per branch)
        elif self.options.mesh.edges == nmv.enums.Meshing.Edges.SMOOTH:
            self.build_soft_edges_arbors()

        else:
            nmv.logger.log('ERROR')

    ################################################################################################
    # @weld_arbors_to_soma
    ################################################################################################
    def weld_arbors_to_soma(self):
        """Welds the arbors to the soma.
        """

        nmv.logger.header('Welding arbors to soma')

        # Gather all the arbors in a list to be joint later into a single mesh object
        arbors_meshes = list()

        # Connecting axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    arbors_meshes.append(arbor.mesh)

        # Connecting apical dendrites
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    arbors_meshes.append(arbor.mesh)

        # Connecting basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    arbors_meshes.append(arbor.mesh)

        # Joint all the meshes into a single mesh
        # arbors_mesh = nmv.mesh.ops.join_mesh_objects(mesh_list=arbors_meshes, name='arbors')

        for arbor_mesh in arbors_meshes:
            self.soma_mesh = nmv.skeleton.ops.connect_arbors_to_meta_ball_soma(
                soma_mesh=self.soma_mesh, arbors_mesh=arbor_mesh)

        # Rename the resulting mesh with the neuron name
        self.soma_mesh.name = self.morphology.label

    ################################################################################################
    # @add_spines_to_surface
    ################################################################################################
    def add_spines_to_surface(self):
        """Adds spines to the surface of the mesh.
        """

        # Build spines from a BBP circuit
        if self.options.mesh.spines == nmv.enums.Meshing.Spines.Source.CIRCUIT:
            nmv.logger.info('Adding Spines from a BBP Circuit')
            spines_objects = nmv.builders.build_circuit_spines(
                morphology=self.morphology, blue_config=self.options.morphology.blue_config,
                gid=self.options.morphology.gid, material=self.spines_materials[0])

        # Just add some random spines for the look only
        elif self.options.mesh.spines == nmv.enums.Meshing.Spines.Source.RANDOM:
            nmv.logger.info('Adding Random Spines')

            spines_builder = nmv.builders.RandomSpineBuilder(
                morphology=self.morphology, options=self.options)
            spines_objects = spines_builder.add_spines_to_morphology()

            spine_mesh_name = '%s_spines' % self.options.morphology.label
            spines_mesh = nmv.mesh.join_mesh_objects(spines_objects, spine_mesh_name)

            # Simply apply a union operation between the soma and the arbor
            self.soma_mesh = nmv.mesh.union_mesh_objects(self.soma_mesh, spines_mesh)

            # Remove the doubles
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')

            nmv.utilities.disable_std_output()
            bpy.ops.mesh.remove_doubles()
            nmv.utilities.enable_std_output()

            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.editmode_toggle()

            # Delete the other mesh
            nmv.scene.ops.delete_list_objects([spines_mesh])

    ################################################################################################
    # @smooth_edges
    ################################################################################################
    def smooth_edges(self):
        """The function cleans the surface and smooths the edges of the mesh.
        """

        if self.options.mesh.edges == nmv.enums.Meshing.Edges.SMOOTH:

            nmv.logger.header('Smooth edges')
            nmv.mesh.remove_doubles(mesh_object=self.soma_mesh, distance=0.01)

            # Triangulate
            nmv.mesh.ops.triangulate_mesh(mesh_object=self.soma_mesh)

            # Smooth the vertices
            nmv.mesh.smooth_object_vertices(mesh_object=self.soma_mesh, level=1)
            nmv.mesh.remove_doubles(mesh_object=self.soma_mesh, distance=0.01)

            # Subdivide the mesh
            nmv.mesh.subdivide_mesh(mesh_object=self.soma_mesh, level=1)

            # Enlarge the mesh
            nmv.mesh.enlarge_mesh_using_displacement_modifier(
                mesh_object=self.soma_mesh, enlargement_factor=0.05)

            # Further smooth object vertices
            nmv.mesh.remove_doubles(mesh_object=self.soma_mesh, distance=0.01)
            nmv.mesh.smooth_object_vertices(mesh_object=self.soma_mesh, level=5)

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):
        """Reconstructs the mesh.
        """

        nmv.logger.header('Building Mesh: UnionBuilder')

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        self.create_skeleton_materials()

        # Verify and repair the morphology, if required
        result, stats = nmv.utilities.profile_function(self.update_morphology_skeleton)
        self.profiling_statistics += stats

        # Apply skeleton - based operation, if required, to slightly modify the skeleton
        result, stats = nmv.utilities.profile_function(self.modify_morphology_skeleton)
        self.profiling_statistics += stats

        # Resample the sections of the morphology skeleton
        self.resample_skeleton_sections()

        # Build the soma, with the default parameters
        self.options.soma.meta_ball_resolution = 0.25
        result, stats = nmv.utilities.profile_function(self.reconstruct_soma_mesh)
        self.profiling_statistics += stats

        # Build the arbors
        result, stats = nmv.utilities.profile_function(self.build_arbors)
        self.profiling_statistics += stats

        # Connect to the soma
        result, stats = nmv.utilities.profile_function(self.weld_arbors_to_soma)
        self.profiling_statistics += stats

        # Add the spines
        result, stats = nmv.utilities.profile_function(self.add_spines_to_surface)
        self.profiling_statistics += stats

        # Cleaning mesh
        result, stats = nmv.utilities.profile_function(self.smooth_edges)
        self.profiling_statistics += stats

        # Surface roughness
        result, stats = nmv.utilities.profile_function(self.add_surface_noise_to_arbor)
        self.profiling_statistics += stats

        # Decimation
        result, stats = nmv.utilities.profile_function(self.decimate_neuron_mesh)
        self.profiling_statistics += stats

        # Transform to the global coordinates, if required
        result, stats = nmv.utilities.profile_function(self.transform_to_global_coordinates)
        self.profiling_statistics += stats

        # Collect the stats. of the mesh
        result, stats = nmv.utilities.profile_function(self.collect_mesh_stats)
        self.profiling_statistics += stats

        # Report
        nmv.logger.statistics(self.profiling_statistics)

        # Write the stats to file
        self.write_statistics_to_file(tag='union')

