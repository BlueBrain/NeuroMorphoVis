####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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
import bpy

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
import nmv.analysis


####################################################################################################
# @ProgressiveBuilder
####################################################################################################
class ProgressiveBuilder(MorphologyBuilderBase):
    """Builds and draws the morphology as a series of disconnected sections like the
    DisconnectedSectionsBuilder, but PROGRESSIVELY."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options,
                 disable_illumination=False):
        """Constructor.

        :param morphology:
            A given morphology.
        :param options:
            NeuroMorphoVis option.
        """

        # Initialize the parent with the common parameters
        MorphologyBuilderBase.__init__(self, morphology, options, disable_illumination)

        # A list of all the articulation spheres - to be converted from bmesh to mesh to save time
        self.articulations_spheres = list()

    ################################################################################################
    # @construct_arbors_poly_lines_list_at_branching_order
    ################################################################################################
    def construct_arbors_poly_lines_list_at_branching_order(self,
                                                            root,
                                                            branching_order,
                                                            poly_lines_list=[],
                                                            prefix='Arbor',
                                                            material_start_index=0):
        """Creates a list of poly-lines corresponding to all the sections in the given tree.

        :param root:
            Arbor root, or children sections.
        :param poly_lines_list:
            A list that will combine all the constructed poly-lines.
        :param branching_order:
            The specific branching order to construct the poly-lines at.
        :param prefix:
            The prefix that is prepended to the name of the poly-line.
        :param material_start_index:
            An index that indicates which material to be used for which arbor.
        """

        # If the section is None, simply return
        if root is None:
            return

        # If the branching order is already greater than that of the current section, simply return
        if branching_order < root.branching_order:
            return

        # If the branching order is less than that of the current section, then process the children
        if branching_order > root.branching_order:
            for child in root.children:
                self.construct_arbors_poly_lines_list_at_branching_order(
                    root=child, branching_order=branching_order, poly_lines_list=poly_lines_list,
                    material_start_index=material_start_index)

        # If this is what we are looking for, construct the poly-line, add it to the list and return
        if branching_order == root.branching_order:
            # Construct the poly-line
            poly_line = nmv.geometry.PolyLine(
                name='%s_%d' % (prefix, root.branching_order),
                samples=nmv.skeleton.get_section_poly_line(section=root),
                material_index=material_start_index + (root.branching_order % 2))

            # Add the poly-line to the poly-lines list
            poly_lines_list.append(poly_line)

            # We are done, return
            return

    ################################################################################################
    # @construct_morphology_poly_lines_list_at_branching_order
    ################################################################################################
    def construct_morphology_poly_lines_list_at_branching_order(self,
                                                                branching_order):
        """Constructing polylines of the morphology at a given branching order.

        :param branching_order:
            Maximum branching order.
        """
        poly_lines_list = list()

        # Apical dendrites
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                if branching_order < self.options.morphology.apical_dendrite_branch_order:
                    for arbor in self.morphology.apical_dendrites:
                        self.construct_arbors_poly_lines_list_at_branching_order(
                            root=arbor,
                            branching_order=branching_order,
                            poly_lines_list=poly_lines_list,
                            prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX,
                            material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                if branching_order < self.options.morphology.axon_branch_order:
                    for arbor in self.morphology.axons:
                        self.construct_arbors_poly_lines_list_at_branching_order(
                            root=arbor,
                            branching_order=branching_order,
                            poly_lines_list=poly_lines_list,
                            prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
                            material_start_index=nmv.enums.Color.AXON_MATERIAL_START_INDEX)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                if branching_order < self.options.morphology.basal_dendrites_branch_order:
                    for arbor in self.morphology.basal_dendrites:
                        self.construct_arbors_poly_lines_list_at_branching_order(
                            root=arbor,
                            branching_order=branching_order,
                            poly_lines_list=poly_lines_list,
                            prefix=nmv.consts.Skeleton.AXON_PREFIX,
                            material_start_index=nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX)

        return poly_lines_list

    ################################################################################################
    # @draw_arbors_progressively
    ################################################################################################
    def draw_arbors_progressively(self):
        """Draws the arbors of the morphology in a progressive fashion."""

        # The maximum branching order of the morphology
        morphology_maximum_branching_order = \
            nmv.analysis.kernel_maximum_branching_order(self.morphology).morphology_result

        for i in range(1, morphology_maximum_branching_order):
            skeleton_poly_lines = self.construct_morphology_poly_lines_list_at_branching_order(i)

            # Draw only the lists that contain any data
            if len(skeleton_poly_lines) > 0:
                starting_frame = i * 10
                ending_frame = (i + 1) * 10

                # Draw the poly-lines as a single object
                drawn_poly_lines = nmv.geometry.draw_poly_lines_in_single_object(
                    poly_lines=skeleton_poly_lines,
                    object_name='%s_%d' % (self.morphology.label, i),
                    edges=self.options.morphology.edges,
                    bevel_object=self.bevel_object,
                    materials=self.skeleton_materials)

                drawn_poly_lines.data.bevel_factor_end = 0.0
                drawn_poly_lines.data.keyframe_insert(data_path="bevel_factor_end", index=-1,
                                                      frame=starting_frame)

                drawn_poly_lines.data.bevel_factor_end = 1.0
                drawn_poly_lines.data.keyframe_insert(data_path="bevel_factor_end", index=-1,
                                                      frame=ending_frame)

                # Append it to the morphology objects
                self.morphology_objects.append(drawn_poly_lines)

                bpy.context.scene.frame_end = ending_frame

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self,
                                 context=None):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        nmv.logger.header('Building Skeleton: ProgressiveBuilder')

        # Update the context
        self.context = context

        # Initialize the builder
        self.initialize_builder()

        # Draw the arbors progressively
        self.draw_arbors_progressively()

        # Draw the soma
        self.draw_soma()

        # Draw the endfeet
        self.draw_endfeet_if_applicable()

        # Add the morphology objects to a collection
        self.collection_morphology_objects_in_collection()

        # Return the list of the drawn morphology objects
        return self.morphology_objects
