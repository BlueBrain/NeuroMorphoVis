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
    if arbor_style == nmv.enums.Arbors.Style.TAPERED or \
       arbor_style == nmv.enums.Arbors.Style.TAPERED_ZIGZAG:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.taper_section])

    # Zigzag the sections
    if arbor_style == nmv.enums.Arbors.Style.ZIGZAG or \
       arbor_style == nmv.enums.Arbors.Style.TAPERED_ZIGZAG:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.zigzag_section])


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

    # Filter the radii of the sections
    #if morphology_options.arbors_radii == nmv.enums.Skeletonization.ArborsRadii.FILTERED:
    #    nmv.skeleton.ops.apply_operation_to_morphology(
    #        *[morphology, nmv.skeleton.ops.filter_section_sub_threshold,
    #          morphology_options.threshold_radius])

    if morphology_options.arbors_radii == nmv.enums.Skeletonization.ArborsRadii.FIXED:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.fix_section_radii,
              morphology_options.sections_fixed_radii_value])

    elif morphology_options.arbors_radii == nmv.enums.Skeletonization.ArborsRadii.SCALED:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[morphology, nmv.skeleton.ops.scale_section_radii,
              morphology_options.sections_radii_scale])
    else:
        pass
