####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# imports
import os
import sys
import imp

# append the internal modules into the system paths
sys.path.append("%s/../modules" % os.path.dirname(os.path.realpath(__file__)))


# use the following modules
import bbp_morphology
import const
import h5_parser


################################################################################
# @load_morphology_from_gid
################################################################################
def load_morphology_from_gid(blue_config,
                             gid):
    """

    :param blue_config:
    :param gid:
    :return:
    """
    # load the BBP morphology using the Brain API
    #bbp_morphology_object = bbp_morphology.load_morphology_from_gid(blue_config, gid)

    # convert it to a our skeleton structure
    # morphology = bbp_morphology.convert_morphology_to_skeleton(gid, bbp_morphology_object)


    file_path = '/abdellah-bbp/morphology-datasets/h5-morphologies/vd110112_INT_A_idA_-_Scale_x1.000_y1.050_z1.000_-_Clone_1.h5'
    morphology_skeleton = h5_parser.parse_h5_morphology(file_path)

    return morphology_skeleton


################################################################################
# @load_morphologies_from_target
################################################################################
def load_morphologies_from_target(blue_config,
                                  target):
    """

    :param blue_config:
    :param target:
    :return:
    """

    # load the BBP morphology using the Brain API
    bbp_morphologies, gids = bbp_morphology.load_morphologies_from_target(
        blue_config, target)

    # convert it to a our skeleton structure
    morphologies = []
    for i, bbp_morphology_object in enumerate(bbp_morphologies):
        morphologies.append(bbp_morphology.convert_morphology_to_skeleton(
            gids[i], bbp_morphology_object))
    return morphologies, gids



def load_morphology_from_swc_file(swc_file):

    swc_morphology = 0
    morphology = swc_morphology.convert_morphology_to_skeleton(swc_morphology)
    return morphology


################################################################################
# @get_minimal_and_maximal_profile_distances
################################################################################
def get_minimal_and_maximal_profile_distances(soma):
    """
    Returns the minimal and maximal distances for the profile points of the
    soma.

    :param soma:
    :return:
    """

    # get the profile points
    profile_points = soma.profile_points

    maximal_distance = -const.infinity
    minimal_distance = const.infinity

    for profile_point in profile_points:

        distance = profile_point.length
        if distance > maximal_distance:
            maximal_distance = distance

        if distance < minimal_distance:
            minimal_distance = distance

    return minimal_distance, maximal_distance