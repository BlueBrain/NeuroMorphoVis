####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import tqdm

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.consts
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities


####################################################################################################
# @RandomSpineBuilder
####################################################################################################
class RandomSpineBuilder:
    """Building and integrating random spines on individual morphology without a digital circuit."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology skeleton.
        :param options:
            NeuroMorphoVis options.
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
    def load_spine_meshes(self):
        """Load all the template spines and ignore the verbose messages of loading."""

        nmv.utilities.disable_std_output()
        self.spine_meshes = nmv.file.load_spines(nmv.consts.Paths.SPINES_MESHES_HQ_DIRECTORY)
        nmv.utilities.enable_std_output()

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
        spine_object.name = 'Spine %d' % index

        # Scale the spine
        random_number = random.uniform(0.75, 1.5)
        nmv.scene.ops.scale_object_uniformly(spine_object, spine.size * random_number)

        # Random rotation
        random_angle = random.uniform(0, 90)
        nmv.scene.rotate_object(spine_object, 0, random_angle, 0)

        # Translate the spine to the post synaptic position
        nmv.scene.ops.set_object_location(spine_object, spine.post_synaptic_position)

        # Rotate the spine towards the pre-synaptic point
        nmv.scene.ops.rotate_object_towards_target(
            spine_object, Vector((0, 1, 0)), spine.pre_synaptic_position)

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

        # Apply the operation to sections with lower branching orders.
        nmv.skeleton.ops.apply_operation_to_trimmed_morphology(
            *[self.morphology,
              self.options.morphology.axon_branch_order,
              self.options.morphology.basal_dendrites_branch_order,
              self.options.morphology.apical_dendrite_branch_order,
              nmv.skeleton.ops.get_random_spines_on_section_recursively,
              self.options.mesh.number_spines_per_micron,
              spines_list])

        # Load all the template spines and ignore the verbose messages of loading
        self.load_spine_meshes()

        nmv.logger.detail('Cloning and integrating spines')
        spine_meshes = list()
        for i, spine in enumerate(
                tqdm.tqdm(spines_list, bar_format=nmv.consts.Messages.TQDM_FORMAT)):
            spine_meshes.append(self.emanate_spine(spine, i))

        # Delete the template spines
        nmv.scene.ops.delete_list_objects(self.spine_meshes)

        # Return the spine meshes list
        return spine_meshes
