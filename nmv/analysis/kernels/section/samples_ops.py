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

# System imports
import copy
import nmv.analysis


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
# @analyze_number_of_samples_per_section
####################################################################################################
def analyze_number_of_samples_per_section(section,
                                          analysis_data):
    """Computes the number of samples of a given section.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # Analysis data
    data = nmv.analysis.AnalysisData
    data.value = len(section.samples)
    data.branching_order = section.branching_order

    # Add to the collecting list
    analysis_data.append(data)


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
# @analyze_number_of_segments_per_section
####################################################################################################
def analyze_number_of_segments_per_section(section,
                                           analysis_data):
    """Computes the number of segments of a given section.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # Analysis data
    import nmv.analysis
    data = nmv.analysis.AnalysisData
    data.value = len(section.samples) - 1
    data.branching_order = section.branching_order

    # Add to the collecting list
    analysis_data.append(data)


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
# @analyze_number_of_zero_radius_samples_per_section
####################################################################################################
def analyze_number_of_zero_radius_samples_per_section(section,
                                                      analysis_data):
    """Computes the number of zero radius samples of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # Number of zero radii samples
    number_zero_radii_samples = 0

    # Assume that radii less than 1 nm is already a zero-radius sample
    for i_sample in section.samples:
        if i_sample.radius < 1e-3:
            number_zero_radii_samples += 1

    # Analysis data
    data = nmv.analysis.AnalysisData
    data.value = number_zero_radii_samples
    data.branching_order = section.branching_order

    # Add to the collecting list
    analysis_data.append(data)


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
# @analyze_samples_radii_of_section
####################################################################################################
def analyze_samples_radii_of_section(section,
                                     analysis_data):
    """Gets a list (results will be appended to the @analysis_data list) of the radii of all the
    samples of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    for i_sample in section.samples:

        # Analysis data
        data = nmv.analysis.AnalysisData
        data.value = i_sample.radius
        data.branching_order = section.branching_order
        data.radial_distance = i_sample.position.length

        # Add to the collecting list
        analysis_data.append(data)


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
# @compute_terminal_tips
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
# @compute_terminal_segments
####################################################################################################
def compute_terminal_segments(section,
                              analysis_data):
    """Checks if the section is a leaf or not. If yes, adds the number of segments in the section
    to the result to account for a terminal segments.

    :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    if section.is_leaf():
        analysis_data.append(len(section.samples) - 1)


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
# @compute_path_distance
####################################################################################################
def compute_path_distance(section,
                          analysis_data):
    """Computes the path distance of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # Computes the path distance if not computed for the parents
    analysis_data.append(section.compute_path_length())


####################################################################################################
# @compute_maximum_euclidean_distance
####################################################################################################
def compute_maximum_euclidean_distance(section,
                                       analysis_data):
    """Computes the maximum Euclidean distance of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # Get the last sample of the section and compute its radial distance if exists, otherwise ignore
    if len(section.samples) > 1:
        analysis_data.append(section.samples[-1].point.length)


####################################################################################################
# @compute_minimum_euclidean_distance
####################################################################################################
def compute_minimum_euclidean_distance(section,
                                       analysis_data):
    """Computes the minimum Euclidean distance of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # Get the last sample of the section and compute its radial distance if exists, otherwise ignore
    if len(section.samples) > 1:
        analysis_data.append(section.samples[0].point.length)


####################################################################################################
# @compute_section_burke_taper
####################################################################################################
def compute_section_burke_taper(section):
    """Computes the Burke Taper of a given section. This function is measured per section between
    two bifurcation points. It is computed as follows:
        The actual diameter of the first bifurcation sample minus previous bifurcation sample
        diameter divided by the total length of the branch.
    This function is applied only on NON ROOT and NON LEAVES branches, i.e. sections with
    bifurcation points.

    NOTE: Further details are explained in LMeasure: http://cng.gmu.edu:8080/Lm/help/index.htm.

    :param section:
        A given section to compute its Burke taper value.
    :return:
        Section Burke taper value.
    """

    # If root or leaf, return 0.0
    if section.is_root() or section.is_leaf():
        return 0.0

    # Section length
    section_length = nmv.analysis.compute_section_length(section=section)

    # Diameter difference
    delta_diameter = (section.parent.samples[-1].radius - section.samples[-1].radius) * 2.0

    # Burke taper value
    burke_taper_value = delta_diameter / section_length

    # Return the value
    return burke_taper_value


####################################################################################################
# @compute_section_hillman_taper
####################################################################################################
def compute_section_hillman_taper(section):
    """
    Computes the Hillman Taper of a given section. This function is measured per section between
    two bifurcation points. It is computed as follows:
        The actual diameter of the first bifurcation sample minus previous bifurcation sample
        diameter divided by the initial one.
    This function is applied only on NON ROOT and NON LEAVES branches, i.e. sections with
    bifurcation points.

    NOTE: Further details are explained in LMeasure: http://cng.gmu.edu:8080/Lm/help/index.htm.

    :param section:
        A given section to compute its Burke taper value.
    :return:
        Section Burke taper value.
    """

    # If root or leaf, return 0.0
    if section.is_root() or section.is_leaf():
        return 0.0

    # Diameter difference
    delta = (section.parent.samples[-1].radius - section.samples[-1].radius)

    # Hillman taper value
    _hillman_taper_value = delta / section.parent.samples[-1].radius

    # Return the value
    return _hillman_taper_value


####################################################################################################
# @compute_sections_burke_taper
####################################################################################################
def compute_sections_burke_taper(section,
                                 sections_burke_taper):
    """Computes the Burke Taper of all the sections along a given arbor.

    :param section:
        A given section to compute its Burke taper value.
    :param sections_burke_taper:
        A list to collect the resulting data.
    """

    # Compute section length
    section_burke_taper = compute_section_burke_taper(section=section)

    # Append the length to the list
    sections_burke_taper.append(section_burke_taper)


####################################################################################################
# @compute_sections_hillman_taper
####################################################################################################
def compute_sections_hillman_taper(section,
                             sections_hillman_taper):
    """Computes the Hillman Taper of all the sections along a given arbor.

    :param section:
        A given section to compute its Hillman taper value.
    :param sections_hillman_taper:
        A list to collect the resulting data.
    """

    # Compute section length
    section_hillman_taper = compute_section_hillman_taper(section=section)

    # Append the length to the list
    sections_hillman_taper.append(section_hillman_taper)


####################################################################################################
# @compute_section_partition_asymmetry
####################################################################################################
def compute_section_partition_asymmetry(section,
                                        sections_partition_asymmetry):

    # The section must have children
    if section.has_children():

        # Section must have at least two children to consider this a branching point
        # NOTE: This is not handling trifurcations
        if len(section.children) > 1:

            # Children
            child_1 = section.children[0]
            child_2 = section.children[1]

            # Compute the number of tips
            n1 = nmv.analysis.compute_total_number_of_terminal_tips_of_arbor(child_1)
            n2 = nmv.analysis.compute_total_number_of_terminal_tips_of_arbor(child_2)

            # Compute the partition asymmetry
            if not (n1 + n2) == 2:
                partition_asymmetry = abs(n1 - n2) / (n1 + n2 - 2)

                # Return the value
                sections_partition_asymmetry.append(partition_asymmetry)


####################################################################################################
# @compute_daughter_ratio
####################################################################################################
def compute_daughter_ratio(section,
                           analysis_data):
    """Computes the daughter ratio of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # The section must have children
    if section.has_children():

        # The section must have two children
        if len(section.children) > 1:

            # Get references to the children sections
            child_0 = section.children[0]
            child_1 = section.children[1]

            # Compute the ratio, irrespective to which one is bigger
            segment_1_radius = 0.5 * (child_0.samples[0].radius + child_0.samples[1].radius)
            segment_2_radius = 0.5 * (child_1.samples[0].radius + child_1.samples[1].radius)

            daughter_ratio = segment_1_radius / segment_2_radius

            # If the ratio is less than 1.0, simply invert it
            if daughter_ratio < 1.0:
                daughter_ratio = 1.0 / daughter_ratio

            # Append the result to the list
            analysis_data.append(daughter_ratio)


####################################################################################################
# @compute_parent_daughter_ratio
####################################################################################################
def compute_parent_daughter_ratios(section,
                                   analysis_data):
    """Computes the parent-daughter ratios of a given section.

     :param section:
        A given section to get analyzed.
    :param analysis_data:
        A list to collect the analysis data.
    """

    # The section must have children
    if section.has_children():

        # Get the parent last segment radius
        parent_radius = 0.5 * (section.samples[-1].radius + section.samples[-2].radius)

        # Make sure that the section has at least one sample
        if len(section.samples) > 1:

            # For every child
            for child in section.children:

                # The child must have at least one sample as well
                if len(child.samples) > 1:

                    # Get the child first segment radius
                    child_radius = 0.5 * (child.samples[0].radius + child.samples[1].radius)

                    # Compute the ratio, irrespective to which one is bigger
                    parent_daughter_ratio = child_radius / parent_radius

                    # Append the result to the list
                    analysis_data.append(parent_daughter_ratio)


####################################################################################################
# @get_maximum_path_distance
####################################################################################################
def get_samples_radii_data_of_section(section,
                                      analysis_data):
    """

    :param section:
    :param analysis_data:
    :return:
    """

    # For every sample along the section
    for i_sample in section.samples:

        # Analysis data
        data = nmv.analysis.AnalysisData(
            value=i_sample.radius,
            branching_order=section.branching_order,
            radial_distance=i_sample.point.length)

        # Add to the collecting list
        analysis_data.append(data)


def get_number_of_samples_per_section_data_of_section(section,
                                                      analysis_data):
    # Analysis data
    data = nmv.analysis.AnalysisData(
        value=len(section.samples),
        branching_order=section.branching_order)

    # Add to the collecting list
    analysis_data.append(data)
