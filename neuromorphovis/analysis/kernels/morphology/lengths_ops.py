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
# @kernel_total_number_samples
####################################################################################################
def kernel_total_length(morphology):
    """Analyse the total length of aspects the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    # Apply the analysis operation to the morphology
    analysis_result = nmv.analysis.apply_analysis_operation_to_morphology(
        *[morphology,
          nmv.analysis.compute_total_length_of_arbor])

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

    # Return the analysis result of the entire morphology
    return analysis_result