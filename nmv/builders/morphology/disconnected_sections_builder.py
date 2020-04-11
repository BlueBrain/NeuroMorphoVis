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

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Internal imports
import nmv.mesh
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.geometry
import nmv.scene
import nmv.bmeshi
import nmv.shading
import nmv.rendering


####################################################################################################
# @DisconnectedSectionsBuilder
####################################################################################################
class DisconnectedSectionsBuilder:
    """Builds and draws the morphology as a series of disconnected sections.
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

        # A gray material to highlight the other arbors in colors
        self.gray_material = None

        # A list of all the articulation spheres - to be converted from bmesh to mesh to save time
        self.articulations_spheres = list()

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

        # Clear teh materials list
        self.skeleton_materials.clear()

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

        # Index 8 for the gray color
        self.skeleton_materials.extend(nmv.skeleton.ops.create_skeleton_materials(
            name='gray', material_type=self.options.shading.morphology_material,
            color=Vector((0.5, 0.5, 0.5))))

    ################################################################################################
    # @construct_tree_poly_lines
    ################################################################################################
    def construct_tree_poly_lines(self,
                                  root,
                                  poly_lines_list=[],
                                  branching_order=0,
                                  max_branching_order=nmv.consts.Math.INFINITY,
                                  prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
                                  material_start_index=0,
                                  highlight=True):
        """Creates a list of poly-lines corresponding to all the sections in the given tree.

        :param root:
            Arbor root, or children sections.
        :param poly_lines_list:
            A list that will combine all the constructed poly-lines.
        :param branching_order:
            Current branching level of the arbor.
        :param max_branching_order:
            The maximum branching level given by the user.
        :param prefix:
            The prefix that is prepended to the name of the poly-line.
        :param material_start_index:
            An index that indicates which material to be used for which arbor.
        :param highlight:
            Highlight the given arbor.
        """

        # If the section is None, simply return
        if root is None:
            return

        # Increment the branching level
        branching_order += 1

        # Return if we exceed the maximum branching level
        if branching_order > max_branching_order:
            return

        # Adjust the material
        if highlight:
            material_index = material_start_index + (branching_order % 2)
        else:
            material_index = nmv.enums.Color.GRAY_MATERIAL_INDEX

        # Construct the poly-line
        poly_line = nmv.geometry.PolyLine(
            name='%s_%d' % (prefix, branching_order),
            samples=nmv.skeleton.get_section_poly_line(section=root),
            material_index=material_index)

        # Add the poly-line to the poly-lines list
        poly_lines_list.append(poly_line)

        # Process the children, section by section
        for child in root.children:
            self.construct_tree_poly_lines(root=child,
                                           poly_lines_list=poly_lines_list,
                                           branching_order=branching_order,
                                           max_branching_order=max_branching_order,
                                           material_start_index=material_start_index,
                                           highlight=highlight)

    ################################################################################################
    # @draw_section_terminal_as_sphere
    ################################################################################################
    def draw_section_terminal_as_sphere(self,
                                        section):
        """Draws a joint between the different sections along the arbor.

        :param section:
            Section geometry.
        """

        # Get the section data arranged in a poly-line format
        section_data = nmv.skeleton.ops.get_section_poly_line(section)

        # Access the last item
        section_terminal = section_data[-1]

        # Get a Vector(()) for the coordinates of the terminal
        point = section_terminal[0]
        point = Vector((point[0], point[1], point[2]))

        # Get terminal radius
        radius = section_terminal[1]

        # Get the radius for the first samples of the children and use it if it's bigger than the
        # radius of the last sample of the parent terminal.
        for child in section.children:

            # Get the first sample along the child section
            child_data = nmv.skeleton.ops.get_section_poly_line(child)

            # Verify the radius of the child
            child_radius = child_data[0][1]

            # If the radius of the child is bigger, then set the radius of the joint to the
            # radius of the child
            if child_radius > radius:
                radius = child_radius

        # If we scale the morphology, we should account for that in the spheres to
        sphere_radius = radius
        if self.options.morphology.arbors_radii == nmv.enums.Skeleton.Radii.SCALED:
            sphere_radius *= self.options.morphology.sections_radii_scale
        elif self.options.morphology.arbors_radii == nmv.enums.Skeleton.Radii.UNIFIED:
            sphere_radius = self.options.morphology.samples_unified_radii_value

        # Create the sphere based on the largest radius
        section_terminal_sphere = nmv.bmeshi.create_ico_sphere(
            sphere_radius * 1.025, location=point, subdivisions=3)

        # Add the created bmesh sphere to the list
        self.articulations_spheres.append(section_terminal_sphere)

    ################################################################################################
    # @draw_section_as_disconnected_segments
    ################################################################################################
    def draw_section_terminals_as_spheres(self,
                                          root,
                                          material_list=None,
                                          branching_order=0,
                                          max_branching_order=nmv.consts.Math.INFINITY):
        """Draws the terminals of a given arbor as spheres.

        :param root:
            Arbor root.
        :param material_list:
            Sphere material.
        :param branching_order:
            Current branching level.
        :param max_branching_order:
            Maximum branching level the section can grow up to: infinity.
        """

        # Ignore the drawing if the root section is None
        if root is None:
            return

        # Draw the root sample as a sphere
        self.articulations_spheres.append(nmv.bmeshi.create_ico_sphere(
            root.samples[0].radius * 1.025, location=root.samples[0].point, subdivisions=3))

        # Increment the branching level
        branching_order += 1

        # Stop drawing at the maximum branching level
        if branching_order > max_branching_order:
            return

        # Make sure that the arbor exist
        if root is not None:

            # Draw the section terminal sphere
            self.draw_section_terminal_as_sphere(root)

            # Draw the children sections
            for child in root.children:
                self.draw_section_terminals_as_spheres(
                    child, material_list=material_list,
                    branching_order=branching_order, max_branching_order=max_branching_order)

    ################################################################################################
    # @link_and_shade_articulation_spheres
    ################################################################################################
    def link_and_shade_articulation_spheres(self):
        """Links the articulation spheres to the scene.
        """

        joint_bmesh = nmv.bmeshi.join_bmeshes_list(bmeshes_list=self.articulations_spheres)

        # Link the bmesh spheres to the scene
        articulations_spheres = nmv.bmeshi.ops.link_to_new_object_in_scene(
            joint_bmesh, '%s_articulations' % self.morphology.label)

        # Smooth shading
        nmv.mesh.shade_smooth_object(articulations_spheres)

        # Assign the material
        nmv.shading.set_material_to_object(articulations_spheres, self.articulations_materials[0])

        # Append the sphere mesh to the morphology objects
        self.morphology_objects.append(articulations_spheres)

    ################################################################################################
    # @draw_section_as_disconnected_segments
    ################################################################################################
    def draw_articulations(self):
        """Draws the articulations at the branching points.
        """

        # Draw the axon joints
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    self.draw_section_terminals_as_spheres(
                        root=arbor,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        material_list=self.articulations_materials)

        # Draw the basal dendrites joints
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    self.draw_section_terminals_as_spheres(
                        root=arbor,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        material_list=self.articulations_materials)

        # Draw the apical dendrites joints
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    self.draw_section_terminals_as_spheres(
                        root=arbor,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        material_list=self.articulations_materials)

        # Link and shade the articulation spheres
        self.link_and_shade_articulation_spheres()

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        nmv.logger.header('Building skeleton using DisconnectedSectionsBuilder')

        nmv.logger.info('Updating radii')
        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology and then hide it
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')
        nmv.scene.hide_object(bevel_object)

        # Add the bevel object to the morphology objects because if this bevel is lost we will
        # lose the rounded structure of the arbors
        self.morphology_objects.append(bevel_object)

        # Create the skeleton materials
        self.create_single_skeleton_materials_list()

        # Resample the sections of the morphology skeleton
        nmv.builders.morphology.resample_skeleton_sections(builder=self)

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        # Apical dendrite
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor, poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX)

        # Axon
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        prefix=nmv.consts.Skeleton.AXON_PREFIX,
                        material_start_index=nmv.enums.Color.AXON_MATERIAL_START_INDEX)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX)

        # Draw the poly-lines as a single object
        morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=self.morphology.label,
            edges=self.options.morphology.edges, bevel_object=bevel_object,
            materials=self.skeleton_materials)

        # Append it to the morphology objects
        self.morphology_objects.append(morphology_object)

        # For the articulated sections, draw the spheres
        if self.options.morphology.reconstruction_method == \
                nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
            self.draw_articulations()

        # Draw the soma
        nmv.builders.morphology.draw_soma(builder=self)

        # Transforming to global coordinates
        nmv.builders.morphology.transform_to_global_coordinates(builder=self)

        # Return the list of the drawn morphology objects
        nmv.logger.info('Done')
        return self.morphology_objects

    ################################################################################################
    # @draw_highlighted_arbor
    ################################################################################################
    def draw_highlighted_arbor(self,
                               highlighted_arbor_key):
        """Draws a highlighted arbor in the morphology and gray the rest.

        :param highlighted_arbor_key:
            The color code key.
        """

        # Clearing the scene
        nmv.scene.clear_scene()

        nmv.logger.header('Building skeleton using DisconnectedSectionsBuilder')

        nmv.logger.info('Updating Radii')
        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology and then hide it
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')
        nmv.scene.hide_object(bevel_object)

        # Add the bevel object to the morphology objects because if this bevel is lost we will
        # lose the rounded structure of the arbors
        self.morphology_objects.append(bevel_object)

        # Create the skeleton materials
        self.create_single_skeleton_materials_list()

        # Resample the sections of the morphology skeleton
        nmv.builders.morphology.resample_skeleton_sections(builder=self)

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        # Apical dendrite
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for i, arbor in enumerate(self.morphology.apical_dendrites):
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX,
                        highlight=True if highlighted_arbor_key == 'color_apical_%d' % i else False)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for i, arbor in enumerate(self.morphology.axons):
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.AXON_MATERIAL_START_INDEX,
                        highlight=True if highlighted_arbor_key == 'color_axon_%d' % i else False)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for i, arbor in enumerate(self.morphology.basal_dendrites):
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        prefix=nmv.consts.Skeleton.AXON_PREFIX,
                        material_start_index=nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX,
                        highlight=True if highlighted_arbor_key == 'color_basal_%d' % i else False)

        # Draw the poly-lines as a single object
        morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=self.morphology.label,
            edges=self.options.morphology.edges, bevel_object=bevel_object,
            materials=self.skeleton_materials)

        # Append it to the morphology objects
        self.morphology_objects.append(morphology_object)

        # For the articulated sections, draw the spheres
        if self.options.morphology.reconstruction_method == \
                nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
            self.draw_articulations()

        # Draw the soma
        nmv.builders.morphology.draw_soma(builder=self)

        # Transforming to global coordinates
        nmv.builders.morphology.transform_to_global_coordinates(builder=self)

        # Return the list of the drawn morphology objects
        nmv.logger.info('Done')
        return self.morphology_objects

    ################################################################################################
    # @render_highlighted_arbors
    ################################################################################################
    def render_highlighted_arbors(self):

        # Set the arbors radii to be fixed to 1.0
        self.options.shading.material = nmv.enums.Shader.FLAT
        self.options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.UNIFIED
        self.options.morphology.samples_unified_radii_value = 1.0

        bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
            morphology=self.morphology)

        images = list()

        # Apical dendrites
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for i, arbor in self.morphology.apical_dendrites:
                    self.draw_highlighted_arbor(highlighted_arbor_key='color_apical_%d' % i)

                    # Render the image
                    nmv.rendering.render_to_scale(
                        bounding_box=bounding_box,
                        camera_view=nmv.enums.Camera.View.FRONT,
                        image_scale_factor=2,
                        image_name='%s_%s' % (self.options.morphology.label, 'apical_%d' % i),
                        image_directory=self.options.io.analysis_directory)

                    images.append('%s/%s_%s' % (self.options.io.analysis_directory,
                                                self.options.morphology.label, 'apical'))

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for i, arbor in enumerate(self.morphology.axons):
                    self.draw_highlighted_arbor(highlighted_arbor_key='color_axon_%d' % i)

                    # Render the image
                    nmv.rendering.render_to_scale(
                        bounding_box=bounding_box,
                        camera_view=nmv.enums.Camera.View.FRONT,
                        image_scale_factor=2,
                        image_name='%s_%s' % (self.options.morphology.label, 'axon_%d' % i),
                        image_directory=self.options.io.analysis_directory)

                    images.append('%s/%s_%s' % (self.options.io.analysis_directory,
                                                self.options.morphology.label, 'axon'))

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for i, basal_dendrite in enumerate(self.morphology.basal_dendrites):
                    self.draw_highlighted_arbor(highlighted_arbor_key='color_basal_%d' % i)

                    # render
                    # Render the image
                    nmv.rendering.render_to_scale(
                        bounding_box=bounding_box,
                        camera_view=nmv.enums.Camera.View.FRONT,
                        image_scale_factor=2,
                        image_name='%s_%s' % (self.options.morphology.label, 'basal_%d' % i),
                        image_directory=self.options.io.analysis_directory)

                    images.append('%s/%s_%s' % (self.options.io.analysis_directory,
                                                self.options.morphology.label, 'basal_%d' % i))