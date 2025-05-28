####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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
    """Builds the tree of the morphology by linking the parent and children nodes.

    :param sections_list:
        A linear list of sections (NMV Sections) of a specific type to be converted to a tree.
    """
    # Create a dictionary for O(1) lookup of sections by index
    section_map = {section.index: section for section in sections_list}

    # Single pass to set parent and children relationships
    for section in sections_list:
        # Clear existing children to avoid duplicates (in case function is called multiple times)
        section.children = []

        # Assign children
        for child_id in section.children_ids:
            child_section = section_map.get(child_id)
            if child_section:
                section.children.append(child_section)
            else:
                # Optional: Log a warning for invalid child_id
                pass  # Could add logging or error handling if needed

        # Assign parent
        if section.parent_index is not None:
            parent_section = section_map.get(section.parent_index)
            if parent_section:
                section.parent = parent_section
            else:
                # Optional: Log a warning for invalid parent_index
                section.parent = None  # Ensure parent is None if not found
        else:
            section.parent = None


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
