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

# Blender imports
from mathutils import Vector, Matrix


####################################################################################################
# @get_neuron_translation_vector
####################################################################################################
def get_neuron_translation_vector(circuit,
                                  gid):

    # Translation
    neuron = circuit.cells.get(int(gid))
    return Vector((neuron['x'], neuron['y'], neuron['z']))


####################################################################################################
# @get_neuron_orientation_matrix
####################################################################################################
def get_neuron_orientation_matrix(circuit,
                                  gid):

    # Orientation
    neuron = circuit.cells.get(int(gid))
    o = neuron['orientation']
    o0 = Vector((o[0][0], o[0][1], o[0][2]))
    o1 = Vector((o[1][0], o[1][1], o[1][2]))
    o2 = Vector((o[2][0], o[2][1], o[2][2]))

    # Initialize the orientation matrix to I
    orientation_matrix = Matrix()

    orientation_matrix[0][0] = o0[0]
    orientation_matrix[0][1] = o0[1]
    orientation_matrix[0][2] = o0[2]
    orientation_matrix[0][3] = 1.0

    orientation_matrix[1][0] = o1[0]
    orientation_matrix[1][1] = o1[1]
    orientation_matrix[1][2] = o1[2]
    orientation_matrix[1][3] = 1.0

    orientation_matrix[2][0] = o2[0]
    orientation_matrix[2][1] = o2[1]
    orientation_matrix[2][2] = o2[2]
    orientation_matrix[2][3] = 1.0

    orientation_matrix[3][0] = 0.0
    orientation_matrix[3][1] = 0.0
    orientation_matrix[3][2] = 0.0
    orientation_matrix[3][3] = 1.0

    return orientation_matrix


####################################################################################################
# @get_neuron_transformation_matrix
####################################################################################################
def get_neuron_transformation_matrix(circuit,
                                     gid):
    """Get the transformation matrix of a neuron identified by a GID.
    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :return:
        The transformation matrix of the neuron in Blender format.
    """

    # Translation
    translation_vector = get_neuron_translation_vector(circuit=circuit, gid=gid)

    # Get the orientation and update the translation elements in the orientation matrix
    matrix = get_neuron_orientation_matrix(circuit=circuit, gid=gid)
    matrix[0][3] = translation_vector[0]
    matrix[1][3] = translation_vector[1]
    matrix[2][3] = translation_vector[2]

    return matrix


####################################################################################################
# @get_neuron_inverse_transformation_matrix
####################################################################################################
def get_neuron_inverse_transformation_matrix(circuit,
                                             gid):
    """Get the inverse transformation matrix of a neuron identified by a GID.
    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :return:
        The transformation matrix of the neuron in Blender format.
    """

    return get_neuron_transformation_matrix(circuit=circuit, gid=gid).inverted()
