####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
import time

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Internal imports
import nmv.bmeshi
import nmv.enums
import nmv.geometry
import nmv.mesh
import nmv.scene
import nmv.skeleton
import nmv.utilities
import nmv.consts


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
    greatest_radius = nmv.consts.Math.MINUS_INFINITY

    # Iterate over the children of the section
    for child in section.children:

        # If the radius of the child is greater than the greatest radius, then refer to this
        # child to be the primary child
        if len(child.samples) > 0:
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
        if child.index == primary_child.index:

            # Set this section to be the primary
            child.is_primary = True

        # Otherwise, set it to secondary
        else:

            # Set it to be a secondary section
            child.is_primary = False

            # Set the radius of a secondary child to half of the primary branch, for clean branching
            if len(child.samples) > 0:
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
        return

    # If this section is a root, then its primary by default
    if not section.has_parent():

        # Set the section to a primary
        section.is_primary = True

    # If the section has less than two samples
    if len(section.samples) < 2:
        return

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

        # The vectors must have non zero length
        if child_vector.length > 0.0 and parent_vector.length > 0.0:

            # Compute the angle between the two vectors
            angle = parent_vector.angle(child_vector)

            # If the angle is greater than the greatest angle, then update
            # the @primary_child reference
            if angle > greatest_angle:

                # Update the angle
                greatest_angle = angle

                # Update the primary child
                primary_child = child
        else:
            return

    # Create a new children list with update order, where the primary section comes first and the
    # secondary ones come later in the loop for the smooth continuation of the meshing
    children_list_with_updated_order = list()

    # Add the primary child as the first element in the list
    children_list_with_updated_order.append(primary_child)

    # Update the labels
    for child in section.children:

        # If this child is the primary child (compare the IDs, then set its label to primary)
        if child.index == primary_child.index:

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

    # If the section has less than two samples
    if len(section.samples) < 2:
        section.is_primary = False
        return

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
        if child.index == primary_child.index:

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
# @verify_arbor_proximity_to_soma
####################################################################################################
def verify_arbor_proximity_to_soma(arbor,
                                   soma):
    """Validates the proximity of a given arbor to the given soma. If the arbor is too far, then
    probably, it is NOT connected to the soma, otherwise it is.
    This function simply updates the self.far_from_soma  flag of the given arbor

    :param arbor:
        A given arbor of the morphology to check.
    :param soma:
        The soma of the morphology.
    """

    # TODO: Fix this based on some algorithm -> nmv.consts.Skeleton.MAXIMUM_SOMA_RADIUS_REPORTED
    # We must find a convenient algorithm to handle this issue
    if (arbor.samples[0].point - soma.centroid).length < soma.largest_radius * 4:
        arbor.far_from_soma = False


####################################################################################################
# @verify_arbors_connectivity_to_soma
####################################################################################################
def verify_arbors_connectivity_to_soma(morphology):
    """Validates the proximity of the arbors to the soma. If the arbor is too far, then probably it
     is NOT connected to the soma, otherwise it is.

    :param morphology:
        A given morphology skeleton.
    """

    # Apical dendrites
    if morphology.has_apical_dendrites():
        for arbor in morphology.apical_dendrites:
            verify_arbor_proximity_to_soma(arbor=arbor, soma=morphology.soma)

    # Basal dendrites
    if morphology.has_basal_dendrites():
        for arbor in morphology.basal_dendrites:
            verify_arbor_proximity_to_soma(arbor=arbor, soma=morphology.soma)

    # Axons
    if morphology.has_axons():
        for arbor in morphology.axons:
            verify_arbor_proximity_to_soma(arbor=arbor, soma=morphology.soma)


####################################################################################################
# @connect_single_child
####################################################################################################
def connect_single_child(section):
    """If the given section has only one child, then connect this child directly to the parent and
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
# @connect_arbor_to_meta_ball_soma
####################################################################################################
def connect_arbor_to_meta_ball_soma(soma_mesh,
                                    arbor):
    """This function is supposed to handle connecting a soma mesh to an arbor.

    :param soma_mesh:
        A given soma mesh.
    :param arbor:
        A given arbor to be connected to the mesh.
    :return:
        Reference to the soma after connection.
    """

    # If the soma mesh is not valid, then return
    if soma_mesh is None:
        return

        # If the arbor is not valid, then return
    if arbor is None:
        return

    # Simply apply a union operation between the soma and the arbor
    soma_mesh = nmv.mesh.union_mesh_objects(soma_mesh, arbor.mesh)

    # Remove the doubles
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')

    nmv.utilities.disable_std_output()
    bpy.ops.mesh.remove_doubles()
    nmv.utilities.enable_std_output()

    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.editmode_toggle()

    # Delete the other mesh
    nmv.scene.ops.delete_object_in_scene(arbor.mesh)

    # Return a reference to the soma mesh to be used later to do it for the rest of the arbors
    return soma_mesh


####################################################################################################
# @connect_arbor_to_meta_ball_soma
####################################################################################################
def connect_arbors_to_meta_ball_soma(soma_mesh,
                                     arbors_mesh):
    """This function is supposed to handle connecting a soma mesh to an arbor.

    :param soma_mesh:
        A given soma mesh.
    :param arbors_mesh:
        A given joint mesh for all the arbor to be connected to the mesh.
    :return:
        Reference to the soma after connection.
    """

    # If the soma mesh is not valid, then return
    if soma_mesh is None:
        return

        # If the arbor is not valid, then return
    if arbors_mesh is None:
        return

    # Simply apply a union operation between the soma and the arbor
    soma_mesh = nmv.mesh.union_mesh_objects(soma_mesh, arbors_mesh)

    # Remove the doubles
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')

    nmv.utilities.disable_std_output()
    bpy.ops.mesh.remove_doubles()
    nmv.utilities.enable_std_output()

    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.editmode_toggle()

    # Delete the other mesh
    nmv.scene.ops.delete_object_in_scene(arbors_mesh)

    # Return a reference to the soma mesh to be used later to do it for the rest of the arbors
    return soma_mesh

####################################################################################################
# @connect_arbor_to_soft_body_soma
####################################################################################################
def connect_arbor_to_soft_body_soma(soma_mesh,
                                    arbor):
    """Connects the root section of a given arbor to the soma at its initial segment.
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
        A reference to the soma mesh after the connection.
    """

    # If the arbor is not valid, return
    if arbor is None:
        return soma_mesh

    # Verify if the arbor is connected to the soma or not
    if not arbor.connected_to_soma:
        nmv.logger.further_detail('%s is not connected to the soma' % arbor.label)
        return soma_mesh

    # Clip the auxiliary section using a cutting plane that is normal on the branch
    # Get the intersection point between the soma and the apical dendrite
    branch_starting_point = arbor.samples[0].point
    branch_direction = arbor.samples[0].point.normalized()
    intersection_point = branch_starting_point - 0.75 * branch_direction

    # Get the nearest face on the mesh surface to the intersection point
    soma_mesh_face_index = nmv.mesh.ops.get_index_of_nearest_face_to_point(
        soma_mesh, intersection_point)

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Select the soma object
    nmv.scene.ops.select_object(soma_mesh)

    # Select the face using its obtained index
    nmv.mesh.ops.select_face_vertices(soma_mesh, soma_mesh_face_index)

    # Select the section mesh
    nmv.scene.ops.select_object(arbor.mesh)

    # Deselect all the vertices of the section mesh, for safety !
    nmv.mesh.ops.deselect_all_vertices(arbor.mesh)

    # Get the nearest face on the section mesh
    # section_face_index = nmv.mesh.ops.get_index_of_nearest_face_to_point(
    # arbor.mesh, intersection_point)

    section_face_index = nmv.mesh.ops.get_index_of_nearest_face_to_point(
        arbor.mesh, branch_starting_point)

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
    # nmv.mesh.ops.select_all_vertices(soma_mesh)

    # Deselect all the vertices of the parent mesh, for safety reasons
    # nmv.mesh.ops.deselect_all_vertices(soma_mesh)

    return soma_mesh


####################################################################################################
# @connect_arbor_to_meta_ball_soma
# TODO: Remove this function.
####################################################################################################
def connect_arbor_to_meta_ball_soma_update(soma_mesh,
                                           arbor):
    """Connects the root section of a given arbor to the soma at its initial segment.
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
        A reference to the soma mesh after the connection.
    """

    # If the arbor is not valid
    if arbor is None:
        return

    # Verify if the arbor is connected to the soma or not
    if not arbor.connected_to_soma:
        nmv.logger.detail('WARNING: The arbor [%s] is not connected to the soma' % arbor.label)
        return

    # Simply apply a union operator and remove the duplicate object

    # Union the ith mesh object
    soma_mesh = nmv.mesh.ops.union_mesh_objects(soma_mesh, arbor.mesh)

    # Switch to edit mode to REMOVE THE DOUBLES
    # TODO: Use the remove doubles function
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.editmode_toggle()

    # Delete the other mesh
    nmv.scene.ops.delete_list_objects([arbor.mesh])


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


####################################################################################################
# @get_connection_extents
####################################################################################################
def get_soma_to_root_sections_connection_extent(morphology):
    """Return the extents (or regions where the root sections are connected to the soma).

    :return:
        A list of spheres reflecting the extents of the connections between the root sections
        and the soma.
    """

    # Initialize the list
    connection_extents = list()

    # Apical dendrites
    if morphology.has_apical_dendrites():
        for arbor in morphology.apical_dendrites:
            if arbor.connected_to_soma:

                # Get the extent
                extent_center, extent_radius = get_soma_to_root_section_connection_extent(arbor)

                # Append this extent to the list
                connection_extents.append([extent_center, extent_radius])

    # Axons
    if morphology.has_axons():
        for arbor in morphology.axons:
            if arbor.connected_to_soma:

                # Get the extent
                extent_center, extent_radius = get_soma_to_root_section_connection_extent(arbor)

                # Append this extent to the list
                connection_extents.append([extent_center, extent_radius])

    # Basal dendrites
    if morphology.has_basal_dendrites():
        for arbor in morphology.basal_dendrites:
            if arbor.connected_to_soma:

                # Get the extent
                extent_center, extent_radius = get_soma_to_root_section_connection_extent(arbor)

                # Append this extent to the list
                connection_extents.append([extent_center, extent_radius])

    # Return a reference to the list
    return connection_extents


####################################################################################################
# @get_stable_soma_extent
####################################################################################################
def get_stable_soma_extent_for_morphology(morphology):
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
    largest_distance = nmv.consts.Math.MINUS_INFINITY

    # Apical dendrite
    if morphology.has_apical_dendrites():
        for arbor in morphology.apical_dendrites:

            # Compare the initial sample of the first segment of the apical dendrite
            distance = arbor.samples[0].point.length + arbor.samples[0].radius

            if distance > largest_distance:

                # Update the largest distance
                largest_distance = distance

    # Basal dendrites
    if morphology.has_basal_dendrites():
        for arbor in morphology.basal_dendrites:

            # Ensure that this basal dendrite is connected to the soma
            if arbor.connected_to_soma:

                # Compare the initial sample of the first segment of the basal dendrite
                distance = arbor.samples[0].point.length + arbor.samples[0].radius

                if distance > largest_distance:

                    # Update the largest distance
                    largest_distance = distance

    # Axons
    if morphology.has_axons():
        for arbor in morphology.axons:

            # Compare the initial sample of the first segment of the axon
            distance = arbor.samples[0].point.length + arbor.samples[0].radius

            if distance > largest_distance:

                # Ensure that this axon is connected to the soma
                if arbor.connected_to_soma:

                    # Update the largest distance
                    largest_distance = distance

    # Return the extent, and add 1 micron for safety
    return Vector((0.0, 0.0, 0.0)), largest_distance + 1.0


####################################################################################################
# @get_stable_soma_extent
####################################################################################################
def get_stable_soma_extent_for_connected_arbors(arbors):
    """
    This function will return an extent (or a sphere) that reflects the stable zone around the
    soma, where we cannot apply the same noise texture applied to the rest of the arbors.
    It checks the most far connected branch to the soma and then returns the sphere based on its
    distance.

    :param arbors:
        A given list of valid and connected arbors to the soma.
    :return:
        The center and radius of the sphere that represents the stable extent.
    """

    # The distance to the most far branch
    largest_distance = nmv.consts.Math.MINUS_INFINITY

    for arbor in arbors:

        # Compare the initial sample of the first segment of the apical dendrite
        distance = arbor.samples[0].point.length + arbor.samples[0].radius

        if distance > largest_distance:

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
    nmv.scene.set_active_object(mesh_object_1)

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
    nmv.scene.deselect_object(mesh_object_1)

    # Select mesh_object_2 and set it to be the active object
    nmv.scene.select_object(mesh_object_2)

    # Close all the open faces (including the caps) to ensure that there are no holes in the mesh
    nmv.mesh.ops.close_open_faces(mesh_object_2)

    # Get the nearest face to the bridging point
    nearest_face_index_on_mesh_2 = nmv.mesh.ops.get_index_of_nearest_face_to_point(
        mesh_object_2, connecting_point[1])

    # Select this face
    nmv.mesh.ops.select_face_vertices(mesh_object_2, nearest_face_index_on_mesh_2)

    # Select mesh_object_1 and mesh_object_2
    nmv.scene.select_object(mesh_object_1)
    nmv.scene.select_object(mesh_object_2)

    # Set the mesh_object_1 to be active
    nmv.scene.set_active_object(mesh_object_1)

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
                                 max_branching_order,
                                 section,
                                 probability=50.0,
                                 spines_list=[]):
    """Gets the data of some random spines on a given section.

    NOTE: The generated spines are totally random and does not follow any rules for growing the
    spines, they are just used for artistic purposes.

    :param current_branching_level:
        A list of ONLY one item to keep track on the current branching level recursively.
    :param max_branching_order:
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
    if current_branching_level[0] > max_branching_order:
        return

    # Increment the branching level
    current_branching_level[0] += 1

    for i, sample in enumerate(section.samples):

        # If this is the first or last sample, ignore it since they normally intersect children
        # and parent sections
        if i < 2 or i > len(section.samples) - 2:
            continue

        # Random spines
        if probability > random.uniform(0.0, 1.0) * 100.0:

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
