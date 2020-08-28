####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
import random

# Blender imports
from mathutils import Vector, Matrix

# Internal imports
import nmv.consts
import nmv.skeleton


####################################################################################################
# @BBPReader
####################################################################################################
class BBPReader:
    """Morphology reader for BBP circuits"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """
        pass

    ################################################################################################
    # @get_gids_from_target
    ################################################################################################
    @staticmethod
    def get_gids_from_target(blue_config,
                             target):
        """Gets a list of GIDs from a target file of a certain circuit.

        :param blue_config:
            A given BBP circuit file.
        :param target:
            Target, a group of GIDs.
        :return:
            A list of GIDs composing the target.
        """

        # Import BluePy
        try:
            import bluepy.v2
        except ImportError:
            print('ERROR: Cannot import [BluePy], please install it')
            return None

        # Loading a circuit
        from bluepy.v2 import Circuit
        circuit = Circuit(blue_config)

        # Loading the GIDs of the sample target within the circuit
        gids = circuit.cells.ids(target)

        # Return a list of all the GIDs
        return gids

    ################################################################################################
    # @load_bbp_morphology_from_gid
    ################################################################################################
    @staticmethod
    def load_bbp_morphology_from_gid(blue_config,
                                     gid):
        """This function returns a reference to a morphology in a circuit given by its gid.

        :param blue_config:
            A given BBP circuit configuration file.
        :param gid:
            A given neuron GID.
        :return:
            A reference to a BBP morphology structure
        """

        # Import BluePy
        try:
            import bluepy.v2
        except ImportError:
            print('ERROR: Cannot import [BluePy], please install it')
            return None

        # Loading a circuit
        from bluepy.v2 import Circuit
        circuit = Circuit(blue_config)

        # Get the morphology from its GID
        bbp_morphology = circuit.morph.get(int(gid), True)

        # Return a reference to the morphology
        return bbp_morphology

    ################################################################################################
    # @load_bbp_morphology_from_gid_using_h5_file
    ################################################################################################
    @staticmethod
    def load_bbp_morphology_from_gid_using_h5_file(blue_config,
                                                   gid):
        """This function returns a reference to a morphology in a circuit given by its gid.

        :param blue_config:
            A given BBP circuit configuration file.
        :param gid:
            A given neuron GID.
        :return:
            A reference to a BBP morphology structure
        """

        # Import BluePy
        try:
            import bluepy.v2
        except ImportError:
            print('ERROR: Cannot import [BluePy], please install it')
            return None

        # Loading a circuit
        from bluepy.v2 import Circuit
        circuit = Circuit(blue_config)

        # Get the morphology file path from its GID
        # We must ensure that the GID is integer, that's why the cast is there
        h5_morphology_path = circuit.morph.get_filepath(int(gid))

        # Use the H5 morphology loader to load this file
        # Don't center the morphology, as it is assumed to be cleared and reviewed by the team
        h5_reader = nmv.file.H5Reader(h5_file=h5_morphology_path, center_morphology=False)

        # Return a reference to the morphology
        return h5_reader.read_file()

    ################################################################################################
    # @get_neuron_from_gid
    ################################################################################################
    @staticmethod
    def get_neuron_from_gid(blue_config,
                            gid):
        """Return a BBP neuron structure from its input GID.

        :param blue_config:
            Input circuit configuration file.
        :param gid:
            Input neuron GID.
        :return:
            A reference to the BBP neuron
        """

        # Import BluePy
        try:
            import bluepy.v2
        except ImportError:
            print('ERROR: Cannot import [BluePy], please install it')
            return None

        # Loading a circuit
        from bluepy.v2 import Circuit
        circuit = Circuit(blue_config)

        # Get a reference to the neuron where you can access its data later
        bbp_neuron = circuit.cells.get(gid)

        # Return a reference to the BBP neuron
        return bbp_neuron

    ################################################################################################
    # @get_neuron_position_from_gid
    ################################################################################################
    @staticmethod
    def get_neuron_position_from_gid(blue_config,
                                     gid):
        """Gets the position of a BBP neuron from its GID.

        :param blue_config:
            Circuit configuration file.
        :param gid:
            Neuron GID.
        :return:
            Cartesian coordinates of the position of the neuron (soma position)
        """

        # Load the neuron from the BBP-SDK
        neuron = BBPReader.get_neuron_from_gid(blue_config, gid)

        # Return the position of the neuron
        return Vector((neuron['x'], neuron['y'], neuron['z']))

    ################################################################################################
    # @get_neuron_orientation_from_gid
    ################################################################################################
    @staticmethod
    def get_neuron_orientation_from_gid(blue_config,
                                        gid):
        """Get the orientation of a BBP neuron from its GID.

        :param blue_config:
            BBP circuit configuration file.
        :param gid:
            BBP neuron GID.
        :return:
            The orientation of the neuron.
        """

        # Load the neuron from the BBP-SDK
        neuron = BBPReader.get_neuron_from_gid(blue_config, gid)

        # Return the orientation of he neuron
        o = neuron['orientation']
        o0 = Vector((o[0][0], o[0][1], o[0][2]))
        o1 = Vector((o[1][0], o[1][1], o[1][2]))
        o2 = Vector((o[2][0], o[2][1], o[2][2]))
        return Matrix(o0, o1, o2)

    ################################################################################################
    # @get_neuron_mtype_name_from_gid
    ################################################################################################
    @staticmethod
    def get_neuron_mtype_name_from_gid(blue_config,
                                       gid):
        """Get the morphology type (mtype) name of the neuron.

        :param blue_config:
            BBP circuit configuration file.
        :param gid:
            BBP neuron GID.
        :return:
            Neuron morphological type name.
        """

        # Load the neuron from the BBP-SDK
        neuron = BBPReader.get_neuron_from_gid(blue_config, gid)

        # Return the mtype name
        return neuron['mtype']

    ################################################################################################
    # @get_neuron_morphology_label_from_gid
    ################################################################################################
    @staticmethod
    def get_neuron_morphology_label_from_gid(blue_config,
                                             gid):
        """Get the morphology label of the neuron.

        :param blue_config:
            BBP circuit configuration file.
        :param gid:
            BBP neuron GID.
        :return:
            Neuron morphology label.
        """

        # Load the neuron from the BBP-SDK
        neuron = BBPReader.get_neuron_from_gid(blue_config, gid)

        # Return morphology label
        return neuron['morphology']

    ################################################################################################
    # @get_section_from_id
    ################################################################################################
    @staticmethod
    def get_section_from_id(sections,
                            index):
        """Return a BBP section from its ID.

        :param sections:
            A list of BBP sections
        :param index:
            A given section ID.
        :return:
            A BBP section.
        """

        for section in sections:
            if section.id == index:
                return section
        return None

    ################################################################################################
    # @create_morphology_skeleton
    ################################################################################################
    @staticmethod
    def create_morphology_skeleton(root,
                                   sections):
        """Creates the morphological skeleton of a unifying morphology from a BBP one.

        :param root:
            The root of the unifying morphology.
        :param sections:
            A list of input BBP sections to be added to this morphology skeleton.
        :return:
            The root after integrating the input sections.
        """

        # Get section parent and update the root
        parent = BBPReader.get_section_from_id(sections, root.parent_index)
        root.parent = parent

        # Get section children and update the root
        if len(root.children_ids) > 0:

            # Do it child by child
            for child_id in root.children_ids:

                # Get the section based on its index
                child = BBPReader.get_section_from_id(sections, child_id)

                # Create morphology skeleton before adding it to the current branch
                child = BBPReader.create_morphology_skeleton(child, sections)

                # Add the child to the list of children in the parent branch
                root.children.append(child)

        return root

    ################################################################################################
    # @load_morphology_from_circuit
    ################################################################################################
    @staticmethod
    def load_morphology_from_circuit(blue_config,
                                     gid):
        """Return a reference to a morphology in a circuit given by its GID.

        :param blue_config:
            BBP circuit configuration file.
        :param gid:
            BBP neuron GID.
        :return:
            A reference to a BBP morphology structure
        """

        # Load the BBP morphology object using the H5 file reader
        # NOTE: This approach is quite straight forward, but we should make it extensible in
        # the future for SONATA circuits.
        morphology_object = BBPReader.load_bbp_morphology_from_gid_using_h5_file(
            blue_config=blue_config, gid=gid)

        if morphology_object is not None:

            # Return a reference to the loaded morphology object
            return True, morphology_object

        # There is no morphology
        return False, None
