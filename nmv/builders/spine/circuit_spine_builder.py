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

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
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

        # Keep a list of all the spines objects
        spines_objects = []

        # Keep a list of all the protrusion objects
        protrusion_objects = []

        # To load the circuit, 'brain' must be imported
        try:
            import bluepy
        except ImportError:
            raise ImportError('ERROR: Cannot import \'blurpy\'')

        # Load the template spine meshes
        self.load_spine_meshes()

        import nmv.bbp
        #spines = nmv.bbp.get_spines_for_synaptic_pair(circuit=circuit, post_gid=post_gid, pre_gid=pre_gid)
        spines = nmv.bbp.get_spines(circuit=circuit, post_gid=post_gid)
        # Load the synapses from the file
        number_spines = len(spines)
        for i, spine in enumerate(spines):

            # Show progress
            nmv.utilities.time_line.show_iteration_progress('\t Spines', i, number_spines)

            # Emanate a spine
            spine_object = self.emanate_spine(spine, i)

            # Create a protrusion object
            # protrusion_object = self.emanate_protrusion(spine, i)

            # Add the objects to the lists
            spines_objects.append(spine_object)
            #protrusion_objects.append(protrusion_object)

        # Done
        nmv.utilities.time_line.show_iteration_progress(
            '\t Spines', number_spines, number_spines, done=True)

        # Link the spines to the scene in a single step
        nmv.logger.info('Linking spines to the scene')
        for spine_object in spines_objects:
            nmv.scene.link_object_to_scene(spine_object)

        # Link the protrusions to the scene in a single step
        #nmv.logger.info('Linking protrusions to the scene')
        #for protrusion_object in protrusion_objects:
        #    bpy.context.scene.objects.link(protrusion_object)

        # TODO: adjust
        return spines_objects, spines

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
