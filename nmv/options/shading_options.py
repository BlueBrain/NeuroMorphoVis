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

        # Soma color for the soma toolbox
        self.soma_color = nmv.enums.Color.SOMA

        # Soma color for the morphology toolbox
        self.morphology_soma_color = nmv.enums.Color.SOMA

        # Axon color for the morphology toolbox
        self.morphology_axons_color = nmv.enums.Color.AXONS

        # Basal dendrites color for the morphology toolbox
        self.morphology_basal_dendrites_color = nmv.enums.Color.BASAL_DENDRITES

        # Apical dendrites color for the morphology toolbox
        self.morphology_apical_dendrites_color = nmv.enums.Color.APICAL_DENDRITES

        # Articulations color for the morphology toolbox
        self.morphology_articulation_color = nmv.enums.Color.ARTICULATION

        # Soma color for the mesh toolbox
        self.mesh_soma_color = nmv.enums.Color.SOMA

        # Axon color for the mesh toolbox
        self.mesh_axons_color = nmv.enums.Color.AXONS

        # Basal dendrites color for the mesh toolbox
        self.mesh_basal_dendrites_color = nmv.enums.Color.BASAL_DENDRITES

        # Spines color (only for mesh) for the mesh toolbox
        self.mesh_spines_color = nmv.enums.Color.SPINES

        # Nucleus color (only for mesh) for the mesh toolbox
        self.mesh_nucleus_color = nmv.enums.Color.NUCLEI

        # Material for the soma toolbox
        self.soma_material = nmv.enums.Shader.LAMBERT_WARD

        # Material for the morphology toolbox
        self.morphology_material = nmv.enums.Shader.LAMBERT_WARD

        # Material for the mesh toolbox
        self.mesh_material = nmv.enums.Shader.LAMBERT_WARD

    ################################################################################################
    # @set_default
    ################################################################################################
    def set_default(self):
        """Sets the default options for duplicated objects.
        """

        # Soma color for the soma toolbox
        self.soma_color = nmv.enums.Color.SOMA

        # Soma color for the morphology toolbox
        self.morphology_soma_color = nmv.enums.Color.SOMA

        # Axon color for the morphology toolbox
        self.morphology_axons_color = nmv.enums.Color.AXONS

        # Basal dendrites color for the morphology toolbox
        self.morphology_basal_dendrites_color = nmv.enums.Color.BASAL_DENDRITES

        # Apical dendrites color for the morphology toolbox
        self.morphology_apical_dendrites_color = nmv.enums.Color.APICAL_DENDRITES

        # Articulations color for the morphology toolbox
        self.morphology_articulation_color = nmv.enums.Color.ARTICULATION

        # Soma color for the mesh toolbox
        self.mesh_soma_color = nmv.enums.Color.SOMA

        # Axon color for the mesh toolbox
        self.mesh_axons_color = nmv.enums.Color.AXONS

        # Basal dendrites color for the mesh toolbox
        self.mesh_basal_dendrites_color = nmv.enums.Color.BASAL_DENDRITES

        # Spines color (only for mesh) for the mesh toolbox
        self.mesh_spines_color = nmv.enums.Color.SPINES

        # Nucleus color (only for mesh) for the mesh toolbox
        self.mesh_nucleus_color = nmv.enums.Color.NUCLEI

        # Material for the soma toolbox
        self.soma_material = nmv.enums.Shader.LAMBERT_WARD

        # Material for the morphology toolbox
        self.morphology_material = nmv.enums.Shader.LAMBERT_WARD

        # Material for the mesg toolbox
        self.mesh_material = nmv.enums.Shader.LAMBERT_WARD
