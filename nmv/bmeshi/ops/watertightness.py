####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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


####################################################################################################
# @WatertightCheck
####################################################################################################
class WatertightCheck:
    """The watertightness checking class that contains all the elements needed to verify the
    watertightness of a given mesh."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor"""

        # By default, the mesh is not watertight
        self.watertight = False

        # Non-contiguous edges
        self.non_contiguous_edge_count = 0
        self.non_contiguous_edges = None

        # Non-manifold edges
        self.non_manifold_edges_count = 0
        self.non_manifold_edges = None

        # Non-manifold vertices
        self.non_manifold_vertices_count = 0
        self.non_manifold_vertices = None

        # Self-intersections
        self.self_intersecting_faces_count = 0
        self.self_intersecting_faces = None

        # Zero-faces count (can introduce self-intersections)
        self.zero_faces_count = 0
        self.zero_faces = None

    ################################################################################################
    # @is_watertight
    ################################################################################################
    def is_watertight(self):
        """Checks if the mesh is watertight or not."""

        if self.non_manifold_edges_count > 0 or         \
            self.non_manifold_vertices_count > 0 or     \
            self.self_intersecting_faces_count > 0 or   \
            self.zero_faces_count > 0:
            return False
        return True

    ################################################################################################
    # @print_status
    ################################################################################################
    def print_status(self):
        """Prints the status of the watertightness, probably in iterations."""

        print('WATERTIGHTNESS\t \n'
              '\tNon-manifold edges: %d, Non-manifold vertices: %d, Non-contiguous edges : %d\n'
              '\tZero-faces %d, Self-intersecting faces: %d' %
              (self.non_manifold_edges_count,
               self.non_manifold_vertices_count,
               self.non_contiguous_edge_count,
               self.zero_faces_count,
               self.self_intersecting_faces_count))
