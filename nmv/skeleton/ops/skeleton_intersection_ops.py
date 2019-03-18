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


####################################################################################################
# @branches_intersect
####################################################################################################
def branches_intersect(branch_1,
                       branch_2,
                       soma_radius):
    """Check if the given branches intersect at their connections with the soma or not.
    Since the two branches would not be exactly located at the given soma radius, therefore, a good
    intersection test requires mapping their initial segments to the initial
    soma sphere at the given soma radius and then applying the default intersection test.

    :param branch_1:
        The first branch.
    :param branch_2:
        The second branch.
    :param soma_radius:
        The radius of the soma.
    :return:
        True or False.
    """

    # Get the initial segment (is) points of the two branches
    is_point_1 = branch_1.samples[0].point
    is_point_2 = branch_2.samples[0].point

    # Get the initial segments radii of the two branches
    is_radius_1 = branch_1.samples[0].radius
    is_radius_2 = branch_2.samples[0].radius

    # Get the directions of the initial segments of the two branches
    is_direction_1 = is_point_1.normalized()
    is_direction_2 = is_point_2.normalized()

    # Compute the mapping radii (i.e. the scale required to connect the branch to the soma radius)
    scaled_point_1 = is_direction_1 * soma_radius
    scaled_point_2 = is_direction_2 * soma_radius

    # Compute the scaled radii based on [ tan(angle) = r1/x1 = r2/x2 ]
    scaled_radius1 = is_radius_1 * (scaled_point_1.length / is_point_1.length)
    scaled_radius2 = is_radius_2 * (scaled_point_2.length / is_point_2.length)

    # Compute the arc distance between the two scaled points
    arc_length = scaled_point_1.angle(scaled_point_2) * soma_radius

    # If the distance between the centers is less than the radii sum, then they intersect
    if arc_length < (scaled_radius1 + scaled_radius2) :

        # Positive intersection
        return True

    # Negative intersection, the branches do not intersect at all
    return False


####################################################################################################
# @profile_points_intersect
####################################################################################################
def profile_points_intersect(point_1,
                             point_2,
                             index_1,
                             index_2,
                             soma_radius,
                             profile_point_radius=1.0):
    """
    This function checks if the given profile points intersect along the soma or not.

    :param point_1:
        The first profile point.
    :param point_2:
        The second profile point.
    :param index_1:
        The index of the first profile point in the original list.
    :param index_2:
        The index of the second profile point in the original list.
    :param soma_radius:
        The radius of the soma.
    :param profile_point_radius:
        The radius of the profile point, default 1.0 micron.
    :return:
        True or False.
    """

    # Initial segments (is) directions
    is_direction_1 = point_1.normalized()
    is_direction_2 = point_2.normalized()

    # Compute the map (scale to connect the branch to the soma radius)
    scaled_point_1 = is_direction_1 * soma_radius
    scaled_point_2 = is_direction_2 * soma_radius

    # Compute the scaled radii based on [ tan(angle) = r1/x1 = r2/x2 ]
    scaled_radius_1 = profile_point_radius * (scaled_point_1.length / point_1.length)
    scaled_radius_2 = profile_point_radius * (scaled_point_2.length / point_2.length)

    # Compute the arc distance between the two scaled points
    arc_length = scaled_point_1.angle(scaled_point_2) * soma_radius

    # If the distance between the centers is less than the radii sum, then they intersect
    if arc_length < (scaled_radius_1 + scaled_radius_2):

        # Positive intersection, but check the indices to avoid duplication
        if index_2 > index_1:

            # Positive intersection
            return True

    # Negative intersection
    return False


####################################################################################################
# @profile_point_intersect_other_point
####################################################################################################
def profile_point_intersect_other_point(profile_point,
                                        profile_point_index,
                                        profile_points,
                                        soma_radius):
    """
    This function checks if the profile point intersects any other profile point or not.

    :param profile_point:
        A given primary profile point.
    :param profile_point_index:
        The index of the given profile point. This index is required to check the order of the
        intersection, which will be used to avoid duplications.
    :param profile_points:
        A list of all the profile points of the soma, to be able to get the secondary points.
    :param soma_radius:
        The radius of the soma.
    :return:
        True or False.
    """

    # Repeat this operation for every profile point
    # NOTE: The given profile point is the primary profile point and therefore it has priority and
    # the other profile points given in the list 'profile_points' are secondary.
    for i, secondary_profile_point in enumerate(profile_points):

        # Check if the primary and the secondary profile points intersect or not.
        if profile_points_intersect(
                profile_point, secondary_profile_point, profile_point_index, i, soma_radius):

            # Positive intersection
            return True

    # Negative intersection
    return False


####################################################################################################
# @point_branch_intersect
####################################################################################################
def point_branch_intersect(point,
                           branch,
                           soma_radius,
                           profile_point_radius=2.5):
    """
    This function checks if the given point intersects with the given branch at the soma or not.

    :param point:
        A given profile point of the soma.
    :param branch:
        A given branch (or arbor) of the neuron.
    :param soma_radius:
        The radius of the soma.
    :param profile_point_radius:
        The radius of the profile point, default 1.0 micron.
    :return:
        True or False.
    """

    # Get a reference to the first sample of the initial segment of the branch and the profile point
    branch_point = branch.samples[0].point
    profile_point = point

    # Get their radii, assuming that the profile point radius is set to 1.0
    branch_radius = branch.samples[0].radius

    # Get their directions
    branch_point_direction = branch_point.normalized()
    profile_point_direction = profile_point.normalized()

    # Compute the map (scale to connect the branch to the soma radius)
    branch_scaled_point = branch_point_direction * soma_radius
    profile_scaled_point = profile_point_direction * soma_radius

    # Compute the scaled radii based on [ tan(angle) = r1/x1 = r2/x2 ]
    branch_point_scaled_radius = branch_radius * (branch_scaled_point.length / branch_point.length)
    profile_point_scaled_radius = profile_point_radius * \
                                  (profile_scaled_point.length / profile_point.length)

    # Compute the arc distance between the two scaled points
    arc_length = branch_scaled_point.angle(profile_scaled_point) * soma_radius

    # If the distance between the centers is less than the radii sum, then they intersect
    if arc_length < (branch_point_scaled_radius + profile_point_scaled_radius):

        # Positive intersection
        return True

    # Negative intersection
    return False


###################################################################################################
# @axon_intersects_dendrites
####################################################################################################
def axon_intersects_dendrites(axon,
                              dendrites,
                              soma_radius):
    """
    This function checks if the axon intersects with any basal dendrite or not.

    :param axon:
        The axon of the neuron.
    :param dendrites:
        A list of all the basal dendrites of the neuron.
    :param soma_radius:
        The radius of the soma.
    :return:
        True or False.
    """

    # Check if the axon intersects with any dendrite
    for dendrite in dendrites:

        # Branch intersection test
        if branches_intersect(dendrite, axon, soma_radius):

            # Intersection happens
            return True

    # No intersection
    return False


####################################################################################################
# @axon_intersects_apical_dendrite
####################################################################################################
def axon_intersects_apical_dendrite(axon,
                                    apical_dendrite,
                                    soma_radius):
    """
    This function checks if a given axon intersects with the apical dendrite, if exists.

    :param axon:
        The given axon of the neuron.
    :param apical_dendrite:
        The apical dendrite of the neuron, if it exists.
    :param soma_radius:
        The radius of the soma of the neuron.
    :return:
        True or False.
    """

    # If the apical dendrite exists, then proceed with the check
    if apical_dendrite is not None:

        # Is the axon intersecting with the apical dendrite or not
        return branches_intersect(axon, apical_dendrite, soma_radius)

    # Otherwise, return False if the apical dendrite does not exist in the morphology
    return False


####################################################################################################
# @dendrite_intersects_apical_dendrite
####################################################################################################
def dendrite_intersects_apical_dendrite(dendrite,
                                        apical_dendrite,
                                        soma_radius):
    """
    This function checks if a given basal dendrite intersects with the apical dendrite, if exists.

    :param dendrite:
        The given basal dendrite of the neuron.
    :param apical_dendrite:
        The apical dendrite of the neuron, if it exists.
    :param soma_radius:
        The radius of the soma of the neuron.
    :return:
        True or False.
    """

    # If the apical dendrite exists, then proceed with the check
    if apical_dendrite is not None:

        # Is the basal dendrite intersecting with the apical dendrite or not
        return branches_intersect(dendrite, apical_dendrite, soma_radius)

    # Otherwise, return False if the apical dendrite does not exist in the morphology
    return False


####################################################################################################
# @basal_dendrite_intersects_basal_dendrite
####################################################################################################
def basal_dendrite_intersects_basal_dendrite(dendrite,
                                             dendrites,
                                             soma_radius):
    """
    Checks if a given 'or primary' dendrite intersects with a thicker one.

    :param dendrite:
        A given primary dendrite.
    :param dendrites:
        A list of the other dendrites of the neuron (secondary).
    :param soma_radius:
        The radius of the soma of the neuron.
    :return:
        True or False.
    """

    # Check if the primary dendrite intersects with any of the other secondary dendrites
    for secondary_dendrite in dendrites:

        # The dendrite cannot intersect with itself, continue
        if dendrite.id == secondary_dendrite.id:
            continue

        # Check the intersection between the primary and the secondary dendrites
        if branches_intersect(dendrite, secondary_dendrite, soma_radius):

            # If the radius of the primary dendrite is less than the secondary one, then the
            # intersection is true
            primary_radius = dendrite.samples[0].radius
            secondary_radius = secondary_dendrite.samples[0].radius

            # Compare the radii
            if primary_radius < secondary_radius:

                # The primary dendrite intersects with the secondary one and has less radius,
                # then the intersection exists
                return True

    # No intersection
    return False


