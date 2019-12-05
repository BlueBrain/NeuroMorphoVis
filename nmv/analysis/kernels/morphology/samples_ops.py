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
import os

# Internal imports
import nmv
import nmv.consts
import nmv.analysis
import nmv.utilities


def kernel_total_number_samples_at_branching_order(morphology):

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_total_number_samples_of_arbor_distributions,
        nmv.analysis.compute_total_analysis_result_of_morphology_at_branching_order)


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
    analysis_results = nmv.analysis.compile_data(
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
    analysis_results = nmv.analysis.compile_data(morphology,
                                                       nmv.analysis.get_samples_radii_of_arbor)

    # Save the results to text files

    # Create figures



def kernel_analyse_samples_radii_distribution_wrt_distance(morphology,
                                                           oprtions=None):

    pass

def kernel_analyse_segments_lengths(morphology,
                                    options=None):
    pass


####################################################################################################
# @kernel_analyse_samples_radii
####################################################################################################
def kernel_samples_radii_distribution(morphology):

    # Get the analysis results
    analysis_results = nmv.analysis.compile_data(
        morphology,
        nmv.analysis.get_samples_radii_of_arbor)

    # Plot the results
    nmv.analysis.plot_analysis_results(analysis_results)


    # import matplotlib.pyplot as plt

    # fig, ax = plt.subplots()
    #n, bins, patches = ax.hist(analysis_results.axon_result)
    #fig.savefig('%s/neuromorphovis-output/axon-plot.pdf' % os.path.expanduser('~'))

    # print(analysis_results.apical_dendrite_result)
    # n, bins, patches = ax.hist(analysis_results.apical_dendrite_result)
    # fig.savefig('%s/neuromorphovis-output/apical-plot.pdf' % os.path.expanduser('~'))


####################################################################################################
# @kernel_analyse_samples_radii
####################################################################################################
def kernel_number_of_samples_at_branching_order_distributions(morphology):

    analysis_results = nmv.analysis.compile_data(
        morphology,
        nmv.analysis.compute_total_number_samples_of_arbor_distributions)



    nmv.analysis.compute_total_distribution_of_morphology(analysis_results)

    #print(analysis_results.axon_result)

    #print(analysis_results.apical_dendrite_result)

    #for i in analysis_results.basal_dendrites_result:
    #    print(i)

    #print(analysis_results.morphology_result)





def kernel_total_number_of_samples_per_arbor_distribution(morphology, options):

    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_total_number_samples_of_arbor,
        nmv.analysis.compute_total_analysis_result_of_morphology)

    # Plot the distribution
    nmv.analysis.plot_per_arbor_distribution(analysis_results=analysis_results,
                                             morphology=morphology,
                                             options=options,
                                             figure_name='number-of-samples',
                                             x_label='Number of Samples',
                                             title='Number of Samples / Neurite',
                                             add_percentage=True)


def kernel_total_number_of_sections_per_arbor_distribution(morphology,
                                                           options):
    analysis_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_total_number_of_sections_of_arbor,
        nmv.analysis.compute_total_analysis_result_of_morphology)

    # Plot the distribution
    nmv.analysis.plot_per_arbor_distribution(analysis_results=analysis_results,
                                             morphology=morphology,
                                             options=options,
                                             figure_name='number-of-sections',
                                             x_label='Number of Sections',
                                             title='Number of Sections / Neurite',
                                             add_percentage=True)


def kernel_number_samples_per_section(morphology,
                                      options):

    # Analysis results
    analysis_results = nmv.analysis.compile_data(
        morphology,
        nmv.analysis.get_number_of_samples_per_section_data_of_arbor)

    # Aggregate
    nmv.analysis.aggregate_arbors_data_to_morphology(analysis_results)

    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    x_data = list()
    y_data = list()



    colors = (0, 0, 0)

    for result in analysis_results.morphology_result:
        x_data.append(result.branching_order)
        y_data.append(result.value)

    # Create data
    x = np.asarray(x_data)
    y = np.asarray(y_data)

    # Plot
    plt.scatter(x, y, c=colors, alpha=0.5)
    plt.title('Example')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('%s/%s-%s.pdf' % (options.io.analysis_directory,
                                  morphology.label,
                                  'example-1.pdf'),
                bbox_inches='tight')
    plt.close()

    sns.jointplot(x=x, y=y)

    #sns.regplot(x=x, y=y, fit_reg=False)
    plt.savefig('%s/%s-%s.pdf' % (options.io.analysis_directory,
                                  morphology.label,
                                  'example-2.pdf'),
                bbox_inches='tight')
    # Close figure to reset
    plt.close()

    sns.violinplot(x=x, y=y)
    plt.savefig('%s/%s-%s.pdf' % (options.io.analysis_directory,
                                  morphology.label,
                                  'example-3.pdf'),
                bbox_inches='tight')
    # Close figure to reset
    plt.close()


def kernel_samples_radii(morphology, options):

    # Analysis results
    analysis_results = nmv.analysis.compile_data(
        morphology,
        nmv.analysis.get_samples_radii_data_of_arbor)

    # Aggregate
    nmv.analysis.aggregate_arbors_data_to_morphology(analysis_results)

    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns


    x_data = list()
    y_data = list()
    r_data = list()

    for result in analysis_results.morphology_result:
        x_data.append(result.branching_order)
        y_data.append(result.value)
        r_data.append(result.radial_distance)

    # Create data
    x = np.asarray(x_data)
    y = np.asarray(y_data)
    r = np.asarray(r_data)

    colors = (0, 0, 0)
    '''
    # Plot
    plt.scatter(x, y, c=colors, alpha=0.5)
    plt.title('Example')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('/Users/abdellah/Desktop/nmv-release/figures/example.pdf')

    sns.regplot(x=x, y=y, fit_reg=False)
    plt.savefig('/Users/abdellah/Desktop/nmv-release/figures/example2.pdf')

    sns.regplot(x=r, y=y, fit_reg=False)
    plt.savefig('/Users/abdellah/Desktop/nmv-release/figures/example3.pdf')
    
    '''

    #for i in analysis_results.morphology_result:
    #    print(i.value, i.branching_order)


####################################################################################################
# @kernel_segments_length_range_distribution
####################################################################################################
def kernel_samples_per_section_range_distribution(morphology,
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
        nmv.analysis.compute_minimum_samples_count_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)

    # Average
    average_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_number_samples_per_section_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)

    # Maximum
    maximum_results = nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_samples_count_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)

    # Plot
    nmv.analysis.plot_min_avg_max_per_arbor_distribution(
        minimum_results=minimum_results,
        maximum_results=maximum_results,
        average_results=average_results,
        morphology=morphology,
        options=options,
        figure_name='samples-per-section-range',
        x_label='Samples Count',
        title='Samples Count')
