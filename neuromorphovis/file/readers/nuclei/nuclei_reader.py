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

import neuromorphovis as nmv
import neuromorphovis.file


####################################################################################################
# @load_nucleus
####################################################################################################
def load_nucleus(nuclei_directory,
                 nucleus_file):
    """Load a nucleus mesh to the scene from a given directory and returns a reference to it.

    :param nuclei_directory:
        A given directory of nuclei.
    :param nucleus_file:
        A given nucleus file.
    :return:
        A reference to the loaded spine into the scene.
    """

    # Load the nucleus into a blender object
    nucleus_object = nmv.file.import_obj_file(nuclei_directory, nucleus_file)

    # Return a reference to it
    return nucleus_object


####################################################################################################
# @load_spines
####################################################################################################
def load_nuclei(nuclei_directory):
    """Load all the nuclei in a certain directory and return a list of all of them.

    :param nuclei_directory:
        A given directory where the nuclei are located.
    :return:
        A list of all the loaded nuclei.
    """

    # List all the .OBJ files in the directory
    nuclei_files = nmv.file.ops.get_files_in_directory(nuclei_directory, file_extension='.obj')

    # Load the nuclei, one by one into a list
    nuclei_objects_list = []

    # Load nucleus by nucleus
    for nucleus_file in nuclei_files:

        # Load the nucleus
        nucleus_object = load_nucleus(nuclei_directory, nucleus_file)

        # Append the nucleus to the list
        nuclei_objects_list.append(nucleus_object)

    # Return the nuclei list
    return nuclei_objects_list
