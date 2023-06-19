####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
# @kernel_minimum_global_bifurcation_angle
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
