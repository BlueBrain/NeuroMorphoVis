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

# System imports
import random

# Blender imports
import bpy
from mathutils import Vector
from mathutils import Matrix

import nmv
import nmv.consts
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities


####################################################################################################
# @RandomSpineBuilder
####################################################################################################
class RandomSpineBuilder:
    """Building and integrating random spine on individual morphology without a BBP circuit.
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

        # Morphology
        self.morphology = morphology

        # Loaded options from NeuroMorphoVis
        self.options = options

        # A list containing all the spines meshes
        self.spine_meshes = None

    ################################################################################################
    # @load_spine_meshes
    ################################################################################################
    def emanate_spine_from_face(self,
                                dendrite_samples,
                                dendrite_mesh,
                                face_index, id):

        # Create the spine
        spine = nmv.skeleton.Spine()
        spine.post_synaptic_position = dendrite_mesh.data.polygons[face_index].center
        spine.pre_synaptic_position = dendrite_mesh.data.polygons[face_index].center + \
                                      1.0 * dendrite_mesh.data.polygons[face_index].normal

        lenght = 1e5
        for i_sample in dendrite_samples:
            distance = (i_sample.point - spine.post_synaptic_position).length
            #print(distance)
            if distance < lenght:
                spine.size = i_sample.radius * 3
                print(spine.size)

        # Select a random spine from the spines list
        spine_template = random.choice(self.spine_meshes)

        # Get a copy of the template and update it
        spine_object = nmv.scene.ops.duplicate_object(spine_template, id)

        # Rename the spine
        spine_object.name = '%s_spine_%d' % (self.options.morphology.label, id)

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
        self.spine_meshes = nmv.file.load_spines(nmv.consts.Paths.SPINES_MESHES_HQ_DIRECTORY)
        nmv.utilities.enable_std_output()

        # Create the material
        material = nmv.shading.create_material(
            name='%spine_material', color=self.options.mesh.spines_color,
            material_type=self.options.mesh.material)

        # Apply the shader
        for spine_object in self.spine_meshes:

            # Apply the shader to each spine mesh
            nmv.shading.set_material_to_object(spine_object, material)

    ################################################################################################
    # @emanate_spine
    ################################################################################################
    def emanate_spine(self,
                      spine,
                      id):
        """Emanates a spine at a random position on the dendritic tree.

        :param spine:
            A given spine object that contains all the data required to emanate the spine.
        :param id:
            Spine identifier.
        :return:
            The mesh instance that correspond to the spines.
        """

        # Select a random spine from the spines list
        spine_template = random.choice(self.spine_meshes)

        # Get a copy of the template and update it
        spine_object = nmv.scene.ops.duplicate_object(spine_template, id)

        # Rename the spine
        spine_object.name = '%s_spine_%d' % (self.options.morphology.label, id)

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
