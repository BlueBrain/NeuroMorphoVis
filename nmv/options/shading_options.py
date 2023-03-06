####################################################################################################
# Copyright (c) 2016 - 2021, EPFL / Blue Brain Project
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
import nmv.utilities


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

        # Morphology Shading Options ###############################################################
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

        # Endfeet color for the morphology toolbox
        self.morphology_endfeet_color = nmv.enums.Color.ENDFEET

        # The first alternating color that will be used in the alternating pattern
        self.morphology_alternating_color_1 = nmv.consts.Color.MATT_BLACK

        # The second alternating color that will be used in the alternating pattern
        self.morphology_alternating_color_2 = nmv.consts.Color.VERY_WHITE

        # Morphology color coding scheme
        self.morphology_coloring_scheme = nmv.enums.ColorCoding.DEFAULT_SCHEME

        # The resolution of the color map of the morphology (number of elements, typically 64)
        self.morphology_colormap_resolution = nmv.consts.Color.COLORMAP_RESOLUTION

        # Get a list of initial colors from the selected colormap
        self.morphology_colormap_list = nmv.utilities.create_colormap_from_hex_list(
            nmv.enums.ColorMaps.get_hex_color_list(nmv.enums.ColorMaps.GNU_PLOT),
            nmv.consts.Color.COLORMAP_RESOLUTION)

        self.mtypes_colors = list()
        self.etypes_colors = list()

        # Mesh Shading Options #####################################################################
        # Soma color for the mesh toolbox
        self.mesh_soma_color = nmv.enums.Color.SOMA

        # Axon color for the mesh toolbox
        self.mesh_axons_color = nmv.enums.Color.AXONS

        # Apical dendrites color for the mesh toolbox
        self.mesh_apical_dendrites_color = nmv.enums.Color.APICAL_DENDRITES

        # Basal dendrites color for the mesh toolbox
        self.mesh_basal_dendrites_color = nmv.enums.Color.BASAL_DENDRITES

        # Endfeet color for the mesh toolbox
        self.mesh_endfeet_color = nmv.enums.Color.ENDFEET

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

        # Morphology Shading Options ###############################################################
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

        # Endfeet color for the morphology toolbox
        self.morphology_endfeet_color = nmv.enums.Color.ENDFEET

        # The first alternating color that will be used in the alternating pattern
        self.morphology_alternating_color_1 = nmv.consts.Color.MATT_BLACK

        # The second alternating color that will be used in the alternating pattern
        self.morphology_alternating_color_2 = nmv.consts.Color.VERY_WHITE

        # Morphology color coding scheme
        self.morphology_coloring_scheme = nmv.enums.ColorCoding.DEFAULT_SCHEME

        # The resolution of the color map of the morphology (number of elements)
        self.morphology_colormap_resolution = nmv.consts.Color.COLORMAP_RESOLUTION

        # Morphology color-map colors (this is set from the GUI)
        self.morphology_colormap_list = list()

        # Mesh Shading Options #####################################################################
        # Soma color for the mesh toolbox
        self.mesh_soma_color = nmv.enums.Color.SOMA

        # Axon color for the mesh toolbox
        self.mesh_axons_color = nmv.enums.Color.AXONS

        # Basal dendrites color for the mesh toolbox
        self.mesh_basal_dendrites_color = nmv.enums.Color.BASAL_DENDRITES

        # Endfeet color for the mesh toolbox
        self.mesh_endfeet_color = nmv.enums.Color.ENDFEET

        # Spines color (only for mesh) for the mesh toolbox
        self.mesh_spines_color = nmv.enums.Color.SPINES

        # Nucleus color (only for mesh) for the mesh toolbox
        self.mesh_nucleus_color = nmv.enums.Color.NUCLEI

        # Material Shading Options #################################################################
        # Material for the soma toolbox
        self.soma_material = nmv.enums.Shader.LAMBERT_WARD

        # Material for the morphology toolbox
        self.morphology_material = nmv.enums.Shader.LAMBERT_WARD

        # Material for the mesh toolbox
        self.mesh_material = nmv.enums.Shader.LAMBERT_WARD
