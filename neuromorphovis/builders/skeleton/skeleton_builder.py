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
# System imports
import random, copy

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.file
import neuromorphovis.builders
import neuromorphovis.geometry
import neuromorphovis.mesh
import neuromorphovis.scene
import neuromorphovis.shading
import neuromorphovis.skeleton


####################################################################################################
# @SkeletonBuilder
####################################################################################################
class SkeletonBuilder:
    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """
        Constructor.

        :param morphology: A given morphology.
        """

        # Morphology
        self.morphology = morphology

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

        # The directory where the progressive frames will be dumped
        self.progressive_frames_directory = None

        # Progressive rendering camera
        self.progressive_rendering_camera = None

        # Progressive rendering frame index, starts from 1 since the soma will be 0
        self.progressive_frame_index = 1

    ################################################################################################
    # @create_materials
    ################################################################################################
    def create_materials(self,
                         name,
                         color):
        """
        Creates just two materials of the skeleton based on the input parameters of the user.

        :param name: The name of the material/color.
        :param color: The code of the given colors.
        :return: A list of two elements (different or same colors) where we can apply later to
        the drawn sections or segments.
        """

        # A list of the created materials
        materials_list = []

        # Build the materials list
        color_vector = Vector((0.0, 0.0, 0.0))

        # Random colors
        if color.x == -1 and color.y == 0 and color.z == 0:
            for i in range(2):
                color_vector.x = random.uniform(0.0, 1.0)
                color_vector.y = random.uniform(0.0, 1.0)
                color_vector.z = random.uniform(0.0, 1.0)

                # Create the material
                material = nmv.shading.create_material(
                    name='%s_random_%d' % (name, i), color=color_vector,
                    material_type=self.options.morphology.material)

                # Append the material to the materials list
                materials_list.append(material)

        # If set to black / white
        elif color.x == 0 and color.y == -1 and color.z == 0:

            # Black
            color_vector.x = 0.0
            color_vector.y = 0.0
            color_vector.z = 0.0

            # Create the material
            material = nmv.shading.create_material(
                name='%s_bw_0' % name, color=color_vector,
                material_type=self.options.morphology.material)

            # Append the material to the materials list
            materials_list.append(material)

            # White
            color_vector.x = 1.0
            color_vector.y = 1.0
            color_vector.z = 1.0

            # Create the material
            material = nmv.shading.create_material(
                name='%s_bw_1' % name, color=color_vector,
                material_type=self.options.morphology.material)

            # Append the material to the materials list
            materials_list.append(material)

        # Normal color
        else:
            for i in range(2):

                # Create the material
                material = nmv.shading.create_material(
                    name='%s_color_%d' % (name, i), color=color,
                    material_type=self.options.morphology.material)

                # Append the material to the materials list
                materials_list.append(material)

        # Return the list
        return materials_list

    ################################################################################################
    # @create_skeleton_materials
    ################################################################################################
    def create_skeleton_materials(self):
        """
        Creates the materials of the skeleton. The created materials are stored in private
        variables.
        """

        for material in bpy.data.materials:
            if 'soma_skeleton' in material.name or \
               'axon_skeleton' in material.name or \
               'basal_dendrites_skeleton' in material.name or \
               'apical_dendrite_skeleton' in material.name:
                    material.user_clear()
                    bpy.data.materials.remove(material)

        # Soma
        self.soma_materials = self.create_materials(
            name='soma_skeleton', color=self.options.morphology.soma_color)

        # Axon
        self.axon_materials = self.create_materials(
            name='axon_skeleton', color=self.options.morphology.axon_color)

        # Basal dendrites
        self.basal_dendrites_materials = self.create_materials(
            name='basal_dendrites_skeleton', color=self.options.morphology.basal_dendrites_color)

        # Apical dendrite
        self.apical_dendrite_materials = self.create_materials(
            name='apical_dendrite_skeleton', color=self.options.morphology.apical_dendrites_color)

    ################################################################################################
    # @draw_soma_sphere
    ################################################################################################
    def draw_soma_sphere(self):
        """
        Draws a sphere that represents the soma.
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
    # @get_section_poly_line
    ################################################################################################
    def get_section_poly_line(self,
                              section):
        """
        Gets the data of a morphological section arranged in a certain format that can be easily
        read by the poly-line drawing functions.

        :param section: The geometry of a morphological section.
        :return: A data list that includes the samples of the sections and their corresponding
        diameters.
        """

        # An array containing the data of the section
        poly_line_data = None

        # If we use a fixed radius, then get that radius from the user and set all the radii of
        # the sections to it
        if self.options.morphology.unify_sections_radii:
            poly_line_data = nmv.skeleton.ops.get_section_poly_line(
                section=section, fixed_radius=self.options.morphology.sections_fixed_radii_value)

        # Otherwise, use the radii that are given in the morphology file
        else:
            poly_line_data = nmv.skeleton.ops.get_section_poly_line(section=section)

        # Return the list
        return poly_line_data

    ################################################################################################
    # @draw_section_terminal_as_sphere
    ################################################################################################
    def draw_section_terminal_as_sphere(self,
                                        section,
                                        color=None):
        """
        Draws a joint between the different sections along the arbor.

        :param section: Section geometry.
        :param color: Section color.
        """

        # Get the section data arranged in a poly-line format
        section_data = self.get_section_poly_line(section)

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
            child_data = self.get_section_poly_line(child)

            # Verify the radius of the child
            child_radius = child_data[0][1]

            # If the radius of the child is bigger, then set the radius of the joint to the
            # radius of the child
            if child_radius > radius:
                radius = child_radius

        # If we scale the morphology, we should account for that in the spheres to
        sphere_radius = radius
        if self.options.morphology.scale_sections_radii:
            sphere_radius *= self.options.morphology.sections_radii_scale
        elif self.options.morphology.unify_sections_radii:
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
        """
        Draws the terminals of a given arbor as spheres.

        :param root: Arbor root.
        :param material_list: Sphere material.
        :param sphere_objects: A list of all the drawn spheres.
        :param branching_level: Current branching level.
        :param max_branching_level: Maximum branching level the section can grow up to: infinity.
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
                self.draw_section_terminals_as_spheres(child, sphere_objects=sphere_objects,
                    material_list=material_list, branching_level=branching_level,
                    max_branching_level=max_branching_level)

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
        """
        Draw the sections in each arbor as a series of disconnected segments, where each segment is
        represented by a tube.

        :param root: Arbor root.
        :param name: Arbor name.
        :param material_list: Arbor colors.
        :param segments_objects: The drawn list of segments.
        :param branching_level: Current branching level.
        :param max_branching_level: Maximum branching level the section can grow up to: infinity.
        :param bevel_object: A given bevel object to scale the arbor sections.
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
                    child, branching_level=branching_level, max_branching_level=max_branching_level,
                    name=name, material_list=material_list, bevel_object=bevel_object,
                    segments_objects=segments_objects)

    ################################################################################################
    # @draw_section_as_disconnected_object
    ################################################################################################
    def draw_section_as_disconnected_object(self,
                                            section,
                                            name,
                                            material_list=None,
                                            bevel_object=None):
        """
        Draws the section as a tube object.

        :param section: The geometry of a morphological section.
        :param name: The name of the section.
        :param material_list: The color of the section.
        :param bevel_object: A given bevel object to scale the section.
        """

        # Get the section data arranged in a poly-line format
        data = self.get_section_poly_line(section)

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
            #camera_ops.render_scene_to_image(self.progressive_rendering_camera, frame_file_path)

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
        """
        Draws the section as a continuous, yet, disconnected and independent object from the rest
        of the sections of the morphology.

        :param root: Arbor root.
        :param name: Arbor prefix.
        :param material_list: Arbor colors.
        :param sections_objects: A list of all the drawn sections in the morphology.
        :param branching_level: Current branching level.
        :param max_branching_level: Maximum branching level set by the user.
        :param bevel_object: A given bevel object to scale the arbor sections.
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
                    root=child, name=name, material_list=material_list,
                    branching_level=branching_level, max_branching_level=max_branching_level,
                    bevel_object=bevel_object, sections_objects=sections_objects)

    ################################################################################################
    # @draw_morphology_as_disconnected_segments
    ################################################################################################
    def draw_morphology_as_disconnected_segments(self,
                                                 bevel_object=None):
        """
        Draw the morphological arbors as a set of disconnected segments.

        :param bevel_object: A given bevel object to scale the samples.
        :return A list of all the drawn objects
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
        """
        Draw the morphological arbors as a set of disconnected sections.

        :param bevel_object: A given bevel object to scale the samples.
        :return A list of all the drawn objects in the morphology.
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

        """
        Reconstructs and draws the morphology as a series of articulated sections.

        :param bevel_object: A bevel object used to scale the radii of the sections.
        :return: A list of all the objects of the morphology that are already drawn.
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
                material_list=self.axon_materials)

            # Extend the morphology objects list
            morphology_objects.extend(axon_spheres_objects)

        # Draw the basal dendrites joints
        if not self.options.morphology.ignore_basal_dendrites:
            basal_dendrites_spheres_objects = []
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                # Draw the basal dendrites as a set connected sections
                self.draw_section_terminals_as_spheres(
                    root=basal_dendrite,
                    sphere_objects=basal_dendrites_spheres_objects,
                    max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                    material_list=self.basal_dendrites_materials)

            # Extend the morphology objects list
            morphology_objects.extend(basal_dendrites_spheres_objects)

        # Draw the apical dendrite joints
        if not self.options.morphology.ignore_apical_dendrite:
            apical_dendrite_spheres_objects=[]
            self.draw_section_terminals_as_spheres(
                root=self.morphology.apical_dendrite,
                sphere_objects=apical_dendrite_spheres_objects,
                max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                material_list=self.apical_dendrite_materials)

            # Extend the morphology objects list
            morphology_objects.extend(apical_dendrite_spheres_objects)

        # Draw the frame for progressive rendering (for the articulations in a single frame)
        if self.options.morphology.render_progressive:
            frame_file_path = '%s/frame_%s' % (
                self.progressive_frames_directory, '{0:05d}'.format(self.progressive_frame_index))

            # Render the image to film
            #camera_ops.render_scene_to_image(self.progressive_rendering_camera, frame_file_path)

            self.progressive_frame_index += 1

        # Return a reference to the list of drawn objects
        return morphology_objects

    ################################################################################################
    # @draw_morphology_as_connected_sections
    ################################################################################################
    def draw_morphology_as_connected_sections(self,
                                              bevel_object=None,
                                              repair_morphology=False,
                                              taper_sections=False,
                                              zigzag_sections=False):
        """
        Reconstructs and draws the morphology as a series of connected sections.

        :param bevel_object:
            A bevel object used to scale the radii of the sections.
        :param repair_morphology:
            A flag to indicate whether we need to repair the morphology or not.
        :param taper_sections:
            A flag to indicate whether to taper the sections for artistic purposes or not.
        :param zigzag_sections:
            A flag to indicate whether to add abrupt left and right wiggles to the sections for
            artistic purposes or not.
        :return:
            A list of all the objects of the morphology that are already drawn.
        """

        # Verify the connectivity of the arbors of the morphology to the soma
        # nmv.skeleton.ops.update_arbors_connection_to_soma(self.morphology)

        # Primary and secondary branching
        if self.options.morphology.branching == nmv.enums.Skeletonization.Branching.ANGLES:

            # Label the primary and secondary sections based on angles
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_angles])
        else:

            # Label the primary and secondary sections based on radii
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_radii])

        # Resample the morphology skeleton, if the repair is required
        if repair_morphology:

            # Resample the sections
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.resample_sections])

        # Taper the sections if requested
        if self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED or \
           self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED_ZIGZAG:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.taper_section])

        # Zigzag the sections if required
        if self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.ZIGZAG or \
           self.options.mesh.skeletonization == nmv.enums.Meshing.Skeleton.TAPERED_ZIGZAG:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.zigzag_section])

        # Verify the fixed radius options
        fixed_radius = self.options.morphology.sections_fixed_radii_value \
            if self.options.morphology.unify_sections_radii else None

        # A list of objects (references to drawn segments) that compose the morphology
        morphology_objects = []

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            basal_dendrites_sections_objects = []
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                # Draw the basal dendrites as a set connected sections
                dendrite_prefix = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)
                nmv.skeleton.ops.draw_connected_sections(
                    section=copy.deepcopy(basal_dendrite),
                    max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                    name=dendrite_prefix,
                    material_list=self.basal_dendrites_materials,
                    fixed_radius=fixed_radius,
                    bevel_object=bevel_object,
                    repair_morphology=repair_morphology,
                    caps=True,
                    sections_objects=basal_dendrites_sections_objects,
                    render_frame=self.options.morphology.render_progressive,
                    frame_destination=self.progressive_frames_directory,
                    camera=self.progressive_rendering_camera,
                    connect_to_soma=self.options.morphology.connect_to_soma)

            # Extend the morphology objects list
            morphology_objects.extend(basal_dendrites_sections_objects)

        # Draw the apical dendrite
        if not self.options.morphology.ignore_apical_dendrite:

            if self.morphology.apical_dendrite is not None:

                apical_dendrite_sections_objects = []
                nmv.skeleton.ops.draw_connected_sections(
                    section=copy.deepcopy(self.morphology.apical_dendrite),
                    max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                    name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                    material_list=self.apical_dendrite_materials,
                    fixed_radius=fixed_radius,
                    bevel_object=bevel_object,
                    repair_morphology=repair_morphology,
                    caps=True,
                    sections_objects=apical_dendrite_sections_objects,
                    render_frame=self.options.morphology.render_progressive,
                    frame_destination=self.progressive_frames_directory,
                    camera=self.progressive_rendering_camera,
                    connect_to_soma=self.options.morphology.connect_to_soma)

                # Extend the morphology objects list
                morphology_objects.extend(apical_dendrite_sections_objects)

        # Draw the axon as a set connected sections
        if not self.options.morphology.ignore_axon:

            if self.morphology.axon is not None:

                axon_sections_objects = []
                nmv.skeleton.ops.draw_connected_sections(
                    section=copy.deepcopy(self.morphology.axon),
                    max_branching_level=self.options.morphology.axon_branch_order,
                    name=nmv.consts.Arbors.AXON_PREFIX, material_list=self.axon_materials,
                    fixed_radius=fixed_radius, bevel_object=bevel_object,
                    repair_morphology=repair_morphology, caps=True,
                    sections_objects=axon_sections_objects,
                    render_frame=self.options.morphology.render_progressive,
                    frame_destination=self.progressive_frames_directory,
                    camera=self.progressive_rendering_camera,
                    connect_to_soma=self.options.morphology.connect_to_soma)

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

        # Repair severe morphology artifacts if @repair_morphology is set
        #if repair_morphology:

        # Re-sample the morphology for disconnected skeleton
        #resampler = disconnected_morphology_resampler.DisconnectedSkeletonResampler()
        #resampler.resample_morphology(self.morphology)

        # A list of objects (references to drawn segments) that compose the morphology
        morphology_objects = []

        # Verify the fixed radius options
        fixed_radius = self.options.morphology.sections_fixed_radii_value \
            if self.options.morphology.unify_sections_radii else None

        # Draw the axon as a set connected sections
        if not self.options.morphology.ignore_axon:
            axon_sections_objects = []
            nmv.skeleton.ops.draw_disconnected_skeleton_sections(
                section=copy.deepcopy(self.morphology.axon),
                max_branching_level=self.options.morphology.axon_branch_order,
                name=nmv.consts.Arbors.AXON_PREFIX,
                material_list=self.axon_materials,
                fixed_radius=fixed_radius,
                bevel_object=bevel_object,
                repair_morphology=repair_morphology,
                caps=False,
                sections_objects=axon_sections_objects,
                render_frame=self.options.morphology.render_progressive,
                frame_destination=self.progressive_frames_directory,
                camera=self.progressive_rendering_camera,
                extend_to_soma_origin=self.options.morphology.connect_to_soma)

            # Extend the morphology objects list
            morphology_objects.extend(axon_sections_objects)

        # Draw the basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:

            basal_dendrites_sections_objects = []
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                # Draw the basal dendrites as a set connected sections
                dendrite_prefix = '%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)
                nmv.skeleton.ops.draw_disconnected_skeleton_sections(
                    section=copy.deepcopy(basal_dendrite),
                    max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                    name=dendrite_prefix,
                    material_list=self.basal_dendrites_materials,
                    fixed_radius=fixed_radius,
                    bevel_object=bevel_object,
                    repair_morphology=repair_morphology,
                    caps=False,
                    sections_objects=basal_dendrites_sections_objects,
                    render_frame=self.options.morphology.render_progressive,
                    frame_destination=self.progressive_frames_directory,
                    camera=self.progressive_rendering_camera,
                    extend_to_soma_origin=self.options.morphology.connect_to_soma)

            # Extend the morphology objects list
            morphology_objects.extend(basal_dendrites_sections_objects)

        # Draw the apical dendrite
        if not self.options.morphology.ignore_apical_dendrite:
            apical_dendrite_sections_objects = []
            nmv.skeleton.ops.draw_disconnected_skeleton_sections(
                section=copy.deepcopy(self.morphology.apical_dendrite),
                max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                material_list=self.apical_dendrite_materials,
                fixed_radius=fixed_radius,
                bevel_object=bevel_object,
                repair_morphology=repair_morphology,
                caps=False,
                sections_objects=apical_dendrite_sections_objects,
                render_frame=self.options.morphology.render_progressive,
                frame_destination=self.progressive_frames_directory,
                camera=self.progressive_rendering_camera,
                extend_to_soma_origin=self.options.morphology.connect_to_soma)

            # Extend the morphology objects list
            morphology_objects.extend(apical_dendrite_sections_objects)

        # Return a reference to the list of drawn objects
        return morphology_objects

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self):
        """
        This function draws the morphological skeleton
        :return A list of all the drawn morphology objects.
        """
        """
        morphology_ops.apply_operation_to_morphology(
            *[self.morphology,
              morphology_ops.verify_number_of_samples_per_section])

        morphology_ops.apply_operation_to_morphology(
            *[self.morphology,
              morphology_ops.verify_number_of_children])

        morphology_ops.apply_operation_to_morphology(
            *[self.morphology,
              morphology_ops.verify_radii_at_branching_points])

        morphology_ops.apply_operation_to_morphology(
            *[self.morphology,
              morphology_ops.verify_duplicated_samples])
        """

        # nmv.skeleton.ops.update_arbors_connection_to_soma(self.morphology)

        # This list has all the created and drawn objects that compose the morphology.
        # We must keep track on those objects to delete them upon request or when we need to use
        # a different morphology reconstruction technique
        morphology_objects = []

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology
        bevel_object = None
        if self.options.morphology.scale_sections_radii:
            bevel_object = nmv.mesh.create_bezier_circle(
                radius=self.options.morphology.sections_radii_scale,
                vertices=self.options.morphology.bevel_object_sides, name='bevel')
        else:
            bevel_object = nmv.mesh.create_bezier_circle(radius=1.0,
                vertices=self.options.morphology.bevel_object_sides, name='bevel')

        # Add the bevel object to the morphology objects
        morphology_objects.append(bevel_object)

        # Skeletonize based on the selected method
        method = self.options.morphology.reconstruction_method

        # NOTE: Before drawing the skeleton, create the materials once and for all to improve the
        # performance since this is way better than creating a new material per section or segment
        self.create_skeleton_materials()

        # Draw the soma as a sphere object
        if self.options.morphology.soma_representation == nmv.enums.Soma.Representation.SPHERE:

            # Draw the soma
            soma_sphere = self.draw_soma_sphere()

            # Add the bevel object to the morphology objects
            morphology_objects.append(soma_sphere)

        # Or as a reconstructed profile using the soma builder
        elif self.options.morphology.soma_representation == nmv.enums.Soma.Representation.REALISTIC:

            # Create a soma builder object
            soma_builder_object = nmv.builders.SomaBuilder(self.morphology, self.options)

            # Reconstruct the three-dimensional profile of the soma mesh without applying the
            # default shader to it, since we need to use the shader specified in the morphology
            # options
            soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

            # Apply the shader given in the morphology options
            nmv.shading.set_material_to_object(soma_mesh, self.soma_materials[0])

            # Add the soma mesh to the morphology objects
            morphology_objects.append(soma_mesh)

        # Otherwise, ignore the soma drawing
        else:
            nmv.logger.log('Ignoring soma representation')

        """
        # If morphology progressive rendering is enabled, create the directory here and render a
        # frame following the reconstruction of each piece of the morphology.
        if self.options.morphology.render_progressive:

            # Create a directory where the sequence frames will be generated
            self.progressive_frames_directory = '%s/%s_morphology_progressive' % (
                self.options.output.sequences_directory, self.options.morphology.label)
            nmv.file.ops.clean_and_create_directory(self.progressive_frames_directory)

            # Set camera location and target based on the selected view to render the images
            morphology_bbox = self.morphology.bounding_box
            center = morphology_bbox.center
            camera_z = morphology_bbox.p_max[2] + morphology_bbox.bounds[2]
            camera_location_z = Vector((center.x, center.y, camera_z))

            # Add a camera along the z-axis
            self.progressive_rendering_camera = camera_ops.add_camera(location=camera_location_z)

            # Rotate the camera
            camera_ops.rotate_camera_for_front_view(camera=self.progressive_rendering_camera)

            # Update the camera resolution.
            camera_ops.set_camera_resolution_for_specific_view(
                camera=self.progressive_rendering_camera,
                resolution=self.options.morphology.full_view_resolution, view='FRONT',
                bounds=morphology_bbox.bounds)

            # Draw the first frame for the soma
            # The file path of the frame
            frame_file_path = '%s/frame_%s' % (
                self.progressive_frames_directory, '{0:05d}'.format(0))

            # Render the image to film
            camera_ops.render_scene_to_image(self.progressive_rendering_camera, frame_file_path)
        """
        nmv.logger.log('**************************************************************************')
        nmv.logger.log('Building skeleton')
        nmv.logger.log('**************************************************************************')

        """
        # Remove duplicate samples
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.ops.verify_segments_length_wrt_radius])

        # Remove duplicate samples
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.ops.remove_duplicate_samples, 0.5])

        nmv.logger.log('after')
        # Remove duplicate samples
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.ops.verify_segments_length_wrt_radius])

        # Get a list of short sections and connect them to the parents
        short_sections_list = list()
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.ops.verify_short_sections_and_return_them,
              short_sections_list])
        
        for short_section in short_sections_list:
            nmv.skeleton.ops.repair_short_sections_by_connection_to_child(section=short_section)
        """
        # Draw the morphology as a set of disconnected tubes, where each SEGMENT is a tube
        if method == nmv.enums.Skeletonization.Method.DISCONNECTED_SEGMENTS:
            morphology_objects.extend(self.draw_morphology_as_disconnected_segments(
                bevel_object=bevel_object))

        # Draw the morphology skeleton, where each arbor is disconnected at the bifurcating points
        elif method == nmv.enums.Skeletonization.Method.DISCONNECTED_SKELETON_ORIGINAL:
            morphology_objects.extend(self.draw_morphology_as_disconnected_skeleton(
                bevel_object=bevel_object, repair_morphology=False))

        # Draw the morphology skeleton, where each arbor is disconnected at the bifurcating points
        elif method == nmv.enums.Skeletonization.Method.DISCONNECTED_SKELETON_REPAIRED:
            morphology_objects.extend(self.draw_morphology_as_disconnected_skeleton(
                bevel_object=bevel_object, repair_morphology=True))

        # Draw the morphology as a set of disconnected tubes, where each SECTION is a tube
        elif method == nmv.enums.Skeletonization.Method.DISCONNECTED_SECTIONS:
            morphology_objects.extend(self.draw_morphology_as_disconnected_sections(
                bevel_object=bevel_object))

        # Draw the morphology as a set of articulated tubes, where each SECTION is connected to
        # the following one by a sphere
        elif method == nmv.enums.Skeletonization.Method.ARTICULATED_SECTIONS:
            morphology_objects.extend(self.draw_morphology_as_articulated_sections(
                bevel_object=bevel_object))

        # Change the structure of the morphology for artistic purposes
        elif method == nmv.enums.Skeletonization.Method.TAPERED:
            morphology_objects.extend(self.draw_morphology_as_connected_sections(
                bevel_object=bevel_object, repair_morphology=True, taper_sections=True))

        # Change the structure of the morphology for artistic purposes
        elif method == nmv.enums.Skeletonization.Method.TAPERED_ZIGZAG:
            morphology_objects.extend(self.draw_morphology_as_connected_sections(
                bevel_object=bevel_object, repair_morphology=True,
                taper_sections=True, zigzag_sections=True))

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
            morphology_objects.extend(self.draw_morphology_as_connected_sections(
                bevel_object=bevel_object, repair_morphology=True))

        # Hide the bevel object to avoid having it rendered
        bevel_object.hide = True

        # Delete the progressive camera if it was used during the reconstruction
        if self.progressive_rendering_camera is not None:
            nmv.scene.ops.delete_list_objects([self.progressive_rendering_camera])

        # Return the list of the drawn morphology objects
        return morphology_objects

