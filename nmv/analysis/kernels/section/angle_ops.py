####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
# @compute_sections_local_bifurcation_angles
####################################################################################################
def compute_sections_local_bifurcation_angles(section,
                                              sections_local_angles):
    """Computes the local bifurcation angles of the given section.

    :param section:
        A given section to compute its surface area.
    :param sections_local_angles:
        Section local bifurcation angle.
    """

    # The section must have 'at least' two children to compute this angle.
    if section.has_children():

        # The section must have two children
        if len(section.children) == 2:

            # Access the children
            child_1 = section.children[0]
            child_2 = section.children[1]

            # If the section has less than two samples, then report the error
            if len(child_1.samples) < 2:
                return
            if len(child_2.samples) < 2:
                return

            # Construct the vectors
            vector_1 = (child_1.samples[1].point - child_1.samples[0].point)
            vector_2 = (child_2.samples[1].point - child_2.samples[0].point)

            # If the second sample in the child is located exactly at the first one, pick the third
            if vector_1.length < 1e-6:

                # Ensure that the section has at least three samples
                if len(child_1.samples) < 3:
                    return

                # Again, construct the vector
                vector_1 = (child_1.samples[2].point - child_1.samples[0].point)

                # If the vector has zero length, return
                if vector_1.length < 1e-6:
                    return

            # If the second sample in the child is located exactly at the first one, pick the third
            if vector_2.length < 1e-6:

                # Ensure that the section has at least three samples
                if len(child_2.samples) < 3:
                    return

                    # Again, construct the vector
                vector_2 = (child_2.samples[2].point - child_2.samples[0].point)

                # If the vector has zero length, return
                if vector_2.length < 1e-6:
                    return

            # Compute the bifurcation angles
            vector_1 = vector_1.normalized()
            vector_2 = vector_2.normalized()
            angle = vector_1.angle(vector_2)

            # Append the angle to the list
            sections_local_angles.append(angle * 180.0 / 3.14)


####################################################################################################
# @compute_sections_global_bifurcation_angles
####################################################################################################
def compute_sections_global_bifurcation_angles(section,
                                               sections_global_angles):
    """Computes the global bifurcation angles of the given section.

    :param section:
        A given section to compute its surface area.
    :param sections_global_angles:
        Section global bifurcation angle.
    """

    # The section must have 'at least' two children to compute this angle.
    if section.has_children():

        # The section must have at least two children
        if len(section.children) == 2:

            # Access the children
            child_1 = section.children[0]
            child_2 = section.children[1]

            # If the section has less than two samples, then report the error
            if len(child_1.samples) < 2:
                return
            if len(child_2.samples) < 2:
                return

            # Compute the vectors
            vector_1 = (child_1.samples[-1].point - child_1.samples[0].point)
            vector_2 = (child_2.samples[-1].point - child_2.samples[0].point)

            # Ensure no Zero vectors
            if vector_1.length < 1e-6:
                return
            if vector_2.length < 1e-6:
                return

            # Compute the angles
            vector_1 = vector_1.normalized()
            vector_2 = vector_2.normalized()
            angle = vector_1.angle(vector_2)

            # Append the angle to the list
            sections_global_angles.append(angle * 180.0 / 3.14)
