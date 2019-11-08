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
# @kernel_maximum_branching_order
####################################################################################################
def kernel_maximum_branching_order(morphology):
    """Computes the maximum branching order of the morphology per arbor.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_branching_order_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)
