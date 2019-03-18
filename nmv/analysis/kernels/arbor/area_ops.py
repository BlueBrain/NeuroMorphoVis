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
# @compute_arbor_total_surface_area
####################################################################################################
def compute_arbor_total_surface_area(arbor):
    """Computes the total surface area of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The total surface area of the arbor in um squared.
    """

    # A list that will contain the surface areas of all the sections along the arbor
    sections_surface_areas = list()

    # Compute the surface area of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_surface_areas_from_segments,
          sections_surface_areas])

    # Total arbor length
    arbor_total_surface_area = 0.0

    # Iterate and sum up all the sections surface areas
    for surface_area in sections_surface_areas:

        # Add to the arbor surface area
        arbor_total_surface_area += surface_area

    # Return the total section surface area
    return arbor_total_surface_area


####################################################################################################
# @compute_minimum_surface_area_per_section
####################################################################################################
def compute_minimum_section_surface_area(arbor):
    """Computes the minimum section surface area per section of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The minimum surface area of the smallest section along the given arbor in um squared.
    """

    # A list that will contain the surface areas of all the sections along the arbor
    sections_surface_areas = list()

    # Compute the surface area of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_surface_areas_from_segments,
          sections_surface_areas])

    # Return the minimum section surface area
    return min(sections_surface_areas)


####################################################################################################
# @compute_maximum_surface_area_per_section
####################################################################################################
def compute_maximum_section_surface_area(arbor):
    """Computes the maximum section surface area of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The maximum surface area of the largest section along the given arbor in um squared.
    """

    # A list that will contain the surface areas of all the sections along the arbor
    sections_surface_areas = list()

    # Compute the surface area of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_surface_areas_from_segments,
          sections_surface_areas])

    # Return the maximum section surface area
    return max(sections_surface_areas)


####################################################################################################
# @compute_average_section_surface_area
####################################################################################################
def compute_average_section_surface_area(arbor):
    """Computes the average surface area per section of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The average surface area per section of the arbor in um squared.
    """

    # A list that will contain the surface areas of all the sections along the arbor
    sections_surface_areas = list()

    # Compute the surface area of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_surface_areas_from_segments,
          sections_surface_areas])

    # Total arbor length
    arbor_total_surface_area = 0.0

    # Iterate and sum up all the sections surface areas
    for surface_area in sections_surface_areas:

        # Add to the arbor surface area
        arbor_total_surface_area += surface_area

    # Return the total section surface area
    return arbor_total_surface_area / len(sections_surface_areas)