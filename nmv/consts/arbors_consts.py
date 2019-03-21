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


####################################################################################################
# @Arbors
####################################################################################################
class Arbors:
    """Arbors constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Maximum branching order
    MAX_BRANCHING_ORDER = 100

    # Default branching order for the axon is different, as it is ignored in many cases
    AXON_DEFAULT_BRANCHING_ORDER = 2

    # Axon prefix
    AXON_PREFIX = 'Axon'

    # Basal dendrites prefix
    BASAL_DENDRITES_PREFIX = 'BasalDendrite'

    # Apical dendrites prefix
    APICAL_DENDRITES_PREFIX = 'ApicalDendrite'

    # A little distance before p0 on the root section from the soma side (for nice connection)
    SOMA_EXTRUSION_DELTA = 0.7

    # A little distance before p0 on the root section from the arbor side (for nice connection)
    ARBOR_EXTRUSION_DELTA = 0.2

    # The number of samples that will be used to extend a section from the root section to soma
    N_SAMPLES_ROOT_TO_ORIGIN = 5

    # The index of the sample index in an SWC file
    SWC_SAMPLE_INDEX_IDX = 0

    # The index of the type of a sample in an SWC file
    SWC_SAMPLE_TYPE_IDX = 1

    # The index of the x-coordinates of a sample in an SWC file
    SWC_SAMPLE_X_COORDINATES_IDX = 2

    # The index of the y-coordinates of a sample in an SWC file
    SWC_SAMPLE_Y_COORDINATES_IDX = 3

    # The index of the z-coordinates of a sample in an SWC file
    SWC_SAMPLE_Z_COORDINATES_IDX = 4

    # The index of the radius of a sample in an SWC file
    SWC_SAMPLE_RADIUS_IDX = 5

    # The index of the parent index of a sample in an SWC file
    SWC_SAMPLE_PARENT_INDEX_IDX = 6

    # The index of a sample that has no parent in an SWC file
    SWC_NO_PARENT_SAMPLE_TYPE = -1

    # The index of an undefined samples in an SWC file
    SWC_UNDEFINED_SAMPLE_TYPE = 0

    # The index of a soma sample in an SWC file
    SWC_SOMA_SAMPLE_TYPE = 1

    # the index of an axon sample in an SWC file
    SWC_AXON_SAMPLE_TYPE = 2

    # The index of a basal dendrite sample in an SWC file
    SWC_BASAL_DENDRITE_SAMPLE_TYPE = 3

    # The index of an apical dendrite sample in an SWC file
    SWC_APICAL_DENDRITE_SAMPLE_TYPE = 4

    # The index of a fork point sample (bi- or tri-furcation)
    SWC_FORK_POINT_SAMPLE_TYPE = 5

    # The index of an end point sample in an SWC file
    SWC_END_POINT_SAMPLE_TYPE = 6

    # The index of a custom sample in an SWC file
    SWC_CUSTOM_SAMPLE_TYPE = 7

    # The directory that stores morphology points in an .H5 file
    H5_POINTS_DIRECTORY = '/points'

    # The directory that stores morphology connectivity in an .H5 file
    H5_STRUCTURE_DIRECTORY = '/structure'

    # The directory that stores morphology perimeters in an .H5 file
    # This is only used for glia, but not used for neurons
    H5_PERIMETERS_DIRECTORY = '/perimeters'

    # The index of the x-coordinates of a sample in an H5 file
    H5_SAMPLE_X_COORDINATES_IDX = 0

    # The index of the y-coordinates of a sample in an H5 file
    H5_SAMPLE_Y_COORDINATES_IDX = 1

    # The index of the z-coordinates of a sample in an H5 file
    H5_SAMPLE_Z_COORDINATES_IDX = 2

    # The index of the radius of a sample in an H5 file
    H5_SAMPLE_RADIUS_IDX = 3

    # The identifier of a section of type axon in an H5 file
    H5_AXON_SECTION_TYPE = 2

    # The identifier of a section of type basal dendrite in an H5 file
    H5_BASAL_DENDRITE_SECTION_TYPE = 3

    # The identifier of a section of type apical dendrite in an H5 file
    H5_APICAL_DENDRITE_SECTION_TYPE = 4
