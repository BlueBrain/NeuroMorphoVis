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

from neuromorphovis.analysis import AnalysisItem
from neuromorphovis.analysis import arbor_analysis_ops

####################################################################################################
# Apply each item in this list on the morphology
####################################################################################################
per_morphology = [

]


####################################################################################################
# Apply each item in this list on each arbor or neurite in the morphology
####################################################################################################
per_arbor = [

    ################################################################################################
    # Length
    ################################################################################################
    # Total neurite length
    AnalysisItem(variable='TotalLength',
                 name='Total Length',
                 filter_function=arbor_analysis_ops.compute_arbor_total_length,
                 description='Total length of the neurite',
                 data_format='FLOAT',
                 unit='LENGTH'),

    ################################################################################################
    # Area
    ################################################################################################
    # Total neurite surface area
    AnalysisItem(variable='TotalSurfaceArea',
                 name='Total Surface Area',
                 filter_function=arbor_analysis_ops.compute_arbor_total_surface_area,
                 description='Total surface area of the neurite',
                 data_format='FLOAT',
                 unit='AREA'),
]






