####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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
import nmv.skeleton


####################################################################################################
# @construct_swc_samples_list_from_section
####################################################################################################
def construct_swc_samples_list_from_section(section,
                                            samples_list):
    """Constructs a list of samples retrieved from the given section compliant with SWC format.

    # A list of all the samples parsed from the morphology file, to be used as a lookup table
    # to construct the morphology skeleton directly
    # http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html
    # Each sample in this list has the following structure:
    #       [0] The index of the sample or sample number
    #       [1] The type of the sample or structure identifier
    #       [2] Sample x-coordinates
    #       [3] Sample y-coordinates
    #       [4] Sample z-coordinates
    #       [5] Sample radius
    #       [6] The index of the parent sample

    :param section:
        A given morphological section.
    :param samples_list:
        The container where the samples will get appended to.
    """

    # Root sections are always connected to the soma, i.e. parent index is 1
    if section.is_root():

        # Add the first sample along the root
        sample_string = '%d %d %f %f %f %f 1' % (section.samples[0].morphology_idx,
                                                 section.samples[0].type,
                                                 section.samples[0].point[0],
                                                 section.samples[0].point[1],
                                                 section.samples[0].point[2],
                                                 section.samples[0].radius)
        samples_list.append(sample_string)

        # Update the indices of the rest of the samples along the section
        for i in range(1, len(section.samples)):
            sample_string = '%d %d %f %f %f %f %d' % (section.samples[i].morphology_idx,
                                                      section.samples[i].type,
                                                      section.samples[i].point[0],
                                                      section.samples[i].point[1],
                                                      section.samples[i].point[2],
                                                      section.samples[i].radius,
                                                      section.samples[i].morphology_idx - 1)
            samples_list.append(sample_string)

    # Non root sections start from the samples of the branching points
    else:

        # Add the first sample along the branching point
        sample_string = '%d %d %f %f %f %f %d' % (section.samples[1].morphology_idx,
                                                  section.samples[1].type,
                                                  section.samples[1].point[0],
                                                  section.samples[1].point[1],
                                                  section.samples[1].point[2],
                                                  section.samples[1].radius,
                                                  section.parent.samples[-1].morphology_idx)
        samples_list.append(sample_string)

        # Update the indices of the rest of the samples along the section
        for i in range(2, len(section.samples)):
            sample_string = '%d %d %f %f %f %f %d' % (section.samples[i].morphology_idx,
                                                      section.samples[i].type,
                                                      section.samples[i].point[0],
                                                      section.samples[i].point[1],
                                                      section.samples[i].point[2],
                                                      section.samples[i].radius,
                                                      section.samples[i].morphology_idx - 1)
            samples_list.append(sample_string)


####################################################################################################
# @construct_swc_samples_list_from_arbor
####################################################################################################
def construct_swc_samples_list_from_arbor(arbor,
                                          samples_list):
    """Constructs a list of samples retrieved from the given arbor compliant with SWC format.

    :param arbor:
        A given morphological arbor.
    :param samples_list:
        The container where the samples will get appended to.
    """

    # Construct the root section
    construct_swc_samples_list_from_section(arbor, samples_list)

    # Update the children sections recursively
    for child in arbor.children:
        construct_swc_samples_list_from_arbor(child, samples_list)


####################################################################################################
# @construct_swc_samples_list_from_soma
####################################################################################################
def construct_swc_samples_list_from_soma(soma,
                                         samples_list):
    """Constructs a list of samples retrieved from the soma, compliant with SWC format.

    :param soma:
        The soma of a given morphology.
    :param samples_list:
        The container where the samples will get appended to.
    """

    # Soma centroid and radius
    sample_string = '1 1 %f %f %f %f -1' % (soma.centroid[0],
                                            soma.centroid[1],
                                            soma.centroid[2],
                                            soma.mean_radius)
    samples_list.append(sample_string)

    # Soma profile points
    for i, profile_point in enumerate(soma.profile_points):
        sample_string = '%d 1 %f %f %f %f 1' % (i + 2,
                                                profile_point[0],
                                                profile_point[1],
                                                profile_point[2],
                                                1.0)
        samples_list.append(sample_string)


####################################################################################################
# @construct_swc_samples_list_from_morphology_tree
####################################################################################################
def construct_swc_samples_list_from_morphology_tree(morphology_object):
    """Constructs a list of samples retrieved from the given morphology skeleton compliant with
    SWC format.

    :param morphology_object:
        A given morphology object.
    :return:
        A list of samples compliant with the SWC format.
    """

    # A list that contains all the samples in the morphology file
    swc_samples_list = list()

    # Soma
    if morphology_object.soma is not None:
        construct_swc_samples_list_from_soma(morphology_object.soma, swc_samples_list)

    # Apical dendrite
    if morphology_object.apical_dendrite is not None:
        construct_swc_samples_list_from_arbor(morphology_object.apical_dendrite, swc_samples_list)

    # basal dendrites
    if morphology_object.dendrites is not None:
        # Do it dendrite by dendrite
        for basal_dendrite in morphology_object.dendrites:
            construct_swc_samples_list_from_arbor(basal_dendrite, swc_samples_list)

    # Axon
    if morphology_object.axon is not None:
        construct_swc_samples_list_from_arbor(morphology_object.axon, swc_samples_list)

    # Return the SWC-complaint  list of samples
    return swc_samples_list


####################################################################################################
# @write_morphology_to_swc_file
####################################################################################################
def write_morphology_to_swc_file(morphology_object,
                                 file_path):
    """Write the morphology skeleton to an SWC file.

    :param morphology_object:
        A given morphology object to be written to SWC file.
    :param file_path:
        The path where to write the file to.
    """

    # Before writing, we must update the indices of the samples along the entire morphology
    number_soma_samples = 0

    # The soma counts as a single sample
    if morphology_object.soma is not None:
        number_soma_samples += 1

        # The profile points along the soma count as well as samples
        number_soma_samples += len(morphology_object.soma.profile_points)

    # Update the global indices of the samples of the arbors then
    nmv.skeleton.ops.update_samples_indices_per_morphology(
        morphology_object, number_soma_samples + 1)

    # Build the samples list
    swc_samples_list = construct_swc_samples_list_from_morphology_tree(morphology_object)

    # Write the list to a file labeled with the same name of the morphology
    nmv.file.write_list_string_to_file(
        swc_samples_list, '%s/%s.swc' % (file_path, morphology_object.label))





