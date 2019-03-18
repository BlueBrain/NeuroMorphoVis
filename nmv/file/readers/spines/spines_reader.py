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

# System imports
import sys, os

import nmv
import nmv.file


####################################################################################################
# @load_spine
####################################################################################################
def load_spine(spines_directory,
               spine_file):
    """Load a spine mesh to the scene from a given directory and returns a reference to it.

    :param spines_directory:
        A given directory of spines.
    :param spine_file:
        A given spine file.
    :return:
        A reference to the loaded spine into the scene.
    """

    # Load the spine into a blender object
    spine_object = nmv.file.import_obj_file(spines_directory, spine_file)

    # Return a reference to it
    return spine_object


####################################################################################################
# @load_spines
####################################################################################################
def load_spines(spines_directory):
    """Load all the spines in a certain directory and return a list of all of them.

    :param spines_directory:
        A given directory where the spines are located.
    :return:
        A list of all the loaded spines.
    """

    # List all the obj files in the directory
    spines_files = nmv.file.ops.get_files_in_directory(spines_directory, file_extension='.obj')

    # Load the spines, one by one into a list
    spines_objects_list = list()

    # Load spine by spine
    for spine_file in spines_files:

        # Load the spine
        spine_object = load_spine(spines_directory, spine_file)

        # Append the spine to the list
        spines_objects_list.append(spine_object)

    # Return the spines list
    return spines_objects_list
