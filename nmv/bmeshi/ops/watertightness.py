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

    def __init__(self):
        self.watertight = False
        self.non_contiguous_edge_count = 0
        self.non_contiguous_edges = None
        self.non_manifold_edges_count = 0
        self.non_manifold_edges = None
        self.non_manifold_vertices_count = 0
        self.non_manifold_vertices = None
        self.self_intersecting_faces_count = 0
        self.self_intersecting_faces = None
        self.zero_faces_count = 0
        self.zero_faces = None

    def is_watertight(self):
        #if self.non_contiguous_edge_count > 0 or \
        #    self.non_manifold_edges_count > 0 or \
        #    self.non_manifold_vertices_count > 0 or \
        #    self.self_intersecting_faces_count > 0 or \
        #    self.zero_faces_count > 0:
        #    return False
        if self.non_manifold_edges_count > 0 or \
            self.non_manifold_vertices_count > 0 or \
            self.self_intersecting_faces_count > 0 or \
            self.zero_faces_count > 0:
            return False
        return True

    def print_status(self):
        print('WATERTIGHNTESS\t \n'
              '\t Non-manifold edges: %d\n'
              '\t Non-manifold vertices: %d\n'
              '\t Non-contiguous edges : %d\n'
              '\t Zero-faces %d\n'
              '\t Self-intersecting faces: %d\n' %
              (self.non_manifold_edges_count,
               self.non_manifold_vertices_count,
               self.non_contiguous_edge_count,
               self.zero_faces_count,
               self.self_intersecting_faces_count))
