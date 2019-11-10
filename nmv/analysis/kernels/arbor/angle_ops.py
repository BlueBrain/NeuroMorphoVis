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
# @compute_minimum_local_bifurcation_angle_of_arbor
####################################################################################################
def compute_minimum_local_bifurcation_angle_of_arbor(arbor):
    """Computes the minimum local bifurcation angle of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The minimum local bifurcation angle of the arbor in degrees.
    """

    # A list that will contain the bifurcation angles of all the sections along the arbor
    sections_bifurcation_angles = list()

    # Compute the angles of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_local_bifurcation_angles,
          sections_bifurcation_angles])

    # Return the minimum local bifurcation angle
    return min(sections_bifurcation_angles)


####################################################################################################
# @compute_maximum_local_bifurcation_angle_of_arbor
####################################################################################################
def compute_maximum_local_bifurcation_angle_of_arbor(arbor):
    """Computes the maximum local bifurcation angle of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The maximum local bifurcation angle of the arbor in degrees.
    """

    # A list that will contain the bifurcation angles of all the sections along the arbor
    sections_bifurcation_angles = list()

    # Compute the angles of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_local_bifurcation_angles,
          sections_bifurcation_angles])

    # Return the minimum local bifurcation angle
    return max(sections_bifurcation_angles)


####################################################################################################
# @compute_average_local_bifurcation_angle_of_arbor
####################################################################################################
def compute_average_local_bifurcation_angle_of_arbor(arbor):
    """Computes the average local bifurcation angle of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The average local bifurcation angle of the arbor in degrees.
    """

    # A list that will contain the bifurcation angles of all the sections along the arbor
    sections_bifurcation_angles = list()

    # Compute the angles of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_local_bifurcation_angles,
          sections_bifurcation_angles])

    # Total arbor local bifurcation angle
    arbor_total_bifurcation_angle = 0.0

    # Iterate and sum up all the sections surface areas
    for angle in sections_bifurcation_angles:

        # Add to the arbor local bifurcation angle
        arbor_total_bifurcation_angle += angle

    # Return the total section surface area
    return arbor_total_bifurcation_angle / len(sections_bifurcation_angles)


####################################################################################################
# @compute_minimum_global_bifurcation_angle_of_arbor
####################################################################################################
def compute_minimum_global_bifurcation_angle_of_arbor(arbor):
    """Computes the minimum global bifurcation angle of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The minimum global bifurcation angle of the arbor in degrees.
    """

    # A list that will contain the bifurcation angles of all the sections along the arbor
    sections_bifurcation_angles = list()

    # Compute the angles of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_global_bifurcation_angles,
          sections_bifurcation_angles])

    # Return the minimum local bifurcation angle
    return min(sections_bifurcation_angles)


####################################################################################################
# @compute_maximum_global_bifurcation_angle_of_arbor
####################################################################################################
def compute_maximum_global_bifurcation_angle_of_arbor(arbor):
    """Computes the maximum global bifurcation angle of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The maximum local bifurcation angle of the arbor in degrees.
    """

    # A list that will contain the bifurcation angles of all the sections along the arbor
    sections_bifurcation_angles = list()

    # Compute the angles of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_global_bifurcation_angles,
          sections_bifurcation_angles])

    # Return the minimum local bifurcation angle
    return max(sections_bifurcation_angles)


####################################################################################################
# @compute_average_global_bifurcation_angle_of_arbor
####################################################################################################
def compute_average_global_bifurcation_angle_of_arbor(arbor):
    """Computes the average global bifurcation angle of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The average global bifurcation angle of the arbor in degrees.
    """

    # A list that will contain the bifurcation angles of all the sections along the arbor
    sections_bifurcation_angles = list()

    # Compute the angles of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_global_bifurcation_angles,
          sections_bifurcation_angles])

    # Total arbor local bifurcation angle
    arbor_total_bifurcation_angle = 0.0

    # Iterate and sum up all the sections surface areas
    for angle in sections_bifurcation_angles:

        # Add to the arbor local bifurcation angle
        arbor_total_bifurcation_angle += angle

    # Return the total section surface area
    return arbor_total_bifurcation_angle / len(sections_bifurcation_angles)