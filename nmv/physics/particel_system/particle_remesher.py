####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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

# System
import numpy
import math

# Blender
import bpy
import bmesh

import nmv.physics


####################################################################################################
# ParticleRemesher
####################################################################################################
class ParticleRemesher:
    """

    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 field_resolution=5000,
                 resolution=60,
                 mask_resolution=50,
                 field_sampling_method='EULER',
                 gp_influence=0.2,
                 relaxation_steps=1,
                 particle_relaxation= 1.0,
                 repulsion_iterations=5,
                 repulsion_strength=0.05,
                 subdivisions=1,
                 polygon_mode='TRIANGLES'):

        self.field_resolution = field_resolution
        self.resolution = resolution
        self.mask_resolution = mask_resolution
        self.field_sampling_method = field_sampling_method
        self.gp_influence = gp_influence

        self.relaxation_steps = relaxation_steps
        self.particle_relaxation = particle_relaxation

        self.repulsion_iterations = repulsion_iterations
        self.repulsion_strength = repulsion_strength
        self.subdivisions = subdivisions
        self.polygon_mode = polygon_mode

        self.field_smoothing_iterations = [30, 30, 100]
        self.field_smoothing_depth = [100, 30, 0]
        self.mirror_axes = [False, False, False]
        self.sharp_angle = 20 * (math.pi / 180.0)

    def run(self, mesh_object, context, interactive=False):

        # Create a new bmesh from the given mesh object to improve the performance
        nmv.logger.info('Converting to BMesh')
        bmesh_object = bmesh.new()
        bmesh_object.from_mesh(mesh_object.data)

        nmv.logger.info('Cleaning the Mesh')
        # For every vertex in the bmesh if the vertex is not linked to a proper face, remove
        # it from the mesh
        for vert in bmesh_object.verts:
            if len(vert.link_faces) < 1:
                bmesh_object.verts.remove(vert)

        # Fill all the holes in the mesh
        bmesh.ops.holes_fill(bmesh_object, edges=bmesh_object.edges)

        # Triangulate the mesh
        bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)

        # Update the mesh data in the system
        bmesh_object.to_mesh(mesh_object.data)

        # Return and keep the state if interactive
        if interactive:
            yield

        # Get the dimensions of the mesh
        nmv.logger.info('Decimating')
        model_size = max(mesh_object.dimensions)

        # Switch to edit mode
        bpy.ops.object.mode_set(mode="EDIT")

        # Select all vertices
        bpy.ops.mesh.select_all(action="SELECT")

        # Decimate based in the field resolution
        bpy.ops.mesh.decimate(ratio=self.field_resolution / len(bmesh_object.verts))

        # Switch back to the object mode
        bpy.ops.object.mode_set(mode="OBJECT")

        # Return and keep the state if interactive
        if interactive:
            yield

        nmv.logger.info('Creating a Particle System')
        particle_manager = nmv.physics.SurfaceParticleSystem(
            mesh_object, model_size, self.resolution, self.mask_resolution)

        # Update its parameter
        particle_manager.field_sampling_method = self.field_sampling_method
        particle_manager.triangle_mode = True  # (self.polygon_mode == "TRI")
        particle_manager.field.hex_mode = True  # (self.polygon_mode == "TRI")

        # Draw if interactive
        '''
        if interactive:
            particle_manager.field.draw.setup_handler()
            particle_manager.draw.setup_handler()
            particle_manager.field.preview_fast()
        '''

        # Return and keep the state if interactive
        if interactive:
            yield

        # Pencil
        if self.gp_influence > 0:
            particle_manager.field.initialize_from_grease_pencil(context)
            particle_manager.field.weights /= max(0.00000001, 1 - self.gp_influence)
            particle_manager.field.weights = particle_manager.field.weights.clip(0, 1)
            particle_manager.grease_pencil_gp_spawn_particles(context)

        # Smooth
        for i in range(3):
            nmv.logger.info('Creating Cross Field [Step %d]' % i)
            particle_manager.field.smooth(
                self.field_smoothing_iterations[i], self.field_smoothing_depth[i])

            # Axis mirroring
            for axis in range(3):
                if self.mirror_axes[axis]:
                    particle_manager.field.mirror(axis)

            # Return and keep the state if interactive
            if interactive:
                yield

        # Update the view
        '''
        if interactive:
            particle_manager.field.preview()
        '''
        # The sharp angle must be less than 180 to proceed
        if self.sharp_angle < math.pi:
            nmv.logger.info('Spawning Particles')
            particle_manager.sharp_edge_spawn_particles(bmesh_object, self.sharp_angle)

        # Handling singularities
        if len(particle_manager.particles) == 0:
            nmv.logger.info('Detecting Singularities')
            particle_manager.field.detect_singularities()
            particle_manager.singularity_spawn_particles()

        if len(particle_manager.particles) == 0:
            nmv.logger.info('Curvature')
            particle_manager.curvature_spawn_particles(5)

        # Propagate the results
        for i, _ in enumerate(
                particle_manager.propagate_particles(self.relaxation_steps,
                                                     self.particle_relaxation)):
            nmv.logger.info('Propagating particles [%d]' % i)

            '''
            if interactive:
                particle_manager.draw_particles(self.relaxation_steps)
            '''

            if interactive:
                yield

        for i, _ in enumerate(
                particle_manager.repeal_particles(iterations=self.repulsion_iterations,
                                                  factor=self.repulsion_strength)):
            # NOTE: We don't need any drawing functions
            # particle_manager.draw_particles()
            # DebugText.lines = ["Particle repulsion:",
            #                   f"Step {i + 1}"]
            yield

        for i in range(3):
            if self.mirror_axes[i]:
                particle_manager.mirror_particles(axis=i)

        '''
        # Update the drawing
        if interactive:
            particle_manager.draw_particles()
        '''

        # Return and keep the state if interactive
        if interactive:
            yield

        nmv.logger.info('Tessellating')

        # Creating a new Bmesh object from the old one and a BVH
        bmesh_object, bvh = particle_manager.create_mesh(bmesh_object, self.sharp_angle)

        # QUAD triangulation
        if self.polygon_mode == "QUADS":

            # Update the mesh
            bmesh_object.to_mesh(mesh_object.data)

            # Return and keep the state if interactive
            if interactive:
                yield

            # For every subdivision
            for i in range(self.subdivisions):

                # Create a new modifier
                subdivision_modifier = context.active_object.modifiers.new(
                    type="SUBSURF", name="Subd")

                # Level 1
                subdivision_modifier.levels = 1

                # First iteration use simple and then Catmull-Clarck
                subdivision_modifier.subdivision_type = "SIMPLE" if i == 0 else "CATMULL_CLARK"

                # Apply the modifier
                bpy.ops.object.modifier_apply(modifier=subdivision_modifier.name)

                # Create a bmesh object from the current mesh in the scene
                bmesh_object = bmesh.new()
                bmesh_object.from_mesh(mesh_object.data)

                # In the first iteration
                if i == 0:

                    # MOve towards a quad topology
                    nmv.physics.straigthen_quad_topology(bmesh_object)

                    # Relax the topology
                    nmv.physics.relax_topology(bmesh_object)

                # Snap along the BVH grid
                nmv.physics.bvh_snap(bvh, bmesh_object.verts)

                # Update the mesh
                bmesh_object.to_mesh(mesh_object.data)

        # Triangles and Quads
        elif self.polygon_mode == "TRI_AND_QUADS":

            # For every subdivision iteration
            for i in range(self.subdivisions):

                # Split the mesh into triangles
                nmv.physics.subdivide_split_triangles(bmesh_object)
                # relax_topology(bmesh_object)

                # Snap along the BVH grid
                nmv.physics.bvh_snap(bvh, bmesh_object.verts)

            # Update the mesh
            bmesh_object.to_mesh(mesh_object.data)

        # Only triangles
        else:

            # For every subdivision
            for i in range(self.subdivisions):

                # Triangulate the mesh
                bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)

                # Subdivide
                bmesh.ops.subdivide_edges(
                    bmesh_object, edges=bmesh_object.edges, cuts=1, use_grid_fill=True)

                # Relax the topology
                nmv.physics.relax_topology(bmesh_object)

                # Snap along the grid
                nmv.physics.bvh_snap(bvh, bmesh_object.verts)

            # Update the mesh
            bmesh_object.to_mesh(mesh_object.data)

        # Final return
        if interactive:
            yield True

