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
import nmv.shading
import nmv.utilities


####################################################################################################
# @DisconnectedSegmentsBuilder
####################################################################################################
class DisconnectedSegmentsBuilder(MorphologyBuilderBase):
    """Builds and draws the morphology as a series of disconnected segments for analysis."""

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
            Arbor root, or children sections.
        :param poly_lines_list:
            A list that will combine all the constructed poly-lines.
        :param branching_order:
            Current branching level of the arbor.
        :param max_branching_order:
            The maximum branching level given by the user.
        :param prefix:
            The prefix that is prepended to the name of the poly-line.
        """

        # If the section is None, simply return
        if root is None:
            return

        # Increment the branching level
        branching_order += 1

        # Return if we exceed the maximum branching level
        if branching_order > max_branching_order:
            return

        # Get a reference to the coloring scheme
        scheme = self.options.shading.morphology_coloring_scheme

        # Segment length
        if scheme == nmv.enums.ColorCoding.BY_LENGTH:

            # Get the minimum and maximum values from the morphology itself
            minimum_value = self.morphology.stats.minimum_segment_length
            maximum_value = self.morphology.stats.maximum_segment_length
            # Construct the segments polylines
            for i in range(len(root.samples) - 1):

                # Reference to the original segment samples
                sample_1 = root.samples[i]
                sample_2 = root.samples[i + 1]

                # Get the index
                material_index = nmv.utilities.get_index(
                    value=nmv.skeleton.compute_segment_length(sample_1, sample_2),
                    minimum_value=minimum_value, maximum_value=maximum_value,
                    number_steps=self.options.shading.morphology_colormap_resolution)

                # Construct the polyline and append it to the polyline to the polylines list
                poly_lines_list.append(nmv.geometry.PolyLine(
                    name='%s_%d_%d' % (prefix, branching_order, i),
                    samples=nmv.skeleton.get_polyline_samples_from_segment(sample_1, sample_2),
                    material_index=material_index))

        elif scheme == nmv.enums.ColorCoding.DISTANCE_FROM_SOMA:

            # Get the minimum and maximum values from the morphology itself
            minimum_value = 0
            maximum_value = self.morphology.stats.maximum_path_distance

            # Construct the segments polylines
            for i in range(len(root.samples) - 1):

                # Reference to the original segment samples
                sample_1 = root.samples[i]
                sample_2 = root.samples[i + 1]

                # Get the index
                material_index = nmv.utilities.get_index(
                    value=nmv.skeleton.compute_path_distance_to_segment(
                        segment_index=i, section=root),
                    minimum_value=minimum_value, maximum_value=maximum_value,
                    number_steps=self.options.shading.morphology_colormap_resolution)

                # Construct the polyline and append it to the polyline to the polylines list
                poly_lines_list.append(nmv.geometry.PolyLine(
                    name='%s_%d_%d' % (prefix, branching_order, i),
                    samples=nmv.skeleton.get_polyline_samples_from_segment(sample_1, sample_2),
                    material_index=material_index))

        elif scheme == nmv.enums.ColorCoding.EUCLIDEAN_DISTANCE:

            # Get the minimum and maximum values from the morphology itself
            minimum_value = 0
            maximum_value = self.morphology.stats.maximum_euclidean_distance

            # Construct the segments polylines
            for i in range(len(root.samples) - 1):

                # Reference to the original segment samples
                sample_1 = root.samples[i]
                sample_2 = root.samples[i + 1]

                # Get the index
                material_index = nmv.utilities.get_index(
                    value=nmv.skeleton.compute_euclidean_distance_to_segment(sample_1, sample_2),
                    minimum_value=minimum_value, maximum_value=maximum_value,
                    number_steps=self.options.shading.morphology_colormap_resolution)

                # Construct the polyline and append it to the polyline to the polylines list
                poly_lines_list.append(nmv.geometry.PolyLine(
                    name='%s_%d_%d' % (prefix, branching_order, i),
                    samples=nmv.skeleton.get_polyline_samples_from_segment(sample_1, sample_2),
                    material_index=material_index))

        # Segment radius
        elif scheme == nmv.enums.ColorCoding.BY_RADIUS:

            # Get the minimum and maximum values from the morphology itself
            minimum_value = self.morphology.stats.minimum_sample_radius
            maximum_value = self.morphology.stats.maximum_sample_radius

            # Construct the segments polylines
            for i in range(len(root.samples) - 1):

                # Reference to the original segment samples
                sample_1 = root.samples[i]
                sample_2 = root.samples[i + 1]

                # Get the index
                material_index = nmv.utilities.get_index(
                    value=nmv.skeleton.compute_segment_radius(sample_1, sample_2),
                    minimum_value=minimum_value, maximum_value=maximum_value,
                    number_steps=self.options.shading.morphology_colormap_resolution)

                # Construct the polyline and append it to the polyline to the polylines list
                poly_lines_list.append(nmv.geometry.PolyLine(
                    name='%s_%d_%d' % (prefix, branching_order, i),
                    samples=nmv.skeleton.get_polyline_samples_from_segment(sample_1, sample_2),
                    material_index=material_index))

        # Segment surface area
        elif scheme == nmv.enums.ColorCoding.BY_SURFACE_AREA:

            # Get the minimum and maximum values from the morphology itself
            minimum_value = self.morphology.stats.minimum_segment_surface_area
            maximum_value = self.morphology.stats.maximum_segment_surface_area

            # Construct the segments polylines
            for i in range(len(root.samples) - 1):

                # Reference to the original segment samples
                sample_1 = root.samples[i]
                sample_2 = root.samples[i + 1]

                # Get the index
                material_index = nmv.utilities.get_index(
                    value=nmv.skeleton.compute_segment_surface_area(sample_1, sample_2),
                    minimum_value=minimum_value, maximum_value=maximum_value,
                    number_steps=self.options.shading.morphology_colormap_resolution)

                # Construct the polyline and append it to the polyline to the polylines list
                poly_lines_list.append(nmv.geometry.PolyLine(
                    name='%s_%d_%d' % (prefix, branching_order, i),
                    samples=nmv.skeleton.get_polyline_samples_from_segment(sample_1, sample_2),
                    material_index=material_index))

        # Segment volume
        elif scheme == nmv.enums.ColorCoding.BY_VOLUME:

            # Get the minimum and maximum values from the morphology itself
            minimum_value = self.morphology.stats.minimum_segment_volume
            maximum_value = self.morphology.stats.maximum_segment_volume

            # Construct the segments polylines
            for i in range(len(root.samples) - 1):

                # Reference to the original segment samples
                sample_1 = root.samples[i]
                sample_2 = root.samples[i + 1]

                # Get the index
                material_index = nmv.utilities.get_index(
                    value=nmv.skeleton.compute_segment_volume(sample_1, sample_2),
                    minimum_value=minimum_value, maximum_value=maximum_value,
                    number_steps=self.options.shading.morphology_colormap_resolution)

                # Construct the polyline and append it to the polyline to the polylines list
                poly_lines_list.append(nmv.geometry.PolyLine(
                    name='%s_%d_%d' % (prefix, branching_order, i),
                    samples=nmv.skeleton.get_polyline_samples_from_segment(sample_1, sample_2),
                    material_index=material_index))

        # Segment volume
        elif scheme == nmv.enums.ColorCoding.ALTERNATING_COLORS:
            minimum_value = 0
            maximum_value = 100

            # Construct the segments polylines
            for i in range(len(root.samples) - 1):

                # Reference to the original segment samples
                sample_1 = root.samples[i]
                sample_2 = root.samples[i + 1]

                # Construct the polyline and append it to the polyline to the polylines list
                poly_lines_list.append(nmv.geometry.PolyLine(
                    name='%s_%d_%d' % (prefix, branching_order, i),
                    samples=nmv.skeleton.get_polyline_samples_from_segment(sample_1, sample_2),
                    material_index=i % 2))

        # Single color
        else:

            minimum_value = 0
            maximum_value = 100

            # Construct the segments polylines
            for i in range(len(root.samples) - 1):

                # Reference to the original segment samples
                sample_1 = root.samples[i]
                sample_2 = root.samples[i + 1]

                if i % 2 == 0:
                    material_index = 0
                else:
                    material_index = 1

                # Construct the polyline and append it to the polyline to the polylines list
                poly_lines_list.append(nmv.geometry.PolyLine(
                    name='%s_%d_%d' % (prefix, branching_order, i),
                    samples=nmv.skeleton.get_polyline_samples_from_segment(sample_1, sample_2),
                    material_index=material_index))

        # Update the interface with the minimum and maximum values for the color-mapping
        if self.context is not None:
            self.context.scene.NMV_MinimumValue = str('%.2f' % minimum_value)
            self.context.scene.NMV_MaximumValue = str('%.2f' % maximum_value)

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
                                  material_start_index=0):
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
        """

        # If the section is None, simply return
        if root is None:
            return

        # Increment the branching level
        branching_order += 1

        # Return if we exceed the maximum branching level
        if branching_order > max_branching_order:
            return

        # Get a list of segments poly-lines samples
        segments_poly_lines = nmv.skeleton.get_segments_poly_lines(section=root)

        # Construct the poly-line
        for i, segment_poly_line in enumerate(segments_poly_lines):
            poly_line = nmv.geometry.PolyLine(
                name='%s_%d_%d' % (prefix, branching_order, i),
                samples=segment_poly_line,
                material_index=material_start_index + (i % 2))

            # Add the poly-line to the poly-lines list
            poly_lines_list.append(poly_line)

        # Process the children, section by section
        for child in root.children:
            self.construct_tree_poly_lines(root=child,
                                           poly_lines_list=poly_lines_list,
                                           branching_order=branching_order,
                                           max_branching_order=max_branching_order,
                                           material_start_index=material_start_index)

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

        # Apical dendrites
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
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
    def draw_arbors(self,
                    bevel_object):

        # Apical dendrites
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_color_coded_polylines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object,
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
                        edges=self.options.morphology.edges, bevel_object=bevel_object,
                        materials=self.basal_dendrites_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_color_coded_polylines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object,
                        materials=self.axons_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

    ################################################################################################
    # @draw_each_arbor_as_single_object
    ################################################################################################
    def draw_each_arbor_as_single_object(self,
                                         bevel_object):
        """Draws each arbor as a single object.

         :param bevel_object:
            Bevel object used to interpolate the polylines.
        """

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
                        prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object,
                        materials=self.skeleton_materials)

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
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
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

        nmv.logger.header('Building Skeleton: DisconnectedSegmentsBuilder')

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology and then hide it
        bevel_object = self.create_bevel_object()

        # Add the bevel object to the morphology objects because if this bevel is lost we will
        # lose the rounded structure of the arbors
        self.morphology_objects.append(bevel_object)

        # Create the skeleton materials
        self.create_single_skeleton_materials_list()

        # Updating radii
        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Resample the sections of the morphology skeleton
        self.resample_skeleton_sections()

        self.create_base_skeleton_materials()

        self.draw_arbors(bevel_object=bevel_object)

        # Draws each arbor in the morphology as a single object
        # self.draw_each_arbor_as_single_object(bevel_object=bevel_object)

        # Draw the soma
        self.draw_soma()

        # Draw every endfoot in the list and append the resulting mesh to the collector
        for endfoot in self.morphology.endfeet:
            self.morphology_objects.append(endfoot.create_surface_patch(material=self.endfeet_materials[0]))

        # Transforming to global coordinates
        self.transform_to_global_coordinates()

        # Add the morphology objects to a collection
        self.collection_morphology_objects_in_collection()

        # Return the list of the drawn morphology objects
        return self.morphology_objects
