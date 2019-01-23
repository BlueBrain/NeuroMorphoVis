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
import copy

# Blender imports
import bpy, mathutils

# Internal modules
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.geometry
import neuromorphovis.mesh
import neuromorphovis.skeleton
import neuromorphovis.scene


####################################################################################################
# @MorphologyEditor
####################################################################################################
class MorphologyEditor:
    """Morphology Editor
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
        :param options:
            System options
        """

        # Morphology
        self.morphology = morphology

        # All the options of the project (an instance of NeuroMorphoVisOptions)
        self.options = options

        self.apical_skeleton = None

        self.basal_dendrites_skeletons = list()

        self.axon_skeleton = None

    ################################################################################################
    # @add_soma_to_arbor_segment
    ################################################################################################
    @staticmethod
    def add_soma_to_arbor_segment(arbor,
                                  arbor_skeleton_mesh):
        """Adds a little segment from the soma center (or the origin) to the first sample along the
        arbor.

        :param arbor:
            A given arbor of the morphology.
        :param arbor_skeleton_mesh:
            The skeleton mesh of the arbor (that is so far a vertex point at the origin)
        """

        # Initial point is at the soma center (typically origin)
        point_0 = mathutils.Vector((0.0, 0.0, 0.0))

        # Last point is at the first sample of the root section of the arbor
        point_1 = arbor.samples[0].point

        # Deselect all the objects in the scene and select the skeleton mesh
        nmv.scene.deselect_all()
        nmv.scene.select_objects([arbor_skeleton_mesh])

        # Select the vertex that we need to start the extrusion process from (0 is the soma vertex)
        nmv.mesh.select_vertex(arbor_skeleton_mesh, 0)

        # Toggle from the object mode to the edit mode
        bpy.ops.object.editmode_toggle()

        # Extrude
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror": False},
                                         TRANSFORM_OT_translate={"value": point_1 - point_0})

        # Toggle from the object mode to the edit mode
        bpy.ops.object.editmode_toggle()

    ################################################################################################
    # @extrude_section
    ################################################################################################
    @staticmethod
    def extrude_section_along_arbor_skeleton(section,
                                             arbor_skeleton_mesh):
        """Extrudes the section along its samples starting from the first one to the last one.

        :param section:
            A given section to extrude a mesh around it.
        :param arbor_skeleton_mesh:
            The skeleton mesh of the arbor (we keep extruding this skeleton till the last sample).
        """

        # On all the samples of the section
        for i in range(0, len(section.samples) - 1):

            # Points
            point_0 = section.samples[i].point
            point_1 = section.samples[i + 1].point

            # Select the vertex that we need to start the extrusion process from
            nmv.mesh.ops.select_vertex(arbor_skeleton_mesh, section.samples[i].arbor_idx)

            # Toggle from the object mode to the edit mode
            bpy.ops.object.editmode_toggle()

            # Extrude
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror": False},
                                             TRANSFORM_OT_translate={"value": point_1 - point_0})

            # Toggle from the object mode to the edit mode
            bpy.ops.object.editmode_toggle()

    ################################################################################################
    # @create_root_point_mesh
    ################################################################################################
    def extrude_arbor_along_skeleton(self,
                                     root,
                                     arbor_skeleton_mesh):
        """Extrude the given arbor section by section recursively.

        :param root:
            The root of a given section.
        :param arbor_skeleton_mesh:
            The skeleton mesh of the arbor (we keep extruding this skeleton till the last sample).
        """

        # Extrude the section
        self.extrude_section_along_arbor_skeleton(root, arbor_skeleton_mesh)

        # Extrude the children sections recursively
        for child in root.children:
            self.extrude_arbor_along_skeleton(child, arbor_skeleton_mesh)

    ################################################################################################
    # @create_arbor_mesh
    ################################################################################################
    def create_arbor_skeleton_mesh(self,
                                   arbor,
                                   arbor_name):
        """Creates a skeleton mesh of the given arbor recursively.

        :param arbor:
            A given arbor.
        :param arbor_name:
            The name of the arbor.
        :return:
            A reference to the created skeleton mesh object.
        """

        # Initially, this index is set to ONE and incremented later (soma index = 0)
        samples_global_arbor_index = [1]
        nmv.skeleton.ops.update_samples_indices_per_arbor(arbor, samples_global_arbor_index)

        # Create an initial proxy mesh at the origin
        arbor_skeleton_mesh = nmv.geometry.create_vertex_mesh(name=arbor_name)

        # First of all, add an auxiliary segment from the soma center to the first sample
        self.add_soma_to_arbor_segment(arbor=arbor, arbor_skeleton_mesh=arbor_skeleton_mesh)

        # Extrude arbor mesh using the skinning method using a temporary radius
        self.extrude_arbor_along_skeleton(root=arbor, arbor_skeleton_mesh=arbor_skeleton_mesh)

        # Link the created skeleton to the morphology
        return arbor_skeleton_mesh

    ################################################################################################
    # @build_arbors
    ################################################################################################
    def create_morphological_skeleton(self):
        """Creates the skeleton of the morphology such that we can control it and update it
        during the repair operation.

        NOTE: All the created objects are linked after their creation to the morphology itself.
        """

        # Header
        nmv.logger.header('Creating Morphology Skeleton for Repair')

        # Apical dendrite
        if self.morphology.apical_dendrite is not None:

            nmv.logger.info('Apical dendrite')
            self.apical_skeleton = self.create_arbor_skeleton_mesh(
                arbor=self.morphology.apical_dendrite,
                arbor_name=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX)

        # Do it dendrite by dendrite
        for i, basal_dendrite in enumerate(self.morphology.dendrites):

            # Create the basal dendrite meshes
            nmv.logger.info('Dendrite [%d]' % i)
            self.basal_dendrites_skeletons.append(self.create_arbor_skeleton_mesh(
                arbor=basal_dendrite,
                arbor_name='%s_%d' % (nmv.consts.Arbors.BASAL_DENDRITES_PREFIX, i)))

        # Create the apical dendrite mesh
        if self.morphology.axon is not None:

            nmv.logger.info('Axon')
            self.axon_skeleton = self.create_arbor_skeleton_mesh(
                arbor=self.morphology.axon,
                arbor_name=nmv.consts.Arbors.AXON_PREFIX)

    ################################################################################################
    # @update_section_coordinates
    ################################################################################################
    @staticmethod
    def update_section_coordinates(section,
                                   arbor_skeleton_mesh):
        """Updates the coordinates of the samples of the given section from the skeleton object.

        :param section:
            A given section to update the positions of its samples.
        :param arbor_skeleton_mesh:
            The skeleton mesh of the arbor that is modified by the user.
        """

        # On all the samples of the section
        for i in range(0, len(section.samples)):

            # Update the position
            section.samples[i].point = copy.deepcopy(nmv.mesh.ops.get_vertex_position(
                mesh_object=arbor_skeleton_mesh, vertex_index=section.samples[i].arbor_idx))

    ################################################################################################
    # @update_arbor_coordinates
    ################################################################################################
    def update_arbor_coordinates(self,
                                 root,
                                 arbor_skeleton_mesh):
        """"Updates the coordinates of the samples of the given arbor from the skeleton object.

        :param root:
            The root of a given section.
        :param arbor_skeleton_mesh:
            The skeleton mesh of the arbor that is modified by the user.
        """

        # Update for the current section
        self.update_section_coordinates(root, arbor_skeleton_mesh)

        # Update the children sections recursively
        for child in root.children:
            self.update_arbor_coordinates(child, arbor_skeleton_mesh)

    ################################################################################################
    # @update_arbor_coordinates
    ################################################################################################
    def update_skeleton_coordinates(self):

        # Header
        nmv.logger.header('Updating Morphology Skeleton Coordinates')

        # Apical dendrite
        if self.morphology.apical_dendrite is not None:

            nmv.logger.info('Apical dendrite')
            self.update_arbor_coordinates(
                root=self.morphology.apical_dendrite,
                arbor_skeleton_mesh=self.apical_skeleton)

        # Do it dendrite by dendrite
        for i, basal_dendrite in enumerate(self.morphology.dendrites):

            nmv.logger.info('Dendrite [%d]' % i)
            self.update_arbor_coordinates(
                root=basal_dendrite,
                arbor_skeleton_mesh=self.basal_dendrites_skeletons[i])

        # Create the apical dendrite mesh
        if self.morphology.axon is not None:

            nmv.logger.info('Axon')
            self.update_arbor_coordinates(
                root=self.morphology.axon,
                arbor_skeleton_mesh=self.axon_skeleton)
