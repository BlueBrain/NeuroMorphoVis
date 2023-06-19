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
import nmv.bbp
import nmv.mesh
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities
import nmv.geometry


####################################################################################################
# @RandomSpineBuilder
####################################################################################################
class CircuitSpineBuilder:
    """Building and integrating accurate spines using a BBP circuit.
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

        # Protrusion mesh
        self.protrusion_mesh = None

    ################################################################################################
    # @load_spine_meshes
    ################################################################################################
    def load_spine_meshes(self):
        """Loads all the spine meshes from the spines directory
        """

        # Load all the template spines and ignore the verbose messages of loading
        nmv.utilities.disable_std_output()
        self.spine_meshes = nmv.file.load_spines(nmv.consts.Paths.SPINES_MESHES_LQ_DIRECTORY)
        nmv.utilities.enable_std_output()

        self.protrusion_mesh = \
            nmv.file.import_obj_file(nmv.consts.Paths.SPINES_MESHES_LQ_DIRECTORY, 'tip.obj')

        # Create the material
        material = nmv.shading.create_material(
            name='%spine_material', color=self.options.shading.mesh_spines_color,
            material_type=self.options.shading.mesh_material)

        # Apply the shader
        for spine_object in self.spine_meshes:
            nmv.shading.set_material_to_object(spine_object, material)

        nmv.shading.set_material_to_object(self.protrusion_mesh, material)

    ################################################################################################
    # @emanate_protrusion
    ################################################################################################
    def emanate_protrusion(self,
                           spine,
                           index):
        """Emanates a protrusion of a spine at an exact position on the dendritic tree.

        :param spine:
            A given spine object that contains all the data required to emanate the spine.
        :param index:
            Spine index.
        :return:
            The mesh instance that correspond to the spines.
        """

        # Get a protrusion object
        protrusion_object = nmv.scene.ops.duplicate_object(self.protrusion_mesh,
                                                           'protrusion_%d' % index,
                                                           link_to_scene=False)

        # Scale the object based on the radius of the branch
        nmv.scene.ops.scale_object_uniformly(protrusion_object, spine.post_synaptic_radius)

        # Locate it
        nmv.scene.ops.set_object_location(protrusion_object, spine.post_synaptic_position)

        # Rotate it
        nmv.scene.ops.rotate_object_towards_target(
            protrusion_object, Vector((0, 0, 1)), spine.pre_synaptic_position)

        # Return a reference to the spine
        return protrusion_object

    ################################################################################################
    # @emanate_spine
    ################################################################################################
    def emanate_spine(self,
                      spine,
                      index):
        """Emanates a spine at an exact position on the dendritic tree.

        :param spine:
            A given spine object that contains all the data required to emanate the spine.
        :param index:
            Spine index.
        :return:
            The mesh instance that correspond to the spines.
        """

        # Select a random spine from the spines list
        spine_template = random.choice(self.spine_meshes)

        # Get a copy of the template and update it
        spine_object = nmv.scene.ops.duplicate_object(spine_template, index, link_to_scene=False)

        # Compute the spine extent
        # spine_extent = (spine.post_synaptic_position - spine.pre_synaptic_position).length

        # Scale the spine
        nmv.scene.ops.scale_object_uniformly(spine_object, spine.size)

        # Translate the spine to the post synaptic position
        nmv.scene.ops.set_object_location(spine_object, spine.post_synaptic_position)

        # Rotate the spine towards the pre-synaptic point
        # We assume that the normal is heading towards to -Z axis for computing the rotation
        nmv.scene.ops.rotate_object_towards_target(
            spine_object, Vector((0, 0, 1)), spine.pre_synaptic_position)

        # Return a reference to the spine
        return spine_object

    ################################################################################################
    # @add_spines_to_morphology
    ################################################################################################
    def add_spines_to_morphology(self, circuit, post_gid, pre_gid=None):
        """Builds all the spines on a spiny neuron using a BBP circuit.

        :return:
            A joint mesh of the reconstructed spines.
        """

        # To load the circuit, 'brain' must be imported
        try:
            import bluepy
        except ImportError:
            raise ImportError('ERROR: Cannot import \'bluepy\'')

        # Load the template spine meshes
        self.load_spine_meshes()
        spines = nmv.bbp.get_spines(circuit=circuit, post_gid=post_gid)

        # Load the synapses from the file
        spine_meshes = list()
        for i, spine in enumerate(
                tqdm.tqdm(spines, bar_format=nmv.consts.Messages.TQDM_FORMAT)):
            spine_meshes.append(self.emanate_spine(spine, i))

        # Link the spines to the scene in a single step
        nmv.logger.info('Linking spines to the scene')
        for spine_object in spine_meshes:
            nmv.scene.link_object_to_scene(spine_object)

        # Delete the template spines
        nmv.scene.ops.delete_list_objects(self.spine_meshes)

        # Return the spine meshes list
        return spine_meshes
