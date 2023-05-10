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

# Internal imports
from .base import MorphologyBuilderBase
import nmv.mesh
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.geometry
import nmv.scene
import nmv.bmeshi
import nmv.shading
import nmv.utilities


####################################################################################################
# @SamplesBuilder
####################################################################################################
class SamplesBuilder(MorphologyBuilderBase):
    """Builds and draws the morphology as a series of samples where each sample is represented by
    a sphere.

    Note that we use 'bmeshes' to generate the spheres and then link them to the scene ALL AT ONCE
    to make their creation faster.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor.

        :param morphology:
            A given morphology.
        """

        # Initialize the parent with the common parameters
        MorphologyBuilderBase.__init__(self, morphology, options)

    ################################################################################################
    # @draw_sections_as_spheres
    ################################################################################################
    def draw_sections_as_spheres(self,
                                 root,
                                 name,
                                 sphere_objects=[],
                                 branching_order=0,
                                 max_branching_order=nmv.consts.Math.INFINITY):
        """Draw the section as a list of spheres.

        :param root:
            Root section of the tree to be drawn.
        :param name:
            Prefix for labeling the spheres.
        :param sphere_objects:
            A list of the drawn spheres.
         :param branching_order:
            Current branching level of the arbor.
        :param max_branching_order:
            The maximum branching level given by the user.
        :return:
        """

        # Ignore the drawing if the root section is None
        if root is None:
            return

        # Increment the branching level
        branching_order += 1

        # Stop drawing at the maximum branching level
        if branching_order > max_branching_order:
            return

        # Make sure that the arbor exist and then draw the spheres, append them to the objects list
        if root is not None:
            drawn_spheres = nmv.skeleton.draw_section_samples_as_spheres(
                section=root, optimize_based_on_radius=True)

            # Add the drawn segments to the 'segments_objects'
            sphere_objects.extend(drawn_spheres)

            # Draw the children sections
            for child in root.children:
                self.draw_sections_as_spheres(
                    root=child,
                    branching_order=branching_order,
                    max_branching_order=max_branching_order,
                    name=name,
                    sphere_objects=sphere_objects)

    ################################################################################################
    # @link_and_shade_spheres_as_group
    ################################################################################################
    def link_and_shade_spheres_as_group(self,
                                        sphere_list,
                                        material,
                                        prefix):
        """Links the spheres created from the bmesh interface to the scene.

        :param sphere_list:
            A list of sphere to be linked to the scene and shaded with the corresponding materials.
        :param material:
            The material that will be applied to the spheres (representing the samples) after being
            linked to the scene.
        :param prefix:
            Prefix to name each sphere object after linking it to the scene.
        """

        # Join all the bmesh objects into a single joint bmesh
        joint_bmesh = nmv.bmeshi.join_bmeshes_list(bmeshes_list=sphere_list)

        # Link the bmesh spheres to the scene to visualize the arbor samples
        arbor_mesh = nmv.bmeshi.ops.link_to_new_object_in_scene(joint_bmesh, prefix)

        # Smooth shading
        nmv.mesh.shade_smooth_object(arbor_mesh)

        # Assign the material
        nmv.shading.set_material_to_object(arbor_mesh, material)

        # Append the arbor mesh to the morphology objects
        self.morphology_objects.append(arbor_mesh)

    ################################################################################################
    # @link_and_shade_arbor_spheres
    ################################################################################################
    def link_and_shade_arbor_spheres(self,
                                     sphere_list,
                                     materials_list,
                                     prefix):
        """Links the added sphere that compose the arbor to the scene.

        :param sphere_list:
            A list of sphere to be linked to the scene and shaded with the corresponding materials.
        :param materials_list:
            A list of materials to be applied to the spheres after being linked to the scene.
        :param prefix:
            Prefix to name each sphere object after linking it to the scene.
        """

        # A list that will contain all the objects to be joint in a single mesh for performance
        joint_objects = list()

        # Iteration objects
        iteration_objects = list()

        for i, sphere in enumerate(sphere_list):

            # Show progress
            nmv.utilities.time_line.show_iteration_progress('Sample', i, len(sphere_list))

            name = '%s %d' % (prefix, i)

            # Link the bmesh spheres to the scene
            sphere_mesh = nmv.bmeshi.ops.link_to_new_object_in_scene(sphere, name)

            # Add the sphere to the group
            iteration_objects.append(sphere_mesh)

            # Group every 100 objects into a single group
            if i % 50 == 0:

                # Join the meshes into a group
                joint_object = nmv.mesh.join_mesh_objects(
                    mesh_list=iteration_objects, name='Group %d' % (i % 100))

                # Add to the joint objects list
                joint_objects.append(joint_object)

                # Clear the iteration objects
                iteration_objects.clear()

        # Join the meshes into a group, if @iteration_objects has more than one object
        if len(iteration_objects) > 1:
            joint_object = nmv.mesh.join_mesh_objects(
                mesh_list=iteration_objects, name='Group %d' % (i % 100))

            # Add to the joint objects
            joint_objects.append(joint_object)

        # Done
        nmv.utilities.time_line.show_iteration_progress(
            'Sample', len(sphere_list), len(sphere_list), done=True)

        # Compile the arbor mesh
        arbor_mesh = nmv.mesh.join_mesh_objects(mesh_list=joint_objects, name=prefix)

        # Smooth shading
        nmv.mesh.shade_smooth_object(arbor_mesh)

        # Assign the material
        nmv.shading.set_material_to_object(arbor_mesh, materials_list[0])

        # Append the sphere mesh to the morphology objects
        self.morphology_objects.append(arbor_mesh)

    ################################################################################################
    # @draw_arbors
    ################################################################################################
    def draw_arbors(self):
        """Draws the arbors."""

        nmv.logger.info('Constructing arbors - spheres')

        # Apical dendrite
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    apical_dendrite_spheres = list()
                    self.draw_sections_as_spheres(
                        root=arbor, name=arbor.label,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        sphere_objects=apical_dendrite_spheres)
                    self.link_and_shade_arbor_spheres(
                        sphere_list=apical_dendrite_spheres,
                        materials_list=self.apical_dendrites_materials,
                        prefix=arbor.label)

        # Axon
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    axon_spheres = list()
                    self.draw_sections_as_spheres(
                        root=arbor, name=arbor.label,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        sphere_objects=axon_spheres)
                    self.link_and_shade_arbor_spheres(
                        sphere_list=axon_spheres,
                        materials_list=self.axons_materials,
                        prefix=arbor.label)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    basal_dendrites_spheres = list()
                    self.draw_sections_as_spheres(
                        root=arbor, name=arbor.label,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        sphere_objects=basal_dendrites_spheres)
                    self.link_and_shade_arbor_spheres(
                        sphere_list=basal_dendrites_spheres,
                        materials_list=self.basal_dendrites_materials,
                        prefix=arbor.label)

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self,
                                 context=None):
        """Reconstruct and draw the morphological skeleton.

        :param context:
            Blender context to access the UI
        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """
        nmv.logger.header('Building Skeleton: SamplesBuilder')

        # Update the context
        self.context = context

        # Initialize the builder
        self.initialize_builder()

        # Draws the arbors
        self.draw_arbors()

        # Draw the soma
        self.draw_soma()

        # Draw the endfeet, if applicable
        self.draw_endfeet_if_applicable()

        # Add the morphology objects to a collection
        self.collection_morphology_objects_in_collection()

        # Return the list of the drawn morphology objects
        return self.morphology_objects
