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


####################################################################################################
# @Synaptics
####################################################################################################
class Synaptics:
    """Synaptics enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @UseCase
    ################################################################################################
    class UseCase:
        """Synaptics use cases enumerators
        """

        NOT_SELECTED = 'NOT_SELECTED'

        AFFERENT = 'VISUALIZE_AFFERENT_SYNAPSES'

        EFFERENT = 'VISUALIZE_EFFERENT_SYNAPSES'

        AFFERENT_AND_EFFERENT = 'VISUALIZE_AFFERENT_AND_EFFERENT_SYNAPSES'

        EXCITATORY = 'VISUALIZE_EXCITATORY_SYNAPSES'

        INHIBITORY = 'VISUALIZE_INHIBITORY_SYNAPSES'

        EXCITATORY_AND_INHIBITORY = 'VISUALIZE_EXCITATORY_AND_INHIBITORY_SYNAPSES'

        SYNAPTIC_PATHWAYS = 'VISUALIZE_SYNAPTIC_PATHWAYS'

        SPECIFIC_COLOR_CODED_SET = 'VISUALIZE_SPECIFIC_COLOR_CODED_SET'

    class ColorCoding:

        SINGLE_COLOR = 'SYNAPSE_SINGLE_COLOR'

        COLOR_CODED_PRE_SYNAPTIC_MTYPE = 'COLOR_CODED_PRE_SYNAPTIC_MTYPE'

        COLOR_CODED_POST_SYNAPTIC_MTYPE = 'COLOR_CODED_POST_SYNAPTIC_MTYPE'

        COLOR_CODED_PRE_SYNAPTIC_ETYPE = 'COLOR_CODED_PRE_SYNAPTIC_ETYPE'

        COLOR_CODED_POST_SYNAPTIC_ETYPE = 'COLOR_CODED_POST_SYNAPTIC_ETYPE'


        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

