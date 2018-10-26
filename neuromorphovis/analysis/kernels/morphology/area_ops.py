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
import neuromorphovis as nmv
import neuromorphovis.analysis


####################################################################################################
# @kernel_total_surface_area
####################################################################################################
def kernel_total_surface_area(morphology):
    """Analyse the total surface area of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Apply the analysis operation to the morphology
    analysis_result = nmv.analysis.apply_analysis_operation_to_morphology(
        *[morphology,
          nmv.analysis.compute_arbor_total_surface_area])

    # Update the morphology result from the arbors
    nmv.analysis.compute_total_analysis_result_of_morphology(analysis_result)

    # Return the analysis result of the entire morphology
    return analysis_result


####################################################################################################
# @kernel_minimum_section_surface_area
####################################################################################################
def kernel_minimum_section_surface_area(morphology):
    """Find the minimum section surface area of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Apply the analysis operation to the morphology
    analysis_result = nmv.analysis.apply_analysis_operation_to_morphology(
        *[morphology,
          nmv.analysis.compute_minimum_section_surface_area])

    # Update the morphology result from the arbors
    nmv.analysis.compute_minimum_analysis_result_of_morphology(analysis_result)

    # Return the analysis result of the entire morphology
    return analysis_result


####################################################################################################
# @kernel_maximum_section_surface_area
####################################################################################################
def kernel_maximum_section_surface_area(morphology):
    """Find the maximum section surface area of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Apply the analysis operation to the morphology
    analysis_result = nmv.analysis.apply_analysis_operation_to_morphology(
        *[morphology,
          nmv.analysis.compute_maximum_section_surface_area])

    # Update the morphology result from the arbors
    nmv.analysis.compute_maximum_analysis_result_of_morphology(analysis_result)

    # Return the analysis result of the entire morphology
    return analysis_result


####################################################################################################
# @kernel_average_section_surface_area
####################################################################################################
def kernel_average_section_surface_area(morphology):
    """Find the average section surface area of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Apply the analysis operation to the morphology
    analysis_result = nmv.analysis.apply_analysis_operation_to_morphology(
        *[morphology,
          nmv.analysis.compute_average_section_surface_area])

    # Update the morphology result from the arbors
    nmv.analysis.compute_average_analysis_result_of_morphology(analysis_result)

    # Return the analysis result of the entire morphology
    return analysis_result