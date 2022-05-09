####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
import nmv.consts
import nmv.file
import nmv.skeleton
import nmv.utilities


####################################################################################################
# @load_h5py
####################################################################################################
def load_h5py():
    """Loads the h5py module, and makes sure that it is loaded to be able to proceed.

    """
    # Import h5py and install it if it does not exist
    try:
        import h5py
    except ImportError:
        print('Package *h5py* is not installed. Installing it....')
        nmv.utilities.pip_install_wheel(package_name='h5py')

    # Import the h5py module, even after the installation and return it
    import h5py
    return h5py


####################################################################################################
# @H5Reader
####################################################################################################
class H5Reader:
    """.H5 morphology reader

    In this version of NMV, this reader loads is capable of reading neuronal morphologies with h5v1
    files that are compliant with the BBP/HBP specification for version 1.
    Further details can be found in the following links:
    https://github.com/BlueBrain/morphology-documentation/blob/main/source/h5v1.rst
    https://developer.humanbrainproject.eu/docs/projects/morphology-documentation/0.0.2/h5v1.html
    The loader can load astrocyte morphologies that are stored in H5 files based on the script
    integrated in NMV. This file format is an extension to the h5v1 format, with endfeet data
    included. This format is being used until we have a stable specification, in which we can
    directly use the MorphIO loader to read all the NGV structures from multi-populated circuits.

    NOTE: For astrocytes, the morphologies are loaded at the origin unless users want to visualize
    them in their global coordinates.
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

        # A list of all the endfeet, if the input morphology is an H5 file
        self.endfeet_list = list()

        # A list of the profile points of the soma
        self.profile_points = list()

        # The centroid of the morphology, should be the origin, unless the profile points are skewed
        self.centroid = Vector((0.0, 0.0, 0.0))

        # The original centroid, as loaded from the file, or computed from the profile points
        self.original_centroid = Vector((0.0, 0.0, 0.0))

    ################################################################################################
    # @is_astrocyte_morphology_with_endfeet
    ################################################################################################
    def is_astrocyte_morphology_with_endfeet(self):
        """Checks if the read H5 file is a morphology file with endfeet data.

        :return:
            Returns True if the loaded morphology is an astrocyte morphology with endfeet, and
            False otherwise.
        """

        # Load the h5py module
        h5py = load_h5py()

        # Read the h5 file using the python module into a data array
        data = h5py.File(self.morphology_file, 'r')

        # Astrocyte-specific directories
        directories = [nmv.consts.Skeleton.H5_ASTROCYTE_COORDINATES_DIRECTORY,
                       nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_TRIANGLES_DATA_DIRECTORY,
                       nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_TRIANGLES_INDEX_DIRECTORY,
                       nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_VERTEX_DATA_DIRECTORY,
                       nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_VERTEX_INDEX_DIRECTORY]

        # Verify for each directory
        for directory in directories:
            try:
                d = data[directory]
            except KeyError:
                return False

        # All checks OK.
        return True

    ################################################################################################
    # @read_astrocyte_centroid
    ################################################################################################
    def read_astrocyte_centroid(self):
        """Reads the astrocyte centroid and store it in a mathutils.Vector.
        """

        # Load the h5py module
        h5py = load_h5py()

        # Read the h5 file using the python module into a data array
        data = h5py.File(self.morphology_file, 'r')

        # Get a reference to the coordinates of the soma coordinates
        center = data[nmv.consts.Skeleton.H5_ASTROCYTE_COORDINATES_DIRECTORY]

        # Construct a Vector object of the loaded centroid from the morphology
        self.original_centroid = Vector((center[0][0], center[0][1], center[0][2]))

    ################################################################################################
    # @read_processes
    ################################################################################################
    def read_processes(self):
        """Reads the processes, or arbors and stores them in the
        @self.points_list and @self.structure_list structures.

        :return:
            True if you can read the processes, and None otherwise.
        """

        # Load the h5py module
        h5py = load_h5py()

        # Load the data
        data = h5py.File(self.morphology_file, 'r')

        # Read the point list from the points directory
        try:
            points_list = data[nmv.consts.Skeleton.H5_POINTS_DIRECTORY]
            self.points_list = [Vector((p[0], p[1], p[2], p[3])) for p in points_list]
        except KeyError:
            nmv.logger.log('ERROR: Cannot load the points from [%s]' % self.morphology_file)
            return None

        # Get the structure list from the structures directory
        try:
            self.structure_list = data[nmv.consts.Skeleton.H5_STRUCTURE_DIRECTORY]
        except KeyError:
            nmv.logger.log('ERROR: Cannot load the structure from [%s]' % self.morphology_file)
            return None

        # The file has been read successfully
        return True

    ################################################################################################
    # @read_astrocyte_endfeet
    ################################################################################################
    def read_astrocyte_endfeet(self):
        """Reads the astrocyte endfeet data, and stores the results in @self.endfeet_points.
        """

        # Load the h5py module
        h5py = load_h5py()

        # Load the data
        data = h5py.File(self.morphology_file, 'r')

        # Get a reference to the indices of the triangles
        triangle_indices = data[nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_TRIANGLES_INDEX_DIRECTORY]

        # Get a reference to the data of the triangles
        triangle_data = data[nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_TRIANGLES_DATA_DIRECTORY]

        # Get a reference to the indices of the vertices
        vertex_indices = data[nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_VERTEX_INDEX_DIRECTORY]

        # Get a reference to the data of the vertices
        vertex_data = data[nmv.consts.Skeleton.H5_ASTROCYTE_ENDFEET_VERTEX_DATA_DIRECTORY]

        # Count the number of endfeet, from the indices of either the vertices or the triangles
        number_endfeet = len(triangle_indices)

        # For all the vertices, create a Blender-compatible array
        endfeet_points = list()

        for i in range(number_endfeet):

            vertex_start_index = vertex_indices[i][0]
            vertex_last_index = vertex_indices[i][1]

            # Vertices
            endfoot_points = [
                Vector((vertex_data[j][0], vertex_data[j][1], vertex_data[j][2], vertex_data[j][3]))
                for j in range(vertex_start_index, vertex_last_index + 1)]
            endfeet_points.append(endfoot_points)

        # For every endfoot, collect the triangles and points in endfeet
        for i in range(number_endfeet):

            if i == 0:
                vertex_index_shift = 0
            else:
                vertex_index_shift = int(vertex_indices[i][0])

            # Triangles indices
            triangle_start_index = triangle_indices[i][0]
            triangle_last_index = triangle_indices[i][1]

            # Triangles
            endfoot_triangles = [Vector((int(triangle_data[j][0] - vertex_index_shift),
                                         int(triangle_data[j][1] - vertex_index_shift),
                                         int(triangle_data[j][2] - vertex_index_shift)))
                                 for j in range(triangle_start_index, triangle_last_index + 1)]

            # Create the endfeet
            self.endfeet_list.append(nmv.skeleton.Endfoot(
                name='Endfoot %s' % str(i + 1), points=endfeet_points[i],
                triangles=endfoot_triangles))

    ################################################################################################
    # @read_profile_points
    ################################################################################################
    def read_profile_points(self):
        """Reads a list of the profile points of the soma to the @self.profile_points list.

        NOTE: The h5v1 files by default have somata profile points that can be helpful for building
        accurate 3D somatic profiles using the 2D projection.
        """

        # Get the index of the starting point of the soma section
        first_profile_point_index = self.structure_list[0][0]

        # Get the index of the last point of the soma section
        last_profile_point_index = self.structure_list[1][0]

        # Consider every profile point
        for i in range(first_profile_point_index, last_profile_point_index):

            # Construct the profile point
            x = self.points_list[i][nmv.consts.Skeleton.H5_SAMPLE_X_COORDINATES_IDX]
            y = self.points_list[i][nmv.consts.Skeleton.H5_SAMPLE_Y_COORDINATES_IDX]
            z = self.points_list[i][nmv.consts.Skeleton.H5_SAMPLE_Z_COORDINATES_IDX]
            profile_point = Vector((x, y, z))

            # Add the profile point to the list
            self.profile_points.append(profile_point)

    ################################################################################################
    # @build_soma
    ################################################################################################
    def build_soma(self,
                   axon_tree=None,
                   basal_dendrites_trees=None,
                   apical_dendrite_tree=None):
        """Builds the soma and returns a reference to it.

        :param axon_tree:
            The reconstructed tree of the axon.
        :param basal_dendrites_trees:
            The reconstructed trees of the basal dendrites.
        :param apical_dendrite_tree:
            The reconstructed tree of the apical dendrite.
        :return:
            A reference to the soma object.
        """

        # Compute the profile points from the arbors
        arbors_profile_points = list()

        # Axon profile point
        if axon_tree is not None:
            arbors_profile_points.extend(
                nmv.file.readers.morphology.get_arbors_profile_points([axon_tree]))

        # Basal dendrites points
        if basal_dendrites_trees is not None:
            arbors_profile_points.extend(
                nmv.file.readers.morphology.get_arbors_profile_points(basal_dendrites_trees))

        # Apical dendrite profile point
        if apical_dendrite_tree is not None:
            arbors_profile_points.extend(
                nmv.file.readers.morphology.get_arbors_profile_points([apical_dendrite_tree]))

        # Compute the mean radius of the soma
        soma_mean_radius = 0
        for point in self.profile_points:
            soma_mean_radius += (point - self.centroid).length
        soma_mean_radius = soma_mean_radius / len(self.profile_points)

        nmv_soma = nmv.skeleton.Soma(
            centroid=self.centroid, mean_radius=soma_mean_radius,
            profile_points=self.profile_points, arbors_profile_points=arbors_profile_points)

        # Return a reference to the soma object
        return nmv_soma

    ################################################################################################
    # @build_sections_from_points_and_structures
    ################################################################################################
    def build_sections_from_points_and_structures(self):
        """Builds a list of sections from the data obtained from the H5 files.

        :return:
            A linear list of sections of the entire morphology.
        """

        # Parse the sections and add them to a linear list [index, parent, type, samples]
        sections_list = list()

        for i_section in range(1, len(self.structure_list)):

            # For all the sections, except the last one, the points go until the next start offset
            # defined by the next row in the structure dataset. For the last one, then it runs until
            # the end of the points' dataset.
            if i_section < len(self.structure_list) - 1:

                # Get the index of the starting point of the section (offset)
                section_first_point_index = self.structure_list[i_section][0]

                # Get the index of the last point of the section
                section_last_point_index = self.structure_list[i_section + 1][0]

            # Last section
            else:

                # Get the index of the starting point of the section (offset)
                section_first_point_index = self.structure_list[i_section][0]

                # Get the index of the last point of the section
                section_last_point_index = len(self.points_list) - 1

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
                x = self.points_list[i_sample][nmv.consts.Skeleton.H5_SAMPLE_X_COORDINATES_IDX]
                y = self.points_list[i_sample][nmv.consts.Skeleton.H5_SAMPLE_Y_COORDINATES_IDX]
                z = self.points_list[i_sample][nmv.consts.Skeleton.H5_SAMPLE_Z_COORDINATES_IDX]
                point = Vector((x, y, z))

                # Radius
                # NOTE: What is reported in our .H5 files is the diameter unlike the .SWC files
                radius = self.points_list[i_sample][nmv.consts.Skeleton.H5_SAMPLE_RADIUS_IDX] * 0.5

                # Build a NeuroMorphoVis sample
                nmv_sample = nmv.skeleton.Sample(point=point, radius=radius, index=sample_index,
                                                 morphology_id=sample_index, type=section_type)

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
    # @build_arbors_from_sections
    ################################################################################################
    def build_arbors_from_sections(self):
        """Builds the arbors from the given sections.

        :return:
            References to the axons, basal and apical dendrites lists respectively.
        """

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
                index=section_id, parent_index=section_parent_id, children_ids=section_children_ids,
                samples=section_samples, type=section_type)

            # Axon
            if section_type == nmv.consts.Skeleton.H5_AXON_SECTION_TYPE:

                # Add the section to the axons list
                axons_sections.append(nmv_section)

            # Basal dendrite
            elif section_type == nmv.consts.Skeleton.H5_BASAL_DENDRITE_SECTION_TYPE:

                # Add the section to the basal dendrites list
                basal_dendrites_sections.append(nmv_section)

            # Apical dendrite
            elif section_type == nmv.consts.Skeleton.H5_APICAL_DENDRITE_SECTION_TYPE:

                # Add the section to the apical dendrites list
                apical_dendrites_sections.append(nmv_section)

            # Undefined section type
            else:

                # Report an error
                nmv.logger.log('ERROR: Unknown section type [%s] !' % str(section_type))

        # Build the axon tree
        nmv.file.readers.morphology.build_tree(axons_sections)

        # Build the basal tree
        nmv.file.readers.morphology.build_tree(basal_dendrites_sections)

        # Build the apical tree
        nmv.file.readers.morphology.build_tree(apical_dendrites_sections)

        # Apical dendrites
        apical_dendrites = nmv.skeleton.ops.build_arbors_from_sections(apical_dendrites_sections)

        # Basal dendrites
        basal_dendrites = nmv.skeleton.ops.build_arbors_from_sections(basal_dendrites_sections)

        # Axons
        axons = nmv.skeleton.ops.build_arbors_from_sections(axons_sections)

        # Labeling and tagging the apical dendrites
        if apical_dendrites is not None:
            if len(apical_dendrites) == 1:
                apical_dendrites[0].label = 'Apical Dendrite'
                apical_dendrites[0].tag = 'ApicalDendrite'
            else:
                for i in range(len(apical_dendrites)):
                    apical_dendrites[i].label = 'Apical Dendrite %d' % (i + 1)
                    apical_dendrites[i].tag = 'ApicalDendrite%d' % (i + 1)

        # Labeling the basal dendrites
        if basal_dendrites is not None:
            if len(basal_dendrites) == 1:
                basal_dendrites[0].label = 'Basal Dendrite'
                basal_dendrites[0].tag = 'BasalDendrite'
            else:
                for i in range(len(basal_dendrites)):
                    basal_dendrites[i].label = 'Basal Dendrite %d' % (i + 1)
                    basal_dendrites[i].tag = 'BasalDendrite%d' % (i + 1)

        # Labeling and tagging the axons
        if axons is not None:
            if len(axons) == 1:
                axons[0].label = 'Axon'
                axons[0].tag = 'Axon'
            else:
                for i in range(len(axons)):
                    axons[i].label = 'Axon %d' % (i + 1)
                    axons[i].tag = 'Axon%d' % (i + 1)

        # Return references to the build arbors
        return axons, basal_dendrites, apical_dendrites

    ################################################################################################
    # @read_file
    ################################################################################################
    def read_file(self):
        """Read a morphology skeleton given in .H5 file into a NeuroMorphoVis morphology structure.

        :return:
            Returns a reference to a NeuroMorphoVis morphology as read from the file.
        """

        # Get the morphology label from the file name, to used for annotation
        label = nmv.file.ops.get_file_name_from_path(self.morphology_file)

        # Check if the morphology is an astrocyte
        is_astrocyte = False
        if self.is_astrocyte_morphology_with_endfeet():
            nmv.logger.info('Reading an astrocyte with H5 structure!')
            is_astrocyte = True

            # Read the actual centroid of the astrocyte
            self.read_astrocyte_centroid()

            # Read the processes of the astrocyte
            self.read_processes()

            # Read the endfeet of the astrocyte
            self.read_astrocyte_endfeet()

            # Collects all the profile points to accurately reconstruct the soma
            self.read_profile_points()

        else:
            nmv.logger.info('Reading a neuron with H5v1 structure!')

            # Read the processes
            self.read_processes()

            # Compute the centroid of the soma
            self.read_profile_points()

        # Build the arbors from the sections
        axons, basal_dendrites, apical_dendrites = self.build_arbors_from_sections()

        # Build the soma
        soma = self.build_soma()

        # Construct the morphology skeleton in NMV format
        nmv_morphology = nmv.skeleton.Morphology(soma=soma,
                                                 axons=axons,
                                                 basal_dendrites=basal_dendrites,
                                                 apical_dendrites=apical_dendrites,
                                                 label=label)

        # Update the centroid
        nmv_morphology.original_center = self.original_centroid

        # In case it is an astrocyte morphology, update the endfeet list
        nmv_morphology.endfeet = self.endfeet_list

        # Update the astrocyte flag
        nmv_morphology.is_astrocyte = is_astrocyte

        # Return a reference to the reconstructed morphology skeleton
        return nmv_morphology
