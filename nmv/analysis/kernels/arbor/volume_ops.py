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
    return min(sections_volumes)


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
    return max(sections_volumes)


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

    # Iterate and sum up all the sections volumes
    for volume in sections_volumes:

        # Add to the arbor volume
        arbor_total_volume += volume

    # Return the total section volume
    return arbor_total_volume / len(sections_volumes)