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
# @kernel_total_length
####################################################################################################
def kernel_total_length(morphology):
    """Analyse the total length aspects the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_length_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_section_length
####################################################################################################
def kernel_minimum_section_length(morphology):
    """Find the minimum section length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_minimum_section_length_of_arbor,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_section_length
####################################################################################################
def kernel_maximum_section_length(morphology):
    """Find the maximum section length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_section_length_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_section_length
####################################################################################################
def kernel_average_section_length(morphology):
    """Find the average section length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_average_section_length_of_arbor,
                                      nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_segment_length
####################################################################################################
def kernel_minimum_segment_length(morphology):
    """Find the minimum segment length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_minimum_segment_length_of_arbor,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_segment_length
####################################################################################################
def kernel_maximum_segment_length(morphology):
    """Find the maximum segment length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_segment_length_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_segment_length
####################################################################################################
def kernel_average_segment_length(morphology):
    """Find the average segment length of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_average_segment_length_of_arbor,
                                      nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_segment_length
####################################################################################################
def kernel_zero_length_segments(morphology):
    """Find the number of zero-length segments of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_number_zero_length_segments_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_segment_length
####################################################################################################
def kernel_short_sections(morphology):
    """Find the number of the short sections of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_number_of_short_sections_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)
