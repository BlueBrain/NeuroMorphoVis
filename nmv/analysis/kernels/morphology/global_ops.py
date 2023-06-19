####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
# @kernel_global_number_apical_dendrites
####################################################################################################
def kernel_global_number_apical_dendrites(morphology):
    """Counts the number of apical dendrites of the morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return 0 if morphology.apical_dendrites is None else len(morphology.apical_dendrites)


####################################################################################################
# @kernel_global_number_basal_dendrites
####################################################################################################
def kernel_global_number_basal_dendrites(morphology):
    """Counts the number of basal dendrites of the morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return 0 if morphology.basal_dendrites is None else len(morphology.basal_dendrites)


####################################################################################################
# @kernel_global_number_axons
####################################################################################################
def kernel_global_number_axons(morphology):
    """Counts the number of axons dendrites of the morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return 0 if morphology.axons is None else len(morphology.axons)


####################################################################################################
# @kernel_global_total_number_neurites
####################################################################################################
def kernel_global_total_number_neurites(morphology):
    """Counts the total number of neurites of the morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return kernel_global_number_apical_dendrites(morphology) +  \
           kernel_global_number_basal_dendrites(morphology) +   \
           kernel_global_number_axons(morphology)


####################################################################################################
# @kernel_global_total_number_stems
####################################################################################################
def kernel_global_total_number_stems(morphology):
    """Counts the total number of stems in the morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return morphology.number_stems


####################################################################################################
# @combine_results_into_single_list
####################################################################################################
def combine_results_into_single_list(basal_dendrites_list,
                                     apical_dendrites_list,
                                     axons_list):
    """Combines the results of a the entire morphology into a single list.

    :param basal_dendrites_list:
        A list of numbers corresponding to the analysis results of the basal dendrites.
    :param apical_dendrites_list:
        A list of numbers corresponding to the analysis results of the apical dendrites.
    :param axons_list:
        A list of numbers corresponding to the analysis results of the axons.
    :return:
        A list combining all the results.
    """

    # A list that will combine all the lists to get a specific number depending on the operation
    resulting_list = list()

    # Basals
    if basal_dendrites_list is not None:
        resulting_list.extend(basal_dendrites_list)

    # Apicals
    if apical_dendrites_list is not None:
        resulting_list.extend(apical_dendrites_list)

    # Axons
    if axons_list is not None:
        resulting_list.extend(axons_list)

    # Return the resulting list
    return resulting_list
