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


# Internal imports
import neuromorphovis as nmv


####################################################################################################
# @build_arbors_from_sections
####################################################################################################
def build_arbors_from_sections(sections_list):
    """Returns a list of nodes where we can access the different sections of a single arbor as a
    tree.

    :param sections_list:
        A linear list of sections.
    :return:
        A list containing references to the root nodes of the different arbors in the sections list.
    """

    # If the sections list is None
    if sections_list is None:

        # This is an issue
        nmv.logger.log('ERROR: Invalid sections list')

        # Return None
        return None

    # If the sections list is empty
    if len(sections_list) == 0:

        # This might be an issue
        nmv.logger.log('WARNING: Empty sections list!')

        # Then return None
        return None

    # A list of roots
    roots = list()

    # Iterate over the sections and get the root ones
    for section in sections_list:

        # If the section has no parent, it is a root then
        if section.parent is None:

            # Append this root to the list
            roots.append(section)

    # If the list does not contain any roots, then return None, otherwise return the entire list
    if len(roots) == 0:

        # This might be an issue
        nmv.logger.log('WARNING: No roots found in the sections list')

        # Return None
        return None

    else:

        # Return the root list
        return roots
