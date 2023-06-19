####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import nmv.skeleton


####################################################################################################
# @get_connected_arbors_to_soma_after_verification
####################################################################################################
def get_connected_arbors_to_soma_after_verification(morphology,
                                                    soma_center,
                                                    soma_radius):
    """This functions checks the connectivity of all the arbors of the morphology and soma.

    :param morphology:
        The morphology skeleton.
    :param soma_radius:
        A radius used to validate if the arbors are intersecting or not.
        
    :return:
        A list of connected arbors.
    """

    # Compile a linear list of all the arbors
    all_arbors = list()
    if morphology.has_apical_dendrites():
        for arbor in morphology.apical_dendrites:
            all_arbors.append(arbor)

    if morphology.has_basal_dendrites():
        for arbor in morphology.basal_dendrites:
            all_arbors.append(arbor)

    if morphology.has_axons():
        for arbor in morphology.axons:
            all_arbors.append(arbor)

    # Exclude the arbors that are not close to the soma
    close_arbors = list()
    for arbor in all_arbors:
        if not arbor.far_from_soma:
            close_arbors.append(arbor)

    # Sort the close arbors based on radii of the first samples of the arbors
    close_arbors.sort(key=lambda close_arbor: close_arbor.samples[0].radius, reverse=True)

    # Valid arbors
    valid_arbors = list()

    # A list of the indices of the intersecting branches
    intersecting_arbors_indices = list()

    # Check the intersecting arbors
    for primary in close_arbors:

        # This flag indicates that the primary arbor is not intersecting with any other arbors
        # in the morphology. If this flag stays False after the loop, then we can safely append
        # the primary arbor to the valid_arbors list
        is_intersecting = False

        # If the primary arbor is already added to the valid_arbors list, then this flag must be
        # switched to True to avoid adding it twice
        already_valid = False

        # For each arbor
        for secondary in close_arbors:

            # Ignore the same arbor
            if primary.label == secondary.label:
                continue

            # Check the intersection
            if nmv.skeleton.arbors_intersect(primary, secondary, soma_center, soma_radius):

                # The arbor is intersecting
                is_intersecting = True

                intersecting_arbors_indices.append(primary.index)
                intersecting_arbors_indices.append(secondary.index)

                # If the radius of the primary arbor is larger than that of the secondary
                if primary.samples[0].radius > secondary.samples[0].radius:

                    # For the primary arbor
                    if not already_valid:
                        valid_arbors.append(primary)

                    already_valid = True

        # If the arbor is finally verified to be not intersecting, add it
        if not is_intersecting:

            # If the arbor is not added already to valid_arbors list, add it
            if not already_valid:
                valid_arbors.append(primary)

            # We therefore can switch the connected_to_soma flag to True
            primary.connected_to_soma = True

    # Return the valid arbors list for extrusion
    return valid_arbors
