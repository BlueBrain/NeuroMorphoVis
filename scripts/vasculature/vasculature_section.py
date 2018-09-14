####################################################################################################
# Copyright (c) 2018, EPFL / Blue Brain Project
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


####################################################################################################
# VasculatureSection
####################################################################################################
class VasculatureSection:
    """ A morphological section represents a series of morphological samples of vasculature. """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 index,
                 samples_list):
        """Constructor

        :param index:
            Section index.
        :param samples_list:
            A list of samples that compose this section.
        """

        # Section index
        self.index = index

        # Segments samples (points along the section)
        self.samples_list = samples_list

        # A reference to the section parents, if exist
        self.parents = list()

        # A list of the children, if exist
        self.children = list()

        # Section name
        self.name = 'section_' + str(index)

    ################################################################################################
    # @update_children
    ################################################################################################
    def update_children(self, child_section):
        """Updates the children sections list.

        :param child_section:
            The child section that is supposed to be emanating from this section.
        """

        # Append the child to the list
        # TODO: Verify if a child already exists with the same index or not!
        self.children.append(child_section)

    ################################################################################################
    # @update_parents
    ################################################################################################
    def update_parents(self, parent_section):
        """Updates the parents section list.

        :param parent_section:
            The parent section with which this section is emanating from.
        """

        # Append the section to the list
        self.parents.append(parent_section)

    ################################################################################################
    # @is_root
    ################################################################################################
    def is_root(self):
        """Check if the section is root or not.

        :return:
            True if the section is root, and False otherwise.
        """

        if len(self.parents) == 0:
            return True

        return False

    ################################################################################################
    # @has_children
    ################################################################################################
    def has_children(self):
        """Check if the section has children sections or not.

        :return:
            True or False.
        """

        if len(self.children) > 0:
            return True

        return False

    ################################################################################################
    # @has_parents
    ################################################################################################
    def has_parents(self):
        """Check if the section has a parent sections or not.

        :return:
            True of False.
        """

        if len(self.parents) > 0:
            return True

        return False
