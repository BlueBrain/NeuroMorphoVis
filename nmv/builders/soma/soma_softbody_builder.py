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

# System imports
import random
import math
import copy

# Blender imports
import bpy

# Internal imports
import nmv.bmeshi
import nmv.consts
import nmv.enums
import nmv.geometry
import nmv.mesh
import nmv.physics
import nmv.scene
import nmv.shading
import nmv.skeleton
import nmv.utilities


####################################################################################################
# @SomaSoftBodyBuilder
####################################################################################################
class SomaSoftBodyBuilder:
    """A robust factory for reconstructing a three-dimensional profile of neuronal somata on a
    physically-plausible basis using soft body objects, Hooke's law and the physics engine of
    Blender.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology.
        :param options:
            NeuroMorphoVis options
        """

        # Morphology
        self.morphology = copy.deepcopy(morphology)

        # All the options of the project (an instance of NeuroMorphoVisOptions)
        self.options = options

        # A common vertex group used to store all the vertices that will be grouped for the hooks
        self.vertex_group = None

        # A list of all the hooks that are created to stretch the soma
        self.hooks_list = None

        # A list of all the arbors that are connected to the soma.
        self.valid_arbors = None

        # Set the initial soma radius to half of its mean radius
        self.initial_soma_radius = \
            options.soma.radius_scale_factor * morphology.soma.smallest_radius

        # Ensure the connection between the arbors and the soma
        nmv.skeleton.ops.verify_arbors_connectivity_to_soma(self.morphology)

    ################################################################################################
    # @add_noise_to_soma_surface
    ################################################################################################
    def add_noise_to_soma_surface(self,
                                  soma_mesh,
                                  delta=0.05):
        """Add some random noise of the soma surface.

        :param soma_mesh:
            A given soma mesh.
        :param delta:
            The noise delta.
        """

        # Get the connection extents
        connection_extents = nmv.skeleton.ops.get_soma_to_root_sections_connection_extent(
            self.morphology)

        for i in range(len(soma_mesh.data.vertices)):
            vertex = soma_mesh.data.vertices[i]

            if nmv.skeleton.ops.is_point_located_within_extents(vertex.co, connection_extents):
                continue

            vertex.select = True
            vertex.co = vertex.co + (vertex.normal * random.uniform(-delta / 2.0, delta / 2.0))
            vertex.select = False

    ################################################################################################
    # @get_extrusion_scale
    ################################################################################################
    def get_branch_extrusion_scale(self,
                                   arbor):
        """Compute the ratio between the radius of the arbor at the initial segment and its
        mapping on the initial ico-sphere that is used to reconstruct the soma.

        :param arbor:
            The arbor (or arbor) that we need to compute the extrusion scale for.
        :return:
            The ratio between the given soma radius and the extrusion radius of the arbor.
        """

        # Distance between the soma and initial sample of the arbor
        distance = (arbor.samples[0].point - self.morphology.soma.centroid).length

        # Compute the extrusion radius based on the arbor radius and also the soma radius
        extrusion_radius = arbor.samples[0].radius * self.initial_soma_radius / distance

        # Compute the scale factor between the two radii
        scale_factor = arbor.samples[0].radius / extrusion_radius

        # Return the computed scale factor
        return scale_factor

    ################################################################################################
    # @create_profile_point_extrusion_face
    ################################################################################################
    def create_profile_point_extrusion_face(self,
                                            initial_soma_sphere,
                                            profile_point,
                                            profile_point_index,
                                            visualize_connection=False):
        """Create a circular extrusion face on the soma sphere that corresponds to a given
        profile point.

        NOTE: This functionality helps creating more realistic somata given that the profile
        points are not intersecting.

        :param initial_soma_sphere:
            The ico-sphere that represent the initial shape of the soma.
        :param profile_point:
            A given two-dimensional profile point of the soma.
        :param profile_point_index:
            The index of the given profile point.
        :param visualize_connection:
            Add a sphere to represent the connection between the profile point and the soma.
        :return:
            The centroid of the created extrusion face.
        """

        # Compute the direction from the origin to the profile point
        direction = (profile_point - self.morphology.soma.centroid).normalized()

        # Compute the intersecting point on the soma
        profile_point_on_soma = self.initial_soma_radius * direction

        # Verify the extrusion connection by drawing a sphere at the connection point
        if visualize_connection:

            # Label the connection
            connection_id = 'connection_profile_point_%s' % (str(profile_point_index))

            # Visualize the extrusion connection
            nmv.skeleton.ops.visualize_extrusion_connection(
                point=profile_point_on_soma, radius=1.0, connection_id=connection_id)

        # Get the nearest face to the projected point on soma, subdivide it and use it for the
        # extrusion operation
        nearest_face_index = nmv.bmeshi.ops.get_nearest_face_index(
            initial_soma_sphere, profile_point_on_soma)

        # Make a subdivision for extra processing
        faces_indices = nmv.bmeshi.ops.subdivide_faces(initial_soma_sphere, [nearest_face_index])

        # Get the nearest face to the projection on soma after refinement
        nearest_face_index = nmv.bmeshi.ops.get_nearest_face_index(
            initial_soma_sphere, profile_point_on_soma)

        # Return the face centroid to be used for retrieving the face later
        # We can search the nearest face w.r.t the centroid and the results is guaranteed
        extrusion_face = nmv.bmeshi.ops.get_face_from_index(initial_soma_sphere, nearest_face_index)

        # Return the computed centroid of the extrusion face
        return extrusion_face.calc_center_median()

    ################################################################################################
    # @attach_hook_to_extrusion_face_on_profile_point
    ################################################################################################
    def attach_hook_to_extrusion_face_on_profile_point(self,
                                                       initial_soma_sphere,
                                                       profile_point,
                                                       profile_point_index,
                                                       use_face=True):
        """Attach a Blender hook on the extrusion face that corresponds to a profile point.

        :param initial_soma_sphere:
            The ico-sphere that represent the initial shape of the soma.
        :param profile_point:
            A given two-dimensional profile point of the soma.
        :param profile_point_index:
            The index of the given profile point.
        :param use_face:
            If this flag is set, we will use a full face for extruding the profile point.
        """

        # Attach a full face for extruding a profile point
        if use_face:

            # Get the face index near to the profile point
            face_index = nmv.mesh.ops.get_index_of_nearest_face_to_point(
                initial_soma_sphere, profile_point)

            # Get a reference to the face itself from its index
            face = initial_soma_sphere.data.polygons[face_index]

            # Get all the vertices of the face
            vertices_indices = face.vertices[:]

            # Get the face center
            face_center = face.center

        # Attach a single vertex
        else:

            # Get the index of a single vertex that is close to the profile point
            vertex_index = nmv.mesh.ops.get_index_of_nearest_vertex_to_point(
                initial_soma_sphere, profile_point)

            # Use the only vertex we use in a list
            vertices_indices = [vertex_index]

            # Assume that the face center is the vertex coordinate
            face_center = initial_soma_sphere.data.vertices[vertex_index].co

        # Compute the hook points (initial and terminal)
        point_0 = face_center + face_center.normalized() * 0.01
        point_1 = profile_point

        # add the vertices to the existing vertex group
        nmv.mesh.ops.add_vertices_to_existing_vertex_group(vertices_indices, self.vertex_group)

        # create the hook and attach it to the vertices
        hook = nmv.physics.hook.ops.add_hook_to_vertices(
            initial_soma_sphere, vertices_indices, name='hook_%d' % profile_point_index)

        # the hook should be stretched from the center of the face to the arbor
        # initial segment point
        # set the hook positions at the different key frames
        nmv.physics.hook.ops.locate_hook_at_keyframe(hook, point_0, 1)
        nmv.physics.hook.ops.locate_hook_at_keyframe(hook, point_1, 50)

        # add the hook to the hooks list
        self.hooks_list.append(hook)

    ################################################################################################
    # @build_soma_based_on_profile_points_only
    ################################################################################################
    def build_soma_based_on_profile_points_only(self,
                                                apply_shader=True):
        """Reconstruct a three-dimensional profile of the soma based on the profile points only.

        This function is quite helpful for testing the reconstructed projection with the profile
        of the soma.

        :param apply_shader:
            Apply the given soma shader in the configuration. This flag will be set to False when
            the soma is created in another builder such as the skeleton builder or the piecewise
            mesh builder.
        :return:
            A reference to the reconstructed soma.
        """

        # Log
        nmv.logger.header('Building soma using Profile Point only')

        # Create a ico-sphere 'bmesh' to represent the initial shape of the soma
        initial_soma_sphere_bmesh = nmv.bmeshi.create_ico_sphere(
            radius=self.initial_soma_radius, location=self.morphology.soma.centroid,
            subdivisions=self.options.soma.subdivision_level)

        # NOTE: The face extrusion process requires two lists to proceed, the first keeps the
        # centers of all the faces that will be extruded and the other keeps the valid profile
        # points that do NOT intersect

        # Initialize an array to keep track on the centers of the extruded faces
        faces_centers = list()

        # Initialize a list to keep track on the valid profile points
        valid_profile_points = list()

        # Iterate on every profile point available from the soma information to validate it
        nmv.logger.info('Verifying profile points intersection')
        for i, profile_point in enumerate(self.morphology.soma.profile_points):

            # Check if the profile point intersects with other points in the list or not
            if nmv.skeleton.ops.profile_point_intersect_other_point(
                    profile_point, i, self.morphology.soma.profile_points,
                    self.initial_soma_radius):

                # Report the intersection
                nmv.logger.detail("WARNING: Profile point [%d] intersection" % i)

                # Next point
                continue

            # Otherwise, we can consider the profile point valid and append it to the list
            valid_profile_points.append(profile_point)

            # Get the center of the face that is created for the profile point
            nmv.logger.detail("Profile point [%d] is valid" % i)
            face_center = self.create_profile_point_extrusion_face(
                initial_soma_sphere_bmesh, profile_point, i)

            # Append the face to the list
            faces_centers.append(face_center)

        # Link the soma sphere bmesh to the scene using a mesh object
        soma_sphere_mesh = nmv.bmeshi.ops.link_to_new_object_in_scene(
            initial_soma_sphere_bmesh, nmv.consts.Skeleton.SOMA_PREFIX)

        # Create a vertex group to link all the vertices of the extrusion faces to it
        self.vertex_group = nmv.mesh.ops.create_vertex_group(soma_sphere_mesh)

        # Create a hook list to be able to delete all the hooks after finishing the simulation
        self.hooks_list = list()

        for i, face_centroid in enumerate(faces_centers):
            self.attach_hook_to_extrusion_face_on_profile_point(
                soma_sphere_mesh, valid_profile_points[i], i)

        # Set the time-line to zero
        bpy.context.scene.frame_set(0)

        # Apply the soft body operation on the mesh
        nmv.physics.soft_body.ops.apply_soft_body_to_object(
            soma_sphere_mesh, self.vertex_group, self.options.soma)

        # Apply the soma shader directly to the soft body object, otherwise create the soma here
        # and apply the material later.
        if apply_shader:

            # Create the soma material and assign it to the ico-sphere
            soma_material = nmv.shading.create_material(
                name='soma_material', color=self.options.shading.soma_color,
                material_type=self.options.shading.soma_material)

            # Apply the shader to the ico-sphere
            nmv.shading.set_material_to_object(
                mesh_object=soma_sphere_mesh, material_reference=soma_material)

            # Create an illumination specific for the given material
            nmv.shading.create_material_specific_illumination(self.options.shading.soma_material)

        # Return a reference to the reconstructed soma mesh
        return soma_sphere_mesh

    ################################################################################################
    # @create_branch_extrusion_face
    ################################################################################################
    def create_branch_extrusion_face(self,
                                     initial_soma_sphere,
                                     arbor,
                                     visualize_connection=False):
        """Build a connecting extrusion face for emanating the arbor from the soma.

        This function returns the centroid of the face to be a basis for building the arbor
        itself later and attaching it to the soma.

        :param initial_soma_sphere:
            The ico-sphere that represent the initial shape of the soma.
        :param arbor:
            The arbor where the extrusion will happen.
        :param visualize_connection:
            Add a sphere to represent the connection between the arbor and the soma.
        :return:
            The centroid of the created extrusion face.
        """

        # Compute the direction from the origin to the branching point
        connection_direction = (arbor.samples[0].point - self.morphology.soma.centroid).normalized()

        # Compute the intersecting point on the soma and the difference between that on the soma
        # and that on the arbor starting point
        connection_point_on_soma = self.morphology.soma.centroid + connection_direction * self.initial_soma_radius

        # Compute the extrusion radius that will be applied on the soma_sphere
        distance_to_soma = (arbor.samples[0].point - self.morphology.soma.centroid).length
        scale_factor = self.initial_soma_radius / distance_to_soma
        extrusion_radius = arbor.samples[0].radius * scale_factor

        # Create a reference circle for reshaping the connection cross section to a clean shape,
        # for instance a circle approximation
        connection_circle = nmv.bmeshi.create_circle(
            radius=extrusion_radius, location=connection_point_on_soma, vertices=32)

        # Verify the extrusion connection by drawing a sphere at the connection point
        if visualize_connection:

            # Label the connection
            connection_id = 'connection_%s_%s' % (arbor.type, str(arbor.index))

            # Plot a sphere at the connection point if requested
            nmv.skeleton.ops.visualize_extrusion_connection(
                point=connection_point_on_soma, radius=extrusion_radius,
                connection_id=connection_id)

        # The connection rotation target is mandatory to point the connection circle to it, then
        # compute it and rotate the face towards it
        connection_rotation_target = connection_point_on_soma + connection_direction * 0.1
        nmv.bmeshi.ops.rotate_face_from_center_to_point(
            connection_circle, 0, connection_rotation_target)

        # Select the vertices that intersect with the extrusion sphere to prepare the face for
        # the extrusion process
        faces_indices = nmv.bmeshi.ops.get_indices_of_faces_intersecting_sphere(
            initial_soma_sphere, connection_point_on_soma, extrusion_radius)

        # Get the actual intersecting faces via their indices (this is for smoothing)
        faces_indices = nmv.bmeshi.ops.get_indices_of_faces_fully_intersecting_sphere(
            initial_soma_sphere, connection_point_on_soma, extrusion_radius)

        # If we did not get any faces from the previous operation, then try to get the nearest face
        # This case might happen when the arbor is very thin and cannot map to more than one face
        if len(faces_indices) < 1:

            # Get the nearest face, subdivide it and use it
            nearest_face_index = nmv.bmeshi.ops.get_nearest_face_index(
                initial_soma_sphere, connection_point_on_soma)

            # Make a subdivision for extra processing for the obtained face
            faces_indices = nmv.bmeshi.ops.subdivide_faces(
                initial_soma_sphere, [nearest_face_index], cuts=2)

        # Merge the selected faces into a single face that will be used for the extrusion
        extrusion_face_index = nmv.bmeshi.ops.merge_faces_into_one_face(
            initial_soma_sphere, faces_indices)

        # Map the face to a reference connection circle
        nmv.bmeshi.ops.convert_face_to_circle(
            initial_soma_sphere, extrusion_face_index, connection_point_on_soma, extrusion_radius)

        # Return face centroid to be used for retrieving the face later
        # we can search the nearest face w.r.t the centroid and the results is guaranteed
        extrusion_face = nmv.bmeshi.ops.get_face_from_index(
            initial_soma_sphere, extrusion_face_index)

        # Store the index of the face to the arbor to use it later for the extrusion
        arbor.soma_face_index = extrusion_face_index
        arbor.soma_face_centroid = extrusion_face.calc_center_median()

        # Return the computed centroid of the extrusion face
        return extrusion_face.calc_center_median()

    ################################################################################################
    # @attach_hook_to_extrusion_face
    ################################################################################################
    def attach_hook_to_extrusion_face(self,
                                      initial_soma_sphere,
                                      arbor,
                                      extrusion_face_centroid,
                                      extrusion_scale):
        """Attache a hook to the extrusion face and locate it at the different keyframes.

        :param initial_soma_sphere:
            The initial spehere used to represent the soma.
        :param arbor:
            A given arbor to create the extrusion face.
        :param extrusion_face_centroid:
            The centroid of the extrusion face.
        :param extrusion_scale:
            The extrusion scale to scale the face after its extrusion.
        """

        # Search for the extrusion face by getting the nearest face in the soma sphere object to
        # the given centroid point
        face_index = nmv.mesh.ops.get_index_of_nearest_face_to_point(
            initial_soma_sphere, extrusion_face_centroid)
        face = initial_soma_sphere.data.polygons[face_index]

        # Retrieve a list of all the vertices of the face
        vertices_indices = face.vertices[:]

        # Get the center of the extrusion face
        face_center = face.center

        # Compute the initial and the last points
        point_0 = face_center + face_center.normalized() * 0.01
        point_1 = arbor.samples[0].point

        # Start with a little bit of offset for bridging the arbor with the soma directly
        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            point_1 = point_1 - point_1.normalized() * nmv.consts.Skeleton.SOMA_EXTRUSION_DELTA

        # Add the vertices to the existing vertex group
        nmv.mesh.ops.add_vertices_to_existing_vertex_group(vertices_indices, self.vertex_group)

        # Create the hook and attach it to the vertices
        hook = nmv.physics.hook.ops.add_hook_to_vertices(
            initial_soma_sphere, vertices_indices, name='hook_%d' % arbor.index)

        # The hook is stretched from the center of the face to the arbor initial segment point
        # Set the hook positions at the different key frames
        nmv.physics.hook.ops.locate_hook_at_keyframe(hook, point_0, 1)
        nmv.physics.hook.ops.scale_hook_at_keyframe(hook, 1, 1)
        nmv.physics.hook.ops.locate_hook_at_keyframe(hook, point_1, 50)
        nmv.physics.hook.ops.scale_hook_at_keyframe(hook, 1, 50)

        # The hooks is scaled between 50 and 60
        nmv.physics.hook.ops.scale_hook_at_keyframe(hook, extrusion_scale, 60)

        # Add the hook to the hooks list
        self.hooks_list.append(hook)

        # Return index of the extrusion face to be used later for arbor extrusion
        return face_index

    ################################################################################################
    # @subdivide_sphere_at_extrusion_points
    ################################################################################################
    def subdivide_at_extrusion_point(self,
                                     soma_bmesh_sphere,
                                     arbor):
        """Makes initial subdivision of the initial soma sphere at the extrusion points of the
        a given arbor to increase the accuracy when performing the pulling operation.

        :param soma_bmesh_sphere:
            The initial sphere that represents the soma.
        :param arbor:
            The initial section of a given arbor.
        """

        # Compute the direction from the origin to the branching point
        connection_direction = (arbor.samples[0].point - self.morphology.soma.centroid).normalized()

        # Compute the intersecting point on the soma and the difference between that on the soma
        # and that on the arbor starting point
        distance_to_soma = connection_direction * self.initial_soma_radius
        connection_point_on_soma = self.morphology.soma.centroid + distance_to_soma

        # Compute the extrusion radius that will be applied on the soma_sphere
        distance_to_soma = (arbor.samples[0].point - self.morphology.soma.centroid).length
        scale_factor = self.initial_soma_radius / distance_to_soma
        extrusion_radius = arbor.samples[0].radius * scale_factor

        # Select the vertices that intersect with the extrusion sphere to prepare the face for
        # the extrusion process
        faces_indices = nmv.bmeshi.ops.get_indices_of_faces_intersecting_sphere(
            soma_bmesh_sphere, connection_point_on_soma, extrusion_radius)

        # Make a subdivision for extra processing, if the topology is not required to be preserved
        nmv.bmeshi.ops.subdivide_faces(soma_bmesh_sphere, faces_indices, cuts=2)

    ################################################################################################
    # @build_soma_soft_body
    ################################################################################################
    def build_soma_soft_body(self,
                             use_profile_points=False,
                             apply_shader=True):
        """Build the soma based on soft-body simulation and Hooke's law.

        The building process ASSUMES non-overlapping and too faraway branches.

        :param use_profile_points:
            Integrate the effect of extruding towards the profile points as well.
        :param apply_shader:
            Apply the given soma shader in the configuration. This flag will be set to False when
            the soma is created in another builder such as the skeleton builder or the piecewise
            mesh builder.
        :return
            The soft body object after the deformation. This object will be used later to build
            the soma mesh.
        """

        # Log
        nmv.logger.header('Soma reconstruction with SoftBody')

        # Get a list of valid arbors where we can pull the sphere towards without being intersecting
        self.valid_arbors = nmv.skeleton.get_connected_arbors_to_soma_after_verification(
            morphology=self.morphology, soma_center=self.morphology.soma.centroid,
            soma_radius=self.initial_soma_radius)

        # Create a ico-sphere bmesh to represent the starting shape of the soma
        soma_bmesh_sphere = nmv.bmeshi.create_ico_sphere(
            radius=self.initial_soma_radius, location=self.morphology.soma.centroid,
            subdivisions=self.options.soma.subdivision_level)

        # subdivide the extrusion faces around the valid arbors
        for arbor in self.valid_arbors:
            self.subdivide_at_extrusion_point(soma_bmesh_sphere, arbor)

        # Keep a list of all the extrusion face centroids, for later
        roots_and_faces_centroids = []

        # Re-classify the arbors to be able to deal with the selectivity
        valid_apical_dendrites = list()
        valid_basal_dendrites = list()
        valid_axons = list()

        for arbor in self.valid_arbors:
            if arbor.is_axon():
                valid_axons.append(arbor)
            elif arbor.is_apical_dendrite():
                valid_apical_dendrites.append(arbor)
            else:
                valid_basal_dendrites.append(arbor)

        # Apical dendrites
        if not self.options.morphology.ignore_apical_dendrites:

            # Build towards the apical dendrite, if the apical dendrite is available
            if len(valid_apical_dendrites) > 0:

                # THe branching order must be greater than zero
                if self.options.morphology.apical_dendrite_branch_order > 0:

                    # Build towards the dendrites, if possible
                    for arbor in valid_apical_dendrites:
                        nmv.logger.detail(arbor.label)

                        # Create the extrusion face, where the pulling will occur
                        extrusion_face_centroid = self.create_branch_extrusion_face(
                            soma_bmesh_sphere, arbor, visualize_connection=False)

                        # Update the list
                        roots_and_faces_centroids.append([arbor, extrusion_face_centroid])

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Build towards the basal dendrites, if the basal dendrites are available
            if len(valid_basal_dendrites) > 0:

                # THe branching order must be greater than zero
                if self.options.morphology.basal_dendrites_branch_order > 0:

                    # Build towards the dendrites, if possible
                    for arbor in valid_basal_dendrites:
                        nmv.logger.detail(arbor.label)

                        # Create the extrusion face, where the pulling will occur
                        extrusion_face_centroid = self.create_branch_extrusion_face(
                            soma_bmesh_sphere, arbor, visualize_connection=False)

                        # Update the list
                        roots_and_faces_centroids.append([arbor, extrusion_face_centroid])

        # Axons
        if not self.options.morphology.ignore_axons:

            # Build towards the axons, if the axon is available
            if len(valid_axons) > 0:

                # THe branching order must be greater than zero
                if self.options.morphology.axon_branch_order > 0:

                    # Build towards the dendrites, if possible
                    for arbor in valid_axons:
                        nmv.logger.detail(arbor.label)

                        # Create the extrusion face, where the pulling will occur
                        extrusion_face_centroid = self.create_branch_extrusion_face(
                            soma_bmesh_sphere, arbor, visualize_connection=False)

                        # Update the list
                        roots_and_faces_centroids.append([arbor, extrusion_face_centroid])

        # Pull towards the profile points as well if requested
        valid_profile_points = list()
        if use_profile_points:

            # NOTE: The face extrusion process requires two lists to proceed, the first keeps the
            # centers of all the faces that will be extruded and the other keeps the valid profile
            # points that do NOT intersect

            # Initialize an array to keep track on the centers of the extruded faces
            faces_centers = list()

            # Iterate on every profile point available from the soma information to validate it
            nmv.logger.info('Verifying profile points intersection')
            for i, point in enumerate(self.morphology.soma.profile_points):

                # Check if the profile point intersects with other points in the list or not
                if nmv.skeleton.ops.profile_point_intersect_other_point(
                        point, i, self.morphology.soma.profile_points, self.initial_soma_radius):

                    # Report the intersection
                    nmv.logger.detail("WARNING: Profile point [%d] intersection" % i)

                    # Next point
                    continue

                # Verify no intersection with the valid apical dendrites
                if not self.options.morphology.ignore_apical_dendrites:
                    if len(valid_apical_dendrites) > 0:
                        intersect = False
                        for arbor in valid_basal_dendrites:
                            if nmv.skeleton.ops.point_branch_intersect(
                                    point, arbor, self.initial_soma_radius):
                                intersect = True

                        # Next point
                        if intersect:
                            continue

                # Verify no intersection with the valid basal dendrites
                if not self.options.morphology.ignore_basal_dendrites:
                    if len(valid_basal_dendrites) > 0:
                        intersect = False
                        for arbor in valid_basal_dendrites:
                            if nmv.skeleton.ops.point_branch_intersect(
                                    point, arbor, self.initial_soma_radius):
                                intersect = True

                        # Next point
                        if intersect:
                            continue

                # Verify no intersection with the valid axons
                if not self.options.morphology.ignore_axons:
                    if len(valid_axons) > 0:
                        intersect = False
                        for arbor in valid_axons:
                            if nmv.skeleton.ops.point_branch_intersect(
                                    point, arbor, self.initial_soma_radius):
                                intersect = True

                        # Next point
                        if intersect:
                            continue

                # Otherwise, we can consider the profile point valid and append it to the list
                valid_profile_points.append(point)

                # Get the center of the face that is created for the profile point
                nmv.logger.detail("Profile point [%d] is valid" % i)
                face_center = self.create_profile_point_extrusion_face(soma_bmesh_sphere, point, i)

                # Append the face to the list
                faces_centers.append(face_center)

        """ Physics """
        # Link the soma sphere to the scene
        soma_sphere_object = nmv.bmeshi.ops.link_to_new_object_in_scene(
            soma_bmesh_sphere, nmv.consts.Skeleton.SOMA_PREFIX)

        # Create a vertex group to link all the vertices of the extrusion faces to it
        self.vertex_group = nmv.mesh.ops.create_vertex_group(soma_sphere_object)

        # Create a hooks list to be able to delete all the hooks after finishing the simulation
        self.hooks_list = list()

        # Create a list to keep track on the indices of the vertices of the extruded faces
        extrusion_faces_vertices_indices = list()

        # Create a list to keep track on the indices of the extruded faces
        faces_indices = list()

        # Attach the hooks to the faces that correspond to the branches
        for root_and_face_center in roots_and_faces_centroids:

            # Get the arbor
            arbor = root_and_face_center[0]

            # Get the center of the face
            face_centroid = root_and_face_center[1]

            # Get the indices of the faces
            face_index = nmv.mesh.ops.get_index_of_nearest_face_to_point(
                soma_sphere_object, face_centroid)

            # Get a reference to the face
            face = soma_sphere_object.data.polygons[face_index]

            # Get a list of the indices of the vertices of the face
            vertices_indices = face.vertices[:]

            # Append to the list
            extrusion_faces_vertices_indices.extend(vertices_indices)

            # Get the extrusion scale
            extrusion_scale = self.get_branch_extrusion_scale(arbor)

            # Attach hook to an extrusion face
            face_index = self.attach_hook_to_extrusion_face(
                soma_sphere_object, arbor, face_centroid, extrusion_scale)

            # Append the face index to the list
            faces_indices.append(face_index)

        for i, profile_point in enumerate(valid_profile_points):
            # Attach hook to the profile point
            self.attach_hook_to_extrusion_face_on_profile_point(
                soma_sphere_object, profile_point, i)

        # Set the time-line to zero
        bpy.context.scene.frame_set(0)

        # Apply the soft body operation
        nmv.physics.ops.apply_soft_body_to_object(
            soma_sphere_object, self.vertex_group, self.options.soma)

        # Apply the soma shader directly to the soft body object, otherwise create the soma here
        # and apply the material later.
        if apply_shader:

            # Create the soma material and assign it to the ico-sphere
            soma_material = nmv.shading.create_material(
                name=nmv.consts.Skeleton.SOMA_PREFIX, color=self.options.shading.soma_color,
                material_type=self.options.shading.soma_material)

            # Apply the shader to the ico-sphere
            nmv.shading.set_material_to_object(
                mesh_object=soma_sphere_object, material_reference=soma_material)

            # Create an illumination specific for the given material
            nmv.shading.create_material_specific_illumination(
                self.options.shading.soma_material)

        # Return a reference to the reconstructed soma
        return soma_sphere_object

    ################################################################################################
    # @build_soma_mesh_from_soft_body_object
    ################################################################################################
    def build_soma_mesh_from_soft_body_object(self,
                                              soft_body_object):
        """The soma is reconstructed in two steps. The first builds the soft body object and then
        the mesh is obtained by converting the soft body object into a watertight mesh.

        This function assumes that the soft body object was created in a previous step and
        converts this object into a mesh.

        :param soft_body_object:
            A soft body object that reflects the profile of the soma.
        :return:
            A reference to the soma mesh.
        """

        # Convert the object to a mesh
        soma_mesh = nmv.scene.ops.convert_object_to_mesh(soft_body_object)

        # Delete the vertex group (physics)
        soma_mesh.vertex_groups.remove(self.vertex_group)

        # Delete the hooks (physics)
        nmv.scene.ops.delete_list_objects(self.hooks_list)

        # Smoothing the soma via shade smoothing
        nmv.mesh.ops.shade_smooth_object(soma_mesh)

        # Return the reconstructed soma object
        return soma_mesh

    ################################################################################################
    # @reconstruct_soma_mesh
    ################################################################################################
    def reconstruct_soma_mesh(self,
                              apply_shader=True,
                              add_noise_to_surface=True):
        """Reconstructs the mesh of the soma of the neuron in a single step.

        :param apply_shader:
            Apply the given soma shader in the configuration. This flag will be set to False when
            the soma is created in another builder such as the skeleton builder or the piecewise
            mesh builder.
        :param add_noise_to_surface:
            Adds noise to the soma surface to make it much more realistic.
        :return:
            A reference to the reconstructed mesh of the soma.
        """

        # Build the soft body of the soma
        soma_soft_body = self.build_soma_soft_body(apply_shader=apply_shader)

        # Update the frame based on the soft body simulation
        for frame_index in range(0, self.options.soma.simulation_steps):

            # Set the frame index
            bpy.context.scene.frame_set(frame_index)

            # Update the progress shell
            nmv.utilities.show_progress(
                '* Simulation ', frame_index, self.options.soma.simulation_steps)

        # Report process done
        nmv.utilities.show_progress(
            '* Simulation ', self.options.soma.simulation_steps, self.options.soma.simulation_steps,
            done=True)

        # Build the soma mesh from the soft body object after deformation
        reconstructed_soma_mesh = self.build_soma_mesh_from_soft_body_object(soma_soft_body)

        # Add noise to the soma surface to make it more realistic
        if add_noise_to_surface:
            self.add_noise_to_soma_surface(reconstructed_soma_mesh)

        # Return a reference to the reconstructed soma
        return reconstructed_soma_mesh

    ################################################################################################
    # @remove_vertices_within_arbor_initial_segment
    ################################################################################################
    def remove_vertices_within_arbor_initial_segment(self,
                                                     mesh_object,
                                                     radius_scale=1.0,
                                                     angle=25):
        """Removes the vertices that are located around the initial segments of the arbors to
        make a smooth transition along the arbors when using the soft-body somata with the
        MetaBuilder.

        :param mesh_object:
            A given mesh object that should represent the reconstructed soma.
        :param radius_scale:
            The scale of the radius to avoid destroying the extrusion faces.
        :param angle:
            The angle in degrees between the normal of the connection face and the vertices to be
            deleted, by default 25.
        :return
            Returns the valid arbors that are connected to the soma.
        """

        # Check if the valid arbors are there or not
        if self.valid_arbors is None:
            self.valid_arbors = nmv.skeleton.get_connected_arbors_to_soma_after_verification(
                morphology=self.morphology, soma_center=self.morphology.soma.centroid,
                soma_radius=self.initial_soma_radius)

        # Select the mesh object
        nmv.scene.select_object(mesh_object)

        # Compose a list of the indices of the vertices that will be deleted
        vertices_indices = list()

        # For every valid arbor
        for arbor in self.valid_arbors:

            # For each vertex in the mesh object
            for vertex in mesh_object.data.vertices:

                # Check if the vertex is inside the sphere or not
                if nmv.geometry.is_point_inside_sphere(
                        arbor.samples[0].point, arbor.samples[0].radius * radius_scale, vertex.co):

                    # Compute the angle between the normals
                    angle_between_vertex_normal_and_face_normal = math.degrees(
                        arbor.samples[0].point.normalized().angle(vertex.normal))

                    # If the angle is less than the given, then add it to the list
                    if angle_between_vertex_normal_and_face_normal < angle:
                        vertices_indices.append(vertex.index)

        # Remove the vertices from the mesh
        nmv.mesh.remove_vertices(mesh_object=mesh_object, vertices_indices=vertices_indices)

        # Return a list of the valid arbors that are connected to the soma.
        return self.valid_arbors

    ################################################################################################
    # @remove_faces_within_arbor_initial_segment
    ################################################################################################
    def remove_faces_within_arbor_initial_segment(self,
                                                  mesh_object,
                                                  radius_scale=1.0,
                                                  angle=25):
        """Removes the faces that are located around the initial segments of the arbors to
        make a smooth transition along the arbors when using the soft-body somata with the
        MetaBuilder.

        :param mesh_object:
            A given mesh object that should represent the reconstructed soma.
        :param radius_scale:
            The scale of the radius to avoid destroying the extrusion faces.
        :param angle:
            The angle in degrees between the normal of the connection face and the vertices to be
            deleted, by default 25.
        :return
            Returns the valid arbors that are connected to the soma.
        """

        # Check if the valid arbors are there or not
        if self.valid_arbors is None:
            self.valid_arbors = nmv.skeleton.get_connected_arbors_to_soma_after_verification(
                morphology=self.morphology, soma_center=self.morphology.soma.centroid,
                soma_radius=self.initial_soma_radius)

        # Select the mesh object
        nmv.scene.select_object(mesh_object)

        # Deselect all the vertices in the mesh
        nmv.mesh.deselect_all_vertices(mesh_object)

        # For every valid arbor
        for arbor in self.valid_arbors:

            # For every face in the mesh
            for face in mesh_object.data.polygons.values():

                # Check if the vertex is inside the sphere or not
                if nmv.geometry.is_point_inside_sphere(
                        arbor.samples[0].point, arbor.samples[0].radius, face.center):

                    # Compute the angles between the normals
                    angle_between_normals = arbor.samples[0].point.normalized().angle(face.normal)

                    # If the angle is less than the given one, select the face
                    if math.degrees(angle_between_normals) < angle:
                        face.select = True

        # Switch to edit mode
        bpy.ops.object.editmode_toggle()

        # Delete the selected face
        bpy.ops.mesh.delete(type='FACE')

        # Switch back to the object more
        bpy.ops.object.editmode_toggle()

        # Return a reference to the valid arbors that are connected to the soma
        return self.valid_arbors

    ################################################################################################
    # @reconstruct_soma_profile_mesh
    ################################################################################################
    def reconstruct_soma_profile_mesh(self,
                                      apply_shader=True):
        """Reconstruct the mesh of the soma of the neuron in a single step based on the profile
        points only.

        :param apply_shader:
            Apply the given soma shader in the configuration. This flag will be set to False when
            the soma is created in another builder such as the skeleton builder or the piecewise
            mesh builder.
        :return:
            A reference to the reconstructed mesh of the soma.
        """

        # Build the soft body of the soma
        soma_soft_body = self.build_soma_based_on_profile_points_only(apply_shader=apply_shader)

        # Update the frame based on the soft body simulation
        for frame_index in range(0, self.options.soma.simulation_steps):

            # Set the frame index
            bpy.context.scene.frame_set(frame_index)

            # Update the progress shell
            nmv.utilities.show_progress('* Simulation ',
                                        frame_index, self.options.soma.simulation_steps)

        # Report process done
        nmv.utilities.show_progress(
            '* Simulation ', self.options.soma.simulation_steps, self.options.soma.simulation_steps)

        # Build the soma mesh from the soft body object after deformation
        reconstructed_soma_mesh = self.build_soma_mesh_from_soft_body_object(soma_soft_body)

        # Add noise to the soma surface to make it more realistic
        self.add_noise_to_soma_surface(reconstructed_soma_mesh)

        # Return a reference to the reconstructed soma
        return reconstructed_soma_mesh
