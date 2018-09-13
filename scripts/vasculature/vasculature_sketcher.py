####################################################################################################
# Copyright (c) 2018, EPFL / Blue Brain Project
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



# Blender import
from mathutils import Vector

# Import vasculature scripts
import vasculature_sample
import vasculature_section


####################################################################################################
# VasculatureSketcher
####################################################################################################
class VasculatureSketcher:
    """Vasculature sketching class."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 points_list,
                 segments_list,
                 sections_list,
                 connections_list):
        """Constructor

        :param points_list:
            A list of all the points in the morphology skeleton.
        :param segments_list:
            A list of all the edges in the morphology skeleton.
        :param sections_list:
            A list of all the sections in the morphology skeleton.
        :param connections_list:
            A list of all the connections in the morphology skeleton.
        """

        # A list of all the points in the morphology
        self.morphology_points_list = points_list

        # A list of all the segments in the morphology
        self.morphology_segments_list = segments_list

        # A list of all the sections in the morphology
        self.morphology_sections_list = sections_list

        # A list of all the connections in the morphology
        self.morphology_connections_list = connections_list

        # A linear list of all the sections in the vasculature morphology
        self.sections_list = list()

        # A list of all the root sections into the skeleton that can give us access to the rest
        # of the sections
        self.roots = list()