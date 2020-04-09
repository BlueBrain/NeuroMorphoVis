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
# @kernel_global_number_apical_dendrites
####################################################################################################
def kernel_global_number_apical_dendrites(morphology):
    """Counts the number of apical dendrites of the morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return 0 if morphology.apical_dendrite is None else 1


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

    return 0 if morphology.dendrites is None else len(morphology.dendrites)


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

    return 0 if morphology.axon is None else 1


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

    return kernel_global_number_apical_dendrites(morphology) + \
           kernel_global_number_basal_dendrites(morphology) + \
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

