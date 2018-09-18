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


# Blender imports
from mathutils import Vector

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.consts


####################################################################################################
# @BoundingBox
####################################################################################################
class BoundingBox:
    """Bounding box
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self, 
                 p_min=nmv.consts.Math.ORIGIN,
                 p_max=nmv.consts.Math.ORIGIN,
                 center=nmv.consts.Math.ORIGIN,
                 bounds=nmv.consts.Math.ORIGIN):
        """Constructor
        """

        # Construct the bounding box from @p_min and @p_max
        if p_min != nmv.consts.Math.ORIGIN and max != nmv.consts.Math.ORIGIN:
            self.p_min = p_min
            self.p_max = p_max
            self.bounds = p_max - p_min
            self.center = p_min + (self.bounds / 2.0)

        # Construct the bounding box from @bounds and @center
        else:
            self.bounds = bounds
            self.center = center
            self.p_min = center - (self.bounds / 2.0)
            self.p_max = center + (self.bounds / 2.0)

    ################################################################################################
    # @extend_bbox
    ################################################################################################
    def extend_bbox(self,
                    delta=1.0):
        """Extends the bounding box few microns uniformly in all the directions.

        :param delta:
            The value that will be used to extend the bounding box.
        """

        self.p_min -= Vector((delta, delta, delta))
        self.p_max += Vector((delta, delta, delta))
        self.bounds = self.p_max - self.p_min
        self.center = self.p_min + (self.bounds / 2.0)

    ################################################################################################
    # @print_details
    ################################################################################################
    def print_details(self,
                      name='BBox'):
        """Prints the bounding box data.
        """  
        nmv.logger.log("Shape BBox: %s" % name)
        nmv.logger.log("pMin: " + str(self.p_min))
        nmv.logger.log("pMax: " + str(self.p_max))
        nmv.logger.log("Bounds: " + str(self.bounds))
        nmv.logger.log("Center: " + str(self.center))
