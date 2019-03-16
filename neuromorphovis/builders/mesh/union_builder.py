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
import neuromorphovis as nmv
import neuromorphovis.builders
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.mesh
import neuromorphovis.shading
import neuromorphovis.skeleton
import neuromorphovis.scene


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
        self.reconstructed_soma_mesh = None

    ################################################################################################
    # @build_arbors
    ################################################################################################
    def build_arbors(self,
                     bevel_object,
                     caps):
        """
        Builds the arbors of the neuron as tubes and AT THE END converts them into meshes.
        If you convert them during the building, the scene is getting crowded and the process is
        getting exponentially slower.

        :param bevel_object: A given bevel object to scale the section at the different samples.
        :param caps: A flag to indicate whether the drawn sections are closed or not.
        :return: A list of all the individual meshes of the arbors.
        """

        # Remove the internal samples, or the samples that intersect the soma at the first
        # section and each arbor
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology,
              nmv.skeleton.ops.remove_samples_inside_soma])

        # The arbors can be selected to be reconstructed with sharp edges or smooth ones. For the
        # sharp edges, we do NOT need to resample the morphology skeleton. However, if the smooth
        # edges option is selected, the arbors must be re-sampled to avoid any meshing artifacts
        # after applying the vertex smoothing filter. The resampling filter for the moment
        # re-samples the morphology sections at 2.5 microns, however this can be improved later
        # by adding an algorithm that re-samples the section based on its radii.
        # if self.options.mesh.edges == enumerators.__meshing_smooth_edges__:

        # Apply the resampling filter on the whole morphology skeleton
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.ops.resample_sections, 0.5])

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

        # Create a list that keeps references to the meshes of all the connected pieces of the
        # arbors of the mesh.
        arbors_objects = []

        # Draw the axon as a set connected sections

        if self.morphology.axon is not None:
            if not self.options.morphology.ignore_axon:
                nmv.logger.log('\t * Axon')

                # Individual sections (tubes) of the axon
                axon_objects = []

                nmv.skeleton.ops.draw_connected_sections(
                    section=copy.deepcopy(self.morphology.axon),
                    max_branching_level=self.options.morphology.axon_branch_order,
                    name=nmv.consts.Arbors.AXON_PREFIX,
                    material_list=self.axon_materials,
                    bevel_object=bevel_object,
                    repair_morphology=True,
                    caps=False,
                    sections_objects=axon_objects)

                # Convert the section object (tubes) into meshes
                for mesh_object in axon_objects:
                    nmv.scene.ops.convert_object_to_mesh(mesh_object)

                axon_mesh = nmv.mesh.ops.union_mesh_objects_in_list(axon_objects)

                # Smooth the mesh object
                # nmv.mesh.smooth_object(mesh_object=axon_mesh, level=2)

                # Add a reference to the mesh object
                self.morphology.axon.mesh = axon_mesh

                # Add the sections (tubes) of the axons to the list
                arbors_objects.append(axon_mesh)

        # Draw the apical dendrite, if exists
        if self.morphology.apical_dendrite is not None:
            if not self.options.morphology.ignore_apical_dendrite:
                nmv.logger.log('\t * Apical dendrite')

                # Individual sections (tubes) of the apical dendrite
                apical_dendrite_objects = []

                # A list of all the connecting points of the apical dendrites
                apical_dendrite_connection_points = []

                secondary_sections = []

                if self.morphology.apical_dendrite is not None:
                    nmv.skeleton.ops.draw_connected_sections(
                        section=copy.deepcopy(self.morphology.apical_dendrite),
                        max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                        name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                        material_list=self.apical_dendrites_materials,
                        bevel_object=bevel_object,
                        repair_morphology=True,
                        caps=False,
                        sections_objects=apical_dendrite_objects,
                        secondary_sections=secondary_sections)

                    # Convert the section object (tubes) into meshes
                    for mesh_object in apical_dendrite_objects:
                        nmv.scene.ops.convert_object_to_mesh(mesh_object)

                    apical_dendrite_mesh = nmv.mesh.ops.union_mesh_objects_in_list(
                        apical_dendrite_objects)

                    # Smooth the mesh object
                    # nmv.mesh.smooth_object(mesh_object=apical_dendrite_mesh, level=2)

                    # Further smoothing, only with shading
                    #nmv.mesh.shade_smooth_object(apical_dendrite_mesh)

                    # Add a reference to the mesh object
                    self.morphology.apical_dendrite.mesh = apical_dendrite_mesh

                    # Add the sections (tubes) of the basal dendrites to the list
                    arbors_objects.append(apical_dendrite_mesh)

        # Draw the basal dendrites
        if self.morphology.dendrites is not None:
            if not self.options.morphology.ignore_basal_dendrites:

                # Individual sections (tubes) of each basal dendrite
                basal_dendrites_objects = []

                # Do it dendrite by dendrite
                for i, basal_dendrite in enumerate(self.morphology.dendrites):

                    nmv.logger.log('\t * Dendrite [%d]' % i)

                    # Individual sections (tubes) of the basal dendrite
                    basal_dendrite_objects = []

                    # Draw the basal dendrites as a set connected sections
                    basal_dendrite_prefix = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)

                    nmv.skeleton.ops.draw_connected_sections(
                        section=copy.deepcopy(basal_dendrite),
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                        name=basal_dendrite_prefix,
                        material_list=self.basal_dendrites_materials,
                        bevel_object=bevel_object,
                        repair_morphology=True,
                        caps=False,
                        sections_objects=basal_dendrite_objects)

                    # Convert the section object (tubes) into meshes
                    for mesh_object in basal_dendrite_objects:
                        nmv.scene.ops.convert_object_to_mesh(mesh_object)

                    basal_dendrite_mesh = nmv.mesh.ops.union_mesh_objects_in_list(
                        basal_dendrite_objects)

                    # Smooth the mesh object
                    # nmv.mesh.smooth_object(mesh_object=basal_dendrite_mesh, level=2)

                    # Further smoothing, only with shading
                    #nmv.mesh.shade_smooth_object(basal_dendrite_mesh)

                    # Add a reference to the mesh object
                    self.morphology.dendrites[i].mesh = basal_dendrite_mesh

                    # Add the sections (tubes) of the basal dendrite to the list
                    arbors_objects.append(basal_dendrite_mesh)

        # Return the list of meshes
        return arbors_objects



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

        # Connecting apical dendrite
        if not self.options.morphology.ignore_apical_dendrite:

            # There is an apical dendrite
            if self.morphology.apical_dendrite is not None:
                nmv.logger.log('\t * Apical dendrite')
                nmv.skeleton.ops.connect_arbor_to_soma(
                    self.reconstructed_soma_mesh, self.morphology.apical_dendrite)

        # Connecting basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Do it dendrite by dendrite
            for i, basal_dendrite in enumerate(self.morphology.dendrites):
                nmv.logger.log('\t * Dendrite [%d]' % i)
                nmv.skeleton.ops.connect_arbor_to_soma(
                    self.reconstructed_soma_mesh, basal_dendrite)

        # Connecting axon
        if not self.options.morphology.ignore_axon:
            nmv.logger.log('\t * Axon')
            nmv.skeleton.ops.connect_arbor_to_soma(
                self.reconstructed_soma_mesh, self.morphology.axon)

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
        self.build_arbors(bevel_object=bevel_object, caps=True,
                          roots_connection=roots_connection)

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
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0 * math.sqrt(2), vertices=4, name='arbors_bevel')

        # If the meshes of the arbors are 'welded' into the soma, then do NOT connect them to the
        #  soma origin, otherwise extend the arbors to the origin
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_SOMA
        else:
            roots_connection = nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN

        # Create the arbors using this 4-side bevel object and OPEN caps (for smoothing)
        self.build_arbors(bevel_object=bevel_object, caps=False,
                          roots_connection=roots_connection)

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
        """
        Reconstructs the neuronal mesh as a set of piecewise watertight meshes.
        The meshes are logically connected, but the different branches are intersecting,
        so they can be used perfectly for voxelization purposes, but they cannot be used for
        surface rendering with transparency.
        """

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        nmv.builders.create_skeleton_materials(builder=self)

        # Verify and repair the morphology, if required
        # self.verify_morphology_skeleton()

        # Apply skeleton-based operation, if required, to slightly modify the morphology skeleton
        # self.modify_morphology_skeleton()

        # Build the soma
        # self.reconstruct_soma_mesh()

        # Build the arbors
        # self.reconstruct_arbors_meshes()

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


        # Create a bevel object that will be used to create an proxy skeleton of the mesh
        # Note that the radius is set to conserve the volumes of the branches
        #bevel_object = nmv.mesh.create_bezier_circle(
        #    radius=1.0 * math.sqrt(2), vertices=4, name='bevel')

        bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=16, name='bevel')


        # Create the arbors using this 4-side bevel object and open caps (for smoothing)
        arbors_meshes = self.build_arbors(bevel_object=bevel_object, caps=True)
        #return

        # Smooth and close the faces in one step
        for mesh in arbors_meshes:
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.vert_connect_concave()
            bpy.ops.object.editmode_toggle()
            #nmv.mesh.ops.smooth_object(mesh, level=2)

        return arbors_meshes
        # Close the caps to be able to bridge
        for mesh in arbors_meshes:
            nmv.mesh.ops.close_open_faces(mesh)

        # return None
        nmv.logger.log('Connecting the branches to the soma')
        self.connect_arbors_to_soma()

        return

        # Apical dendrite
        if not self.options.morphology.ignore_apical_dendrite:

            # There is an apical dendrite
            if self.morphology.apical_dendrite is not None:

                nmv.logger.log('\t * Apical dendrite')
                nmv.skeleton.ops.connect_arbor_to_soma(self.reconstructed_soma_mesh, self.morphology.apical_dendrite)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Individual sections (tubes) of each basal dendrite
            basal_dendrites_objects = []

            # Do it dendrite by dendrite
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                nmv.logger.log('\t * Dendrite [%d]' % i)
                nmv.skeleton.ops.connect_arbor_to_soma(self.reconstructed_soma_mesh, basal_dendrite)

        if not self.options.morphology.ignore_axon:

            nmv.logger.log('\t * Axon')
            nmv.skeleton.ops.connect_arbor_to_soma(self.reconstructed_soma_mesh, self.morphology.axon)

        return None

        # Join the arbors and the soma in the same mesh object and rename it to the
        # morphology name
        neuron_mesh = nmv.mesh.ops.join_mesh_objects(
            mesh_list=neuron_meshes, name='%s_mesh' % self.options.morphology.label)



        # Close all the open faces to avoid leaks (watertight)
        # nmv.mesh.ops.close_open_faces(neuron_mesh)

        # Delete the bevel object
        nmv.scene.ops.delete_object_in_scene(bevel_object)

        # Return a reference to the created neuron mesh
        return neuron_mesh
