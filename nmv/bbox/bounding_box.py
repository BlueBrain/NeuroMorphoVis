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

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.consts


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
    # @extend_bbox
    ################################################################################################
    def extend_bbox(self,
                    delta_x=1.0,
                    delta_y=1.0,
                    delta_z=1.0):
        """Extends the bounding box few microns uniformly in all the directions.

        :param delta_x:
            The value that will be used to extend the bounding box around the x-axis.
        :param delta_y:
            The value that will be used to extend the bounding box around the y-axis.
        :param delta_z:
            The value that will be used to extend the bounding box around the z-axis.
        """

        self.p_min -= Vector((delta_x, delta_y, delta_z))
        self.p_max += Vector((delta_x, delta_y, delta_z))
        self.bounds = self.p_max - self.p_min
        self.center = self.p_min + (self.bounds / 2.0)

    ################################################################################################
    # @get_largest_dimension
    ################################################################################################
    def get_largest_dimension(self):
        """Gets the largest dimension of the bounding box

        :return:
            The largest dimension of the bounding box.
        """

        largest_dimension = self.bounds[0]
        if self.bounds[1] > largest_dimension:
            largest_dimension = self.bounds[1]
        if self.bounds[2] > largest_dimension:
            largest_dimension = self.bounds[2]
        return largest_dimension

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
