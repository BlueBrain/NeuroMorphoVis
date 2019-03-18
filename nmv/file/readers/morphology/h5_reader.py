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

# Blender imports
from mathutils import Vector

# Internal imports
import nmv
import nmv.consts
import nmv.file
import nmv.skeleton


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

        # A list of all the points in the morphology file
        self.points_list = list()

        # A list of all the connectivity data in the morphology file
        self.structure_list = list()

        # A list of all the perimeters that are specific to astrocyte morphologies
        self.perimeters_list = list()

    ################################################################################################
    # @build_tree
    ################################################################################################
    @staticmethod
    def build_tree(sections_list):
        """Builds the tree of the morphology by linking the parent node and the children ones.

        :param sections_list:
            A linear list of sections of a specific type to be converted to a tree.
        """

        # For each section, get the IDs of the children nodes, then find and append them to the
        # children lists.
        # Also find the ID of the parent node and update the parent accordingly.
        branching_order = 0
        for i_section in sections_list:

            # First round
            for child_id in i_section.children_ids:

                # For each section
                for j_section in sections_list:

                    # Is it a child
                    if child_id == j_section.id:

                        # Append it to the list
                        i_section.children.append(j_section)

            # Second round
            for k_section in sections_list:

                # Is it parent
                if i_section.parent_id == k_section.id:

                    # Set it to be a parent
                    i_section.parent = k_section

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

    ################################################################################################
    # @build_soma
    ################################################################################################
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
        soma_profile_points = list()

        # Update the soma profile point list
        for i_sample in range(soma_section_first_point_index, soma_section_last_point_index):

            # Profile point
            x = points_list[i_sample][nmv.consts.Arbors.H5_SAMPLE_X_COORDINATES_IDX]
            y = points_list[i_sample][nmv.consts.Arbors.H5_SAMPLE_Y_COORDINATES_IDX]
            z = points_list[i_sample][nmv.consts.Arbors.H5_SAMPLE_Z_COORDINATES_IDX]
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
        arbors_profile_points = list()

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
        nmv_soma = nmv.skeleton.Soma(
            centroid=soma_centroid, mean_radius=mean_soma_radius,
            profile_points=soma_profile_points, arbors_profile_points=arbors_profile_points)

        # Return a reference to the soma object
        return nmv_soma

    ################################################################################################
    # @read_points_and_structures
    ################################################################################################
    def read_points_and_structures(self):
        """Reads the content of the morphology file, mainly the points and the connectivity data.

        :return:
            Returns None in case of invalid directories.
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
            nmv.logger.log('FATAL_ERROR: Cannot find a compatible \'h5py\' version!')

            # Exit NMV
            exit(0)

        try:

            # Read the point list from the points directory
            self.points_list = data[nmv.consts.Arbors.H5_POINTS_DIRECTORY].value

        except ImportError:

            # Error
            nmv.logger.log('ERROR: Cannot load the data points from [%s]' % self.morphology_file)

            # Return None
            return None

        try:

            # Get the structure list from the structures directory
            self.structure_list = data[nmv.consts.Arbors.H5_STRUCTURE_DIRECTORY].value

        except ImportError:

            nmv.logger.log('ERROR: Cannot load the data structure from [%s]' % self.morphology_file)

            # Return None
            return None

        # The file has been read successfully
        return True

    ################################################################################################
    # @build_sections_from_points_and_structures
    ################################################################################################
    def build_sections_from_points_and_structures(self):
        """Builds a list of sections from the data obtained from the .H5 files

        :return:
            A linear list of sections of the entire morphology.
        """

        # Parse the sections and add them to a linear list [index, parent, type, samples]
        sections_list = list()

        for i_section in range(1, len(self.structure_list) - 1):

            # Get the index of the starting point of the section
            section_first_point_index = self.structure_list[i_section][0]

            # Get the index of the last point of the section
            section_last_point_index = self.structure_list[i_section + 1][0]

            # Section index
            section_index = i_section

            # Get section type
            # 1: soma, 2: axon, 3: basal dendrite, 4: apical dendrite.
            section_type = self.structure_list[i_section][1]

            # Get the section parent index
            section_parent_index = int(self.structure_list[i_section][2])

            # Get the positions and radii of each sample along the section
            samples = list()

            # Sample index
            sample_index = 0

            # Reconstruct the samples
            for i_sample in range(section_first_point_index, section_last_point_index):

                # Position
                x = self.points_list[i_sample][nmv.consts.Arbors.H5_SAMPLE_X_COORDINATES_IDX]
                y = self.points_list[i_sample][nmv.consts.Arbors.H5_SAMPLE_Y_COORDINATES_IDX]
                z = self.points_list[i_sample][nmv.consts.Arbors.H5_SAMPLE_Z_COORDINATES_IDX]
                point = Vector((x, y, z))

                # Radius
                # NOTE: What is reported in our .H5 files is the diameter unlike the .SWC files
                radius = self.points_list[i_sample][nmv.consts.Arbors.H5_SAMPLE_RADIUS_IDX] / 2.0

                # Build a NeuroMorphoVis sample
                nmv_sample = nmv.skeleton.Sample(
                    point=point, radius=radius, id=sample_index, morphology_id=sample_index,
                    type=section_type)

                # Add the sample to the list
                samples.append(nmv_sample)

                # Next sample
                sample_index += 1

            # Build a section list until all the sections are parsed
            section = [section_index, section_parent_index, section_type, samples]

            # Add this section to the parsed sections list
            sections_list.append(section)

        # Return a reference to the sections list
        return sections_list

    ################################################################################################
    # @read_file
    ################################################################################################
    def read_file(self):
        """Read a morphology skeleton given in .H5 file into a NeuroMorphoVis morphology structure.

        :return:
            Returns a reference to a NeuroMorphoVis morphology as read from the file.
        """

        # Read the content of the .H5 file
        self.read_points_and_structures()

        # Build sections from the parsed points and structures from the morphology file
        sections_list = self.build_sections_from_points_and_structures()

        # A linear list of the sections of the axons
        axons_sections = list()

        # A linear list of basal dendrites sections
        basal_dendrites_sections = list()

        # A linear list of the apical dendrites sections
        apical_dendrites_sections = list()

        # Construct a tree of sections and filter them based on their type
        for i_section in sections_list:

            # Section ID
            section_id = i_section[0]

            # Section parent ID
            section_parent_id = i_section[1]

            # Section children IDs, if exist
            section_children_ids = list()

            for j_section in sections_list:

                # If the parent ID of another section is equivalent to the ID of this section, then
                # it is a child
                if section_id == j_section[1]:

                    # Append it
                    section_children_ids.append(j_section[0])

            # Section type
            section_type = i_section[2]

            # Section samples
            section_samples = i_section[3]

            # Construct a skeleton section
            nmv_section = nmv.skeleton.Section(
                id=section_id, parent_id=section_parent_id, children_ids=section_children_ids,
                samples=section_samples, type=section_type)

            # Axon
            if section_type == nmv.consts.Arbors.H5_AXON_SECTION_TYPE:

                # Add the section to the axons list
                axons_sections.append(nmv_section)

            # Basal dendrite
            elif section_type == nmv.consts.Arbors.H5_BASAL_DENDRITE_SECTION_TYPE:

                # Add the section to the basal dendrites list
                basal_dendrites_sections.append(nmv_section)

            # Apical dendrite
            elif section_type == nmv.consts.Arbors.H5_APICAL_DENDRITE_SECTION_TYPE:

                # Add the section to the apical dendrites list
                apical_dendrites_sections.append(nmv_section)

            # Undefined section type
            else:

                # Report an error
                nmv.logger.log('ERROR: Unknown section type [%s] !' % str(section_type))

        # Build the axon tree
        self.build_tree(axons_sections)

        # Build the basal dendritic tree
        self.build_tree(basal_dendrites_sections)

        # Build the apical dendritic tree
        self.build_tree(apical_dendrites_sections)

        # Build the basal dendritic arbors
        basal_dendrites_arbors = nmv.skeleton.ops.build_arbors_from_sections(
            basal_dendrites_sections)

        # Build the axon, or axons if the morphology has more than a single axon
        # NOTE: For consistency, if we have more than a single axon, we use the principal one and
        # add the others later to the basal dendrites list
        axon_arbor = None
        axons_arbors = nmv.skeleton.ops.build_arbors_from_sections(axons_sections)
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
        apical_dendrites_arbors = nmv.skeleton.ops.build_arbors_from_sections(
            apical_dendrites_sections)

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
        nmv_soma = self.build_soma(self.points_list, self.structure_list)

        # Update the morphology label
        label = nmv.file.ops.get_file_name_from_path(self.morphology_file)

        # Construct the morphology skeleton
        nmv_morphology = nmv.skeleton.Morphology(
            soma=nmv_soma, axon=axon_arbor, dendrites=basal_dendrites_arbors,
            apical_dendrite=apical_dendrite_arbor, label=label)

        # Return a reference to the reconstructed morphology skeleton
        return nmv_morphology
