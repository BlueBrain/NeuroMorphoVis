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

# System imports
import copy

# Blender imports
from mathutils import Vector

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.file
import neuromorphovis.skeleton


####################################################################################################
# @SWCWriter
####################################################################################################
class SWCWriter:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # The path where the morphology will be exported
        self.output_file_path = None

        self.morphology = None

        # A list of all the samples parsed from the morphology file, to be used as a lookup table
        # to construct the morphology skeleton directly
        # http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html
        # Each sample in this list has the following structure:
        #       [0] The index of the sample or sample number
        #       [1] The type of the sample or structure identifier
        #       [2] Sample x-coordinates
        #       [3] Sample y-coordinates
        #       [4] Sample z-coordinates
        #       [5] Sample radius
        #       [6] The index of the parent sample
        self.samples_list = list()

        # A list of the indices of the terminals of the sections
        # This list is only updated once during the morphology loading, and then used to build the
        # sections later in an accelerated way
        self.sections_terminal_samples_indices = list()

        # A list of the indices of each 'disconnected' section in the morphology
        self.sections_samples_indices_list = list()

        # A list of continuous paths extracted from the morphology file
        self.paths = list()


def write_morphology_to_swc_file(morphology_object,
                                 file_path):

    # Update the global indices
    nmv.skeleton.ops.update_samples_indices_per_morphology(morphology_object)

    # Soma


    samples_list = nmv.skeleton.ops.construct_samples_list_from_morphology_tree(morphology_object)

    sample_string = '1 1 0.0 0.0 0.0 7.83715 -1'

    samples_list.insert(0, sample_string)
    for i in samples_list:
        print (i)
    # Add to a list

    # dump the list to the file

    # done





