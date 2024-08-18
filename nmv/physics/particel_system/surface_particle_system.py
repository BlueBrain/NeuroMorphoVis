####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import math

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

    ################################################################################################
    # @curvature_spawn_particles
    ################################################################################################
    def curvature_spawn_particles(self, n=10):

        d_sqr = self.particle_size * self.particle_size

        verts = sorted(self.field.bm.verts, key=nmv.physics.average_curvature)
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
    # @grease_pencil_gp_spawn_particles
    ################################################################################################
    def grease_pencil_gp_spawn_particles(self, context):
        r = max(self.particle_size, self.particle_size_mask)
        mat = self.field.matrix.inverted()
        frame = nmv.physics.get_grease_pencil_frame(context)
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
    # @singularity_spawn_particles
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
    # @sharp_edge_spawn_particles
    ################################################################################################
    def sharp_edge_spawn_particles(self,
                                   source_bm,
                                   sharp_angle=0.523599):

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
                size = nmv.physics.lerp(s, self.particle_size, self.particle_size_mask)
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
            size = nmv.physics.lerp(s, self.particle_size, self.particle_size_mask)
            valid = True
            for neighbor in self.grid.test_sphere(location, radius=size):
                valid = False
                break

            if valid:
                sharp_particle_from_vert(vert)

    ################################################################################################
    # @propagate_particles
    ################################################################################################
    def propagate_particles(self,
                            relaxation=3,
                            factor=0.5):
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
                    vecs = nmv.physics.hex_symmetry_space(particle.dir, particle.normal)
                    vecs = (vecs[0], vecs[1], vecs[4])
                else:
                    vecs = nmv.physics.symmetry_space(particle.dir, particle.normal)
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

    ################################################################################################
    # @repeal_particles
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

    ################################################################################################
    # @mirror_particles
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
    # @new_particle
    ################################################################################################
    def new_particle(self,
                     location,
                     direction=None):

        location, normal, direction, s, c = self.field.sample_point(location, direction)

        # Create a new particle
        particle = nmv.physics.Particle(location, normal, self.field.bvh)

        # Update its direction
        particle.dir = direction

        # Update its radius
        particle.radius = nmv.physics.lerp(s, self.particle_size, self.particle_size_mask)

        # Add the particle to the system
        self.particles.add(particle)

        # Insert the particle in the grid
        self.grid.insert(particle)

        # Return a reference to the particle
        return particle

    ################################################################################################
    # @remove_particle
    ################################################################################################
    def remove_particle(self,
                        particle):

        # Remove the particle from the system
        self.particles.remove(particle)

        # Remove it from the grid
        self.grid.remove(particle)

        # Update its tag
        particle.tag = "REMOVED"

    ################################################################################################
    # @draw_particles
    ################################################################################################
    def draw_particles(self, relaxation_steps=3):
        self.draw.clear_data()
        self.draw.point_size = 8
        for particle in self.particles:
            self.draw.add_point(particle.co,
                                particle.color * (particle.tag_number / relaxation_steps))
        self.draw.update_batch()

    ################################################################################################
    # @create_mesh
    ################################################################################################
    def create_mesh(self,
                    bmesh_object,
                    sharp_angle=0.52):
        """

        :param bmesh_object:
        :param sharp_angle:
        :return:
        """

        # Triangulate the faces in the bmesh object
        bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)

        # Compute the BVH of the given bmesh object
        source_bvh = BVHTree.FromBMesh(bmesh_object)

        # Verify the mask of the given bmesh object
        mask_layer = bmesh_object.verts.layers.paint_mask.verify()

        subdivision_iterations = 5
        while True:

            # A list of the subdivided edges
            subdivide_edges = list()

            # For each edge in the edges
            for edge in bmesh_object.edges:

                # Get its length
                edge_length = edge.calc_length()

                # Get the center point of the edge
                edge_center = (edge.verts[0][mask_layer] + edge.verts[1][mask_layer]) / 2.0

                # Compute the target edge length
                target_edge_length = nmv.physics.lerp(edge_center,
                                                      self.particle_size,
                                                      self.particle_size_mask)

                # Subdivide the edge and add it to the list
                if target_edge_length * 0.5 <= edge_length:
                    subdivide_edges.append(edge)

            # Adjust the counter to see if we are done or not
            subdivision_iterations -= 1
            if not subdivide_edges or subdivision_iterations < 0:
                break

            # Add the new edges in the mesh
            bmesh.ops.subdivide_edges(
                bmesh_object, edges=subdivide_edges, cuts=1,
                use_grid_fill=True, use_only_quads=True)

            # Triangulate the mesh
            bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces, quad_method="SHORT_EDGE")

            # Use the beauty method to recreate the topology of the mesh
            bmesh.ops.beautify_fill(
                bmesh_object, edges=bmesh_object.edges, faces=bmesh_object.faces, method="AREA")

        # Update the bmesh object lookup tables
        bmesh_object.verts.ensure_lookup_table()
        bmesh_object.edges.ensure_lookup_table()
        bmesh_object.faces.ensure_lookup_table()

        # A reference to the number of the vertices in the bmesh object
        number_vertices = len(bmesh_object.verts)

        # Build the BVH tree of the bmesh object
        bvh = BVHTree.FromBMesh(bmesh_object)


        sharp = 20
        smooth = 10

        # Compile a list of the particles
        particles = numpy.array(
            [particle.co for particle in self.particles], dtype=numpy.float64, ndmin=2)

        # Compile a list of weights
        weights = numpy.array(
            [smooth if particle.tag == "SHARP" else sharp for particle in self.particles],
            dtype=numpy.int8)

        # Compile a list of the locations
        locations = numpy.array(
            [vert.co for vert in bmesh_object.verts], dtype=numpy.float64, ndmin=2)

        # Particle mapping list
        particles_mapping = numpy.full((number_vertices,), -1, dtype=numpy.int64)

        # Current front surface of the mesh
        current_front = set()

        # For each particle
        for i in range(len(self.particles)):

            # Get its coordinates
            co = particles[i]

            # Find the nearest coordinate to this one in the BHV
            location, normal, index, dist = bvh.find_nearest(co)

            # If the location is valid
            if location:

                # Compute the new vertex
                vert = min(bmesh_object.faces[index].verts,
                           key=lambda v: (v.co - Vector(co)).length_squared * (
                               2 if particles_mapping[v.index] == -1 else 1))

                # Update the tag
                vert.tag = True

                # Update the particle mapping list
                particles_mapping[vert.index] = i

                # Add the new vertex to the front array
                current_front.add(vert)

        # As long as this set is filled
        while current_front:

            # An empty new set
            new_front = set()

            # For every vertex along the current front
            for vert in current_front:

                # For each edge connected to this vertex
                for edge in vert.link_edges:

                    # Get the other vertex
                    other_vertex = edge.other_vert(vert)

                    # If the tag of the other vertex is False
                    if not other_vertex.tag:

                        # Add the other vertex to the new front
                        new_front.add(other_vertex)

                        # Update the mapping
                        particles_mapping[other_vertex.index] = particles_mapping[vert.index]

                        # Update the tag
                        other_vertex.tag = True

            # Current front is the new front
            current_front = new_front

        edges_limit = 10

        # Create an array of edges
        edges = numpy.empty((number_vertices, edges_limit), dtype=numpy.int64)

        # Compute the edge counts
        edges_count = numpy.empty((number_vertices,), dtype=numpy.int64)

        # For every vertex in the bmesh object
        for vert in bmesh_object.verts:

            # Update the edges connected to this vertex
            edges_count[vert.index] = min(edges_limit, len(vert.link_edges))

            # For every edge in the edges connected to the vertex
            for i, edge in enumerate(vert.link_edges):

                # If the index is beyond the limit, break
                if i >= edges_limit:
                    break

                # Otherwise, update the connected vertex
                other_vertex = edge.other_vert(vert)
                edges[vert.index][i] = other_vertex.index

        # Create an array of the IDs
        ids = numpy.arange(number_vertices)

        # TODO: What is this?
        for i in range(30):
            cols = numpy.random.randint(0, edges_limit) % edges_count
            edge_indexes = edges[ids, cols]
            edge_mappings = particles_mapping[edge_indexes]
            distance = ((particles[particles_mapping] - locations) ** 2).sum(axis=1) * weights[particles_mapping]
            edge_distance = ((particles[edge_mappings] - locations) ** 2).sum(axis=1) * weights[edge_mappings]
            particles_mapping = numpy.where(edge_distance > distance, particles_mapping, edge_mappings)

        # Create a new bmesh that will contain the final mesh
        new_bmesh_object = bmesh.new()

        # Create the vertices list from the particles
        verts = [new_bmesh_object.verts.new(co) for co in particles]

        # For each particle in the system
        for index, particle in enumerate(self.particles):

            # Sharp particle
            if particle.tag == "SHARP":

                # Update the vertex tag to True
                verts[index].tag = True

        # For each face in the bmesh object
        for face in bmesh_object.faces:

            # Get the indices of the particles after the mapping
            particles_indexes = set(particles_mapping[vert.index] for vert in face.verts)

            # With three-particles (vertices)
            if len(particles_indexes) == 3:

                # Compile a new face in the new bmesh object
                try:
                    new_bmesh_object.faces.new((verts[i] for i in particles_indexes))
                except ValueError:
                    pass

        # Recalculate the normals of the new mesh after adding the new vertices
        bmesh.ops.recalc_face_normals(new_bmesh_object, faces=new_bmesh_object.faces)

        # Create the mesh
        for i in range(50):
            stop = True

            # For every vertex in the new bmesh object
            for vert in new_bmesh_object.verts:

                # If the vertex is connected to less than three-vertices
                if len(vert.link_edges) < 3:

                    # Remove the vertex
                    new_bmesh_object.verts.remove(vert)

                    # Do not stop the iterations
                    stop = False

            # For every edge in the new bmesh object
            for edge in new_bmesh_object.edges:

                # If the edge is connected to less than two faces
                if len(edge.link_faces) < 2:

                    # Remove the edge
                    new_bmesh_object.edges.remove(edge)

                    # Do not stop the iterations
                    stop = False

            # Remove doubles to clean the mesh
            bmesh.ops.remove_doubles(
                bmesh_object, verts=bmesh_object.verts,
                dist=min(self.particle_size, self.particle_size_mask) * 0.1)

            # Fill the holes in the new bmesh object
            bmesh.ops.holes_fill(new_bmesh_object, edges=new_bmesh_object.edges)

            # Triangulate the new bmesh object
            bmesh.ops.triangulate(
                new_bmesh_object, faces=new_bmesh_object.faces, quad_method="SHORT_EDGE")

            # If done, break the loop
            if stop:
                break

        # Snap the vertices of the bmesh object along the source BVH
        nmv.physics.bvh_snap(source_bvh, bmesh_object.verts)

        # Fill the holes in the new bmesh object
        bmesh.ops.holes_fill(new_bmesh_object, edges=new_bmesh_object.edges)

        # Triangulate the new bmesh object
        bmesh.ops.triangulate(new_bmesh_object, faces=new_bmesh_object.faces)

        # Recalculate the face normals
        bmesh.ops.recalc_face_normals(new_bmesh_object, faces=new_bmesh_object.faces)

        # If the sharp angle is less then 180
        if sharp_angle < math.pi:

            # Verify the edges
            crease = new_bmesh_object.edges.layers.crease.verify()

            # For every edge in the bmesh object
            for edge in new_bmesh_object.edges:

                # If edge with sharp angle, update the seam to True
                if edge.calc_face_angle(0) > sharp_angle:
                    edge[crease] = 1.0
                    edge.seam = True

        # If faces are not triangulated
        if not self.triangle_mode:
            for i in range(2):
                stop = True

                # Add the new triangles
                bmesh.ops.join_triangles(
                    new_bmesh_object, faces=new_bmesh_object.faces, angle_face_threshold=3.14,
                    angle_shape_threshold=3.14, cmp_seam=True)

                # Relax the topology of the bmesh object
                nmv.physics.relax_topology(new_bmesh_object)

                # Snap again along the source BVH
                nmv.physics.bvh_snap(source_bvh, new_bmesh_object.verts)

        # Relax the topology of the new bmesh object
        nmv.physics.relax_topology(new_bmesh_object)

        # Snap again
        nmv.physics.bvh_snap(source_bvh, new_bmesh_object.verts)

        # Return a reference to the new bmesh object and the source BVH
        return new_bmesh_object, source_bvh
