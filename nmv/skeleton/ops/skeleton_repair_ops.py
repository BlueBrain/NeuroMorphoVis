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
import os, sys, copy, math

# Internal imports
import nmv
import nmv.skeleton


####################################################################################################
# @repair_short_sections_by_compression
####################################################################################################
def repair_short_sections_by_compression(section,
                                         consider_subdivision=False):
    """Repair a given short section.
    This function computes the section length and compares it with a minimalistic value to
    verify if this section can be considered short or not.
    If the section is reported to be short, then, we change the radii of the entire section to
    a certain value that corresponds to its length.

    :param section:
        A root section, of a given arbor.
    :param consider_subdivision:
        If this flag is set to True, then we will scale the minimal section length by sqrt(2) to
        account for the subdivision operations that are used following to meshing a proxy geometry.
    """

    # Get the section length
    section_length = nmv.skeleton.ops.compute_section_length(section)

    # Consider the subdivision values
    subdivision_factor = math.sqrt(2) if consider_subdivision else 1.0

    # Get the minimal section length that can be used to re-sample the section
    # This distance can be computed from the radii of the last sample of the parent section and
    # the first sample of this section
    # The section must have at least two samples, otherwise this function will give an error
    if section.has_parent():
        minimal_section_length = 2 * subdivision_factor * \
                                 (section.parent.samples[-1].radius + section.samples[-1].radius)
    else:
        minimal_section_length = 2 * subdivision_factor * \
                                 (section.samples[0].radius + section.samples[-1].radius)

    # If section length is less than the minimal section length, then fix the radii
    if section_length < minimal_section_length:

        # Report the repair
        nmv.logger.log('\t\t* REPAIRING: Short section [%s: %d], using compression' %
              (section.get_type_string(), section.id))

        # Get the average radius of the section can therefore be computed based on the
        # minimal section length value
        average_section_radius = section_length / 4.0

        # Iterate over all the samples along the section and set their radii to this value
        for sample in section.samples:

            # Update the radius value
            sample.radius = average_section_radius

        # Since we have change the radii of the short section, therefore, we must accordingly
        # update the radius of the last sample of the parent section and set the radii of the
        # first samples of the children at the same level to the @average_section_radius to
        # avoid any branching artifacts
        if section.has_parent():

            # Set the radius of the last sample of the parent to @average_section_radius
            section.parent.samples[-1].radius = average_section_radius

            # Set the radii of the first samples of the children sections at the same level to the
            # @average_section_radius
            for child in section.parent.children:
                child.samples[0].radius = average_section_radius


####################################################################################################
# @repair_short_sections_by_connection_to_child
####################################################################################################
def repair_short_sections_by_connection_to_child(section):
    """
    Repairs a given short section by connecting it to a child to form a longer section.
    NOTE: The section is connected to the child section that can form a continuation with the
    least angle between the section and its children.

    :param section:
        A given section to repair
    """

    # Get the primary child that is almost continuous to the section.
    primary_child = nmv.skeleton.ops.get_continuation_child(section=section)

    # Append the samples of the primary child to the parent section, and do not add the last
    # sample to avoid duplicating samples
    for i in range(len(primary_child.samples) - 2):
        section.samples.append(primary_child.samples[i])

    # Update the children list with the rest of the children (given that there are more than two)
    updated_children_list = list()
    for child in section.children:

        # Ignore the primary child, since it has been already integrated into the parent
        if child.id == primary_child.id:
            continue

        else:

            # Add the child to the list
            updated_children_list.append(child)

    # Update the children list
    section.children = updated_children_list


####################################################################################################
# @repair_sections_with_single_child
####################################################################################################
def repair_sections_with_single_child(section):
    """
    If a section has a single child, then consider this child as a continuation to the parent
    section and update the morphology.

    :param section:
        A root section, of a given arbor.
    """

    # Get the number of children of the section
    number_children = len(section.children)

    # The section must have only one child
    if number_children == 1:

        # Report the repair
        nmv.logger.log('\t\t* REPAIRING: Section [%s: %d] has been connected to parent' %
              (section.get_type_string(), section.id))

        # Apply the filter
        nmv.skeleton.ops.connect_single_child(section=section)


####################################################################################################
# @repair_parents_with_smaller_radii
####################################################################################################
def repair_parents_with_smaller_radii(section):
    """
    If the initial sample of the section (at the branching point) has larger radius than that
    of the last sample of the parent section, then, fix this radius by making it equivalent to
    that of the parent sample.

    :param section:
        A given section to update the radius of its first sample based on the values of the radii
        of the children sections.
    """

    # If the section has no children, then return
    if not section.has_children():

        # Return
        return

    # Get the largest radius of the children sections
    largest_radius_of_children_sections = nmv.skeleton.ops.get_largest_radius_of_children(section)

    # If the radius of the last sample of the parent section is smaller than that of the greatest
    # child, then fix this radius
    if section.samples[-1].radius < largest_radius_of_children_sections:

        # Set the radius of the last sample of the section to the that largest radius
        section.samples[-1].radius = largest_radius_of_children_sections

        # Report the repair
        nmv.logger.log('\t\t* REPAIRING: Section [%s: %d], radius [%f]' %
              (section.get_type_string(), section.id, section.samples[-1].radius))