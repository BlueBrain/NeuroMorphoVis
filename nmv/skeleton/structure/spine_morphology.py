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
import copy

# Internal imports
import nmv.bbox
import nmv.skeleton
import nmv.utilities


################################################################################################
# SpineSection
################################################################################################
class SpineSection:
    """A class to represent a section of a given spine.
    """

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self, samples):
        """Constructor
        """

        # Morphology soma
        self.samples = samples


####################################################################################################
# SpineMorphology
####################################################################################################
class SpineMorphology:
    """
    A class to represent the morphological skeleton of a tree structure, for example neuron.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self, sections):
        """Constructor
        """

        # Morphology soma
        self.sections = sections

