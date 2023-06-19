####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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

import nmv
import nmv.analysis


####################################################################################################
# @add_distributions
####################################################################################################
def add_distributions(analysis_distributions,
                      maximum_branching_order=None):
    """Adds the distributions computed per arbor (or neurite) to compute the total distribution of
    the entire morphology.

    :param analysis_distributions:
        A structure that contains the analysis distributions of the axon, basal and apical
        dendrites. Note that this struct contains a member for the morphology which will be filled
        here.
    :param maximum_branching_order:
        The maximum branching order of the morphology. If not given or equal to None, it is
        automatically computed from the input distributions.
    """

    # Make sure that the distributions are not empty
    if analysis_distributions is None:
        return

    # Compute the maximum branching order if not given
    if maximum_branching_order is None:

        # Initially set to Zero
        maximum_branching_order = 0

        # Every item contains a list of two values: item[0]: branching order, item[1]: value
        for item in analysis_distributions:
            if item[0] > maximum_branching_order:
                maximum_branching_order = item[0]

    # Compile a list that is composed of nested lists equivalent to the maximum branching order
    compiled_data = list()
    for i in range(maximum_branching_order):
        compiled_data.append(0)

    # Sum up
    for item in analysis_distributions:
        compiled_data[item[0] - 1] += item[1]

    # Aggregate list
    aggregate_analysis_data = list()
    for i, item in enumerate(compiled_data):
        aggregate_analysis_data.append([i + 1, item])

    # Return the final aggregate list
    return aggregate_analysis_data
