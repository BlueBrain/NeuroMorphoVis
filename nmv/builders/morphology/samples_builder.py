####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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

    NOTE: We use bmeshes to generate the spheres and then link them to the scene all at once.
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
    # @create_single_skeleton_materials_list
    ################################################################################################
    def create_single_skeleton_materials_list(self):
        """Creates a list of all the materials required for coloring the skeleton.

        NOTE: Before drawing the skeleton, create the materials, once and for all, to improve the
        performance since this is way better than creating a new material per section or segment
        or any individual object.
        """
        nmv.logger.info('Creating materials')

        # Create the default material list
        self.create_skeleton_materials_and_illumination()

        # Index: 0 - 1
        self.skeleton_materials.extend(self.soma_materials)

        # Index: 2 - 3
        self.skeleton_materials.extend(self.apical_dendrites_materials)

        # Index: 4 - 5
        self.skeleton_materials.extend(self.basal_dendrites_materials)

        # Index: 6 - 7
        self.skeleton_materials.extend(self.axons_materials)

    ################################################################################################
    # @draw_sections_as_spheres
    ################################################################################################
    def draw_sections_as_spheres(self,
                                 root,
                                 name,
                                 material_list=[],
                                 sphere_objects=[],
                                 branching_order=0,
                                 max_branching_order=nmv.consts.Math.INFINITY):
        """Draw the section as a list of spheres.

        :param root:
            Root section of the tree to be drawn.
        :param name:
            Prefix for labeling the spheres.
        :param material_list:
            A list of materials specific to the type of arbor being drawn.
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
            drawn_spheres = nmv.skeleton.draw_section_samples_as_spheres(section=root)

            # Add the drawn segments to the 'segments_objects'
            sphere_objects.extend(drawn_spheres)

            # Draw the children sections
            for child in root.children:
                self.draw_sections_as_spheres(
                    root=child,
                    branching_order=branching_order,
                    max_branching_order=max_branching_order,
                    name=name,
                    material_list=material_list,
                    sphere_objects=sphere_objects)

    ################################################################################################
    # @link_and_shade_spheres_as_group
    ################################################################################################
    def link_and_shade_spheres_as_group(self,
                                        sphere_list,
                                        materials_list,
                                        prefix):
        """Links the added sphere to the scene.

        :param sphere_list:
            A list of sphere to be linked to the scene and shaded with the corresponding materials.
        :param materials_list:
            A list of materials to be applied to the spheres after being linked to the scene.
        :param prefix:
            Prefix to name each sphere object after linking it to the scene.
        """

        joint_bmesh = nmv.bmeshi.join_bmeshes_list(bmeshes_list=sphere_list)

        # Link the bmesh spheres to the scene
        sphere_mesh = nmv.bmeshi.ops.link_to_new_object_in_scene(joint_bmesh, prefix)

        # Smooth shading
        nmv.mesh.shade_smooth_object(sphere_mesh)

        # Assign the material
        nmv.shading.set_material_to_object(sphere_mesh, materials_list[0])

        # Append the sphere mesh to the morphology objects
        self.morphology_objects.append(sphere_mesh)

    ################################################################################################
    # @link_and_shade_spheres
    ################################################################################################
    def link_and_shade_spheres(self,
                               sphere_list,
                               materials_list,
                               prefix):
        """Links the added sphere to the scene.

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

            name = '%s_%d' % (prefix, i)

            # Link the bmesh spheres to the scene
            sphere_mesh = nmv.bmeshi.ops.link_to_new_object_in_scene(sphere, name)

            # Add the sphere to the group
            iteration_objects.append(sphere_mesh)

            # Group every 100 objects into a single group
            if i % 50 == 0:

                # Join the meshes into a group
                joint_object = nmv.mesh.join_mesh_objects(
                    mesh_list=iteration_objects, name='group_%d' % (i % 100))

                # Add to the joint objects list
                joint_objects.append(joint_object)

                # Clear the iteration objects
                iteration_objects.clear()

        # Join the meshes into a group, if @iteration_objects has more than one object
        if len(iteration_objects) > 1:
            joint_object = nmv.mesh.join_mesh_objects(
                mesh_list=iteration_objects, name='group_%d' % (i % 100))

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

        # Create the skeleton materials
        self.create_single_skeleton_materials_list()

        # Updating radii
        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Resample the sections of the morphology skeleton
        self.resample_skeleton_sections()

        # Apical dendrite
        nmv.logger.info('Constructing spheres')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    apical_dendrite_spheres = list()
                    self.draw_sections_as_spheres(
                        root=arbor, name=arbor.label,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        material_list=self.apical_dendrites_materials,
                        sphere_objects=apical_dendrite_spheres)

                    # Link the spheres and shade
                    self.link_and_shade_spheres(sphere_list=apical_dendrite_spheres,
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
                        material_list=self.axons_materials, sphere_objects=axon_spheres)

                    # Link the spheres and shade
                    self.link_and_shade_spheres(sphere_list=axon_spheres,
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
                        material_list=self.basal_dendrites_materials,
                        sphere_objects=basal_dendrites_spheres)

                    # Link the spheres and shade
                    self.link_and_shade_spheres(sphere_list=basal_dendrites_spheres,
                                                materials_list=self.basal_dendrites_materials,
                                                prefix=arbor.label)
        # Draw the soma
        self.draw_soma()

        # Draw every endfoot in the list and append the resulting mesh to the collector
        for endfoot in self.morphology.endfeet:
            self.morphology_objects.append(endfoot.create_surface_patch(material=self.endfeet_materials[0]))

        # Transforming to global coordinates
        self.transform_to_global_coordinates()

        # Return the list of the drawn morphology objects
        return self.morphology_objects
