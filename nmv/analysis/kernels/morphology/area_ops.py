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
# @kernel_total_surface_area
####################################################################################################
def kernel_total_surface_area(morphology):
    """Analyse the total surface area of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_arbor_total_surface_area,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


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

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_minimum_section_surface_area,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


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

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_section_surface_area,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


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

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_average_section_surface_area,
                                      nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_branching_order
####################################################################################################
def kernel_total_arbor_surface_area_distribution(morphology,
                                                 options):

    # Apply the kernel
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_arbor_total_surface_area,
        nmv.analysis.compute_total_analysis_result_of_morphology)

    # Plot the distribution
    nmv.analysis.plot_per_arbor_distribution(analysis_results=analysis_results,
                                             morphology=morphology,
                                             options=options,
                                             figure_name='surface-area',
                                             x_label='Area (\u03BCm\u00b2)',
                                             title='Neurites Surface Area',
                                             add_percentage=True)


####################################################################################################
# @kernel_segment_surface_area_range_distribution
####################################################################################################
def kernel_segment_surface_area_range_distribution(morphology,
                                                   options,
                                                   figure_title,
                                                   figure_axis_label,
                                                   figure_label):
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
        nmv.analysis.compute_minimum_segment_surface_area,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Average
    average_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_segment_surface_area,
        nmv.analysis.compute_average_analysis_result_of_morphology)

    # Maximum
    maximum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_segment_surface_area,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Plot
    nmv.analysis.plot_min_avg_max_per_arbor_distribution(
        minimum_results=minimum_results,
        maximum_results=maximum_results,
        average_results=average_results,
        morphology=morphology,
        options=options,
        figure_name=figure_label,
        x_label=figure_axis_label,
        title=figure_title)


####################################################################################################
# @kernel_segments_length_range_distribution
####################################################################################################
def kernel_sections_surface_area_range_distribution(morphology,
                                                    options,
                                                    figure_title,
                                                    figure_axis_label,
                                                    figure_label):
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
        nmv.analysis.compute_minimum_section_surface_area,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Average
    average_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_section_surface_area,
        nmv.analysis.compute_average_analysis_result_of_morphology)

    # Maximum
    maximum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_section_surface_area,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Plot
    nmv.analysis.plot_min_avg_max_per_arbor_distribution(
        minimum_results=minimum_results,
        maximum_results=maximum_results,
        average_results=average_results,
        morphology=morphology,
        options=options,
        figure_name=figure_label,
        x_label=figure_axis_label,
        title=figure_title)
