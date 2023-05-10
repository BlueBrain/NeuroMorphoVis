###################################################################################################
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
# @Suffix
####################################################################################################
class Suffix:
    """Suffix constants"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Suffix appended to the name of a front image of the soma
    SOMA_FRONT = '_soma_front'

    # Suffix appended to the name of a side image of the soma
    SOMA_SIDE = '_soma_side'

    # Suffix appended to the name of a top image of the soma
    SOMA_TOP = '_soma_top'

    # Suffix appended to the name of a directory where a 360 sequence of the soma will be rendered
    SOMA_360 = '_soma_360'

    # Suffix appended to the name of a directory where a progressive sequence will be rendered
    SOMA_PROGRESSIVE = '_soma_progressive'

    # Suffix appended to the name of a reconstructed soma mesh file
    SOMA_MESH = '_soma'

    # Suffix appended to the name of an image of the morphology
    MORPHOLOGY = '_morphology'

    # Suffix appended to the name of a front image of the morphology
    MORPHOLOGY_FRONT = '_morphology_front'

    # Suffix appended to the name of a side image of the morphology
    MORPHOLOGY_SIDE = '_morphology_side'

    # Suffix appended to the name of a top image of the morphology
    MORPHOLOGY_TOP = '_morphology_top'

    # Suffix appended to the name of a directory where a 360 of the morphology will be rendered
    MORPHOLOGY_360 = '_morphology_360'

    # Suffix appended to the name of a directory where a progressive sequence will be rendered
    MORPHOLOGY_PROGRESSIVE = '_morphology_progressive'

    # Suffix appended to the name of a front image of a reconstructed mesh
    MESH_FRONT = '_mesh_front'

    # Suffix appended to the name of a side image of a reconstructed mesh
    MESH_SIDE = '_mesh_side'

    # Suffix appended to the name of a top image of a reconstructed mesh
    MESH_TOP = '_mesh_top'

    # Suffix appended to the name of a directory where a 360 of the mesh will be rendered
    MESH_360 = '_mesh_360'

    # Rendered with a fixed radius
    FIXED_RADIUS = '_fixed_radius'

    # Dendrogram
    DENDROGRAM = '_dendrogram'

    # Synaptics
    SYNAPTICS_FRONT = "_synaptics_front"
    SYNAPTICS_SIDE = "_synaptics_side"
    SYNAPTICS_TOP = "_synaptics_top"

