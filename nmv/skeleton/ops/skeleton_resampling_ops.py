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

# System imports
import os, copy, math

# Internal import
import nmv.consts
import nmv.geometry
import nmv.skeleton
import nmv.enums


####################################################################################################
# @update_samples_indices_per_arbor
####################################################################################################
def update_samples_indices_per_arbor(section,
                                     index):
    """Updates the global indices (per arbor) of all the samples along the given section.

    Note: This global index of the sample w.r.t to the arbor it belongs to.

    :param section:
        A given section to update the indices of its samples.
    :param index:
        A list that contains a single value that accounts for the index of the arbor.
        Note that we use this list as a trick to update the index value recursively.
    """

    # If the given section is root
    if section.is_root():

        # Update the arbor index of the first sample
        section.samples[0].arbor_idx = index[0]

        # Increment the index value
        index[0] += 1

    else:

        # The index of the root is basically the same as the index of the last sample of the
        # parent arbor
        section.samples[0].arbor_idx = section.parent.samples[-1].arbor_idx

    # Update the indices of the rest of the samples along the section
    for i in range(1, len(section.samples)):

        # Set the arbor index of the current sample
        section.samples[i].arbor_idx = index[0]

        # Increment the index
        index[0] += 1

    # Update the children sections recursively
    for child in section.children:

        # Update the children
        update_samples_indices_per_arbor(child, index)


####################################################################################################
# @update_samples_indices_per_arbor_globally
####################################################################################################
def update_samples_indices_per_arbor_globally(section,
                                              index):
    """Updates the global indices (per morphology) of all the samples along the given section.

    Note: This global index of the sample w.r.t to the arbor it belongs to.

    :param section:
        A given section to update the indices of its samples.
    :param index:
        A list that contains a single value that accounts for the index of the arbor.
        Note that we use this list as a trick to update the index value recursively.
    """

    # If the given section is root
    if section.is_root():

        # Update the arbor index of the first sample
        section.samples[0].morphology_idx = index[0]

        # Increment the index value
        index[0] += 1

    else:

        # The index of the root is basically the same as the index of the last sample of the
        # parent arbor
        section.samples[0].morphology_idx = section.parent.samples[-1].morphology_idx

    # Update the indices of the rest of the samples along the section
    for i in range(1, len(section.samples)):

        # Set the arbor index of the current sample
        section.samples[i].morphology_idx = index[0]

        # Increment the index
        index[0] += 1

    # Update the children sections recursively
    for child in section.children:

        # Update the children
        update_samples_indices_per_arbor_globally(child, index)


####################################################################################################
# @update_samples_indices_per_morphology
####################################################################################################
def update_samples_indices_per_morphology(morphology_object,
                                          starting_index):
    """Updates the indices of the samples (globally on the morphology level).

    NOTE: This will help us easily to write any SWC morphology file without any issues even if
    the morphology skeleton is re-sampled.

    :param morphology_object:
        A morphology object.
    :param starting_index:
        The starting index of the first sample along the arbors. This index is updated based on
        how many samples that belong to the soma.
    """

    # Initially, this index is set to ONE and incremented later (soma index = 0)
    samples_global_morphology_index = [starting_index]

    # Apical dendrites
    if morphology_object.has_apical_dendrites():
        for arbor in morphology_object.apical_dendrites:
            update_samples_indices_per_arbor_globally(arbor, samples_global_morphology_index)

    # Basal dendrites
    if morphology_object.has_basal_dendrites():
        for arbor in morphology_object.basal_dendrites:
            update_samples_indices_per_arbor_globally(arbor, samples_global_morphology_index)

    # Axons
    if morphology_object.has_axons():
        for arbor in morphology_object.axons:
            update_samples_indices_per_arbor_globally(arbor, samples_global_morphology_index)


####################################################################################################
# @resample_section_at_fixed_step
####################################################################################################
def resample_section_at_fixed_step(section,
                                   sampling_step=1.0,
                                   resample_shorter_sections=True):
    """Resamples the section at a given sampling step. If the section has only two sample,
    it will never get resampled. If the section length is smaller than the sampling step, a
    convenient sampling step will be computed and used.

    :param section:
        A given section to resample.
    :param sampling_step:
        User-defined sampling step, by default 1.0 micron.
    :param resample_shorter_sections:
        If this flag is set to True, the short sections will be resampled.
    """

    # If the section has no samples, report this as an error and ignore this filter
    if len(section.samples) == 0:
        nmv.logger.error('Section [%s: %d] has NO samples, cannot be re-sampled' %
                         (section.get_type_string(), section.index))
        return

    # If the section has ONLY one sample, report this as an error and ignore this filter
    elif len(section.samples) == 1:
        nmv.logger.error('Section [%s: %d] has only ONE sample, cannot be re-sampled' %
                         (section.get_type_string(), section.index))
        return

    # If the section length is less than the sampling step, then adaptively resample it
    if nmv.skeleton.compute_section_length(section=section) < sampling_step:
        if resample_shorter_sections:

            # Get a good sampling step that would match this small section
            section_length = nmv.skeleton.compute_section_length(section=section)
            section_number_samples = len(section.samples)
            section_step = section_length / section_number_samples

            # Resample the section at this sampling step
            resample_section_at_fixed_step(section=section, sampling_step=section_step)
        return

    # Sample index
    i = 0

    # Just keep moving along the section till you hit the last section
    while True:

        # Break if we reach the last sample
        if i >= len(section.samples) - 1:
            break

        # Compute the distance between the current sample and the next one
        distance = (section.samples[i + 1].point - section.samples[i].point).length

        # If the distance is less than the resampling step, then remove this sample  at [i + 1]
        if distance < sampling_step:

            if i >= len(section.samples) - 2:
                break

            # Remove the sample
            section.samples.remove(section.samples[i + 1])

            # Proceed to the next sample
            continue

        # If the sample is at a greater step, then add a new sample exactly at the current step
        else:

            # Compute the auxiliary sample radius based on the previous and next samples
            radius = (section.samples[i + 1].radius + section.samples[i].radius) / 2.0

            # Compute the direction
            direction = (section.samples[i + 1].point - section.samples[i].point).normalized()

            # Compute the auxiliary sample point, use epsilon for floating point comparison
            point = section.samples[i].point + (direction * sampling_step)

            # Add the auxiliary sample, the index of the sample is set to -1 (auxiliary sample)
            auxiliary_sample = nmv.skeleton.Sample(
                point=point, radius=radius, index=-1, section=section, type=section.samples[i].type)

            # Update the samples list
            section.samples.insert(i + 1, auxiliary_sample)

            # Move to the nex sample
            i += 1

            # Break if we reach the last sample
            if i >= len(section.samples) - 1:
                break

    # After resampling the section, update the logical indexes of the samples
    section.reorder_samples()


####################################################################################################
# @resample_section_adaptively
####################################################################################################
def resample_section_adaptively(section):
    """Resample the sections adaptively based on the radii of each sample and the distance between
    each two consecutive samples.

    :param section:
        A given section to resample.
    """

    # If the section has in general less than two samples, then there is nothing to be sampled.
    if len(section.samples) < 2:
        return
    else:

        # Sample index
        i = 0

        # Just keep moving along the section till you hit the last section
        while True:

            # Break if we reach the last sample
            if i >= len(section.samples) - 1:
                break

            # Compute the distance between the current sample and the next one
            distance = (section.samples[i + 1].point - section.samples[i].point).length

            # Get the extent of the sample, where no other samples should be located
            extent = section.samples[i].radius

            # If the next sample is located within the extent of this sample, then remove it
            if distance < extent:

                if i >= len(section.samples) - 2:
                    break

                # Remove the sample
                section.samples.remove(section.samples[i + 1])

                # Proceed to the next sample
                continue

            # If the sample is at a greater step, then add a new sample exactly at the current step
            else:

                # Compute the auxiliary sample radius based on the previous and next samples
                radius = (section.samples[i + 1].radius + section.samples[i].radius) / 2.0

                # Compute the direction
                direction = (section.samples[i + 1].point - section.samples[i].point).normalized()

                # Compute the auxiliary sample point, use epsilon for floating point comparison
                point = section.samples[i].point + (direction * section.samples[i].radius)

                # Add the auxiliary sample, the index of the sample is set to -1 (auxiliary sample)
                auxiliary_sample = nmv.skeleton.Sample(
                    point=point, radius=radius, index=-1, section=section,
                    type=section.samples[i].type)

                # Update the samples list
                section.samples.insert(i + 1, auxiliary_sample)

                # Move to the nex sample
                i += 1

                # Break if we reach the last sample
                if i >= len(section.samples) - 1:
                    break

        # After resampling the section, update the logical indexes of the samples
        section.reorder_samples()


####################################################################################################
# @resample_section_adaptively_relaxed
####################################################################################################
def resample_section_adaptively_relaxed(section):
    """Resample the sections adaptively based on the combined sum of the radii of each two
    consecutive samples and the distance between them.

    :param section:
        A given section to resample.
    """

    # If the section has in general less than two samples, then there is nothing to be sampled.
    if len(section.samples) < 2:
        return

    else:

        # Sample index
        i = 0

        # Just keep moving along the section till you hit the last section
        while True:

            # Break if we reach the last sample
            if i >= len(section.samples) - 1:
                break

            # Compute the distance between the current sample and the next one
            distance = (section.samples[i + 1].point - section.samples[i].point).length

            # Get the extent of the sample, where no other samples should be located
            extent = section.samples[i + 1].radius + section.samples[i].radius

            # If the next sample is located within the extent of this sample, then remove it
            if distance < extent:

                if i >= len(section.samples) - 2:
                    break

                # Remove the sample
                section.samples.remove(section.samples[i + 1])

                # Proceed to the next sample
                continue

            # If the sample is at a greater step, then add a new sample exactly at the current step
            else:

                # Compute the auxiliary sample radius based on the previous and next samples
                radius = (section.samples[i + 1].radius + section.samples[i].radius) / 2.0

                # Compute the direction
                direction = (section.samples[i + 1].point - section.samples[i].point).normalized()

                # Compute the auxiliary sample point, use epsilon for floating point comparison
                point = section.samples[i].point + (direction * extent)

                # Add the auxiliary sample, the index of the sample is set to -1 (auxiliary sample)
                auxiliary_sample = nmv.skeleton.Sample(
                    point=point, radius=radius, index=-1, section=section,
                    type=section.samples[i].type)

                # Update the samples list
                section.samples.insert(i + 1, auxiliary_sample)

                # Move to the nex sample
                i += 1

                # Break if we reach the last sample
                if i >= len(section.samples) - 1:
                    break

        # After resampling the section, update the logical indexes of the samples
        section.reorder_samples()


####################################################################################################
# @resample_section_based_on_smallest_segment
####################################################################################################
def resample_section_based_on_smallest_segment(section):
    """Resamples a section based on the smallest segment.

    :param section:
        A given section to resample.
    """

    # Large value
    smallest_segment_length = 1e3

    # Iterate on all the segments
    for i in range(len(section.samples) - 1):

        # Compute its length
        segment_length = (section.samples[i + 1].point - section.samples[i].point).length

        # Validate
        if segment_length < smallest_segment_length:
            smallest_segment_length = segment_length

    # Resample the section
    if smallest_segment_length > 0.5:
        resample_section_at_fixed_step(section=section, sampling_step=smallest_segment_length)
    else:
        resample_section_at_fixed_step(section=section, sampling_step=0.5)


####################################################################################################
# @add_sample_at_section_center
####################################################################################################
def add_sample_at_section_center(section):
    """Adds additional or auxiliary sample at the center of the section between the first and
    last samples to avoid any under-sampling artifacts.
    NOTE: This function is ONLY applied on sections that have two samples.

    :param section:
        A given section with two samples only.
    """

    # Verify that the section has only two samples
    if len(section.samples) == 2:

        # Compute the auxiliary sample position
        sample_position = (section.samples[0].point + section.samples[1].point) / 2.0

        # Compute the auxiliary sample radius
        sample_radius = (section.samples[0].radius + section.samples[1].radius) / 2.0

        # Build the extra samples, and use -1 for the ID to indicate that it is an auxiliary sample
        auxiliary_sample = nmv.skeleton.Sample(
            point=sample_position, radius=sample_radius, index=-1, morphology_id=-1, section=section,
            type=section.samples[0].type)

        # Add the auxiliary sample to the section
        section.samples.insert(1, auxiliary_sample)

        # Reorder the samples and their IDs along the section
        section.reorder_samples()


####################################################################################################
# @remove_duplicate_samples
####################################################################################################
def remove_duplicate_samples(section,
                             threshold=1.0):
    """Remove duplicate samples along a given section.
    If the distance between the samples is less than the threshold, then remove the second sample.

    :param section:
        A given section to remove its duplicates.
    :param threshold:
        A threshold distance, by default 1.0 micron.
    """

    # Iterate over all the samples along the section
    for i, sample in enumerate(list(section.samples)):

        # Ensure that we don't exceed the section length
        if i == len(section.samples) - 2:
            break

        # Compute the distance between the two samples
        distance = (section.samples[i + 1].point - section.samples[i].point).length

        # If the distance is lower than the threshold
        if distance < threshold:

            # Then remove the duplicate sample
            section.samples.remove(section.samples[i + 1])

            # Repeat the process
            remove_duplicate_samples(section=section, threshold=threshold)

            # Due to the recursive call of the function, there are no more samples to process,
            break


####################################################################################################
# @remove_samples_inside_soma
####################################################################################################
def remove_samples_inside_soma(section,
                               soma_center):
    """Remove the samples located inside the soma that result in intersecting the initial section of
    the branch with the soma. This function is ONLY applied to a root section that is connected
    directly to the soma. It compute the distance between the first sample and the origin
    and then, computes the distance between the rest of the samples and the origin. If the
    distance between the origin and any of the samples is SMALLER than that of the first sample,
    then remove the sample from the section.

    NOTE: Make sure that the section has at least two samples to avoid the meshing artifacts.
    NOTE: If the section has initially two samples and has internal sample, then flip the samples.

    :param section:
        A given section to remove its internal samples that are located inside the soma.
    :param soma_center:
        The center of the soma.
    """

    # Cases where the section cannot be resampled
    if section.has_parent() or len(section.samples) < 2:
        return

    # Handle the case when the section has only two samples
    elif len(section.samples) == 2:

        # Make a copy of both samples along the section
        sample_0 = copy.copy(section.samples[0])
        sample_1 = copy.copy(section.samples[1])

        # Compare the distances between the two samples and the origin
        if (sample_1.point - soma_center).length < (sample_0.point - soma_center).length:
            section.samples[0] = sample_1
            section.samples[1] = sample_0

    # The section has more than TWO samples
    else:

        # Compute the minimal distance at which the samples with smaller distances will be filtered
        minimal_distance = (section.samples[0].point - soma_center).length

        # Iterate over the next samples
        for i, sample in enumerate(list(section.samples)):

            # Ignore the first sample
            if i == 0:
                continue

            # Compare the distance between the sample and the origin to the minimal distance
            if (sample.point - soma_center).length < minimal_distance:

                # Remove the sample
                section.samples.remove(sample)

                # Report the repair
                nmv.logger.log('\t\t* REPAIRING: Removing internal sample, section [%s: %d]' %
                      (section.get_type_string(), section.index))

                # After removing this sample, the section might have two samples only, so we
                # recursively call this function and break afterwards.
                remove_samples_inside_soma(section=section, soma_center=soma_center)

                # Break
                break


####################################################################################################
# @remove_samples_within_extent
####################################################################################################
def remove_samples_within_extent(section,
                                 extent_center,
                                 extent_radius,
                                 ignore_first_sample=False):
    """Remove the samples located within a given extent (or sphere) from a section beginning.
    This function verifies whether the samples along the given sphere are located within its extent
    or not. If yes, the samples are removed, otherwise nothing happens.
    NOTE: The function returns the number of samples removed from the section, for verification.

    :param section:
        A sections to remove the samples from.
    :param extent_center:
        The center of the sphere extent.
    :param extent_radius:
        The radius of the sphere extent.
    :param ignore_first_sample:
        If this flag is set, the first sample is not removed.
    :return
        The number of samples removed during the application of this filter.
    """

    # If the section has LESS THAN two samples, the section cannot be resampled.
    if len(section.samples) < 2:
        return

    # Count the number of removed samples from the section
    number_of_removed_samples = 0

    # Do it sample by sample (keep a COPY of the samples list via {list(section.samples)})
    for i, sample in enumerate(list(section.samples)):

        # Keep the first sample if requested
        if i == 0:

            # The @ignore_first_sample flag must be set to True
            if ignore_first_sample:

                # Skip the first sample
                continue

        # Check if the sample is located within the extent of the given sphere
        if nmv.geometry.ops.is_point_inside_sphere(extent_center, extent_radius, sample.point):

            # Remove the sample from the section
            section.samples.remove(sample)

            # Increment the counter of the removed samples
            number_of_removed_samples += 1

    # Return the number of removed samples
    return number_of_removed_samples


####################################################################################################
# @resample_skeleton
####################################################################################################
def resample_skeleton(morphology,
                      morphology_options):
    """Resamples the morphology skeleton based no the input of the user.
    NOTE: This resampling process is performed on a per-section basis, so the first and last samples
    of the section are left intact.

    :param morphology:
        The morphology object.
    :param morphology_options:
        The options of the morphology.
    """

    # The adaptive resampling is quite important to prevent breaking the structure
    if morphology_options.resampling_method == nmv.enums.Skeleton.Resampling.ADAPTIVE_RELAXED:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, resample_section_adaptively_relaxed])
    elif morphology_options.resampling_method == nmv.enums.Skeleton.Resampling.ADAPTIVE_PACKED:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, resample_section_adaptively])
    elif morphology_options.resampling_method == nmv.enums.Skeleton.Resampling.FIXED_STEP:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, resample_section_at_fixed_step, morphology_options.resampling_step])


