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
import nmv.enums


####################################################################################################
# @update_skeleton_branching
####################################################################################################
def update_skeleton_branching(morphology,
                              branching_method):
    """Labels the child sections in the morphology into primary and secondary sections based on a
    selected branching method defined by the user.

    :param morphology:
        The morphology object.
    :param branching_method:
        The selected branching method, either based on angles or based on radii.
        * nmv.enums.Skeleton.Branching.ANGLES: based on angles.
        * nmv.enums.Skeleton.Branching.RADII: based on radii.
    """

    # Label the sections either based on angles or radii
    if branching_method == nmv.enums.Skeleton.Branching.ANGLES:
        nmv.skeleton.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_angles])
    else:
        nmv.skeleton.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_radii])

    # Update the branching orders
    nmv.skeleton.apply_operation_to_morphology(
        *[morphology, nmv.skeleton.ops.update_branching_order_section])
