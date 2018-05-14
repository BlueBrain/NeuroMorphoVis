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
import random

# Blender imports
import bpy
from mathutils import Vector
from mathutils import Matrix

import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.shading
import neuromorphovis.skeleton
import neuromorphovis.scene
import neuromorphovis.utilities


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
                      spine):
        """Emanates a spine at an exact position on the dendritic tree.

        :param spine:
            A given spine object that contains all the data required to emanate the spine.

        :return:
            The mesh instance that correspond to the spines.
        """

        # Select a random spine from the spines list
        spine_template = random.choice(self.spine_meshes)

        # Get a copy of the template and update it
        spine_object = nmv.scene.ops.duplicate_object(spine_template, id)

        # Scale the spine
        spine_scale = spine.size + random.uniform(0.75, 1.0)
        nmv.scene.ops.scale_object_uniformly(spine_object, spine_scale)

        # Translate the spine to the post synaptic position
        nmv.scene.ops.set_object_location(spine_object, spine.post_synaptic_position)

        # Rotate the spine towards the pre-synaptic point
        nmv.scene.ops.rotate_object_towards_target(
            spine_object, spine.post_synaptic_position, spine.pre_synaptic_position)

        # Return a reference to the spine
        return spine_object

    ################################################################################################
    # @add_spines_to_morphology
    ################################################################################################
    def add_spines_to_morphology(self):
        """Builds all the spines on a spiny neuron using a BBP circuit.

        :param morphology:
            A given morphology.
        :param blue_config:
            BBP circuit configuration file.
        :param gid:
            Neuron gid.
        :param material:
            Spine material.
        :return:
            A list of all the reconstructed spines along the neuron.
        """

        # Keep a list of all the spines objects
        spines_objects = []

        # To load the circuit, 'brain' must be imported
        try:
            import brain
        except ImportError:
            raise ImportError('ERROR: Cannot import \'brain\'')

        # Load the circuit, silently please
        circuit = brain.Circuit(self.morphology.blue_config)

        # Get all the synapses for the corresponding gid.
        synapses = circuit.afferent_synapses({int(self.morphology.gid)})

        # Get the local to global transforms
        local_to_global_transform = circuit.transforms({int(self.morphology.gid)})[0]

        # Print(local_to_global_transform)
        transformation_matrix = Matrix()
        for i in range(4):
            transformation_matrix[i][:] = local_to_global_transform[i]

        # Invert the transformation matrix
        transformation_matrix = transformation_matrix.inverted()

        # Create a timer to report the performance
        building_timer = nmv.utilities.timer.Timer()

        nmv.logger.info('Integrating spines')
        building_timer.start()

        spines_list = list()

        # Load the synapses from the file
        number_spines = len(synapses)
        for i, synapse in enumerate(synapses):

            # Show progress
            nmv.utilities.time_line.show_iteration_progress('Spines', i, number_spines)

            """ Ignore soma synapses """
            # If the post-synaptic section id is zero, then revoke it, and continue
            post_section_id = synapse.post_section()
            if post_section_id == 0:
                continue

            # Get the pre-and post-positions in the global coordinates
            pre_position = synapse.pre_surface_position()
            post_position = synapse.post_center_position()

            # Transform the spine positions to the circuit coordinates
            pre_synaptic_position = Vector((pre_position[0], pre_position[1], pre_position[2]))
            post_synaptic_position = Vector((post_position[0], post_position[1], post_position[2]))

            pre_synaptic_position = transformation_matrix * pre_synaptic_position
            post_synaptic_position = transformation_matrix * post_synaptic_position

            # Add all the spines into a list
            # Create the spine
            spine = nmv.skeleton.Spine()
            spine.post_synaptic_position = post_synaptic_position
            spine.pre_synaptic_position = pre_synaptic_position
            spine.size = 1.0
            spines_list.append(spine)

        # Load the synapses from the file
        number_spines = len(spines_list)
        for i, spine in enumerate(spines_list):

            # Show progress
            nmv.utilities.time_line.show_iteration_progress('\t Spines', i, number_spines)

            # Emanate a spine
            spine_object = self.emanate_spine(spine)

            # Add the object to the list
            spines_objects.append(spine_object)

        # Done
        nmv.utilities.time_line.show_iteration_progress('\t Spines', number_spines, number_spines,
                                                        done=True)

        # Report the time
        building_timer.end()
        nmv.logger.info('Spines: [%f] seconds' % building_timer.duration())

        # Delete the template spines
        nmv.scene.ops.delete_list_objects(self.spine_meshes)

        # Return the spines objects list
        return spines_objects
