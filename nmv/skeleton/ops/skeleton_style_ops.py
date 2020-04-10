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

# Internal imports
import nmv.enums
import nmv.skeleton


####################################################################################################
# @update_arbors_style
####################################################################################################
def update_arbors_style(morphology,
                        arbor_style):
    """Update the style of the arbors of a given morphology skeleton.

    :param morphology:
        A given morphology skeleton.
    :param arbor_style:
        A given style to be applied on the arbors of the morphology skeleton.
    """

    # Taper the sections
    if arbor_style == nmv.enums.Skeleton.Style.TAPERED or \
       arbor_style == nmv.enums.Skeleton.Style.TAPERED_ZIGZAG:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.taper_section])

    # Zigzag the sections
    if arbor_style == nmv.enums.Skeleton.Style.ZIGZAG or \
       arbor_style == nmv.enums.Skeleton.Style.TAPERED_ZIGZAG:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.zigzag_section])

    # Straight
    if arbor_style == nmv.enums.Skeleton.Style.STRAIGHT:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.simplify_section_to_straight_line])


####################################################################################################
# @update_arbors_radii
####################################################################################################
def update_arbors_radii(morphology,
                        morphology_options):
    """Update the radii of the arbors of a given morphology skeleton.

    :param morphology:
        A given morphology skeleton.
    :param morphology_options:
        Morphology options.
    """

    # Selected option
    option = morphology_options.arbors_radii

    # Filtered
    if option == nmv.enums.Skeleton.Radii.FILTERED:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.filter_section_sub_threshold,
              morphology_options.threshold_radius])

    elif option == nmv.enums.Skeleton.Radii.UNIFIED:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.unify_section_radii,
              morphology_options.samples_unified_radii_value])

    elif option == nmv.enums.Skeleton.Radii.UNIFIED_PER_ARBOR_TYPE:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.unify_section_radii_based_on_type,
              morphology_options.axon_samples_unified_radii_value,
              morphology_options.apical_dendrite_samples_unified_radii_value,
              morphology_options.basal_dendrites_samples_unified_radii_value])

    elif option == nmv.enums.Skeleton.Radii.SCALED:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.scale_section_radii,
              morphology_options.sections_radii_scale])
    else:
        return

