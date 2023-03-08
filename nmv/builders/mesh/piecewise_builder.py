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
class PiecewiseBuilder(MeshBuilderBase):
    """Mesh builder that creates piecewise meshes.
    NOTES:
        - The meshes produced by this builder are not guaranteed to be watertight.
        - This is the fastest mesh builder amongst all the other builders in the Meshing Toolbox.
        - You can still color-code each arbor type in the morphology, unlike the MetaBuilder.
        - The resulting mehes can be used with Ultraliser to create optimized and watertight ones.
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
        self.profiling_statistics = 'PiecewiseBuilder Profiling Stats.: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'PiecewiseBuilder Mesh: \n'

        # Verify the connectivity of the arbors to the soma
        nmv.skeleton.verify_arbors_connectivity_to_soma(morphology=self.morphology)

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

        # Apical dendrites
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for i, arbor in enumerate(self.morphology.apical_dendrites):
                    nmv.logger.detail(arbor.label)

                    # A list to keep all the generated objects of the arbor
                    arbor_objects = list()

                    nmv.skeleton.ops.draw_connected_sections(
                        section=arbor,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        name=arbor.label,
                        material_list=self.apical_dendrites_materials,
                        bevel_object=bevel_object,
                        repair_morphology=False,
                        caps=caps,
                        sections_objects=arbor_objects,
                        roots_connection=roots_connection)

                    # Ensure that apical dendrite objects were reconstructed
                    if len(arbor_objects) > 0:

                        # Join the objects into a single object
                        arbor_object = nmv.scene.join_objects(scene_objects=arbor_objects)

                        # Add a reference to the mesh object
                        self.morphology.apical_dendrites[i].mesh = arbor_object

                        # Add the sections (tubes) of the apical dendrite to the list
                        self.apical_dendrites_meshes.append(arbor_object)

                        # Convert the section object (tubes) into meshes
                        nmv.scene.ops.convert_object_to_mesh(arbor_object)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for i, arbor in enumerate(self.morphology.basal_dendrites):
                    nmv.logger.detail(arbor.label)

                    # A list to keep all the generated objects of the arbor
                    arbor_objects = list()

                    # Draw the basal dendrites as a set connected sections
                    nmv.skeleton.ops.draw_connected_sections(
                        section=arbor,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        name=arbor.label,
                        material_list=self.basal_dendrites_materials,
                        bevel_object=bevel_object,
                        repair_morphology=False,
                        caps=caps,
                        sections_objects=arbor_objects,
                        roots_connection=roots_connection)

                    # Ensure that objects were reconstructed
                    if len(arbor_objects) > 0:

                        # Join the objects into a single object
                        arbor_object = nmv.scene.join_objects(scene_objects=arbor_objects)

                        # Add a reference to the mesh object
                        self.morphology.basal_dendrites[i].mesh = arbor_object

                        # Add the sections (tubes) of the basal dendrite to the list
                        self.basal_dendrites_meshes.append(arbor_object)

                        # Convert the section object (tubes) into meshes
                        nmv.scene.ops.convert_object_to_mesh(arbor_object)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for i, arbor in enumerate(self.morphology.axons):
                    nmv.logger.detail(arbor.label)

                    # A list to keep all the generated objects of the arbor
                    arbor_objects = list()

                    # Draw the axon as a set connected sections
                    nmv.skeleton.ops.draw_connected_sections(
                        section=arbor,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        name=arbor.label,
                        material_list=self.axons_materials,
                        bevel_object=bevel_object,
                        repair_morphology=False,
                        caps=caps,
                        sections_objects=arbor_objects,
                        roots_connection=roots_connection)

                    # Ensure that axon objects were reconstructed
                    if len(arbor_objects) > 0:

                        # Join the objects into a single object
                        arbor_object = nmv.scene.join_objects(scene_objects=arbor_objects)

                        # Add a reference to the mesh object
                        self.morphology.axons[i].mesh = arbor_object

                        # Add the sections (tubes) of the basal dendrite to the list
                        self.axons_meshes.append(arbor_object)

                        # Convert the section object (tubes) into meshes
                        nmv.scene.ops.convert_object_to_mesh(arbor_object)

    ################################################################################################
    # @build_hard_edges_arbors
    ################################################################################################
    def build_hard_edges_arbors(self):
        """Reconstruct the meshes of the arbors of the neuron with HARD edges.
        """

        # Create a bevel object that will be used to create the mesh
        bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=8, name='arbors_bevel')

        # If the meshes of the arbors are 'welded' into the soma, then do NOT connect them to the
        #  soma origin, otherwise extend the arbors to the origin
        if self.options.mesh.soma_type == nmv.enums.Soma.Representation.SOFT_BODY:
            if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
                roots_connection = nmv.enums.Skeleton.Roots.CONNECT_CONNECTED_TO_SOMA
            else:
                roots_connection = nmv.enums.Skeleton.Roots.CONNECT_CONNECTED_TO_ORIGIN
        else:
            roots_connection = nmv.enums.Skeleton.Roots.CONNECT_CONNECTED_TO_ORIGIN

        # Create the arbors using this 16-side bevel object and CLOSED caps (no smoothing required)
        self.build_arbors(bevel_object=bevel_object, caps=True, roots_connection=roots_connection)

        # Close caps
        nmv.logger.detail('Closing caps')

        # Close the caps of the apical dendrites meshes
        for arbor_object in self.apical_dendrites_meshes:
            nmv.mesh.close_open_faces(arbor_object)

        # Close the caps of the basal dendrites meshes
        for arbor_object in self.basal_dendrites_meshes:
            nmv.mesh.close_open_faces(arbor_object)

        # Close the caps of the axon meshes
        for arbor_object in self.axons_meshes:
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
        bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=8, name='arbors_bevel')

        # If the meshes of the arbors are 'welded' into the soma, then do NOT connect them to the
        #  soma origin, otherwise extend the arbors to the origin
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            roots_connection = nmv.enums.Skeleton.Roots.CONNECT_CONNECTED_TO_SOMA
        else:
            roots_connection = nmv.enums.Skeleton.Roots.CONNECT_CONNECTED_TO_ORIGIN

        # Create the arbors using this 4-side bevel object and OPEN caps (for smoothing)
        self.build_arbors(bevel_object=bevel_object, caps=False, roots_connection=roots_connection)

        # Smooth and close the faces of the apical dendrites meshes
        for mesh in self.apical_dendrites_meshes:
            nmv.mesh.ops.smooth_object_vertices(mesh_object=mesh, level=2)

        # Smooth and close the faces of the basal dendrites meshes
        for mesh in self.basal_dendrites_meshes:
            nmv.mesh.ops.smooth_object_vertices(mesh_object=mesh, level=2)

        # Smooth and close the faces of the axon meshes
        for mesh in self.axons_meshes:
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

        nmv.logger.header('Reconstructing arbors')

        # Hard edges (less samples per branch)
        if self.options.mesh.edges == nmv.enums.Meshing.Edges.HARD:
            self.build_hard_edges_arbors()

        # Smooth edges (more samples per branch)
        elif self.options.mesh.edges == nmv.enums.Meshing.Edges.SMOOTH:
            self.build_soft_edges_arbors()

        else:
            nmv.logger.log('ERROR')

    ################################################################################################
    # @build_endfeet
    ################################################################################################
    def build_endfeet(self):
        """Builds the endfeet in case of loading astrocytic morphologies.
        """

        self.endfeet_meshes.extend(self.reconstruct_endfeet())

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

        nmv.logger.header('Building Mesh: PiecewiseBuilder')

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        self.create_skeleton_materials()

        # Verify and repair the morphology, if required
        result, stats = nmv.utilities.profile_function(self.update_morphology_skeleton)
        self.profiling_statistics += stats

        # Verify the connectivity of the arbors to the soma to filter the disconnected arbors,
        # for example, an axon that is emanating from a dendrite or two intersecting dendrites
        nmv.skeleton.ops.verify_arbors_connectivity_to_soma(self.morphology)

        # Build the soma, with the default parameters
        result, stats = nmv.utilities.profile_function(self.reconstruct_soma_mesh)
        self.profiling_statistics += stats

        # Build the arbors
        result, stats = nmv.utilities.profile_function(self.reconstruct_arbors_meshes)
        self.profiling_statistics += stats

        # Connect to the soma
        result, stats = nmv.utilities.profile_function(self.connect_arbors_to_soma)
        self.profiling_statistics += stats

        # Build the endfeet
        result, stats = nmv.utilities.profile_function(self.build_endfeet)
        self.profiling_statistics += stats

        # Tessellation
        result, stats = nmv.utilities.profile_function(self.decimate_neuron_mesh)
        self.profiling_statistics += stats

        # Surface roughness
        result, stats = nmv.utilities.profile_function(self.add_surface_noise_to_arbor)
        self.profiling_statistics += stats

        # Add the spines
        result, stats = nmv.utilities.profile_function(self.add_spines_to_surface)
        self.profiling_statistics += stats

        # Join all the objects into a single object
        result, stats = nmv.utilities.profile_function(self.join_mesh_object_into_single_object)
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
        self.write_statistics_to_file(tag='piecewise')

        # Return a list of all the mesh objects in the scene
        mesh_objects = self.get_neuron_mesh_objects()
        return mesh_objects

    ################################################################################################
    # @reconstruct_mesh_in_single_object
    ################################################################################################
    def reconstruct_mesh_in_single_object(self):
        """Returns a single mesh object for all the neuron components.

        :return:
            A single mesh object of the neuron.
        """

        return nmv.mesh.join_mesh_objects(mesh_list=self.reconstruct_mesh(),
                                          name='Mesh_%s' % self.morphology.label)
