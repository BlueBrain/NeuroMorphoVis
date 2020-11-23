# System
import numpy
import math

# Blender
import bpy
import bmesh
from itertools import product
from mathutils import Vector, Matrix, Color
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform


def get_gp_frame(context):
    frame = None
    gp = context.scene.grease_pencil
    if gp:
        if gp.layers:
            if gp.layers.active:
                if gp.layers.active.active_frame:
                    frame = gp.layers.active.active_frame
                    print(frame)
    return frame


def average_curvature(vert):
    curv = 0
    tot = 0
    for edge in vert.link_edges:
        other = edge.other_vert(vert)
        d = other.co - vert.co
        nd = other.normal - vert.normal
        curv += nd.dot(d) / d.length_squared
        tot += 1
    if not tot:
        return 0
    else:
        return curv / tot


def curvature_direction(vert):
    if vert.is_boundary:
        for edge in vert.link_edges:
            if edge.is_boundary:
                other = edge.other_vert(vert)
                d = vert.co - other.co
                return d.normalized()
    try:
        other = min((edge.other_vert(vert) for edge in vert.link_edges),
                    key=lambda v: v.normal.dot(vert.normal))
        vec = other.normal.cross(vert.normal).normalized()
        if vec.length_squared == 0:
            raise ValueError()
        return vec
    except ValueError:
        return random_tangent_vector(vert.normal)


def average_curvature(vert):
    return sum(
        (abs(edge.other_vert(vert).normal.dot(vert.normal)) for edge in vert.link_edges)) / len(
        vert.link_edges)


def random_tangent_vector(normal):
    return normal.cross(numpy.random.sample(3) - 0.5).normalized()


def vert_normal(vert):
    return vert.normal


def normalize_vectors_array(arr):
    magnitudes = numpy.sqrt((arr ** 2).sum(axis=1))
    return arr / magnitudes[:, numpy.newaxis]


def best_matching_vector(tests, reference):
    return max(tests, key=lambda v: v.dot(reference))


def best_matching_vector_unsigned(tests, reference):
    return max(tests, key=lambda v: abs(v.dot(reference)))


def best_vector_combination(vecs_a, vecs_b):
    a, b = max(product(vecs_a, vecs_b), key=lambda a: a[0].dot(a[1]))
    return a, b


def symmetry_space(vec, normal):
    vec1 = Vector(vec).cross(normal)
    vec = Vector(vec)
    return vec, vec1, -vec, -vec1


def hex_symmetry_space(vec, normal):
    x = Vector(vec)
    y = Vector(vec).cross(normal)
    e = x * 0.5 + y * 0.866025
    f = x * -0.5 + y * 0.866025
    return x, e, f, -x, -e, -f


class Field:
    def __init__(self, obj, max_adjacent=20):

        self.matrix = obj.matrix_world.copy()
        # self.draw = DrawCallback()
        # self.draw.matrix = self.matrix
        self.bm = bmesh.new()
        self.bm.from_mesh(obj.data)
        bmesh.ops.triangulate(self.bm, faces=self.bm.faces)
        self.bm.verts.ensure_lookup_table()
        self.bm.edges.ensure_lookup_table()
        self.bm.faces.ensure_lookup_table()

        self.hex_mode = False

        self.bvh = BVHTree.FromBMesh(self.bm)
        self.n = len(self.bm.verts)
        self.max_adjacent = max_adjacent
        self.singularities = []

        self.locations = numpy.array([vert.co for vert in self.bm.verts], dtype=numpy.float32)
        self.normals = numpy.zeros((self.n, 3), dtype=numpy.float32)
        self.adjacent_counts = numpy.zeros((self.n,), dtype=numpy.float32)
        self.field = numpy.zeros((self.n, 3), dtype=numpy.float64)
        self.scale = numpy.zeros((self.n,), dtype=numpy.float64)
        self.curvature = numpy.zeros((self.n,), dtype=numpy.float64)
        self.weights = numpy.ones((self.n,), dtype=numpy.float64)

        self.connectivity = numpy.zeros((self.n, max_adjacent), dtype=numpy.int64)
        mask_layer = self.bm.verts.layers.paint_mask.verify()
        for vert in self.bm.verts:
            i = vert.index
            self.field[i] = curvature_direction(vert)
            self.normals[i] = vert_normal(vert)
            self.scale[i] = vert[mask_layer]
            self.curvature[i] = average_curvature(vert)
            self.adjacent_counts[i] = min(len(vert.link_edges), max_adjacent)
            if vert.is_boundary:
                self.weights[vert.index] = 0
            for j, e in enumerate(vert.link_edges):
                if j >= max_adjacent:
                    continue
                self.connectivity[i, j] = e.other_vert(vert).index

    def initialize_from_gp(self, context):
        mat = self.matrix.inverted()
        frame = get_gp_frame(context)
        seen_verts = set()
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
                    seen_verts.add(vert)

        current_front = set()
        for vert in seen_verts:
            for edge in vert.link_edges:
                other = edge.other_vert(vert)
                if other not in seen_verts:
                    current_front.add(vert)

        while current_front:
            new_front = set()
            for vert in current_front:
                d = Vector()
                tot = 0
                for edge in vert.link_edges:
                    other = edge.other_vert(vert)
                    if other in seen_verts:
                        if not tot:
                            d = Vector(self.field[other.index])
                        else:
                            d += best_matching_vector(
                                symmetry_space(self.field[other.index], other.normal),
                                d
                            )
                        tot += 1
                    else:
                        new_front.add(other)
                        self.weights[other.index] = self.weights[vert.index] + 1
                    if tot:
                        self.field[vert.index] = d.normalized().cross(vert.normal)
            seen_verts |= current_front
            new_front -= seen_verts
            current_front = new_front
        self.weights /= self.weights.max()

    def walk_edges(self, depth=0):
        cols = numpy.arange(self.n)
        ids = numpy.random.randint(0, self.max_adjacent, (self.n,)) % self.adjacent_counts
        ids = ids.astype(numpy.int_)
        adjacent_edges = self.connectivity[cols, ids]
        for _ in range(depth):
            ids = numpy.random.randint(0, self.max_adjacent, (self.n,)) % self.adjacent_counts[
                adjacent_edges]
            ids = ids.astype(numpy.int_)
            adjacent_edges = self.connectivity[adjacent_edges, ids]
        return adjacent_edges

    def smooth(self, iterations=100, depth=3, hex_mode=False):

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
            cols = numpy.arange(self.n)
            rval = vectors[idx, cols]
            nans = numpy.isnan(rval)
            rval[nans] = 0
            return rval * (1 / (w + 1))

        if not self.hex_mode:
            for i in range(iterations):
                print(i)
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
                print(i)
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

        self.field = normalize_vectors_array(self.field)

    def autoscale(self):
        symmetry = hex_symmetry_space if self.hex_mode else symmetry_space

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

                vert2_vec = best_matching_vector(symmetry(self.field[vert2.index], vert2.normal),
                                                 vert1_vec)

                vert1_vec = Vector((vert1_vec.dot(u), vert1_vec.dot(v)))
                vert2_vec = Vector((vert2_vec.dot(u), vert2_vec.dot(v)))

                ang += vert1_vec.angle_signed(vert2_vec)
            self.scale[vert.index] = ang
        for i in range(20):
            self.scale += self.scale[self.walk_edges(0)]
            self.scale /= 2
        self.scale -= self.scale.min()
        self.scale /= self.scale.max()

    def mirror(self, axis=0):
        mirror_vec = Vector()
        mirror_vec[axis] = -1
        for vert in self.bm.verts:
            if vert.co[axis] < 0:
                mirror_co = vert.co.copy()
                mirror_co[axis] *= -1
                location, normal, vec, s, c = self.sample_point(mirror_co)
                self.field[vert.index] = vec - vec.dot(mirror_vec) * 2 * mirror_vec

    def detect_singularities(self):
        symmetry = hex_symmetry_space if self.hex_mode else symmetry_space
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
                vec1 = best_matching_vector(symmetry_cached(v1), vec0)
                v2_symmetry = symmetry_cached(v2)
                match0 = best_matching_vector(v2_symmetry, vec0)
                match1 = best_matching_vector(v2_symmetry, vec1)
                if match0.dot(match1) < 0.5:
                    singularities.append(face.calc_center_median())
        else:
            for vert in self.bm.verts:
                ang = 0
                u = random_tangent_vector(vert.normal)
                v = u.cross(vert.normal)
                last_vec = None
                for loop in vert.link_loops:
                    vert1 = loop.link_loop_next.vert
                    vert2 = loop.link_loop_next.link_loop_next.vert
                    if not last_vec:
                        vert1_vec = symmetry_cached(vert1)[0]
                    else:
                        vert1_vec = last_vec
                    vert2_vec = best_matching_vector(symmetry_cached(vert2), vert1_vec)
                    last_vec = vert2_vec
                    vert1_vec = Vector((vert1_vec.dot(u), vert1_vec.dot(v)))
                    vert2_vec = Vector((vert2_vec.dot(u), vert2_vec.dot(v)))
                    ang += vert1_vec.angle_signed(vert2_vec)
                if ang > 0.9:
                    singularities.append(vert.co)

        self.singularities = singularities

    def sample_point(self, point, ref_dir=None):
        location, normal, index, distance = self.bvh.find_nearest(point)
        if location:
            face = self.bm.faces[index]
            face_verts_co = [vert.co for vert in face.verts]
            if not ref_dir:
                ref_dir = self.field[face.verts[0].index]

            field = [
                best_matching_vector(
                    symmetry_space(
                        self.field[vert.index], vert.normal) if not self.hex_mode
                    else hex_symmetry_space(self.field[vert.index], vert.normal),
                    reference=ref_dir
                )
                for vert in face.verts
            ]

            dir = barycentric_transform(point, *face_verts_co, *field)
            scale_curv = [Vector((self.scale[vert.index], self.curvature[vert.index], 0)) for vert
                          in face.verts]
            scale_curv = barycentric_transform(point, *face_verts_co, *scale_curv)
            scale = scale_curv[0]
            curv = scale_curv[1]
            dir -= normal * normal.dot(dir)
            dir.normalize()
            return location, normal, dir, scale, curv
        else:
            return None, None, None, None


####################################################################################################
# @subdivide_split_triangles
####################################################################################################
def subdivide_split_triangles(bmesh_object):
    """
    NOTE: This implementation is based on the code of https://github.com/jeacom25b/Tesselator-1-28.

    :param bmesh_object:
        A given bmesh object to subdivide and split its triangles
    """

    # Subdivide the edges of a bmesh with a single cut
    bmesh.ops.subdivide_edges(
        bmesh_object, edges=bmesh_object.edges, cuts=1, use_grid_fill=True, smooth=True)

    # Lists to collect the data
    collapse = list()
    triangulate = set()
    visited_vertices = set()

    # For each vertex in the bmesh object
    for vertex in bmesh_object.verts:

        # If the vertex is shared within five edges to five vertices
        if len(vertex.link_faces) == 5:

            # Get the face signature
            face_signature = tuple(sorted(len(face.verts) for face in vertex.link_faces))

            # Signature must be a tuple of (3, 4, 4, 4, 4)
            if face_signature == (3, 4, 4, 4, 4):

                # For every face in the faces containing the vertex
                for face in vertex.link_faces:

                    # If the face is a triangle, i.e. must have three vertices
                    if len(face.verts) == 3:

                        # For each edge in the face
                        for edge in face.edges:

                            # Construct a set of vertices for searching
                            vertices = set(edge.verts)

                            # If this vertex has not been processed
                            if vertex not in vertices and not vertices & visited_vertices:
                                # Operate
                                visited_vertices |= vertices

                                # Add to the collapse list
                                collapse.append(edge)

                            # Add to the triangulate set
                            triangulate |= set(face for v in vertices for face in v.link_faces)

    # Triangulate the bmesh object from the built list of triangles with the SORT_EDGE method
    bmesh.ops.triangulate(bmesh_object, faces=list(triangulate), quad_method="SHORT_EDGE")

    # Collapse
    bmesh.ops.collapse(bmesh_object, edges=collapse)

    # Build the mesh by joining the triangles together
    bmesh.ops.join_triangles(bmesh_object, faces=bmesh_object.faces,
                             angle_face_threshold=3.16, angle_shape_threshold=3.16,
                             cmp_seam=True)


####################################################################################################
# @relax_topology
####################################################################################################
def relax_topology(bmesh_object):
    """
    NOTE: This implementation is based on the code of https://github.com/jeacom25b/Tesselator-1-28.

    :param bmesh_object:
    :return:
    """

    # For every vertex in the bmesh object
    for vertex in bmesh_object.verts:

        # Make sure that this vertex is not a boundary vertex
        if vertex.is_boundary:
            continue

        # Construct an average vector
        avg = Vector()

        # Get the number of edges connected to this vertex
        number_edges_connected_to_vertex = len(vertex.link_edges)
        for edge in vertex.link_edges:

            # If the edge is seam, then ignore it
            if edge.seam:
                number_edges_connected_to_vertex = 0
                break

            # Get the other edge
            other = edge.other_vert(vertex)

            # Extend the average vector
            avg += other.co

        # If the vertex is connected to 3, 5 or 0 edges, continue
        if number_edges_connected_to_vertex in (3, 5, 0):
            continue

        # Otherwise, compute the final result of the average vector
        avg /= number_edges_connected_to_vertex
        avg -= vertex.co
        avg -= vertex.normal * vertex.normal.dot(avg)

        # Update the vertex position
        vertex.co += avg * 0.5


####################################################################################################
# @straigthen_quad_topology
####################################################################################################
def straigthen_quad_topology(bmesh_object):
    """
    NOTE: This implementation is based on the code of https://github.com/jeacom25b/Tesselator-1-28.

    :param bmesh_object:
        The given bmesh object.
    """

    # For each vertex in the bmesh object
    for vertex in bmesh_object.verts:

        # Ignore boundary vertices
        if vertex.is_boundary:
            continue

        # If the vertex is connected to three edges
        if len(vertex.link_edges) == 3:

            # It is a valida candidate
            valid = True

            # For each edge connected to the vertex
            for edge in vertex.link_edges:

                # If it is a seam edge, then ignore it
                if edge.seam:
                    # It is not a valid edge, next
                    valid = False
                    break

            # If it is a valid vertex
            if valid:
                # Make new pairs
                pairs = [(e_a.other_vert(vertex).co, e_b.other_vert(vertex).co)
                         for e_a in vertex.link_edges
                         for e_b in vertex.link_edges
                         if e_a is not e_b]

                # Pick the best pair
                best_pair = min(pairs, key=lambda pair: (pair[0] - pair[1]).length_squared)

                # Update the vertex position
                vertex.co = sum(best_pair, vertex.co * 0.2) / 2.2


####################################################################################################
# @bvh_snap
####################################################################################################
def bvh_snap(bvh, vertices):
    """Snaps a given list of vertices to a given BVH.
    NOTE: This implementation is based on the code of https://github.com/jeacom25b/Tesselator-1-28.

    :param bvh:
        A given BVH to snap the vertices to.
    :param vertices:
        A list of vertices to be snapped to the given BVH.
    """

    # For every vertex in the given list
    for vertex in vertices:

        # If this vertex is a boundary one, ignore it
        if vertex.is_boundary:
            continue

        # Initially, set the proceed flag to False
        proceed = False

        # For every edge connected to the vertex
        for edge in vertex.link_edges:

            # If the edge is seam, break and go for the next vertex
            if edge.seam:
                proceed = True
                break

        # Next vertex please, no valid conditions were found
        if proceed:
            continue

        # Final vertex position, initially set to None to check if is valid or not
        final_position = None

        # Get the initial position
        start = vertex.co

        # Build a normal ray
        ray = vertex.normal

        # Get the candidate locations by casting the ray along the normal directions
        location1, normal, index, distance1 = bvh.ray_cast(start, ray)
        location2, normal, index, distance2 = bvh.ray_cast(start, -ray)

        # Get a candidate position based on the nearest vertex
        location3, normal, index, distance3 = bvh.find_nearest(vertex.co)

        # Compute the final position based on the output
        if location1 and location2:
            final_position = location2 if distance2 < distance1 else location1
        elif location1:
            final_position = location1
            if location3:
                if distance3 * 3 < distance1:
                    final_position = location3
        elif location2:
            final_position = location2
            if location3:
                if distance3 * 3 < distance2:
                    final_position = location3
        else:
            if location3:
                final_position = location3

        # Finally, if the final position is computed, then update the vertex position
        if final_position:
            vertex.co = final_position


def lerp(v, a, b):
    return (1 - v) * a + v * b


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


####################################################################################################
# SurfaceParticleSystem
####################################################################################################
class SurfaceParticleSystem:
    def __init__(self,
                 mesh_object,
                 model_size=1,
                 resolution=60,
                 mask_resolution=100):

        self.triangle_mode = False
        self.particles = set()
        self.field = Field(mesh_object)

        # self.draw = DrawCallback()
        # self.draw.matrix = obj.matrix_world

        self.particle_size = model_size / resolution
        self.particle_size_mask = model_size / mask_resolution

        self.field_sampling_method = "RUNGE_KUTTA"

        self.grid = SpatialHash(self.particle_size * 2)

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################
    def curvature_spawn_particles(self, n=10):
        d_sqr = self.particle_size * self.particle_size
        verts = sorted(self.field.bm.verts, key=average_curvature)
        for i in range(n):
            vert = verts[i]
            not_valid = False
            for particle in self.particles:
                if (vert.co - particle.co).length_squared < d_sqr:
                    not_valid = True
                    break
            if not not_valid:
                self.new_particle(vert.co)

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################
    def gp_spawn_particles(self, context):
        r = max(self.particle_size, self.particle_size_mask)
        mat = self.field.matrix.inverted()
        frame = get_gp_frame(context)
        if frame:
            for stroke in frame.strokes:
                for point in stroke.points:
                    co = mat @ point.co
                    valid = True
                    for particle in self.grid.test_sphere(co, r):
                        d = co - particle.co
                        if d.length < particle.radius:
                            valid = False
                    if valid:
                        p = self.new_particle(co)
                        p.tag = "GREASE"
                        p.color = Vector((0, 1, 0, 1))

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################
    def singularity_spawn_particles(self):
        r = max(self.particle_size, self.particle_size_mask)
        for singularity in self.field.singularities:
            valid = True
            for particle in self.grid.test_sphere(singularity, r):
                d = particle.co - singularity
                if d.length < particle.radius * 3:
                    break
            if valid:
                self.new_particle(singularity)

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################
    def sharp_edge_spawn_particles(self, source_bm, sharp_angle=0.523599):

        def sharp_particle_from_vert(vert):
            p = self.new_particle(vert.co)
            p.tag = "SHARP"
            p.normal = vert.normal
            p.dir = p.dir - p.normal * p.dir.dot(p.normal)
            p.color = Vector((0, 1, 0, 1))

        new_bm = bmesh.new()
        for edge in source_bm.edges:
            if edge.calc_face_angle(0) > sharp_angle or edge.is_boundary:
                verts = [new_bm.verts.new(vert.co) for vert in edge.verts]
                new_bm.edges.new(verts)
        bmesh.ops.remove_doubles(new_bm,
                                 verts=new_bm.verts,
                                 dist=min(self.particle_size, self.particle_size_mask) * 0.001)

        n = 10
        while True:
            subdivide = []
            for edge in new_bm.edges:
                center = (edge.verts[0].co + edge.verts[1].co) / 2
                location, normal, dir, s, c = self.field.sample_point(center)
                size = lerp(s, self.particle_size, self.particle_size_mask)
                if edge.calc_length() > size * 0.1:
                    subdivide.append(edge)
            if not subdivide or n <= 0:
                break
            n -= 1
            bmesh.ops.subdivide_edges(new_bm, edges=subdivide, cuts=1)

        for vert in new_bm.verts:
            if vert.calc_edge_angle(0) > sharp_angle or len(vert.link_edges) > 2:
                sharp_particle_from_vert(vert)

        dir = Vector(numpy.random.sample((3,))).normalized()

        for vert in sorted(new_bm.verts, key=lambda v: v.co.dot(dir)):
            location, normal, dir, s, c = self.field.sample_point(vert.co)
            size = lerp(s, self.particle_size, self.particle_size_mask)
            valid = True
            for neighbor in self.grid.test_sphere(location, radius=size):
                valid = False
                break

            if valid:
                sharp_particle_from_vert(vert)

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################
    def propagate_particles(self,
                            relaxation=3,
                            factor=0.5):

        # Get a reference to the grid
        grid = self.grid

        # A list of all the particles on the front surface
        current_front = list(self.particles)

        # If non-propagated particles still exist
        while len(current_front) > 0:

            # To visualize the result
            yield

            # A new list to collect the data
            new_front = list()

            # For every particle in the current front
            for particle in current_front:

                # Check the tag
                if particle.tag not in {"SHARP", "GREASE"}:
                    remove = False
                    for intruder in grid.test_sphere(particle.co, particle.radius * 1.5,
                                                     exclude=(particle,)):
                        avg_rad = (intruder.radius + particle.radius) * 0.5
                        dist = (intruder.co - particle.co).length
                        avg_loc = (intruder.co + particle.co) * 0.5
                        if intruder.tag in {"SHARP", "GREASE"} and dist < avg_rad * 0.7:
                            remove = True
                            break
                        elif dist < avg_rad * 0.5:
                            remove = True
                            intruder.co = avg_loc
                            break
                    if remove:
                        self.remove_particle(particle)
                        continue

                if self.triangle_mode:
                    vecs = hex_symmetry_space(particle.dir, particle.normal)
                    vecs = (vecs[0], vecs[1], vecs[4])
                else:
                    vecs = symmetry_space(particle.dir, particle.normal)
                    vecs = (vecs[0], vecs[1], vecs[3])

                for dir in vecs:
                    try:

                        if self.field_sampling_method == "EULER":
                            location, normal, dir, s, c = self.field.sample_point(
                                particle.co + dir * particle.radius,
                                dir)

                        elif self.field_sampling_method == "MIDPOINT":
                            location, normal, dir, s, c = self.field.sample_point(
                                particle.co + dir * particle.radius * 0.5, dir)
                            n = normal * particle.radius * 0.1 * (1 if c > 0 else -1)
                            dir = (location - particle.co + (
                                        dir * particle.radius * 0.5)).normalized()
                            location, normal, dir2, s, c = self.field.sample_point(
                                n + particle.co + dir * particle.radius, dir)

                        elif self.field_sampling_method == "RUNGE_KUTTA":
                            location, normal, dir1, s, c = self.field.sample_point(
                                particle.co + dir * particle.radius * 0.3, dir)
                            n = normal * particle.radius * 0.1 * (1 if c > 0 else -1)

                            location, normal, dir2, s, c = self.field.sample_point(
                                n + particle.co + dir1 * particle.radius * 0.5, dir1)

                            location, normal, dir3, s, c = self.field.sample_point(
                                n + particle.co + dir2 * particle.radius, dir2)

                            dir = (dir + 2 * dir1 + 2 * dir2 + dir)
                            n = normal * particle.radius * 0.1 * (1 if c > 0 else -1)
                            location, normal, dir, s, c = self.field.sample_point(
                                n + particle.co + dir2 * particle.radius, dir)
                    except ValueError:
                        continue

                    valid = True
                    for neighbor in grid.test_sphere(location, particle.radius * 0.7,
                                                     exclude=(particle,)):
                        if not neighbor.tag in {"SHARP",
                                                "GREASE"} and not neighbor is particle.parent:
                            # neighbor.co += location * 0.3
                            # neighbor.co /= 1.3
                            neighbor.add_location_sample(location, weight=factor)
                            grid.update(neighbor)
                        valid = False
                        break

                    if valid:
                        p = self.new_particle(location, dir)
                        radius_diff = p.radius - particle.radius
                        if abs(radius_diff) > 0.5 * particle.radius:
                            p.radius = particle.radius * 1.5 if radius_diff > 0 else particle.radius * 0.5
                        p.parent = particle
                        grid.insert(p)
                        new_front.append(p)

                location, normal, dir, _, _ = self.field.sample_point(particle.co)
                particle.co = location
                particle.normal = normal
                particle.dir = dir
                grid.update(particle)
                if particle.tag_number < relaxation:
                    new_front.append(particle)
                    particle.tag_number += 1

            current_front = new_front

        # particles = list(self.particles)
        # for particle in particles:
        #     if particle.tag not in {"SHARP", "REMOVED"}:
        #         remove = False
        #         for intruder in grid.test_sphere(particle.co, particle.radius * 0.7, exclude=(particle,)):
        #             remove = True
        #             break
        #         if remove:
        #             self.remove_particle(particle)
        #             particle.tag = "REMOVED"

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################
    def repeal_particles(self, iterations=20, factor=0.01):
        particles = list(self.particles)
        tree = KDTree(len(particles))
        for index, particle in enumerate(particles):
            tree.insert(particle.co, index)
        tree.balance()

        for i in range(iterations):
            new_tree = KDTree(len(self.particles))
            for index, particle in enumerate(particles):
                if particle.tag in {"SHARP", "GREASE"}:
                    continue

                d = Vector()

                for loc, other_index, dist in tree.find_n(particle.co, 3):
                    if dist == 0:
                        continue
                    other = particles[other_index]
                    vec = particle.co - other.co

                    d += (vec / (dist ** 3))

                    if not self.triangle_mode:
                        u = particle.dir
                        v = u.cross(particle.normal)
                        for vec in (u + v, u - v, -u + v, -u - v):
                            vec *= particle.radius
                            vec += other.co
                            vec -= particle.co
                            dist = vec.length
                            d -= vec * 0.3 / (dist ** 3)

                d.normalize()
                location, normal, dir, s, c = self.field.sample_point(
                    particle.co + (d * factor * particle.radius))
                if location:
                    particle.co = location
                    particle.normal = normal
                    self.grid.update(particle)
                    particle.dir = dir

                new_tree.insert(particle.co, index)
            new_tree.balance()
            tree = new_tree

            yield i

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################

    def mirror_particles(self, axis):
        particles = list(self.particles)
        for particle in particles:
            r = particle.radius * 0.5

            if -r * 0.7 <= particle.co[axis] <= r:
                particle.co[axis] = 0

            elif particle.co[axis] < 0:
                self.remove_particle(particle)

            else:
                mirror_co = particle.co.copy()
                mirror_co[axis] *= -1
                self.new_particle(mirror_co)

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################

    def new_particle(self, location, dir=None):
        location, normal, dir, s, c = self.field.sample_point(location, dir)
        particle = Particle(location, normal, self.field.bvh)
        particle.dir = dir
        particle.radius = lerp(s, self.particle_size, self.particle_size_mask)
        self.particles.add(particle)
        self.grid.insert(particle)
        return particle

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################

    def remove_particle(self, particle):
        self.particles.remove(particle)
        self.grid.remove(particle)
        particle.tag = "REMOVED"

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################

    def create_mesh(self,
                    bmesh_object,
                    sharp_angle=0.52,
                    subdivision_iterations=5):

        # Triangulate the bmesh object
        bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)

        # Construct the BVH of the bmesh
        source_bvh = BVHTree.FromBMesh(bmesh_object)

        # Verify the bmesh object paint mask layer
        mask_layer = bmesh_object.verts.layers.paint_mask.verify()

        # Subdivision loop
        while True:

            # Create a list of subdivided edges
            subdivide_edges = list()

            # For each edge in the bmesh object
            for edge in bmesh_object.edges:

                # Get the edge length
                edge_length = edge.calc_length()

                # Compute the center point of the edge
                center_point = 0.5 * (edge.verts[0][mask_layer] + edge.verts[1][mask_layer])

                # Interpolate to get the target edge length
                target_edge_length = lerp(center_point, self.particle_size, self.particle_size_mask)

                # The target edge length must be less than half the original edge length
                if target_edge_length * 0.5 <= edge_length:
                    subdivide_edges.append(edge)

            # Counter
            subdivision_iterations -= 1

            # Break if no more edges could be subdivided or we reach the limit
            if not subdivide_edges or subdivision_iterations < 0:
                break

            # Apply the subdivision operation from the bmesh API
            bmesh.ops.subdivide_edges(
                bmesh_object, edges=subdivide_edges, cuts=1,
                use_grid_fill=True, use_only_quads=True)

            # Construct the new faces based on the SHORT_EDGE algorithm
            bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces, quad_method="SHORT_EDGE")

            # Beauty fill to make the faces look nice
            bmesh.ops.beautify_fill(bmesh_object, edges=bmesh_object.edges,
                                    faces=bmesh_object.faces, method="AREA")

        # Update the lookup tables
        bmesh_object.verts.ensure_lookup_table()
        bmesh_object.edges.ensure_lookup_table()
        bmesh_object.faces.ensure_lookup_table()

        # Get the number of vertices of the new mesh
        number_vertices = len(bmesh_object.verts)

        # Construct the BVH of the mesh
        bvh = BVHTree.FromBMesh(bmesh_object)

        sharp = 20
        smooth = 10

        # Build the particle system assets as numpy arrays for the performance
        # Particles
        particles = numpy.array(
            [particle.co for particle in self.particles], dtype=numpy.float64, ndmin=2)

        # Weights
        weights = numpy.array(
            [smooth if particle.tag == "SHARP" else sharp for particle in self.particles],
            dtype=numpy.int8)

        # Locations from the vertices
        locations = numpy.array([vert.co for vert in bmesh_object.verts], dtype=numpy.float64,
                                ndmin=2)

        # Particles mapping
        particles_mapping = numpy.full((number_vertices,), -1, dtype=numpy.int64)

        current_front = set()

        # For each particle, or vertex, in the system
        for i in range(len(self.particles)):

            # Get its location
            co = particles[i]

            # Compute its new location, normal, index and distance from the given one
            location, normal, index, dist = bvh.find_nearest(co)

            # If the location is true
            if location:
                # Compute the vertex
                vert = min(bmesh_object.faces[index].verts,
                           key=lambda v: (v.co - Vector(co)).length_squared *
                                         (2 if particles_mapping[v.index] == -1 else 1))

                # Update the tag
                vert.tag = True

                # Update the mapping
                particles_mapping[vert.index] = i

                # Add the vertex
                current_front.add(vert)

        while current_front:
            new_front = set()
            for vert in current_front:
                for edge in vert.link_edges:
                    other = edge.other_vert(vert)
                    if not other.tag:
                        new_front.add(other)
                        particles_mapping[other.index] = particles_mapping[vert.index]
                        other.tag = True
            current_front = new_front

        edges_limit = 10
        edges = numpy.empty((number_vertices, edges_limit), dtype=numpy.int64)
        edges_count = numpy.empty((number_vertices,), dtype=numpy.int64)

        for vert in bmesh_object.verts:
            edges_count[vert.index] = min(edges_limit, len(vert.link_edges))
            for i, edge in enumerate(vert.link_edges):
                if i >= edges_limit:
                    break
                other = edge.other_vert(vert)
                edges[vert.index][i] = other.index

        ids = numpy.arange(number_vertices)
        for i in range(30):
            cols = numpy.random.randint(0, edges_limit) % edges_count
            edge_indexes = edges[ids, cols]
            edge_mappings = particles_mapping[edge_indexes]
            distance = ((particles[particles_mapping] - locations) ** 2).sum(axis=1) * weights[
                particles_mapping]
            edge_distance = ((particles[edge_mappings] - locations) ** 2).sum(axis=1) * weights[
                edge_mappings]
            particles_mapping = numpy.where(edge_distance > distance, particles_mapping,
                                            edge_mappings)

        # Create a new bmesh object
        new_bmesh_object = bmesh.new()

        verts = [new_bmesh_object.verts.new(co) for co in particles]
        for index, particle in enumerate(self.particles):
            if particle.tag == "SHARP":
                verts[index].tag = True

        for face in bmesh_object.faces:
            particles_indexes = set(particles_mapping[vert.index] for vert in face.verts)
            if len(particles_indexes) == 3:
                try:
                    new_bmesh_object.faces.new((verts[i] for i in particles_indexes))
                except ValueError:
                    pass
        bmesh.ops.recalc_face_normals(new_bmesh_object, faces=new_bmesh_object.faces)

        for i in range(50):
            stop = True
            for vert in new_bmesh_object.verts:
                le = len(vert.link_edges)
                if le < 3:
                    new_bmesh_object.verts.remove(vert)
                    stop = False

            for edge in new_bmesh_object.edges:
                if len(edge.link_faces) < 2:
                    new_bmesh_object.edges.remove(edge)
                    stop = False
            bmesh.ops.remove_doubles(bmesh_object, verts=bmesh_object.verts,
                                     dist=min(self.particle_size, self.particle_size_mask) * 0.1)
            bmesh.ops.holes_fill(new_bmesh_object, edges=new_bmesh_object.edges)
            bmesh.ops.triangulate(new_bmesh_object, faces=new_bmesh_object.faces,
                                  quad_method="SHORT_EDGE")
            if stop:
                break

        bvh_snap(source_bvh, bmesh_object.verts)

        bmesh.ops.holes_fill(new_bmesh_object, edges=new_bmesh_object.edges)
        bmesh.ops.triangulate(new_bmesh_object, faces=new_bmesh_object.faces)
        bmesh.ops.recalc_face_normals(new_bmesh_object, faces=new_bmesh_object.faces)

        # ==========================================================================================

        if sharp_angle < math.pi:
            crease = new_bmesh_object.edges.layers.crease.verify()
            for edge in new_bmesh_object.edges:
                if edge.calc_face_angle(0) > sharp_angle:
                    edge[crease] = 1.0
                    edge.seam = True

        # ==========================================================================================

        if not self.triangle_mode:
            for i in range(2):
                stop = True
                bmesh.ops.join_triangles(new_bmesh_object, faces=new_bmesh_object.faces,
                                         angle_face_threshold=3.14,
                                         angle_shape_threshold=3.14,
                                         cmp_seam=True)
                relax_topology(new_bmesh_object)
                bvh_snap(source_bvh, new_bmesh_object.verts)

        relax_topology(new_bmesh_object)
        bvh_snap(source_bvh, new_bmesh_object.verts)
        return new_bmesh_object, source_bvh


def run_algorithm(obj, context):
    field_resolution = 5000
    resolution = 60
    mask_resolution = 50
    field_sampling_method = 'EULER'
    gp_influence = 0.2

    relaxation_steps = 1
    particle_relaxation = 1.0

    repulsion_iterations = 5
    repulsion_strength = 0.05

    subdivisions = 1

    # obj = context.active_object
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    for vert in bm.verts:
        if len(vert.link_faces) < 1:
            bm.verts.remove(vert)
    bmesh.ops.holes_fill(bm, edges=bm.edges)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(obj.data)

    # DebugText.lines = ["Decimating mesh."]
    yield

    model_size = max(obj.dimensions)

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.decimate(ratio=field_resolution / len(bm.verts))
    bpy.ops.object.mode_set(mode="OBJECT")
    yield

    particle_manager = SurfaceParticleSystem(obj, model_size,
                                             resolution,
                                             mask_resolution)

    particle_manager.field_sampling_method = field_sampling_method
    particle_manager.triangle_mode = True  # (self.polygon_mode == "TRI")
    particle_manager.field.hex_mode = True  # (self.polygon_mode == "TRI")
    # particle_manager.field.draw.setup_handler()
    # particle_manager.draw.setup_handler()
    # particle_manager.field.preview_fast()
    yield

    if gp_influence > 0:
        particle_manager.field.initialize_from_gp(context)
        particle_manager.field.weights /= max(0.00000001, 1 - gp_influence)
        particle_manager.field.weights = particle_manager.field.weights.clip(0, 1)
        particle_manager.gp_spawn_particles(context)

    field_smoothing_iterations = [30, 30, 100]
    field_smoothing_depth = [100, 30, 0]

    for i in range(3):
        particle_manager.field.smooth(field_smoothing_iterations[i],
                                      field_smoothing_depth[i])

        mirror_axes = [False, False, False]
        for axis in range(3):
            if mirror_axes[axis]:
                particle_manager.field.mirror(axis)

        # DebugText.lines = ["Creating Cross Field", f"Step: {i + 1}"]
        yield

    # NOTE: we don't need to preview any thing here
    # particle_manager.field.preview()

    sharp_angle = 20 * (math.pi / 180.0)
    if sharp_angle < math.pi:
        particle_manager.sharp_edge_spawn_particles(bm, sharp_angle)

    if len(particle_manager.particles) == 0:
        particle_manager.field.detect_singularities()
        particle_manager.singularity_spawn_particles()

    if len(particle_manager.particles) == 0:
        particle_manager.curvature_spawn_particles(5)

    for i, _ in enumerate(
            particle_manager.propagate_particles(relaxation_steps,
                                                 particle_relaxation)):
        # particle_manager.draw_particles(relaxation_steps)
        # DebugText.lines = [f"Propagating particles {('.', '..', '...')[i % 3]}"]
        yield

    for i, _ in enumerate(
            particle_manager.repeal_particles(iterations=repulsion_iterations,
                                              factor=repulsion_strength)):
        # NOTE: We don't need any drawing functions
        # particle_manager.draw_particles()
        # DebugText.lines = ["Particle repulsion:",
        #                   f"Step {i + 1}"]
        yield

    for i in range(3):
        if mirror_axes[i]:
            particle_manager.mirror_particles(axis=i)
            print("Mirror")

    # NOTE: we don't ened to visualizae
    # self.particle_manager.draw_particles()

    # DebugText.lines = ["Tesselating."]
    yield

    bm, bvh = particle_manager.create_mesh(bm, sharp_angle)

    for i in range(subdivisions):
        bmesh.ops.triangulate(bm, faces=bm.faces)
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1, use_grid_fill=True)
        relax_topology(bm)
        bvh_snap(bvh, bm.verts)
    bm.to_mesh(obj.data)

    yield True

