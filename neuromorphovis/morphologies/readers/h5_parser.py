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
import os, sys

# Blender imports
import bpy
from mathutils import Vector

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append('%s/' % path)

# Internal imports
import file_ops

import neuromorphovis.skeleton

import neuromorphovis.file

####################################################################################################
# @get_arbors_profile_points
####################################################################################################
def get_arbors_profile_points(arbors):
    """
    Gets the initial segments of a list of arbors.
    The returned points will be appended to the actual two-dimensional profile given by the
    morphology to compute the initial radius of the soma that will be used for the soft body
    operations.

    :param arbors: A list of morphological arbors.
    :return: A list of points.
    """
    # A list of all the profile points extracted from the arbors
    arbor_profile_points = []

    for arbor in arbors:

        # Make sure that this arbor exists in the morphology
        if arbor is not None:

            # Get the first sample along the root of the tree
            arbor_profile_points.append(arbor.samples[0].point)

    # Return the list
    return arbor_profile_points


####################################################################################################
# @build_soma
####################################################################################################
def build_soma(points_list,
               structure_list,
               axon_tree=None,
               basal_dendrites_trees=None,
               apical_dendrite_tree=None):
    """
    This function builds the soma and returns a reference to it.

    :param points_list: Morphology point list.
    :param structure_list: Morphology section list.
    :param axon_tree: The reconstructed tree of the axon.
    :param basal_dendrites_trees: The reconstructed trees of the basal dendrites.
    :param apical_dendrite_tree: The reconstructed tree of the apical dendrite.
    :return: A reference to the soma.
    """

    # Get the index of the starting point of the soma section
    soma_section_first_point_index = structure_list[0][0]

    # Get the index of the last point of the soma section
    soma_section_last_point_index = structure_list[1][0]

    # Get the positions of each sample along the soma section
    soma_profile_points = []

    # Update the soma profile point list
    for i_sample in range(soma_section_first_point_index, soma_section_last_point_index):

        # Profile point
        x = points_list[i_sample][0]
        y = points_list[i_sample][1]
        z = points_list[i_sample][2]
        profile_point = Vector((x, y, z))

        # Add the profile point to the list
        soma_profile_points.append(profile_point)

    # Compute soma centroid
    soma_centroid = Vector((0.0, 0.0, 0.0))
    for i_point in soma_profile_points:
        soma_centroid += i_point
    soma_centroid /= len(soma_profile_points)

    # Compute the soma mean radius
    mean_soma_radius = 0.0
    for i_point in soma_profile_points:
        distance = i_point - soma_centroid
        mean_soma_radius += distance.length
    mean_soma_radius /= len(soma_profile_points)

    # Compute the profile points from the arbors
    arbors_profile_points = []

    # Axon profile point
    if axon_tree is not None:
        arbors_profile_points.extend(get_arbors_profile_points([axon_tree]))

    # Basal dendrites points
    if basal_dendrites_trees is not None:
        arbors_profile_points.extend(get_arbors_profile_points(basal_dendrites_trees))

    # Apical dendrite profile point
    if apical_dendrite_tree is not None:
        arbors_profile_points.extend(get_arbors_profile_points([apical_dendrite_tree]))

    # Construct the soma object
    soma_object = skeleton.Soma(centroid=soma_centroid, mean_radius=mean_soma_radius,
        profile_points=soma_profile_points, arbors_profile_points=arbors_profile_points)

    # Return a reference to the soma object
    return soma_object


####################################################################################################
# @build_tree
####################################################################################################
def build_tree(sections):
    """
    This function builds the tree skeleton of the morphology by linking the parent node and also
    the children nodes.

    :param sections: A linear list of sections of a specific type.
    """

    # For each section, get the IDs of the children nodes, then find them and append them to the
    # children lists. Also find the ID of the parent node and update the parent accordingly.
    for i_section in sections:
        for child_id in i_section.children_ids:
            for j_section in sections:
                if child_id == j_section.id:
                    i_section.children.append(j_section)
        for k_section in sections:
            if i_section.parent_id == k_section.id:
                i_section.parent = k_section


####################################################################################################
# @build_single_arbor
####################################################################################################
def build_single_arbor(sections):
    """
    This function builds a single arbor, mainly axons and apical dendrites to be able to access
    them as a tree.

    :param sections: A linear list of sections.
    :return: The root node of the tree.
    """

    roots = []
    for i_section in sections:
        if i_section.parent_id == 0:
            roots.append(i_section)

    # If the list does not contain any roots, then return None, if only one root, return it as a
    # single object, otherwise return the entire list.
    if len(roots) == 0:
        return None
    elif len(roots) == 1:
        return roots[0]


####################################################################################################
# @build_multiple_arbors
####################################################################################################
def build_multiple_arbors(sections):
    """
    This function returns a node, or a list of nodes where we can access the different sections of
    a single arbor as a tree.
    For the axon and apical dendrites, the function returns the root of a single branch. However,
    for the basal dendrites, the function returns a list of roots, where each root reflects a single
    independent branch emanating from the soma.

    :param sections: A linear list of axons sections.
    :return: The root node of the axon.
    """

    roots = []
    for i_section in sections:
        if i_section.parent_id == 0:
            roots.append(i_section)

    # If the list does not contain any roots, then return None, if only one root, return it as a
    # single object, otherwise return the entire list
    if len(roots) == 0:
        return None
    else:
        return roots


####################################################################################################
# @parse_h5_morphology
####################################################################################################
def parse_h5_morphology(h5_file):
    """
    This function parses the h5 file into a linear list of sections and returns a morphology
    skeleton.

    :param h5_file: Input h5 morphology.
    :return: Morphology skeleton ready for consumption by Meshy.
    """

    import sys
    sys.path.append(
        '/opt/local/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages')

    # Import the h5py module
    import h5py

    # Read the h5 file using the python module
    data = h5py.File(h5_file, 'r')

    # The h5 file contains, normally, three directories: 'points, structure and perimeters'.
    points_directory = '/points'
    structure_directory = '/structure'
    perimeters_directory = '/perimeters'

    # The data will be stored in three lists: points, structure and perimeters
    points_list = None
    structure_list = None
    perimeters_list = None

    # Get the points list
    try:
        points_list = data[points_directory].value
    except ImportError:
        nmv.logger.log('ERROR: Cannot load the data points from [%s]' % h5_file)

    # Get the structure list
    try:
        structure_list = data[structure_directory].value
    except ImportError:
        nmv.logger.log('ERROR: Cannot load the data structure from [%s]' % h5_file)

    # For the moment, we ignore the perimeters_list until further moment.
    # TODO: Update parsing the perimeters_directory.

    number_points = len(points_list)
    number_sections = len(structure_list)

    # Parse the sections and add them to a linear list [index, parent, type, samples]
    parsed_sections = []
    for i_section in range(1, number_sections - 1):

        # Get the index of the starting point of the section
        section_first_point_index = structure_list[i_section][0]

        # Get the index of the last point of the section
        section_last_point_index = structure_list[i_section + 1][0]

        # Section index
        section_index = i_section

        # Get section type
        section_type = structure_list[i_section][1]

        # Get the section parent index
        section_parent_index = int(structure_list[i_section][2])

        # Get the positions and radii of each sample along the section
        section_samples = []
        i = 0
        for i_sample in range(section_first_point_index, section_last_point_index):

            # Position
            x = points_list[i_sample][0]
            y = points_list[i_sample][1]
            z = points_list[i_sample][2]
            point = Vector((x, y, z))

            # Radius
            # NOTE: What is reported in our .h5 files is the diameter not the radius
            radius = points_list[i_sample][3] / 2.0

            # Build section sample
            section_sample = skeleton.Sample(point=point, radius=radius, id=i)

            # Add the sample to the list
            section_samples.append(section_sample)
            i += 1

        # Build a temporary section list until all the sections are parsed
        parsed_section = [section_index, section_parent_index, section_type, section_samples]

        # Add this section to the parsed sections list
        parsed_sections.append(parsed_section)

    # After parsing the data of all the sections, we can build the morphology skeleton, by finding
    # the parents and children sections.
    axon_sections = []
    basal_dendrites_sections = []
    apical_dendrite_sections = []
    for i_parsed_section in parsed_sections:

        # Section ID
        section_id = i_parsed_section[0]

        # Section parent ID
        section_parent_id = i_parsed_section[1]

        # Section children IDs, if exist
        section_children_ids = []
        for j_parsed_section in parsed_sections:

            # If the parent ID of another section is equivalent to the ID of this section, then
            # it is a child.
            if section_id == j_parsed_section[1]:
                section_children_ids.append(j_parsed_section[0])

        # Section type
        section_type = i_parsed_section[2]

        # Section samples
        section_samples = i_parsed_section[3]

        # Construct a skeleton section
        skeleton_section = skeleton.Section(id=section_id, parent_id=section_parent_id,
            children_ids=section_children_ids, samples=section_samples, type=section_type)

        # Add the skeleton section to the corresponding list, whether axon, apical or basal dendrite
        # For neurons the values are: 1: soma, 2: axon, 3: basal dendrite, 4: apical dendrite.
        # For glia cells the values are: 1: soma, 2: glia process, 3 glia end-foot.
        if section_type == 2:
            axon_sections.append(skeleton_section)
        elif section_type == 3:
            basal_dendrites_sections.append(skeleton_section)
        elif section_type == 4:
            apical_dendrite_sections.append(skeleton_section)
        else:
            nmv.logger.log('ERROR: Unknown section type!')

    # Build the axon, basal and apical dendrites trees
    build_tree(axon_sections)
    build_tree(basal_dendrites_sections)
    build_tree(apical_dendrite_sections)

    # Build the axon, basal and apical dendrites trees
    axon = build_single_arbor(axon_sections)
    basal_dendrites = build_multiple_arbors(basal_dendrites_sections)
    apical_dendrite = build_single_arbor(apical_dendrite_sections)

    # Build the soma
    soma_object = build_soma(points_list, structure_list)

    # Update the morphology label
    label = file_ops.get_file_name_from_path(h5_file)

    # Construct the morphology skeleton
    reconstructed_morphology = skeleton.Morphology(soma=soma_object, axon=axon,
        dendrites=basal_dendrites, apical_dendrite=apical_dendrite, label=label)

    # Return a reference to the reconstructed morphology object that is compatible with Meshy.
    return reconstructed_morphology
