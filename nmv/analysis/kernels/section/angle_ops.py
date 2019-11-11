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

# System imports
import math


####################################################################################################
# @compute_section_surface_area_from_segments
####################################################################################################
def compute_sections_local_bifurcation_angles(section,
                                              sections_local_angles):
    """Computes the local bifurcation angles of the given section.

    :param section:
        A given section to compute its surface area.
    :return:
        Section local bifurcation angle.
    """

    # The section must have 'at least' two children to compute this angle.
    if section.has_children():

        if len(section.children) == 2:

            # Access the children
            child_1 = section.children[0]
            child_2 = section.children[1]

            # If the section has less than two samples, then report the error
            if len(child_1.samples) < 2:
                return

            if len(child_2.samples) < 2:
                return

            vector_1 = (child_1.samples[1].point - child_1.samples[0].point)
            vector_2 = (child_2.samples[1].point - child_2.samples[0].point)

            if vector_1.length < 1e-5:
                return

            if vector_2.length < 1e-5:
                return

            vector_1 = vector_1.normalized()
            vector_2 = vector_2.normalized()
            angle = vector_1.angle(vector_2)

            sections_local_angles.append(angle)


####################################################################################################
# @compute_sections_global_bifurcation_angles
####################################################################################################
def compute_sections_global_bifurcation_angles(section,
                                               sections_global_angles):
    """Computes the global bifurcation angles of the given section.

    :param section:
        A given section to compute its surface area.
    :return:
        Section global bifurcation angle.
    """

    # The section must have 'at least' two children to compute this angle.
    if section.has_children():

        if len(section.children) == 2:

            # Access the children
            child_1 = section.children[0]
            child_2 = section.children[1]

            # If the section has less than two samples, then report the error
            if len(child_1.samples) < 2:
                return

            if len(child_2.samples) < 2:
                return

            vector_1 = (child_1.samples[-1].point - child_1.samples[0].point)
            vector_2 = (child_2.samples[-1].point - child_2.samples[0].point)

            if vector_1.length < 1e-5:
                return

            if vector_2.length < 1e-5:
                return

            vector_1 = vector_1.normalized()
            vector_2 = vector_2.normalized()
            angle = vector_1.angle(vector_2)

            sections_global_angles.append(angle)
