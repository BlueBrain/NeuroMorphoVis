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
# @AnalysisData
####################################################################################################
class AnalysisData:
    """Analysis data collected with respect to branching order and radii to be able to plot
    histograms and more informative graphs.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 value=None,
                 distribution=None,
                 branching_order=None,
                 section_index=None,
                 radial_distance=None):
        """Constructor

        :param value:
            The value obtained from the analysis kernel on every section in the morphology.
        :param distribution:
            The distribution obtained from the analysis kernel on every section in the morphology.
        :param branching_order:
            The branching order at a specific sample.
        :param radial_distance:
             The radial distance from a given sample to the origin
        """

        # The value obtained from the analysis kernel on every section in the morphology
        self.value = value

        # The distribution obtained from the analysis kernel on every section in the morphology
        self.distribution = distribution

        # The branching order at a specific section
        self.branching_order = branching_order

        # The index of the section
        self.section_index = section_index

        # The radial distance from a given sample to the origin
        self.radial_distance = radial_distance
