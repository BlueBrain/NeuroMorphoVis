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
import copy

# Blender imports
from mathutils import Vector

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.file
import neuromorphovis.skeleton


####################################################################################################
# @SWCReader
####################################################################################################
class SWCReader:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 swc_file):
        """Constructor

        :param swc_file:
            A given .SWC morphology file.
        """

        # Set the path to the given h5 file
        self.morphology_file = swc_file

        # A list of all the samples parsed from the morphology file, to be used as a lookup table
        #  to construct the morphology skeleton directly
        # Each sample in this list has the following structure:
        # [0] The index of the sample
        # [1] The type of the sample
        # [2] Sample x-coordinates
        # [3] Sample y-coordinates
        # [4] Sample z-coordinates
        # [5] Sample radius
        # [6] The index of the parent sample
        self.samples_list = list()

    ################################################################################################
    # @read_samples
    ################################################################################################
    def read_samples(self):
        """Reads an SWC files and returns a list of all the samples in the file"""

        # Open the file, read it line by line and store the result in list.
        morphology_file = open(self.morphology_file, 'r')

        # Add a dummy sample to the list at index 0 to match the indices
        # The zeroth sample always defines the soma parameters, and it is parsed independently
        self.samples_list.append([0, 0, 0.0, 0.0, 0.0, 0.0, 0])

        # For each line in the morphology file
        for line in morphology_file:

            # Ignore lines with comments that have '#'
            if '#' in line:
                continue

            # Extract the data from the line
            data = line.strip('\n').split(' ')

            # If unwanted spaces exit, remove them
            for i in data:
                if i == '':
                    data.remove(i)

            # Get the index
            index = int(data[nmv.consts.Arbors.SWC_SAMPLE_INDEX_IDX])

            # Get the branch type
            sample_type = int(data[nmv.consts.Arbors.SWC_SAMPLE_TYPE_IDX])

            # Get the X-coordinate
            x = float(data[nmv.consts.Arbors.SWC_SAMPLE_X_COORDINATES_IDX])

            # Get the Y-coordinate
            y = float(data[nmv.consts.Arbors.SWC_SAMPLE_Y_COORDINATES_IDX])

            # Get the Z-coordinate
            z = float(data[nmv.consts.Arbors.SWC_SAMPLE_Z_COORDINATES_IDX])

            # Get the sample radius
            radius = float(data[nmv.consts.Arbors.SWC_SAMPLE_RADIUS_IDX])

            # Get the sample parent index
            parent_index = int(data[nmv.consts.Arbors.SWC_SAMPLE_PARENT_INDEX_IDX])

            # Add the sample to the list
            self.samples_list.append([index, sample_type, x, y, z, radius, parent_index])

    ################################################################################################
    # @get_nmv_sample_from_samples_list
    ################################################################################################
    def get_nmv_sample_from_samples_list(self,
                                         sample_index):
        """Gets a NeuroMorphoVis sample from the original list of samples that was parsed from
        the SWC morphology file.

        :param sample_index:
            The index of the sample.
        :return:
            A NeuroMorphoVis sample object.
        """

        # Get the sample and its data
        sample_data = self.samples_list[sample_index]

        # Index of the sample
        sample_id = sample_data[0]

        # The type of the sample
        sample_type = sample_data[1]

        # The cartesian coordinates of the sample
        sample_point = Vector((sample_data[2], sample_data[3], sample_data[4]))

        # Sample radius
        sample_radius = sample_data[5]

        # The index of the parent sample
        parent_sample_id = sample_data[6]

        # Construct a nmv sample object
        nmv_sample = neuromorphovis.skeleton.Sample(
            point=sample_point, radius=sample_radius, id=sample_id, morphology_id=0,
            type=sample_type, parent_id=parent_sample_id)

        # Return a reference to the reconstructed object
        return nmv_sample

    ################################################################################################
    # @get_samples_list_by_type
    ################################################################################################
    def get_samples_list_by_type(self,
                                 sample_type):
        """Gets a list of samples of a specific type from the list of morphological samples that
        was constructed after reading the SWC file.

        :param sample_type:
            The type of samples, belonging to which branch.
        :return:
            A list of samples that are of specific type.
        """

        # A list of samples that are similar to the given type
        samples_list = list()

        # For each sample in the given samples list
        for sample in self.samples_list:

            # If the types are matching
            if sample[1] == sample_type:

                # Append the sample to the list
                samples_list.append(sample)

        # Return the list of samples
        return samples_list

    ################################################################################################
    # @build_connected_paths
    ################################################################################################
    def build_soma(self,
                   axons_arbors,
                   basal_dendrites_arbors,
                   apical_dendrites_arbors):

        # Get the original profile points that are found in the SWC file
        soma_samples = self.get_samples_list_by_type(nmv.consts.Arbors.SWC_SOMA_SAMPLE_TYPE)

        # Get the soma profile points (contour)
        soma_profile_points = list()

        # Get the soma center and radius from the soma samples
        soma_centroid = Vector((0.0, 0.0, 0.0))
        soma_radius = 0.0

        # Filter the samples
        for sample in soma_samples:

            # If the sample has no parent (-1)
            if sample[-1] == nmv.consts.Arbors.SWC_NO_PARENT_SAMPLE_TYPE:

                # Get soma centroid
                soma_centroid = Vector((sample[nmv.consts.Arbors.SWC_SAMPLE_X_COORDINATES_IDX],
                                        sample[nmv.consts.Arbors.SWC_SAMPLE_Y_COORDINATES_IDX],
                                        sample[nmv.consts.Arbors.SWC_SAMPLE_Z_COORDINATES_IDX]))

                # Get soma radius
                soma_radius = sample[nmv.consts.Arbors.SWC_SAMPLE_RADIUS_IDX]

            # Otherwise, this is a profile point
            else:

                # Construct the profile point
                soma_profile_point = \
                    Vector((sample[nmv.consts.Arbors.SWC_SAMPLE_X_COORDINATES_IDX],
                            sample[nmv.consts.Arbors.SWC_SAMPLE_Y_COORDINATES_IDX],
                            sample[nmv.consts.Arbors.SWC_SAMPLE_Z_COORDINATES_IDX]))

                # Append the profile point to the list
                soma_profile_points.append(soma_profile_point)

        # Get the arbors profiles points, that represent the root sample of each arbor
        soma_profile_points_on_arbors = list()

        # Arbor points of the axons
        if axons_arbors is not None:

            # For each arbor
            for arbor in axons_arbors:

                # Get the initial sample along the arbor
                soma_profile_point = arbor.samples[0]

                # Append this point to the list
                soma_profile_points_on_arbors.append(soma_profile_point)

        # Arbor points of the apical dendrites
        if apical_dendrites_arbors is not None:

            # For each arbor
            for arbor in apical_dendrites_arbors:

                # Get the initial sample along the arbor
                soma_profile_point = arbor.samples[0]

                # Append this point to the list
                soma_profile_points_on_arbors.append(soma_profile_point)

        # Arbor points of the basal dendrites
        if basal_dendrites_arbors is not None:

            # For each arbor
            for arbor in basal_dendrites_arbors:

                # Get the initial sample along the arbor
                soma_profile_point = arbor.samples[0]

                # Append this point to the list
                soma_profile_points_on_arbors.append(soma_profile_point)

        # Construct the soma object
        soma_object = neuromorphovis.skeleton.Soma(
            centroid=soma_centroid, mean_radius=soma_radius,  profile_points=soma_profile_points,
            arbors_profile_points=soma_profile_points_on_arbors)

        # Return a reference to the soma object
        return soma_object

    ################################################################################################
    # @get_sections_from_path
    ################################################################################################
    def get_sections_from_path(self,
                               path,
                               sections_terminals):
        """Gets a list of sections from a given path.

        :param path:
            A given path that contains at least a single section.
        :param sections_terminals:
            A list of all the terminals of the sections.

        :return:
            A list of sections contained within the given path.
        """

        # A list of all the sections reconstructed from the path
        sections_lists = list()

        # Use each section terminal indices to identify the section and reconstruct it
        for section_terminals in sections_terminals:

            # The index of the first sample along the section
            first_sample_index = section_terminals[0]

            # The index of the last sample along the section
            last_sample_index = section_terminals[1]

            # A flag to indicate whether this sample should be added to the list or not
            collect = False

            # A list to contain all the samples along the section
            samples_list = list()

            # Iterate over the samples in the path
            for index in path:

                # Is this the first sample along the section
                if index == first_sample_index:

                    # Get the a nmv sample based on its index
                    nmv_sample = self.get_nmv_sample_from_samples_list(index)

                    # Append the sample to the list
                    samples_list.append(nmv_sample)

                    # Turn on the collection flag to start getting the in-between samples
                    collect = True

                    # Next sample
                    continue

                # If the collection flag is set
                if collect:

                    # Get the a nmv sample based on its index
                    nmv_sample = self.get_nmv_sample_from_samples_list(index)

                    # Append the sample to the list
                    samples_list.append(nmv_sample)

                # If this was the last sample
                if index == last_sample_index:

                    # Break and proceed to the next section
                    break

            # Construct an nmv section that ONLY contains the samples list, and UPDATE its other
            # members later when all the other sections are reconstructed
            nmv_section = neuromorphovis.skeleton.Section(samples=samples_list)

            # Append this section to the sections list
            sections_lists.append(nmv_section)

        # Return a reference to the reference list
        return sections_lists

    ################################################################################################
    # @build_connected_paths
    ################################################################################################
    @staticmethod
    def build_connected_paths(samples_list):
        """Constructs connected paths from a given list of samples. Each path is simply represented
        by a list of indices that can be used later to query the actual data of each sample.

        :param samples_list:
            A list of samples that are supposedly belonging to a single branch type.
        :return:
            A list of all the connected paths that are formed from the given list of samples.
        """

        # A list of paths
        paths_list = list()

        # Number of samples in the input list
        number_samples = len(samples_list)

        # The index of the current sample
        current_sample_index = 0

        # Proceed if we have more samples
        while current_sample_index < number_samples - 1:

            # If this is the soma sample, then ignore it
            # NOTE: Soma samples are indicated by -1 as a parent index
            if samples_list[current_sample_index][6] == -1:

                # Increment the sample index
                current_sample_index = current_sample_index + 1

                # Next sample
                continue

            # If this is a root sample with no parent, then ignore
            # NOTE: Root samples are indicated by 1 as a parent index
            if samples_list[current_sample_index][6] == 1:

                # Increment the sample index
                current_sample_index = current_sample_index + 1

                # Next sample
                continue

            # Construct a path here
            path = list()

            # Get the first sample along the section
            current_sample = samples_list[current_sample_index]

            # Add the parent sample, or the starting sample along the branch
            path.append(current_sample[6])

            # Add the current sample as well
            path.append(current_sample[0])

            # Increment the section of the current sample
            current_sample_index = current_sample_index + 1

            # Process the samples again
            for i in range(current_sample_index, number_samples):

                # If the parent index matches the current sample index
                if samples_list[i][6] == samples_list[i - 1][0]:

                    # Add this sample to the list
                    path.append(samples_list[i][0])

                    # Increment the sample index
                    current_sample_index = current_sample_index + 1

                else:

                    # No more samples to add to the path, so append the path to the list
                    paths_list.append(path)

                    # break the 'for' loop
                    break

        # Return a list of all the paths constructed from the list
        return paths_list

    ################################################################################################
    # @build_disconnected_sections_from_paths
    ################################################################################################
    def build_sections_from_paths(self,
                                  paths_list,
                                  section_type):
        """Builds a list of disconnected sections from a list of paths list, where each path can be
        composed of more than a single section.

        :param paths_list:
            A list of paths, where each path is composed of a list of indices that map to those
            of the samples given by the samples_list.
        :param section_type:
            The type of the section.
        :return:
            A list of sections, however, they are not connected and must be processed to build
            the tree of each arbor.
        """

        # Get a list of the starting samples of each path of the given paths
        starting_samples = list()

        # Also get a list of the ending samples of each path of the given paths
        ending_samples = list()

        # For each path in the list
        for path in paths_list:

            # Append the first sample to the list
            starting_samples.append(path[0])

            # Append the last samples to the list
            ending_samples.append(path[-1])

        # Remove the duplicated samples from the lists
        starting_samples = set(starting_samples)
        ending_samples = set(ending_samples)

        # Sort the starting samples
        starting_samples = sorted(starting_samples)

        # A list of all the sections
        sections_list = list()

        # For each path
        for path in paths_list:

            # A list that contains the indices of all the terminals of the sections on the path
            sections_terminal_indices = list()

            # Construct a list that accounts for the fork points of the path
            fork_samples = list()

            # Construct another list that contains the indices of the bifurcation samples
            bifurcation_samples = list()

            # For each starting sample
            for starting_sample_index in starting_samples:

                # If this sample is along the path
                if starting_sample_index in path:

                    # And also if this sample is not the first sample along the path
                    if not starting_sample_index == path[0]:

                        # Then this sample is a bifurcation sample, add it to the list
                        bifurcation_samples.append(starting_sample_index)

            # Construct the section samples terminals, add the first sample
            fork_samples.append(path[0])

            # Add the bifurcation samples
            for bifurcation_sample_index in bifurcation_samples:
                fork_samples.append(bifurcation_sample_index)

            # Add the terminal sample
            fork_samples.append(path[-1])

            # Construct the rest of the section
            for i_sample in range(0, len(fork_samples) - 1):

                # The index of the starting sample of the section
                starting_index = fork_samples[i_sample]

                # The index of the ending sample of the section
                ending_index = fork_samples[i_sample + 1]

                # Add the indices of the section terminals to the list
                sections_terminal_indices.append([starting_index, ending_index])

            # Get a list of all the sections on the current path
            path_sections_list = self.get_sections_from_path(path, sections_terminal_indices)

            # Append the reconstructed sections to the sections list
            sections_list.extend(path_sections_list)

        # Label the sections and set different indices to them
        for i, section in enumerate(sections_list):

            # Update the section index
            section.id = i

            # Update the section type
            section.type = section_type

        # Copy the sections list
        sections_list_clone = copy.deepcopy(sections_list)

        # Now, link the sections together relying on thr indices of the initial and final samples
        for i_section in sections_list:

            # Traversal
            for j_section in sections_list_clone:

                # Ignore processing the same section twice
                if i_section.id == j_section.id:
                    continue

                # Root sections
                if i_section.samples[0].parent_id == 1:

                    # Set the parent ID to None
                    i_section.parent_id = None

                    # Set the parent to None
                    i_section.parent = None

                # If the index of the first sample of the section is the last of another section
                if i_section.samples[0].id == j_section.samples[-1].id:

                    # Set the parent id to that of the parent section
                    i_section.parent_id = j_section.id

                    # Set the reference to the parent id to that of the parent section
                    i_section.parent = j_section

                # If the index of the last sample of the section is that of the first sample of
                # another section
                if i_section.samples[-1].id == j_section.samples[0].id:

                    # Append the child section id to the children section IDs
                    i_section.children_ids.append(j_section.id)

                    # Append a reference to the child section as well
                    i_section.children.append(j_section)

        # Return a list of all the disconnected sections
        return sections_list

    ################################################################################################
    # @read_file
    ################################################################################################
    def build_arbors_from_samples(self,
                                  arbor_type):
        """Builds a list of connected arbors from a list of disconnected samples for a given or
        specific type

        :param arbor_type:
            The type of the arbor.

        :return:
            A list of trees, each representing an arbor of the morphology skeleton.
        """

        # Get a list of samples that ONLY correspond to the given type
        samples_list = self.get_samples_list_by_type(sample_type=arbor_type)

        # Build connected paths (can include more than a single morphological section) from a list
        # of disconnected samples
        paths = self.build_connected_paths(samples_list)

        # Build sections from the constructed paths
        sections = self.build_sections_from_paths(paths, arbor_type)

        # Build a list of arbors from a list of sections
        arbors = nmv.skeleton.ops.build_arbors_from_sections(sections)

        # Return a reference to the constructed arbors
        return arbors

    ################################################################################################
    # @read_file
    ################################################################################################
    def read_file(self):
        """Reads an SWC morphology file and return a reference to a NeuroMorphoVis morphology
        structure.

        :return:
            Returns a reference to a NeuroMorphoVis morphology structure that contains the skeleton.
        """

        # Read all the samples from the morphology file an store them into a list
        self.read_samples()

        # Build the basal dendrites
        basal_dendrites_arbors = self.build_arbors_from_samples(
            nmv.consts.Arbors.SWC_BASAL_DENDRITE_SAMPLE_TYPE)

        # Build the axon, or axons if the morphology has more than a single axon
        # NOTE: For consistency, if we have more than a single axon, we use the principal one and
        # add the others later to the basal dendrites list
        axon_arbor = None
        axons_arbors = self.build_arbors_from_samples(nmv.consts.Arbors.SWC_AXON_SAMPLE_TYPE)
        if axons_arbors is not None:

            # Set the principal axon
            axon_arbor = axons_arbors[0]

            # If we have more than a single axon, use the principal one and move the others to the
            # basal dendrites
            if len(axons_arbors) > 1:

                # Add the others to the basal dendrites
                for i in range(1, len(axons_arbors)):
                    basal_dendrites_arbors.append(axons_arbors[i])

        # Build the apical dendrites, or apical dendrites if the morphology has more than a
        # single apical dendrites
        # NOTE: For consistency, if we have more than a single morphology, we use the principal one
        # and add the others later to the basal dendrites list
        apical_dendrite_arbor = None
        apical_dendrites_arbors = self.build_arbors_from_samples(
            nmv.consts.Arbors.SWC_APICAL_DENDRITE_SAMPLE_TYPE)
        if apical_dendrites_arbors is not None:

            # Set the principal axon
            apical_dendrite_arbor = apical_dendrites_arbors[0]

            # If we have more than a single axon, use the principal one and move the others to the
            # basal dendrites
            if len(apical_dendrites_arbors) > 1:

                # Add the others to the basal dendrites
                for i in range(1, len(apical_dendrites_arbors)):
                    basal_dendrites_arbors.append(apical_dendrites_arbors[i])

        # Build the soma
        soma = self.build_soma(
            axons_arbors=axons_arbors,
            basal_dendrites_arbors=basal_dendrites_arbors,
            apical_dendrites_arbors=apical_dendrites_arbors)

        # Update the morphology label
        label = neuromorphovis.file.ops.get_file_name_from_path(self.morphology_file)

        # Construct the morphology skeleton
        nmv_morphology = neuromorphovis.skeleton.Morphology(
            soma=soma, axon=axon_arbor, dendrites=basal_dendrites_arbors,
            apical_dendrite=apical_dendrite_arbor, label=label)

        # Return a reference to the reconstructed morphology skeleton
        return nmv_morphology
