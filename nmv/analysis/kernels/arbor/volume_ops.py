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

# Internal imports
import nmv
import nmv.analysis
import nmv.skeleton


####################################################################################################
# @compute_arbor_total_volume
####################################################################################################
def compute_arbor_total_volume(arbor):
    """Computes the total volume of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The total volume of the arbor in um cube.
    """

    # A list that will contain the volumes of all the sections along the arbor
    sections_volumes = list()

    # Compute the volumes of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_volumes_from_segments,
          sections_volumes])

    # Total arbor length
    arbor_total_volume = 0.0

    # Iterate and sum up all the sections volumes
    for volume in sections_volumes:

        # Add to the arbor volume
        arbor_total_volume += volume

    # Return the total section volume
    return arbor_total_volume


####################################################################################################
# @compute_minimum_section_volume
####################################################################################################
def compute_minimum_section_volume(arbor):
    """Computes the minimum section volume of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The minimum section volume of the arbor in um cube.
    """

    # A list that will contain the volumes of all the sections along the arbor
    sections_volumes = list()

    # Compute the volumes of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_volumes_from_segments,
          sections_volumes])

    # Return the minimum section volume
    if len(sections_volumes) > 0:
        return min(sections_volumes)
    else:
        return 0.0


####################################################################################################
# @compute_maximum_section_volume
####################################################################################################
def compute_maximum_section_volume(arbor):
    """Computes the maximum section volume of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The maximum section volume of the arbor in um cube.
    """

    # A list that will contain the volumes of all the sections along the arbor
    sections_volumes = list()

    # Compute the volumes of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_volumes_from_segments,
          sections_volumes])

    # Return the minimum section volume
    if len(sections_volumes) > 0:
        return max(sections_volumes)
    else:
        return 0.0


####################################################################################################
# @compute_arbor_total_volume
####################################################################################################
def compute_average_section_volume(arbor):
    """Computes the average section volume of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The average section volume of the arbor in um cube.
    """

    # A list that will contain the volumes of all the sections along the arbor
    sections_volumes = list()

    # Compute the volumes of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_volumes_from_segments,
          sections_volumes])

    # Total arbor length
    arbor_total_volume = 0.0

    # At least a single item
    if len(sections_volumes) == 0:
        return  0.0

    # Remove zeros in the list if any
    if 0 in sections_volumes:
        sections_volumes.remove(0)

    # Iterate and sum up all the sections volumes
    for volume in sections_volumes:

        # Add to the arbor volume
        arbor_total_volume += volume

    # Return the total section volume
    return arbor_total_volume / len(sections_volumes)


####################################################################################################
# @compute_minimum_section_volume
####################################################################################################
def compute_minimum_segment_volume(arbor):
    """Computes the minimum section volume of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The minimum section volume of the arbor in um cube.
    """

    # A list that will contain the volumes of all the sections along the arbor
    segments_volumes = list()

    # Compute the volumes of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_segments_volumes_in_section,
          segments_volumes])

    # Return the minimum section volume
    if len(segments_volumes) > 0:
        return min(segments_volumes)
    else:
        return 0.0


####################################################################################################
# @compute_minimum_section_volume
####################################################################################################
def compute_maximum_segment_volume(arbor):
    """Computes the minimum section volume of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The minimum section volume of the arbor in um cube.
    """

    # A list that will contain the volumes of all the sections along the arbor
    segments_volumes = list()

    # Compute the volumes of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_segments_volumes_in_section,
          segments_volumes])

    # Return the minimum section volume
    if len(segments_volumes) > 0:
        return max(segments_volumes)
    else:
        return 0.0


####################################################################################################
# @compute_minimum_section_volume
####################################################################################################
def compute_average_segment_volume(arbor):
    """Computes the minimum section volume of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The minimum section volume of the arbor in um cube.
    """

    # A list that will contain the volumes of all the sections along the arbor
    segments_volumes = list()

    # Compute the volumes of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_segments_volumes_in_section,
          segments_volumes])

    # At least a single element
    if len(segments_volumes) == 0:
        return 0.0

    # Return the minimum section volume
    return sum(segments_volumes) / len(segments_volumes)
