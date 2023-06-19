####################################################################################################
# Copyright (c) 2016 _ 2020, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender_based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################


####################################################################################################
# @Analysis
####################################################################################################
class Analysis:
    """Analysis constants"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # These constants are only used to make it easy gathering all the generated analysis PDFs and
    # PNGs into a single document later.
    NUMBER_SAMPLE_PER_ARBOR = 'number_of_samples_per_arbor'
    NUMBER_TERMINAL_TIPS_PER_ARBOR = 'number_of_terminal_tips_per_arbor'
    NUMBER_TERMINAL_SEGMENTS_PER_ARBOR = 'number_of_terminal_segments_per_arbor'
    NUMBER_SECTIONS_PER_ARBOR = 'number_of_sections_per_arbor'

    # Branching
    MAXIMUM_BRANCHING_ORDER_PER_ARBOR = 'maximum_branching_order_per_arbor'
    NUMBER_BIFURCATIONS_PER_ARBOR = 'number_of_bifurcations_per_arbor'

    # Distance
    MAXIMUM_PATH_DISTANCE_PER_ARBOR = 'maximum_path_distance_per_arbor'
    MAXIMUM_EUCLIDEAN_DISTANCE_PER_ARBOR = 'maximum_euclidean_distance_per_arbor'
    MINIMUM_EUCLIDEAN_DISTANCE_PER_ARBOR = 'minimum_euclidean_distance_per_arbor'

    # Length
    ARBOR_LENGTH = 'arbor_length'
    SECTIONS_LENGTH_RANGE_PER_ARBOR = 'sections_length_range_per_arbor'
    SEGMENTS_LENGTH_RANGE_PER_ARBOR = 'segments_length_range_per_arbor'

    # Surface Area
    ARBOR_SURFACE_AREA = 'arbor_surface_area'
    SECTIONS_SURFACE_RANGE_PER_ARBOR = 'sections_surface_area_range_per_arbor'
    SEGMENTS_SURFACE_RANGE_PER_ARBOR = 'segments_surface_area_range_per_arbor'

    # Volume
    ARBOR_VOLUME = 'arbor_volume'
    SECTIONS_VOLUME_RANGE_PER_ARBOR = 'sections_volume_range_per_arbor'
    SEGMENTS_VOLUME_RANGE_PER_ARBOR = 'segments_volume_range_per_arbor'

    # Ratios
    CONTRACTION_PER_ARBOR = 'contraction_per_arbor'
    SAMPLES_RADII_PER_ARBOR = 'samples_radii_range_per_arbor'
    TAPER_1_RANGE_PER_ARBOR = 'burke_taper_range_per_arbor'
    TAPER_2_RANGE_PER_ARBOR = 'hillman_taper_range_per_arbor'
    DAUGHTER_RATIO_RANGE_PER_ARBOR = 'daughter_ratio_range_per_arbor'
    PARENT_DAUGHTER_RATIO_RANGE_PER_ARBOR = 'parent_daughter_ratio_range_per_arbor'

    # Angles
    LOCAL_BIFURCATION_ANGLE_RANGE_PER_ARBOR = 'local_bifurcation_angle_range_per_arbor'
    GLOBAL_BIFURCATION_ANGLE_RANGE_PER_ARBOR = 'global_bifurcation_angle_range_per_arbor'

    # Artifacts
    NUMBER_SHORT_SECTIONS_PER_ARBOR = 'number_of_short_sections_per_arbor'
    NUMBER_ZERO_RADII_SAMPLES_PER_ARBOR = 'number_of_zero_radii_samples_per_arbor'

    # Analysis text file
    ANALYSIS_FILE_NAME = 'analysis_results'
