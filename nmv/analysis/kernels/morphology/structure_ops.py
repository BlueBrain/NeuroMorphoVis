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
import nmv.analysis


####################################################################################################
# @kernel_total_number_samples
####################################################################################################
def kernel_total_number_sections(morphology):
    """Compute the total number of sections of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_number_of_sections_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_total_number_bifurcations
####################################################################################################
def kernel_total_number_bifurcations(morphology):
    """Compute the total number of bifurcations of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_number_of_bifurcations_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_total_number_trifurcations
####################################################################################################
def kernel_total_number_trifurcations(morphology):
    """Compute the total number of bifurcations of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_number_of_trifurcations_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_total_number_terminal_tips
####################################################################################################
def kernel_total_number_terminal_tips(morphology):
    """Compute the total number of terminal tips of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_number_of_terminal_tips_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_total_number_terminal_segments
####################################################################################################
def kernel_total_number_terminal_segments(morphology):
    """Compute the total number of terminal segments of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_total_number_of_terminal_segments_of_arbor,
        nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_path_distance
####################################################################################################
def kernel_maximum_path_distance(morphology):
    """Computes the maximum path distance from the soma along all the arbors till their last sample.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_path_distance_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_branching_order
####################################################################################################
def kernel_maximum_branching_order(morphology):
    """Computes the maximum branching order of the morphology per arbor.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Apply the kernel
    result = nmv.analysis.invoke_kernel(morphology,
                                        nmv.analysis.compute_maximum_branching_order_of_arbor,
                                        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Axon
    if result.axons_result is not None:
        for i in range(len(result.axons_result)):
            morphology.loaded_axons[i].maximum_branching_order = result.axons_result[i]

    # Apical dendrite
    if result.apical_dendrites_result is not None:
        for i in range(len(result.apical_dendrites_result)):
            morphology.loaded_apical_dendrites[i].maximum_branching_order = \
                result.apical_dendrites_result[i]

    # Basal dendrites
    if result.basal_dendrites_result is not None:
        for i in range(len(result.basal_dendrites_result)):
            morphology.dendrites[i].maximum_branching_order = result.basal_dendrites_result[i]

    # Pass the analysis results to the morphology
    morphology.maximum_branching_order = result

    # Return the final result
    return result
