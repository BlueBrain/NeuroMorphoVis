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

import nmv
import nmv.skeleton


####################################################################################################
# @verify_number_of_samples_per_section
####################################################################################################
def verify_segments_length(section):
    """
    Verifies the lengths of the segments that composed the section.

    :param section:
        A given section to be verified.
    """

    for i in range(len(section.samples) - 2):

        # Compute segment length
        segment_length = (section.samples[i + 1].point - section.samples[i].point).length

        # Report it
        nmv.logger.log('\t\t* ANALYSIS: Section [%s: %d] @ segment [%d] @ segment length [%f] ' %
              (section.get_type_string(), section.id, i, segment_length))


####################################################################################################
# @verify_number_of_samples_per_section
####################################################################################################
def verify_segments_length_wrt_radius(section):
    """
    Verifies the lengths of the segments that composed the section.

    :param section:
        A given section to be verified.
    """

    for i in range(len(section.samples) - 2):

        # Compute segment length
        segment_length = (section.samples[i + 1].point - section.samples[i].point).length

        # Get section radius
        radius = section.samples[i].radius

        if segment_length < radius:

            # Report it
            nmv.logger.log('\t\t* ANALYSIS: Section [%s: %d] @ segment [%d]: length [%f], radius [%f] ' %
                  (section.get_type_string(), section.id, i, segment_length, section.samples[i].radius))


####################################################################################################
# @verify_number_of_samples_per_section
####################################################################################################
def verify_number_of_samples_per_section(section):
    """
    Verifies the number of samples per section.

    :param section:
        A given section to be verified.
    """

    # Compute the number of samples per section
    number_samples_per_section = len(section.samples)

    # If the section has no samples, report this as an error and ignore this filter
    if number_samples_per_section == 0:

        # Report the error
        nmv.logger.log('\t\t* ERROR: Section [%s: %d] has NO samples, cannot be re-sampled' %
              (section.get_type_string(), section.id))

    # If the section has only two samples, then report it as an error
    if number_samples_per_section == 1:

        # Report the error
        nmv.logger.log('\t\t* ERROR: Section [%s: %d] has only ONE sample' %
              (section.get_type_string(), section.id))

    # If the section has only two samples, then report it as a warning
    if number_samples_per_section == 2:

        # Report the warning
        nmv.logger.log('\t\t* WARNING: Section [%s: %d] has only TWO samples' %
              (section.get_type_string(), section.id))


####################################################################################################
# @verify_section_length_with_respect_to_radii
####################################################################################################
def verify_section_length_with_respect_to_radii(section):
    """
    Verifies the section length with respect to its radii.
    This verification determines if the section is long enough or not. The section is considered
    SHORT if its length was less than DOUBLE the sum of the radii of its first and last samples.

    :param: section
        A given section to be verified.
    """

    # Ensure that the section has at least two samples, otherwise give an error
    if len(section.samples) < 2:

        # Report the issue
        nmv.logger.log('\t\t* ERROR: Section [%s: %d] has less than TWO samples' %
              (section.get_type_string(), section.id))

    # Compute the section length
    section_length = nmv.skeleton.ops.compute_section_length(section)

    # Get the radii of the first and last samples of the section
    first_sample_radius = section.samples[0].radius
    last_sample_radius = section.samples[-1].radius

    # Compute the minimal section length
    minimal_section_length = 2 * (first_sample_radius + last_sample_radius)

    # If the section length is less than the sum of the diameters, report that issue
    if section_length < minimal_section_length:

        # Report the issue
        nmv.logger.log('\t\t* WARNING: Section [%s: %d] is SHORT [%f < %f]' %
              (section.get_type_string(), section.id, section_length, minimal_section_length))

        return True

    return False


####################################################################################################
# @verify_section_length_with_respect_to_radii
####################################################################################################
def verify_short_sections_and_return_them(section,
                                          short_sections_detected=[]):
    """
    Verifies the section length with respect to its radii, identifies the short sections and
    return them in a list.

    :param section:
        A given section to verify.
    :param short_sections_detected:
        A list to keep the detected short section.
    """

    # If the section is short
    if verify_section_length_with_respect_to_radii(section=section):

        # Append it to the list
        short_sections_detected.append(section)


####################################################################################################
# @verify_number_of_children
####################################################################################################
def verify_number_of_children(section):
    """
    Verifies the number of children for a given section.
    Normally, each section should have TWO children at a bifurcation point, however, in
    certain cases, the section can contain only ONE child, THREE children or even more.

    :param: section
        A given section to be verified.
    """

    # Get the number of children of the section
    number_children = len(section.children)

    # The section has only one child
    if number_children == 1:

        # Report the issue
        nmv.logger.log('\t\t* WARNING: Section [%s: %d] has only ONE child' %
              (section.get_type_string(), section.id))

    # The section has more than two children
    if number_children > 2:

        # Report the issue
        nmv.logger.log('\t\t* WARNING: Section [%s: %d] has [%d] children' %
              (section.get_type_string(), section.id, number_children))


####################################################################################################
# @verify_radii_at_branching_points
####################################################################################################
def verify_radii_at_branching_points(section):
    """
    Verifies the radii of the given section at the branching points.
    If the radius of the first child sample is greater than that of the last sample of the
    parent, then report this issue.

    :param: section
        A given section to be verified.
    """

    # Skip the root sections
    if section.has_parent():

        # Compare the radius of the first sample of the section with that of the last sample of
        # the parent one, if this child is greater, then report an issue
        if section.samples[0].radius > section.parent.samples[-1].radius:

            # Report the issue
            nmv.logger.log('\t\t* WARNING: Section [%s: %d] has a radius issue: Parent=[%f], Child=[%f]' %
                  (section.get_type_string(), section.id, section.parent.samples[-1].radius,
                   section.samples[0].radius))


####################################################################################################
# @verify_duplicated_samples
####################################################################################################
def verify_duplicated_samples(section,
                              threshold=1.0):
    """
    Verifies if the section has doubles (or samples that are too close or not).

    :param: section
        A given section to be verified.
    """

    # Check the distance between every two successive samples and compare it with the threshold
    for i in range(len(section.samples) - 2):

        # Compute the distance between the two samples
        distance = (section.samples[i + 1].point - section.samples[i].point).length

        # Compare the distance with the threshold
        if distance < threshold:

            # Report the issue
            nmv.logger.log('\t\t* WARNING: Section [%s: %d] has DUPLICATES @ sample [%d], distance [%f]' %
                  (section.get_type_string(), section.id, i + 1, distance))


####################################################################################################
# @verify_axon_connection_to_soma
####################################################################################################
def verify_axon_connection_to_soma(morphology):
    """
    Verifies if the axon of a morphology is connected to its soma or not. If the initial segment of
    the axon is located far-away from the soma, the axon is connected to the closest dendrite.
    The intersection between the axon and the dendrites is checked, the axon is connected to the
    closest dendrite that is intersecting with it.

    :param morphology:
        The morphology skeleton of a neuron.
    """

    # Ensure that presence of the axon in the morphology
    if morphology.axon is None:

        # Report the issue
        nmv.logger.log('\t\t* WARNING: This morphology does NOT have an axon')

        # Skip
        return

    # Is the axon disconnected from the soma !
    if nmv.skeleton.ops.is_arbor_disconnected_from_soma(morphology.axon):

        # Report the issue
        nmv.logger.log('\t\t* WARNING: Section [%s: %d] is disconnected from the soma' %
              (morphology.axon.get_type_string(), morphology.axon.id))


####################################################################################################
# @verify_basal_dendrites_connection_to_soma
####################################################################################################
def verify_basal_dendrites_connection_to_soma(morphology):
    """
    Verifies if any basal dendrite is connected to the soma or not. The apical dendrite is always
    assumed to be connected to the soma since its large. Then it checks if the basal dendrite is
    connected to the apical dendrite or not.

    :param morphology:
        A given morphology skeleton.
    """

    # Verify dendrite by dendrite
    for i_basal_dendrite, basal_dendrite in enumerate(morphology.dendrites):

        # Is the basal dendrite disconnected from the soma !
        if nmv.skeleton.ops.is_arbor_disconnected_from_soma(basal_dendrite):

            # Report the issue
            nmv.logger.log('\t\t* WARNING: Section [%s: %d] is disconnected from the soma' %
                  (morphology.axon.get_type_string(), morphology.axon.id))

        # Is the basal dendrite intersecting with the apical dendrite, if exists !
        if morphology.apical_dendrite is not None:

            # Verify if the axon intersects with the apical dendrite
            if nmv.skeleton.ops.dendrite_intersects_apical_dendrite(
                    dendrite=basal_dendrite, apical_dendrite=morphology.apical_dendrite,
                    soma_radius=morphology.soma.mean_radius):

                # Report the issue
                nmv.logger.log('\t\t* WARNING: Section [%s: %d] intersects with section [%s: %d]' %
                      (morphology.axon.get_type_string(), morphology.axon.id,
                       morphology.apical_dendrite.get_type_string(), morphology.apical_dendrite.id))

        # Is the basal dendrite intersecting with another basal dendrite !
        # NOTE: The intersection function returns a positive result if this input basal
        # dendrite is intersecting with another basal dendrite with largest radius
        if nmv.skeleton.ops.basal_dendrite_intersects_basal_dendrite(
            dendrite=basal_dendrite, dendrites=morphology.dendrites,
                soma_radius=morphology.soma.mean_radius):

                # Report the issue
                nmv.logger.log('\t\t* WARNING: Section [%s: %d] intersects with section [%s: %d]' %
                      (morphology.axon.get_type_string(), morphology.axon.id,
                       morphology.apical_dendrite.get_type_string(), morphology.apical_dendrite.id))


################################################################################################
# @verify_arbors_connection_to_soma
################################################################################################
def verify_arbors_connection_to_soma(morphology):
    """
    Verifies if the different arbors of the morphology are connected to the soma or not. The apical
    dendrite is always assumed to be connected to the soma since its large. We then check the
    connectivity of the axon and the basal dendrites one by one.

    :param morphology:
        A given morphology skeleton.
    """

    # Verify the connectivity of the basal dendrites
    verify_basal_dendrites_connection_to_soma(morphology=morphology)

    # Verify the connectivity of the axon
    verify_axon_connection_to_soma(morphology=morphology)