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
    """A class to represent a section of a given spine
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

        # Morphology full bounding box
        self.bounding_box = None

        # Update the bounding boxes
        self.compute_bounding_box()

    ################################################################################################
    # @compute_bounding_box
    ################################################################################################
    def compute_bounding_box(self):
        """Computes the bounding box of the morphology
        """

        # Make sure that it has at least one section
        if len(self.sections) == 0:
            return

        # Compute the bounding box for each section
        spine_morphology_bounding_boxes = \
            nmv.skeleton.ops.compute_sections_list_bounding_box(self.sections)

        # Get the joint bounding box from the list if it has more then one section
        if len(spine_morphology_bounding_boxes) > 1:
            spine_morphology_bounding_box = nmv.bbox.extend_bounding_boxes(
                spine_morphology_bounding_boxes)

            # Save the morphology bounding box
            self.bounding_box = copy.deepcopy(spine_morphology_bounding_box)

        # Otherwise, just get the first one
        else:
            self.bounding_box = spine_morphology_bounding_boxes[0]
