####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# Blender imports
import bpy

import neuromorphovis as nmv
import neuromorphovis.bmeshi
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.mesh
import neuromorphovis.physics
import neuromorphovis.scene
import neuromorphovis.shading
import neuromorphovis.skeleton
import neuromorphovis.utilities


####################################################################################################
# @SomaBuilder
####################################################################################################
class SomaBuilder:
    """A robust factory for reconstructing a three-dimensional profile of neuronal somata on a
    physically-plausible basis using soft body objects, Hooke's law and the physics engine of
    Blender.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options,
                 full_arbor_extrusion=True,
                 preserve_topology_at_connections=False):
        """Constructor

        :param morphology:
            A given morphology.
        :param options:
            System options.
        :param full_arbor_extrusion:
            A flag to indicate if the faces that correspond to the arbors will be extruded until
            they hit the initial sample on the root arbor or not.
        """

        # Morphology
        self.morphology = morphology

        # All the options of the project (an instance of MeshyOptions)
        self.options = options

        # A common vertex group used to store all the vertices that will be grouped for the hooks
        self.vertex_group = None

        # A list of all the hooks that are created to stretch the soma
        self.hooks_list = None

        # If this flag is set, the faces will be extruded EXACTLY to the first sample on the root
        self.full_arbor_extrusion = full_arbor_extrusion

        # Preserving the topology of the mesh. This flag is used to create high quality meshes
        # with preserved topology to allow smooth connections with arbors in the meshing mode.
        # By default this flag is set to False, however, if the flag is set to True,
        # a high number of subdivisions will be used, for example 6, and no face subdivision
        # operations will be performed on the mesh.
        self.preserve_topology_at_connections = preserve_topology_at_connections

        # Ensure the connection between the arbors and the soma
        nmv.skeleton.ops.update_arbors_connection_to_soma(self.morphology)

    ################################################################################################
    # @get_extrusion_scale
    ################################################################################################
    @staticmethod
    def get_branch_extrusion_scale(branch,
                                   soma_radius):
        """Compute the ratio between the radius of the branch (or arbor) at the initial segment and
        its mapping on the initial ico-sphere that is used to reconstruct the soma.

        :param branch:
            The branch (or arbor) that we need to compute the extrusion scale for.
        :param soma_radius:
            The radius of the initial ico-sphere that represent the soma.
        :return:
            The ratio between the given soma radius and the extrusion radius of the branch.
        """

        # Compute the scale factor that will be applied on the initial sphere representing the soma
        # and then compute the extrusion radius
        extrusion_radius = branch.samples[0].radius * soma_radius / branch.samples[0].point.length

        # Compute the scale factor between the two radii
        scale_factor = branch.samples[0].radius / extrusion_radius

        # Return the computed scale factor
        return scale_factor

    ################################################################################################
    # @create_profile_point_extrusion_face
    ################################################################################################
    @staticmethod
    def create_profile_point_extrusion_face(soma_sphere,
                                            soma_radius,
                                            profile_point,
                                            profile_point_index,
                                            visualize_connection=False):
        """To reshape the soma based on the profile points, we will extrude only towards the points
        that do not have any intersections with the branches to improve the realism of the soma.

        :param soma_sphere:
            The ico-sphere that represent the initial shape of the soma.
        :param soma_radius:
            The radius of the ico-sphere that reflect the initial shape of the soma.
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
        direction = profile_point.normalized()

        # Compute the intersecting point on the soma
        profile_point_on_soma = soma_radius * direction

        # Verify the extrusion connection by drawing a sphere at the connection point
        if visualize_connection:

            # Label the connection
            connection_id = 'connection_profile_point_%s' % (str(profile_point_index))

            # Visualize the extrusion connection
            # TODO: Verify the value we use to consider the branch far away from the soma.
            nmv.skeleton.ops.visualize_extrusion_connection(
                point=profile_point_on_soma, radius=1.0, connection_id=connection_id)

        # Get the nearest face to the projected point on soma, subdivide it and use it for the
        # extrusion operation
        nearest_face_index = nmv.bmeshi.ops.get_nearest_face_index(
            soma_sphere, profile_point_on_soma)

        # Make a subdivision for extra processing
        faces_indices = nmv.bmeshi.ops.subdivide_faces(soma_sphere, [nearest_face_index])

        # Get the nearest face to the projection on soma after refinement
        nearest_face_index = nmv.bmeshi.ops.get_nearest_face_index(
            soma_sphere, profile_point_on_soma)

        # Return the face centroid to be used for retrieving the face later
        # We can search the nearest face w.r.t the centroid and the results is guaranteed
        extrusion_face = nmv.bmeshi.ops.get_face_from_index(soma_sphere, nearest_face_index)

        # Return the computed centroid of the extrusion face
        return extrusion_face.calc_center_median()

    ################################################################################################
    # @create_branch_extrusion_face
    ################################################################################################
    def create_branch_extrusion_face(self,
                                     soma_sphere,
                                     soma_radius,
                                     branch,
                                     visualize_connection=False):
        """Build a connecting extrusion face for emanating the branch from the soma.

        This function returns the centroid of the face to be a basis for building the branch
        itself later and attaching it to the soma.

        :param soma_sphere:
            The ico-sphere that represent the initial shape of the soma.
        :param soma_radius:
            The radius of the ico-sphere that reflect the initial shape of the soma.
        :param branch:
            The branch where the extrusion will happen.
        :param visualize_connection:
            Add a sphere to represent the connection between the branch and the soma.
        :return:
            The centroid of the created extrusion face.
        """

        # Compute the direction from the origin to the branching point
        connection_direction = branch.samples[0].point.normalized()

        # Compute the intersecting point on the soma and the difference between that on the soma
        # and that on the branch starting point
        connection_point_on_soma = connection_direction * soma_radius

        # Compute the extrusion radius that will be applied on the soma_sphere
        scale_factor = soma_radius / branch.samples[0].point.length
        extrusion_radius = branch.samples[0].radius * scale_factor

        # Create a reference circle for reshaping the connection cross section to a clean shape,
        # for instance a circle approximation
        connection_circle = nmv.bmeshi.create_circle(
            radius=extrusion_radius, location=connection_point_on_soma, vertices=32)

        # Verify the extrusion connection by drawing a sphere at the connection point
        if visualize_connection:

            # Label the connection
            connection_id = 'connection_%s_%s' % (branch.type, str(branch.id))

            # Plot a sphere at the connection point if requested
            nmv.skeleton.ops.visualize_extrusion_connection(
                point=connection_point_on_soma, radius=extrusion_radius,
                connection_id=connection_id)

        # The connection rotation target is mandatory to point the connection circle to it, then
        # compute it and rotate the face towards it
        # TODO: We might need to change the direction based on the directionality of the rest of
        # the section
        connection_rotation_target = connection_point_on_soma + connection_direction * 0.1
        nmv.bmeshi.ops.rotate_face_from_center_to_point(connection_circle, 0, connection_rotation_target)

        # Select the vertices that intersect with the extrusion sphere to prepare the face for
        # the extrusion process
        faces_indices = nmv.bmeshi.ops.get_indices_of_faces_intersecting_sphere(
            soma_sphere, connection_point_on_soma, extrusion_radius)

        # Make a subdivision for extra processing, if the topology is not required to be preserved
        if self.options.soma.irregular_subdivisions:
            nmv.bmeshi.ops.subdivide_faces(soma_sphere, faces_indices, cuts=1)

        # Get the actual intersecting faces via their indices (this is for smoothing)
        faces_indices = nmv.bmeshi.ops.get_indices_of_faces_fully_intersecting_sphere(
            soma_sphere, connection_point_on_soma, extrusion_radius)

        # If we did not get any faces from the previous operation, then try to get the nearest face
        # This case might happen when the branch is very thin and cannot map to more than one face

        if len(faces_indices) < 1:

            # Get the nearest face, subdivide it and use it
            nearest_face_index = nmv.bmeshi.ops.get_nearest_face_index(
                soma_sphere, connection_point_on_soma)

            # Make a subdivision for extra processing for the obtained face
            faces_indices = nmv.bmeshi.ops.subdivide_faces(soma_sphere, [nearest_face_index], cuts=2)

        # Merge the selected faces into a single face that will be used for the extrusion
        extrusion_face_index = nmv.bmeshi.ops.merge_faces_into_one_face(soma_sphere, faces_indices)

        # Map the face to a reference connection circle
        nmv.bmeshi.ops.convert_face_to_circle(
            soma_sphere, extrusion_face_index, connection_point_on_soma, extrusion_radius)

        # Return face centroid to be used for retrieving the face later
        # we can search the nearest face w.r.t the centroid and the results is guaranteed
        extrusion_face = nmv.bmeshi.ops.get_face_from_index(soma_sphere, extrusion_face_index)

        # Store the index of the face to the branch to use it later for the extrusion
        branch.soma_face_index = extrusion_face_index
        branch.soma_face_centroid = extrusion_face.calc_center_median()

        # Return the computed centroid of the extrusion face
        return extrusion_face.calc_center_median()

    ################################################################################################
    # @attach_hook_to_extrusion_face
    ################################################################################################
    def attach_hook_to_extrusion_face(self,
                                      soma_sphere_object,
                                      branch,
                                      extrusion_face_centroid,
                                      vertex_group,
                                      hooks_list,
                                      extrusion_scale):
        """Attache a hook to the extrusion face and locate it at the different keyframes.

        :param soma_sphere_object:
        :param branch:
        :param extrusion_face_centroid:
        :param vertex_group:
        :param hooks_list:
        :param extrusion_scale:
        :return:
        """

        # Search for the extrusion face by getting the nearest face in the soma sphere object to
        # the given centroid point
        face_index = nmv.mesh.ops.get_index_of_nearest_face_to_point(
            soma_sphere_object, extrusion_face_centroid)
        face = soma_sphere_object.data.polygons[face_index]

        # Retrieve a list of all the vertices of the face
        vertices_indices = face.vertices[:]

        face_center = face.center
        point_0 = face_center + face_center.normalized() * 0.01
        point_1 = branch.samples[0].point
        #

        if not self.full_arbor_extrusion:
            point_1 = point_1 - face_center.normalized() * nmv.consts.Arbors.SOMA_EXTRUSION_DELTA

        # Add the vertices to the existing vertex group
        nmv.mesh.ops.add_vertices_to_existing_vertex_group(vertices_indices, vertex_group)

        # Create the hook and attach it to the vertices
        hook = nmv.physics.hook.ops.add_hook_to_vertices(
            soma_sphere_object, vertices_indices, name='hook_%d' % branch.id)

        # The hook is stretched from the center of the face to the branch initial segment point
        # Set the hook positions at the different key frames
        nmv.physics.hook.ops.locate_hook_at_keyframe(hook, point_0, 1)
        nmv.physics.hook.ops.scale_hook_at_keyframe(hook, 1, 1)
        nmv.physics.hook.ops.locate_hook_at_keyframe(hook, point_1, 50)
        nmv.physics.hook.ops.scale_hook_at_keyframe(hook, 1, 50)

        # The hooks is scaled between 50 and 60
        nmv.physics.hook.ops.scale_hook_at_keyframe(hook, extrusion_scale, 60)

        # Add the hook to the hooks list
        hooks_list.append(hook)

        # Return index of the extrusion face to be used later for branch extrusion
        return face_index

    ################################################################################################
    # @attach_hook_to_extrusion_face_on_profile_point
    ################################################################################################
    @staticmethod
    def attach_hook_to_extrusion_face_on_profile_point(soma_sphere_object,
                                                       profile_point,
                                                       profile_point_index,
                                                       extrusion_face_centroid,
                                                       vertex_group,
                                                       hooks_list):
        """

        :param soma_sphere_object:
        :param profile_point:
        :param extrusion_face_centroid:
        :param vertex_group:
        :param hooks_list:
        :return:
        """

        # search for the extrusion face by getting the nearest face in the soma
        # sphere object to the given centroid point
        # face_index = mesh_ops.get_index_of_nearest_face_to_point(
        #    soma_sphere_object, extrusion_face_centroid)
        # face = soma_sphere_object.data.polygons[face_index]

        # use vertex
        vertex_index = nmv.mesh.ops.get_index_of_nearest_vertex_to_point(
            soma_sphere_object, profile_point)

        # retrieve a list of all the vertices of the face
        vertices_indices = [vertex_index]  # face.vertices[:]
        face_center = soma_sphere_object.data.vertices[vertex_index].co

        # face.center
        point_0 = face_center + face_center.normalized() * 0.01
        point_1 = profile_point

        # add the vertices to the existing vertex group
        nmv.mesh.ops.add_vertices_to_existing_vertex_group(vertices_indices, vertex_group)

        # create the hook and attach it to the vertices
        hook = nmv.physics.hook.ops.add_hook_to_vertices(soma_sphere_object, vertices_indices,
            name='hook_%d' % profile_point_index)

        # the hook should be stretched from the center of the face to the branch
        # initial segment point
        # set the hook positions at the different key frames
        nmv.physics.hook.ops.locate_hook_at_keyframe(hook, point_0, 1)
        nmv.physics.hook.ops.locate_hook_at_keyframe(hook, point_1, 50)

        # add the hook to the hooks list
        hooks_list.append(hook)

        # return index of the extrusion face to be used later for branch extrusion
        return None

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

        # Get thea reference to the soma from the morphology
        soma = self.morphology.soma

        # Get the profile points from the soma
        profile_points = soma.profile_points

        # If the topology needs to be preserved, then a high number of subdivisions is required,
        # otherwise use the subdivision level given by the user
        subdivisions = \
            6 if self.preserve_topology_at_connections else self.options.soma.subdivision_level

        # Create a ico-sphere bmesh to represent the starting shape of the soma
        soma_radius = soma.mean_radius / 2.0
        soma_bmesh_sphere = nmv.bmeshi.create_ico_sphere(
            radius=soma_radius, subdivisions=subdivisions)

        # Extrude the faces
        faces_centers = []
        non_intersecting_profile_points = []
        for i, profile_point in enumerate(profile_points):
            if nmv.skeleton.ops.profile_point_intersect_other_point(
                    profile_point, i, profile_points, soma_radius):
                nmv.logger.log("WARNING: profile points intersection")
                continue

            if profile_point.length > soma_radius:
                non_intersecting_profile_points.append(profile_point)
                face_center = self.create_profile_point_extrusion_face(
                    soma_bmesh_sphere, soma_radius, profile_point, i)
                faces_centers.append(face_center)

        # Link the soma sphere to the scene
        soma_sphere_object = nmv.bmeshi.ops.link_to_new_object_in_scene(
            soma_bmesh_sphere, '%s_soma' % self.options.morphology.label)

        # Create a vertex group to link all the vertices of the extrusion faces to it
        self.vertex_group = nmv.bmeshi.ops.create_vertex_group(soma_sphere_object)

        # Create a hook list to be able to delete all the hooks after finishing the simulation
        self.hooks_list = []
        for i, face_centroid in enumerate(faces_centers):

            # Attach hook to an extrusion face
            self.attach_hook_to_extrusion_face_on_profile_point(
                soma_sphere_object, non_intersecting_profile_points[i], i, face_centroid,
                self.vertex_group, self.hooks_list)

        # Set the time-line to zero
        bpy.context.scene.frame_set(0)

        # Apply the soft body operation
        nmv.physics.soft_body.ops.apply_soft_body_to_object(soma_sphere_object, self.vertex_group,
            self.options.soma)

        # Apply the soma shader directly to the soft body object, otherwise create the soma here
        # and apply the material later.
        """
        if apply_shader:
            # Create the soma material and assign it to the ico-sphere
            soma_material = None

            # Lambert shader
            if self.options.soma.soma_material == enumerators.__rendering_lambert__:
                soma_material = materials.create_default_material('soma_color_lambert',
                    self.options.soma.soma_color, (0.0, 0.0, 0.0), 1.0)

            # Electron shader
            elif self.options.soma.soma_material == enumerators.__rendering_electron__:
                soma_material = electron.create_electron_material('soma_color_electron',
                    self.options.soma.soma_color, (0.0, 0.0, 0.0))

            # By default create lambert material
            else:
                nmv.logger.log('WARNING: Undefined material [%s]. Creating lambert shader' %
                      self.options.soma.soma_material)
                soma_material = materials.create_default_material('soma_color_lambert',
                    self.options.soma.soma_color, (0.0, 0.0, 0.0), 1.0)

            # Apply the shader to the ico-sphere
            materials.set_material_to_object(soma_sphere_object, soma_material)
        """

        return soma_sphere_object

    ################################################################################################
    # @build_soma_soft_body
    ################################################################################################
    def build_soma_soft_body(self,
                             apply_shader=True):
        """Build the soma based on soft-body simulation and Hooke's law.

        The building process ASSUMES non-overlapping and too faraway branches.

        :param apply_shader:
            Apply the given soma shader in the configuration. This flag will be set to False when
            the soma is created in another builder such as the skeleton builder or the piecewise
            mesh builder.
        :return
            The soft body object after the deformation. This object will be used later to build
            the soma mesh.
        """

        # Soma, and its radius
        soma = self.morphology.soma

        # TODO: fix
        soma_radius = soma.mean_radius / 2.0

        # Axon root
        axon_root = self.morphology.axon

        # Dendrites roots
        dendrites_roots = self.morphology.dendrites

        # Apical dendrite root
        apical_dendrite_root = self.morphology.apical_dendrite

        # If the topology needs to be preserved, then a high number of subdivisions is required,
        # otherwise use the subdivision level given by the user
        subdivisions = \
            6 if self.preserve_topology_at_connections else self.options.soma.subdivision_level

        # Create a ico-sphere bmesh to represent the starting shape of the soma
        soma_bmesh_sphere = nmv.bmeshi.create_ico_sphere(
            radius=soma_radius, subdivisions=subdivisions)

        # Keep a list of all the extrusion face centroids, for later
        roots_and_faces_centroids = []

        nmv.logger.log('**************************************************************************')
        nmv.logger.log('Building soma')
        nmv.logger.log('**************************************************************************')

        # Apical dendrite
        if not self.options.morphology.ignore_apical_dendrite:

            # Build towards the apical dendrite, if the apical dendrite is available
            if apical_dendrite_root is not None:

                nmv.logger.log('\t * Apical dendrite')

                # Create the extrusion face, where the pulling will occur
                extrusion_face_centroid = self.create_branch_extrusion_face(
                    soma_bmesh_sphere, soma_radius, apical_dendrite_root,
                    visualize_connection=False)

                # Update the list
                roots_and_faces_centroids.append([apical_dendrite_root, extrusion_face_centroid])

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Build towards the dendrites, if possible
            for i, dendrite_root in enumerate(dendrites_roots):

                # The dendrite must be connected to the soma
                if dendrite_root.connected_to_soma:

                    # Which dendrite ?!!
                    nmv.logger.log('\t * Dendrite [%d]' % i)

                    # Create the extrusion face, where the pulling will occur
                    extrusion_face_centroid = self.create_branch_extrusion_face(
                        soma_bmesh_sphere, soma_radius, dendrite_root,
                        visualize_connection=False)

                    # Update the list
                    roots_and_faces_centroids.append([dendrite_root, extrusion_face_centroid])

                # This basal dendrite is not connected to soma
                else:

                    # Report the issue
                    nmv.logger.log('\t * Dendrite [%d] is NOT connected to soma' % i)

        # Axon
        if not self.options.morphology.ignore_axon:

            # The axon must be connected to the soma
            if axon_root.connected_to_soma:

                nmv.logger.log('\t * Axon')

                # Create the extrusion face, where the pulling will occur
                extrusion_face_centroid = self.create_branch_extrusion_face(
                    soma_bmesh_sphere, soma_radius, axon_root, visualize_connection=False)

                # Update the list
                roots_and_faces_centroids.append([axon_root, extrusion_face_centroid])

            # The axon is not connected to soma
            else:

                # Report the issue
                nmv.logger.log('\t * Axon is NOT connected to soma')

        """ Physics """
        # Link the soma sphere to the scene
        soma_sphere_object = nmv.bmeshi.ops.link_to_new_object_in_scene(
            soma_bmesh_sphere, '%s_soma' % self.options.morphology.label)

        # Create a vertex group to link all the vertices of the extrusion faces to it
        self.vertex_group = nmv.mesh.ops.create_vertex_group(soma_sphere_object)

        # Create a hooks list to be able to delete all the hooks after finishing the simulation
        extrusion_faces_vertices_indices = []
        self.hooks_list = []
        faces_indices = []
        for root_and_face_center in roots_and_faces_centroids:
            branch = root_and_face_center[0]
            face_centroid = root_and_face_center[1]

            # Get the indices of the faces
            face_index = nmv.mesh.ops.get_index_of_nearest_face_to_point(
                soma_sphere_object, face_centroid)
            face = soma_sphere_object.data.polygons[face_index]
            vertices_indices = face.vertices[:]
            extrusion_faces_vertices_indices.extend(vertices_indices)

            # Get the extrusion scale
            extrusion_scale = self.get_branch_extrusion_scale(branch, soma_radius)

            # Attach hook to an extrusion face
            face_index = self.attach_hook_to_extrusion_face(
                soma_sphere_object, branch, face_centroid, self.vertex_group, self.hooks_list,
                extrusion_scale)
            faces_indices.append(face_index)


        # Get the soma scale factor
        # scale_factor = soma.mean_radius / soma_radius

        # Scale the soma radius to match reality
        # building_ops.scale_soma_radius(soma_sphere_object, extrusion_faces_vertices_indices,
        #                                scale_factor, self.hooks_list)

        # Set the time-line to zero
        bpy.context.scene.frame_set(0)

        # Apply the soft body operation
        nmv.physics.ops.apply_soft_body_to_object(
            soma_sphere_object, self.vertex_group, self.options.soma)

        # Apply the soma shader directly to the soft body object, otherwise create the soma here
        # and apply the material later.
        if apply_shader:

            # Create the soma material and assign it to the ico-sphere
            soma_material = nmv.shading.create_material(name='soma',
                color=self.options.soma.soma_color, material_type=self.options.soma.soma_material)

            # Apply the shader to the ico-sphere
            nmv.shading.set_material_to_object(
                mesh_object=soma_sphere_object, material_reference=soma_material)

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
                              apply_shader=True):
        """Reconstructs the mesh of the soma of the neuron in a single step.

        :param apply_shader:
            Apply the given soma shader in the configuration. This flag will be set to False when
            the soma is created in another builder such as the skeleton builder or the piecewise
            mesh builder.
        :return:
            A reference to the reconstructed mesh of the soma.
        """

        # Build the soft body of the soma
        soma_soft_body = self.build_soma_soft_body(apply_shader=apply_shader)

        # Update the frame based on the soft body simulation
        for frame_index in range(nmv.consts.Simulation.MIN_FRAME, nmv.consts.Simulation.MAX_FRAME):

            # Set the frame index
            bpy.context.scene.frame_set(frame_index)

            # Update the progress shell
            nmv.utilities.show_progress('Simulation: ', frame_index, nmv.consts.Simulation.MAX_FRAME)

        # Report process done
        nmv.utilities.show_progress(
            'Simulation: \n', nmv.consts.Simulation.MAX_FRAME, nmv.consts.Simulation.MAX_FRAME)

        # Build the soma mesh from the soft body object after deformation
        reconstructed_soma_mesh = self.build_soma_mesh_from_soft_body_object(soma_soft_body)

        # Return a reference to the reconstructed soma
        return reconstructed_soma_mesh

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
        for frame_index in range(nmv.consts.Simulation.MIN_FRAME, nmv.consts.Simulation.MAX_FRAME):

            # Set the frame index
            bpy.context.scene.frame_set(frame_index)

            # Update the progress shell
            nmv.utilities.show_progress('Simulation: ', frame_index, nmv.consts.Simulation.MAX_FRAME)

        # Report process done
        nmv.utilities.show_progress(
            'Simulation: \n', nmv.consts.Simulation.MAX_FRAME, nmv.consts.Simulation.MAX_FRAME)

        # Build the soma mesh from the soft body object after deformation
        reconstructed_soma_mesh = self.build_soma_mesh_from_soft_body_object(soma_soft_body)

        # Return a reference to the reconstructed soma
        return reconstructed_soma_mesh
