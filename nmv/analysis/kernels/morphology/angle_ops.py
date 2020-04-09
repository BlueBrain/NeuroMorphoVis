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
import nmv
import nmv.analysis


####################################################################################################
# @kernel_minimum_local_bifurcation_angle
####################################################################################################
def kernel_minimum_local_bifurcation_angle(morphology):
    """Compute the minimum local bifurcation angles of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_local_bifurcation_angle_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_maximum_local_bifurcation_angle
####################################################################################################
def kernel_maximum_local_bifurcation_angle(morphology):
    """Compute the maximum local bifurcation angles of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_local_bifurcation_angle_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_local_bifurcation_angle
####################################################################################################
def kernel_average_local_bifurcation_angle(morphology):
    """Compute the average local bifurcation angles of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_local_bifurcation_angle_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_minimum_local_bifurcation_angle
####################################################################################################
def kernel_minimum_global_bifurcation_angle(morphology):
    """Compute the minimum global bifurcation angles of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_global_bifurcation_angle_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_maximum_global_bifurcation_angle
####################################################################################################
def kernel_maximum_global_bifurcation_angle(morphology):
    """Compute the maximum global bifurcation angles of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_global_bifurcation_angle_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_global_bifurcation_angle
####################################################################################################
def kernel_average_global_bifurcation_angle(morphology):
    """Compute the average global bifurcation angles of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_global_bifurcation_angle_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_segments_length_range_distribution
####################################################################################################
def kernel_section_local_bifurcation_angle_range_distribution(morphology,
                                              options):
    """Computes and plots the range of section lengths across the morphology along the different
    arbors.

    :param morphology:
        A given morphology skeleton to analyse.
    :param options:
        System options.
    """

    # Minimum
    minimum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_local_bifurcation_angle_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Average
    average_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_local_bifurcation_angle_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)

    # Maximum
    maximum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_local_bifurcation_angle_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Plot
    nmv.analysis.plot_min_avg_max_per_arbor_distribution(
        minimum_results=minimum_results,
        maximum_results=maximum_results,
        average_results=average_results,
        morphology=morphology,
        options=options,
        figure_name='local-bifurcation-angle',
        x_label='Angle (Degrees)',
        title='Local Bifurcation Angle')

####################################################################################################
# @kernel_segments_length_range_distribution
####################################################################################################
def kernel_section_global_bifurcation_angle_range_distribution(morphology,
                                              options):
    """Computes and plots the range of section lengths across the morphology along the different
    arbors.

    :param morphology:
        A given morphology skeleton to analyse.
    :param options:
        System options.
    """

    # Minimum
    minimum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_global_bifurcation_angle_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Average
    average_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_global_bifurcation_angle_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)

    # Maximum
    maximum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_global_bifurcation_angle_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Plot
    nmv.analysis.plot_min_avg_max_per_arbor_distribution(
        minimum_results=minimum_results,
        maximum_results=maximum_results,
        average_results=average_results,
        morphology=morphology,
        options=options,
        figure_name='global-bifurcation-angle',
        x_label='Angle (Degrees)',
        title='Global Bifurcation Angle')