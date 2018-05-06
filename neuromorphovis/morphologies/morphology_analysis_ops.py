####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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

# System imports
import os, sys, math

# Append the internal modules into the system paths
sys.path.append("%s/../modules" % os.path.dirname(os.path.realpath(__file__)))


####################################################################################################
# @compute_section_length
####################################################################################################
def compute_section_length(section):
    """
    Computes the length of a given section.
    NOTE: This function returns a meaningful value for the roots sections, ONLY when the negative
    samples are removed from the branch, otherwise, the contribution of the negative samples
    will be integrated. The negative samples are those located closer to the origin of the soma
    than the first samples of the section.

    :param section:
        A given section to compute its length.
    :return:
        Section total length in microns.
    """

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Report the issue
        nmv.logger.log('\t\t* ERROR: Section [%s: %d] has less than TWO samples' %
              (section.get_type_string(), section.id))

        # Return 0
        return 0.0

    # Section length
    section_length = 0.0

    # Integrate the distance between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the points along each segment on the section
        point_0 = section.samples[i].point
        point_1 = section.samples[i + 1].point

        # Update the section length
        section_length += (point_1 - point_0).length

    # Return the section length
    return section_length


####################################################################################################
# @compute_average_section_radius
####################################################################################################
def compute_average_section_radius(section):
    """
    Computes the average radius of a section getting the mean value of the radii of all samples
    along the section.

    :param section:
        A given section to compute its average radius.
    :return:
        The average radius of the section.
    """

    # Average section radius
    average_section_radius = 0.0

    # Sum the radii of all the sample
    for sample in section.samples:

        # Add the radius
        average_section_radius += sample.radius

    # Get the average
    average_section_radius /= len(section.samples)

    # Return the average section radius
    return average_section_radius


####################################################################################################
# @compute_number_of_samples_per_section
####################################################################################################
def compute_number_of_samples_per_section(section):
    """
    Computes the number of samples per section in a certain arbor.
    NOTE: The number of segments is computed from the number of samples.

    :param section:
        A given section to compute the number of samples composing it.
    :return:
        The number of samples that are located along the section.
    """

    return len(section.samples)


####################################################################################################
# @compute_number_of_segments_per_section
####################################################################################################
def compute_number_of_segments_per_section(section):

    """
    Computes the number of segments per section in a certain arbor.
    NOTE: The number of segments is computed from the number of samples.

    :param section:
        A given section to compute the number of segments composing it.
    :return:
        The number of samples that are located along the section.
    """

    return compute_number_of_samples_per_section(section) - 1


####################################################################################################
# @get_largest_radius_of_children
####################################################################################################
def get_largest_radius_of_children(section):
    """
    Gets the radius of the largest child section at its first sample.

    :param section:
        A given section to retrieve the radius of the thickest child.
    :return:
        The radius of the largest child section at its first sample.
    """

    # The radius of the greatest child
    greatest_radius = 0

    # Iterate over the children of the section
    for child in section.children:

        # If the radius of the first sample of the child is greater than the greatest radius,
        # then update it
        if child.samples[0].radius > greatest_radius:

            # Update the greatest radius
            greatest_radius = child.samples[0].radius

    return greatest_radius


####################################################################################################
# @get_smallest_radius_of_children
####################################################################################################
def get_smallest_radius_of_children(section):
    """
    Gets the radius of the smallest child section at its first sample.

    :param section:
        A given section to retrieve the radius of the thinnest child.
    :return:
        The radius of the thinnest child section at its first sample.
    """

    # Set the initial value to something big
    smallest_radius = 1000000000

    # Iterate and compare
    for child in section.children:

        # Get the radius of the first sample of the child
        child_radius = child.samples[0].radius

        # Compare
        if child_radius < smallest_radius:

            # Set the smallest radius to it
            smallest_radius = child_radius

    # Return the smallest radius
    return smallest_radius




####################################################################################################
# @get_resampling_distance_of_secondary_section
####################################################################################################
def get_resampling_distance_of_secondary_section(secondary_section):
    """

    :param section:
    :return:
    """

    # Get a reference to the primary section at the same branching level
    primary_section = None
    for child in secondary_section.parent.children:

        # If the child is primary, select it and break
        if child.is_primary:

            # Set this section to the primary_section
            primary_section = child

            # Break, we found the primary section
            break

    # Get the initial re-sampling distance based on the first sample of the primary child
    resampling_distance_step = primary_section.samples[0].radius * 2

    # Get the primary section direction
    primary_section_direction = \
        (primary_section.samples[1].point - primary_section.samples[0].point).normalized()

    # Get the primary section re-sampling point
    primary_section_resampling_point = primary_section.samples[0].point + \
                                     (primary_section_direction * resampling_distance_step)

    # Get the direction of the secondary child (the current section)
    secondary_section_direction = \
        (secondary_section.samples[1].point - secondary_section.samples[0].point).normalized()

    # The minimal distance between the two sections (primary and secondary), avoid intersections
    minimal_branching_distance = primary_section.samples[0].radius * 2

    # Iterate until finding the suitable sampling point along the secondary section
    i = 1.0
    while True:

        # The re-smapling distance where the secondary section will be re-sampled
        secondary_section_resampling_distance = i * resampling_distance_step

        # Compute the secondary re-sampling point
        secondary_section_resampling_point = secondary_section.samples[0].point + \
                           (secondary_section_direction * secondary_section_resampling_distance)

        # Compute the branching distance between the two sections
        branching_distance = \
            (secondary_section_resampling_point - primary_section_resampling_point).length

        # Compare the branching distance with the minimum required
        if branching_distance > minimal_branching_distance:

            # Break and return the secondary section resampling distance
            return secondary_section_resampling_distance

        # Otherwise, search for more suitable sampling distance
        else: i += 1.0


####################################################################################################
# @get_resampling_distance_of_secondary_section_based_on_angle
####################################################################################################
def get_resampling_distance_of_secondary_section_based_on_angle(section):
    """
    This function assumes that the section is SECONDARY, otherwise the section is not resampled

    :param section:
    :return:
    """

    # Get the parent section
    parent_section = section.parent

    # Get the primary section
    primary_section = None
    for child in parent_section.children:
        if child.is_primary:
            primary_section = child

    # Get the direction of the primary section
    primary_section_vector = \
        (primary_section.samples[1].point - primary_section.samples[0].point).normalized()

    # Get the direction of the secondary section
    secondary_section_vector = (section.samples[1].point - section.samples[0].point).normalized()

    # Get the angle between the primary section and the secondary section
    angle = primary_section_vector.angle(secondary_section_vector)

    # Compute the resampling distance
    delta = 0.5
    resampling_distance = (section.samples[0].radius * math.sqrt(2) / math.tan(0.5 * angle)) + delta

    # Return the resampling distance
    return resampling_distance


####################################################################################################
# @get_continuation_child
####################################################################################################
def get_continuation_child(section):
    """
    Gets the child that can form a continuation from the given parent section.

    :param section:
        A given section.
    :return:
        The child that is almost continuous from the parent.
    """

    # If the section does not have any children, then this filter is not valid
    if not section.has_children():

        # Return
        return None

    # If the section has one child, then return it by default
    if len(section.children) == 1:
        return section.children[0]

    # Get the vector of the parent section based on its last two samples
    parent_vector = (section.samples[-2].point - section.samples[-1].point).normalized()

    # Store a reference to the primary child
    primary_child = None

    # The angle between the parent and child sections
    greatest_angle = 0

    # Iterate over the children of the section
    for child in section.children:

        # Compute the vector of the child section based on its first two samples
        child_vector = (child.samples[1].point - child.samples[0].point).normalized()

        # Compute the angle between the two vectors
        angle = parent_vector.angle(child_vector)

        # If the angle is greater than the greatest angle, then update the @primary_child reference
        if angle > greatest_angle:

            # Update the angle
            greatest_angle = angle

            # Update the primary child
            primary_child = child

    # Return a reference to the child
    return primary_child
