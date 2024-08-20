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

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @MorphologyOptions
####################################################################################################
class MorphologyOptions:
    """The morphology options"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor"""

        # INPUT SOURCE OPTIONS #####################################################################
        # The GID of a given neuron in a given circuit using a blue config
        self.gid = None

        # The circuit configuration file
        self.blue_config = None

        # Sonata configuration file
        self.libsonata_config = None
        self.libsonata_population = None

        # The circuit, where the given neuron is loaded from. In fact, we keep a reference of the
        # circuit within the morphology options to avoid the delays from loading the circuit data
        # from a remote file system. This parameter will be automatically filled after loading a
        # neuron morphology from a circuit
        # self.circuit = None

        # Morphology file path (if read from .H5 or .SWC file)
        self.morphology_file_path = None

        # Morphology file name (if read from .H5 or .SWC file)
        self.morphology_file_name = None

        # Morphology label (based on the GID or the morphology file name)
        self.label = None

        # Center at the origin, by default it is True
        self.center_at_origin = True

        # RECONSTRUCTION OPTIONS ###################################################################
        # Arbor style, ORIGINAL by default
        self.arbor_style = nmv.enums.Skeleton.Style.ORIGINAL

        # Soma reconstruction technique (IGNORE, SPHERE, or SOFT_BODY, or META_BALLS by default)
        self.soma_representation = nmv.enums.Soma.Representation.META_BALLS

        # Branching of the morphologies in the connected modes, either based on angles or radii
        self.branching = nmv.enums.Skeleton.Branching.RADII

        # Morphology edge styles
        self.edges = nmv.enums.Skeleton.Edges.SHARP

        # The arbors connectivity to the soma
        self.arbors_to_soma_connection = nmv.enums.Skeleton.Roots.ALL_CONNECTED

        # Enable/Disable axon reconstruction
        self.ignore_axons = False

        # Enable/Disable basal dendrites reconstruction
        self.ignore_basal_dendrites = False

        # Enable/Disable apical dendrite reconstruction (if exists)
        self.ignore_apical_dendrites = False

        # Axon branching order
        self.axon_branch_order = nmv.consts.Skeleton.AXON_DEFAULT_BRANCHING_ORDER

        # Basal dendrites branching order
        self.basal_dendrites_branch_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER

        # Apical dendrites branch order
        self.apical_dendrite_branch_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER

        # Resampling method
        self.resampling_method = nmv.enums.Skeleton.Resampling.NONE

        # Resampling step
        self.resampling_step = 1.0

        # The radii of the samples defined per section
        self.arbors_radii = nmv.enums.Skeleton.Radii.ORIGINAL

        # A scale factor for the radii of the sections
        self.sections_radii_scale = 1.0

        # A unified value for the radii of all the sections in the morphology
        self.samples_unified_radii_value = 1.0

        # A particular unified radius given to all the samples of the axon sections
        self.axon_samples_unified_radii_value = 1.0

        # A particular unified radius given to all the samples of the apical dendrite sections
        self.apical_dendrite_samples_unified_radii_value = 1.0

        # A particular unified radius given to all the samples of the basal dendrites sections
        self.basal_dendrites_samples_unified_radii_value = 1.0

        # Minimum threshold radius value, where any section with lower radius values will not drawn
        self.minimum_threshold_radius = 1e-5

        # Maximum threshold radius value, where any section with bigger radius values will not drawn
        self.maximum_threshold_radius = 1e5

        # Dendrogram type
        self.dendrogram_type = nmv.enums.Dendrogram.Type.SIMPLIFIED

        # Global coordinates
        self.global_coordinates = False

        # Number of sides of the bevel object used to scale the sections
        # This parameter controls the quality of the reconstructed morphology
        self.bevel_object_sides = nmv.consts.Meshing.BEVEL_OBJECT_SIDES

        # Selected a method to reconstruct the morphology
        self.reconstruction_method = nmv.enums.Skeleton.Method.DISCONNECTED_SECTIONS

        # EXPORT OPTIONS ###################################################################
        # Export the morphology to .segments file
        self.export_segments = False

        # Export the morphology to .swc file
        self.export_swc = False

        # Export the morphology skeleton to .blend file for rendering using tubes
        self.export_blend = False

    ################################################################################################
    # @set_default
    ################################################################################################
    def set_default(self):
        """Sets the default options for duplicated objects.
        """

        # Arbor style
        self.arbor_style = nmv.enums.Skeleton.Style.ORIGINAL

        # Soma reconstruction technique (IGNORE, SPHERE, or REALISTIC by default)
        self.soma_representation = nmv.enums.Soma.Representation.SPHERE

        # Branching of the morphologies in the connected modes, either based on angles or radii
        self.branching = nmv.enums.Skeleton.Branching.RADII

        # Morphology edge styles
        self.edges = nmv.enums.Skeleton.Edges.SHARP

        # The arbors connectivity to the soma
        self.arbors_to_soma_connection = nmv.enums.Skeleton.Roots.ALL_CONNECTED

        # Enable/Disable axon reconstruction
        self.ignore_axons = False

        # Enable/Disable basal dendrites reconstruction
        self.ignore_basal_dendrites = False

        # Enable/Disable apical dendrite reconstruction (if exists)
        self.ignore_apical_dendrites = False

        # Axon branching order
        self.axon_branch_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER

        # Basal dendrites branching order
        self.basal_dendrites_branch_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER

        # Apical dendrites branch order
        self.apical_dendrite_branch_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER

        # The radii of the sections (as specified in the morphology file, scaled with a given
        # scale factor, or constant at given fixed value)
        self.arbors_radii = nmv.enums.Skeleton.Radii.ORIGINAL

        # A scale factor for the radii of the sections
        self.sections_radii_scale = 1.0

        # A fixed and unified value for the radii of all the sections in the morphology
        self.samples_unified_radii_value = 1.0

        # Minimum threshold radius value, where any section with lower radius values will not drawn
        self.minimum_threshold_radius = 1e-5

        # Maximum threshold radius value, where any section with bigger radius values will not drawn
        self.maximum_threshold_radius = 1e5

        # Global coordinates
        self.global_coordinates = False

        # Number of sides of the bevel object used to scale the sections
        # This parameter controls the quality of the reconstructed morphology
        self.bevel_object_sides = nmv.consts.Meshing.BEVEL_OBJECT_SIDES

        # Selected a method to reconstruct the morphology
        self.reconstruction_method = nmv.enums.Skeleton.Method.DISCONNECTED_SECTIONS

    ################################################################################################
    # @adjust_to_analysis_mode
    ################################################################################################
    def adjust_to_analysis_mode(self):
        """Ajust the options to be used during the analysis mode. For example setting the branching
        orders to maximum, not ignoring any branches, etc....
        """

        # Arbor style
        self.arbor_style = nmv.enums.Skeleton.Style.ORIGINAL

        # Soma reconstruction technique (IGNORE, SPHERE, or SOFT_BODY, or META_BALLS by default)
        self.soma_representation = nmv.enums.Soma.Representation.META_BALLS

        # Branching of the morphologies in the connected modes, either based on angles or radii
        self.branching = nmv.enums.Skeleton.Branching.RADII

        # Morphology edge styles
        self.edges = nmv.enums.Skeleton.Edges.SHARP

        # The arbors connectivity to the soma
        self.arbors_to_soma_connection = nmv.enums.Skeleton.Roots.ALL_CONNECTED

        # Enable/Disable axon reconstruction
        self.ignore_axons = False

        # Enable/Disable basal dendrites reconstruction
        self.ignore_basal_dendrites = False

        # Enable/Disable apical dendrite reconstruction (if exists)
        self.ignore_apical_dendrites = False

        # Axon branching order
        self.axon_branch_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER

        # Basal dendrites branching order
        self.basal_dendrites_branch_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER

        # Apical dendrites branch order
        self.apical_dendrite_branch_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER

        # Resampling method
        self.resampling_method = nmv.enums.Skeleton.Resampling.NONE

        # Number of sides of the bevel object used to scale the sections
        # This parameter controls the quality of the reconstructed morphology
        self.bevel_object_sides = nmv.consts.Meshing.BEVEL_OBJECT_SIDES
