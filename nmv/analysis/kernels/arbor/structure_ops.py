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

import nmv
import nmv.analysis
import nmv.skeleton


####################################################################################################
# @compute_total_number_of_sections_of_arbor
####################################################################################################
def compute_total_number_of_sections_of_arbor(arbor):
    """Computes the total number of sections along the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Total number of sections of the arbor.
    """

    # A list that will be used to count the sections in the arbor
    sections = list()

    # Compute the number of segments of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.count_section,
          sections])

    # Total number of samples
    total_number_sections = 0

    # Iterate and sum up
    for i in sections:

        # Add to the total number of samples
        total_number_sections += i

    # Return the total number of samples of the given arbor
    return total_number_sections


####################################################################################################
# @compute_total_number_of_bifurcations_of_arbor
####################################################################################################
def compute_total_number_of_bifurcations_of_arbor(arbor):
    """Computes the total number of bifurcations along the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Total number of bifurcations of the arbor.
    """

    # A list that will contain the number of bifurcations per section
    bifurcations = list()

    # Apply the operation per section
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.count_bifurcations,
          bifurcations])

    # Total number of samples
    total_bifurcations = 0

    # Iterate and sum up
    for bifurcation in bifurcations:

        # Add to the total number of samples
        total_bifurcations += bifurcation

    # Return the total number of samples of the given arbor
    return total_bifurcations


####################################################################################################
# @compute_total_number_of_trifurcations_of_arbor
####################################################################################################
def compute_total_number_of_trifurcations_of_arbor(arbor):
    """Computes the total number of trifurcations along the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        Total number of trifurcations of the arbor.
    """

    # A list that will contain the number of trifurcations per section
    trifurcations = list()

    # Apply the operation per section
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.count_trifurcations,
          trifurcations])

    # Total number of trifurcations
    total_trifurcations = 0

    # Iterate and sum up
    for trifurcation in trifurcations:

        # Add to the total number of samples
        total_trifurcations += trifurcation

    # Return the total number of samples of the given arbor
    return total_trifurcations


####################################################################################################
# @compute_maximum_branching_order_of_arbor
####################################################################################################
def compute_maximum_branching_order_of_arbor(arbor):
    """Computes the maximum branching order of a given arbor.

    :param arbor:
        A given arbor to analyze.
    :return
        The maximum branching order of the given arbor.
    """

    # A list that will contain a count of each
    branching_orders = list()

    # Apply the operation per section
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.get_maximum_branching_order,
          branching_orders])

    # Return the maximum branching order of the arbor
    return max(branching_orders)
