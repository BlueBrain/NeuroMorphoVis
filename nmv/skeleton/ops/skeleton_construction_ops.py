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

# System imports
import copy
import math

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @update_section_parenting
####################################################################################################
def update_section_parenting(section,
                             sections_list):
    """Updates the section parents' and children references.

    :param section:
        A given section to update.
    :param sections_list:
        A list of all the sections in the morphology.
    """

    # Detect if the section has no parent, then set it as a root
    # Use the first sample to identify if this section is a root or not
    if str(section.samples[0].parent_index) == str(-1):

        # This section is a root
        section.parent = None
        section.parent_index = None

    for i_section in sections_list:

        # If this is the same section
        if i_section.index == section.index:

            # Next section
            continue

        # If the last sample along the section has the same index of the first sample of the
        # auxiliary section, then the auxiliary section is a child
        if section.samples[-1].index == i_section.samples[0].index:

            # Add the auxiliary section as a child to the parent section
            section.children.append(i_section)
            section.children_ids.append(i_section.index)

        # If the first sample along the section has the same index of the last sample of the
        # auxiliary section, then the auxiliary section is a parent
        if section.samples[0].index == i_section.samples[-1].index:

            # Set the auxiliary section to be a parent to this child section
            section.parent = i_section
            section.parent_index = i_section.index


####################################################################################################
# @build_arbors_from_sections
####################################################################################################
def build_arbors_from_sections(sections_list):
    """Returns a list of nodes where we can access the different sections of a single arbor as a
    tree.

    :param sections_list:
        A linear list of sections.
    :return:
        A list containing references to the root nodes of the different arbors in the sections list.
    """

    # If the sections list is None
    if sections_list is None:

        # This is an issue
        nmv.logger.log('ERROR: Invalid sections list')

        # Return None
        return None

    # If the sections list is empty
    if len(sections_list) == 0:

        # Then return None
        return None

    # A list of roots
    roots = list()

    # Iterate over the sections and get the root ones
    for section in sections_list:

        # If the section has no parent, it is a root then
        if section.parent is None:

            # Append this root to the list
            roots.append(section)

    # If the list does not contain any roots, then return None, otherwise return the entire list
    if len(roots) == 0:

        # This might be an issue
        nmv.logger.log('WARNING: No roots found in the sections list')

        # Return None
        return None

    else:

        # Return the root list
        return roots


####################################################################################################
# @build_arbor_as_single_object
####################################################################################################
def build_arbor_as_single_object(section, name,
                                 poly_line_data=[],
                                 poly_lines_data=[],
                                 secondary_sections=[],
                                 branching_order=0,
                                 max_branching_order=nmv.consts.Math.INFINITY,
                                 repair_morphology=False,
                                 ignore_branching_samples=False,
                                 roots_connection=nmv.enums.Skeleton.Roots.ALL_DISCONNECTED):
    """Draw a list of sections connected together as a poly-line.

    :param section:
        Section root.
    :param poly_line_data:
        A list of lists containing the data of the poly-line format.
    :param poly_lines_data:
        A list that should contain all the poly-lines.
    :param secondary_sections:
        A list of the secondary sections along the arbor.
    :param branching_order:
        Current branching level.
    :param max_branching_order:
        Maximum branching level the section can grow up to, infinity.
    :param name:
        Section name.
    :param repair_morphology:
        Apply some filters to repair the morphology during the poly-line construction.
    :param ignore_branching_samples:
        Ignore fetching the branching samples from the morphology skeleton.
    :param roots_connection:
        How the root sections are connected to the soma.
    """

    # Ignore the drawing if the section is None
    if section is None:
        return

    # Increment the branching level
    branching_order += 1

    # Verify if this is the last section along the arbor or not
    is_last_section = False
    if branching_order >= max_branching_order or not section.has_children():
        is_last_section = True

    # Verify if this a continuous section or not
    is_continuous = True
    if len(poly_line_data) == 0:
        is_continuous = False
        secondary_sections.append(section)

    # Get a list of all the poly-line that corresponds to the given section
    section_data = nmv.skeleton.ops.get_connected_sections_poly_line(
        section=section,
        roots_connection=roots_connection,
        is_continuous=is_continuous,
        is_last_section=is_last_section,
        ignore_branching_samples=ignore_branching_samples,
        process_section_terminals=False)

    # Extend the polyline samples for final mesh building
    poly_line_data.extend(section_data)

    # If the section does not have any children, then draw the section and clean the
    # poly_line_data list
    if (not section.has_children()) or (branching_order >= max_branching_order):

        # Add the section object to the sections_objects list
        poly_lines_data.append(copy.deepcopy(poly_line_data))

        # Clean the polyline samples list
        poly_line_data[:] = []

        # If no more branching is required, then exit the loop
        return

    # Iterate over the children sections and draw them, if any
    for child in section.children:

        # Draw the children sections
        build_arbor_as_single_object(
            section=child, name=name, poly_line_data=poly_line_data,
            poly_lines_data=poly_lines_data, secondary_sections=secondary_sections,
            branching_order=branching_order, max_branching_order=max_branching_order,
            repair_morphology=repair_morphology, roots_connection=roots_connection)


####################################################################################################
# @get_section_polyline_color_index_based_on_length
####################################################################################################
def get_section_polyline_color_index_based_on_length(
        section, morphology, colormap_resolution=nmv.consts.Color.COLORMAP_RESOLUTION):

    # The minimum value is the minimum section length in the morphology
    minimum = morphology.stats.minimum_section_length

    # The maximum value is the maximum section length in the morphology
    maximum = morphology.stats.maximum_section_length

    return math.ceil(colormap_resolution * section.stats.length / (maximum - minimum)) - 1
