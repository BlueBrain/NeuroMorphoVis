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
def kernel_total_number_samples(morphology):
    """Analyse the total number of samples of the given morphology.

    This analysis accounts for the number of samples of each individual arbor or neurite of the
    morphology and the total number of samples of the entire morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_total_number_samples_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_number_samples_per_section
####################################################################################################
def kernel_minimum_number_samples_per_section(morphology):
    """Analyses the minimum number of samples per section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_minimum_samples_count_of_arbor,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_number_samples_per_section
####################################################################################################
def kernel_maximum_number_samples_per_section(morphology):
    """Analyses the maximum number of samples per section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_samples_count_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_number_samples_per_section
####################################################################################################
def kernel_average_number_samples_per_section(morphology):
    """Analyses the average number of samples per section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_number_samples_per_section_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_number_zero_radius_samples
####################################################################################################
def kernel_number_zero_radius_samples(morphology):
    """Find the number of zero-radii samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_number_of_zero_radius_samples_per_section_of_arbor,
        nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_sample_radius
####################################################################################################
def kernel_minimum_sample_radius(morphology):
    """Find the minimum radius of the samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_sample_radius_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_sample_radius
####################################################################################################
def kernel_maximum_sample_radius(morphology):
    """Find the minimum radius of the samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_sample_radius_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_sample_radius
####################################################################################################
def kernel_average_sample_radius(morphology):
    """Find the average radius of the samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_sample_radius_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)


def kernel_analyse_number_of_samples_per_section(morphology, options=None):

    # Get the analysis results
    analysis_results = nmv.analysis.get_analysis_lists(
        morphology,
        nmv.analysis.get_number_of_samples_per_section_of_arbor)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(analysis_results.axon_result)
    fig.savefig('/bbp/example/plot.pdf')


def kernel_analyse_number_of_samples_per_section_wrt_distance(morphology, options):

    # compute the sample count wrt distance from soma (also we need one for bifurcations)
    pass

def kernel_analyse_number_of_samples_per_section_wrt_branching_order(morphology, options):
    pass


####################################################################################################
# @kernel_analyse_samples_radii
####################################################################################################
def kernel_analyse_samples_radii(morphology,
                                 options=None):

    # Get the analysis results
    analysis_results = nmv.analysis.get_analysis_lists(morphology,
                                                       nmv.analysis.get_samples_radii_of_arbor)

    # Save the results to text files

    # Create figures



def kernel_analyse_samples_radii_distribution_wrt_distance(morphology,
                                                           oprtions=None):

    pass

def kernel_analyse_segments_lengths(morphology,
                                    options=None):
    pass




