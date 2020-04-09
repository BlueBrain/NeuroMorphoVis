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

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.geometry
import nmv.consts


####################################################################################################
# get_subtree_leaves
####################################################################################################
def get_subtree_leaves(section,
                       leaves):
    """Returns a list with all the leaves of a subtree where the given section is considered
    the root.

    :param section:
        The root section of the subtree.
    :param leaves:
        The list that will be used to collect the subtree.
    :return:
    """

    # If the section is leaf, then append it to the leaves list
    if section.is_leaf():
        leaves.append(section)

    # Otherwise, go recursively
    for child in section.children:
        get_subtree_leaves(section=child, leaves=leaves)


####################################################################################################
# get_arbor_leaves
####################################################################################################
def get_arbor_leaves(arbor):
    """Returns a list with all the leaves of the given arbor.

    :param arbor:
        A given arbor to get its leaf nodes.
    :return:
        A list of nodes (or sections) that represent the leaves of the arbor tree.
    """

    # Leaves list
    leaves = list()

    # Arbor must not be None, otherwise return an empty list
    if arbor is None:
        return leaves

    # Start from the arbor root and go recursively
    get_subtree_leaves(section=arbor, leaves=leaves)

    # Return the list
    return leaves


####################################################################################################
# compute_dendrogram_x_coordinates_for_parents
####################################################################################################
def compute_dendrogram_x_coordinates_for_parents(section):
    """This function computes the X-coordinates of the dendrogram points starting from a given
    section and goes recursively up to the maximum possible parent in the arbor tree.
    If the @dendrogram_x parameter of any of the sections along the path is None, the function
    returns immediately.

    The first call of this function should be used for a leaf section, and then propagates up to
    the maximum possible parent.

    :param section:
        An entry section to start computing the X-axis values of the dendrograms.
    """

    # If the section is None, return please
    if section is None:
        return

    # The parent section must not be None
    if section.parent is not None:

        # Compute X-coordinates for all the children
        x = 0
        for child in section.parent.children:

            # If the X-coordinate of any of the children section is not computed, return
            if child.dendrogram_x is None:
                return

            # Otherwise add the value
            x += child.dendrogram_x

        # Normalize to get the center point
        x /= len(section.parent.children)

        # Do it
        section.parent.dendrogram_x = x

    # Go recursively
    compute_dendrogram_x_coordinates_for_parents(section=section.parent)


####################################################################################################
# compute_dendrogram_y_coordinates_for_children
####################################################################################################
def compute_dendrogram_y_coordinates_for_children(section):
    """This function computes the Y-coordinates of the dendrogram points starting from a given
    root section and goes recursively down to the leaves.

    :param section:
        The root section of the subtree where we are computing the Y-coordinates of the dendrogram.
    """

    # The actual Y-coordinate is equivalent to the path length of the section
    section.dendrogram_y = section.compute_path_length()

    # Go recursively
    for child in section.children:
        compute_dendrogram_y_coordinates_for_children(section=child)


####################################################################################################
# compute_arbor_dendrogram_individually
####################################################################################################
def compute_arbor_dendrogram_individually(arbor,
                                          delta=10,
                                          continuing_index=0):
    """Computes the dendrogram of a given arbor individually and not as a part of the entire
    morphology.

    :param arbor:
        A given arbor to compute its dendrogram.
    :param delta:
        The distance between the leaves.
    :param continuing_index:
        An index that reflects the continuation from one arbor to another.
    """
    # Get a list of all the leaf nodes in the arbor
    leaves = get_arbor_leaves(arbor=arbor)

    # Assuming that the leaves will start at 0.0 on the x-axis
    for i, leaf in enumerate(leaves):

        # Compute the X-coordinates of the leaves
        leaf.dendrogram_x = (i + continuing_index) * delta

    # Compute the X-coordinates of the rest of the arbor tree
    for leaf in leaves:
        compute_dendrogram_x_coordinates_for_parents(leaf)

    # Compute the Y-coordinates starting from the parent node
    compute_dendrogram_y_coordinates_for_children(section=arbor)


####################################################################################################
# compute_morphology_dendrogram_per_arbor_individually
####################################################################################################
def compute_morphology_dendrogram_per_arbor_individually(morphology,
                                                         delta):
    """Computes the dendrogram of the entire morphology taking into consideration that each arbor is
    treated as an individual item.

    :param morphology:
        A morphology to compute its dendrogram.
    :param delta:
        The distance between the leaves.
    """

    # Apical dendrite
    if morphology.apical_dendrite is not None:
        compute_arbor_dendrogram_individually(arbor=morphology.apical_dendrite, delta=delta)

    # Basal dendrites
    if morphology.dendrites is not None:
        for basal_dendrite in morphology.dendrites:
            compute_arbor_dendrogram_individually(arbor=basal_dendrite, delta=delta)

    # Axon
    if morphology.axon is not None:
        compute_arbor_dendrogram_individually(arbor=morphology.axon, delta=delta)


####################################################################################################
# compute_morphology_dendrogram
####################################################################################################
def compute_morphology_dendrogram(morphology,
                                  delta):
    """Computes the dendrogram of the entire morphology as a single object considering the shifts
    required between the different arbors.

    :param morphology:
        A morphology to compute its dendrogram.
    :param delta:
        The distance between the leaves.
    """

    # This index is used to keep track on the distance between different leaves on different arbors
    continuing_index = 0

    # Apical dendrite
    if morphology.apical_dendrite is not None:
        compute_arbor_dendrogram_individually(arbor=morphology.apical_dendrite,
                                              delta=delta)

        # Add the leaves count 
        continuing_index = len(get_arbor_leaves(arbor=morphology.apical_dendrite))

    # Basal dendrites
    if morphology.dendrites is not None:
        for basal_dendrite in morphology.dendrites:
            compute_arbor_dendrogram_individually(
                arbor=basal_dendrite, delta=delta, continuing_index=continuing_index)

            # Add the leaves count 
            continuing_index += len(get_arbor_leaves(arbor=basal_dendrite))

    # Axon
    if morphology.axon is not None:
        compute_arbor_dendrogram_individually(arbor=morphology.axon, delta=delta,
                                              continuing_index=continuing_index)


####################################################################################################
# create_dendrogram_poly_lines_list_of_arbor
####################################################################################################
def create_dendrogram_poly_lines_list_of_arbor(section,
                                               poly_lines_data=[],
                                               max_branching_order=nmv.consts.Math.INFINITY,
                                               mode='FLAT',
                                               stretch_legs=True):

    # Stop if the maximum branching order has been reached
    if section.branching_order > max_branching_order:
        return

    # If the given section is a root, set the start along the Y-axis to zero, otherwise to the path
    # length of the parent
    if section.is_root():
        start_y = 0
    else:
        start_y = section.parent.path_length
    end_y = start_y + section.length

    # The two points that represent the section
    point_1 = Vector((section.dendrogram_x, start_y, 0))
    point_2 = Vector((section.dendrogram_x, end_y, 0))

    # Construct a simple poly-line with two points at the start and end of the poly-line
    samples = list()

    if mode == 'FLAT':
        samples.append([(point_1[0], point_1[1], point_1[2], 1), 2.0])
        samples.append([(point_2[0], point_2[1], point_2[2], 1), 2.0])
    else:

        # Add the first sample
        samples.append([(point_1[0], point_1[1], point_1[2], 1), section.samples[0].radius])

        delta = 0
        for i in range(len(section.samples) - 1):
            delta += (section.samples[i + 1].point - section.samples[i].point).length
            radius = section.samples[i].radius
            samples.append([(section.dendrogram_x, start_y + delta, 0.0, 1), radius])

    # Construct the poly-line
    poly_line = nmv.geometry.PolyLine(
        name='section_%s' % str(section.id),
        samples=samples,
        material_index=section.get_material_index() + (section.branching_order % 2))

    # Append the polyline to the list
    poly_lines_data.append(poly_line)

    # Stop if the maximum branching order has been reached
    if section.branching_order > max_branching_order - 1:
        return

    # Draw the horizontal line
    if section.has_children():

        number_children = len(section.children)

        for i in range(number_children - 1):
            child_1 = section.children[i]
            child_2 = section.children[i + 1]

            samples = list()
            radius_1 = 0.5 # child_1.samples[0].radius
            radius_2 = 0.5 # child_2.samples[0].radius
            if stretch_legs:
                x_1 = child_1.dendrogram_x - radius_1
                x_2 = child_2.dendrogram_x + radius_2
            else:
                x_1 = child_1.dendrogram_x
                x_2 = child_2.dendrogram_x
            samples.append([(x_1, end_y, 0, 1), radius_1])
            samples.append([(x_2, end_y, 0, 1), radius_2])
            poly_line = nmv.geometry.PolyLine(
                name='section_%s' % str(section.id),
                samples=samples,
                material_index=section.get_material_index() + (section.branching_order % 2))

            # Append the polyline to the list
            poly_lines_data.append(poly_line)

    # Go recursively
    for child in section.children:
        create_dendrogram_poly_lines_list_of_arbor(
            section=child, poly_lines_data=poly_lines_data, max_branching_order=max_branching_order,
            mode=mode)


####################################################################################################
# add_soma_to_stems_line
####################################################################################################
def add_soma_to_stems_line(morphology,
                           poly_lines_data=[],
                           ignore_apical_dendrite=True,
                           ignore_basal_dendrites=True,
                           ignore_axon=True):

    x_values = list()
    radii = list()

    if not ignore_apical_dendrite:
        if morphology.apical_dendrite is not None:
            x_values.append(morphology.apical_dendrite.dendrogram_x)
            radii.append(morphology.apical_dendrite.samples[0].radius)

    if not ignore_basal_dendrites:
        if morphology.dendrites is not None:
            for basal_dendrite in morphology.dendrites:
                x_values.append(basal_dendrite.dendrogram_x)
                radii.append(basal_dendrite.samples[0].radius)

    if not ignore_axon:
        if morphology.axon is not None:
            x_values.append(morphology.axon.dendrogram_x)
            radii.append(morphology.axon.samples[0].radius)

    # Average radius
    avg_radius = sum(radii) / len(radii)

    # Final value
    center = (min(x_values) + max(x_values)) * 0.5
    center = Vector((-center, -avg_radius * 2.0, 0))

    # Compute the line points
    point_1 = Vector((min(x_values), -avg_radius, 0))
    point_2 = Vector((max(x_values), -avg_radius, 0))

    # Construct a simple poly-line with two points at the start and end of the poly-line
    samples = list()

    samples.append([(point_1[0], point_1[1], point_1[2], 1), avg_radius])
    samples.append([(point_2[0], point_2[1], point_2[2], 1), avg_radius])

    # Construct the poly-line
    poly_line = nmv.geometry.PolyLine(name='root', samples=samples, material_index=0)

    # Append the polyline to the list
    poly_lines_data.append(poly_line)

    return center




