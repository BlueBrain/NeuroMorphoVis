####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Blender
from mathutils import Vector, Matrix


####################################################################################################
# @get_cell_transformation
####################################################################################################
def get_cell_transformation(circuit,
                            gid):
    """Get the transformation matrix of a neuron identified by a GID.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :return:
        The transformation matrix of the neuron in Blender format.
    """

    # Get the neuron
    neuron = circuit.cells.get(gid)

    # Translation
    translation = Vector((neuron['x'], neuron['y'], neuron['z']))

    # Orientation
    o = neuron['orientation']
    o0 = Vector((o[0][0], o[0][1], o[0][2]))
    o1 = Vector((o[1][0], o[1][1], o[1][2]))
    o2 = Vector((o[2][0], o[2][1], o[2][2]))

    # Initialize the transformation matrix to I
    transformation_matrix = Matrix()

    transformation_matrix[0][0] = o0[0]
    transformation_matrix[0][1] = o0[1]
    transformation_matrix[0][2] = o0[2]
    transformation_matrix[0][3] = translation[0]

    transformation_matrix[1][0] = o1[0]
    transformation_matrix[1][1] = o1[1]
    transformation_matrix[1][2] = o1[2]
    transformation_matrix[1][3] = translation[1]

    transformation_matrix[2][0] = o2[0]
    transformation_matrix[2][1] = o2[1]
    transformation_matrix[2][2] = o2[2]
    transformation_matrix[2][3] = translation[2]

    transformation_matrix[3][0] = 0.0
    transformation_matrix[3][1] = 0.0
    transformation_matrix[3][2] = 0.0
    transformation_matrix[3][3] = 1.0

    return transformation_matrix
