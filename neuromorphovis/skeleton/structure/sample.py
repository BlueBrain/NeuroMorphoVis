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


####################################################################################################
# Sample
####################################################################################################
class Sample:
    """Morphological skeleton sample.

    The section is composed of a set of segments, and each segment is composed of two samples.
    Each sample has a point in the cartesian coordinates and a radius that reflect the
    cross-sectional area of the morphology at a certain point. The sample is identified by
    two indexes or IDs, the first is used to label the order of the sample along the
    morphological section, and the second represents the order of the sample in the morphology
    file.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 point,
                 radius,
                 id,
                 morphology_id=-1,
                 section=None):
        """Constructor

        :param point:
            Sample position in the cartesian space, Vector((x, y, z)).
        :param radius:
            Sample radius in microns.
        :param id:
            Sample index along the section from 0 to N-1 if the section has N samples.
        :param morphology_id:
            Sample index as reported in the morphology file.
        :param section:
            A reference to the section where the sample belongs to, initially None.
            This member is updated after re-constructing the morphology skeleton.
        """

        # Sample cartesian point
        self.point = point

        # Sample radius
        self.radius = radius

        # Sample index along the section (from 0 to N, updated after section construction)
        self.id = id

        # Sample index as reported in the morphology file, -1 is UNKNOWN or AUXILIARY
        self.morphology_index=morphology_id

        # The section, where the sample belongs (updated after the section construction)
        self.section = section

    ################################################################################################
    # @logger.log_data
    ################################################################################################
    def print_data(self):
        """Print the details of the sample.
        """

        nmv.logger.log('Sample [%d]:[point=(%f, %f, %f), radius=%f]' %
              (self.id, self.point.x(), self.point.y(), self.point.z(), self.radius))