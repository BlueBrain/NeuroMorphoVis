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
        - You can still color-code each arbor type in the morphology.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options,
                 this_is_proxy_mesh=False):
        """Constructor

        :param morphology:
            A given morphology skeleton to create a mesh for.
        :param options:
            Loaded options from NeuroMorphoVis.
        :param this_is_proxy_mesh:
            A flag to indicate that the resulting mesh from this builder is a proxy mesh or not.
        """

        # Initialize the parent with the common parameters
        MeshBuilderBase.__init__(self, morphology, options, 'piecewise')

        # A flag to indicate that the resulting mesh is a proxy mesh
        self.this_is_proxy_mesh = this_is_proxy_mesh

        # Statistics
        self.profiling_statistics = 'PiecewiseBuilder Profiling Stats.: \n'

        # Stats. about the mesh
        self.mesh_statistics = 'PiecewiseBuilder Mesh: \n'

    ################################################################################################
    # @confirm_single_or_multiple_mesh_objects
    ################################################################################################
    def confirm_single_or_multiple_mesh_objects(self):
        """Confirms if the generated mesh from this builder is joint in a single mesh object or
        multiple ones. The result depends on the selection of the user and the nature of the builder
        and other factors, therefore this function is re-implemented for every builder."""

        # If this is a proxy mesh, then it is a single mesh object, otherwise, it is user-defined
        if self.this_is_proxy_mesh:
            self.result_is_single_object_mesh = True
        else:
            connection = self.options.mesh.neuron_objects_connection
            if connection == nmv.enums.Meshing.ObjectsConnection.CONNECTED:
                self.result_is_single_object_mesh = True
            else:
                self.result_is_single_object_mesh = False

    ################################################################################################
    # @initialize_builder
    ################################################################################################
    def initialize_builder(self):
        """Initializes the different parameters/options of the builder required for building."""

        # Is it a single object or multiple objects
        self.confirm_single_or_multiple_mesh_objects()

        # Create the materials of the morphology skeleton
        self.create_skeleton_materials()

        # Create illumination only if this is not a proxy mesh
        if not self.this_is_proxy_mesh:
            self.create_illumination()

        # Verify and repair the morphology, if required
        self.update_morphology_skeleton()

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
                        soma_center=self.morphology.soma.centroid,
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

                        # Rename the arbor object
                        arbor_object.name = arbor.label

                        # Append the resulting mesh to the meshes list
                        self.neuron_meshes.append(arbor_object)

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
                        soma_center=self.morphology.soma.centroid,
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

                        # Rename the arbor object
                        arbor_object.name = arbor.label

                        # Append the resulting mesh to the meshes list
                        self.neuron_meshes.append(arbor_object)

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
                        soma_center=self.morphology.soma.centroid,
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

                        # Rename the arbor object
                        arbor_object.name = arbor.label

                        # Append the resulting mesh to the meshes list
                        self.neuron_meshes.append(arbor_object)

    ################################################################################################
    # @build_hard_edges_arbors
    ################################################################################################
    def build_hard_edges_arbors(self):
        """Reconstruct the meshes of the arbors of the neuron with HARD edges."""

        # Create a bevel object that will be used to create the mesh
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, resolution=self.options.morphology.bevel_object_sides, name='Cross Section')

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
    # @reconstruct_arbors_meshes
    ################################################################################################
    def reconstruct_arbors_meshes(self):
        """Reconstruct the arbors."""

        nmv.logger.header('Reconstructing arbors')

        # Hard edges (less samples per branch)
        self.build_hard_edges_arbors()

    ################################################################################################
    # @create_joint_proxy_mesh
    ################################################################################################
    def create_joint_proxy_mesh(self):

        # Join all the mesh objects into a single one
        self.neuron_mesh = nmv.mesh.join_mesh_objects(self.neuron_meshes, self.morphology.label)

        # Clear all the lists that contain references to the meshes, they are not valid anymore
        self.clear_meshes_lists()

        # Adjust the origin of the resulting mesh
        nmv.mesh.set_mesh_origin(
            mesh_object=self.neuron_mesh, coordinate=self.morphology.soma.centroid)

    ################################################################################################
    # @reconstruct_mesh
    ################################################################################################
    def reconstruct_mesh(self):
        """Reconstructs the mesh."""

        nmv.logger.header('Building Mesh: PiecewiseBuilder')

        # Initialization
        result, stats = self.PROFILE(self.initialize_builder)
        self.profiling_statistics += stats

        # Build the soma
        result, stats = self.PROFILE(self.reconstruct_soma_mesh)
        self.profiling_statistics += stats

        # Build the arbors
        result, stats = self.PROFILE(self.reconstruct_arbors_meshes)
        self.profiling_statistics += stats

        # Connect to the soma to the arbors, if required
        result, stats = self.PROFILE(self.connect_arbors_to_soma)
        self.profiling_statistics += stats

        # Build the endfeet, if required
        result, stats = self.PROFILE(self.build_endfeet)
        self.profiling_statistics += stats

        # Tessellation, if required
        if not self.this_is_proxy_mesh:
            result, stats = self.PROFILE(self.decimate_neuron_mesh)
            self.profiling_statistics += stats

        # Add the spines
        if not self.this_is_proxy_mesh:
            result, stats = self.PROFILE(self.add_spines_to_surface)
            self.profiling_statistics += stats

        # Aggregation and origin adjustments
        if self.this_is_proxy_mesh:
            result, stats = self.PROFILE(self.join_objects_and_adjust_origin)
        else:
            result, stats = self.PROFILE(self.create_joint_proxy_mesh)
        self.profiling_statistics += stats

        # Report the statistics of this builder
        if not self.this_is_proxy_mesh:
            self.report_builder_statistics()

        # Return the list of the resulting mesh, either as a single object or multiple ones
        return [self.neuron_mesh] if self.result_is_single_object_mesh else self.neuron_meshes
