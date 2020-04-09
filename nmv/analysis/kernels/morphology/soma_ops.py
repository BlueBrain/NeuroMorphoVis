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
import nmv.analysis


####################################################################################################
# @kernel_soma_get_reported_mean_radius
####################################################################################################
def kernel_soma_get_reported_mean_radius(morphology):
    """Get the mean radius of the soma as reported in the morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return morphology.soma.mean_radius


####################################################################################################
# @kernel_soma_get_minimum_radius
####################################################################################################
def kernel_soma_get_minimum_radius(morphology):
    """Get the minimum radius of the soma as based on the reported profile points and the root
    samples of all the connected arbors (or stems).

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return morphology.soma.smallest_radius


####################################################################################################
# @kernel_soma_get_maximum_radius
####################################################################################################
def kernel_soma_get_maximum_radius(morphology):
    """Get the maximum radius of the soma as based on the reported profile points and the root
    samples of all the connected arbors (or stems).

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return morphology.soma.largest_radius


####################################################################################################
# @kernel_soma_get_average_surface_area
####################################################################################################
def kernel_soma_get_average_surface_area(morphology):
    """Get the average surface area of the soma based on the mean radius reported in the morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return 4 * 3.14 * (morphology.soma.mean_radius * morphology.soma.mean_radius)


####################################################################################################
# @kernel_global_get_soma_volume
####################################################################################################
def kernel_soma_get_average_volume(morphology):
    """Get the volume of the soma based on its mean radius as reported in the morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    radius = morphology.soma.mean_radius
    return (3.0 / 4.0) * 3.14 * (radius * radius * radius)


####################################################################################################
# @kernel_soma_get_reported_mean_radius
####################################################################################################
def kernel_soma_count_profile_points(morphology):
    """Count the profile points of the soma as reported in the morphology file.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return len(morphology.soma.profile_points)
