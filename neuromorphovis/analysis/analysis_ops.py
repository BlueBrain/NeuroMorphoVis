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

import neuromorphovis as nmv
import neuromorphovis.analysis


####################################################################################################
# @apply_analysis_filters
####################################################################################################
def apply_analysis_filters(morphology,
                           context):
    """Applies the analysis filters one by one on the morphology

    :param morphology:
        Loaded morphology.
    :param context:
        Blender context.
    :return
        True if the analysis filters are applied without any issues, False otherwise.
   """

    try:

        # Axon
        if morphology.apical_dendrite is not None:

            # For each entry in the analysis list
            for entry in nmv.analysis.sample_per_neurite:

                # Apply the filter function
                entry.apply_filter(
                    arbor=morphology.apical_dendrite,
                    arbor_prefix=morphology.apical_dendrite.get_type_prefix(), context=context)

        # Basal dendrites
        if morphology.dendrites is not None:

            # For each basal dendrite
            for i, basal_dendrite in enumerate(morphology.dendrites):

                # For each entry in the analysis list
                for feature in nmv.analysis.sample_per_neurite:

                    # Apply the filter function
                    feature.apply_filter(
                        arbor=basal_dendrite,
                        arbor_prefix='%s%i' % (basal_dendrite.get_type_prefix(), i),
                        context=context)

        # Apical
        if morphology.axon is not None:

            # For each entry in the analysis list
            for entry in nmv.analysis.sample_per_neurite:

                # Apply the filter function
                entry.apply_filter(
                    arbor=morphology.axon,
                    arbor_prefix=morphology.axon.get_type_prefix(), context=context)

        # Return true to update the flags
        return True

    # Issue
    except ValueError:
        return False















