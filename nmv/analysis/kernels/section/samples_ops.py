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

# System imports
import copy

# Internal imports
import nmv


####################################################################################################
# @compute_number_of_samples_per_section_distributions
####################################################################################################
def compute_number_of_samples_per_section_distributions(section,
                                                        analysis_data):
    """Computes the number of samples of a given section and its branching order.
    The analysis result will be appended as a list of only pair of items, where the first item is
    the branching order and the second one is the number of samples. This list will be appended
    to the given analysis data list.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    analysis_data.append([section.branching_order, len(section.samples)])


####################################################################################################
# @compute_number_of_samples_per_section
####################################################################################################
def compute_number_of_samples_per_section(section,
                                          analysis_data):
    """Computes the number of samples of a given section.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    analysis_data.append(len(section.samples))


####################################################################################################
# @compute_number_of_segments_per_section
####################################################################################################
def compute_number_of_segments_per_section(section,
                                           analysis_data):
    """Computes the number of segments of a given section.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    analysis_data.append(len(section.samples) - 1)


####################################################################################################
# @compute_number_of_segments_per_section
####################################################################################################
def compute_number_of_zero_radius_samples_per_section(section,
                                                      analysis_data):
    """Computes the number of zero radius samples of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # Number of zero radii samples
    number_zero_radii_samples = 0

    for i_sample in section.samples:
        if i_sample.radius < 0.000001:
            number_zero_radii_samples += 1

    analysis_data.append(number_zero_radii_samples)


####################################################################################################
# @compute_minimum_sample_radius_per_section
####################################################################################################
def compute_minimum_sample_radius_per_section(section,
                                              analysis_data):
    """Computes the minimum sample radius of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # A list of radii of all the samples of a given section
    radii = list()

    for i_sample in section.samples:
        radii.append(i_sample.radius)

    analysis_data.append(min(radii))


####################################################################################################
# @compute_maximum_sample_radius_per_section
####################################################################################################
def compute_maximum_sample_radius_per_section(section,
                                              analysis_data):
    """Computes the maximum sample radius of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # A list of radii of all the samples of a given section
    radii = list()

    for i_sample in section.samples:
        radii.append(i_sample.radius)

    analysis_data.append(max(radii))


####################################################################################################
# @compute_average_sample_radius_per_section
####################################################################################################
def compute_average_sample_radius_per_section(section,
                                              analysis_data):
    """Computes the average sample radius of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # A list of radii of all the samples of a given section
    radii = list()

    for i_sample in section.samples:
        radii.append(i_sample.radius)

    analysis_data.append(1.0 * sum(radii) / len(radii))


####################################################################################################
# @get_samples_radii_of_section
####################################################################################################
def get_samples_radii_of_section(section,
                                 analysis_data):
    """Gets a list (results will be appended to the @analysis_data list) of the radii of all the
    samples of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    for i_sample in section.samples:
        analysis_data.append(i_sample.radius)


####################################################################################################
# @get_number_of_samples_per_section_of_section
####################################################################################################
def get_number_of_samples_per_section_of_section(section,
                                                 analysis_data):
    """Gets a list (results will be appended to the @analysis_data list) of the number of samples
    per section of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    analysis_data.append(len(section.samples))


####################################################################################################
# @get_samples_radii_and_distance_to_soma_of_section
####################################################################################################
def get_samples_radii_and_distance_to_soma_of_section(section,
                                                      analysis_data):
    """Gets a list (results will be appended to the @analysis_data list) of the radii of all the
    samples of a given section and their distance to the soma.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    for i_sample in section.samples:
        analysis_data.append([i_sample.radius, i_sample.point.length])


####################################################################################################
# @count_section
####################################################################################################
def count_section(section,
                  analysis_data):
    """Counts this section and adds 1 to the analysis data to account for its count in the final
    results.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    analysis_data.append(1)


####################################################################################################
# @count_bifurcations
####################################################################################################
def count_bifurcations(section,
                       analysis_data):
    """Checks if the section has bifurcations at its end or not. If yes, it adds one to the
    analysis data, otherwise None.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    if len(section.children) == 2:
        analysis_data.append(1)


####################################################################################################
# @count_trifurcations
####################################################################################################
def count_trifurcations(section,
                        analysis_data):
    """Checks if the section has trifurcations at its end or not. If yes, it adds one to the
    analysis data, otherwise None.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    if len(section.children) == 3:
        analysis_data.append(1)


####################################################################################################
# @count_trifurcations
####################################################################################################
def compute_terminal_tips(section,
                          analysis_data):
    """Checks if the section is a leaf or not. If yes, adds one to the result to account for a
    terminal tip.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    if section.is_leaf():
        analysis_data.append(1)


####################################################################################################
# @get_maximum_branching_order
####################################################################################################
def get_maximum_branching_order(section,
                                analysis_data):
    """Gets the maximum branching order of the arbor.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    if not section.has_children():
        analysis_data.append(copy.deepcopy(section.branching_order))


####################################################################################################
# @get_maximum_path_distance
####################################################################################################
def get_maximum_path_distance(section,
                              analysis_data,
                              maximum_branching_order,
                              path_distance):
    """Gets the maximum branching order of the arbor.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # Get a reference to the current distance

    # Compute the section length
    section_length = nmv.analysis.compute_section_length(section=section)

    path_distance[0] += section_length

    if not section.has_children():
        analysis_data.append(copy.deepcopy(path_distance[0]))
        path_distance[0] -= section_length

