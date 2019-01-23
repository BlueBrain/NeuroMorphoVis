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
# Sample
####################################################################################################
class Sample:
    """Morphological skeleton sample.

    The section is composed of a set of segments, and each segment is composed of two samples.
    Each sample has a point in the cartesian coordinates and a radius that reflect the
    cross-sectional area of the morphology at a certain point. The sample is identified by
    two indexes or IDs, the first is used to label the order of the sample along the
    morphological section, and the second represents the order of the sample in the morphology
    file.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 point,
                 radius,
                 id,
                 type=-1,
                 morphology_id=-1,
                 section=None,
                 parent_id=-1):
        """Constructor

        :param point:
            Sample position in the cartesian space, Vector((x, y, z)).
        :param radius:
            Sample radius in microns.
        :param id:
            Sample index along the section from 0 to N-1 if the section has N samples.
        :param type:
            Sample type.
        :param morphology_id:
            Sample index as reported in the morphology file.
        :param section:
            A reference to the section where the sample belongs to, initially None.
            This member is updated after re-constructing the morphology skeleton.
        """

        # Sample cartesian point
        self.point = point

        # Sample radius
        self.radius = radius

        # Sample index along the section (from 0 to N, updated after section construction)
        self.id = id

        # The global index of the sample w.r.t to the arbor it belongs to
        self.arbor_idx = -1

        # The global index of the sample w.r.t to the morphology
        self.morphology_idx = -1

        # Sample index as reported in the morphology file, -1 is UNKNOWN or AUXILIARY
        self.morphology_index = morphology_id

        # The section, where the sample belongs (updated after the section construction)
        self.section = section

        # Sample type
        self.type = type

        # The index of the parent sample, required for the connectivity of SWC files
        self.parent_id = parent_id
