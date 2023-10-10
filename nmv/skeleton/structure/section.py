####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.enums
import nmv.analysis


####################################################################################################
# Section
####################################################################################################
class Section:
    """A morphological section represents a series of morphological samples."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 index=-1,
                 parent_index=-1,
                 children_ids=None,
                 samples=None,
                 type=None,
                 label='Section',
                 tag='Section'):
        """Constructor

        :param index:
            Section index.
        :param parent_index:
            The index of the parent section.
        :param children_ids:
            A list of the indexes of the children sections.
        :param samples:
            A list of samples that compose this section.
        :param type:
            Section type, can be AXON, DENDRITE, APICAL_DENDRITE, or NONE.
        :param label:
            Arbor label to indicate which one is that.
        :param tag:
            A tag to identify the arbor when using it as a variable name.
        """

        # Section index
        self.index = index

        # The index of the parent section
        self.parent_index = parent_index

        # A list of the indexes of the children sections
        if children_ids is not None:
            self.children_ids = children_ids
        else:
            self.children_ids = list()

        # Segment samples (points along the section)
        self.samples = samples

        # Add a reference to the section as a member variable of the sample, for accessibility !
        if self.samples is not None:
            for sample in self.samples:
                sample.section = self

        # Section type: AXON (2), DENDRITE (3), APICAL_DENDRITE (4), or NONE
        self.type = type

        # A reference to the section parent, if it exists
        self.parent = None

        # Arbor label, only for roots
        self.label = label

        # Arbor tag, only for roots
        self.tag = tag

        # A list of the children
        self.children = list()

        # The branching order of this section
        self.branching_order = 0

        # Is the 'root' section of any branch connected to the soma or not ?!
        # By default, for all the sections, this options is set to False, however, for the root
        # sections, the branch is checked if it is connected to the soma or not. If True, then we
        # keep a reference to the face that will be used to extrude or connect that branch to soma.
        # This parameter is mainly used for the SoftBody soma reconstruction. 
        self.connected_to_soma = False

        # Is the section (mainly the root sections that represent the arbors) far from the soma ?!
        # This parameter is set to True by default, until it has been updated by the section-to-soma
        # connection functions. It is being mainly used for the MetaBall soma reconstruction.
        # The self.connected_to_soma parameter is used for the SoftBody soma reconstruction.
        self.far_from_soma = True

        # A reference to the reconstructed mesh that represents the section.
        # NOTE: This reference will be used to link the mesh to the soma if the arbor is connected
        # to the soma relying on the value of the connected_to_soma variable.
        # It is only used for specific meshing algorithms
        self.mesh = None

        # The index of the face that is supposed to connect the soma with the root section of a
        # branch.
        # NOTE: This variable is only set to the root sections.
        self.soma_face_index = None

        # The centroid of a branch
        # NOTE: This variable is only set to the root sections.
        self.soma_face_centroid = None

        # This parameter defines whether this section is a continuation for a parent section or
        # not. By default, it is set to False, however, during the morphology pre-processing, it
        # must be updated if the section is determined to be a continuous one.
        self.is_primary = False

        # Initial value for the maximum branching level
        self.maximum_branching_order = 100

        # The length of the section, initially None, till getting computed
        self.length = None

        # The path length from the root node till the end of this section along the arbor
        self.path_length = None

        # The X-coordinate of the dendrogram of this section
        self.dendrogram_x = None

        # The Y-coordinate of the dendrogram of this section
        self.dendrogram_y = None

        # Arbor color
        self.color = Vector((1.0, 1.0, 1.0))

        # Statistical analysis data of the section
        self.stats = nmv.analysis.SectionStats()

    ################################################################################################
    # @get_type_string
    ################################################################################################
    def get_type_string(self):
        """Return a string that reflects the type of the arbor, AXON, APICAL or BASAL.

        :return:
            String that reflects the type of the arbor, AXON, APICAL or BASAL
        """

        if str(self.type) == '2':
            return 'AXON'
        elif str(self.type) == '3':
            return 'BASAL_DENDRITE'
        elif str(self.type) == '4':
            return 'APICAL_DENDRITE'
        else:
            return 'UNKNOWN_BRANCH_TYPE'

    ################################################################################################
    # @get_type_prefix
    ################################################################################################
    def get_type_prefix(self):
        """Returns a string prefix that is used to register UI components.

        These components are accessible from the following calls:
            * bpy.context.scene.NMV_Axon[SOME_VARIABLE] for axons
            * bpy.context.scene.NMV_BasalDendrite[NUMBER][SOME_VARIABLE] for basal dendrites
            * bpy.context.scene.NMV_ApicalDendrite[SOME_VARIABLE] for apical dendrites
        :return:
            String that reflects the type of the section, or which arbor it belongs to.
        """

        if str(self.type) == '2':
            return 'Axon'
        elif str(self.type) == '3':
            return 'BasalDendrite'
        elif str(self.type) == '4':
            return 'ApicalDendrite'
        else:
            return 'UnknownBranch'

    ################################################################################################
    # @get_type_label
    ################################################################################################
    def get_type_label(self):
        """Returns the label of the section.

        :return:
            A string that reflects the type of the arbor and can be used to label UI components.
        """

        if str(self.type) == '2':
            return 'Axon'
        elif str(self.type) == '3':
            return 'Basal Dendrite'
        elif str(self.type) == '4':
            return 'Apical Dendrite'
        else:
            return 'Unknown Branch'

    ################################################################################################
    # @get_material_index
    ################################################################################################
    def get_material_index(self):
        """Returns the material index that is used to create a corresponding colored material
        to be applied to the corresponding object when reconstructed in the scene.

        :return:
            Material index.
        """

        if str(self.type) == '2':
            return nmv.enums.Color.AXON_MATERIAL_START_INDEX
        elif str(self.type) == '3':
            return nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX
        elif str(self.type) == '4':
            return nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX
        else:
            # By default, use the basal dendrites colors
            return nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX

    ################################################################################################
    # @is_axon
    ################################################################################################
    def is_axon(self):
        """Check if this section belongs to the axon or not.

        :return:
            True if the section belongs to the axon.
        """
        if str(self.type) == '2':
            return True
        return False

    ################################################################################################
    # @is_basal_dendrite
    ################################################################################################
    def is_basal_dendrite(self):
        """Check if this section belongs to a basal dendrite or not.

        :return:
            True if the section belongs to a basal dendrite.
        """
        if str(self.type) == '3':
            return True
        return False

    ################################################################################################
    # @is_apical_dendrite
    ################################################################################################
    def is_apical_dendrite(self):
        """Check if this section belongs to an apical dendrite or not.

        :return:
            True if the section belongs to an apical dendrite.
        """
        if str(self.type) == '4':
            return True
        return False

    ################################################################################################
    # @is_root
    ################################################################################################
    def is_root(self):
        """Check if the section is root or not.

        :return:
            True if the section is root, and False otherwise.
        """
        if self.parent is None:
            return True
        return False

    ################################################################################################
    # @is_leaf
    ################################################################################################
    def is_leaf(self):
        """Checks if the section is leaf (last branch in a tree) in the tree or not.

        :return:
            True if the section is leaf and False otherwise.
        """
        if len(self.children) > 0:
            return False
        return True

    ################################################################################################
    # @has_children
    ################################################################################################
    def has_children(self):
        """Check if the section has children sections or not.

        :return:
            True or False.
        """

        if len(self.children) > 0:
            return True

        return False

    ################################################################################################
    # @has_parent
    ################################################################################################
    def has_parent(self):
        """Check if the section has a parent section or not.

        :return:
            True of False.
        """

        if self.parent_index is None or self.parent is None:
            return False

        return True

    ################################################################################################
    # @reorder_samples
    ################################################################################################
    def reorder_samples(self):
        """After the insertion of new samples into the section, their order is changed. Therefore,
        we must re-order them to be able to link them with their logical order.
        """

        # Update the indexes of the samples based on their order along the section
        for i, section_sample in enumerate(self.samples):

            # Set the sample index according to its order along the section in the samples list
            section_sample.index = i

    ################################################################################################
    # @compute_length
    ################################################################################################
    def compute_length(self):
        """Computes the length of the section.

        :return:
            Returns the length of the section in case this function is called from an object.
        """

        # Re-initialize to zero, in case it is still None
        self.length = 0

        # Add the length of every segment along the section
        for i in range(len(self.samples) - 1):

            sample_0 = self.samples[i]
            sample_1 = self.samples[i + 1]
            self.length += (sample_1.point - sample_0.point).length

        # Return the result
        return self.length

    ################################################################################################
    # @compute_average_radius
    ################################################################################################
    def compute_average_radius(self):
        """Computes the average radius of the section.

        :return:
            Returns the average radius of the section.
        """

        average_radius = 0.0
        for sample in self.samples:
            average_radius += sample.radius
        average_radius /= len(self.samples)

        return average_radius

    ################################################################################################
    # @compute_parents_path_length
    ################################################################################################
    def compute_parents_path_length(self):
        """Computes the path length of the parent sections recursively.
        """

        # The parent must not be None
        if self.parent is not None:

            # Compute the path length
            self.parent.compute_path_length()

            # Go recursively
            self.compute_parents_path_length()

    ################################################################################################
    # @compute_path_length
    ################################################################################################
    def compute_path_length(self):
        """Computes the path length of the section. The path length is the distance from the root
        node till the end of this section along the arbor.

        Note that the result of this function is only correct if path_length is computed for all
        the parent sections.

        :return:
            Returns the path length of the section in case of being called from an object.
        """

        # Re-initialize to zero, in case it is still None
        self.path_length = 0

        # If this is a root section, the path length is simply the section length
        if self.is_root():
            self.path_length = self.compute_length()

        # Otherwise, it is the sum of the path length of the parent and the length of this section
        else:

            # If the path length of the parent is still None, compute the parents please
            if self.parent.path_length is None:
                self.compute_parents_path_length()

            # Now we can correctly
            self.path_length = self.compute_length() + self.parent.path_length

        # Return the result
        return self.path_length

    ################################################################################################
    # @is_terminal
    ################################################################################################
    def is_terminal(self):
        """Checks if the section is a terminal one or not."""

        return True if len(self.children) == 0 else False

