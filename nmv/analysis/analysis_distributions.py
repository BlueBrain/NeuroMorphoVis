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

# Internal imports
from nmv.analysis.structs import AnalysisDistribution
from nmv.analysis.kernels.morphology import *

####################################################################################################
# Global analysis items, only applied on a global level not per-arbor level
####################################################################################################
distributions = [

    AnalysisDistribution(
        name='Samples Radii',
        kernel=kernel_samples_radii_distribution,
        description='The distribution of the radii of all the samples in the morphology',
        data_format='INT'),

    AnalysisDistribution(
        name='Number of Samples per Section w.r.t Branching Order',
        kernel=kernel_number_of_samples_at_branching_order_distributions,
        description='sss',
        data_format='INT'
    )
]
