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
# VasculatureSample
####################################################################################################
class VasculatureSample:
    """Vasculature morphological sample.

    The section is composed of a set of segments or edges , and each segment is composed of two
    samples. Each sample has a point in the cartesian coordinates and a radius that reflect the
    cross-sectional area of the morphology at a certain point.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 index,
                 point,
                 radius):
        """Constructor

        :param point:
            Sample position in the cartesian space, Vector((x, y, z)).
        :param radius:
            Sample radius in microns.
        :param index:
            Sample index along the section from 0 to N-1 if the section has N samples.
        """

        # Sample cartesian point
        self.point = point

        # Sample radius
        self.radius = radius

        # Sample index along the section (from 0 to N, updated after section construction)
        self.index = index
