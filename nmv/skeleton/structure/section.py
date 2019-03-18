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


####################################################################################################
# Section
####################################################################################################
class Section:
    """ A morphological section represents a series of morphological samples. """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 id=-1,
                 parent_id=-1,
                 children_ids=None,
                 samples=None,
                 type=None):
        """Constructor

        :param id:
            Section index.
        :param parent_id:
            The index of the parent section.
        :param children_ids:
            A list of the indexes of the children sections.
        :param samples:
            A list of samples that compose this section.
        :param type:
            Section type, can be AXON, DENDRITE, APICAL_DENDRITE, or NONE.
        """

        # Section index
        self.id = id

        # The index of the parent section
        self.parent_id = parent_id

        # A list of the indexes of the children sections
        if children_ids is not None:
            self.children_ids = children_ids
        else:
            self.children_ids = list()

        # Segments samples (points along the section)
        self.samples = samples

        # Add a reference to the section as a member variable of the sample, for accessibility !
        if self.samples is not None:
            for sample in self.samples:
                sample.section = self

        # Section type: AXON (2), DENDRITE (3), APICAL_DENDRITE (4), or NONE
        self.type = type

        # A reference to the section parent, if it exists
        self.parent = None

        # A list of the children
        self.children = list()

        # The branching order of this section
        self.branching_order = 0

        # Is the 'root' section of any branch connected to the soma or not ?!
        # NOTE: By default for all the sections, this options is set to False, however,
        # for the root sections, the branch is checked if it is connected to the soma or not. If
        # True, then we keep a reference to the face that will be used to extrude or connect that
        # branch to the soma.
        self.connected_to_soma = False

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

        # This parameters defines whether this section is a continuation for a parent section or
        # not. By default it is set to False, however, during the morphology pre-processing, it must
        # be updated if the section is determined to be a continuous one.
        self.is_primary = False

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
            * bpy.context.Scene.Axon[SOME_VARIABLE] for axons
            * bpy.context.Scene.BasalDendrite[NUMBER][SOME_VARIABLE] for basal dendrites
            * bpy.context.Scene.ApicalDendrite[SOME_VARIABLE] for apical dendrites
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
    # @is_basal_dendrite
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

        if self.parent_id is None or self.parent is None:
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
            section_sample.id = i
