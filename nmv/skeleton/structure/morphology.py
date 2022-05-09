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

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.analysis
import nmv.bbox
import nmv.skeleton
import nmv.utilities


####################################################################################################
# Morphology
####################################################################################################
class Morphology:
    """
    A class to represent the morphological skeleton of a tree structure, for example neuron.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 soma=None, 
                 axons=None,
                 basal_dendrites=None,
                 apical_dendrites=None,
                 gid=None, 
                 mtype=None,
                 label=None):
        """Constructor

        :param soma:
            Morphology soma.
        :param axons:
            Morphology axons sections, if available.
        :param basal_dendrites:
            Morphology basal dendrites sections, if available.
        :param apical_dendrites:
            Morphology apical dendrites sections, if available.
        :param gid:
            Morphology GID, if available.
        :param mtype:
            Morphology type, if available.
        :param label:
            A given label to the morphology. If the morphology is loaded from a file, the label
            will be set to the file prefix, however, if it was loaded from a circuit it will be
            set to its gid prepended by a 'neuron_' prefix.
        """

        # Morphology soma
        self.soma = soma

        # Morphology axons
        self.axons = axons

        # Morphology basal dendrites
        self.basal_dendrites = basal_dendrites

        # Morphology apical dendrites
        self.apical_dendrites = apical_dendrites

        # A copy of the original axons list, needed for comparison
        self.original_axons = copy.deepcopy(axons)

        # A copy of the original basal dendrites list, needed for comparison
        self.original_basal_dendrites = copy.deepcopy(basal_dendrites)

        # A copy of the original apical dendrites list, needed for comparison
        self.origin_apical_dendrites = copy.deepcopy(apical_dendrites)

        # Morphology GID
        self.gid = gid

        # Morphology type
        self.mtype = mtype

        # The original center of the morphology
        self.original_center = None

        # Number of stems as reported in the morphology file
        self.number_stems = 0

        # Morphology label (will be morphology name or gid)
        self.label = label
        if gid is not None:
            self.label = str(gid)

        # Morphology full bounding box
        self.bounding_box = None

        # Relaxed bounding box
        self.relaxed_bounding_box = None

        # Morphology unified bounding box
        self.unified_bounding_box = None

        # Update the bounding boxes
        self.compute_bounding_box()

        # Update the branching order
        self.update_branching_order()

        # Maximum branching order
        self.maximum_branching_order = 1000

        # The color of the apical dendrites, see @create_morphology_color_palette
        self.apical_dendrites_colors = None

        # The colors of the basal dendrites, see @create_morphology_color_palette
        self.basal_dendrites_colors = None

        # The color of the axons, see @create_morphology_color_palette
        self.axons_colors = None

        # The color of the soma, see @create_morphology_color_palette
        self.soma_color = None

        # Statistical analysis data of the morphology
        self.stats = nmv.analysis.MorphologyStats()

        # Statistical analysis data of each arbor in the morphology
        self.arbors_stats = [nmv.analysis.ArborStats()] * self.get_total_number_of_arbors()

        # If this is an astrocyte morphologies, this should be a list of endfeet, otherwise None
        self.endfeet = list()

        # If the loaded morphology is an astrocyte, update this flag to True
        self.is_astrocyte = False

    ################################################################################################
    # @build_samples_lists_recursively
    ################################################################################################
    def build_samples_lists_recursively(self,
                                        section,
                                        samples_list=[]):
        """Build the list of samples recursively.

        :param section:
            A given section to get its samples.
        :param samples_list:
            A list to append the samples to.
        """

        for i_sample in section.samples:
            samples_list.append(i_sample)

        for child in section.children:
            self.build_samples_lists_recursively(child, samples_list)

    ################################################################################################
    # @has_axons
    ################################################################################################
    def has_axons(self):
        """Checks if the morphology has axons reported in the data or not.

        :return:
            True or False.
        """

        if self.axons is None:
            return False
        return True

    ################################################################################################
    # @has_basal_dendrites
    ################################################################################################
    def has_basal_dendrites(self):
        """Checks if the morphology has basal dendrites reported in the data or not.

        :return:
            True or False.
        """

        if self.basal_dendrites is None:
            return False
        return True

    ################################################################################################
    # @has_apical_dendrites
    ################################################################################################
    def has_apical_dendrites(self):
        """
        Checks if the morphology has an apical dendrites reported in the data or not.

        :return:
            True or False.
        """

        if self.apical_dendrites is None:
            return False
        return True

    ################################################################################################
    # @has_endfeet
    ################################################################################################
    def has_endfeet(self):
        """Checks if the morphology has endfeet or not.

        :return:
            True or False.
        """

        # None by default returns no endfeet
        if self.endfeet is None:
            return False

        # Assuming an empty list, then has no endfeet
        if len(self.endfeet) == 0:
            return False

        # Otherwise, yes it has endfeet
        return True

    ################################################################################################
    # @compute_bounding_box
    ################################################################################################
    def compute_bounding_box(self):
        """
        Computes the bounding box of the morphology
        """

        # A list of all the bounding boxed of all the arbors
        morphology_bounding_boxes = list()

        # Compute the bounding box of the axons
        if self.has_axons():
            for arbor in self.axons:
                morphology_bounding_boxes.append(nmv.skeleton.ops.compute_arbor_bounding_box(arbor))

        # Compute basal dendrites bounding boxes
        if self.has_basal_dendrites():
            for arbor in self.basal_dendrites:
                morphology_bounding_boxes.append(
                    nmv.skeleton.ops.compute_arbor_bounding_box(arbor))

        # Compute apical dendrites bounding boxes
        if self.has_apical_dendrites():
            for arbor in self.apical_dendrites:
                morphology_bounding_boxes.append(
                    nmv.skeleton.ops.compute_arbor_bounding_box(arbor))

        # Get the joint bounding box from the list
        morphology_bounding_box = nmv.bbox.extend_bounding_boxes(morphology_bounding_boxes)

        # Save the morphology bounding box
        self.bounding_box = copy.deepcopy(morphology_bounding_box)

        '''
        # Extend the bounding box a little to verify the results
        morphology_bounding_box.p_min[0] -= 5
        morphology_bounding_box.p_min[1] -= 5
        morphology_bounding_box.p_min[2] -= 5
        morphology_bounding_box.p_max[0] += 5
        morphology_bounding_box.p_max[1] += 5
        morphology_bounding_box.p_max[2] += 5
        morphology_bounding_box.bounds[0] += 10
        morphology_bounding_box.bounds[1] += 10
        morphology_bounding_box.bounds[2] += 10

        # Save the morphology bounding box
        self.relaxed_bounding_box = copy.deepcopy(morphology_bounding_box)

        # Compute the unified bounding box
        self.unified_bounding_box = nmv.bbox.compute_unified_bounding_box(self.relaxed_bounding_box)
        '''

    ################################################################################################
    # @set_section_branching_order
    ################################################################################################
    def set_section_branching_order(self,
                                    section,
                                    order=1):
        """Sets the branching order of the section and its children recursively.

        :param section:
            A given section.
        :param order:
            Section branching order.
        """

        # Set the branching order of the section
        section.branching_order = order

        # Set the branching order of the children
        for child in section.children:
            self.set_section_branching_order(section=child, order=order + 1)

    ################################################################################################
    # @update_branching_order
    ################################################################################################
    def update_branching_order(self):
        """Updates the branching order of the arbors.
        """

        # Apical dendrites
        if self.has_apical_dendrites():
            for arbor in self.apical_dendrites:
                self.set_section_branching_order(arbor)

        # Axons
        if self.has_axons():
            for arbor in self.axons:
                self.set_section_branching_order(arbor)

        # Basal dendrites
        if self.has_basal_dendrites():
            for arbor in self.basal_dendrites:
                self.set_section_branching_order(arbor)

    ################################################################################################
    # @get_total_number_of_arbors
    ################################################################################################
    def get_total_number_of_arbors(self):
        """Computes the total number of arbors in the morphology.

        :return:
            The total number of arbors or neurites in the morphology.
        """

        # The total number of arbors
        total_arbor_count = 0

        # Apical dendrites
        if self.has_apical_dendrites():
            total_arbor_count += len(self.apical_dendrites)

        # Basal dendrites
        if self.has_basal_dendrites():
            total_arbor_count += len(self.basal_dendrites)

        # Axons
        if self.has_axons():
            total_arbor_count += len(self.axons)

        # Return the total
        return total_arbor_count

    ################################################################################################
    # @create_morphology_color_palette
    ################################################################################################
    def create_morphology_color_palette(self,
                                        palette_name=None):

        # Verify the presence of the plotting packages
        nmv.utilities.verify_plotting_packages()

        import numpy
        import matplotlib
        matplotlib.use('agg')
        import matplotlib.pyplot

        # TODO: Add further palettes
        # palette = seaborn.color_palette("pastel", self.get_total_number_of_arbors())

        palette = matplotlib.pyplot.get_cmap('Spectral')

        step = 1
        palette = palette(numpy.linspace(0, 1.0, step * (1 + self.get_total_number_of_arbors())))

        shade_factor = 0.9
        for i in range(len(palette)):
            palette[i][0] *= shade_factor
            palette[i][1] *= shade_factor
            palette[i][2] *= shade_factor

        # An index to keep track on the colors
        color_index = 0

        # Apical dendrites
        if self.has_apical_dendrites():
            self.apical_dendrites_colors = list()
            for arbor in self.apical_dendrites:
                self.apical_dendrites_colors.append(palette[color_index])
                arbor.color = Vector((palette[color_index][0],
                                      palette[color_index][1],
                                      palette[color_index][2]))
                color_index += step

        # Basal dendrites
        if self.has_basal_dendrites():
            self.basal_dendrites_colors = list()
            for arbor in self.basal_dendrites:
                self.basal_dendrites_colors.append(palette[color_index])
                arbor.color = Vector((palette[color_index][0],
                                      palette[color_index][1],
                                      palette[color_index][2]))
                color_index += step

        # Axons
        if self.has_axons():
            self.axons_colors = list()
            for arbor in self.axons:
                self.axons_colors.append(palette[color_index])
                arbor.color = Vector((palette[color_index][0],
                                      palette[color_index][1],
                                      palette[color_index][2]))
                color_index += step

        # Soma
        self.soma_color = Vector((palette[color_index][0],
                                  palette[color_index][1],
                                  palette[color_index][2]))






