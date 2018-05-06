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

# Blender imports
from mathutils import Vector

# Internal imports
import neuromorphovis.file
import neuromorphovis.skeleton


####################################################################################################
# @H5Reader
####################################################################################################
class H5Reader:
    """.H5 morphology reader
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 h5_file):
        """Constructor

        :param h5_file:
            A given .H5 morphology file.
        """

        # Set the path to the given h5 file
        self.morphology_file = h5_file

    ################################################################################################
    # @build_tree
    ################################################################################################
    @staticmethod
    def build_tree(sections):
        """Build the tree of the morphology by linking the parent node and the children ones.

        :param sections:
            A linear list of sections of a specific type to be converted to a tree.
        """

        # For each section, get the IDs of the children nodes, then find and append them to the
        # children lists.
        # Also find the ID of the parent node and update the parent accordingly.
        for i_section in sections:
            # First round
            for child_id in i_section.children_ids:
                for j_section in sections:
                    if child_id == j_section.id:
                        i_section.children.append(j_section)

            # Second round
            for k_section in sections:
                if i_section.parent_id == k_section.id:
                    i_section.parent = k_section

    ################################################################################################
    # @build_single_arbor
    ################################################################################################
    @staticmethod
    def build_single_arbor(sections):
        """Build the set of sections into a single arbor tree.

        NOTE: This function is mainly used for axons and apical dendrites. However,
        and in certain cases, the morphology might have more than a single apical dendrite or
        even more than one axon, but it is quite rare to occur.

        :param sections:
            A list of sections of the arbor.
        :return:
            A reference to the root node of the arbor tree.
        """
        # A list of roots
        roots = list()

        # Iterate over the sections and get the root ones
        for i_section in sections:
            if i_section.parent_id == 0:
                roots.append(i_section)

        # NOTE: If the root list does not contain any roots, then return None. If the list has a
        # single root, then return the root object by getting the first element in the list.
        if len(roots) == 0:
            return None
        elif len(roots) == 1:
            return roots[0]

    ################################################################################################
    # @build_multiple_arbors
    ################################################################################################
    @staticmethod
    def build_multiple_arbors(sections):
        """
        Returns a node, or a list of nodes where we can access the different sections of
        a single arbor as a tree. For the axon and apical dendrites, the function returns the
        root of a single branch. However, for the basal dendrites, the function returns a list
        of roots, where each root reflects a single independent branch emanating from the soma.

        :param sections:
            A linear list of axons sections.
        :return:
            A list containing references to the root nodes of the arbors.
        """

        # A list of roots
        roots = list()

        # Iterate over the sections and get the root ones
        for i_section in sections:
            if i_section.parent_id == 0:
                roots.append(i_section)

        # If the list does not contain any roots, then return None, otherwise return the entire list
        if len(roots) == 0:

            # Return None
            return None

        else:

            # Return the root list
            return roots

    ################################################################################################
    # @get_arbors_profile_points
    ################################################################################################
    @staticmethod
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
        arbor_profile_points = []

        for arbor in arbors:

            # Make sure that this arbor exists in the morphology
            if arbor is not None:

                # Get the first sample along the root of the tree
                arbor_profile_points.append(arbor.samples[0].point)

        # Return the list
        return arbor_profile_points

    ####################################################################################################
    # @build_soma
    ####################################################################################################
    def build_soma(self,
                   points_list,
                   structure_list,
                   axon_tree=None,
                   basal_dendrites_trees=None,
                   apical_dendrite_tree=None):
        """Builds the soma and returns a reference to it.

        :param points_list:
            Morphology point list.
        :param structure_list:
            Morphology section list.
        :param axon_tree:
            The reconstructed tree of the axon.
        :param basal_dendrites_trees:
            The reconstructed trees of the basal dendrites.
        :param apical_dendrite_tree:
            The reconstructed tree of the apical dendrite.
        :return:
            A reference to the soma object.
        """

        # Get the index of the starting point of the soma section
        soma_section_first_point_index = structure_list[0][0]

        # Get the index of the last point of the soma section
        soma_section_last_point_index = structure_list[1][0]

        # Get the positions of each sample along the soma section
        soma_profile_points = []

        # Update the soma profile point list
        for i_sample in range(soma_section_first_point_index, soma_section_last_point_index):

            # Profile point
            x = points_list[i_sample][0]
            y = points_list[i_sample][1]
            z = points_list[i_sample][2]
            profile_point = Vector((x, y, z))

            # Add the profile point to the list
            soma_profile_points.append(profile_point)

        # Compute soma centroid
        soma_centroid = Vector((0.0, 0.0, 0.0))
        for i_point in soma_profile_points:
            soma_centroid += i_point
        soma_centroid /= len(soma_profile_points)

        # Compute the soma mean radius
        mean_soma_radius = 0.0
        for i_point in soma_profile_points:
            distance = i_point - soma_centroid
            mean_soma_radius += distance.length
        mean_soma_radius /= len(soma_profile_points)

        # Compute the profile points from the arbors
        arbors_profile_points = []

        # Axon profile point
        if axon_tree is not None:
            arbors_profile_points.extend(self.get_arbors_profile_points([axon_tree]))

        # Basal dendrites points
        if basal_dendrites_trees is not None:
            arbors_profile_points.extend(self.get_arbors_profile_points(basal_dendrites_trees))

        # Apical dendrite profile point
        if apical_dendrite_tree is not None:
            arbors_profile_points.extend(self.get_arbors_profile_points([apical_dendrite_tree]))

        # Construct the soma object
        soma_object = neuromorphovis.skeleton.Soma(
            centroid=soma_centroid, mean_radius=mean_soma_radius,
            profile_points=soma_profile_points, arbors_profile_points=arbors_profile_points)

        # Return a reference to the soma object
        return soma_object

    ################################################################################################
    # @read_file
    ################################################################################################
    def read_file(self):
        """Read a morphology skeleton given in .H5 file.

        :return:
        """

        # A list of data
        data = None

        # Import the h5py module to read the .H5 file
        try:

            # Import the h5py module
            import h5py

            # Read the h5 file using the python module into a data array
            data = h5py.File(self.morphology_file, 'r')

        # Raise an exception if we cannot import the h5py module
        except ImportError:

            # Report the issue
            print('FATAL_ERROR: Cannot find a compatible h5py version!')

            # Exit the system
            exit(0)

        # The h5 file contains, normally, three directories: 'points, structure and perimeters'
        points_directory = '/points'
        structure_directory = '/structure'
        perimeters_directory = '/perimeters'

        # The data will be stored in three lists: points, structure and perimeters
        points_list = None
        structure_list = None
        perimeters_list = None

        # Read the point list
        try:
            points_list = data[points_directory].value
        except ImportError:
            nmv.logger.log('ERROR: Cannot load the data points from [%s]' % self.morphology_file)

        # Get the structure list
        try:
            structure_list = data[structure_directory].value
        except ImportError:
            nmv.logger.log('ERROR: Cannot load the data structure from [%s]' % self.morphology_file)

        # Get the number of points or samples in the file
        number_points = len(points_list)

        # Get the number of sections in the file
        number_sections = len(structure_list)

        # Parse the sections and add them to a linear list [index, parent, type, samples]
        parsed_sections = []

        for i_section in range(1, number_sections - 1):

            # Get the index of the starting point of the section
            section_first_point_index = structure_list[i_section][0]

            # Get the index of the last point of the section
            section_last_point_index = structure_list[i_section + 1][0]

            # Section index
            section_index = i_section

            # Get section type
            section_type = structure_list[i_section][1]

            # Get the section parent index
            section_parent_index = int(structure_list[i_section][2])

            # Get the positions and radii of each sample along the section
            section_samples = []
            i = 0
            for i_sample in range(section_first_point_index, section_last_point_index):

                # Position
                x = points_list[i_sample][0]
                y = points_list[i_sample][1]
                z = points_list[i_sample][2]
                point = Vector((x, y, z))

                # Radius
                # NOTE: What is reported in our .H5 files is the diameter not the radius
                radius = points_list[i_sample][3] / 2.0

                # Build sample
                section_sample = neuromorphovis.skeleton.Sample(
                    point=point, radius=radius, id=i, morphology_id=i)

                # Add the sample to the list
                section_samples.append(section_sample)

                # Next sample
                i += 1

            # Build a temporary section list until all the sections are parsed
            parsed_section = [section_index, section_parent_index, section_type, section_samples]

            # Add this section to the parsed sections list
            parsed_sections.append(parsed_section)

        # Traverse the tree and construct the arbors.

        # A linear list of the axon sections
        axon_sections = []

        # A linear list of basal dendrites sections
        basal_dendrites_sections = []

        # A linear list of the apical dendrites sections
        apical_dendrites_sections = []

        # Construct a tree of sections and filter them based on their type
        for i_parsed_section in parsed_sections:

            # Section ID
            section_id = i_parsed_section[0]

            # Section parent ID
            section_parent_id = i_parsed_section[1]

            # Section children IDs, if exist
            section_children_ids = []
            for j_parsed_section in parsed_sections:

                # If the parent ID of another section is equivalent to the ID of this section, then
                # it is a child
                if section_id == j_parsed_section[1]:
                    section_children_ids.append(j_parsed_section[0])

            # Section type
            section_type = i_parsed_section[2]

            # Section samples
            section_samples = i_parsed_section[3]

            # Construct a skeleton section
            skeleton_section = neuromorphovis.skeleton.Section(
                id=section_id, parent_id=section_parent_id, children_ids=section_children_ids,
                samples=section_samples, type=section_type)

            # Add the skeleton section to the corresponding list
            # For neurons the values are: 1: soma, 2: axon, 3: basal dendrite, 4: apical dendrite
            # For glia cells the values are: 1: soma, 2: glia process, 3 glia end-foot

            # Axon
            if section_type == 2:

                # Add the section to the axon list
                axon_sections.append(skeleton_section)

            # Basal dendrite
            elif section_type == 3:

                # Add the section to the basal dendrites list
                basal_dendrites_sections.append(skeleton_section)
            elif section_type == 4:

                # Add the section to the apical dendrites list
                apical_dendrites_sections.append(skeleton_section)
            else:

                # Undefined
                print('ERROR: Unknown section type')

        # Build the axon tree
        self.build_tree(axon_sections)

        # Build the basal dendritic tree
        self.build_tree(basal_dendrites_sections)

        # Build the apical dendritic tree
        self.build_tree(apical_dendrites_sections)

        # Build the axon arbor
        axon = self.build_single_arbor(axon_sections)

        # Build the basal dendritic arbors
        basal_dendrites = self.build_multiple_arbors(basal_dendrites_sections)

        # Build the apical dendritic tree
        # NOTE: We will use the build_multiple_arbors procedure to build the apical dendrite and
        # will verify later if more than a single arbor exists in the list
        apical_dendrites = self.build_multiple_arbors(apical_dendrites_sections)

        # A reference to the apical dendrite
        apical_dendrite = None

        # If the morphology contains apical dendrites
        if apical_dendrites is not None:

            # If the length of the apical dendrites list is greate than one, then set the first
            # arbor to be the apical dendrite and append the rest of the arbors to the basal
            # dendrites list
            if len(apical_dendrites) == 1:

                # Set the first and only element in the apical dendrites list to be the apical
                # dendrite
                apical_dendrite = apical_dendrites[0]

            # Otherwise, append the rest of the apical dendrites arbors to the basal dendrites list
            else:

                # Set the first in the apical dendrites list to be the apical dendrite
                apical_dendrite = apical_dendrites[0]

                for i in range(1, len(apical_dendrites)):
                    basal_dendrites.append(apical_dendrites[i])

        # Build the soma
        soma_object = self.build_soma(points_list, structure_list)

        # Update the morphology label
        label = neuromorphovis.file.ops.get_file_name_from_path(self.morphology_file)

        # Construct the morphology skeleton
        morphology_skeleton = neuromorphovis.skeleton.Morphology(
            soma=soma_object, axon=axon, dendrites=basal_dendrites,
            apical_dendrite=apical_dendrite, label=label)

        # Return a reference to the reconstructed morphology skeleton
        return morphology_skeleton
