####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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

# System imports
import random
import copy

# Blender imports
import bpy
from mathutils import Vector

import nmv.consts
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities
import nmv.geometry
import nmv.mesh


####################################################################################################
# @RandomSpineBuilder
####################################################################################################
class RandomSpineBuilderFromMorphology:
    """This builder creates the skeletons of the spines that will be used in the MetaBuilder to
    integrate spines into neuron meshes.

    NOTE: The spines being built here are random and do not correspond to neither a real or
    simulated circuit.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology skeleton to create the mesh for.
        :param options:
            Loaded options from NeuroMorphoVis.
        """

        # Neuron morphology
        self.neuron_morphology = morphology

        # Loaded options from NeuroMorphoVis
        self.options = options

        # A list of all the templates that we can use to build the morphology
        self.spine_template_structures = list()

        # Construct a bevel object that will be used to build the spines
        self.bevel_object = nmv.mesh.create_bezier_circle(radius=1.0,
                                                          vertices=8,
                                                          name='spines_bevel')

        # Build the spine template structures
        self.build_spines_template_structures()

    ################################################################################################
    # @build_spine_structure
    ################################################################################################
    def build_spine_structure(self, spine_morphology):

        # A list of poly-lines
        spine_poly_lines = list()

        # Construct the polyline format
        for section in spine_morphology.sections:
            spine_poly_lines.append(nmv.geometry.PolyLine(
                samples=nmv.skeleton.ops.get_section_poly_line(section=section)))

        # Draw the poly-lines
        spine_structure = nmv.geometry.ops.draw_poly_lines_in_single_object(
            poly_lines=spine_poly_lines, bevel_object=self.bevel_object, poly_line_caps=False)

        # Return a reference to the spine template
        return spine_structure

    ################################################################################################
    # @build_spines_template_structures
    ################################################################################################
    def build_spines_template_structures(self):

        # Load the template spines
        template_spines_morphologies = nmv.file.load_spine_morphologies_from_data_files(
            nmv.consts.Paths.SIMPLE_SPINES_MORPHOLOGIES_DIRECTORY)

        # Build structures from the template morphologies
        for template_morphology in template_spines_morphologies:
            self.spine_template_structures.append(self.build_spine_structure(
                spine_morphology=template_morphology))

    ################################################################################################
    # @get_spine_morphologies_for_arbor
    ################################################################################################
    def get_spine_morphologies_for_arbor(self, arbor, number_spines_per_micron):

        spine_morphologies = list()

        # Get the normals along the segments along the arbors
        nmv.skeleton.ops.apply_operation_to_arbor(
            *[arbor,
              nmv.skeleton.ops.get_random_spines_across_section,
              self.spine_template_structures,
              number_spines_per_micron,
              spine_morphologies])

        # Return a list of spine morphologies (samples and radii) that can be used to draw
        # the spine in the scene at the respective locations
        return spine_morphologies

    ################################################################################################
    # @clean_unwanted_data
    ################################################################################################
    def clean_unwanted_data(self):

        nmv.scene.delete_list_objects(self.spine_template_structures)
        nmv.scene.delete_object_in_scene(self.bevel_object)














    ################################################################################################
    # @load_spine_meshes
    ################################################################################################
    def emanate_spine_from_face(self,
                                dendrite_samples,
                                dendrite_mesh,
                                face_index, index):

        # Create the spine
        spine = nmv.skeleton.Spine()
        spine.post_synaptic_position = dendrite_mesh.data.polygons[face_index].center
        spine.pre_synaptic_position = dendrite_mesh.data.polygons[face_index].center + \
                                      1.0 * dendrite_mesh.data.polygons[face_index].normal

        lenght = 1e5
        for i_sample in dendrite_samples:
            distance = (i_sample.point - spine.post_synaptic_position).length

            if distance < lenght:
                spine.size = i_sample.radius * 3

        # Select a random spine from the spines list
        spine_template = random.choice(self.spine_meshes)

        # Get a copy of the template and update it
        spine_object = nmv.scene.ops.duplicate_object(spine_template, index)

        # Rename the spine
        spine_object.name = '%s_spine_%d' % (self.options.morphology.label, index)

        # Scale the spine
        spine_scale = spine.size
        nmv.scene.ops.scale_object_uniformly(spine_object, spine_scale)

        # Translate the spine to the post synaptic position
        nmv.scene.ops.set_object_location(spine_object, spine.post_synaptic_position)

        # Rotate the spine towards the pre-synaptic point
        #nmv.scene.ops.rotate_object_towards_target(
        #    spine_object, spine.post_synaptic_position, spine.pre_synaptic_position)

        # Rotate it
        nmv.scene.ops.rotate_object_towards_target(
            spine_object, Vector((0, 0, -1)), spine.pre_synaptic_position)

    ################################################################################################
    # @load_spine_meshes
    ################################################################################################
    def load_spine_meshes(self):
        """Loads all the spine meshes from the spines directory

        :return:
        """
        # Load all the template spines and ignore the verbose messages of loading
        nmv.utilities.disable_std_output()
        self.spine_meshes = nmv.file.load_spines(nmv.consts.Paths.SPINES_MESHES_LQ_DIRECTORY)
        nmv.utilities.enable_std_output()

        # Create the material
        material = nmv.shading.create_material(
            name='%spine_material', color=self.options.shading.mesh_spines_color,
            material_type=self.options.shading.mesh_material)

        # Apply the shader
        for spine_object in self.spine_meshes:

            # Apply the shader to each spine mesh
            nmv.shading.set_material_to_object(spine_object, material)

    ################################################################################################
    # @emanate_spine
    ################################################################################################
    def emanate_spine(self,
                      spine,
                      index):
        """Emanates a spine at a random position on the dendritic tree.

        :param spine:
            A given spine object that contains all the data required to emanate the spine.
        :param index:
            Spine identifier.
        :return:
            The mesh instance that correspond to the spines.
        """

        # Select a random spine from the spines list
        spine_template = random.choice(self.spine_meshes)

        # Get a copy of the template and update it
        spine_object = nmv.scene.ops.duplicate_object(spine_template, index)

        # Rename the spine
        spine_object.name = '%s_spine_%d' % (self.options.morphology.label, index)

        # Scale the spine
        spine_scale = spine.size * random.uniform(1.25, 1.5)
        nmv.scene.ops.scale_object_uniformly(spine_object, spine_scale)

        # Translate the spine to the post synaptic position
        nmv.scene.ops.set_object_location(spine_object, spine.post_synaptic_position)

        # Rotate the spine towards the pre-synaptic point
        nmv.scene.ops.rotate_object_towards_target(
            spine_object, Vector((0, 0, -1)),
            spine.pre_synaptic_position * (1 if random.random() < 0.5 else -1))

        # Adjust the shading
        nmv.shading.adjust_material_uv(spine_object, 5)

        # Return a reference to the spine
        return spine_object

    ################################################################################################
    # @add_spines_to_morphology
    ################################################################################################
    def add_spines_to_morphology(self):
        """Add the spines randomly to the morphology.

        :return:
            A list of meshes that correspond to the spines integrated on the morphology.
        """

        # A list of the data of all the spines that will be added to the neuron morphology
        spines_list = list()

        # Remove the internal samples, or the samples that intersect the soma at the first
        # section and each arbor
        nmv.skeleton.ops.apply_operation_to_morphology_partially(
            *[self.morphology,
              self.options.morphology.axon_branch_order,
              self.options.morphology.basal_dendrites_branch_order,
              self.options.morphology.apical_dendrite_branch_order,
              nmv.skeleton.ops.get_random_spines_on_section,
              self.options.mesh.random_spines_percentage,
              spines_list])

        # Keep a list of all the spines objects
        spines_objects = []

        # Load all the template spines and ignore the verbose messages of loading
        self.load_spine_meshes()

        nmv.logger.info('Cloning and integrating spines')
        building_timer = nmv.utilities.timer.Timer()
        building_timer.start()

        # Load the synapses from the file
        number_spines = len(spines_list)
        for i, spine in enumerate(spines_list):

            # Show progress
            nmv.utilities.time_line.show_iteration_progress('\t* Spines', i, number_spines)

            # Emanate a spine
            spine_object = self.emanate_spine(spine, i)

            # Add the object to the list
            spines_objects.append(spine_object)

        # Done
        nmv.utilities.time_line.show_iteration_progress(
            '\t* Spines', number_spines, number_spines, done=True)

        # Report the time
        building_timer.end()
        nmv.logger.info('Spines: [%f] seconds' % building_timer.duration())

        # Delete the template spines
        nmv.scene.ops.delete_list_objects(self.spine_meshes)

        # Return the spines objects list
        return spines_objects

    def build_spine(self):
        # spine file
        spine_file = '/blender/neuromorphovis-blender-2.82/blender-neuromorphovis/2.82/scripts/addons/neuromorphovis/data/spines-morphologies/spine-4.dat'

        # spine morphology
        spine_poly_line_data = list()

        # read spine
        f = open(spine_file, 'r')
        for line in f:
            # extract the data
            data = line.split(' ')
            x = float(data[0])
            y = float(data[1])
            z = float(data[2])
            r = float(data[3]) * 0.5

            # construct the polyline data
            spine_poly_line_data.append([(x, y, z, 1), r])

        # close the fiel
        f.close()

        # build the structure
        bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=16, name='spine')
        spine_polyline = nmv.geometry.draw_poly_line(poly_line_data=spine_poly_line_data,
                                                     bevel_object=bevel_object, caps=True)

        return spine_polyline

    def do_it(self):

        # Number of spines per segment
        number_of_spines_per_segment = 5

        j = 0
        sample_spine = self.build_spine()
        # For the apical dendrites
        # Apical dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for i, arbor in enumerate(self.morphology.basal_dendrites):

                    spines_locations_and_normals = list()

                    # Get the normals along the segments along the arbors
                    nmv.skeleton.ops.apply_operation_to_arbor(
                        *[arbor,
                          nmv.skeleton.ops.get_random_spines_locations_and_normals_across_section,
                          number_of_spines_per_segment,
                          spines_locations_and_normals])

                    for i, spine in enumerate(spines_locations_and_normals):

                        j += 1
                        spine_object = nmv.scene.duplicate_object(sample_spine, 'spine_%d' % j)

                        p0 = spine.location
                        normal = spine.normal
                        p2 = p0 + normal * 1.0

                        nmv.scene.scale_object_uniformly(spine_object, spine.segment_radius)
                        nmv.scene.translate_object(spine_object, p0)
                        nmv.scene.rotate_object_towards_target(spine_object, Vector((0, 1, 0)), p2)

                        #  active.data.splines[0].points[1].co
                        # active.matrix_world
