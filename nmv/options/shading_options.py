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

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @ShadingOptions
####################################################################################################
class ShadingOptions:
    """Shading options.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Soma color
        self.soma_color = nmv.enums.Color.SOMA

        # Axon color
        self.axon_color = nmv.enums.Color.AXONS

        # Basal dendrites color
        self.basal_dendrites_color = nmv.enums.Color.BASAL_DENDRITES

        # Apical dendrites color
        self.apical_dendrites_color = nmv.enums.Color.APICAL_DENDRITES

        # Articulations color (only for morphology)
        self.articulation_color = nmv.enums.Color.ARTICULATION

        # Spines color (only for mesh)
        self.spines_color = nmv.enums.Color.SPINES

        # Nucleus color (only for mesh)
        self.nucleus_color = nmv.enums.Color.NUCLEI

        # Morphology material
        self.material = nmv.enums.Shader.LAMBERT_WARD

    ################################################################################################
    # @set_default
    ################################################################################################
    def set_default(self):
        """Sets the default options for duplicated objects.
        """

        # Soma color
        self.soma_color = nmv.enums.Color.SOMA

        # Axon color
        self.axon_color = nmv.enums.Color.AXONS

        # Basal dendrites color
        self.basal_dendrites_color = nmv.enums.Color.BASAL_DENDRITES

        # Apical dendrites color
        self.apical_dendrites_color = nmv.enums.Color.APICAL_DENDRITES

        # Articulations color
        self.articulation_color = nmv.enums.Color.ARTICULATION

        # Morphology material
        self.material = nmv.enums.Shader.LAMBERT_WARD

