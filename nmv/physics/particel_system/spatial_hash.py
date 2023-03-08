####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# The code in this file is based on the Tesselator add-on, version 1.28, that is provided by
# Jean Da Costa Machado. The code is available at https://github.com/jeacom25b/Tesselator-1-28
# which has a GPL license similar to NeuroMorphoVis.
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
# System imports
import math


####################################################################################################
# SpatialHash
####################################################################################################
class SpatialHash:
    """Spatial hash table.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 cell_size=0.1):
        """Constructor

        :param cell_size:
            The size of the cell in the grid.
        """

        self.buckets = {}
        self.items = {}
        self.size = cell_size

    ################################################################################################
    # @get_key
    ################################################################################################
    def get_key(self,
                location):
        """Returns the key given the location.

        :param location:
            The location of a specific point where we need the key.
        :return:
        """

        # Returns the key
        return (round(location[0] / self.size),
                round(location[1] / self.size),
                round(location[2] / self.size))

    ################################################################################################
    # @insert
    ################################################################################################
    def insert(self,
               item,
               key=None):
        """Inserts an element in the hash grid.

        :param item:
            New element.
        :param key:
            The key of the element.
        """

        # If the key is not given, get it based on its location
        if not key:
            key = self.get_key(item.co)
        if key in self.buckets:
            self.buckets[key].add(item)
        else:
            self.buckets[key] = {item, }
        self.items[item] = self.buckets[key]

    ################################################################################################
    # @remove
    ################################################################################################
    def remove(self,
               item):
        """Removes an element from the hash table.

        :param item:
            The element to be removed.
        """

        self.items[item].remove(item)
        del self.items[item]

    ################################################################################################
    # @update
    ################################################################################################
    def update(self,
               item):
        """Update the element in the hash table.

        :param item:
            The element to be updated.
        """

        self.remove(item)
        self.insert(item)

    ################################################################################################
    # @test_sphere
    ################################################################################################
    def test_sphere(self,
                    co,
                    radius,
                    exclude=()):

        radius_sqr = radius ** 2
        radius = radius / self.size
        location = co / self.size
        min_x = math.floor(location[0] - radius)
        max_x = math.ceil(location[0] + radius)
        min_y = math.floor(location[1] - radius)
        max_y = math.ceil(location[1] + radius)
        min_z = math.floor(location[2] - radius)
        max_z = math.ceil(location[2] + radius)
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    key = (x, y, z)
                    if key in self.buckets:
                        for item in self.buckets[key]:
                            if (item.co - co).length_squared <= radius_sqr:
                                if item in exclude:
                                    continue
                                yield item

