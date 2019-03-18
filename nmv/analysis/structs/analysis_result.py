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
# @AnalysisResult
####################################################################################################
class AnalysisResult:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 apical_dendrite_result=None,
                 basal_dendrites_result=None,
                 axon_result=None,
                 morphology_result=None):
        """Constructor

        :param apical_dendrite_result:
            The analysis result of the apical dendrite.
        :param basal_dendrites_result:
            The analysis result of the basal dendrites.
        :param axon_result:
            The analysis result of the axon.
        :param morphology_result:
            The aggregate analysis result of the entire morphology.
            This is computed for each respective filter from the results of the individual arbors.
        """

        # Apical dendrite
        self.apical_dendrite_result = apical_dendrite_result

        # Basal dendrites
        self.basal_dendrites_result = basal_dendrites_result

        # Axon
        self.axon_result = axon_result

        # Entire morphology
        self.morphology_result = morphology_result
