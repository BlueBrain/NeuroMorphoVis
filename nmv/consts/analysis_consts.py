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


####################################################################################################
# Analysis
####################################################################################################
class Analysis:
    """Analysis constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # These constants are only used to make it easy gathering all the generated analysis PDFs and
    # PNGs into a single document later.
    NUMBER_SAMPLE_PER_ARBOR = 'number-of-samples-per-arbor'
    NUMBER_TERMINAL_TIPS_PER_ARBOR = 'number-of-terminal-tips-per-arbor'
    NUMBER_TERMINAL_SEGMENTS_PER_ARBOR = 'number-of-terminal-segments-per-arbor'
    NUMBER_SECTIONS_PER_ARBOR = 'number-of-sections-per-arbor'

    # Branching
    MAXIMUM_BRANCHING_ORDER_PER_ARBOR = 'maximum-branching-order-per-arbor'
    NUMBER_BIFURCATIONS_PER_ARBOR = 'number-of-bifurcations-per-arbor'

    # Distance
    MAXIMUM_PATH_DISTANCE_PER_ARBOR = 'maximum-path-distance-per-arbor'
    MAXIMUM_EUCLIDEAN_DISTANCE_PER_ARBOR = 'maximum-euclidean-distance-per-arbor'
    MINIMUM_EUCLIDEAN_DISTANCE_PER_ARBOR = 'minimum-euclidean-distance-per-arbor'

    # Length
    ARBOR_LENGTH = 'arbor-length'
    SECTIONS_LENGTH_RANGE_PER_ARBOR = 'sections-length-range-per-arbor'
    SEGMENTS_LENGTH_RANGE_PER_ARBOR = 'segments-length-range-per-arbor'

    # Surface Area
    ARBOR_SURFACE_AREA = 'arbor-surface-area'
    SECTIONS_SURFACE_RANGE_PER_ARBOR = 'sections-surface-area-range-per-arbor'
    SEGMENTS_SURFACE_RANGE_PER_ARBOR = 'segments-surface-area-range-per-arbor'

    # Volume
    ARBOR_VOLUME = 'arbor-volume'
    SECTIONS_VOLUME_RANGE_PER_ARBOR = 'sections-volume-range-per-arbor'
    SEGMENTS_VOLUME_RANGE_PER_ARBOR = 'segments-volume-range-per-arbor'

    # Ratios
    CONTRACTION_PER_ARBOR = 'contraction-per-arbor'
    SAMPLES_RADII_PER_ARBOR = 'samples-radii-range-per-arbor'
    TAPER_1_RANGE_PER_ARBOR = 'burke-taper-range-per-arbor'
    TAPER_2_RANGE_PER_ARBOR = 'hillman-taper-range-per-arbor'
    DAUGHTER_RATIO_RANGE_PER_ARBOR = 'daughter-ratio-range-per-arbor'
    PARENT_DAUGHTER_RATIO_RANGE_PER_ARBOR = 'parent-daughter-ratio-range-per-arbor'

    # Angles
    LOCAL_BIFURCATION_ANGLE_RANGE_PER_ARBOR = 'local-bifurcation-angle-range-per-arbor'
    GLOBAL_BIFURCATION_ANGLE_RANGE_PER_ARBOR = 'global-bifurcation-angle-range-per-arbor'

    # Artifacts
    NUMBER_SHORT_SECTIONS_PER_ARBOR = 'number-of-short-sections-per-arbor'
    NUMBER_ZERO_RADII_SAMPLES_PER_ARBOR = 'number-of-zero-radii-samples-per-arbor'
