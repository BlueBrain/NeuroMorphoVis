####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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

# Internal imports
import nmv


####################################################################################################
# @construct_samples_list_from_section
####################################################################################################
def construct_samples_list_from_section(section,
                                        samples_list):
    """Constructs a list of samples retrieved from the given section.

    :param section:
        A given morphological section.
    :param samples_list:
        The container where the samples will get appended to.
    """

    for i in range(0, len(section.samples) - 1):
        sample_string = '[%f %f %f %f][%f %f %f %f]' % (section.samples[i].point[0],
                                                        section.samples[i].point[1],
                                                        section.samples[i].point[2],
                                                        section.samples[i].radius,
                                                        section.samples[i + 1].point[0],
                                                        section.samples[i + 1].point[1],
                                                        section.samples[i + 1].point[2],
                                                        section.samples[i + 1].radius)
        samples_list.append(sample_string)


####################################################################################################
# @construct_samples_list_from_arbor
####################################################################################################
def construct_samples_list_from_arbor(arbor,
                                      samples_list):
    """Constructs a list of samples retrieved from the given arbor.

    :param arbor:
        A given morphological arbor.
    :param samples_list:
        The container where the samples will get appended to.
    """

    # Construct the root section
    construct_samples_list_from_section(arbor, samples_list)

    # Update the children sections recursively
    for child in arbor.children:
        construct_samples_list_from_arbor(child, samples_list)


####################################################################################################
# @construct_samples_list_from_morphology_tree
####################################################################################################
def construct_samples_list_from_morphology_tree(morphology_object):
    """Constructs a list of samples retrieved from the given morphology skeleton compliant with
    SWC format.

    :param morphology_object:
        A given morphology object.
    :return:
        A list of samples compliant with the SWC format.
    """

    # A list that contains all the samples in the morphology file
    swc_samples_list = list()

    # Apical dendrite
    if morphology_object.apical_dendrite is not None:
        construct_samples_list_from_arbor(morphology_object.apical_dendrite, swc_samples_list)

    # Basal dendrites
    if morphology_object.dendrites is not None:
        # Do it dendrite by dendrite
        for basal_dendrite in morphology_object.dendrites:
            construct_samples_list_from_arbor(basal_dendrite, swc_samples_list)

    # Axon
    if morphology_object.axon is not None:
        construct_samples_list_from_arbor(morphology_object.axon, swc_samples_list)

    # Return the SWC-complaint  list of samples
    return swc_samples_list


####################################################################################################
# @write_morphology_to_segments_file
####################################################################################################
def write_morphology_to_segments_file(morphology_object,
                                      file_path):
    """Write the morphology skeleton to a file (.segments) that is composed of segments only.

    :param morphology_object:
        A given morphology object to be written to SWC file.
    :param file_path:
        The path where to write the file to.
    """

    # Build the samples list
    samples_list = construct_samples_list_from_morphology_tree(morphology_object)

    # Write the list to a file labeled with the same name of the morphology
    nmv.file.write_list_string_to_file(
        samples_list, '%s/%s.segments' % (file_path, morphology_object.label))

