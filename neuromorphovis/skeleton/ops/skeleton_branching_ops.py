####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# Internal imports
import neuromorphovis as nmv
import neuromorphovis.enums


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
