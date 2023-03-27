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


####################################################################################################
# @Synaptics
####################################################################################################
class Synaptics:
    """Synaptics enumerators"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor"""
        pass

    ################################################################################################
    # @UseCase
    ################################################################################################
    class UseCase:
        """Synaptics use cases enumerators"""

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            """Constructor"""
            pass

        # Nothing is selected in the menu, display NOTHING in the panel then
        NOT_SELECTED = 'SYNAPSE_VISUALIZATION_USE_CASE_NOT_SELECTED'

        # Visualize the afferent, or incoming, synapses
        AFFERENT = 'VISUALIZE_AFFERENT_SYNAPSES'

        # Visualize the efferent, or outgoing, synapses
        EFFERENT = 'VISUALIZE_EFFERENT_SYNAPSES'

        # Visualize both the afferent and efferent synapses at the same time
        AFFERENT_AND_EFFERENT = 'VISUALIZE_AFFERENT_AND_EFFERENT_SYNAPSES'

        # Visualize the excitatory synapses only
        EXCITATORY = 'VISUALIZE_EXCITATORY_SYNAPSES'

        # Visualize the inhibitory synapses only
        INHIBITORY = 'VISUALIZE_INHIBITORY_SYNAPSES'

        # Visualize the excitatory and inhibitory synapses
        EXCITATORY_AND_INHIBITORY = 'VISUALIZE_EXCITATORY_AND_INHIBITORY_SYNAPSES'

        # Visualize the synaptic pathways with a pre-synaptic cell
        PATHWAY_PRE_SYNAPTIC = 'VISUALIZE_SYNAPTIC_PATHWAYS_PRE_SYNAPTIC'

        # Visualize the synaptic pathways with a post-synaptic cell
        PATHWAY_POST_SYNAPTIC = 'VISUALIZE_SYNAPTIC_PATHWAYS_POST_SYNAPTIC'

        # Visualize the synapses on a single neuron with a specific color map and specific labels
        SPECIFIC_COLOR_CODED_SET = 'VISUALIZE_SPECIFIC_COLOR_CODED_SET'

        # Visualize projection to a cell (afferent projection)
        PROJECTION_TO_CELL = 'VISUALIZE_PROJECTIONS_TO_CELL'

        # Visualize targets
        TARGETS = 'VISUALIZE_SYNAPTIC_TARGETS'

    ################################################################################################
    # @ColorCoding
    ################################################################################################
    class ColorCoding:
        """Color-coding enumerators"""

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            """Constructor"""
            pass

        # Use a single color to label all the synapses
        SINGLE_COLOR = 'SYNAPSE_SINGLE_COLOR'

        # Color-code the synapses based on the mtypes of the pre- or the post-synaptic neurons
        MTYPE_COLOR_CODED = 'SYNAPSE_MTYPE_COLOR_CODED'

        # Color-code the synapses based on the etype of the pre- or the post-synaptic neurons
        ETYPE_COLOR_CODED = 'SYNAPSE_ETYPE_COLOR_CODED'

