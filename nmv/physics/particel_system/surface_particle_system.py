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

# System imports
import numpy

# Blender imports
import bmesh
from mathutils import Vector
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree

# Internal imports
import nmv.physics


####################################################################################################
# SurfaceParticleSystem
####################################################################################################
class SurfaceParticleSystem:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 mesh_object,
                 model_size=1,
                 resolution=60,
                 mask_resolution=100):

        self.triangle_mode = False
        self.particles = set()
        self.field = nmv.physics.Field(mesh_object)

        # Drawing system
        self.ignore_drawing = True
        if not self.ignore_drawing:
            self.draw = nmv.physics.DrawCallback()

        self.draw.matrix = mesh_object.matrix_world

        self.particle_size = model_size / resolution
        self.particle_size_mask = model_size / mask_resolution

        self.field_sampling_method = "RUNGE_KUTTA"

        self.grid = nmv.physics.SpatialHash(self.particle_size * 2)

    def curvature_spawn_particles(self, n=10):
        d_sqr = self.particle_size ** 2
        verts = sorted(self.field.bm.verts, key=vector_fields.average_curvature)
        for i in range(n):
            vert = verts[i]
            not_valid = False
            for particle in self.particles:
                if (vert.co - particle.co).length_squared < d_sqr:
                    not_valid = True
                    break
            if not not_valid:
                self.new_particle(vert.co)

    def gp_spawn_particles(self, context):
        r = max(self.particle_size, self.particle_size_mask)
        mat = self.field.matrix.inverted()
        frame = vector_fields.get_gp_frame(context)
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

    def propagate_particles(self, relaxation=3, factor=0.5):
        grid = self.grid
        current_front = list(self.particles)
        while len(current_front) > 0:
            yield
            new_front = []
            for particle in current_front:
                if particle.tag not in {"SHARP", "GREASE"}:
                    remove = False
                    for intruder in grid.test_sphere(particle.co, particle.radius * 1.5, exclude=(particle,)):
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
                    vecs = vector_fields.hex_symmetry_space(particle.dir, particle.normal)
                    vecs = (vecs[0], vecs[1], vecs[4])
                else:
                    vecs = vector_fields.symmetry_space(particle.dir, particle.normal)
                    vecs = (vecs[0], vecs[1], vecs[3])

                for dir in vecs:
                    try:

                        if self.field_sampling_method == "EULER":
                            location, normal, dir, s, c = self.field.sample_point(particle.co + dir * particle.radius,
                                                                                  dir)

                        elif self.field_sampling_method == "MIDPOINT":
                            location, normal, dir, s, c = self.field.sample_point(
                                particle.co + dir * particle.radius * 0.5, dir)
                            n = normal * particle.radius * 0.1 * (1 if c > 0 else -1)
                            dir = (location - particle.co + (dir * particle.radius * 0.5)).normalized()
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
                    for neighbor in grid.test_sphere(location, particle.radius * 0.7, exclude=(particle,)):
                        if not neighbor.tag in {"SHARP", "GREASE"} and not neighbor is particle.parent:
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
                location, normal, dir, s, c = self.field.sample_point(particle.co + (d * factor * particle.radius))
                if location:
                    particle.co = location
                    particle.normal = normal
                    self.grid.update(particle)
                    particle.dir = dir

                new_tree.insert(particle.co, index)
            new_tree.balance()
            tree = new_tree

            yield i

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

    def new_particle(self, location, dir=None):
        location, normal, dir, s, c = self.field.sample_point(location, dir)
        particle = Particle(location, normal, self.field.bvh)
        particle.dir = dir
        particle.radius = lerp(s, self.particle_size, self.particle_size_mask)
        self.particles.add(particle)
        self.grid.insert(particle)
        return particle

    def remove_particle(self, particle):
        self.particles.remove(particle)
        self.grid.remove(particle)
        particle.tag = "REMOVED"

    def draw_particles(self, relaxation_steps=3):
        self.draw.clear_data()
        self.draw.point_size = 8
        for particle in self.particles:
            self.draw.add_point(particle.co,
                                particle.color * (particle.tag_number / relaxation_steps))
        self.draw.update_batch()

    def create_mesh(self, bm, sharp_angle=0.52):

        bmesh.ops.triangulate(bm, faces=bm.faces)
        source_bvh = BVHTree.FromBMesh(bm)

        mask_layer = bm.verts.layers.paint_mask.verify()
        n = 5
        while True:
            subdivide_edges = []
            for edge in bm.edges:
                le = edge.calc_length()

                s = (edge.verts[0][mask_layer] + edge.verts[1][mask_layer]) / 2
                target_le = lerp(s, self.particle_size, self.particle_size_mask)
                if target_le * 0.5 <= le:
                    subdivide_edges.append(edge)
            print(len(subdivide_edges))
            print("subdivide", n)
            n -= 1
            if not subdivide_edges or n < 0:
                break
            print("subdivide")
            bmesh.ops.subdivide_edges(bm, edges=subdivide_edges, cuts=1, use_grid_fill=True, use_only_quads=True)
            bmesh.ops.triangulate(bm, faces=bm.faces, quad_method="SHORT_EDGE")
            bmesh.ops.beautify_fill(bm, edges=bm.edges, faces=bm.faces, method="AREA")
        print("done")

        # ==========================================================================================

        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        n = len(bm.verts)

        bvh = BVHTree.FromBMesh(bm)

        sharp = 20
        smooth = 10

        particles = numpy.array([particle.co for particle in self.particles], dtype=numpy.float64, ndmin=2)
        weights = numpy.array([smooth if particle.tag == "SHARP" else sharp for particle in self.particles], dtype=numpy.int8)
        locations = numpy.array([vert.co for vert in bm.verts], dtype=numpy.float64, ndmin=2)
        particles_mapping = numpy.full((n,), -1, dtype=numpy.int64)

        current_front = set()
        for i in range(len(self.particles)):
            co = particles[i]
            location, normal, index, dist = bvh.find_nearest(co)

            if location:
                vert = min(bm.faces[index].verts,
                           key=lambda v: (v.co - Vector(co)).length_squared * (
                               2 if particles_mapping[v.index] == -1 else 1))
                vert.tag = True
                particles_mapping[vert.index] = i
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
        edges = numpy.empty((n, edges_limit), dtype=numpy.int64)
        edges_count = numpy.empty((n,), dtype=numpy.int64)

        for vert in bm.verts:
            edges_count[vert.index] = min(edges_limit, len(vert.link_edges))
            for i, edge in enumerate(vert.link_edges):
                if i >= edges_limit:
                    break
                other = edge.other_vert(vert)
                edges[vert.index][i] = other.index

        ids = numpy.arange(n)
        for i in range(30):
            cols = numpy.random.randint(0, edges_limit) % edges_count
            edge_indexes = edges[ids, cols]
            edge_mappings = particles_mapping[edge_indexes]
            distance = ((particles[particles_mapping] - locations) ** 2).sum(axis=1) * weights[particles_mapping]
            edge_distance = ((particles[edge_mappings] - locations) ** 2).sum(axis=1) * weights[edge_mappings]
            particles_mapping = numpy.where(edge_distance > distance, particles_mapping, edge_mappings)

        # ==========================================================================================

        new_bm = bmesh.new()

        # ==========================================================================================

        verts = [new_bm.verts.new(co) for co in particles]
        for index, particle in enumerate(self.particles):
            if particle.tag == "SHARP":
                verts[index].tag = True

        for face in bm.faces:
            particles_indexes = set(particles_mapping[vert.index] for vert in face.verts)
            if len(particles_indexes) == 3:
                try:
                    new_bm.faces.new((verts[i] for i in particles_indexes))
                except ValueError:
                    pass
        bmesh.ops.recalc_face_normals(new_bm, faces=new_bm.faces)

        # ==========================================================================================

        for i in range(50):
            stop = True
            for vert in new_bm.verts:
                le = len(vert.link_edges)
                if le < 3:
                    new_bm.verts.remove(vert)
                    stop = False

            for edge in new_bm.edges:
                if len(edge.link_faces) < 2:
                    new_bm.edges.remove(edge)
                    stop = False
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=min(self.particle_size, self.particle_size_mask) * 0.1)
            bmesh.ops.holes_fill(new_bm, edges=new_bm.edges)
            bmesh.ops.triangulate(new_bm, faces=new_bm.faces, quad_method="SHORT_EDGE")
            if stop:
                break

        bvh_snap(source_bvh, bm.verts)

        bmesh.ops.holes_fill(new_bm, edges=new_bm.edges)
        bmesh.ops.triangulate(new_bm, faces=new_bm.faces)
        bmesh.ops.recalc_face_normals(new_bm, faces=new_bm.faces)

        # ==========================================================================================

        if sharp_angle < math.pi:
            crease = new_bm.edges.layers.crease.verify()
            for edge in new_bm.edges:
                if edge.calc_face_angle(0) > sharp_angle:
                    edge[crease] = 1.0
                    edge.seam = True

        # ==========================================================================================

        if not self.triangle_mode:
            for i in range(2):
                stop = True
                bmesh.ops.join_triangles(new_bm, faces=new_bm.faces,
                                         angle_face_threshold=3.14,
                                         angle_shape_threshold=3.14,
                                         cmp_seam=True)
                relax_topology(new_bm)
                bvh_snap(source_bvh, new_bm.verts)


        relax_topology(new_bm)
        bvh_snap(source_bvh, new_bm.verts)
        return new_bm, source_bvh
