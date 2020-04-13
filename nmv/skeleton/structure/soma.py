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
import nmv.consts


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
        self.arbors_profile_points = arbors_profile_points

        # If the list is given, sort the profile points
        if self.arbors_profile_points is not None:
            self.arbors_profile_points = sorted(arbors_profile_points)

        # A list containing the distances from the profile point to the soma origin
        self.distances_to_soma = list()

        # Add the soma profile points radii to the distances_to_soma list
        for point in self.profile_points:
            self.distances_to_soma.append(point.length)

        # Add the arbors profile points radii to the distances_to_soma list
        if self.arbors_profile_points is not None:
            for point in self.arbors_profile_points:
                self.distances_to_soma.append(point.length)

        # Sort the radii in the list
        self.distances_to_soma = sorted(self.distances_to_soma)

        # Clean the possible radii list
        self.possible_radii = list()

        for value in self.distances_to_soma:
            if (self.mean_radius / 2.0) < value < (self.mean_radius * 2.0):
                self.possible_radii.append(value)

        # Ensure that the possible radii list is available
        if len(self.possible_radii) > 0:
            self.smallest_radius = self.possible_radii[0] - nmv.consts.Math.LITTLE_EPSILON
            self.largest_radius = self.possible_radii[-1] + nmv.consts.Math.LITTLE_EPSILON

        else:
            self.smallest_radius = self.mean_radius
            self.largest_radius = self.mean_radius




