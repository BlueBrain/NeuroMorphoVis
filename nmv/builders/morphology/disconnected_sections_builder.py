####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Blender imports
from mathutils import Vector

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
import nmv.rendering
import nmv.utilities


####################################################################################################
# @DisconnectedSectionsBuilder
####################################################################################################
class DisconnectedSectionsBuilder(MorphologyBuilderBase):
    """Builds and draws the morphology as a series of disconnected sections."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options,
                 force_meta_ball_soma=False):
        """Constructor.

        :param morphology:
            A given morphology.
        """

        # Initialize the parent with the common parameters
        MorphologyBuilderBase.__init__(self, morphology, options)

        # A list of all the articulation spheres
        self.articulations_spheres = list()

        # Force using the MetaBalls soma in case loading a new morphology
        self.force_meta_ball = force_meta_ball_soma

    ################################################################################################
    # @construct_color_coded_polylines
    ################################################################################################
    def construct_color_coded_polylines(self,
                                        root,
                                        poly_lines_list=[],
                                        branching_order=0,
                                        max_branching_order=nmv.consts.Math.INFINITY,
                                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX):
        """Constructs color-coded polylines depending on the selected coding schemes.

        :param root:
            a given root section.
        :param poly_lines_list:
            A list that will have the polylines appended to it.
        :param branching_order:
            The current branching order for the recursive operation.
        :param max_branching_order:
            The maximum branching order as selected by the user.
        :param prefix:
            Polyline string prefix.
        """

        # If the section is None, simply return
        if root is None:
            return

        # Increment the branching level
        branching_order += 1

        # Return if we exceed the maximum branching level
        if branching_order > max_branching_order:
            return

        # Coloring scheme
        scheme = self.options.shading.morphology_coloring_scheme

        # Section length
        if scheme == nmv.enums.ColorCoding.BY_LENGTH:

            # Get the minimum and maximum values from the morphology itself
            minimum_value = self.morphology.stats.minimum_section_length
            maximum_value = self.morphology.stats.maximum_section_length

            # Get the index
            material_index = nmv.utilities.get_index(
                value=root.stats.length,
                minimum_value=minimum_value,
                maximum_value=maximum_value,
                number_steps=self.options.shading.morphology_colormap_resolution)

        # Section surface area
        elif scheme == nmv.enums.ColorCoding.BY_SURFACE_AREA:

            # Get the minimum and maximum values from the morphology itself
            minimum_value = self.morphology.stats.minimum_section_surface_area
            maximum_value = self.morphology.stats.maximum_section_surface_area

            # Get the index
            material_index = nmv.utilities.get_index(
                value=root.stats.surface_area,
                minimum_value=minimum_value, maximum_value=maximum_value,
                number_steps=self.options.shading.morphology_colormap_resolution)

        # Section volume
        elif scheme == nmv.enums.ColorCoding.BY_VOLUME:

            # Get the minimum and maximum values from the morphology itself
            minimum_value = self.morphology.stats.minimum_section_volume
            maximum_value = self.morphology.stats.maximum_section_volume

            # Get the index
            material_index = nmv.utilities.get_index(
                value=root.stats.volume,
                minimum_value=minimum_value, maximum_value=maximum_value,
                number_steps=self.options.shading.morphology_colormap_resolution)

        # Number of samples in the section
        elif scheme == nmv.enums.ColorCoding.BY_NUMBER_SAMPLES:

            # Get the minimum and maximum values from the morphology itself
            minimum_value = self.morphology.stats.minimum_number_samples_in_section
            maximum_value = self.morphology.stats.maximum_number_samples_in_section

            # Get the index
            material_index = nmv.utilities.get_index(
                value=root.stats.number_samples,
                minimum_value=minimum_value, maximum_value=maximum_value,
                number_steps=self.options.shading.morphology_colormap_resolution)

        # Alternating colors
        elif scheme == nmv.enums.ColorCoding.ALTERNATING_COLORS:
            minimum_value = 0
            maximum_value = 100
            material_index = 0 if root.index % 2 == 0 else 1

        # Else, just add 0 and 100 for a placeholder in the color map
        else:
            minimum_value = 0
            maximum_value = 100

            # Always use the 0 color index to account for a single color
            material_index = 0

        # Update the interface with the minimum and maximum values for the color-mapping
        if self.context is not None:
            self.context.scene.NMV_MinimumValue = str(minimum_value)
            self.context.scene.NMV_MaximumValue = str(maximum_value)

        # Construct the poly-line
        poly_line = nmv.geometry.PolyLine(
            name='%s_%d' % (prefix, branching_order),
            samples=nmv.skeleton.get_section_poly_line(section=root),
            material_index=material_index)

        # Add the poly-line to the poly-lines list
        poly_lines_list.append(poly_line)

        # Process the children, section by section
        for child in root.children:
            self.construct_color_coded_polylines(root=child,
                                                 poly_lines_list=poly_lines_list,
                                                 branching_order=branching_order,
                                                 max_branching_order=max_branching_order)

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
            material_index = nmv.enums.Color.GRAY_MATERIAL_START_INDEX

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
        section_terminal_sphere = nmv.skeleton.draw_articulation_sphere(
            radius=sphere_radius, point=point)

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
        self.articulations_spheres.append(nmv.skeleton.draw_articulation_sphere(
            radius=root.samples[0].radius, point=root.samples[0].point))

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
    # @draw_each_arbor_as_single_object
    ################################################################################################
    def draw_each_arbor_as_single_object(self,
                                         bevel_object):
        """Draws each arbor as a single object.

         :param bevel_object:
            Bevel object used to interpolate the polylines.
        """

        # Apical dendrite
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor, poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object,
                        materials=self.skeleton_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Axon
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        prefix=nmv.consts.Skeleton.AXON_PREFIX,
                        material_start_index=nmv.enums.Color.AXON_MATERIAL_START_INDEX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object,
                        materials=self.skeleton_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object,
                        materials=self.skeleton_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

    ################################################################################################
    # @draw_arbors_as_single_object
    ################################################################################################
    def draw_arbors_as_single_object(self,
                                     bevel_object):
        """Draws all the arbors as a single object.

        :param bevel_object:
            Bevel object used to interpolate the polylines.
        """

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

    ################################################################################################
    # @draw_arbors
    ################################################################################################
    def draw_arbors(self):
        """Draws the arbors of the morphology."""

        # Apical dendrite
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_color_coded_polylines(
                        root=arbor, poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=self.bevel_object,
                        materials=self.apical_dendrites_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_color_coded_polylines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=self.bevel_object,
                        materials=self.basal_dendrites_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Axon
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_color_coded_polylines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        prefix=nmv.consts.Skeleton.AXON_PREFIX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=self.bevel_object,
                        materials=self.axons_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self,
                                 context=None):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        # Update the context
        self.context = context

        nmv.logger.header('Building skeleton using DisconnectedSectionsBuilder')

        # Initialize the builder
        self.initialize_builder()

        # Draw the arbors
        # self.draw_each_arbor_as_single_object(bevel_object=bevel_object)
        self.draw_arbors()

        # For the articulated sections, draw the spheres
        if self.options.morphology.reconstruction_method == \
                nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
            self.draw_articulations()

        # Draw the soma
        if self.force_meta_ball:
            self.draw_meta_balls_soma()
        else:
            self.draw_soma()

        # Draw the endfeet, if applicable
        self.draw_endfeet_if_applicable()

        # Add the morphology objects to a collection
        self.collection_morphology_objects_in_collection()

        # Return the list of the drawn morphology objects
        return self.morphology_objects

    ################################################################################################
    # @draw_arbors_with_individual_colors
    ################################################################################################
    def draw_arbors_with_individual_colors(self):
        """Draws all the arbors each assigned its own color.

        :return:
            A reference to the morphology objects
        """

        # Clearing the scene
        nmv.scene.clear_scene()

        # Radii
        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology and then hide it
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, resolution=self.options.morphology.bevel_object_sides, name='Cross Section')

        # Add the bevel object to the morphology objects because if this bevel is lost we will
        # lose the rounded structure of the arbors
        # self.morphology_objects.append(bevel_object)

        # Do NOT create the skeleton materials list and instead create the colors on the fly
        # self.create_single_skeleton_materials_list()

        # Soma material
        self.soma_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='soma_skeleton', material_type=self.options.shading.morphology_material,
            color=nmv.consts.Color.BLACK)

        # Resample the sections of the morphology skeleton
        self.resample_skeleton_sections()

        # Apical dendrites
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        prefix=arbor.label,
                        material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX,
                        highlight=False)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object)

                    arbor_material = nmv.shading.create_material(
                        name='%s_material' % arbor.tag, color=arbor.color,
                        material_type=self.options.shading.morphology_material)
                    nmv.shading.set_material_to_object(morphology_object, arbor_material)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        prefix=arbor.label,
                        material_start_index=nmv.enums.Color.AXON_MATERIAL_START_INDEX,
                        highlight=False)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object)

                    arbor_material = nmv.shading.create_material(
                        name='%s_material' % arbor.tag, color=arbor.color,
                        material_type=self.options.shading.morphology_material)
                    nmv.shading.set_material_to_object(morphology_object, arbor_material)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        prefix=arbor.label,
                        material_start_index=nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX,
                        highlight=False)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object)

                    arbor_material = nmv.shading.create_material(
                        name='%s_material' % arbor.tag, color=arbor.color,
                        material_type=self.options.shading.morphology_material)
                    nmv.shading.set_material_to_object(morphology_object, arbor_material)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Draw the soma
        self.draw_soma()

        # Return the list of the drawn morphology objects
        return self.morphology_objects

    ################################################################################################
    # @draw_highlighted_arbor
    ################################################################################################
    def draw_highlighted_arbor(self,
                               highlighted_arbor):
        """Draws a highlighted arbor in the morphology and gray the rest.

        :param highlighted_arbor:
            A reference to the highlighted arbor.
        """

        # Clearing the scene
        nmv.scene.clear_scene()

        nmv.logger.header('Building Skeleton: DisconnectedSectionsBuilder')

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology and then hide it
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, resolution=self.options.morphology.bevel_object_sides, name='Cross Section')

        # Add the bevel object to the morphology objects because if this bevel is lost we will
        # lose the rounded structure of the arbors
        # self.morphology_objects.append(bevel_object)

        # Do NOT create the skeleton materials list and instead creat the colors on the fly
        # self.create_single_skeleton_materials_list()
        global_material = nmv.shading.create_material(
            name='global_material', color=nmv.consts.Color.GREYSH,
            material_type=self.options.shading.morphology_material)

        # Soma material
        self.soma_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='soma_skeleton', material_type=self.options.shading.morphology_material,
            color=nmv.consts.Color.BLACK)

        # Updating radii
        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Resample the sections of the morphology skeleton
        self.resample_skeleton_sections()

        # Apical dendrites
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        prefix=arbor.label,
                        material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX,
                        highlight=False)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object)

                    if arbor.tag == highlighted_arbor.tag:
                        arbor_material = nmv.shading.create_material(
                            name='%s_material' % arbor.tag, color=arbor.color,
                            material_type=self.options.shading.morphology_material)
                        nmv.shading.set_material_to_object(morphology_object, arbor_material)
                    else:
                        nmv.shading.set_material_to_object(morphology_object, global_material)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        prefix=arbor.label,
                        material_start_index=nmv.enums.Color.AXON_MATERIAL_START_INDEX,
                        highlight=False)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object)

                    if arbor.tag == highlighted_arbor.tag:
                        arbor_material = nmv.shading.create_material(
                            name='%s_material' % arbor.tag, color=arbor.color,
                            material_type=self.options.shading.morphology_material)
                        nmv.shading.set_material_to_object(morphology_object, arbor_material)
                    else:
                        nmv.shading.set_material_to_object(morphology_object, global_material)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        prefix=arbor.label,
                        material_start_index=nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX,
                        highlight=False)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object)

                    if arbor.tag == highlighted_arbor.tag:
                        arbor_material = nmv.shading.create_material(
                            name='%s_material' % arbor.tag, color=arbor.color,
                            material_type=self.options.shading.morphology_material)
                        nmv.shading.set_material_to_object(morphology_object, arbor_material)
                    else:
                        nmv.shading.set_material_to_object(morphology_object, global_material)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Draw the soma
        self.draw_soma()

        # Return the list of the drawn morphology objects
        return self.morphology_objects

    ################################################################################################
    # @render_highlighted_arbors
    ################################################################################################
    def render_highlighted_arbors(self,
                                  image_resolution=3000):
        """Render the morphology with different colors per arbor for analysis.

        @param image_resolution:
            The rendering resolution of the resulting images. Default 3000 pixels.
        """

        # NOTE: Readjust the parameters here to plot everything for the whole morphology
        self.options.morphology.adjust_to_analysis_mode()

        # Draw the whole morphology with individual colors, but to-scale
        self.options.shading.morphology_material = nmv.enums.Shader.FLAT
        self.draw_arbors_with_individual_colors()

        bounding_box = nmv.skeleton.compute_full_morphology_bounding_box(
            morphology=self.morphology)

        # Original skeleton ########################################################################
        # Render the image at different projections
        for view, suffix in zip([nmv.enums.Camera.View.FRONT,
                                 nmv.enums.Camera.View.SIDE,
                                 nmv.enums.Camera.View.TOP],
                                ['front', 'side', 'top']):

            nmv.rendering.render(
                bounding_box=bounding_box,
                camera_view=view,
                image_resolution=image_resolution,
                image_name='%s_%s' % (self.morphology.label, suffix),
                image_directory='%s/%s' % (self.options.io.analysis_directory,
                                           self.options.morphology.label))

        # Clear the scene
        nmv.scene.clear_scene()

        # Unified radius skeleton ##################################################################
        # Set the arbors radii to be fixed to 1.0
        self.options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.UNIFIED
        largest_dimension = self.morphology.bounding_box.get_largest_dimension()
        self.options.morphology.samples_unified_radii_value = largest_dimension / 1000.0

        # Apical dendrites
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.scene.clear_scene()
                    self.draw_highlighted_arbor(highlighted_arbor=arbor)

                    # Render the image
                    nmv.rendering.render(
                        bounding_box=bounding_box,
                        camera_view=nmv.enums.Camera.View.FRONT,
                        image_resolution=image_resolution,
                        image_name='arbor_%s' % arbor.tag,
                        image_directory='%s/%s' % (self.options.io.analysis_directory,
                                                   self.options.morphology.label))

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.scene.clear_scene()
                    self.draw_highlighted_arbor(highlighted_arbor=arbor)

                    # Render the image
                    nmv.rendering.render(
                        bounding_box=bounding_box,
                        camera_view=nmv.enums.Camera.View.FRONT,
                        image_resolution=image_resolution,
                        image_name='arbor_%s' % arbor.tag,
                        image_directory='%s/%s' % (self.options.io.analysis_directory,
                                                   self.options.morphology.label))

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.scene.clear_scene()
                    self.draw_highlighted_arbor(highlighted_arbor=arbor)

                    # Render the image
                    nmv.rendering.render(
                        bounding_box=bounding_box,
                        camera_view=nmv.enums.Camera.View.FRONT,
                        image_resolution=image_resolution,
                        image_name='arbor_%s' % arbor.tag,
                        image_directory='%s/%s' % (self.options.io.analysis_directory,
                                                   self.options.morphology.label))

        # Projections ##############################################################################

        # To draw the projections to scale, we must compute the radii based on extents
        # Get the largest dimension of the bounding box of the morphology
        largest_dimension = self.morphology.bounding_box.get_largest_dimension()
        self.options.morphology.samples_unified_radii_value = largest_dimension / 1000.0

        # Draw the whole morphology with individual colors
        self.draw_arbors_with_individual_colors()

        # Render the image at different projections
        for view, suffix in zip([nmv.enums.Camera.View.FRONT,
                                 nmv.enums.Camera.View.SIDE,
                                 nmv.enums.Camera.View.TOP],
                             ['front%s' % nmv.consts.Suffix.FIXED_RADIUS,
                              'side%s' % nmv.consts.Suffix.FIXED_RADIUS,
                              'top%s' % nmv.consts.Suffix.FIXED_RADIUS]):
            nmv.rendering.render(
                bounding_box=bounding_box,
                camera_view=view,
                image_resolution=image_resolution,
                image_name='%s_%s' % (self.morphology.label, suffix),
                image_directory='%s/%s' % (self.options.io.analysis_directory,
                                           self.options.morphology.label))

        # Clear the scene
        nmv.scene.clear_scene()
