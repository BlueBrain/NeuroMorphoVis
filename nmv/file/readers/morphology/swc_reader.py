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

# System imports
import copy

# Blender imports
from mathutils import Vector

# Internal imports
import nmv
import nmv.consts
import nmv.file
import nmv.skeleton


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
        self.samples_list = list()

        # A list of the indices of the terminals of the sections
        # This list is only updated once during the morphology loading, and then used to build the
        # sections later in an accelerated way
        self.sections_terminal_samples_indices = list()

        # A list of the indices of each 'disconnected' section in the morphology
        self.sections_samples_indices_list = list()

        # A list of continuous paths extracted from the morphology file
        self.paths = list()

    ################################################################################################
    # @build_connected_paths_from_samples
    ################################################################################################
    def build_connected_paths_from_samples(self):
        """Construct a list of connected paths from the samples.
        """

        # Since we have the soma index equal to 1, then start from index number 2
        index = 2

        # A temporary list to append the indices of each path
        path = list()

        # Process the entire samples list
        while True:

            # Iterate over two samples to verify their connectivity
            sample_i = self.samples_list[index]
            sample_j = self.samples_list[index + 1]

            if sample_i is None or sample_j is None:
                index = index + 1
                continue

            # Ensure that this is not a soma profile point
            if sample_i[nmv.consts.Arbors.SWC_SAMPLE_TYPE_IDX] == \
                    nmv.consts.Arbors.SWC_SOMA_SAMPLE_TYPE:
                index = index + 1
                continue

            # If the two samples are connected
            if sample_j[-1] == sample_i[0]:

                # Add the first sample to the path
                path.append(sample_i[0])

                # Append the last sample in the morphology file
                if index + 1 == self.samples_list[-1][0]:
                    path.append(sample_j[0])

            # Otherwise
            else:

                # Append the last sample to the path
                # path.append(sample_j[-1])
                path.append(sample_i[0])

                # Append the path to the paths list
                self.paths.append(path)

                # Clear the path list to search for a new path
                path = list()

            # Increment the path
            index = index + 1

            # If processing the list is break
            if index > len(self.samples_list) - 2:

                # Append the last path
                self.paths.append(path)

                # Then break
                break

        # Add the starting points and mark the terminals
        for path in self.paths:

            # Get the index of the first sample along the path
            first_sample_index = path[0]

            # Then add the parent sample index at the beginning of the path
            path.insert(0, self.samples_list[first_sample_index][-1])

            # Marking the terminals by adding the indices of the first and last samples
            self.sections_terminal_samples_indices.append(path[0])
            self.sections_terminal_samples_indices.append(path[-1])

        # Sort the sections_terminal_samples_indices list
        self.sections_terminal_samples_indices = sorted(self.sections_terminal_samples_indices)

        # Filter the repeated entries in the sections_terminal_samples_indices list
        self.sections_terminal_samples_indices = list(set(self.sections_terminal_samples_indices))

    ################################################################################################
    # @build_sections_from_paths
    ################################################################################################
    def build_sections_from_paths(self):
        """Builds a list of sections from the paths reconstructed during the reading of the
        morphology.
        """

        for path in self.paths:

            # A list of all the samples located along the path
            samples_located_along_path = list()

            # Get the list
            for sample_index in self.sections_terminal_samples_indices:

                # If the sample index exists in the path
                if sample_index in path:

                    # Append it to the list
                    samples_located_along_path.append(sample_index)

            # Order the list
            samples_located_along_path = sorted(samples_located_along_path)

            # Build the sections
            for i in range(0, len(samples_located_along_path) - 1):

                section_indices = list()

                # Get the first index along the section
                first_sample = samples_located_along_path[i]

                # Get the last index along the section
                last_sample = samples_located_along_path[i + 1]

                first_sample_index = path.index(first_sample)

                last_sample_index = path.index(last_sample)

                for j in range(first_sample_index, last_sample_index + 1):

                    section_indices.append(path[j])

                self.sections_samples_indices_list.append(section_indices)

    ################################################################################################
    # @read_samples
    ################################################################################################
    def read_samples(self):
        """Reads an SWC files and returns a list of all the samples in the file"""

        # Open the file, read it line by line and store the result in list.
        morphology_file = open(self.morphology_file, 'r')

        initial_samples_list = list()

        # Add a dummy sample to the list at index 0 to match the indices
        # The zeroth sample always defines the soma parameters, and it is parsed independently
        initial_samples_list.append([0, 0, 0.0, 0.0, 0.0, 0.0, 0])

        # Translation vector in case the file is not centered at the origin
        translation = Vector((0.0, 0.0, 0.0))

        # Construct a string from each line in the morphology file
        string_list = list()
        for line in morphology_file:
            string_list.append(line)

        # For each line in the string list
        for line in string_list:

            # Ignore lines with comments that have '#'
            if '#' in line:
                continue

            # Ignore empty lines
            if not line.strip():
                continue

            # Extract the data from the line
            data = ' '.join(line.split())
            data = data.strip('\n').split(' ')

            # If unwanted characters exit, remove them
            for i in data:

                # Unwanted spaces
                if i == '':
                    data.remove(i)

                # Unwanted new lines
                if '\n' in i:
                    i.replace('\n', '')

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

            # If this is the soma sample, get the translation vector
            if parent_index == -1:

                translation[0] = x
                translation[1] = y
                translation[2] = z

            # Update the coordinates if the morphology is transformed
            x = x - translation[0]
            y = y - translation[1]
            z = z - translation[2]

            # Add the sample to the list
            initial_samples_list.append([index, sample_type, x, y, z, radius, parent_index])

        # Search for the maximum index of the samples
        maximum_index = 0
        for i_sample in initial_samples_list:
            if i_sample[0] > maximum_index:
                maximum_index = i_sample[0]

        # Create the actual samples list
        for i in range(maximum_index + 1):
            self.samples_list.append(None)

        # Set the samples at their corresponding indices to make it easy to index them, and keep
        # the rest to Null and double check them later
        for i_sample in initial_samples_list:
            self.samples_list[i_sample[0]] = i_sample

        # Construct the connected paths from the samples list
        self.build_connected_paths_from_samples()

        # Construct the individual sections from the paths
        self.build_sections_from_paths()

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
        nmv_sample = nmv.skeleton.Sample(
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
        selected_samples_list = list()

        # For each sample in the given samples list
        for sample in self.samples_list:

            if sample is None:
                continue

            # If the types are matching
            if sample[1] == sample_type:

                # Append the sample to the list
                selected_samples_list.append(sample)

        # Return the list of samples
        return selected_samples_list

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

            # If the sample has no parent (-1), then this is the soma itself
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
                soma_profile_point = arbor.samples[0].point

                # Append this point to the list
                soma_profile_points_on_arbors.append(soma_profile_point)

        # Arbor points of the apical dendrites
        if apical_dendrites_arbors is not None:

            # For each arbor
            for arbor in apical_dendrites_arbors:

                # Get the initial sample along the arbor
                soma_profile_point = arbor.samples[0].point

                # Append this point to the list
                soma_profile_points_on_arbors.append(soma_profile_point)

        # Arbor points of the basal dendrites
        if basal_dendrites_arbors is not None:

            # For each arbor
            for arbor in basal_dendrites_arbors:

                # Get the initial sample along the arbor
                soma_profile_point = arbor.samples[0].point

                # Append this point to the list
                soma_profile_points_on_arbors.append(soma_profile_point)

        # If the soma radius is zero, then get the average of the profile points if exist
        if soma_radius < 1e-5:

            # Set a new radius based on the profile points if they are there
            if len(soma_profile_points) > 0:
                soma_radius = 0.0
                for point in soma_profile_points:
                    soma_radius += point.length
                soma_radius = soma_radius / len(soma_profile_points)

            # Otherwise, use the profile points to get the average radius
            else:
                soma_radius = 0.0
                for point in soma_profile_points_on_arbors:
                    soma_radius += point.length
                soma_radius = soma_radius / len(soma_profile_points_on_arbors)

        # Construct the soma object
        soma_object = nmv.skeleton.Soma(
            centroid=soma_centroid, mean_radius=soma_radius,  profile_points=soma_profile_points,
            arbors_profile_points=soma_profile_points_on_arbors)

        # Return a reference to the soma object
        return soma_object

    ################################################################################################
    # @get_sections_of_specific_type
    ################################################################################################
    def get_sections_of_specific_type(self,
                                      arbor_type):
        """Returns a list of sections of specific type.

        :param arbor_type:
            The type of the requested sections.
        :return:
            A list of all the sections that have specific type.
        """

        sections_list = list()

        # A list that only contains the arbors of the requested type
        arbor_sections_samples_indices_list = list()

        # For each section
        for section_samples_indices in self.sections_samples_indices_list:

            # Get the last sample along this section
            last_sample = self.samples_list[section_samples_indices[-1]]

            # If the type is matching
            if str(last_sample[1]) == str(arbor_type):

                # Append to the list
                arbor_sections_samples_indices_list.append(section_samples_indices)

        # For each section
        for arbor_section in arbor_sections_samples_indices_list:

            # Construct the samples list
            samples_list = list()

            # For each sample in the section
            for arbor_sample_index in arbor_section:

                # Ignore the soma sample
                if self.samples_list[arbor_sample_index][0] == 1:
                    continue

                # Get the a nmv sample based on its index
                nmv_sample = self.get_nmv_sample_from_samples_list(arbor_sample_index)

                samples_list.append(nmv_sample)

            # Construct an nmv section that ONLY contains the samples list, and UPDATE its other
            # members later when all the other sections are reconstructed
            nmv_section = nmv.skeleton.Section(samples=samples_list)

            # Append the reconstructed sections to the sections list
            sections_list.append(nmv_section)

        # Label the sections and set different indices to them
        for i, section in enumerate(sections_list):

            # Update the section index
            section.id = i

            # Update the section type
            section.type = arbor_type

        # Updates the sections parenting
        for section in sections_list:
            nmv.skeleton.ops.update_section_parenting(section, sections_list)

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

        # Get the sections that are specific to the arbor
        sections = self.get_sections_of_specific_type(arbor_type)

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

                # If the basal dendrites list is empty
                if basal_dendrites_arbors is None:

                    # Create a list to be able to append the other arbors
                    basal_dendrites_arbors = list()

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

                # If the basal dendrites list is empty
                if basal_dendrites_arbors is None:

                    # Create a list to be able to append the other arbors
                    basal_dendrites_arbors = list()

                # Add the others to the basal dendrites
                for i in range(1, len(apical_dendrites_arbors)):
                    basal_dendrites_arbors.append(apical_dendrites_arbors[i])

        # Build the soma
        soma = self.build_soma(
            axons_arbors=axons_arbors,
            basal_dendrites_arbors=basal_dendrites_arbors,
            apical_dendrites_arbors=apical_dendrites_arbors)

        # Update the morphology label
        label = nmv.file.ops.get_file_name_from_path(self.morphology_file)

        # Construct the morphology skeleton
        nmv_morphology = nmv.skeleton.Morphology(
            soma=soma, axon=axon_arbor, dendrites=basal_dendrites_arbors,
            apical_dendrite=apical_dendrite_arbor, label=label)

        # Return a reference to the reconstructed morphology skeleton
        return nmv_morphology
