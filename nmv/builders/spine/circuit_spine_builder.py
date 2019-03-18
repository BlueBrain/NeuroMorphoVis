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
            name='%spine_material', color=self.options.mesh.spines_color,
            material_type=self.options.mesh.material)

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
            protrusion_object, Vector((0, 0, -1)), spine.pre_synaptic_position)

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
            spine_object, Vector((0, 0, -1)), spine.pre_synaptic_position)

        # Return a reference to the spine
        return spine_object

    ################################################################################################
    # @add_spines_to_morphology
    ################################################################################################
    def add_spines_to_morphology(self):
        """Builds all the spines on a spiny neuron using a BBP circuit.

        :return:
            A joint mesh of the reconstructed spines.
        """

        # Keep a list of all the spines objects
        spines_objects = []

        # Keep a list of all the protrusion objects
        protrusion_objects = []

        # To load the circuit, 'brain' must be imported
        try:
            import brain
        except ImportError:
            raise ImportError('ERROR: Cannot import \'brain\'')

        # Load the template spine meshes
        self.load_spine_meshes()

        # Load the circuit, silently please
        circuit = brain.Circuit(self.options.morphology.blue_config)

        # Get all the synapses for the corresponding gid.
        synapses = circuit.afferent_synapses({int(self.morphology.gid)})

        # Get the local to global transforms
        global_to_local_transform = nmv.skeleton.ops.get_transformation_matrix(
            self.options.morphology.blue_config, self.options.morphology.gid).inverted()

        # Create a timer to report the performance
        building_timer = nmv.utilities.timer.Timer()

        nmv.logger.info('Integrating spines')
        building_timer.start()

        spines_list = list()

        # Get a BBP morphology object loaded from the circuit
        gids_set = circuit.gids('a' + str(self.morphology.gid))
        loaded = circuit.load_morphologies(gids_set, circuit.Coordinates.local)
        uris_set = circuit.morphology_uris(gids_set)
        morphology = brain.neuron.Morphology(uris_set[0])

        # Load the synapses from the file
        number_spines = len(synapses)
        for i, synapse in enumerate(synapses):

            # Show progress
            nmv.utilities.time_line.show_iteration_progress('Spines', i, number_spines)

            # Ignore soma synapses
            # If the post-synaptic section id is zero, then revoke it, and continue
            post_section_id = synapse.post_section()
            if post_section_id == 0:
                continue

            # To make the spine realistic, you have to add a little notch on top of the location
            # and then add the spine above.
            # The spine length (or scale) will be computed from surface to surface
            # The notch length (or scale) will be computed based on the radius of the branch at the
            # spine

            # Get the pre-and post-positions in the global coordinates
            pre_position = synapse.pre_surface_position()
            post_position = synapse.post_center_position()

            # Transform the spine positions to the circuit coordinates
            pre_synaptic_position = Vector((pre_position[0], pre_position[1], pre_position[2]))
            post_synaptic_position = Vector((post_position[0], post_position[1], post_position[2]))

            spine_scale = (pre_synaptic_position - post_synaptic_position).length
            # print((pre_synaptic_position - post_synaptic_position).length)

            if not self.options.mesh.global_coordinates:
                pre_synaptic_position = global_to_local_transform * pre_synaptic_position
                post_synaptic_position = global_to_local_transform * post_synaptic_position

            # Add all the spines into a list
            # Create the spine
            spine = nmv.skeleton.Spine()
            spine.post_synaptic_position = post_synaptic_position
            spine.pre_synaptic_position = pre_synaptic_position
            spine.post_synaptic_radius = \
                morphology.section(synapse.post_section()).samples()[synapse.post_segment() + 1][3]
            # print(spine.post_synaptic_radius)
            spine.size = spine.post_synaptic_radius
            spines_list.append(spine)

        # Load the synapses from the file
        number_spines = len(spines_list)
        for i, spine in enumerate(spines_list):

            # Show progress
            nmv.utilities.time_line.show_iteration_progress('\t Spines', i, number_spines)

            # Emanate a spine
            spine_object = self.emanate_spine(spine, i)

            # Create a protrusion object
            protrusion_object = self.emanate_protrusion(spine, i)

            # Add the objects to the lists
            spines_objects.append(spine_object)
            protrusion_objects.append(protrusion_object)

        # Done
        nmv.utilities.time_line.show_iteration_progress(
            '\t Spines', number_spines, number_spines, done=True)

        # Link the spines to the scene in a single step
        nmv.logger.info('Linking spines to the scene')
        for spine_object in spines_objects:
            bpy.context.scene.objects.link(spine_object)

        # Link the protrusions to the scene in a single step
        nmv.logger.info('Linking protrusions to the scene')
        for protrusion_object in protrusion_objects:
            bpy.context.scene.objects.link(protrusion_object)

        # TODO: adjust
        return spines_objects, spines_list

        # Merging spines into a single object
        nmv.logger.info('Grouping spines to a single mesh')
        spine_mesh_name = '%s_spines' % self.options.morphology.label
        spines_mesh = nmv.mesh.ops.join_mesh_objects(spines_objects, spine_mesh_name)

        # Report the time
        building_timer.end()
        nmv.logger.info('Spines: [%f] seconds' % building_timer.duration())

        # Delete the template spines
        nmv.scene.ops.delete_list_objects(self.spine_meshes)

        # Return the spines objects list
        return spines_mesh
