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
import math

# Internal imports
import neuromorphovis as nmv
from neuromorphovis.analysis import AnalysisItem
from neuromorphovis.analysis import *
import neuromorphovis.skeleton


####################################################################################################
# @compute_morphology_total_number_samples
####################################################################################################
def compute_morphology_total_number_samples(morphology):
    """Computes the total number of samples of the morphology.

    Note that we use the number of segments to account for the number of samples to avoid
    double-counting the branching points.

    :param morphology:
        A given morphology to analyze.
    :return
        Total number of samples of the morphology.
    """

    # A list that will contain the number of samples per section
    sections_number_samples = list()

    # Compute the number of segments of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_number_of_segments_per_section,
          sections_number_samples])

    # Total number of samples
    total_number_samples = 0

    # Iterate and sum up
    for section_number_samples in sections_number_samples:

        # Add to the total number of samples
        total_number_samples += section_number_samples

    # Add the root sample that is not considered a bifurcation point
    total_number_samples += 1

    # Return the total number of samples of the given arbor
    return total_number_samples