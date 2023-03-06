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
    """Synaptics options
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        self.use_case = None

        # Reconstruction method
        self.synapses_radius = nmv.consts.Synaptics.SYNAPSES_RADIUS

        # Display neuron
        self.display_neuron = True

        # Colors for excitatory and inhibitory synapses
        self.excitatory_synapses_color = nmv.enums.Color.EXCITATORY_SYNAPSES
        self.inhibitory_synapses_color = nmv.enums.Color.INHIBITORY_SYNAPSES

        # Color coding schemes of afferent and efferent synapses
        self.afferent_synapses_color_scheme = nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR
        self.efferent_synapses_color_scheme = nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR

        # Afferent and efferent colors
        self.afferent_synapses_color = nmv.enums.Color.AFFERENT_SYNAPSES
        self.efferent_synapses_color = nmv.enums.Color.EFFERENT_SYNAPSES

        # If the single color option is used, assign its value to this parameter
        self.synapses_color = nmv.enums.Color.SYNAPSES

        # Loading a circuit from GPFS - or any remote file systems - is painfully slow, but since
        # we are loading the circuit at least once to obtain its data, we should pre-obtain some
        # data that could be needed later.
        self.circuit_mtypes = None
        self.circuit_etypes = None

        # The percentage of the synapses loaded on the neuron
        self.percentage = nmv.consts.Synaptics.SYNAPSES_PERCENTAGE








