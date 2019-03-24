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
import math

# Internal imports
import nmv
import nmv.skeleton


####################################################################################################
# @compute_section_volume_from_segments
####################################################################################################
def compute_section_volume_from_segments(section):
    """Computes the volume of a section from its segments.
    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its volume.
    :return:
        Section total volume in cube microns.
    """

    # Section volume
    section_volume = 0.0

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Return 0
        return section_volume

    # Integrate the volume between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the data of the samples along each segment on the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius

        # Compute the segment volume and append to the total section volume
        section_volume += (1.0 / 3.0) * math.pi * (p0 - p1).lenght * (r0 * r0 + r0 * r1 + r1 * r1)

    # Return the section volume
    return section_volume


####################################################################################################
# @compute_section_surface_area_from_segments
####################################################################################################
def compute_section_surface_area_from_segments(section):
    """Computes the surface area of a section from its segments.
    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its surface area.
    :return:
        Section total surface area in square microns.
    """

    # Section surface area
    section_surface_area = 0.0

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Return 0
        return section_surface_area

    # Integrate the surface area between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the data of the samples along each segment on the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius

        # Compute the segment lateral area
        segment_length = (p0 - p1).length
        r_sum = r0 + r1
        r_diff = r0 - r1
        segment_lateral_area = math.pi * r_sum * math.sqrt((r_diff * r_diff) + segment_length)

        # Compute the segment surface area and append it to the total section surface area
        section_surface_area += segment_lateral_area + math.pi * ((r0 * r0 ) + (r1 * r1))

    # Return the section surface area
    return section_surface_area


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

    # Section length
    section_length = 0.0

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Return 0
        return section_length

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
# @compute_max_section_radius
####################################################################################################
def compute_max_section_radius(section):
    """
    Computes the max radius of a section.

    :param section:
        A given section to compute its max radius.
    :return:
        The max radius of the section.
    """

    # Average section radius
    max_section_radius = 0.0

    # Sum the radii of all the sample
    for sample in section.samples:

        if sample.radius > max_section_radius:
            max_section_radius = sample.radius

    # Return the max section radius
    return max_section_radius


####################################################################################################
# @compute_min_section_radius
####################################################################################################
def compute_min_section_radius(section):
    """
    Computes the min radius of a section.

    :param section:
        A given section to compute its min radius.
    :return:
        The min radius of the section.
    """

    # Average section radius
    min_section_radius =10000000

    # Sum the radii of all the sample
    for sample in section.samples:

        if sample.radius < min_section_radius:
            min_section_radius = sample.radius

    # Return the min section radius
    return min_section_radius


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
# @analyze_number_of_samples_per_section
####################################################################################################
def analyze_number_of_samples_per_section(section,
                                          analysis_data_list):
    """Analyze the number of samples per section.

    :param section:
        A given section to get analyzed.
    :param analysis_data_list:
        A list to collect the analysis data.
    """

    analysis_string = 'Section[%s : %d] : %d' % (section.get_type_string(),
                                                 section.id,
                                                 len(section.samples))
    analysis_data_list.append(analysis_string)


####################################################################################################
# @analyze_number_of_segments_per_section
####################################################################################################
def analyze_number_of_segments_per_section(section,
                                           analysis_data_list):
    """Analyze the number of segments per section.

    :param section:
        A given section to get analyzed.
    :param analysis_data_list:
        A list to collect the analysis data.
    """

    analysis_string = 'Section[%s : %d] : %d' % (section.get_type_string(),
                                                 section.id,
                                                 len(section.samples) - 1)
    analysis_data_list.append(analysis_string)


####################################################################################################
# @analyze_number_of_children
####################################################################################################
def analyze_number_of_children_per_section(section,
                                           analysis_data_list):
    """Analyze the number of children per section.

    :param section:
        A given section to get analyzed.
    :param analysis_data_list:
        A list to collect the analysis data.
    """

    if section.has_children():
        analysis_string = 'Section[%s : %d] : %d' % (section.get_type_string(),
                                                     section.id,
                                                     len(section.children))
        analysis_data_list.append(analysis_string)


####################################################################################################
# @analyze_branching_angles_per_section
####################################################################################################
def analyze_branching_angles_per_section(section,
                                         analysis_data_list):
    """Analyze the branching angles along the morphology.

    :param section:
        A given section to get analyzed.
    :param analysis_data_list:
        A list to collect the analysis data.
    """

    if section.has_children():

        # If the section has only a single child, then return
        if len(section.children) == 1:
            return

        # If the section has two children, then get the angle between them
        elif len(section.children) == 2:

            # Get a reference to each child
            child_1 = section.children[0]
            child_2 = section.children[1]

            # Compute the vectors of each child
            child_1_vector = (child_1.samples[1].point - child_1.samples[0].point).normalized()
            child_2_vector = (child_2.samples[1].point - child_2.samples[0].point).normalized()

            # Compute the angle between the two children
            angle = child_1_vector.angle(child_2_vector) * 180.0 / 3.14

            analysis_string = 'Section[%s : %d] : %f' % (section.get_type_string(),
                                                         section.id,
                                                         angle)
            analysis_data_list.append(analysis_string)

        # If the section has more than two children, then assume that the first one is the primary
        else:

            # Primary child
            primary_child = section.children[0]
            primary_child_vector = \
                (primary_child.samples[1].point - primary_child.samples[0].point).normalized()

            # Compute the angle for the rest of the children
            for i in range(1, len(section.children)):

                # Secondary child
                secondary_child = section.children[i]
                secondary_child_vector = (secondary_child.samples[1].point -
                                          secondary_child.samples[0].point).normalized()

                # Compute the angle between the two children
                angle = primary_child_vector.angle(secondary_child_vector) * 180.0 / 3.14

                analysis_string = 'Section[%s : %d] : %f' % (section.get_type_string(),
                                                             section.id,
                                                             angle)
                analysis_data_list.append(analysis_string)


####################################################################################################
# @analyze_branching_radii_per_section
####################################################################################################
def analyze_branching_radii_per_section(section,
                                        analysis_data_list):
    """Analyze the branching radii along the morphology for ONLY the bifurcation points.

    :param section:
        A given section to get analyzed.
    :param analysis_data_list:
        A list to collect the analysis data.
    """

    # Only if the section has two children
    if len(section.children) == 2:

        parent_radius = section.samples[-1].radius
        child_1_radius = section.children[0].samples[0].radius
        child_2_radius = section.children[1].samples[0].radius

        status = 'OK'
        if child_1_radius > parent_radius or child_2_radius > parent_radius:
            status = 'ERROR'

        analysis_string = 'Section[%s : %d] : [%f, %f, %f] : %s' % (section.get_type_string(),
                                                                    section.id,
                                                                    parent_radius,
                                                                    child_1_radius,
                                                                    child_2_radius,
                                                                    status)
        analysis_data_list.append(analysis_string)


####################################################################################################
# @analyze_section_length
####################################################################################################
def analyze_section_length(section,
                           analysis_data_list):
    """Analyze the length of the sections.

    :param section:
        A given section to get analyzed.
    :param analysis_data_list:
        A list to collect the analysis data.
    """

    # If the section has less than two samples, then the section has zero length
    if len(section.samples) < 2:

        analysis_string = 'Section[%s : %d] : Length[%f] : %s' % (section.get_type_string(),
                                                                  section.id,
                                                                  0.0,
                                                                  'ERROR')
        analysis_data_list.append(analysis_string)

    # If the section has more than two samples, then compute the sum of the segments lengths
    else:

        # Compute section length
        section_length = compute_section_length(section=section)

        analysis_string = 'Section[%s : %d] : Length[%f] : %s' % (section.get_type_string(),
                                                                  section.id,
                                                                  section_length,
                                                                  'OK')
        analysis_data_list.append(analysis_string)


####################################################################################################
# @analyze_section_radii
####################################################################################################
def analyze_section_radii(section,
                          analysis_data_list):
    """Analyze the radii of the samples and the average radii of the sections.

    :param section:
        A given section to get analyzed.
    :param analysis_data_list:
        A list to collect the analysis data.
    """

    # Compute average section radius
    average_section_radius = compute_average_section_radius(section=section)

    # Report the radii of the samples
    for i_sample in section.samples:

        analysis_string = 'Section[%s : %d] Average Radius[%f], Sample[%d] : Radius[%f]' % (
            section.get_type_string(), section.id, average_section_radius,
            i_sample.id, i_sample.radius)
        analysis_data_list.append(analysis_string)


####################################################################################################
# @analyze_short_sections
####################################################################################################
def analyze_short_sections(section,
                           analysis_data_list):
    """Analyze the short sections, which have their length shorter than the sum of their
    initial and final diameters.

    :param section:
        A given section to get analyzed.
    :param analysis_data_list:
        A list to collect the analysis data.
    """

    # Only applies if the section has more than two samples
    if len(section.samples) > 1:

        # Compute the sum of the diameters of the first and last samples
        diameters_sum = (section.samples[0].radius + section.samples[-1].radius) * 2

        # Compute section length
        section_length = compute_section_length(section=section)

        # If the sum is smaller than the section length, then report it as an issue
        if section_length < diameters_sum:

            analysis_string = 'Section[%s : %d] : Length[Current : %f, Minimal : %f]' % (
                section.get_type_string(), section.id, section_length, diameters_sum)
            analysis_data_list.append(analysis_string)


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
    """Get the child that can form a continuation from the given parent section.

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
