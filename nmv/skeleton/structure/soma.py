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
# Soma
####################################################################################################
class Soma:
    """ A class to represent the soma of a neuron. """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 centroid,
                 mean_radius,
                 profile_points,
                 arbors_profile_points=None):
        """Constructor

        :param centroid:
            Soma centroid, normally the origin, unless specified.
        :param mean_radius:
            Soma average radius as measured in the lab and reported in the morphology file .
        :param profile_points:
            A list of the profile points that reflect its XY projection.
        :param arbors_profile_points:
            A list of profile points measured from the initial samples of the arbors.
        """

        # Soma center (normally origin if local coordinates are used)
        self.centroid = centroid

        # Soma average radius based on the profile points
        self.mean_radius = mean_radius

        # Soma profile points, they are typically ignored when reconstructing the soma on a
        # physically-plausible basis, but they can also used to make the soma more irregular
        self.profile_points = profile_points

        # The profile points of the arbors
        self.arbors_profile_points = sorted(arbors_profile_points)

        # Possible radii that can be assigned to the soma during its reconstruction
        self.possible_radii = list()

        # Add the soma profile points radii to the possible_radii list
        for point in self.profile_points:
            self.possible_radii.append(point.length)

        # Add the arbors profile points radii to the possible_radii list
        if self.arbors_profile_points is not None:
            for point in self.arbors_profile_points:
                self.possible_radii.append(point.length)

        # Sort the radii in the list
        self.possible_radii = sorted(self.possible_radii)

        # The smallest radius
        self.smallest_radius = self.possible_radii[0]

        # The largest radius
        self.largest_radius = self.possible_radii[-1]


