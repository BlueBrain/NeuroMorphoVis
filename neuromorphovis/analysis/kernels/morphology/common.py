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


####################################################################################################
# @compute_total_analysis_result_of_morphology
####################################################################################################
def compute_total_analysis_result_of_morphology(analysis_result):
    """Computes the total result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # Aggregate result of the entire morphology will be computed later
    analysis_result.morphology_result = 0

    # Apical dendrite
    if analysis_result.apical_dendrite_result is not None:
        analysis_result.morphology_result += analysis_result.apical_dendrite_result

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            analysis_result.morphology_result += basal_dendrite_result

    # Axon
    if analysis_result.axon_result is not None:
        analysis_result.morphology_result += analysis_result.axon_result

####################################################################################################
# @compute_minimum_analysis_result_of_morphology
####################################################################################################
def compute_minimum_analysis_result_of_morphology(analysis_result):
    """Computes the minimum result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrite_result is not None:
        all_arbors_results.append(analysis_result.apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axon_result is not None:
        all_arbors_results.append(analysis_result.axon_result)

    # Update the morphology result
    analysis_result.morphology_result = min(all_arbors_results)


####################################################################################################
# @compute_maximum_analysis_result_of_morphology
####################################################################################################
def compute_maximum_analysis_result_of_morphology(analysis_result):
    """Computes the maximum result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrite_result is not None:
        all_arbors_results.append(analysis_result.apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axon_result is not None:
        all_arbors_results.append(analysis_result.axon_result)

    # Update the morphology result
    analysis_result.morphology_result = max(all_arbors_results)


####################################################################################################
# @compute_average_analysis_result_of_morphology
####################################################################################################
def compute_average_analysis_result_of_morphology(analysis_result):
    """Computes the average result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrite_result is not None:
        all_arbors_results.append(analysis_result.apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axon_result is not None:
        all_arbors_results.append(analysis_result.axon_result)

    # Update the morphology result
    analysis_result.morphology_result = 0
    for result in all_arbors_results:
        analysis_result.morphology_result += result
    analysis_result.morphology_result /= len(all_arbors_results)