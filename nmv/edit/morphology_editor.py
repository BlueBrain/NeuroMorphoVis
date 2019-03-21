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

# Internal modules
import nmv
import nmv.bmeshi
import nmv.mesh
import nmv.scene


####################################################################################################
# @MorphologyGlobalEditor
####################################################################################################
class MorphologyEditor:
    """Morphology Global Editor
    This editor edits the morphology as a single object, rather than representing the skeleton
    with multiple arbor objects. This is quite convenient when you need to edit all the arbors in
    a single step. The implementation uses bmeshes instead of meshes to make it extremely fast to
    toggle and switch between the morphology and the skeleton in case of long axons.
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

        # A skeleton mesh that reflects the morphology
        self.skeleton_mesh = None

    ################################################################################################
    # @update_samples_indices_per_morphology_of_section
    ################################################################################################
    @staticmethod
    def update_samples_indices_per_morphology_of_section(section,
                                                         index):
        """Updates the global sample.morphology_idx variables for the given section.
        :param section:
            A given section to update its sample.morphology_idx values.
        :param index:
            A starting index.
        """

        # If the given section is root
        if section.is_root():

            # Update the arbor index of the first sample
            section.samples[0].morphology_idx = index[0]

            # Increment the index value
            index[0] += 1

        # Non-root sections
        else:

            # The index of the root is basically the same as the index of the last sample of the
            # parent arbor
            section.samples[0].morphology_idx = section.parent.samples[-1].morphology_idx

        # Update the indices of the rest of the samples along the section
        for i in range(1, len(section.samples)):

            # Set the arbor index of the current sample
            section.samples[i].morphology_idx = index[0]

            # Increment the index
            index[0] += 1

    ################################################################################################
    # @update_samples_indices_per_morphology_of_arbor
    ################################################################################################
    def update_samples_indices_per_morphology_of_arbor(self,
                                                       arbor,
                                                       starting_index):
        """Updates the global sample.morphology_idx variables for the given arbor recursively.
        :param arbor:
            A given arbor to update its sample.morphology_idx values.
        :param starting_index:
            A starting index.
        """

        # Do it for section
        self.update_samples_indices_per_morphology_of_section(section=arbor,
                                                              index=starting_index)

        # Update the children sections recursively
        for child in arbor.children:

            # Update the children
            self.update_samples_indices_per_morphology_of_arbor(child, starting_index)

    ################################################################################################
    # @create_morphology_skeleton_as_multiple_arbors
    ################################################################################################
    def update_samples_indices_per_morphology_of_morphology(self):
        """Updates the global sample.morphology_idx variables for the given morphology.
        """

        # Header
        nmv.logger.header('Updating samples indices')

        # Initially, this index is set to ONE and incremented later (soma index = 0)
        samples_global_morphology_index = [1]

        # Apical dendrite
        if self.morphology.apical_dendrite is not None:

            nmv.logger.info('Apical dendrite')
            self.update_samples_indices_per_morphology_of_arbor(
                self.morphology.apical_dendrite, samples_global_morphology_index)

        # Basal dendrites
        if self.morphology.dendrites is not None:

            # Do it dendrite by dendrite
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                nmv.logger.info('Dendrite [%d]' % i)
                self.update_samples_indices_per_morphology_of_arbor(
                    basal_dendrite, samples_global_morphology_index)

        # Axon
        if self.morphology.axon is not None:

            nmv.logger.info('Axon')
            self.update_samples_indices_per_morphology_of_arbor(
                self.morphology.axon, samples_global_morphology_index)

    ################################################################################################
    # @add_soma_to_arbor_segment
    ################################################################################################
    def add_soma_to_arbor_segment(self,
                                  arbor):
        """Adds a little segment from the soma center (or the origin) to the first sample along the
        arbor.
        :param arbor:
            A given arbor of the morphology.
        """

        nmv.bmeshi.ops.extrude_vertex_towards_point(self.skeleton_mesh, 0, arbor.samples[0].point)

    ################################################################################################
    # @extrude_section
    ################################################################################################
    def extrude_section(self,
                        section):
        """Extrudes the section along its samples starting from the first one to the last one.
        :param section:
            A given section to extrude a mesh around it.
        """

        # Iterate over all the samples and extrude vertex by vertex
        for i in range(len(section.samples) - 1):
            nmv.bmeshi.ops.extrude_vertex_towards_point(
                self.skeleton_mesh, section.samples[i].morphology_idx, section.samples[i + 1].point)

    ################################################################################################
    # @extrude_branch
    ################################################################################################
    def extrude_branch(self,
                       root):
        """Extrude the given branch section by section recursively.
        :param root:
            The root of a given section.
        """

        # Extrude the section
        self.extrude_section(root)

        # Extrude the children sections recursively
        for child in root.children:
            self.extrude_branch(child)

    ################################################################################################
    # @extrude_arbor
    ################################################################################################
    def extrude_arbor(self,
                      arbor):
        """Creates a skeleton mesh of the given arbor recursively.
        :param arbor:
            A given arbor.
        :return:
            A reference to the created skeleton mesh object.
        """

        # First of all, add an auxiliary segment from the soma center to the first sample
        self.add_soma_to_arbor_segment(arbor=arbor)

        # Extrude branch mesh
        self.extrude_branch(root=arbor)

    ################################################################################################
    # @extrude_morphology_skeleton
    ################################################################################################
    def extrude_morphology_skeleton(self):
        """Creates the skeleton of the morphology as a single object such that we can control it
        and update it during the repair operation.
        NOTE: All the created objects are linked after their creation to the morphology itself.
        """

        # Header
        nmv.logger.header('Creating Morphology Skeleton for Repair')

        # Apical dendrite
        if self.morphology.apical_dendrite is not None:
            nmv.logger.info('Apical dendrite')
            self.extrude_arbor(arbor=self.morphology.apical_dendrite)

        # Do it dendrite by dendrite
        for i, basal_dendrite in enumerate(self.morphology.dendrites):
            # Create the basal dendrite meshes
            nmv.logger.info('Dendrite [%d]' % i)
            self.extrude_arbor(arbor=basal_dendrite)

        # Create the apical dendrite mesh
        if self.morphology.axon is not None:
            nmv.logger.info('Axon')
            self.extrude_arbor(arbor=self.morphology.axon)

    ################################################################################################
    # @sketch_morphology_skeleton
    ################################################################################################
    def sketch_morphology_skeleton(self):
        """Sketches the skeleton of the morphology as a single object such that we can control it
        and update it during the repair operation.
        NOTE: The created object is linked after their creation to the morphology itself.
        """

        # Updating the samples indices along the entire morphology
        self.update_samples_indices_per_morphology_of_morphology()

        # Create an initial proxy mesh at the origin (reflecting the soma)
        # self.skeleton_mesh = nmv.geometry.create_vertex_mesh(name=self.morphology.label)
        self.skeleton_mesh = nmv.bmeshi.create_vertex()

        # Extrude the morphology skeleton
        self.extrude_morphology_skeleton()

        # Convert the skeleton to a mesh
        self.skeleton_mesh = nmv.bmeshi.convert_bmesh_to_mesh(self.skeleton_mesh, 'Skeleton')

        # Select the skeleton mesh for the edit
        nmv.scene.set_active_object(self.skeleton_mesh)

    ################################################################################################
    # @update_section_coordinates
    ################################################################################################
    def update_section_coordinates(self,
                                   section):
        """Updates the coordinates of the samples of the given section from the skeleton object.
        :param section:
            A given section to update the positions of its samples.
        """

        # On all the samples of the section
        for i in range(0, len(section.samples)):

            # Update the position
            section.samples[i].point = copy.deepcopy(nmv.mesh.ops.get_vertex_position(
                mesh_object=self.skeleton_mesh, vertex_index=section.samples[i].morphology_idx))

    ################################################################################################
    # @update_arbor_coordinates
    ################################################################################################
    def update_arbor_coordinates(self,
                                 root):
        """"Updates the coordinates of the samples of the given arbor from the skeleton object.
        :param root:
            The root of a given section.
        """

        # Update for the current section
        self.update_section_coordinates(root)

        # Update the children sections recursively
        for child in root.children:
            self.update_arbor_coordinates(child)

    ################################################################################################
    # @update_arbor_coordinates
    ################################################################################################
    def update_skeleton_coordinates(self):

        # Header
        nmv.logger.header('Updating Morphology Skeleton Coordinates')

        # Apical dendrite
        if self.morphology.apical_dendrite is not None:

            nmv.logger.info('Apical dendrite')
            self.update_arbor_coordinates(root=self.morphology.apical_dendrite)

        if self.morphology.dendrites is not None:

            # Do it dendrite by dendrite
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                nmv.logger.info('Dendrite [%d]' % i)
                self.update_arbor_coordinates(root=basal_dendrite)

        # Create the apical dendrite mesh
        if self.morphology.axon is not None:

            nmv.logger.info('Axon')
            self.update_arbor_coordinates(root=self.morphology.axon)
