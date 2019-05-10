####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
import random, copy

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv
import nmv.consts
import nmv.enums
import nmv.file
import nmv.builders
import nmv.geometry
import nmv.mesh
import nmv.scene
import nmv.shading
import nmv.skeleton
import nmv.bmeshi


####################################################################################################
# @SkeletonBuilder
####################################################################################################
class SkeletonBuilder:
    """Skeleton builder
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor.

        :param morphology:
            A given morphology.
        """

        # Morphology
        self.morphology = copy.deepcopy(morphology)

        # All the options of the project (an instance of MeshyOptions)
        self.options = options

        # All the reconstructed objects of the morphologies, for example, tubes, spheresm etc... .
        self.morphology_objects = []

        # A list of the colors/materials of the soma
        self.soma_materials = None

        # A list of the colors/materials of the axon
        self.axon_materials = None

        # A list of the colors/materials of the basal dendrites
        self.basal_dendrites_materials = None

        # A list of the colors/materials of the apical dendrite
        self.apical_dendrite_materials = None

        # A list of the colors/materials of the articulation spheres
        self.articulation_materials = None

        # The directory where the progressive frames will be dumped
        self.progressive_frames_directory = None

        # Progressive rendering camera
        self.progressive_rendering_camera = None

        # Progressive rendering frame index, starts from 1 since the soma will be 0
        self.progressive_frame_index = 1

    ################################################################################################
    # @create_skeleton_materials
    ################################################################################################
    def create_skeleton_materials(self):
        """Creates the materials of the skeleton. The created materials are stored in private
        variables.
        """

        # Clear all the materials that are already present in the scene
        for material in bpy.data.materials:
            if 'soma_skeleton' in material.name or \
               'axon_skeleton' in material.name or \
               'basal_dendrites_skeleton' in material.name or \
               'apical_dendrite_skeleton' in material.name or \
               'articulation' in material.name:
                    material.user_clear()
                    bpy.data.materials.remove(material)

        # Soma
        self.soma_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='soma_skeleton', material_type=self.options.morphology.material,
            color=self.options.morphology.soma_color)

        # Axon
        self.axon_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='axon_skeleton', material_type=self.options.morphology.material,
            color=self.options.morphology.axon_color)

        # Basal dendrites
        self.basal_dendrites_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='basal_dendrites_skeleton', material_type=self.options.morphology.material,
            color=self.options.morphology.basal_dendrites_color)

        # Apical dendrite
        self.apical_dendrite_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='apical_dendrite_skeleton', material_type=self.options.morphology.material,
            color=self.options.morphology.apical_dendrites_color)

        # Articulations for the articulated reconstruction method
        self.articulation_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='articulation', material_type=self.options.morphology.material,
            color=self.options.morphology.articulation_color)

        # Create an illumination specific for the given material
        nmv.shading.create_material_specific_illumination(self.options.morphology.material)

    ################################################################################################
    # @draw_section_samples_as_spheres
    ################################################################################################
    @staticmethod
    def draw_section_samples_as_spheres(section):
        """Draw the section samples as a set of spheres.

        :param section:
            A given section to draw.
        :return:
            List of spheres of the section.
        """
        output = list()
        for sample in section.samples:
            sphere = nmv.bmeshi.create_ico_sphere(radius=sample.radius, location=sample.point,
                                                  subdivisions=3)
            output.append(sphere)
        return output

    ################################################################################################
    # @draw_soma_sphere
    ################################################################################################
    def draw_soma_sphere(self):
        """Draws a sphere that represents the soma.
        """

        # Get a reference to the soma
        soma = self.morphology.soma

        # Draw the soma as a sphere
        soma_sphere = nmv.mesh.create_uv_sphere(
            radius=soma.mean_radius, location=soma.centroid, name='soma')

        # Assign a material to the soma sphere
        nmv.shading.set_material_to_object(soma_sphere, self.soma_materials[0])

        # Return a reference to the object
        return soma_sphere

    ################################################################################################
    # @draw_section_terminal_as_sphere
    ################################################################################################
    def draw_section_terminal_as_sphere(self,
                                        section):
        """Draws a joint between the different sections along the arbor.

        :param section:
            Section geometry.
        """

        # Get the section data arranged in a poly-line format
        section_data = nmv.skeleton.ops.get_section_poly_line(section)

        # Access the last item
        section_terminal = section_data[-1]

        # Get a Vector(()) for the coordinates of the terminal
        point = section_terminal[0]
        point = Vector((point[0], point[1], point[2]))

        # Get terminal radius
        radius = section_terminal[1]

        # Get the radius for the first samples of the children and use it if it's bigger than the
        # radius of the last sample of the parent terminal.
        for child in section.children:

            # Get the first sample along the child section
            child_data = nmv.skeleton.ops.get_section_poly_line(child)

            # Verify the radius of the child
            child_radius = child_data[0][1]

            # If the radius of the child is bigger, then set the radius of the joint to the
            # radius of the child
            if child_radius > radius:
                radius = child_radius

        # If we scale the morphology, we should account for that in the spheres to
        sphere_radius = radius
        if self.options.morphology.arbors_radii == nmv.enums.Skeletonization.ArborsRadii.SCALED:
            sphere_radius *= self.options.morphology.sections_radii_scale
        elif self.options.morphology.arbors_radii == nmv.enums.Skeletonization.ArborsRadii.FIXED:
            sphere_radius = self.options.morphology.sections_fixed_radii_value

        # Create the sphere based on the largest radius
        section_terminal_sphere = nmv.geometry.create_uv_sphere(
            radius=sphere_radius * 1.125, location=point, subdivisions=16,
            name='joint_%d' % section.id, color=self.options.morphology.articulation_color)

        # Return a reference to the terminal sphere
        return section_terminal_sphere

    ################################################################################################
    # @draw_section_as_disconnected_segments
    ################################################################################################
    def draw_section_terminals_as_spheres(self,
                                          root,
                                          material_list=None,
                                          sphere_objects=[],
                                          branching_level=0,
                                          max_branching_level=nmv.consts.Math.INFINITY):
        """Draws the terminals of a given arbor as spheres.

        :param root:
            Arbor root.
        :param material_list:
            Sphere material.
        :param sphere_objects:
            A list of all the drawn spheres.
        :param branching_level:
            Current branching level.
        :param max_branching_level:
            Maximum branching level the section can grow up to: infinity.
        """

        # Ignore the drawing if the root section is None
        if root is None:
            return

        # Increment the branching level
        branching_level += 1

        # Stop drawing at the maximum branching level
        if branching_level > max_branching_level:
            return

        # Make sure that the arbor exist
        if root is not None:

            # Draw the section terminal sphere
            section_terminal_sphere = self.draw_section_terminal_as_sphere(root)

            # Assign the material to the sphere
            nmv.shading.set_material_to_object(section_terminal_sphere, material_list[0])

            # Add the sphere to the list of the spheres objects
            sphere_objects.append(section_terminal_sphere)

            # Draw the children sections
            for child in root.children:
                self.draw_section_terminals_as_spheres(
                    child, sphere_objects=sphere_objects, material_list=material_list,
                    branching_level=branching_level, max_branching_level=max_branching_level)

    ################################################################################################
    # @draw_sections_as_spheres
    ################################################################################################
    def draw_sections_as_spheres(self,
                                root,
                                name,
                                material_list=[],
                                segments_objects=[],
                                branching_level=0,
                                max_branching_level=nmv.consts.Math.INFINITY):
        """Draw the section as a list of spheres.

        :param root:
        :param name:
        :param material_list:
        :param segments_objects:
        :param branching_level:
        :param max_branching_level:
        :param bevel_object:
        :return:
        """

        # Ignore the drawing if the root section is None
        if root is None:
            return

        # Increment the branching level
        branching_level += 1

        # Stop drawing at the maximum branching level
        if branching_level > max_branching_level:
            return

        # Make sure that the arbor exist
        if root is not None:

            section_name = '%s_%d' % (name, root.id)
            drawn_spheres = self.draw_section_samples_as_spheres(root)

            # Add the drawn segments to the 'segments_objects'
            segments_objects.extend(drawn_spheres)

            # Draw the children sections
            for child in root.children:
                self.draw_sections_as_spheres(
                    root=child,
                    branching_level=branching_level,
                    max_branching_level=max_branching_level,
                    name=name,
                    material_list=material_list,
                    segments_objects=segments_objects)

    ################################################################################################
    # @draw_section_as_disconnected_segments
    ################################################################################################
    def draw_section_as_disconnected_segments(self,
                                              root,
                                              name,
                                              material_list=[],
                                              segments_objects=[],
                                              branching_level=0,
                                              max_branching_level=nmv.consts.Math.INFINITY,
                                              bevel_object=None):
        """Draw the sections in each arbor as a series of disconnected segments, where each segment
        is represented by a tube.

        :param root:
            Arbor root.
        :param name:
            Arbor name.
        :param material_list:
            Arbor colors.
        :param segments_objects:
            The drawn list of segments.
        :param branching_level:
            Current branching level.
        :param max_branching_level:
            Maximum branching level the section can grow up to: infinity.
        :param bevel_object:
            A given bevel object to scale the arbor sections.
        """

        # Ignore the drawing if the root section is None
        if root is None:
            return

        # Increment the branching level
        branching_level += 1

        # Stop drawing at the maximum branching level
        if branching_level > max_branching_level:
            return

        # Make sure that the arbor exist
        if root is not None:
            section_name = '%s_%d' % (name, root.id)
            drawn_segments = nmv.skeleton.ops.draw_disconnected_segments(
                root, name=section_name,
                material_list=material_list,
                bevel_object=bevel_object,
                render_frame=self.options.morphology.render_progressive,
                frame_destination=self.progressive_frames_directory,
                camera=self.progressive_rendering_camera)

            # Add the drawn segments to the 'segments_objects'
            segments_objects.extend(drawn_segments)

            # Draw the children sections
            for child in root.children:
                self.draw_section_as_disconnected_segments(
                    root=child,
                    branching_level=branching_level,
                    max_branching_level=max_branching_level,
                    name=name,
                    material_list=material_list,
                    bevel_object=bevel_object,
                    segments_objects=segments_objects)

    ################################################################################################
    # @draw_section_as_disconnected_object
    ################################################################################################
    def draw_section_as_disconnected_object(self,
                                            section,
                                            name,
                                            material_list=None,
                                            bevel_object=None):
        """Draws the section as a tube object.

        :param section:
            The geometry of a morphological section.
        :param name:
            The name of the section.
        :param material_list:
            The color of the section.
        :param bevel_object:
            A given bevel object to scale the section.
        """

        # Get the section data arranged in a poly-line format
        data = nmv.skeleton.ops.get_section_poly_line(section)

        # Use the section id to tag the section name
        section_name = '%s_%d_section' % (name, section.id)

        # Section material
        section_material = None
        if material_list is not None:
            if section.id % 2 == 0:
                section_material = material_list[0]
            else:
                section_material = material_list[1]

        # Draw the section
        section_object = nmv.geometry.ops.draw_poly_line(
            poly_line_data=data, name=section_name, material=section_material,
            bevel_object=bevel_object)

        # Draw the frame for progressive rendering
        if self.options.morphology.render_progressive:

            frame_file_path = '%s/frame_%s' % (
                self.progressive_frames_directory, '{0:05d}'.format(self.progressive_frame_index))

            # Render the image to film
            # camera_ops.render_scene_to_image(self.progressive_rendering_camera, frame_file_path)

            self.progressive_frame_index += 1

        # Return a reference to the drawn section object
        return section_object

    ################################################################################################
    # @draw_root_as_disconnected_sections
    ################################################################################################
    def draw_root_as_disconnected_sections(self,
                                           root,
                                           name,
                                           material_list=[],
                                           sections_objects=[],
                                           branching_level=0,
                                           max_branching_level=nmv.consts.Math.INFINITY,
                                           bevel_object=None):
        """Draws the section as a continuous, yet, disconnected and independent object from the
        rest of the sections of the morphology.

        :param root:
            Arbor root.
        :param name:
            Arbor prefix.
        :param material_list:
            Arbor colors.
        :param sections_objects:
            A list of all the drawn sections in the morphology.
        :param branching_level:
            Current branching level.
        :param max_branching_level:
            Maximum branching level set by the user.
        :param bevel_object:
            A given bevel object to scale the arbor sections.
        """

        # Make sure that the arbor exist
        if root is not None:

            # Increment the branching level
            branching_level += 1

            # Stop drawing at the maximum branching level
            if branching_level > max_branching_level:
                return

            # Draw the section as an independent disconnected object
            section_objects = self.draw_section_as_disconnected_object(
                root, name=name, material_list=material_list, bevel_object=bevel_object)

            # Add the section object to the list
            sections_objects.append(section_objects)

            # Process the children, section by section
            for child in root.children:

                # Draw the sections of all the children at the same branching level
                self.draw_root_as_disconnected_sections(
                    root=child,
                    name=name,
                    material_list=material_list,
                    branching_level=branching_level,
                    max_branching_level=max_branching_level,
                    bevel_object=bevel_object,
                    sections_objects=sections_objects)

    ################################################################################################
    # @draw_morphology_as_spheres
    ################################################################################################
    def draw_morphology_as_spheres(self):
        """Draws the morphology as a set of spheres.

        :return:
            A list of spheres.
        """

        # Morphology objects
        morphology_objects = list()

        # Draw the axon
        if not self.options.morphology.ignore_axon:
            if self.morphology.axon is not None:
                nmv.logger.info('Axon')

                axon_segments_objects = []
                self.draw_sections_as_spheres(
                    self.morphology.axon,
                    name=nmv.consts.Arbors.AXON_PREFIX,
                    max_branching_level=self.options.morphology.axon_branch_order,
                    material_list=self.axon_materials,
                    segments_objects=axon_segments_objects)

                # Convert the objects to something and add them to the scene
                for i, item in enumerate(axon_segments_objects):
                    sphere_mesh = nmv.bmeshi.ops.link_to_new_object_in_scene(
                        item, '%s_%d' % ('axon', i))

                    # Smooth shading
                    nmv.mesh.shade_smooth_object(sphere_mesh)

                    # Assign the material
                    nmv.shading.set_material_to_object(sphere_mesh, self.axon_materials[i % 2])

                    # Append the sphere mesh to the morphology objects
                    morphology_objects.append(sphere_mesh)

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Ensure tha existence of basal dendrites
            if self.morphology.dendrites is not None:
                basal_dendrites_segments_objects = []

                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.info('Basal dendrite [%d]' % i)
                    dendrite_name = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)
                    self.draw_sections_as_spheres(
                        basal_dendrite, name=dendrite_name,
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                        material_list=self.basal_dendrites_materials,
                        segments_objects=basal_dendrites_segments_objects)

                # Convert the objects to something and add them to the scene
                for i, item in enumerate(basal_dendrites_segments_objects):
                    sphere_mesh = nmv.bmeshi.ops.link_to_new_object_in_scene(
                        item, '%s_%d' % ('basal_dendrite', i))

                    # Smooth shading
                    nmv.mesh.shade_smooth_object(sphere_mesh)

                    # Assign the material
                    nmv.shading.set_material_to_object(sphere_mesh,
                                                       self.basal_dendrites_materials[i % 2])

                    # Append the sphere mesh to the morphology objects
                    morphology_objects.append(sphere_mesh)

        # Draw the apical dendrite
        if not self.options.morphology.ignore_apical_dendrite:

            # Draw the apical dendrite, if exists
            if self.morphology.apical_dendrite is not None:
                nmv.logger.info('Apical dendrite')

                apical_dendrite_segments_objects = []
                self.draw_sections_as_spheres(
                    self.morphology.apical_dendrite,
                    name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                    max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                    material_list=self.apical_dendrite_materials,
                    segments_objects=apical_dendrite_segments_objects)

                # Convert the objects to something and add them to the scene
                for i, item in enumerate(apical_dendrite_segments_objects):
                    sphere_mesh = nmv.bmeshi.ops.link_to_new_object_in_scene(
                        item, '%s_%d' % ('apical_dendrite', i))

                    # Smooth shading
                    nmv.mesh.shade_smooth_object(sphere_mesh)

                    # Assign the material
                    nmv.shading.set_material_to_object(sphere_mesh,
                                                       self.apical_dendrite_materials[i % 2])

                    # Append the sphere mesh to the morphology objects
                    morphology_objects.append(sphere_mesh)

        # Return a list of the morphology objects
        return morphology_objects

    ################################################################################################
    # @draw_morphology_as_disconnected_segments
    ################################################################################################
    def draw_morphology_as_disconnected_segments(self,
                                                 bevel_object=None):
        """Draw the morphological arbors as a set of disconnected segments.

        :param bevel_object:
            A given bevel object to scale the samples.
        :return
            A list of all the drawn objects
        """

        # A list of objects (references to drawn segments) that compose the morphology
        morphology_objects = []

        # Draw the axon
        if not self.options.morphology.ignore_axon:
            axon_segments_objects = []
            self.draw_section_as_disconnected_segments(
                self.morphology.axon,
                name=nmv.consts.Arbors.AXON_PREFIX,
                max_branching_level=self.options.morphology.axon_branch_order,
                material_list=self.axon_materials,
                bevel_object=bevel_object,
                segments_objects=axon_segments_objects)

            # Extend the morphology objects list
            morphology_objects.extend(axon_segments_objects)

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Ensure tha existence of basal dendrites
            if self.morphology.dendrites is not None:

                basal_dendrites_segments_objects = []

                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    dendrite_name = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)
                    self.draw_section_as_disconnected_segments(
                        basal_dendrite, name=dendrite_name,
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                        material_list=self.basal_dendrites_materials,
                        bevel_object=bevel_object,
                        segments_objects=basal_dendrites_segments_objects)

                # Extend the morphology objects list
                morphology_objects.extend(basal_dendrites_segments_objects)

        # Draw the apical dendrite
        if not self.options.morphology.ignore_apical_dendrite:
            apical_dendrite_segments_objects = []
            self.draw_section_as_disconnected_segments(
                self.morphology.apical_dendrite,
                name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                material_list=self.apical_dendrite_materials,
                bevel_object=bevel_object,
                segments_objects=apical_dendrite_segments_objects)

            # Extend the morphology objects list
            morphology_objects.extend(apical_dendrite_segments_objects)

        # Return a reference to the list of drawn objects
        return morphology_objects

    ################################################################################################
    # @draw_morphology_as_disconnected_sections
    ################################################################################################
    def draw_morphology_as_disconnected_sections(self,
                                                 bevel_object=None):
        """Draw the morphological arbors as a set of disconnected sections.

        :param bevel_object:
            A given bevel object to scale the samples.
        :return
            A list of all the drawn objects in the morphology.
        """

        # A list of objects (references to drawn segments) that compose the morphology
        morphology_objects = []

        # Draw the axon
        if not self.options.morphology.ignore_axon:
            axon_sections_objects = []
            self.draw_root_as_disconnected_sections(
                self.morphology.axon,
                name=nmv.consts.Arbors.AXON_PREFIX,
                material_list=self.axon_materials,
                bevel_object=bevel_object,
                max_branching_level=self.options.morphology.axon_branch_order,
                sections_objects=axon_sections_objects)

            # Extend the morphology objects list
            morphology_objects.extend(axon_sections_objects)

        # Draw the apical dendrite
        if not self.options.morphology.ignore_apical_dendrite:
            apical_dendrite_sections_objects = []
            self.draw_root_as_disconnected_sections(
                self.morphology.apical_dendrite,
                name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                material_list=self.apical_dendrite_materials,
                bevel_object=bevel_object,
                max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                sections_objects=apical_dendrite_sections_objects)

            # Extend the morphology objects list
            morphology_objects.extend(apical_dendrite_sections_objects)

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Ensure tha existence of basal dendrites
            if self.morphology.dendrites is not None:

                basal_dendrites_sections_objects = []

                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    dendrite_prefix = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)
                    self.draw_root_as_disconnected_sections(
                        basal_dendrite,
                        name=dendrite_prefix,
                        material_list=self.basal_dendrites_materials,
                        bevel_object=bevel_object,
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                        sections_objects=basal_dendrites_sections_objects)

                # Extend the morphology objects list
                morphology_objects.extend(basal_dendrites_sections_objects)

        # Return a reference to the list of drawn objects
        return morphology_objects

    ################################################################################################
    # @draw_morphology_as_articulated_sections
    ################################################################################################
    def draw_morphology_as_articulated_sections(self,
                                                bevel_object=None):

        """Reconstructs and draws the morphology as a series of articulated sections.

        :param bevel_object:
            A bevel object used to scale the radii of the sections.
        :return:
            A list of all the objects of the morphology that are already drawn.
        """

        # A list of objects (references to drawn segments) that compose the morphology
        morphology_objects = []

        # Draw the disconnected sections and then draw the articulations or spheres at between the
        # different sections
        sections_objects = self.draw_morphology_as_disconnected_sections(bevel_object=bevel_object)

        # Extend the morphology objects list
        morphology_objects.extend(sections_objects)

        # Draw the articulations
        # Draw the axon joints
        if not self.options.morphology.ignore_axon:
            axon_spheres_objects = []
            self.draw_section_terminals_as_spheres(
                root=self.morphology.axon,
                sphere_objects=axon_spheres_objects,
                max_branching_level=self.options.morphology.axon_branch_order,
                material_list=self.articulation_materials)

            # Extend the morphology objects list
            morphology_objects.extend(axon_spheres_objects)

        # Draw the basal dendrites joints
        if not self.options.morphology.ignore_basal_dendrites:

            # Ensure tha existence of basal dendrites
            if self.morphology.dendrites is not None:

                basal_dendrites_spheres_objects = []
                for i, basal_dendrite in enumerate(self.morphology.dendrites):

                    # Draw the basal dendrites as a set connected sections
                    self.draw_section_terminals_as_spheres(
                        root=basal_dendrite,
                        sphere_objects=basal_dendrites_spheres_objects,
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                        material_list=self.articulation_materials)

                # Extend the morphology objects list
                morphology_objects.extend(basal_dendrites_spheres_objects)

        # Draw the apical dendrite joints
        if not self.options.morphology.ignore_apical_dendrite:
            apical_dendrite_spheres_objects=[]
            self.draw_section_terminals_as_spheres(
                root=self.morphology.apical_dendrite,
                sphere_objects=apical_dendrite_spheres_objects,
                max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                material_list=self.articulation_materials)

            # Extend the morphology objects list
            morphology_objects.extend(apical_dendrite_spheres_objects)

        # Draw the frame for progressive rendering (for the articulations in a single frame)
        if self.options.morphology.render_progressive:
            frame_file_path = '%s/frame_%s' % (
                self.progressive_frames_directory, '{0:05d}'.format(self.progressive_frame_index))

            # Render the image to film
            # camera_ops.render_scene_to_image(self.progressive_rendering_camera, frame_file_path)

            self.progressive_frame_index += 1

        # Return a reference to the list of drawn objects
        return morphology_objects

    ################################################################################################
    # @draw_morphology_as_connected_sections
    ################################################################################################
    def draw_morphology_as_connected_sections(self,
                                              bevel_object=None,
                                              repair_morphology=False,
                                              disconnect_skelecton=False):
        """Reconstruct and draw the morphology as a series of connected sections.

        :param bevel_object:
            A bevel object used to scale the radii of the sections.
        :param repair_morphology:
            A flag to indicate whether we need to repair the morphology or not.
        :return:
            A list of all the objects of the morphology that are already drawn.
        """

        # Re-sample the morphology skeleton, if the repair is required
        if repair_morphology:

            # Remove the samples that intersect with the soma
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.remove_samples_inside_soma])

            # The adaptive resampling is quite important to prevent breaking the structure
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.resample_section_adaptively])

        # Verify the connectivity of the arbors of the morphology to the soma
        nmv.skeleton.ops.update_arbors_connection_to_soma(morphology=self.morphology)

        # Update the branching
        nmv.skeleton.ops.update_skeleton_branching(
            morphology=self.morphology, branching_method=self.options.morphology.branching)

        # Update the style of the arbors
        nmv.skeleton.ops.update_arbors_style(
            morphology=self.morphology, arbor_style=self.options.morphology.arbor_style)

        # Update the radii of the arbors
        nmv.skeleton.ops.update_arbors_radii(
            morphology=self.morphology, morphology_options=self.options.morphology)

        # A list of objects (references to drawn segments) that compose the morphology
        morphology_objects = []

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Ensure tha existence of basal dendrites
            if self.morphology.dendrites is not None:

                # A list to keep all the drawn objects of the basal dendrites
                basal_dendrites_sections_objects = []

                # Draw each basal dendrites as a set connected sections
                for i, basal_dendrite in enumerate(self.morphology.dendrites):

                    dendrite_prefix = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)
                    nmv.skeleton.ops.draw_connected_sections(
                        section=copy.deepcopy(basal_dendrite),
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                        name=dendrite_prefix,
                        material_list=self.basal_dendrites_materials,
                        bevel_object=bevel_object,
                        repair_morphology=repair_morphology,
                        caps=True,
                        sections_objects=basal_dendrites_sections_objects,
                        render_frame=self.options.morphology.render_progressive,
                        frame_destination=self.progressive_frames_directory,
                        camera=self.progressive_rendering_camera,
                        roots_connection=self.options.morphology.arbors_to_soma_connection,
                        ignore_branching_samples=disconnect_skelecton)

                # Extend the morphology objects list
                morphology_objects.extend(basal_dendrites_sections_objects)

        # Draw the apical dendrite
        if not self.options.morphology.ignore_apical_dendrite:

            # Ensure tha existence of the apical dendrite
            if self.morphology.apical_dendrite is not None:

                # Draw the apical dendrite as a set connected sections
                apical_dendrite_sections_objects = []
                nmv.skeleton.ops.draw_connected_sections(
                    section=copy.deepcopy(self.morphology.apical_dendrite),
                    max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                    name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                    material_list=self.apical_dendrite_materials,
                    bevel_object=bevel_object,
                    repair_morphology=repair_morphology,
                    caps=True,
                    sections_objects=apical_dendrite_sections_objects,
                    render_frame=self.options.morphology.render_progressive,
                    frame_destination=self.progressive_frames_directory,
                    camera=self.progressive_rendering_camera,
                    roots_connection=self.options.morphology.arbors_to_soma_connection,
                    ignore_branching_samples=disconnect_skelecton)

                # Extend the morphology objects list
                morphology_objects.extend(apical_dendrite_sections_objects)

        # Draw the axon
        if not self.options.morphology.ignore_axon:

            # Ensure tha existence of the axon
            if self.morphology.axon is not None:

                # Draw the axon as a set connected sections
                axon_sections_objects = []
                nmv.skeleton.ops.draw_connected_sections(
                    section=copy.deepcopy(self.morphology.axon),
                    max_branching_level=self.options.morphology.axon_branch_order,
                    name=nmv.consts.Arbors.AXON_PREFIX, material_list=self.axon_materials,
                    bevel_object=bevel_object,
                    repair_morphology=repair_morphology, caps=True,
                    sections_objects=axon_sections_objects,
                    render_frame=self.options.morphology.render_progressive,
                    frame_destination=self.progressive_frames_directory,
                    camera=self.progressive_rendering_camera,
                    roots_connection=self.options.morphology.arbors_to_soma_connection,
                    ignore_branching_samples=disconnect_skelecton)

                # Extend the morphology objects list
                morphology_objects.extend(axon_sections_objects)

        # Return a reference to the list of drawn objects
        return morphology_objects

    ################################################################################################
    # @draw_morphology_as_connected_sections
    ################################################################################################
    def draw_morphology_as_disconnected_skeleton(self,
                                                 bevel_object=None,
                                                 repair_morphology=False):
        """
        Reconstructs and draws the morphology as a series of connected sections.

        :param bevel_object: A bevel object used to scale the radii of the sections.
        :param repair_morphology: A flag to indicate whether we need to repair the morphology or
        not.
        :return: A list of all the objects of the morphology that are already drawn.
        """

        # Repair severe morphology artifacts if @repair_morphology is set
        if repair_morphology:

            # Repair the section which has single child only
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.repair_sections_with_single_child])

            # Remove duplicate samples
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.remove_duplicate_samples])

            # Repair the short sections
            # morphology_repair_ops.repair_short_sections_of_morphology(self.morphology)

        # Verify the connectivity of the arbors of the morphology to the soma
        nmv.skeleton.ops.update_arbors_connection_to_soma(self.morphology)

        # Primary and secondary branching
        if self.options.mesh.branching == nmv.enums.Skeletonization.Branching.ANGLES:

            # Label the primary and secondary sections based on angles
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_angles])

        else:

            # Label the primary and secondary sections based on radii
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_radii])

        # A list of objects (references to drawn segments) that compose the morphology
        morphology_objects = []

        # Draw the axon as a set connected sections
        if not self.options.morphology.ignore_axon:
            axon_sections_objects = []
            nmv.skeleton.ops.draw_connected_sections(
                section=copy.deepcopy(self.morphology.axon),
                max_branching_level=self.options.morphology.axon_branch_order,
                name=nmv.consts.Arbors.AXON_PREFIX,
                material_list=self.axon_materials,
                bevel_object=bevel_object,
                repair_morphology=repair_morphology,
                caps=True,
                sections_objects=axon_sections_objects,
                render_frame=self.options.morphology.render_progressive,
                frame_destination=self.progressive_frames_directory,
                camera=self.progressive_rendering_camera,
                roots_connection=self.options.morphology.arbors_to_soma_connection,
                ignore_branching_samples=True)

            # Extend the morphology objects list
            morphology_objects.extend(axon_sections_objects)

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            # Ensure tha existence of basal dendrites
            if self.morphology.dendrites is not None:

                basal_dendrites_sections_objects = []

                for i, basal_dendrite in enumerate(self.morphology.dendrites):

                    # Draw the basal dendrites as a set connected sections
                    dendrite_prefix = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)
                    nmv.skeleton.ops.draw_connected_sections(
                        section=copy.deepcopy(basal_dendrite),
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                        name=dendrite_prefix,
                        material_list=self.basal_dendrites_materials,
                        bevel_object=bevel_object,
                        repair_morphology=repair_morphology,
                        caps=True,
                        sections_objects=basal_dendrites_sections_objects,
                        render_frame=self.options.morphology.render_progressive,
                        frame_destination=self.progressive_frames_directory,
                        camera=self.progressive_rendering_camera,
                        roots_connection=self.options.morphology.arbors_to_soma_connection,
                        ignore_branching_samples=True)

                # Extend the morphology objects list
                morphology_objects.extend(basal_dendrites_sections_objects)

        # Draw the apical dendrite
        if not self.options.morphology.ignore_apical_dendrite:
            apical_dendrite_sections_objects = []
            nmv.skeleton.ops.draw_connected_sections(
                section=copy.deepcopy(self.morphology.apical_dendrite),
                max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                material_list=self.apical_dendrite_materials,
                bevel_object=bevel_object,
                repair_morphology=repair_morphology,
                caps=True,
                sections_objects=apical_dendrite_sections_objects,
                render_frame=self.options.morphology.render_progressive,
                frame_destination=self.progressive_frames_directory,
                camera=self.progressive_rendering_camera,
                roots_connection=self.options.morphology.arbors_to_soma_connection,
                ignore_branching_samples=True)

            # Extend the morphology objects list
            morphology_objects.extend(apical_dendrite_sections_objects)

        # Return a reference to the list of drawn objects
        return morphology_objects

    ################################################################################################
    # @transform_to_global_coordinates
    ################################################################################################
    def transform_soma_to_global_coordinates(self, soma_mesh):
        """Transform the soma to the global coordinates.
        """

        # Transform the neuron object to the global coordinates
        if self.options.morphology.global_coordinates:
            nmv.logger.header('Transforming soma to global coordinates')
            nmv.skeleton.ops.transform_to_global_coordinates(
                mesh_object=soma_mesh, blue_config=self.options.morphology.blue_config,
                gid=self.options.morphology.gid)

    ################################################################################################
    # @transform_arbors_to_global_coordinates
    ################################################################################################
    def transform_arbors_to_global_coordinates(self,
                                               arbors):
        if self.options.morphology.global_coordinates:
            nmv.logger.header('Transforming arbors to global coordinates')

            nmv.skeleton.ops.transform_morphology_to_global_coordinates(
                soma_mesh=None, arbors_list=arbors, blue_config=self.options.morphology.blue_config,
                gid=self.options.morphology.gid)

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self):
        """Reconstruct and draw the morphological skeleton using poly-lines.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        # This list has all the created and drawn objects that compose the morphology.
        # We must keep track on those objects to delete them upon request or when we need to use
        # a different morphology reconstruction technique
        morphology_objects = []

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')

        # Add the bevel object to the morphology objects because if this bevel is lost we will
        # lose the rounded structure of the arbors
        morphology_objects.append(bevel_object)

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        self.create_skeleton_materials()

        nmv.logger.header('Building skeleton')
        method = self.options.morphology.reconstruction_method

        # Draw the morphology as a set of disconnected tubes, where each SEGMENT is a tube
        if method == nmv.enums.Skeletonization.Method.DISCONNECTED_SEGMENTS:
            morphology_objects.extend(self.draw_morphology_as_disconnected_segments(
                bevel_object=bevel_object))

        # Draw the morphology as a set of disconnected tubes, where each SECTION is a tube
        elif method == nmv.enums.Skeletonization.Method.DISCONNECTED_SECTIONS:
            morphology_objects.extend(self.draw_morphology_as_disconnected_sections(
                bevel_object=bevel_object))

        # Draw the morphology as a set of samples
        elif method == nmv.enums.Skeletonization.Method.SAMPLES:
            morphology_objects.extend(self.draw_morphology_as_spheres())

        # Draw the morphology as a set of articulated tubes, where each SECTION is connected to
        # the following one by a sphere
        elif method == nmv.enums.Skeletonization.Method.ARTICULATED_SECTIONS:
            morphology_objects.extend(self.draw_morphology_as_articulated_sections(
                bevel_object=bevel_object))

        # Draw the morphology skeleton, where each arbor is disconnected at the bifurcating points
        elif method == nmv.enums.Skeletonization.Method.DISCONNECTED_SKELETON_ORIGINAL:
            morphology_objects.extend(self.draw_morphology_as_connected_sections(
                    bevel_object=bevel_object, repair_morphology=False, disconnect_skelecton=True))

        # Draw the morphology skeleton, where each arbor is disconnected at the bifurcating points
        elif method == nmv.enums.Skeletonization.Method.DISCONNECTED_SKELETON_REPAIRED:
            morphology_objects.extend(self.draw_morphology_as_connected_sections(
                bevel_object=bevel_object, repair_morphology=True, disconnect_skelecton=True))

        # Draw the morphology as a set of connected tubes, where each long SECTION along the arbor
        # is represented by a continuous tube
        elif method == nmv.enums.Skeletonization.Method.CONNECTED_SECTION_ORIGINAL:
            morphology_objects.extend(self.draw_morphology_as_connected_sections(
                bevel_object=bevel_object, repair_morphology=False))

        # Draw the full morphology as a set of connected tubes, where each long SECTION along the
        # arbor is represented by a continuous tube, and the roots are already connected to the
        # origin
        elif method == nmv.enums.Skeletonization.Method.CONNECTED_SECTION_REPAIRED:
            morphology_objects.extend(self.draw_morphology_as_connected_sections(
                bevel_object=bevel_object, repair_morphology=True))

        # By default, use the full morphology method
        else:
            morphology_objects.extend(self.draw_morphology_as_disconnected_sections(
                bevel_object=bevel_object))

        # Hide the bevel object to avoid having it rendered
        bevel_object.hide = True

        # Draw the soma as a sphere object
        if self.options.morphology.soma_representation == nmv.enums.Soma.Representation.SPHERE:

            # Draw the soma sphere
            soma_sphere = self.draw_soma_sphere()

            # Smooth shade the sphere to look nice
            nmv.mesh.ops.shade_smooth_object(soma_sphere)

            # Add the soma sphere to the morphology objects to keep track on it
            morphology_objects.append(soma_sphere)

        # Or as a reconstructed profile using the soma builder
        elif self.options.morphology.soma_representation == nmv.enums.Soma.Representation.REALISTIC:

            # Create a soma builder object
            soma_builder_object = nmv.builders.SomaBuilder(self.morphology, self.options)

            # Reconstruct the three-dimensional profile of the soma mesh without applying the
            # default shader to it,
            # since we need to use the shader specified in the morphology options
            soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

            # Apply the shader given in the morphology options, not the one in the soma toolbox
            nmv.shading.set_material_to_object(soma_mesh, self.soma_materials[0])

            # Add the soma mesh to the morphology objects
            morphology_objects.append(soma_mesh)

        # Otherwise, ignore the soma drawing
        else:
            nmv.logger.log('Ignoring soma representation')

        # Transform the arbors to the global coordinates if required for a circuit
        if self.options.morphology.global_coordinates and           \
                self.options.morphology.blue_config is not None and \
                self.options.morphology.gid is not None:

            # Transforming
            nmv.logger.log('Transforming morphology to global coordinates ')
            nmv.skeleton.ops.transform_morphology_to_global_coordinates(
                morphology_objects=morphology_objects,
                blue_config=self.options.morphology.blue_config,
                gid=self.options.morphology.gid)

        # Return the list of the drawn morphology objects
        return morphology_objects

