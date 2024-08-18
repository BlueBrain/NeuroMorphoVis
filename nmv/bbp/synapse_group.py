####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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


####################################################################################################
# @SynapseGroup
####################################################################################################
class SynapseGroup:
    """A group of synapses sharing a specific parameter."""

    ################################################################################################
    # @__int__
    ################################################################################################
    def __init__(self,
                 name='Synapse Group',
                 synapses_ids_list=None,
                 color=None):
        """Constructor

        :param name:
            The name of the group.
        :param synapses_ids_list:
            A list of all the IDs of the synapse.
        :param color:
            RGB color vector of the synapse.
        """

        # Group name
        self.name = name

        # A list of the IDs of all the synapses in this group
        self.synapses_ids_list = synapses_ids_list

        # The color of the group
        self.color = color
