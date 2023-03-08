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
import numpy

# Blender imports
import bpy
import bmesh
from mathutils import Vector
from mathutils.geometry import barycentric_transform
from mathutils.bvhtree import BVHTree
from itertools import product

# Internal imports
import nmv.physics
import nmv.consts


####################################################################################################
# Field
####################################################################################################
class Field:
    """

    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 mesh_object,
                 max_adjacent=20,
                 enable_drawing=False):
        """Constructor

        :param mesh_object:
            A given mesh object to calculate the field around.
        :param max_adjacent:
            Maximum number of adjacent vertices or edges per vertex.
        :param enable_drawing:
            Enable the drawing functions in the interactive mode.
        """

        # World matrix
        self.matrix = mesh_object.matrix_world.copy()

        # Drawing function and matrix
        if enable_drawing:
            self.draw = nmv.physics.DrawCallback()
            self.draw.matrix = self.matrix

        # Field mesh represented by a bmesh object
        self.bm = bmesh.new()

        # Convert the given mesh into a bmesh
        self.bm.from_mesh(mesh_object.data)

        # Triangulate the mesh before proceeding
        bmesh.ops.triangulate(self.bm, faces=self.bm.faces)

        # Update the lookup tables
        self.bm.verts.ensure_lookup_table()
        self.bm.edges.ensure_lookup_table()
        self.bm.faces.ensure_lookup_table()

        # Disable the HEX mode
        self.hex_mode = False

        # Create the BVH of the bmesh
        self.bvh = BVHTree.FromBMesh(self.bm)
        
        # Get the number of vertices of the bmesh 
        self.number_vertices = len(self.bm.verts)

        # Max adjacent
        self.max_adjacent = max_adjacent

        # A list of singularities
        self.singularities = list()

        # A numpy array of the locations
        self.locations = numpy.array([vert.co for vert in self.bm.verts], dtype=numpy.float32)

        # A numpy array of the normals
        self.normals = numpy.zeros((self.number_vertices, 3), dtype=numpy.float32)

        # A numpy array for the adjacents
        self.adjacent_counts = numpy.zeros((self.number_vertices,), dtype=numpy.float32)

        # A numpy array for the fields
        self.field = numpy.zeros((self.number_vertices, 3), dtype=numpy.float64)

        # A numpy array for the scales
        self.scale = numpy.zeros((self.number_vertices,), dtype=numpy.float64)

        # A numpy array for the curvatures
        self.curvature = numpy.zeros((self.number_vertices,), dtype=numpy.float64)

        # A numpy array for the weights
        self.weights = numpy.ones((self.number_vertices,), dtype=numpy.float64)

        # A numpy array for the connectivity
        self.connectivity = numpy.zeros((self.number_vertices, max_adjacent), dtype=numpy.int64)

        # Mask layer
        mask_layer = self.bm.verts.layers.paint_mask.verify()

        # For each vertex in the bmesh object
        for vertex in self.bm.verts:

            # A reference to the vertex index
            i = vertex.index

            #
            self.field[i] = nmv.physics.curvature_direction(vertex)

            # Get the normal of the vertex
            self.normals[i] = nmv.physics.vert_normal(vertex)

            # Get the scale of the field from the mask layer
            self.scale[i] = vertex[mask_layer]

            # Get the average curvature of the vertex
            self.curvature[i] = nmv.physics.average_curvature(vertex)

            # Get the adjacent vertices
            self.adjacent_counts[i] = min(len(vertex.link_edges), max_adjacent)

            # If this is a boundary vertex, set its weight to zero to avoid creating distorted mesh
            if vertex.is_boundary:
                self.weights[vertex.index] = 0

            # Update the connectivity matrix
            for j, edge in enumerate(vertex.link_edges):

                # Reached maximum adjacent edges
                if j >= max_adjacent:
                    continue

                # Update the connectivity matrix
                self.connectivity[i, j] = edge.other_vert(vertex).index

    ################################################################################################
    # @initialize_from_grease_pencil
    ################################################################################################
    def initialize_from_grease_pencil(self,
                                      context):
        """

        :param context:
        :return:
        """

        mat = self.matrix.inverted()
        frame = nmv.physics.get_grease_pencil_frame(context)
        seen_vertices = set()
        if frame:
            for stroke in frame.strokes:
                le = len(stroke.points)
                for i in range(le - 2):
                    p0 = mat @ stroke.points[i].co
                    p1 = mat @ stroke.points[i + 1].co
                    p2 = mat @ stroke.points[i + 2].co
                    d = p0 - p1
                    d += p1 - p2

                    location, normal, index, dist = self.bvh.find_nearest(p1)
                    face = self.bm.faces[index]
                    vert = min(face.verts, key=lambda v: (v.co - p1).length_squared)
                    self.field[vert.index] = d.normalized()
                    self.weights[vert.index] = 0
                    seen_vertices.add(vert)

        current_front = set()
        for vert in seen_vertices:
            for edge in vert.link_edges:
                other = edge.other_vert(vert)
                if other not in seen_vertices:
                    current_front.add(vert)

        while current_front:
            new_front = set()
            for vert in current_front:
                d = Vector()
                tot = 0
                for edge in vert.link_edges:
                    other = edge.other_vert(vert)
                    if other in seen_vertices:
                        if not tot:
                            d = Vector(self.field[other.index])
                        else:
                            d += nmv.physics.best_matching_vector(
                                nmv.physics.symmetry_space(self.field[other.index], other.normal),
                                d
                            )
                        tot += 1
                    else:
                        new_front.add(other)
                        self.weights[other.index] = self.weights[vert.index] + 1
                    if tot:
                        self.field[vert.index] = d.normalized().cross(vert.normal)
            seen_vertices |= current_front
            new_front -= seen_vertices
            current_front = new_front
        self.weights /= self.weights.max()

    ################################################################################################
    # @walk_edges
    ################################################################################################
    def walk_edges(self,
                   depth=0):
        """

        :param depth:
        :return:
        """


        cols = numpy.arange(self.number_vertices)

        ids = numpy.random.randint(0, self.max_adjacent,
                                   (self.number_vertices,)) % self.adjacent_counts

        ids = ids.astype(numpy.int_)

        adjacent_edges = self.connectivity[cols, ids]

        for _ in range(depth):
            ids = numpy.random.randint(0, self.max_adjacent, (self.number_vertices,)) % \
                  self.adjacent_counts[adjacent_edges]

            ids = ids.astype(numpy.int_)

            adjacent_edges = self.connectivity[adjacent_edges, ids]

        return adjacent_edges

    ################################################################################################
    # @smooth
    ################################################################################################
    def smooth(self,
               iterations=100,
               depth=3):

        def find_best_combinations(a, b):

            w = self.weights[:, numpy.newaxis]
            scores = []
            vectors = []
            for a, b in product(a, (b * w)):
                m = (a * b).sum(axis=1)
                scores.append(m)
                vectors.append((a + b))
            scores = numpy.stack(scores, axis=0)
            vectors = numpy.stack(vectors, axis=0)
            idx = scores.argmax(axis=0)
            cols = numpy.arange(self.number_vertices)
            rval = vectors[idx, cols]
            nans = numpy.isnan(rval)
            rval[nans] = 0
            return rval * (1 / (w + 1))

        if not self.hex_mode:
            for i in range(iterations):

                a = self.field
                b = numpy.cross(self.field, self.normals)
                adjacent_edges = self.walk_edges(depth)

                c = self.field[adjacent_edges]
                d = numpy.cross(c, self.normals[adjacent_edges])

                best = find_best_combinations((a, b, -a, -b), (c, d))
                best = best - self.normals * (best * self.normals).sum(axis=1)[:, numpy.newaxis]
                self.field = best
        else:
            for i in range(iterations):
                x = self.field
                y = numpy.cross(self.field, self.normals)
                a = x
                b = x * 0.5 + y * 0.866025
                c = x * -0.5 + y * 0.866025

                adjacent_edges = self.walk_edges(depth)

                x = self.field[adjacent_edges]
                y = numpy.cross(x, self.normals[adjacent_edges])
                d = x
                e = x * 0.5 + y * 0.866025
                f = x * -0.5 + y * 0.866025

                best = find_best_combinations((a, b, c, -a, -b, -c), (d, e, f))
                best = best - self.normals * (best * self.normals).sum(axis=1)[:, numpy.newaxis]
                self.field = best

        self.field = nmv.physics.normalize_vectors_array(self.field)

    ################################################################################################
    # @autoscale
    ################################################################################################
    def autoscale(self):
        symmetry = nmv.physics.hex_symmetry_space if self.hex_mode else nmv.physics.symmetry_space

        for vert in self.bm.verts:
            u = Vector(self.field[vert.index])
            v = u.cross(vert.normal)
            ang = 0
            last_vec = u
            for loop in vert.link_loops:
                vert1 = loop.link_loop_next.vert
                vert2 = loop.link_loop_next.link_loop_next.vert
                if not last_vec:
                    vert1_vec = Vector(self.field[vert1.index])
                else:
                    vert1_vec = last_vec

                vert2_vec = nmv.physics.best_matching_vector(symmetry(self.field[vert2.index], vert2.normal), vert1_vec)

                vert1_vec = Vector((vert1_vec.dot(u), vert1_vec.dot(v)))
                vert2_vec = Vector((vert2_vec.dot(u), vert2_vec.dot(v)))

                ang += vert1_vec.angle_signed(vert2_vec)
            self.scale[vert.index] = ang
        for i in range(20):
            self.scale += self.scale[self.walk_edges(0)]
            self.scale /= 2
        self.scale -= self.scale.min()
        self.scale /= self.scale.max()

    ################################################################################################
    # @mirror
    ################################################################################################
    def mirror(self, axis=0):
        mirror_vec = Vector()
        mirror_vec[axis] = -1
        for vert in self.bm.verts:
            if vert.co[axis] < 0:
                mirror_co = vert.co.copy()
                mirror_co[axis] *= -1
                location, normal, vec, s, c = self.sample_point(mirror_co)
                self.field[vert.index] = vec - vec.dot(mirror_vec) * 2 * mirror_vec

    ################################################################################################
    # @detect_singularities
    ################################################################################################
    def detect_singularities(self):
        symmetry = nmv.physics.hex_symmetry_space if self.hex_mode else nmv.physics.symmetry_space
        cache = {}

        def symmetry_cached(vert):
            if vert in cache:
                return cache[vert]
            else:
                s = symmetry(self.field[vert.index], vert.normal)
                cache[vert] = s
                return s

        singularities = []

        if not self.hex_mode:
            for face in self.bm.faces:
                v0 = face.verts[0]
                v1 = face.verts[1]
                v2 = face.verts[2]
                vec0 = self.field[v0.index]
                vec1 = nmv.physics.best_matching_vector(symmetry_cached(v1), vec0)
                v2_symmetry = symmetry_cached(v2)
                match0 = nmv.physics.best_matching_vector(v2_symmetry, vec0)
                match1 = nmv.physics.best_matching_vector(v2_symmetry, vec1)
                if match0.dot(match1) < 0.5:
                    singularities.append(face.calc_center_median())
        else:
            for vert in self.bm.verts:
                ang = 0
                u = nmv.physics.random_tangent_vector(vert.normal)
                v = u.cross(vert.normal)
                last_vec = None
                for loop in vert.link_loops:
                    vert1 = loop.link_loop_next.vert
                    vert2 = loop.link_loop_next.link_loop_next.vert
                    if not last_vec:
                        vert1_vec = symmetry_cached(vert1)[0]
                    else:
                        vert1_vec = last_vec
                    vert2_vec = nmv.physics.best_matching_vector(symmetry_cached(vert2), vert1_vec)
                    last_vec = vert2_vec
                    vert1_vec = Vector((vert1_vec.dot(u), vert1_vec.dot(v)))
                    vert2_vec = Vector((vert2_vec.dot(u), vert2_vec.dot(v)))
                    ang += vert1_vec.angle_signed(vert2_vec)
                if ang > 0.9:
                    singularities.append(vert.co)

        self.singularities = singularities

    ################################################################################################
    # @detect_singularities
    ################################################################################################
    def sample_point(self, point, ref_dir=None):
        location, normal, index, distance = self.bvh.find_nearest(point)
        if location:
            face = self.bm.faces[index]
            face_verts_co = [vert.co for vert in face.verts]
            if not ref_dir:
                ref_dir = self.field[face.verts[0].index]

            field = [
                nmv.physics.best_matching_vector(
                    nmv.physics.symmetry_space(
                        self.field[vert.index], vert.normal) if not self.hex_mode
                    else nmv.physics.hex_symmetry_space(self.field[vert.index], vert.normal),
                    reference=ref_dir
                )
                for vert in face.verts
            ]

            dir = barycentric_transform(point, *face_verts_co, *field)
            scale_curv = [Vector((self.scale[vert.index], self.curvature[vert.index], 0)) for vert in face.verts]
            scale_curv = barycentric_transform(point, *face_verts_co, *scale_curv)
            scale = scale_curv[0]
            curv = scale_curv[1]
            dir -= normal * normal.dot(dir)
            dir.normalize()
            return location, normal, dir, scale, curv
        else:
            return None, None, None, None
    '''
    ################################################################################################
    # @detect_singularities
    ################################################################################################
    def preview(self):
        draw = self.draw
        draw.blend_mode = nmv.consts.Drawing.MULTIPLY_BLEND
        draw.line_width = 1.5
        draw.point_size = 20
        draw.clear_data()

        blue = Vector((0.7, 0.7, 1, 1))
        red = Vector((1, 0, 0, 1))
        white = Vector((1, 1, 1, 1))
        for vert in self.bm.verts:
            fac = self.scale[vert.index]
            loc = vert.co
            color = numpy.array((fac ** 2, ((1 - fac) * 4 * fac), (1 - fac) ** 2, 1))
            color += 2
            color /= 3
            size = sum(edge.calc_length() for edge in vert.link_edges) / len(vert.link_edges)
            u = Vector(self.field[vert.index]) * size
            vecs = nmv.physics.symmetry_space(u, vert.normal) if not self.hex_mode else nmv.physics.hex_symmetry_space(u, vert.normal)
            for v in vecs:
                draw.add_line(loc, loc + v, color1=color, color2=white)

        for singularity in self.singularities:
            draw.add_point(singularity, red)

        draw.update_batch()
    
    ################################################################################################
    # @detect_singularities
    ################################################################################################
    def preview_fast(self):
        draw = self.draw
        draw.blend_mode = nmv.consts.Drawing.MULTIPLY_BLEND
        draw.line_width = 1
        d = self.locations - self.locations[self.walk_edges(0)]
        edge_lengths = numpy.sqrt(numpy.sum(d ** 2, axis=1))[:, numpy.newaxis]
        draw.line_coords = numpy.empty((self.number_vertices * 2, 3), dtype=numpy.float32)
        draw.line_coords[0::2] = self.locations
        draw.line_coords[1::2] = self.locations + self.field * edge_lengths * 0.5
        white = numpy.array([[1, 1, 1, 1]])
        blue = numpy.array([[0, 0, 1, 1]])
        draw.line_colors = numpy.empty((self.number_vertices * 2, 4), dtype=numpy.float32)
        draw.line_colors[0::2] = numpy.repeat(blue, [self.number_vertices], axis=0)
        draw.line_colors[1::2] = numpy.repeat(white, [self.number_vertices], axis=0)
        self.draw.update_batch()
    '''