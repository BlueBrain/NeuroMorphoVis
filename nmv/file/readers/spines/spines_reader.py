####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.file
import nmv.skeleton


####################################################################################################
# @load_spine_morphology_from_data_file
####################################################################################################
def load_spine_morphology_from_data_file(spines_directory,
                                         spine_file):
    """Loads a spine morphology to the scene from a given directory and return a reference to it.

    NOTE: These spines do not have branched. They are just samples that construct a single section.

    :param spines_directory:
        A given directory of spines.
    :param spine_file:
        A given spine morphology file.
    :return:
        Returns a spine morphology.
    """

    # Spine section samples, as a list of samples
    all_spine_samples = list()

    # Number of sections in the morphology
    number_sections = 0

    # read spine
    file_handle = open('%s/%s' % (spines_directory, spine_file), 'r')
    for i, line in enumerate(file_handle):

        # Ignore lines with comments that have '#'
        # TODO: Possibly a bug
        if '#' in line:
            continue

        # Ignore empty lines
        if not line.strip():
            continue

        # Extract the position and radius data
        data = line.split(' ')
        section_index = int(data[0])
        x = float(data[1])
        y = float(data[2])
        z = float(data[3])
        r = float(data[4]) * 0.5

        # Construct the spine sample from the extracted data
        spine_sample = [section_index, x, y, z, r, i]

        # Append the sample to the samples
        all_spine_samples.append(spine_sample)

        # Update the number of sections in the morphology
        number_sections = section_index + 1

    # Close the file
    file_handle.close()

    # Construct the sections list to build the morphology skeleton
    sections_list = list()
    for i in range(number_sections):
        sections_list.append(nmv.skeleton.SpineSection(samples=list()))

    # Process each sample in the list
    for sample in all_spine_samples:

        # Make it clear
        section_index = sample[0]
        x = sample[1]
        y = sample[2]
        z = sample[3]
        r = sample[4]
        sample_index = sample[5]

        # Update the sections with the corresponding samples
        sections_list[section_index].samples.append(
            nmv.skeleton.Sample(point=Vector((x, y, z)), radius=r, index=sample_index))

    # Construct spine morphology
    spine_morphology = nmv.skeleton.SpineMorphology(sections=sections_list)

    # Return a reference to the spine morphology
    return spine_morphology


####################################################################################################
# @load_spine_morphologies_from_data_files
####################################################################################################
def load_spine_morphologies_from_data_files(spines_directory):
    """Loads a list of non-branched spine morphologies.

    :param spines_directory:
        The directory that contains all the spine morphology files.
    :return:
        A list of spine morphologies.
    """

    # List all the data files in the directory
    spines_files = nmv.file.ops.get_files_in_directory(spines_directory, file_extension='.spine')

    # Load the spines, one by one into a list
    spines_morphologies = list()

    # Load spine by spine
    for spine_file in spines_files:

        # Load the spine morphology
        spine_morphology = load_spine_morphology_from_data_file(spines_directory, spine_file)

        # Append the spine to the list
        spines_morphologies.append(spine_morphology)

    # Return the spines list
    return spines_morphologies


####################################################################################################
# @load_spine
####################################################################################################
def load_spine_obj_mesh(spines_directory,
                        spine_file):
    """Load an OBJ spine mesh to the scene from a given directory and returns a reference to it.

    :param spines_directory:
        A given directory of spines.
    :param spine_file:
        A given spine OBJ mesh file.
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
        spine_object = load_spine_obj_mesh(spines_directory, spine_file)

        # Append the spine to the list
        spines_objects_list.append(spine_object)

    # Return the spines list
    return spines_objects_list


