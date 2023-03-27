####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @SynapticsOptions
####################################################################################################
class SynapticsOptions:
    """Synaptics options"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor"""

        # Synapse visualization use case
        self.use_case = None

        # In case
        self.synaptics_json_file = None

        # Reconstruction method
        self.synapses_radius = nmv.consts.Synaptics.SYNAPSES_RADIUS

        # Colors for excitatory and inhibitory synapses
        self.excitatory_synapses_color = nmv.enums.Color.EXCITATORY_SYNAPSES
        self.inhibitory_synapses_color = nmv.enums.Color.INHIBITORY_SYNAPSES

        # Color coding schemes of afferent and efferent synapses
        self.afferent_color_coding = nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR
        self.efferent_color_coding = nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR

        # Afferent and efferent colors
        self.afferent_synapses_color = nmv.enums.Color.AFFERENT_SYNAPSES
        self.efferent_synapses_color = nmv.enums.Color.EFFERENT_SYNAPSES

        # If the single color option is used, assign its value to this parameter
        self.synapses_color = nmv.enums.Color.SYNAPSES

        # The percentage of the synapses loaded on the neuron
        self.percentage = nmv.consts.Synaptics.SYNAPSES_PERCENTAGE

        # The GIDs of pre- and post-synaptic neurons that are only used to visualize shared synapses
        self.pre_synaptic_gid = None
        self.post_synaptic_gid = None

        # Parameters for a single neuron and NOT a PAIR
        self.display_dendrites = True
        self.display_axons = True
        self.dendrites_color = nmv.enums.Color.BASAL_DENDRITES
        self.axons_color = nmv.enums.Color.AXONS

        # A list of the color map of the pre- or post-synaptic mtypes and etypes synapses
        # NOTE: This list is initialized once a neuron is loaded from the circuit
        self.mtypes_colors = list()
        self.etypes_colors = list()

        # Parameters for a PAIR, NOT a SINGLE neuron
        self.display_pre_synaptic_dendrites = True
        self.display_pre_synaptic_axons = True
        self.pre_synaptic_dendrites_color = nmv.enums.Color.BASAL_DENDRITES
        self.pre_synaptic_axons_color = nmv.enums.Color.AXONS
        self.display_post_synaptic_dendrites = True
        self.display_post_synaptic_axons = True
        self.post_synaptic_dendrites_color = nmv.enums.Color.BASAL_DENDRITES
        self.post_synaptic_axons_color = nmv.enums.Color.AXONS

        # Neuron radius
        self.unify_branch_radii = True
        self.unified_radius = 1.0

        self.shader = nmv.enums.Shader.LAMBERT_WARD

        self.customized_synaptics_group = None
        self.customized_synaptics_colors = list()









