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
import nmv
import nmv.enums


####################################################################################################
# @update_skeleton_branching
####################################################################################################
def update_skeleton_branching(morphology,
                              branching_method):
    """Update the skeleton branching into primary and secondary sections based on a selected method.

    :param morphology:
        A given morphology skeleton.
    :param branching_method:
        A selected branching method.
        * nmv.enums.Skeletonization.Branching.ANGLES: based on angles.
        * nmv.enums.Skeletonization.Branching.RADII: based on radii.
    """

    # Primary and secondary branching
    if branching_method == nmv.enums.Skeletonization.Branching.ANGLES:

        # Label the primary and secondary sections based on angles
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_angles])
    else:

        # Label the primary and secondary sections based on radii
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_radii])

    # Update the branching orders
    nmv.skeleton.ops.apply_operation_to_morphology(
        *[morphology, nmv.skeleton.ops.update_branching_order_section])
