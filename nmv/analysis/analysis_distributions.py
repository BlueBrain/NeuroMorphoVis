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
from .structs import *
from .kernels import *
import nmv.enums


distributions = [

    AnalysisDistribution(
        name='Total Number of Samples per Arbor',
        description='The total number of sampler per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Samples / Arbor',
        figure_name='number-of-samples-per-arbor',
        figure_xlabel='Number of Samples',
        compute_total_kernel=compute_number_of_samples_of_arbor,
        add_percentage=True),
]

####################################################################################################
# Global analysis items, only applied on a global level not per-arbor level
####################################################################################################
distributionss = [

    AnalysisDistribution(
        name='Total Number of Samples per Arbor',
        description='The total number of sampler per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Samples / Arbor',
        figure_name='number-of-samples-per-arbor',
        figure_xlabel='Number of Samples',
        compute_total_kernel=compute_number_of_samples_of_arbor,
        add_percentage=True),

    AnalysisDistribution(
        name='Total Number of Terminal Tips per Arbor',
        description='The total number of terminal tips per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Terminal Tips / Arbor',
        figure_name='number-of-terminal-tips-per-arbor',
        figure_xlabel='Number of Tips',
        compute_total_kernel=compute_total_number_of_terminal_tips_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Total Number of Bifurcations per Arbor',
        description='The total number of bifurcations per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Bifurcations / Arbor',
        figure_name='number-of-bifurcations-per-arbor',
        figure_xlabel='Number of Bifurcations',
        compute_total_kernel=compute_total_number_of_bifurcations_of_arbor,
        add_percentage=True),

    AnalysisDistribution(
        name='Maximum Branching Order per Arbor',
        description='The maximum branching order per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Maximum Branching Order / Arbor',
        figure_name='maximum-branching-order-per-arbor',
        figure_xlabel='Branching Order',
        compute_total_kernel=compute_maximum_branching_order_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Total Arbor Length',
        description='The total length of each arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Arbor Length',
        figure_name='arbor-length',
        figure_xlabel='Length (\u03BCm)',
        compute_total_kernel=compute_total_length_of_arbor,
        add_percentage=True),

    AnalysisDistribution(
        name='Samples Radii Range per Arbor',
        description='The range of samples radii per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Samples Radii Range / Arbor',
        figure_name='samples-radii-range-per-arbor',
        figure_xlabel='Sample Radius (\u03BCm)',
        compute_min_kernel=compute_minimum_sample_radius_of_arbor,
        compute_avg_kernel=compute_average_sample_radius_of_arbor,
        compute_max_kernel=compute_maximum_sample_radius_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Total Number of Section per Arbor',
        description='The total number of sections per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Sections / Arbor',
        figure_name='number-of-sections-per-arbor',
        figure_xlabel='Number of Sections',
        compute_total_kernel=compute_total_number_of_sections_of_arbor,
        add_percentage=True),

    AnalysisDistribution(
        name='Total Number of Short Section per Arbor',
        description='The total number of short sections (where the length of the section is '
                    'less than the sum of the diameters of the first and last samples) per arbor '
                    'in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Short Sections / Arbor',
        figure_name='number-of-short-sections-per-arbor',
        figure_xlabel='Number of Short Sections',
        compute_total_kernel=compute_number_of_short_sections_of_arbor,
        add_percentage=True),

    AnalysisDistribution(
        name='Maximum Path Distance per Arbor',
        description='The maximum distance from the soma to the terminal tip per arbor in the '
                    'morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Maximum Path Distance / Arbor',
        figure_name='maximum-path-distance-per-arbor',
        figure_xlabel='Path Distance from Soma (\u03BCm)',
        compute_total_kernel=compute_maximum_path_distance_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Maximum Euclidean Distance per Arbor',
        description='The maximum radial distance from the soma to the terminal tip per arbor in '
                    'the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Maximum Euclidean Distance / Arbor',
        figure_name='maximum-euclidean-distance-per-arbor',
        figure_xlabel='Radial Distance from Soma (\u03BCm)',
        compute_total_kernel=compute_maximum_euclidean_distance_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Minimum Euclidean Distance per Arbor',
        description='The minimum radial distance from the soma to the first sample along every '
                    'arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Minimum Euclidean Distance / Arbor',
        figure_name='minimum-euclidean-distance-per-arbor',
        figure_xlabel='Radial Distance from Soma (\u03BCm)',
        compute_total_kernel=compute_minimum_euclidean_distance_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Sections Contraction Range per Arbor',
        description='The range of sections contraction per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Sections Contraction Range / Arbor',
        figure_name='sections-contraction-range-per-arbor',
        figure_xlabel='Contraction Ratio',
        compute_min_kernel=compute_minimum_section_contraction_of_arbor,
        compute_avg_kernel=compute_average_section_contraction_of_arbor,
        compute_max_kernel=compute_maximum_section_contraction_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Arbor Surface Area',
        description='The surface area of each arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Arbor Surface Area',
        figure_name='arbor-surface-area',
        figure_xlabel='Area (\u03BCm\u00b2)',
        compute_total_kernel=compute_arbor_total_surface_area,
        add_percentage=True),

    AnalysisDistribution(
        name='Arbor Volume',
        description='The volume of each arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Arbor Volume',
        figure_name='arbor-volume',
        figure_xlabel='Area (\u03BCm\u00b3)',
        compute_total_kernel=compute_arbor_total_volume,
        add_percentage=True),

    AnalysisDistribution(
        name='Sections Length Range per Arbor',
        description='The range of sections length per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Sections Length Range / Arbor',
        figure_name='sections-length-range-per-arbor',
        figure_xlabel='Length (\u03BCm)',
        compute_min_kernel=compute_minimum_section_length_of_arbor,
        compute_avg_kernel=compute_average_section_length_of_arbor,
        compute_max_kernel=compute_maximum_section_length_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Segments Length Range per Arbor',
        description='The range of segments length per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Segments Length Range / Arbor',
        figure_name='segments-length-range-per-arbor',
        figure_xlabel='Length (\u03BCm)',
        compute_min_kernel=compute_minimum_segment_length_of_arbor,
        compute_avg_kernel=compute_average_segment_length_of_arbor,
        compute_max_kernel=compute_maximum_segment_length_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Sections Surface Area Range per Arbor',
        description='The range of sections surface area per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Sections Surface Area Range / Arbor',
        figure_name='sections-surface-area-range-per-arbor',
        figure_xlabel='Area (\u03BCm\u00b2)',
        compute_min_kernel=compute_minimum_section_surface_area,
        compute_avg_kernel=compute_average_section_surface_area,
        compute_max_kernel=compute_maximum_section_surface_area,
        add_percentage=False),

    AnalysisDistribution(
        name='Segments Surface Area Range per Arbor',
        description='The range of segments surface area per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Segments Surface Area Range / Arbor',
        figure_name='segments-surface-area-range-per-arbor',
        figure_xlabel='Area (\u03BCm\u00b2)',
        compute_min_kernel=compute_minimum_segment_surface_area,
        compute_avg_kernel=compute_average_segment_surface_area,
        compute_max_kernel=compute_maximum_segment_surface_area,
        add_percentage=False),

    AnalysisDistribution(
        name='Sections Volume Range per Arbor',
        description='The range of sections volume per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Sections Volume Range / Arbor',
        figure_name='sections-volume-range-per-arbor',
        figure_xlabel='Volume (\u03BCm\u00b3)',
        compute_min_kernel=compute_minimum_section_volume,
        compute_avg_kernel=compute_average_section_volume,
        compute_max_kernel=compute_maximum_section_volume,
        add_percentage=False),

    AnalysisDistribution(
        name='Segments Volume Range per Arbor',
        description='The range of segments volume per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Segments Volume Range / Arbor',
        figure_name='segments-volume-range-per-arbor',
        figure_xlabel='Volume (\u03BCm\u00b3)',
        compute_min_kernel=compute_minimum_segment_volume,
        compute_avg_kernel=compute_average_segment_volume,
        compute_max_kernel=compute_maximum_segment_volume,
        add_percentage=False),
]

'''
distributionss = [

    
    

    


    

    AnalysisDistribution(
        name='Samples Radii',
        kernel=kernel_samples_radii,
        description='Radii range',
        data_format='FLOAT',
        figure_title='Samples Radii',
        figure_axis_label='Sample Radius (\u03BCm)',
        figure_label='samples-radii'),

]
'''
