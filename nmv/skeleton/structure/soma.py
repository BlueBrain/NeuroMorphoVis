####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
                 arbors_profile_points=None,
                 reported_centroid=None,
                 reported_mean_radius=None):
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

        # Soma centroid (normally origin if local coordinates are used)
        self.centroid = centroid

        # The soma centroid as reported in the morphology file
        self.reported_centroid = reported_centroid

        # Soma average radius
        self.mean_radius = mean_radius

        # The soma average radius as reported in the morphology file
        self.reported_mean_radius = reported_mean_radius

        # Soma profile points, they are typically ignored when reconstructing the soma on a
        # physically-plausible basis, but they can also be used to make the soma more irregular
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
            self.distances_to_soma.append((point - self.centroid).length)

        # Add the arbors profile points radii to the distances_to_soma list
        if self.arbors_profile_points is not None:
            for point in self.arbors_profile_points:
                self.distances_to_soma.append((point - self.centroid).length)

        # Sort the radii in the list
        self.distances_to_soma = sorted(self.distances_to_soma)

        # If the mean radius is already smaller than the minimum radius
        if self.mean_radius < self.distances_to_soma[0]:
            actual_mean_radius = sum(self.distances_to_soma) / (len(self.distances_to_soma) * 1.0)
        else:
            actual_mean_radius = mean_radius

        # Clean the possible radii list
        self.possible_radii = list()

        for value in self.distances_to_soma:
            if (actual_mean_radius / 2.0) < value < (actual_mean_radius * 3.0):
                self.possible_radii.append(value)

        # Ensure that the possible radii list is available
        if len(self.possible_radii) > 0:
            self.smallest_radius = self.possible_radii[0] - nmv.consts.Math.LITTLE_EPSILON
            self.largest_radius = self.possible_radii[-1] + nmv.consts.Math.LITTLE_EPSILON

        else:
            self.smallest_radius = actual_mean_radius
            self.largest_radius = actual_mean_radius

        # A list of points representing the 3d profile of the soma
        self.profile_3d = list()
