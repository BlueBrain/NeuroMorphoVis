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
