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
import random

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Internal imports
import nmv
import nmv.enums
import nmv.geometry
import nmv.mesh
import nmv.scene
import nmv.skeleton


####################################################################################################
# @is_arbor_starting_inside_soma
####################################################################################################
def is_arbor_starting_inside_soma(arbor,
                                  soma_radius):
    """Check if the arbor is starting inside the soma or not.

    :param arbor:
        A given arbor to verify its connection to the soma.
    :param soma_radius:
        The initial radius of the soma.
    :return:
        True or False.
    """

    # The given section must be root to apply this filter
    if arbor.is_root():

        # Sample by sample of the root section
        for i_sample in arbor.samples:

            # If the sample is located within the soma extent, return True
            if i_sample.point.length < soma_radius:
                return True

    # Otherwise return False
    return False


####################################################################################################
# @is_arbor_disconnected_from_soma
####################################################################################################
def is_arbor_disconnected_from_soma(arbor,
                                    threshold=15.0):
    """Check if a branch is disconnected from the soma or not based on a given threshold distance.

    :param arbor:
        A given arbor to verify its connection to the soma.
    :param threshold:
        A threshold distance, by default 15.0 microns.
    :return:
        True or False.
    """

    # The given section must be parent to apply this filter, otherwise return
    if arbor.has_parent():

        # This is not a parent section, it is not connected to the soma, by default!
        return False

    # Compare the distance between the initial segment of the arbor to the threshold value
    if arbor.samples[0].point.length > threshold:

        # The arbor is disconnected
        return True

    # Otherwise, it is connected
    return False


####################################################################################################
# @label_primary_and_secondary_sections_based_on_radii
####################################################################################################
def label_primary_and_secondary_sections_based_on_radii(section):
    """Labels the children of a given section to primary or secondary, based on the radii of the
    children. The child is labeled primary if its first sample has a greater radius than the
    other child.

    :param section:
        A given section to set the order of its children to either primary or secondary.
    """

    # If the section does not have any children, then it is not valid to apply this filter
    if not section.has_children():

        # Return
        return

    # Store a reference to the primary child
    primary_child = None

    # The radius of the greatest child
    greatest_radius = 0

    # Iterate over the children of the section
    for child in section.children:

        # If the radius of the child is greater than the greatest radius, then refer to this
        # child to be the primary child
        if child.samples[0].radius > greatest_radius:

            # Update the primary_child
            primary_child = child

            # Update the greatest radius
            greatest_radius = child.samples[0].radius

    # Create a new children list with update order, where the primary section comes first and the
    # secondary ones come later in the loop for the smooth continuation of the meshing
    children_list_with_updated_order = list()

    # Add the primary child as the first element in the list
    children_list_with_updated_order.append(primary_child)

    # Iterate over the children again to update their labels
    for child in section.children:

        # If the child is the same as the primary child (compare the IDs), label it the primary
        if child.id == primary_child.id:

            # Set this section to be the primary
            child.is_primary = True

        # Otherwise, set it to secondary
        else:

            # Set it to be a secondary section
            child.is_primary = False

            # Set the radius of a secondary child to half of the primary branch, for clean branching
            child.samples[0].radius = greatest_radius * 0.5

            # Append the secondary child to the children list that has the new order
            children_list_with_updated_order.append(child)

    # Update the children list in the section
    section.children = children_list_with_updated_order


####################################################################################################
# @label_primary_and_secondary_sections_based_on_angles
####################################################################################################
def label_primary_and_secondary_sections_based_on_angles(section):
    """Labels the children of the section to primary or secondary, based on the angles between the
    section, that is considered parent and the children. Note that the greater the angle is between
    the parent section and the child, the more primary the child is.

    NOTE: To avoid resampling artifacts, the radius of the parent section is UPDATED to match the
    greatest radius of the first sample of the children sections.

    :param section:
        A given section to set the order of its children to either primary or secondary.
    """

    # If the section does not have any children, then this filter is not valid
    if not section.has_children():

        # Return
        return

    # If this section is a root, then its primary by default
    if not section.has_parent():

        # Set the section to a primary
        section.is_primary = True

    # Get the vector of the parent section based on its last two samples
    parent_vector = (section.samples[-2].point - section.samples[-1].point).normalized()

    # Compute the parent vector length
    parent_vector_length = (section.samples[-2].point - section.samples[-1].point).length

    # Ensure that the parent vector is not zero
    if parent_vector_length < 0.0001:
        parent_vector = (section.samples[-3].point - section.samples[-1].point).normalized()

    # Store a reference to the primary child
    primary_child = None

    # The angle between the parent and child sections
    greatest_angle = 0

    # The radius of the greatest child
    greatest_radius = 0

    # Iterate over the children of the section
    for child in section.children:

        # If the radius of the first sample of the child is greater than the greatest radius,
        # then update it
        if child.samples[0].radius > greatest_radius:

            # Update the greatest radius
            greatest_radius = child.samples[0].radius

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

    # Create a new children list with update order, where the primary section comes first and the
    # secondary ones come later in the loop for the smooth continuation of the meshing
    children_list_with_updated_order = list()

    # Add the primary child as the first element in the list
    children_list_with_updated_order.append(primary_child)

    # Update the labels
    for child in section.children:

        # If this child is the primary child (compare the IDs, then set its label to primary)
        if child.id == primary_child.id:

            # Update the label
            child.is_primary = True

            # Set the radius of the primary child to the greatest
            child.samples[0].radius = greatest_radius

        # Otherwise, set it to secondary
        else:

            # Append the secondary child to the children list that has the new order
            children_list_with_updated_order.append(child)

            # Update the label
            child.is_primary = False

            # Set the radius of a secondary child to half of the primary branch
            child.samples[0].radius = greatest_radius * 0.25

    # Update the children list in the section
    section.children = children_list_with_updated_order

    # Update the radius of the last sample of the section according to the @greatest_radius to
    # match that of the first sample of the primary branch
    if section.samples[-1].radius < greatest_radius:
        section.samples[-1].radius = greatest_radius


####################################################################################################
# @label_primary_and_secondary_sections_based_on_angles_with_fixed_radii
####################################################################################################
def label_primary_and_secondary_sections_based_on_angles_with_fixed_radii(section):
    """Labels the children of the section to primary or secondary, based on the angles between the
    section, that is considered parent and the children. Note that the greater the angle is between
    the parent section and the child, the more primary the child is.

    NOTE: To avoid resampling artifacts, the radius of the parent section is UPDATED to match the
    greatest radius of the first sample of the children sections.

    :param section:
        A given section to set the order of its children to either primary or secondary.
    """

    # If the section does not have any children, then this filter is not valid
    if not section.has_children():

        # Return
        return

    # If this section is a root, then its primary by default
    if not section.has_parent():

        # Set the section to a primary
        section.is_primary = True

    # Get the vector of the parent section based on its last two samples
    parent_vector = (section.samples[-2].point - section.samples[-1].point).normalized()

    # Store a reference to the primary child
    primary_child = None

    # The angle between the parent and child sections
    greatest_angle = 0.0

    smallest_angle = 1e3

    # The radius of the greatest child
    greatest_radius = section.samples[-1].radius

    # The smallest radius
    smallest_radius = 1e3

    # Iterate over the children of the section
    for child in section.children:

        # If the radius of the first sample of the child is greater than the greatest radius,
        # then update it
        if child.samples[0].radius > greatest_radius:

            # Update the greatest radius
            greatest_radius = child.samples[0].radius

        # If the radius of the first sample of the child is smaller than the smallest radius,
        # then update it
        if child.samples[0].radius < smallest_radius:

            # Update the greatest radius
            smallest_radius = child.samples[0].radius

    # Iterate again over the children of the section
    for child in section.children:

        # Compute the vector of the child section based on its first two samples
        child_vector = (child.samples[1].point - child.samples[0].point)
        if child_vector.length > 0:
            child_vector = child_vector.normalized()

        # Compute the angle between the two vectors
        angle = parent_vector.angle(child_vector)

        if angle < smallest_angle:
            smallest_angle = angle

        # If the angle is greater than the greatest angle, then update the @primary_child reference
        if angle > greatest_angle:

            # Update the angle
            greatest_angle = angle

            # Update the primary child
            primary_child = child

    # Create a new children list with update order, where the primary section comes first and the
    # secondary ones come later in the loop for the smooth continuation of the meshing
    children_list_with_updated_order = list()

    # Add the primary child as the first element in the list
    children_list_with_updated_order.append(primary_child)

    # Update the labels
    for child in section.children:

        # If this child is the primary child (compare the IDs, then set its label to primary)
        if child.id == primary_child.id:

            # Update the label
            child.is_primary = True

            # Set the radius of the primary child to the greatest
            child.samples[0].radius = smallest_radius



        # Otherwise, set it to secondary
        else:

            # Append the secondary child to the children list that has the new order
            children_list_with_updated_order.append(child)

            # Update the label
            child.is_primary = False

            # Set the radius of a secondary child to half of the primary branch
            child.samples[0].radius = smallest_radius



    # Update the children list in the section
    section.children = children_list_with_updated_order

    # Update the radius of the last sample of the section according to the @greatest_radius to
    # match that of the first sample of the primary branch
    section.samples[-1].radius = smallest_radius


####################################################################################################
# @find_nearest_sample_along_section
####################################################################################################
def find_nearest_sample_along_section(point,
                                      section,
                                      nearest_sample_found=None):
    """Find the nearest sample along the given section to the given point.

    :param point:
        A given point in the three-dimensional space.
    :param section:
        A given section to search for the nearest sample along.
    :param nearest_sample_found:
        The current nearest sample found.
    :return:
        The nearest sample found along the section.
    """

    # If @nearest_sample_found is None, then set the initial sample along the section to it till
    # further notice
    if nearest_sample_found is None:
        nearest_sample_found = section.samples[0]

    for sample in section.samples:

        # Compute the distance between the point and the sample
        current_sample_to_point_distance = (point - sample.point).length

        # Compute the distance between the point and the @nearest_sample_found
        nearest_sample_to_point_distance = (point - nearest_sample_found.point).length

        # Compare
        if current_sample_to_point_distance < nearest_sample_to_point_distance:

            # Update the nearest sample
            nearest_sample_found = sample

    # Iterate over the children
    for child in section.children:

        # Find the nearest sample recursively
        nearest_sample_found = find_nearest_sample_along_section(point, child, nearest_sample_found)

    # Return a reference to the nearest sample
    return nearest_sample_found


####################################################################################################
# @find_nearest_apical_dendritic_sample_to_axon
####################################################################################################
def find_nearest_apical_dendritic_sample_to_axon(morphology,
                                                 nearest_sample=None):
    """Find the nearest sample along the apical dendrite to the axon.
    Therefore, the axon can be emanating from the apical dendrite and not directly from the soma.

    :param morphology:
        The morphology skeleton of the neuron.
    :param nearest_sample:
        A reference to the current nearest sample if exists.
    :return:
        The nearest sample along the apical dendrite to the axon initial sample.
    """

    # Ensure the presence of the apical dendrite
    if morphology.apical_dendrite is None:

        # If there is no apical dendrite, then return None!
        return None

    # Find the nearest sample between the axon initial segment and the apical dendrite
    nearest_sample = find_nearest_sample_along_section(
        morphology.axon.samples[0].point, morphology.apical_dendrite, nearest_sample)

    # Return the sample along the apical dendrite that it is very close the axon initial sample
    return nearest_sample


####################################################################################################
# @find_nearest_basal_dendritic_sample_to_axon
####################################################################################################
def find_nearest_basal_dendritic_sample_to_axon(morphology,
                                                nearest_sample=None):
    """Find the nearest sample along the basal dendrites to the axon.
    Therefore, the axon can be emanating from a basal dendrite and not directly from the soma.

    :param morphology:
        The morphology skeleton of the neuron.
    :param nearest_sample:
        A reference to the current nearest sample if exists.
    :return:
        The nearest sample along a basal dendrite to the axon initial sample.
    """

    # Iterate over the basal dendrites and apply the test
    for basal_dendrite in morphology.dendrites:

        # Find the nearest sample between the axon initial segment and the basal dendrite
        nearest_sample = find_nearest_sample_along_section(
            morphology.axon.samples[0].point, basal_dendrite, nearest_sample)

    # Return the sample along the basal dendrites that it is very close the axon initial sample
    return nearest_sample


####################################################################################################
# @find_nearest_dendritic_sample_to_axon
####################################################################################################
def find_nearest_dendritic_sample_to_axon(morphology):
    """Find the nearest dendrite to the axon in case if the axon was disconnected
    from the soma. Therefore, the axon can be emanating from a dendrite and not directly from the
    soma.

    :param morphology:
        The morphology skeleton of the neuron.
    :return:
        A reference to the arbor with which the axon is emanating from.
    """

    # A reference to the nearest sample found along the nearest dendrite
    # The initial value is set to None to indicate no samples found so far
    nearest_sample = None

    # If the apical dendrites exists, then check it.
    if morphology.apical_dendrite is not None:

        # Find the nearest sample between the axon initial segment and the apical dendrite
        nearest_sample = find_nearest_apical_dendritic_sample_to_axon(morphology, nearest_sample)

    # Find the nearest sample between the axon initial segment and the basal dendrites
    nearest_sample = find_nearest_basal_dendritic_sample_to_axon(morphology, nearest_sample)

    # Return the nearest sample on the dendritic tree to the axon initial sample
    return nearest_sample


####################################################################################################
# @find_nearest_apical_dendritic_sample_to_basal_dendrite
####################################################################################################
def find_nearest_apical_dendritic_sample_to_basal_dendrite(morphology,
                                                           basal_dendrite):
    """Find the nearest sample on the apical dendrite to the given basal dendrite.

    :param morphology:
        The morphology skeleton of the neuron.
    :param basal_dendrite:
        The basal dendrite.
    :return:
        The nearest sample on the apical dendrite to the given basal dendrite.
    """

    # Find the nearest sample between the dendrite initial sample and the apical dendrite
    nearest_sample = find_nearest_sample_along_section(
        point=basal_dendrite.samples[0].point, section=morphology.apical_dendrite)

    # Return the nearest sample found
    return nearest_sample


####################################################################################################
# @find_nearest_basal_dendritic_sample_to_basal_dendrite
####################################################################################################
def find_nearest_basal_dendritic_sample_to_basal_dendrite(morphology,
                                                          basal_dendrite):
    """Find the nearest sample on a basal dendrite to the given basal dendrite.

    :param morphology:
        The morphology skeleton of the neuron.
    :param basal_dendrite:
        The basal dendrite.
    :return:
        The nearest sample on a basal dendrite to the given one.
    """

    # A reference to the nearest sample found
    # The initial value is set to None to indicate no samples found so far
    nearest_sample = None

    for dendrite in morphology.dendrites:

        # If the @basal_dendrite is the same as the @dendrite, then skip the check
        if dendrite.id == basal_dendrite.id:
            continue

        # Find the nearest sample between the dendrite initial sample and the other basal dendrite
        nearest_sample = find_nearest_sample_along_section(
            point=basal_dendrite.samples[0].point, section=dendrite,
            nearest_sample_found=nearest_sample)

    # Return the nearest sample found
    return nearest_sample


################################################################################################
# @verify_axon_connection_to_soma
################################################################################################
def verify_axon_connection_to_soma(morphology):
    """Verify if the axon of a morphology is connected to its soma or not.

    If the initial segment of the axon is located far-away from the soma, the axon is connected
    to the closest dendrite. The intersection between the axon and the dendrites is checked,
    the axon is connected to the closest dendrite that is intersecting with it.

    :param morphology:
        The morphology skeleton of a neuron.
    """

    # Report the verification process
    nmv.logger.info('Axon connectivity to soma')

    # Ensure that presence of the axon in the morphology
    if morphology.axon is None:

        # Report the issue
        nmv.logger.detail('WARNING: This morphology does NOT have an axon')

        # Skip
        return

    # Is the axon disconnected from the soma !
    if is_arbor_disconnected_from_soma(morphology.axon):

        # Report the issue
        nmv.logger.detail('WARNING: The axon @ section [%d] is disconnected from the soma'
                          % morphology.axon.id)

        # Get the nearest arbor and sample to the axon initial segment
        nearest_sample = find_nearest_dendritic_sample_to_axon(morphology)

        # Report the repair
        nmv.logger.detail('REPAIRING: The axon is re-connected to section [%d, %s] @ sample [%s]'
                          % (nearest_sample.section.id, nearest_sample.section.get_type_string(),
                             str(nearest_sample.id)))

        # Mark the axon disconnected from the soma
        morphology.axon.connected_to_soma = False

        # Update the axon initial sample based on the nearest dendritic sample
        # The sample should have the same location
        morphology.axon.samples[0].point = nearest_sample.point

        # The sample should have a smaller radius to avoid the extrusion artifacts
        morphology.axon.samples[0].radius = nearest_sample.radius * 0.5

        # The axon is found not connected to the soma
        return

    # Is the axon intersecting with the apical dendrite, if exists !
    if morphology.apical_dendrite is not None:

        # Verify if the axon intersects with the apical dendrite
        if nmv.skeleton.ops.axon_intersects_apical_dendrite(
                axon=morphology.axon, apical_dendrite=morphology.apical_dendrite,
                soma_radius=morphology.soma.mean_radius):

            # Report the issue
            nmv.logger.detail(
                'WARNING: The axon @ section [%d] is intersecting with apical dendrite'
                % morphology.axon.id)

            # Find the intersection sample
            nearest_sample = find_nearest_apical_dendritic_sample_to_axon(morphology)

            # Report the repair
            nmv.logger.detail(
                'REPAIRING: The axon @ section [%d] is re-connected to section '
                '[%d, %s] @ sample [%s]' % (morphology.axon.id,
                                            nearest_sample.section.id,
                                            nearest_sample.section.get_type_string(),
                                            str(nearest_sample.id)))

            # Mark the axon disconnected from the soma
            morphology.axon.connected_to_soma = False

            # Update the axon initial sample based on the nearest dendritic sample
            # The sample should have the same location
            morphology.axon.samples[0].point = nearest_sample.point

            # The sample should have a smaller radius to avoid the extrusion artifacts
            morphology.axon.samples[0].radius = nearest_sample.radius * 0.5

            # The axon is found to be intersecting with the apical dendrite
            return

    # Is the axon intersecting with any basal dendrite !
    if nmv.skeleton.ops.axon_intersects_dendrites(
            axon=morphology.axon, dendrites=morphology.dendrites,
            soma_radius=morphology.soma.mean_radius):

        # Report the issue
        nmv.logger.detail('WARNING: The axon @ section [%d] is intersecting with a basal dendrite'
              % morphology.axon.id)

        # Find the intersection sample
        nearest_sample = find_nearest_basal_dendritic_sample_to_axon(
                morphology)

        # Report the repair
        nmv.logger.detail('REPAIRING: The axon is re-connected to section [%d, %s] @ sample [%s]'
              % (nearest_sample.section.id, nearest_sample.section.get_type_string(),
                 str(nearest_sample.id)))

        # Mark the axon disconnected from the soma
        morphology.axon.connected_to_soma = False

        # Update the axon initial sample based on the nearest dendritic sample
        # The sample should have the same location
        morphology.axon.samples[0].point = nearest_sample.point

        # The sample should have a smaller radius to avoid the extrusion artifacts
        morphology.axon.samples[0].radius = nearest_sample.radius * 0.5

        # The axon is found to be intersecting with the apical dendrite
        return

    # Mark the axon connected to the soma
    morphology.axon.connected_to_soma = True

    nmv.logger.detail('NOTE: The axon @ section [%d] is connected to the soma' % morphology.axon.id)


################################################################################################
# @verify_basal_dendrites_connection_to_soma
################################################################################################
def verify_basal_dendrites_connection_to_soma(morphology):
    """Verify if any basal dendrite is connected to the soma or not.

    NOTE: The apical dendrite is always assumed to be connected to the soma since its large
    enough and can be very tough for the experimentalist to miss it.

    To resolve the connectivity issue, we compute from the profile points the most far point and
    consider it the maximum distance a branch can get extended to.

    :param morphology:
        A given morphology skeleton.
    """

    # Get the distance between the soma origin and most far profile point
    maximum_arbor_distance = morphology.soma.largest_radius

    # If the morphology has no basal dendrites
    if morphology.dendrites is None:

        # Return
        return

    # Verify dendrite by dendrite
    for i_basal_dendrite, basal_dendrite in enumerate(morphology.dendrites):

        nmv.logger.info('Basal dendrite [%d] connectivity to soma' % i_basal_dendrite)

        # If the basal dendrite is starting inside the soma, then disconnect it
        # NOTE: The negative sample must be removed a priori for this filter to work
        if is_arbor_starting_inside_soma(basal_dendrite, 0.5 * morphology.soma.mean_radius):

            # Mark the basal dendrite DISCONNECTED from the soma
            basal_dendrite.connected_to_soma = False

            # Report the issue
            nmv.logger.detail('WARNING: The basal dendrite [%d] is disconnected [INSIDE] from '
                              'soma' % i_basal_dendrite)

            # Next arbor
            continue

        # Is the basal dendrite disconnected from the soma !
        if is_arbor_disconnected_from_soma(basal_dendrite, threshold=maximum_arbor_distance):

            # Mark the basal dendrite DISCONNECTED from the soma
            basal_dendrite.connected_to_soma = False

            # Report the issue
            nmv.logger.detail('WARNING: The basal dendrite [%d] is disconnected [FAR] from soma'
                              % i_basal_dendrite)

            # Report the repair
            nmv.logger.detail('REPAIRING: The basal dendrite [%d] @ section [%d] is re-connected '
                              'to the soma' % (i_basal_dendrite, basal_dendrite.id))

            # Get the direction of the initial sample of the basal dendrite
            basal_dendrite.samples[0].point = \
                basal_dendrite.samples[0].point.normalized() * maximum_arbor_distance

            # Mark the basal dendrite CONNECTED from the soma
            basal_dendrite.connected_to_soma = True

            # Done, next basal dendrite
            continue

        # Mark the basal dendrite connected to the soma
        basal_dendrite.connected_to_soma = True

        nmv.logger.detail('NOTE: The basal dendrite [%d] @ section [%d] is connected to the soma' %
                          (i_basal_dendrite, basal_dendrite.id))

    for i_basal_dendrite, basal_dendrite in enumerate(morphology.dendrites):

        # Verify if the axon intersects with the apical dendrite
        if nmv.skeleton.ops.dendrite_intersects_apical_dendrite(
                dendrite=basal_dendrite,
                apical_dendrite=morphology.apical_dendrite,
                soma_radius=morphology.soma.mean_radius):

            # Mark the basal dendrite connected to the soma
            basal_dendrite.connected_to_soma = False

            continue

        # Is the basal dendrite intersecting with another basal dendrite !
        # NOTE: The intersection function returns a positive result if this input basal
        # dendrite is intersecting with another basal dendrite with largest radius
        if nmv.skeleton.ops.basal_dendrite_intersects_basal_dendrite(
                dendrite=basal_dendrite, dendrites=morphology.dendrites,
                soma_radius=morphology.soma.mean_radius):

            # Mark the basal dendrite connected to the soma
            basal_dendrite.connected_to_soma = False

            continue


################################################################################################
# @update_arbors_connection_to_soma
################################################################################################
def update_arbors_connection_to_soma(morphology):
    """Verify if the different arbors of the morphology are connected to the soma or not.
    The apical dendrite is always assumed to be connected to the soma since its large.
    We then check the connectivity of the axon and the basal dendrites one by one.

    :param morphology:
        A given morphology skeleton.
    """

    # If the apical dendrite exists, then set its connectivity to True directly
    if morphology.apical_dendrite is not None:
        morphology.apical_dendrite.connected_to_soma = True

    # Verify the connectivity of the basal dendrites
    if morphology.dendrites is not None:
        verify_basal_dendrites_connection_to_soma(morphology=morphology)

    # Verify the connectivity of the axon
    if morphology.axon is not None:
        verify_axon_connection_to_soma(morphology=morphology)


####################################################################################################
# @connect_single_child
####################################################################################################
def connect_single_child(section):
    """
    If the given section has only one child, then connect this child directly to the parent and
    update the skeleton.
    NOTE: The replicated sample (at the bifurcation point) must be removed.

    :param section:
        A section to repair.
    """

    # Ensure that the section has only a single child
    if len(section.children) == 1:

        # Get the samples of the 'ONLY' child section
        child_samples = section.children[0].samples

        # Update the parent samples
        for i, sample in enumerate(child_samples):

            # Skip the bifurcation sample
            if i == 0:
                continue

            # Append the sample to the parent samples
            section.samples.append(sample)

        # Update the morphology skeleton
        section.children = section.children[0].children

        # Update the section number of children
        section.children = []

        # Update the IDs of the children
        section.children_ids = []


####################################################################################################
# @connect_arbor_to_soma
####################################################################################################
def connect_arbor_to_soma(soma_mesh,
                          arbor):
    """
    Connects the root section of a given arbor to the soma at its initial segment.
    This function checks if the arbor mesh is 'logically' connected to the soma or not, following
    to the initial validation steps that determines if the arbor has a valid connection point to
    the soma or not.
    If the arbor is 'logically' connected to the soma, this function returns immediately.
    The arbor is a Section object, see Section() @ section.py.

    :param soma_mesh:
        The mesh object of the soma.
    :param arbor:
        The mesh object of the arbor.
    :return:
    """

    # If the arbor is not valid
    if arbor is None:

        # Return
        return

    # Verify if the arbor is connected to the soma or not
    if not arbor.connected_to_soma:
        nmv.logger.log('\t\t * WARNING: The neurite [%s: %d] is not connected to the soma' %
              (arbor.get_type_string(), arbor.id))
        return

    # Clip the auxiliary section using a cutting plane that is normal on the branch
    # Get the intersection point between the soma and the apical dendrite
    branch_starting_point = arbor.samples[0].point
    branch_direction = arbor.samples[0].point.normalized()
    intersection_point = branch_starting_point - 0.75 * branch_direction

    """
    # TODO: This clipping approach is not valida with newer versions of blender! 
    # Construct a clipping plane and rotate it towards the origin
    # plane_name = 'intersection_plane_%d' % arbor.id
    clipping_plane = mesh_objects.create_plane(
        radius=2.0, location=intersection_point, name=plane_name)
    nmv.mesh.ops.rotate_face_towards_point(clipping_plane, Vector((0, 0, 0)))

    # Clip the arbor mesh and return a reference to the result
    section_mesh = nmv.mesh.ops.intersect_mesh_objects(arbor.mesh, clipping_plane)
    
    # Delete the clipping plane to clean the scene
    nmv.scene.ops.delete_list_objects([clipping_plane])
    """

    # Get the nearest face on the mesh surface to the intersection point
    soma_mesh_face_index = nmv.mesh.ops.get_index_of_nearest_face_to_point(
        soma_mesh, intersection_point)

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Select the soma object
    nmv.scene.ops.select_objects([soma_mesh])

    # Select the face using its obtained index
    nmv.mesh.ops.select_face_vertices(soma_mesh, soma_mesh_face_index)

    # Select the section mesh
    nmv.scene.ops.select_objects([arbor.mesh])

    # Deselect all the vertices of the section mesh, for safety !
    nmv.mesh.ops.deselect_all_vertices(arbor.mesh)

    # Get the nearest face on the section mesh
    section_face_index = nmv.mesh.ops.get_index_of_nearest_face_to_point(
        arbor.mesh, intersection_point)

    # Select the face
    nmv.mesh.ops.select_face_vertices(arbor.mesh, section_face_index)

    # Apply a joint operation, for the moment, use 'neuron' as the mesh object, since it will
    # be changed later
    soma_mesh = nmv.mesh.ops.join_mesh_objects([soma_mesh, arbor.mesh], name=soma_mesh.name)

    # Toggle to the edit mode to be able to apply the edge loop operation
    bpy.ops.object.editmode_toggle()

    # Apply the bridging operator
    bpy.ops.mesh.bridge_edge_loops()

    # Smooth the connection
    bpy.ops.mesh.faces_shade_smooth()

    # Switch back to object mode, to be able to export the mesh
    bpy.ops.object.editmode_toggle()

    # Select all the vertices of the final mesh
    nmv.mesh.ops.select_all_vertices(soma_mesh)

    # Deselect all the vertices of the parent mesh, for safety reasons
    nmv.mesh.ops.deselect_all_vertices(soma_mesh)


####################################################################################################
# @get_soma_to_root_section_connection_extent
####################################################################################################
def get_soma_to_root_section_connection_extent(section):
    """Get a sphere object reflecting the extent (or the space) between a root section and the soma.

    NOTE: The function assumes that the section is ROOT and is ALREADY connected to the soma. If
    this is not the case, the result might be wrong.

    :param section:
        A given root section that is supposed to be connected to the soma.
    :return:
        A sphere [center, radius] representing the extent between the section and the soma.
    """

    # Get section direction
    direction = section.samples[0].point.normalized()

    # The extent is simply a sphere with a center and radius, and therefore we will assume that
    # the center is 0.5 microns far from the initial sample on the section
    delta = 0.5
    extent_center = section.samples[0].point - (direction * delta)

    # Extent radius is a bit greater than double the radius of the first sample along the section
    extent_radius = section.samples[0].radius * 2.5

    # Return the extent center and the extent radius
    return extent_center, extent_radius


################################################################################################
# @get_connection_extents
################################################################################################
def get_soma_to_root_sections_connection_extent(morphology):
    """Return the extents (or regions where the root sections are connected to the soma).

    :return:
        A list of spheres reflecting the extents of the connections between the root sections
        and the soma.
    """

    # Initialize the list
    connection_extents = list()

    # Apical dendrite
    if morphology.apical_dendrite is not None:

        # Only if the apical is connected
        if morphology.apical_dendrite.connected_to_soma:

            # Get the extent
            extent_center, extent_radius = get_soma_to_root_section_connection_extent(
                morphology.apical_dendrite)

            # Append this extent to the list
            connection_extents.append([extent_center, extent_radius])

    # Apical dendrite
    if morphology.axon is not None:

        # Only if the axon is connected
        if morphology.axon.connected_to_soma:

            # Get the extent
            extent_center, extent_radius = get_soma_to_root_section_connection_extent(
                    morphology.axon)

            # Append this extent to the list
            connection_extents.append([extent_center, extent_radius])

    # Basal dendrite s
    if morphology.dendrites is not None:

        # For each dendrite
        for dendrite in morphology.dendrites:

            # Only if the dendrite is connected
            if dendrite.connected_to_soma:

                # Get the extent
                extent_center, extent_radius = get_soma_to_root_section_connection_extent(dendrite)

                # Append this extent to the list
                connection_extents.append([extent_center, extent_radius])

    # Return a reference to the list
    return connection_extents


####################################################################################################
# @get_stable_soma_extent
####################################################################################################
def get_stable_soma_extent(morphology):
    """
    This function will return an extent (or a sphere) that reflects the stable zone around the
    soma, where we cannot apply the same noise texture applied to the rest of the arbors.
    It checks the most far connected branch to the soma and then returns the sphere based on its
    distance.

    :param morphology:
        A given morphology to get its stable extent.
    :return:
        The center and radius of the sphere that represents the stable extent.
    """

    # The distance to the most far branch
    largest_distance = 0

    # Apical dendrite
    if morphology.apical_dendrite is not None:

        # Compare the initial sample of the first segment of the apical dendrite
        distance = morphology.apical_dendrite.samples[0].point.length + \
                   morphology.apical_dendrite.samples[0].radius
        if distance > largest_distance:

            # Update the largest distance
            largest_distance = distance

    # Basal dendrites
    if morphology.dendrites is not None:
        for dendrite in morphology.dendrites:

            # Ensure that this basal dendrite is connected to the soma
            if dendrite.connected_to_soma:

                # Compare the initial sample of the first segment of the basal dendrite
                distance = dendrite.samples[0].point.length + dendrite.samples[0].radius
                if distance > largest_distance:

                    # Update the largest distance
                    largest_distance = distance

    # Axon
    if morphology.axon is not None:

        # Compare the initial sample of the first segment of the axon
        distance = morphology.axon.samples[0].point.length + \
                   morphology.axon.samples[0].radius
        if distance > largest_distance:

            # Ensure that this axon is connected to the soma
            if morphology.axon.connected_to_soma:

                # Update the largest distance
                largest_distance = distance

    # Return the extent, and add 1 micron for safety
    return Vector((0.0, 0.0, 0.0)), largest_distance + 1.0


####################################################################################################
# @is_point_located_within_extents
####################################################################################################
def is_point_located_within_extents(point,
                                    extents):
    """
    Checks if a given point is located with a list of given extents.

    :param point:
        A point along the mesh.
    :param extents:
        A list of extents [centers, radii]
    :return:
        True or False.
    """

    # Check the presence of the point inside the extents
    for extent in extents:

        # Get the data from the list
        extent_center = extent[0]
        extent_radius = extent[1]

        # If the point is located inside the extent, return True
        if nmv.geometry.ops.is_point_inside_sphere(extent_center, extent_radius, point):
            return True

    # No, the point is not located inside the extent
    return False


####################################################################################################
# @update_secondary_arbor_starting_point_to_avoid_intersection
####################################################################################################
def update_secondary_arbor_starting_point_to_avoid_intersection(secondary_poly_line,
                                                                primary_mesh,
                                                                delta):
    """

    :param secondary_poly_line:
    :param primary_mesh:
    :param delta:
    :return:
    """

    # Get the length of the secondary poly-line
    secondary_poly_line_length = nmv.skeleton.ops.get_poly_line_length(secondary_poly_line)

    first_distance = secondary_poly_line.data.splines.active.points[0].radius * 2

    # check in advance if the distance works or not
    initial_starting_factor = nmv.skeleton.ops.get_poly_line_normalized_start_factor(
        first_distance, secondary_poly_line_length)

    # Update the starting factor of the secondary poly-line
    secondary_poly_line.data.bevel_factor_start = initial_starting_factor

    if nmv.skeleton.ops.poly_line_intersect_mesh(
            poly_line=secondary_poly_line, mesh=primary_mesh):

        # Trial and error
        for i in range(1, 100):

            # Get the starting factor
            factor = initial_starting_factor + (delta * i)

            starting_factor = nmv.skeleton.ops.get_poly_line_normalized_start_factor(
                factor, secondary_poly_line_length)

            # Update the starting factor of the secondary poly-line
            secondary_poly_line.data.bevel_factor_start = starting_factor

            # If the two poly-lines do not intersect, then RETURN
            if nmv.skeleton.ops.poly_line_intersect_mesh(
                    poly_line=secondary_poly_line, mesh=primary_mesh):
                continue
            else:
                return
    else:
        return


####################################################################################################
# @bridge_arbor_poly_line_to_skeleton_mesh
####################################################################################################
def bridge_arbor_poly_line_to_skeleton_mesh(arbor_poly_line,
                                            skeleton_mesh,
                                            connecting_point):
    """

    :param arbor_poly_line:
    :param skeleton_mesh:
    :param connecting_point:
    :return:
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    factor = arbor_poly_line.data.splines.active.points[0].radius
    update_secondary_arbor_starting_point_to_avoid_intersection(arbor_poly_line, skeleton_mesh,
                                                                factor)
    mesh_object_1 = skeleton_mesh

    # Now, we can safely convert the arbor to a mesh
    mesh_object_2 = nmv.scene.ops.convert_object_to_mesh(arbor_poly_line)


    # Select mesh_object_1 and set it to be the active object
    bpy.context.scene.objects.active = mesh_object_1

    # Close all the open faces (including the caps) to ensure that there are no holes in the mesh
    # mesh_face_ops.close_open_faces(mesh_object_1)

    # Get the nearest face to the starting point
    indices = nmv.mesh.ops.get_indices_of_nearest_faces_to_point_within_delta(
        mesh_object_1, connecting_point[0])
    nearest_face_index_on_mesh_1 = nmv.mesh.ops.get_index_of_nearest_face_to_point_in_faces(
        mesh_object_1, indices, connecting_point[1])

    # Get the nearest face to the morphology sample
    #nearest_face_index_on_mesh_1 = mesh_face_ops.get_index_of_nearest_face_to_point(
        #mesh_object_1, connecting_point)

    # Select this face
    nmv.mesh.ops.select_face_vertices(mesh_object_1, nearest_face_index_on_mesh_1)

    # Deselect mesh_object_1
    mesh_object_1.select = False

    # Select mesh_object_2 and set it to be the active object
    mesh_object_2.select = True

    # Close all the open faces (including the caps) to ensure that there are no holes in the mesh
    nmv.mesh.ops.close_open_faces(mesh_object_2)

    # Get the nearest face to the bridging point
    nearest_face_index_on_mesh_2 = nmv.mesh.ops.get_index_of_nearest_face_to_point(
        mesh_object_2, connecting_point[1])

    # Select this face
    nmv.mesh.ops.select_face_vertices(mesh_object_2, nearest_face_index_on_mesh_2)

    # Select mesh_object_1 and mesh_object_2
    mesh_object_1.select = True
    mesh_object_2.select = True

    # Set the mesh_object_1 to be active
    bpy.context.scene.objects.active = mesh_object_1

    # Set tha parenting order, the parent mesh is becoming an actual parent
    bpy.ops.object.parent_set()

    # Join the two meshes in one mesh
    bpy.ops.object.join()

    # Switch to edit mode to be able to implement the bridging operator
    bpy.ops.object.editmode_toggle()

    # apply the bridging operator
    bpy.ops.mesh.bridge_edge_loops()

    # switch back to object mode
    bpy.ops.object.editmode_toggle()

    # Deselect all the vertices of the parent mesh, mesh_object_1
    nmv.mesh.ops.deselect_all_vertices(mesh_object_1)


####################################################################################################
# @bridge_mesh_objects_in_list
####################################################################################################
def bridge_arbors_to_skeleton_mesh(arbors_poly_line_list,
                                   connecting_points_list):
    """

    :param arbors_poly_line_list:
    :param connecting_points_list:
    :return:
    """

    # The first arbor in the list is ALWAYS the primary arbor, therefor it does NOT require any
    # processing of intersection test. This arbor will be converted from a poly-line to a mesh
    # to form the basis of the skeleton mesh of the arbor and the rest of the poly-lines will be
    # later bridged to it.
    arbor_skeleton_mesh = nmv.scene.ops.convert_object_to_mesh(arbors_poly_line_list[0])

    # Iterate over the reset of the arbors in the list to bridge them
    for i in range(len(arbors_poly_line_list) - 1):

        # Get a reference to the secondary arbor poly-line
        secondary_arbor_poly_line = arbors_poly_line_list[i + 1]

        # Get the connecting point
        connecting_point = connecting_points_list[i + 1]

        # Bridge the arbor poly-line to the skeleton mesh
        bridge_arbor_poly_line_to_skeleton_mesh(
            arbor_poly_line=secondary_arbor_poly_line, skeleton_mesh=arbor_skeleton_mesh,
            connecting_point=connecting_point)

    # Return
    return arbor_skeleton_mesh


####################################################################################################
# @get_random_spines_on_section
####################################################################################################
def get_random_spines_on_section(current_branching_level,
                                 max_branching_level,
                                 section,
                                 probability=5.0,
                                 spines_list=[]):
    """Gets the data of some random spines on a given section.

    NOTE: The generated spines are totally random and does not follow any rules for growing the
    spines, they are just used for artistic purposes.

    :param current_branching_level:
        A list of ONLY one item to keep track on the current branching level recursively.
    :param max_branching_level:
        The maximum branching level of a neuron.
    :param section:
        A given section to generate the spines for.
    :param probability:
        The probability of growing spine at a certain sample.
    :param spines_list:
        The list that integrates the generated spines recursively.
    """

    # If this section is axon, the return and don't add any spines
    if section.is_axon():
        return

    # If the current branching level is greater than the maximum one, exit
    if current_branching_level[0] > max_branching_level:
        return

    # Increment the branching level
    current_branching_level[0] += 1

    for i, sample in enumerate(section.samples):

        # If this is the first or last sample, ignore it since they normally intersect children
        # and parent sections
        if i < 2 or i > len(section.samples) - 2:
            continue

        # Random spines
        if probability > random.uniform(0.0, 1.0) * 100:

            # Get the position of sample
            sample_position = sample.point

            # Get the section size at this sample (corresponding to the radius of the sample)
            sample_radius = sample.radius

            # The post synaptic position is the sample position
            post_synaptic_position = sample_position

            # The pre-synaptic position is computed based on the samples i-1 and i+1
            p0 = section.samples[i - 1].point
            p1 = section.samples[i].point
            p2 = section.samples[i + 1].point

            # Get the vectors
            v1 = p0 - p1
            v2 = p2 - p1

            # Compute the pre-synaptic direction
            pre_synaptic_direction = v1.cross(v2)

            # Compute a random pre-synaptic position
            pre_synaptic_position = post_synaptic_position + (pre_synaptic_direction * 1.0)

            # Create the spine
            spine = nmv.skeleton.Spine()
            spine.post_synaptic_position = post_synaptic_position
            spine.pre_synaptic_position = pre_synaptic_position
            spine.size = sample_radius
            spines_list.append(spine)
