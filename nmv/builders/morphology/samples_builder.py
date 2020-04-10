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
import nmv.mesh
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.geometry
import nmv.scene
import nmv.bmeshi
import nmv.shading


####################################################################################################
# @SamplesBuilder
####################################################################################################
class SamplesBuilder:
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

        # Morphology
        self.morphology = copy.deepcopy(morphology)

        # System options
        self.options = copy.deepcopy(options)

        # All the reconstructed objects of the morphology, for example, poly-lines, spheres etc...
        self.morphology_objects = []

        # A list of the colors/materials of the soma
        self.soma_materials = None

        # A list of the colors/materials of the axon
        self.axons_materials = None

        # A list of the colors/materials of the basal dendrites
        self.basal_dendrites_materials = None

        # A list of the colors/materials of the apical dendrite
        self.apical_dendrites_materials = None

        # A list of the colors/materials of the articulation spheres
        self.articulations_materials = None

        # An aggregate list of all the materials of the skeleton
        self.skeleton_materials = list()

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
        nmv.builders.morphology.create_skeleton_materials_and_illumination(builder=self)

        # Index: 0 - 1
        self.skeleton_materials.extend(self.soma_materials)

        # Index: 2 - 3
        self.skeleton_materials.extend(self.apical_dendrites_materials)

        # Index: 4 - 5
        self.skeleton_materials.extend(self.basal_dendrites_materials)

        # Index: 6 - 7
        self.skeleton_materials.extend(self.axons_materials)

    ################################################################################################
    # @draw_section_samples_as_spheres
    ################################################################################################
    def draw_section_samples_as_spheres(self,
                                        section):
        """Draw the section samples as a set of spheres.

        :param section:
            A given section to draw.
        :return:
            List of spheres of the section.
        """

        output = list()
        for sample in section.samples:
            sphere = nmv.bmeshi.create_ico_sphere(
                radius=sample.radius, location=sample.point, subdivisions=3)
            output.append(sphere)
        return output

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

        # Make sure that the arbor exist
        if root is not None:

            section_name = '%s_%d' % (name, root.id)
            drawn_spheres = self.draw_section_samples_as_spheres(root)

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
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        nmv.logger.header('Building skeleton using SamplesBuilder')

        nmv.logger.info('Updating Radii')
        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Create the skeleton materials
        self.create_single_skeleton_materials_list()

        # Resample the sections of the morphology skeleton
        nmv.builders.morphology.resample_skeleton_sections(builder=self)

        # Apical dendrite
        nmv.logger.info('Constructing spheres')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.apical_dendrite is not None:
                nmv.logger.detail('Apical dendrite')
                apical_dendrite_spheres = list()
                self.draw_sections_as_spheres(
                    self.morphology.apical_dendrite,
                    name=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX,
                    max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                    material_list=self.apical_dendrites_materials,
                    sphere_objects=apical_dendrite_spheres)

                # Link the spheres and shade
                self.link_and_shade_spheres(sphere_list=apical_dendrite_spheres,
                                            materials_list=self.apical_dendrites_materials,
                                            prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX)

        # Axon
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                nmv.logger.detail('Axon')
                axon_spheres = list()
                self.draw_sections_as_spheres(
                    self.morphology.axon,
                    name=nmv.consts.Skeleton.AXON_PREFIX,
                    max_branching_order=self.options.morphology.axon_branch_order,
                    material_list=self.axons_materials,
                    sphere_objects=axon_spheres)

                # Link the spheres and shade
                self.link_and_shade_spheres(sphere_list=axon_spheres,
                                            materials_list=self.axons_materials,
                                            prefix=nmv.consts.Skeleton.AXON_PREFIX)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for i, basal_dendrite in enumerate(self.morphology.basal_dendrites):
                    nmv.logger.detail('Basal dendrite [%d]' % i)

                    # If the basal dendrites list contains any axons
                    if 'Axon' in basal_dendrite.label:
                        if not self.options.morphology.ignore_axons:
                            basal_dendrites_spheres = list()
                            self.draw_sections_as_spheres(
                                basal_dendrite, name=basal_dendrite.label,
                                max_branching_order=self.options.morphology.axon_branch_order,
                                material_list=self.axons_materials,
                                sphere_objects=basal_dendrites_spheres)

                            # Link the spheres and shade
                            self.link_and_shade_spheres(sphere_list=basal_dendrites_spheres,
                                                        materials_list=self.axons_materials,
                                                        prefix=basal_dendrite.label)

                    # If the basal dendrites list contains any apicals
                    elif 'Apical' in basal_dendrite.label:
                        basal_dendrites_spheres = list()
                        self.draw_sections_as_spheres(
                            basal_dendrite, name=basal_dendrite.label,
                            max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                            material_list=self.apical_dendrites_materials,
                            sphere_objects=basal_dendrites_spheres)

                        # Link the spheres and shade
                        self.link_and_shade_spheres(sphere_list=basal_dendrites_spheres,
                                                    materials_list=self.apical_dendrites_materials,
                                                    prefix=basal_dendrite.label)

                    # This is a basal dendrite
                    else:
                        dendrite_name = '%s_%d' % (nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX, i)
                        basal_dendrites_spheres = list()
                        self.draw_sections_as_spheres(
                            basal_dendrite, name=dendrite_name,
                            max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                            material_list=self.basal_dendrites_materials,
                            sphere_objects=basal_dendrites_spheres)

                        # Link the spheres and shade
                        self.link_and_shade_spheres(sphere_list=basal_dendrites_spheres,
                                                    materials_list=self.basal_dendrites_materials,
                                                    prefix=dendrite_name)
        # Draw the soma
        nmv.builders.morphology.draw_soma(builder=self)

        # Transforming to global coordinates
        nmv.builders.morphology.transform_to_global_coordinates(builder=self)

        # Return the list of the drawn morphology objects
        nmv.logger.info('Done')
        return self.morphology_objects
