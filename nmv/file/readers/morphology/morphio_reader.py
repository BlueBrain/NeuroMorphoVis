####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import nmv.bbox
import nmv.consts
import nmv.file
import nmv.skeleton
import nmv.utilities


####################################################################################################
# @MorphIOLoader
####################################################################################################
class MorphIOLoader:
    """A powerful morphology reader that uses the MorphIO library to load the neuronal morphologies.
    MorphIO is an open source project developed by the Blue Brain Project at EPFL. The code is
    available on GitHub: https://github.com/BlueBrain/MorphIO. Note that we use MorphIO to load
    morphologies in .ASC, .SWC and .H5 formats. The structure is mapped then to the NMV one.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology_file,
                 center_morphology=True):
        """Constructor

        :param morphology_file:
            A given path to the morphology file.
        """

        # Set the path to the given morphology file irrespective to its extension
        self.morphology_file = morphology_file

        # A list of sections that are extracted from the file for processing
        self.sections_list = list()

        # A list of all the points in the morphology file, for bounding box computations
        self.points_list = list()

        # A list of the profile points of the soma, based on the arbors and those reported
        # specifically for the soma
        self.soma_profile_points = list()

        # Final soma centroid, it could be the same as the original if the morphology is centered
        self.soma_centroid = None

        # The average radius of the soma based on the arbors
        self.soma_mean_radius = None

        # If this flag is set, the soma of the neuron must be located at the origin
        self.center_morphology = center_morphology

    ################################################################################################
    # @build_soma
    ################################################################################################
    def build_soma(self,
                   axons_trees=None,
                   basal_dendrites_trees=None,
                   apical_dendrite_tree=None):
        """Builds the soma and returns a reference to it.

        :param axons_trees:
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
        if axons_trees is not None:
            arbors_profile_points.extend(
                nmv.file.readers.morphology.common.get_arbors_profile_points(axons_trees))

        # Basal dendrites points
        if basal_dendrites_trees is not None:
            arbors_profile_points.extend(
                nmv.file.readers.morphology.common.get_arbors_profile_points(basal_dendrites_trees))

        # Apical dendrite profile point
        if apical_dendrite_tree is not None:
            arbors_profile_points.extend(
                nmv.file.readers.morphology.common.get_arbors_profile_points(apical_dendrite_tree))

        # Compute the mean radius of the soma
        # soma_mean_radius = self.soma_mean_radius
        # for point in self.soma_profile_points:
        #     soma_mean_radius += (point - self.soma_centroid).length
        # soma_mean_radius = soma_mean_radius / len(self.soma_profile_points)

        if self.center_morphology:
            soma_centroid = Vector((0, 0, 0))
        else:
            soma_centroid = self.soma_centroid

        nmv_soma = nmv.skeleton.Soma(
            centroid=soma_centroid, mean_radius=self.soma_mean_radius,
            profile_points=self.soma_profile_points, arbors_profile_points=arbors_profile_points)

        # Return a reference to the soma object
        return nmv_soma

    ################################################################################################
    # @read_data_from_file
    ################################################################################################
    def read_data_from_file(self):
        """Loads the data from the given file in the constructor."""

        # Import the required module
        import morphio
        from morphio import Morphology

        # Ignore the console warning and output
        # nmv.utilities.disable_std_output()

        # Load the morphology data using MorphIO
        morphology_data = None
        try:
            morphology_data = Morphology(self.morphology_file)
        except FileNotFoundError:
            nmv.logger.error("Cannot load morphology file! [%s]" % self.morphology_file)
            return morphology_data

        # Soma mean radius from MorphIO
        self.soma_mean_radius = morphology_data.soma.diameters[0] * 0.5
        self.soma_centroid = Vector((morphology_data.soma.center[0],
                                     morphology_data.soma.center[1],
                                     morphology_data.soma.center[2]))

        # Construct the points list in the Vector format
        for s in morphology_data.sections:
            for p in s.points:
                v_point = Vector((p[0], p[1], p[2]))

                if self.center_morphology:
                    v_point -= self.soma_centroid

                self.points_list.append(v_point)

        # A linear list of the sections of the axons
        axons_sections = list()

        # A linear list of basal dendrites sections
        basal_dendrites_sections = list()

        # A linear list of the apical dendrites sections
        apical_dendrites_sections = list()

        nmv_sections = list()

        for s in morphology_data.sections:

            # Get the section ID
            section_id = s.id

            # Get the parent section ID
            if s.is_root:
                section_parent_id = None
            else:
                section_parent_id = s.parent.id

            # Children IDs
            section_children_ids = list()
            if len(s.children) > 0:
                for child in s.children:
                    section_children_ids.append(child.id)

            if s.type == morphio.SectionType.axon:
                section_type = 2

            elif s.type == morphio.SectionType.basal_dendrite:
                section_type = 3

            elif s.type == morphio.SectionType.apical_dendrite:
                section_type = 4

            # Consider all other sections as basal dendrites
            else:
                nmv.logger.warning("This section is not a standard section!")
                section_type = 3

            # Section samples
            section_samples = list()
            for i in range(len(s.points)):

                # Sample point
                sample_point = Vector((s.points[i][0], s.points[i][1], s.points[i][2]))
                if self.center_morphology:
                    sample_point -= self.soma_centroid

                # Sample radius
                sample_radius = s.diameters[i] * 0.5

                # Get the sample type from the section type
                sample_type = section_type

                # Sample ID, simply let it be the operator
                sample_id = i

                # Parent ID, simply let it the current -1
                parent_sample_id = i + 1

                # Construct a nmv sample object
                nmv_sample = nmv.skeleton.Sample(
                    point=sample_point, radius=sample_radius, index=sample_id, morphology_id=0,
                    type=sample_type, parent_index=parent_sample_id)

                section_samples.append(nmv_sample)

            # Construct a skeleton section
            nmv_section = nmv.skeleton.Section(
                index=section_id, parent_index=section_parent_id, children_ids=section_children_ids,
                samples=section_samples, type=section_type)

            # Append the section to the sections list
            self.sections_list.append(nmv_sections)

            # Axon
            if s.type == morphio.SectionType.axon:

                # Add the section to the axons list
                axons_sections.append(nmv_section)

            # Basal dendrite
            elif s.type == morphio.SectionType.basal_dendrite:

                # Add the section to the basal dendrites list
                basal_dendrites_sections.append(nmv_section)

            # Apical dendrite
            elif s.type == morphio.SectionType.apical_dendrite:

                # Add the section to the apical dendrites list
                apical_dendrites_sections.append(nmv_section)

            # Undefined section type
            else:

                # Report an error
                nmv.logger.warning('ERROR: Unknown section type [%s] !' % str(section_type))

                # Add the section to the basal dendrites list
                basal_dendrites_sections.append(nmv_section)

        # Build the axon tree
        nmv.file.readers.morphology.common.build_tree(axons_sections)

        # Build the basal tree
        nmv.file.readers.morphology.common.build_tree(basal_dendrites_sections)

        # Build the apical tree
        nmv.file.readers.morphology.common.build_tree(apical_dendrites_sections)

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

        # Build the soma
        soma = self.build_soma(axons_trees=axons,
                               basal_dendrites_trees=basal_dendrites,
                               apical_dendrite_tree=apical_dendrites)

        # Update the morphology label
        label = nmv.file.ops.get_file_name_from_path(self.morphology_file)

        # Get the morphology file format
        file_format = nmv.file.ops.get_file_format_from_path(self.morphology_file)

        # Construct the morphology skeleton
        nmv_morphology = nmv.skeleton.Morphology(soma=soma,
                                                 axons=axons,
                                                 basal_dendrites=basal_dendrites,
                                                 apical_dendrites=apical_dendrites,
                                                 label=label,
                                                 file_format=file_format)

        # Update the centroid
        nmv_morphology.original_center = Vector((0, 0, 0)) # self.soma_centroid

        # Enable the std_output again
        nmv.utilities.enable_std_output()

        # Return a reference to the reconstructed morphology skeleton
        return nmv_morphology
