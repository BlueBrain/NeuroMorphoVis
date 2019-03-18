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
import random

# Blender imports
from mathutils import Vector, Matrix

# Internal imports
import nmv
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

        # Import brain
        try:
            import brain
        except ImportError:
            print('ERROR: Cannot import brain')
            return None

        # Open a circuit with a given blue config
        bbp_circuit = brain.Circuit(blue_config)

        # Create a GID-set and load the morphologies from these GIDs
        gids = bbp_circuit.gids(target)

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

        # Import brain
        try:
            import brain
        except ImportError:
            print('ERROR: Cannot import brain')
            return None

        # Load the circuit
        bbp_circuit = brain.Circuit(blue_config)

        # Create a GID-set and load the morphology corresponding to the given GID
        gids_set = bbp_circuit.gids('a' + str(gid))

        loaded = bbp_circuit.load_morphologies(gids_set, bbp_circuit.Coordinates.local)
        uris_set = bbp_circuit.morphology_uris(gids_set)

        # Get a BBP morphology object loaded from the circuit
        bbp_morphology_object = brain.neuron.Morphology(uris_set[0])

        # Return a reference to the morphology
        return bbp_morphology_object

    ################################################################################################
    # @load_morphologies_from_target
    ################################################################################################
    @staticmethod
    def load_morphologies_from_target(blue_config,
                                      target):
        """Returns a reference to all the morphologies in a circuit given by certain target.

        :param blue_config:
            A given circuit configuration file.
        :param target:
            Input target
        :return:
            A reference to all the BBP morphologies loaded from the target and their GIDs
        """

        # Import brain
        try:
            import brain
        except ImportError:
            print('ERROR: Cannot import brain')
            return None

        # Open a circuit with a given blue config
        bbp_circuit = brain.Circuit(blue_config)

        # Create a GID-set and load the morphologies from these GIDs
        gids = bbp_circuit.gids(target)
        uris = bbp_circuit.morphology_uris(gids)[0]
        brain.neuron.Morphology(uris)
        bbp_morphologies = bbp_circuit.load_morphologies(gids, bbp_circuit.Coordinates.local)

        # Return a reference to the morphologies and their GIDs
        return bbp_morphologies, gids

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

        # Import BBP-SDK module inside the function to avoid the BBP tree complexity for non-BBP
        # morphologies.
        import bbp

        # Create a new experiment
        bbp_experiment = bbp.Experiment()

        # Open the blue-config file
        bbp_experiment.open(blue_config)

        # Create a micro-circuit
        bbp_microcircuit = bbp_experiment.microcircuit()

        # Set the cell target to the given gid
        bbp_cell_target = bbp.Cell_Target()
        bbp_cell_target.insert(int(gid))

        # Load the circuit
        bbp_microcircuit.load(bbp_cell_target, bbp.Loading_Flags.NEURONS)

        # Get the neuron from the microcircuit
        bbp_neuron = bbp_microcircuit.neurons()

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
        for data in neuron:
            return data.position()

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
        for data in neuron:
            return data.orientation()

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
        for data in neuron:
            return data.morphology_type().name()

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
        for data in neuron:
            return data.morphology_label()

    ################################################################################################
    # @get_section_from_id
    ################################################################################################
    @staticmethod
    def get_section_from_id(sections,
                            id):
        """Return a BBP section from its ID.

        :param sections:
            A list of BBP sections
        :param id:
            A given section ID.
        :return:
            A BBP section.
        """

        for section in sections:
            if section.id == id:
                return section
        return None

    ################################################################################################
    # @get_starting_sections_from_sections_list
    ################################################################################################
    @staticmethod
    def get_starting_sections_from_sections_list(sections_list):
        """Returns the starting sections from a sections list.
        For example, it will return the first section on the axon and the apical dendrite.
        In case of dendrites, it will return a list of all the starting sections.

        :param sections_list:
            A BBP section list with IDs
        :return:
            A list of BBP sections
        """

        # Filter all the sections given in a list and return the root (that have no parents)
        sections = []

        # Do it section by section
        for section in sections_list:

            # The section should not have any parents
            if section.parent_id is None:

                # Append it to the list
                sections.append(BBPReader.get_section_from_id(sections_list, section.id))

        return sections

    ################################################################################################
    # @get_soma
    ################################################################################################
    @staticmethod
    def get_soma(bbp_morphology):
        """Returns a reference to the soma of a given BBP morphology.

        :param bbp_morphology:
            BBP morphology.
        :return:
            A reference to the soma of the given BBP morphology
        """

        return bbp_morphology.soma()

    ################################################################################################
    # @get_axon
    ################################################################################################
    @staticmethod
    def get_axon(bbp_morphology):
        """This function returns the sections of the axon of a given BBP morphology.

        :param bbp_morphology:
            BBP morphology.
        :return:
            The sections of the axon of the given BBP morphology.
        """

        # Import brain
        try:
            import brain
        except ImportError:
            print('ERROR: Cannot import brain')
            return None

        return bbp_morphology.sections({brain.neuron.SectionType.axon})

    ################################################################################################
    # @get_dendrites
    ################################################################################################
    @staticmethod
    def get_dendrites(bbp_morphology):
        """This function returns the sections of the dendrites of a given BBP morphology.

        :param bbp_morphology:
            BBP morphology.
        :return:
            The sections of the dendrites of the given BBP morphology.
        """

        # Import brain
        try:
            import brain
        except ImportError:
            print('ERROR: Cannot import brain')
            return None

        dendrites = [bbp_morphology.section(int(id)) for id in
                     bbp_morphology.section_ids({brain.neuron.SectionType.dendrite})]
        return dendrites

    ################################################################################################
    # @get_apical_dendrite
    ################################################################################################
    @staticmethod
    def get_apical_dendrite(bbp_morphology):
        """Returns the sections of the apical dendrite of a given BBP morphology.

        :param bbp_morphology:
            BBP morphology.
        :return:
            The sections of the apical dendrite of the given BBP morphology.
        """

        # Import brain
        try:
            import brain
        except ImportError:
            print('ERROR: Cannot import brain')
            return None

        apical_dendrite = [bbp_morphology.section(int(id)) for id in
                           bbp_morphology.section_ids({brain.neuron.SectionType.apical_dendrite})]
        return apical_dendrite

    ################################################################################################
    # @get_soma_profile_points
    ################################################################################################
    @staticmethod
    def get_soma_profile_points(bbp_soma):
        """Returns a list of all the profile points of the soma.

        :param bbp_soma:
            Soma of a BBP morphology.
        :return:
            A list of all the profile points of a BBP soma.
        """

        # List of all profile points of the soma
        soma_profile_points = []
        for point in bbp_soma.profile_points():
            soma_profile_points.append(Vector((point[0], point[1], point[2])))
        return soma_profile_points

    ################################################################################################
    # @get_soma_profile_points_data
    ################################################################################################
    @staticmethod
    def get_soma_profile_points_data(bbp_soma):
        """Returns a list of positions and radii of the profile points.
        The structure of the data is as follows:
            @data[0] position, @data[1] radius, @data[2] index
            The index of a soma profile point is 0.
            The radius of a soma profile point is 1.0.

        :param bbp_soma:
            Soma of a BBP morphology.
        :return:
            A list of positions and radii of the profile points of the soma.
        """

        # List of all profile points of the soma
        soma_profile_points_data = []
        for point in bbp_soma.profile_points():
            soma_profile_points_data.append([Vector((point[0], point[1], point[2])), 1.0, 0])
        return soma_profile_points_data

    ################################################################################################
    # @get_axon_profile_points_data
    ################################################################################################
    @staticmethod
    def get_axon_profile_points_data(bbp_axon):
        """Returns the data of the first point on the axon initial segment.
        The structure of the data is as follows:
            @data[0] position, @data[1] radius, @data[2] index
            The index of an axon profile point is 1.
            The radius of an axon profile point is set to the sample radius.
        :param bbp_axon:
            Axon of a BBP morphology
        :return:
            A list of positions and radii of the profile points of the axon
        """

        # List of all profile points of the axon
        axon_profile_points_data = []
        if len(bbp_axon) > 0:  # Ensure that the axon is present in the skeleton
            axon_profile_points_data.append([Vector((bbp_axon[0].samples()[0][0],
                                                     bbp_axon[0].samples()[0][1],
                                                     bbp_axon[0].samples()[0][2])),
                                             bbp_axon[0].samples()[0][3] / 2.0, 1])
        return axon_profile_points_data

    ################################################################################################
    # @get_dendrites_profile_points_data
    ################################################################################################
    @staticmethod
    def get_dendrites_profile_points_data(bbp_dendrites):
        """This function returns the data of the first points on dendrites initial segments.
        The structure of the data is as follows:
            @data[0] position, @data[1] radius, @data[2] index
            The index of a dendrite profile point is 2.
            The radius of an axon profile point is set to the sample radius.

        :param bbp_dendrites:
            Dendrites of a BBP morphology
        :return:
            A list of positions and radii of the profile points of the dendrites
        """

        # List of all profile points of the axon
        dendrites_profile_points_data = []
        for dendrite in bbp_dendrites:

            # The profile points are only available for root sections
            if dendrite.parent() is None:
                dendrites_profile_points_data.append([Vector((dendrite.samples()[0][0],
                                                              dendrite.samples()[0][1],
                                                              dendrite.samples()[0][2])),
                                                      dendrite.samples()[0][3] / 2.0, 2])
        return dendrites_profile_points_data

    ################################################################################################
    # @get_apical_dendrite_profile_points_data
    ################################################################################################
    @staticmethod
    def get_apical_dendrite_profile_points_data(bbp_apical_dendrite):
        """
        This function returns the data of the first points on apical dendrite initial segments.
        The structure of the data is as follows:
            @data[0] position, @data[1] radius, @data[2] index
            The index of an apical dendrite profile point is 3.
            The radius of an axon profile point is set to the sample radius.

        :param bbp_apical_dendrite:
            Apical dendrite of a BBP morphology.
        :return:
            A list of positions and radii of the profile points of an apical dendrite.
        """

        # List of all profile points of the apical dendrite
        apical_dendrite_profile_points_data = []
        if len(
                bbp_apical_dendrite) > 0:  # Ensure that the apical dendrite is present in the skeleton
            apical_dendrite_profile_points_data.append(
                [Vector((bbp_apical_dendrite[0].samples()[0][0],
                         bbp_apical_dendrite[0].samples()[0][1],
                         bbp_apical_dendrite[0].samples()[0][2])),
                 bbp_apical_dendrite[0].samples()[0][3] / 2.0,
                 3])
        return apical_dendrite_profile_points_data

    ################################################################################################
    # @get_axon_starting_point
    ################################################################################################
    @staticmethod
    def get_axon_starting_point(bbp_axon):
        """Returns the first sample on the axon initial segment.

        :param bbp_axon:
            Axon of a BBP morphology.
        :return:
            The first sample on the axon initial segment.
        """

        axon_starting_point = [Vector((bbp_axon[0].samples()[0][0],
                                       bbp_axon[0].samples()[0][1],
                                       bbp_axon[0].samples()[0][2]))]
        return axon_starting_point

    ################################################################################################
    # @get_axon_starting_radius
    ################################################################################################
    @staticmethod
    def get_axon_starting_radius(bbp_axon):
        """
        This function returns the radius of the first point on the axon initial segment.

        :param bbp_axon:
            Axon of a BBP morphology.
        :return:
            The radius of the first sample on the axon initial segment.
        """

        axon_starting_radius = bbp_axon[0].samples()[0][3] / 2.0
        return axon_starting_radius

    ################################################################################################
    # @get_dendrites_starting_points
    ################################################################################################
    @staticmethod
    def get_dendrites_starting_points(bbp_dendrites):
        """
        This function returns a list of the first points of each dendrite.

        :param bbp_dendrites:
            A list of dendrites of a BBP morphology.
        :return:
            A list of points representing first samples on the initial segments of the dendrites.
        """

        dendrites_starting_points = []
        for dendrite in bbp_dendrites:

            # Only consider the roots
            if dendrite.parent() is None:
                dendrites_starting_points.append(Vector((dendrite.samples()[0][0],
                                                         dendrite.samples()[0][1],
                                                         dendrite.samples()[0][2])))
        return dendrites_starting_points

    ################################################################################################
    # @get_dendrites_starting_radii
    ################################################################################################
    @staticmethod
    def get_dendrites_starting_radii(bbp_dendrites):
        """Returns a list of the radii of the first points of each dendrite.

        :param bbp_dendrites:
            A list of dendrites of a BBP morphology.
        :return:
            A list of radii representing the first samples on the initial segments of the dendrites.
        """

        dendrites_starting_radii = []
        for dendrite in bbp_dendrites:

            # Only consider the roots
            if dendrite.parent() is None:
                dendrites_starting_radii.append(dendrite.samples()[0][3] / 2.0)
        return dendrites_starting_radii

    ################################################################################################
    # @get_apical_dendrite_starting_point
    ################################################################################################
    @staticmethod
    def get_apical_dendrite_starting_point(bbp_apical_dendrite):
        """Return the first point on the apical dendrite.

        :param bbp_apical_dendrite:
            Apical dendrite of a BBP morphology.
        :return:
            The first point on the apical dendrite.
        """

        apical_dendrite_starting_point = [Vector((bbp_apical_dendrite[0].samples()[0][0],
                                                  bbp_apical_dendrite[0].samples()[0][1],
                                                  bbp_apical_dendrite[0].samples()[0][2]))]
        return apical_dendrite_starting_point

    ################################################################################################
    # @get_apical_dendrite_starting_radius
    ################################################################################################
    @staticmethod
    def get_apical_dendrite_starting_radius(bbp_apical_dendrite):
        """Return the radius of the first point on the apical_dendrite.

        :param bbp_apical_dendrite:
            Apical dendrite of a BBP morphology.
        :return:
            The radius of the first point on the apical dendrite.
        """

        apical_dendrite_starting_radius = bbp_apical_dendrite[0].samples()[0][3] / 2.0
        return apical_dendrite_starting_radius

    ################################################################################################
    # @get_morphology_exemplars
    ################################################################################################
    @staticmethod
    def get_morphology_exemplars(blue_config,
                                 random_selection=False):
        """Returns a list of exemplars where each one represent a category of the different
        morphologies. If the random selection flag is set, then they will be picked up randomly,
        otherwise, the first one of each selected type will be picked.

        :param blue_config:
            A circuit configuration file.
        :param random_selection:
            Randomly selected cells.
        :return:
            A list of exemplars to all the mtypes that exist in the circuit.
        """

        # Import bbp
        try:
            import bbp
        except ImportError:
            print('ERROR: Cannot import brain')
            return None

        # Create an experiment
        bbp_experiment = bbp.Experiment()

        # Open the blue config
        bbp_experiment.open(blue_config)

        # Load the entire mc2_Column in the micro-circuit
        bbp_microcircuit = bbp_experiment.microcircuit()
        bbp_cell_target = bbp_experiment.cell_target('mc2_Column')
        bbp_microcircuit.load(bbp_cell_target, bbp.Loading_Flags.NEURONS)

        # retrieve a list of all the neurons in the circuit
        bbp_neurons = bbp_microcircuit.neurons()

        # create a list of selected exemplars
        exemplars_list = []
        for m_type in nmv.consts.MTYPES:

            # All the cells with that specific m-type
            m_type_cells = []

            # Get all the cells with that specific m-type
            for neuron in bbp_neurons:

                # Get BBP neuron data from the BBP-SDK
                neuron_gid = neuron.gid()
                neuron_m_type = neuron.morphology_type().name()
                if neuron_m_type == m_type:
                    m_type_cells.append([neuron_gid, neuron_m_type])

            # Select a random cell and add it to the exemplars list, otherwise, use the first m-type
            if random_selection:
                exemplars_list.append(random.choice(m_type_cells))
            else:
                exemplars_list.append(m_type_cells[0])

        # Return the exemplars list
        return exemplars_list

    ################################################################################################
    # @convert_bbp_sections
    ################################################################################################
    @staticmethod
    def convert_bbp_sections(bbp_morphology_sections):
        """Converts BBP morphology sections to the unifying structure.

        :param bbp_morphology_sections:
            Input sections of a BBP morphology.
        :return:
            A list of converted sections.
        """

        sections = []
        for bbp_morphology_section in bbp_morphology_sections:

            # Get the section ID
            section_id = bbp_morphology_section.id()

            # Get the parent section ID
            if bbp_morphology_section.parent() is None:
                parent_section_id = None
            else:
                parent_section_id = bbp_morphology_section.parent().id()

            # Get the section type
            section_type = bbp_morphology_section.type()

            # Retrieve all the segments (point or samples) along the section
            bbp_morphology_samples = bbp_morphology_section.samples()

            # Build the morphology skeleton samples
            samples = []
            for i, morphology_sample in enumerate(bbp_morphology_samples):

                # Sample position
                point = Vector((morphology_sample[0], morphology_sample[1], morphology_sample[2]))

                # Sample radius
                radius = morphology_sample[3] / 2.0

                # Construct a Sample object and add the data to it
                morphology_sample = nmv.skeleton.Sample(point=point, radius=radius, id=i)
                samples.append(morphology_sample)

            # Retrieve all children IDs
            children_ids = []
            for child in bbp_morphology_section.children():
                children_ids.append(child.id())

            # Build section
            section = nmv.skeleton.Section(
                id=section_id, parent_id=parent_section_id, children_ids=children_ids, samples=samples,
                type=section_type)

            # Set the parenting
            if parent_section_id is None:
                section.parent = None

            for i_section in sections:
                if i_section.id == parent_section_id:
                    section.parent = i_section.parent

            # Add the section to the list
            sections.append(section)

        # Return a list of the converted sections
        return sections

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
        parent = BBPReader.get_section_from_id(sections, root.parent_id)
        root.parent = parent

        # Get section children and update the root
        if len(root.children_ids) > 0:

            # Do it child by child
            for child_id in root.children_ids:

                # Get the section based on its id
                child = BBPReader.get_section_from_id(sections, child_id)

                # Create morphology skeleton before adding it to the current branch
                child = BBPReader.create_morphology_skeleton(child, sections)

                # Add the child to the list of children in the parent branch
                root.children.append(child)

        return root

    ################################################################################################
    # @convert_bbp_morphology_to_list
    ################################################################################################
    @staticmethod
    def convert_bbp_morphology_to_list(gid, bbp_morphology_object):
        """Converts a BBP morphology to list.

        :param gid:
            BBP neuron GID.
        :param bbp_morphology_object:
            BBP morphology object.
        :return:
            A list of BBP morphology sections.
        """

        # Soma
        bbp_morphology_soma = BBPReader.get_soma(bbp_morphology_object)

        # Axon
        bbp_morphology_axon = BBPReader.get_axon(bbp_morphology_object)

        # Dendrites
        bbp_morphology_dendrites = BBPReader.get_dendrites(bbp_morphology_object)

        # Apical dendrite
        bbp_morphology_apical_dendrites = BBPReader.get_apical_dendrite(bbp_morphology_object)

        # Soma center
        centroid = bbp_morphology_soma.centroid()

        # Soma mean radius
        mean_radius = bbp_morphology_soma.mean_radius()

        # Soma profile points
        profile_points = []
        for bbp_morphology_soma_profile_point in bbp_morphology_soma.profile_points():

            # Profile points
            profile_point = Vector((bbp_morphology_soma_profile_point[0],
                                    bbp_morphology_soma_profile_point[1],
                                    bbp_morphology_soma_profile_point[2]))
            profile_points.append(profile_point)

        # Create the soma
        soma = nmv.skeleton.Soma(
            centroid=centroid, mean_radius=mean_radius, profile_points=profile_points)

        # Create a linear list of the axon
        axon = BBPReader.convert_bbp_sections(bbp_morphology_axon)

        # Create a linear list of the dendrites
        dendrites = BBPReader.convert_bbp_sections(bbp_morphology_dendrites)

        # Create a linear list of the apical dendrite, if exists
        apical_dendrite = None
        if len(bbp_morphology_apical_dendrites) > 0:
            apical_dendrite = BBPReader.convert_bbp_sections(bbp_morphology_apical_dendrites)

        # Return a reference to each part
        return soma, axon, dendrites, apical_dendrite

    ################################################################################################
    # @convert_morphology_to_skeleton
    ################################################################################################
    @staticmethod
    def convert_morphology_to_skeleton(gid,
                                       bbp_morphology):
        """Converts BBP morphologies into our format that is used in this framework.

        :param gid:
            BBP neuron GID.
        :param bbp_morphology:
            Original BBP morphology.
        :return:
            Morphology skeleton.
        """

        # Convert a BBP morphology into a list of all the sections
        soma, axon_list, basal_dendrites_list, apical_dendrite_list = \
            BBPReader.convert_bbp_morphology_to_list(gid, bbp_morphology)

        # Create the axon tree
        axon_root = BBPReader.get_starting_sections_from_sections_list(axon_list)[0]
        axon = BBPReader.create_morphology_skeleton(axon_root, axon_list)

        # Create the dendrites trees
        dendrites_roots = BBPReader.get_starting_sections_from_sections_list(basal_dendrites_list)
        dendrites = []
        for dendrite_root in dendrites_roots:
            dendrite = BBPReader.create_morphology_skeleton(dendrite_root, basal_dendrites_list)
            dendrites.append(dendrite)

        # Create the apical dendrites tree, if exists
        apical_dendrite = None
        if apical_dendrite_list is not None:
            apical_dendrite_root = BBPReader.get_starting_sections_from_sections_list(
                apical_dendrite_list)[0]
            apical_dendrite = BBPReader.create_morphology_skeleton(
                apical_dendrite_root, apical_dendrite_list)

        # Create the tree representation of the morphology
        morphology = nmv.skeleton.Morphology(
            soma=soma, axon=axon, dendrites=dendrites, apical_dendrite=apical_dendrite, gid=gid)

        # Return the morphology tree skeleton
        return morphology

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

        # Load the BBP morphology object
        bbp_morphology_object = BBPReader.load_bbp_morphology_from_gid(
            blue_config=blue_config, gid=gid)

        # Convert the BBP morphology object to a skeleton
        morphology_object = BBPReader.convert_morphology_to_skeleton(
            gid=gid, bbp_morphology=bbp_morphology_object)

        if morphology_object is not None:

            # Return a reference to the loaded morphology object
            return True, morphology_object

        return False, None
