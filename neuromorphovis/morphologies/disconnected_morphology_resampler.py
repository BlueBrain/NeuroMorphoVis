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

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# System imports
import os, sys, math

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Append the internal modules into the system paths
sys.path.append("%s/../modules" % os.path.dirname(os.path.realpath(__file__)))

# Internal imports
import bounding_box
import line_ops
import mesh_objects
import morphology_analysis_ops
import camera_ops
import sample
import sphere_ops
import morphology_connection_ops
import morphology_repair_ops
import morphology_resampling_ops

####################################################################################################
# @DisconnectedSkeletonResampler
####################################################################################################
class DisconnectedSkeletonResampler():
    """
    Resampling operations for the disconnected skeleton mode.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """
        Constructor
        """
        info = 'Re-sampler for resampling the morphology for disconnected skeleton mode'

    ################################################################################################
    # @resample_primary_section_front
    ################################################################################################
    @staticmethod
    def resample_primary_section_front(section):
        """

        :param section:
        :return:
        """

        # If this section is a root, ignore resampling its front
        if not section.has_parent():
            return

        nmv.logger.log('\t\t* RESAMPLING: Primary section [%s]' % (str(section.id)))

        # The re-sampling distance of the primary section is computed based on the section radius
        resampling_distance = section.samples[0].radius * math.sqrt(2)

        # Remove the samples that are located within the resampling distance
        # The extent center is the first sample point and the extent radius is the
        # resampling distance
        number_removed_sampled = morphology_resampling_ops.remove_samples_within_extent(
            section=section, extent_center= section.samples[0].point,
            extent_radius=resampling_distance, ignore_first_sample=True)

        # Compute the section direction after the removal of the close samples
        section_direction = (section.samples[1].point - section.samples[0].point).normalized()

        # Auxiliary sample position
        sample_position = section.samples[0].point + (section_direction * resampling_distance)

        # The auxiliary sample radius is the same as that of the first sample
        sample_radius = section.samples[0].radius

        # Build the extra samples, and use -1 for the ID to indicate that it is an auxiliary sample
        auxiliary_sample = sample.Sample(
            point=sample_position, radius=sample_radius, id=-1, section=section)

        if number_removed_sampled > 0:
            nmv.logger.log('\t\t* REPAIRING: Removing samples primary section [%s]' % (str(section.id)))

        # Insert the auxiliary sample just
        section.samples.insert(1, auxiliary_sample)

        # Reorder the samples and their IDs along the section
        section.reorder_samples()

    ################################################################################################
    # @resample_secondary_section_front
    ################################################################################################
    @staticmethod
    def resample_secondary_section_front(section):
        """

        :param section:
        :return:
        """

        # Get the parent section
        parent_section = section.parent

        # Get the primary section
        primary_section = None
        for child in parent_section.children:
            if child.is_primary:
                primary_section = child

        # Get the direction of the primary section
        primary_section_vector = \
            (primary_section.samples[1].point - primary_section.samples[0].point).normalized()

        # Get the direction of the secondary section
        secondary_section_vector = (section.samples[1].point - section.samples[0].point).normalized()

        # Get the angle between the primary section and the secondary section
        angle = primary_section_vector.angle(secondary_section_vector) * 180.0 / 3.14

        if angle < 30 or angle > 150:
            nmv.logger.log('section [%s] : angle: %f' % (str(section.id), angle))

            secondary_point = section.samples[1].point
            secondary_point_distance = \
                (section.samples[1].point - section.samples[0].point).length
            primary_point = primary_section.samples[0].point + (secondary_point_distance * primary_section_vector)

            primary_to_secondary_point_direction = (secondary_point - primary_point).normalized()
            section.samples[0].point += primary_to_secondary_point_direction * \
                                        primary_section.samples[0].radius * 2

            section.samples[1].point += \
                primary_to_secondary_point_direction * primary_section.samples[0].radius * 2

        # If the section doesn't have a parent, return
        if not section.has_parent():

            # Return, a secondary branch with no parent does not exist !
            return

        # Get the resampling distance of the secondary section
        resampling_distance = \
            morphology_analysis_ops.get_resampling_distance_of_secondary_section_based_on_angle(
                section)

        # The re-sampling distance of the primary section is computed based on the section radius
        #resampling_distance = section.parent.samples[-1].radius * 2 * math.sqrt(2)

        # Filter all the samples that are located within this sampling distance along the branch
        number_removed_sampled = morphology_resampling_ops.remove_samples_within_extent(
            section=section, extent_center=section.samples[0].point,
            extent_radius=resampling_distance, ignore_first_sample=True)

        if number_removed_sampled > 0:
            nmv.logger.log('\t\t* REPAIRING: Removing samples secondary section [%s]' % (str(section.id)))

        # Compute the section direction after the removal of the close samples
        section_direction = (section.samples[1].point - section.samples[0].point).normalized()

        # Auxiliary sample position
        sample_position = section.samples[0].point + (section_direction * resampling_distance)

        # The auxiliary sample radius is the same as that of the first sample
        sample_radius = section.samples[0].radius

        # Build the extra samples, and use -1 for the ID to indicate that it is an auxiliary sample
        auxiliary_sample = sample.Sample(
            point=sample_position, radius=sample_radius, id=-1, section=section)

        # Insert the auxiliary sample just
        section.samples.insert(1, auxiliary_sample)

        # Reorder the samples and their IDs along the section
        section.reorder_samples()

    ################################################################################################
    # @resample_section_ending
    ################################################################################################
    @staticmethod
    def resample_section_ending(section):
        """

        :param section:
        :return:
        """

        # Reverse the sample list
        section.samples = list(reversed(section.samples))

        # Re-sample it
        DisconnectedSkeletonResampler.resample_primary_section_front(section)

        # Reverse the sample list
        section.samples = list(reversed(section.samples))

    ################################################################################################
    # @resample_primary_section
    ################################################################################################
    @staticmethod
    def resample_primary_section(section):
        """

        :param section:
        :return:
        """

        # Re-sample the front of the primary section
        DisconnectedSkeletonResampler.resample_primary_section_front(section)

        # Re-sample the rear end of the primary section
        DisconnectedSkeletonResampler.resample_section_ending(section)

    ################################################################################################
    # @resample_secondary_section
    ################################################################################################
    @staticmethod
    def resample_secondary_section(section):
        """

        :param section:
        :return:
        """

        # Re-sample the front of the secondary section
        DisconnectedSkeletonResampler.resample_secondary_section_front(section)

        # Re-sample the rear end of the secondary section
        DisconnectedSkeletonResampler.resample_section_ending(section)

    ################################################################################################
    # @resample_section
    ################################################################################################
    @staticmethod
    def resample_section(section):
        """

        :param section:
        :return:
        """

        # Handle a primary section
        if section.is_primary:
            DisconnectedSkeletonResampler.resample_primary_section(section)

        # Handle a secondary section
        #else:
        #    DisconnectedSkeletonResampler.resample_secondary_section(section)

    ################################################################################################
    # @resample_arbor
    ################################################################################################
    @staticmethod
    def resample_arbor(section):
        """

        :param section:
        :return:
        """

        # Resample the root section
        DisconnectedSkeletonResampler.resample_section(section)

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            DisconnectedSkeletonResampler.resample_arbor(child)

    ################################################################################################
    # @resample_morphology_for_disconnected_skeleton
    ################################################################################################
    @staticmethod
    def resample_morphology(morphology):
        """

        :param morphology:
        :return:
        """

        # If the apical dendrite exists, then resample the apical dendrite
        if morphology.apical_dendrite is not None:

            # Resample the apical dendrite
            DisconnectedSkeletonResampler.resample_arbor(morphology.apical_dendrite)

        # If the basal dendrites are valid, then repair their sections
        if morphology.dendrites is not None:

            # Do it dendrite by dendrite
            for dendrite in morphology.dendrites:

                # Resample the basal dendrites
                DisconnectedSkeletonResampler.resample_arbor(dendrite)

        # If the axon is valid, then resample it
        if morphology.axon is not None:

            # Resample the axon
            DisconnectedSkeletonResampler.resample_arbor(morphology.axon)
