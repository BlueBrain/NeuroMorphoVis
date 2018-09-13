####################################################################################################
# Copyright (c) 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# Import vasculature scripts
from .vasculature_sample import *
from .vasculature_section import *


####################################################################################################
# VasculatureSection
####################################################################################################
class VasculatureSkeletonizer:
    """Vasculature skeletonization class."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 points_list,
                 segments_list,
                 sections_list,
                 connections_list):
        """Constructor

        :param points_list:
            A list of all the points in the morphology skeleton.
        :param segments_list:
            A list of all the edges in the morphology skeleton.
        :param sections_list:
            A list of all the sections in the morphology skeleton.
        :param connections_list:
            A list of all the connections in the morphology skeleton.
        """

        # A list of all the points in the morphology
        self.morphology_points_list = points_list

        # A list of all the segments in the morphology
        self.morphology_segments_list = segments_list

        # A list of all the sections in the morphology
        self.morphology_sections_list = sections_list

        # A list of all the connections in the morphology
        self.morphology_connections_list = connections_list

        # A linear list of all the sections in the vasculature morphology
        self.sections_list = list()

        # A list of all the root sections into the skeleton that can give us access to the rest
        # of the sections
        self.roots = list()

    ################################################################################################
    # @get_sample_on_segment
    ################################################################################################
    def get_sample_on_segment(self,
                              sample_index):
        """Returns an object of VasculatureSample using its index from the morphology samples list.

        :param sample_index:
            The index of the sample.
        :return:
            Returns an object of VasculatureSample using its index from the morphology samples list.
        """

        # The coordinates of the first sample
        x = raw_samples_list[sample_index][0]
        y = raw_samples_list[sample_index][1]
        z = raw_samples_list[sample_index][2]

        # The cartesian coordinates of the sample
        point = Vector((x, y, z))

        # The radius of the first sample
        radius = raw_samples_list[sample_index][3]

        # Construct a new sample and return a reference to it
        return VasculatureSample(sample_index, point, radius)

    ################################################################################################
    # @get_samples_on_section
    ################################################################################################
    def get_samples_on_section(self,
                               initial_segment_index,
                               final_segment_index):
        """Returns a list of all the samples belonging to a section that is composed of a set of
        connected segments.

        :param initial_segment_index:
            The index of the initial segment along the section.
        :param final_segment_index:
            The index of the final segment along the section.
        :return:
            Returns a list of all the samples that belong to the section.
        """

        # A list of all the samples along the section
        section_samples_list = list()

        # Traverse the section, segment by segment
        for i_segment in range(initial_segment_index, final_segment_index):

            # Get the first sample along the segment
            sample = self.get_sample_on_segment(self.morphology_segments_list[i_segment][0])

            # Add the sample to the samples list
            section_samples_list.append(sample)

        # Return a reference to the samples list along the section
        return section_samples_list

    ################################################################################################
    # @build_sections_list
    ################################################################################################
    def build_sections_list(self):
        """Builds a list of all the sections in the morphology to be able to skeletonize it
        """

        # For each section in the morphology sections list
        for i_section in range(len(morphology_sections_list) - 1):
            # The index of the first segment (or edge) along the section
            initial_segment_index = self.morphology_sections_list[i_section]

            # The index of the last segment (or edge) along the section
            final_segment_index = self.morphology_sections_list[i_section + 1]

            # Get a list that has all the samples of the section
            section_samples_list = self.get_samples_on_section(initial_segment_index,
                                                               final_segment_index)

            # Construct the section
            section = VasculatureSection(i_section, section_samples_list)

            # Add the section to the final list
            self.sections_list.append(section)

    ################################################################################################
    # @build_skeleton_trees
    ################################################################################################
    def build_skeleton_trees(self):
        """Use the connectivity data to build the trees of the different structures in the data.
        """

        # For each connection in the data
        for i_connection in range(len(raw_connectivity_list)):

            # Get the index of the parent
            parent_index = self.morphology_connections_list[i_connection][0]

            # Get the index of the child
            child_index = self.morphology_connections_list[i_connection][1]

            # Update the children list
            sections_list[parent_index].update_children(sections_list[child_index])

            # Update the parent from None to a specific parent, otherwise it is a root
            sections_list[child_index].update_parent(sections_list[parent_index])

        # Updating the roots
        for section in self.sections_list:

            # If the section has no parent
            if section.parent is None:

                # Add him to the root list
                self.roots.append(section)

    ################################################################################################
    # @skeletonize
    ################################################################################################
    def skeletonize(self):
        """Skeletonizes the vasculature morphology.
        """

        # Build the sections list
        self.build_sections_list()

        # Build the trees
        self.build_skeleton_trees()


