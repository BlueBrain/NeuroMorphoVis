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


# Internal imports
import nmv.options


####################################################################################################
# @Globals
####################################################################################################
class Globals:
    """UI globals"""

    def __init__(self): pass

    # This flag is used to verify if NeuroMorphoVis is already initialized or not
    nmv_initialized = False

    # NeuroMorphoVis options
    options = nmv.options.NeuroMorphoVisOptions()

    # The morphology skeleton object loaded after UI interaction
    morphology = None

    # All the icons loaded for the UI
    icons = None

    # The reconstructed soma mesh object
    soma_mesh = None

    # Builder
    morphology_builder = None

    # A list of all the objects that correspond to the reconstructed morphology skeleton
    reconstructed_skeleton = list()

    # A list of all the objects that correspond to the reconstructed mesh of the neuron
    # NOTE: If this list contains a single mesh object, then it accounts for the entire mesh after
    # joining all the mesh objects together
    reconstructed_mesh = list()

    # Reference to the circuit
    circuit = None

    is_morphology_reconstructed = False

    is_morphology_rendered = False

