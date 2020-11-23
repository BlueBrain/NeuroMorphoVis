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


####################################################################################################
# Particle
####################################################################################################
class Particle:
    """A particle to simulate a particle system.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 location,
                 normal,
                 bvh_tree=None):
        """Constructor

        :param location:
            Initial particle location.
        :param normal:
            Initial particle normal.
        :param bvh_tree:
            BVH.
        """

        # Particle color
        self.color = Vector((1, 0, 0, 1))

        # Particle radius, initially set to Zero
        self.radius = 0

        # Particle location
        self.co = location

        # Particle normal
        self.normal = normal

        # System BVH
        self.bvh = bvh_tree

        # Particle direction in every update in the simulation
        self.dir = Vector((1, 0, 0))

        # Particle field
        self.field = None

        # Particle parent
        self.parent = None

        # Particle name or tag
        self.tag = "PARTICLE"

        # Particle tag number, initially set to Zero
        self.tag_number = 0

        # Accumulation, initially set to the particle location before applying any forces
        self.accumulation = location

        # Accumulation counter, initially set to 1
        self.accumulation_counts = 1

        # Normal accumulation, initially set to the given normal
        self.normal_accumulation = normal

        # Normal accumulation counter, initially set to 1
        self.normal_accumulation_counts = 1

    ################################################################################################
    # @add_location_sample
    ################################################################################################
    def add_location_sample(self,
                            location,
                            weight=0.3):
        """Update the location of the particle based on a given sample.

        :param location:
            Location
        :param weight:
            Weight, by default 0.3.
        """

        # Accumulation
        self.accumulation += location * weight

        # Accumulation counts
        self.accumulation_counts += weight

        # Update the location of the particle
        self.co = self.accumulation / self.accumulation_counts

    ################################################################################################
    # @add_normal_sample
    ################################################################################################
    def add_normal_sample(self,
                          normal,
                          weight):
        """Update the normal of the particle based on a given sample.

        :param normal:
            Normal
        :param weight:
            Weight
        """

        # Accumulation
        self.normal_accumulation += normal * weight

        # Accumulation counts
        self.normal_accumulation_counts += weight

        # Update the normal of the particle
        self.normal = self.normal_accumulation / self.normal_accumulation_counts

