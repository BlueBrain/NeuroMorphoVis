####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import os

# Internal imports
import nmv.enums


####################################################################################################
# @build_tree
####################################################################################################
def build_tree(sections_list):
    """Builds the tree of the morphology by linking the parent node and the children ones.

    :param sections_list:
        A linear list of sections (NMV Sections) of a specific type to be converted to a tree.
    """

    # For each section, get the IDs of the children nodes, then find and append them to the
    # children lists.
    # Also find the ID of the parent node and update the parent accordingly.
    for i_section in sections_list:

        # First round
        for child_id in i_section.children_ids:

            # For each section
            for j_section in sections_list:

                # Is it a child
                if child_id == j_section.index:

                    # Append it to the list
                    i_section.children.append(j_section)

        # Second round
        for k_section in sections_list:

            # Is it parent
            if i_section.parent_index == k_section.index:

                # Set it to be a parent
                i_section.parent = k_section


####################################################################################################
# @get_arbors_profile_points
####################################################################################################
def get_arbors_profile_points(arbors):
    """Gets the initial segments of a list of arbors.

    The returned points will be appended to the actual two-dimensional profile given by the
    morphology to compute the initial radius of the soma that will be used for the soft body
    operations.

    :param arbors:
        A list of morphological arbors.
    :return:
        A list of points.
    """
    # A list of all the profile points extracted from the arbors
    arbor_profile_points = list()

    # For every arbor in the morphology
    for arbor in arbors:

        # Make sure that this arbor exists in the morphology
        if arbor is not None:

            # Get the first sample along the root of the tree
            arbor_profile_points.append(arbor.samples[0].point)

    # Return the list
    return arbor_profile_points


####################################################################################################
# @get_morphology_file_format
####################################################################################################
def get_morphology_file_format(morphology_file_path):
    """Returns the file format of the morphology from its absolute path.

    :param morphology_file_path:
        The absolute path of the morphology.
    :return:
        The file format enumerator of the morphology, or None.
    """
    morphology_prefix, morphology_extension = os.path.splitext(morphology_file_path)
    if 'asc' in morphology_extension.lower():
        return nmv.enums.Morphology.Format.ASCII
    elif 'swc' in morphology_extension.lower():
        return nmv.enums.Morphology.Format.SWC
    elif 'h5' in morphology_extension.lower():
        return nmv.enums.Morphology.Format.H5
    else:
        return None
