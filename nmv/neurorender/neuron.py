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
# @Neuron
####################################################################################################
class Neuron:
    """Neuron
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 gid,
                 mtype,
                 mlabel,
                 layer,
                 position,
                 orientation,
                 tag,
                 soma_min_radius,
                 soma_mean_radius,
                 soma_max_radius,
                 membrane_mesh,
                 membrane_material,
                 nucleus_mesh,
                 nucleus_material,
                 spines_mesh,
                 spines_material):
        """Constructor

        :param gid:
             Neuron GID.
        :param mtype:
            Neuron morphology type.
        :param mlabel:
            Neuron morphology label.
        :param layer:
            Neuron layer.
        :param position:
            Neuron position.
        :param orientation:
            Neuron Y orientation.
        :param tag:
            A tag for labeling the neuron.
        :param soma_min_radius:
            The minimum radius of the soma.
        :param soma_mean_radius:
            The mean radius of the soma.
        :param soma_max_radius:
            The maximum radius of the soma.
        :param membrane_mesh:
            Neuron membrane mesh.
        :param membrane_material:
            Neuron membrane mesh material.
        :param nucleus_mesh:
            Neuron nucleus mesh.
        :param nucleus_material:
            Neuron nucleus mesh material.
        :param spines_mesh:
            Neuron spine mesh.
        :param spines_material:
            Neuron spine mesh material.
        """

        # Neuron GID
        self.gid = gid

        # Neuron layer
        self.layer = layer

        # Neuron morphology type
        self.mtype = mtype

        # Neuron morphology label
        self.mlabel = mlabel

        # Neuron tag
        self.tag = tag

        # Neuron soma minimum radius
        self.soma_min_radius = soma_min_radius

        # Neuron soma mean radius
        self.soma_mean_radius = soma_mean_radius

        # Neuron soma maximum radius
        self.soma_max_radius = soma_max_radius

        # Neuron position
        self.position = position

        # Neuron Y orientation
        self.orientation = orientation

        # Neuron membrane surface mesh
        self.membrane_mesh = membrane_mesh

        # Neuron nucleus surface mesh
        self.nucleus_mesh = nucleus_mesh

        # Neuron spine mesh
        self.spines_mesh = spines_mesh

        # Neuron membrane material
        self.membrane_material = membrane_material

        # Neuron nucleus material
        self.nucleus_material = nucleus_material

        # Neuron spines material
        self.spines_material = spines_material

    ################################################################################################
    # @print_data
    ################################################################################################
    def print_data(self):
        """Prints the data of the neuron
        """
        print('* Neuron: \n')
        print('\t GID : [%s] ' % str(self.gid))
        print('\t Morphology type : [%s] ' % str(self.mtype))
        print('\t Morphology label : [%s] ' % str(self.mlabel))
        print('\t Position : [%s] ' % str(self.position))
        print('\t Orientation : [%s] ' % str(self.orientation))
        print('\t Tag : [%s] ' % str(self.tag))
        print('\t Soma minimum radius : [%s] ' % str(self.soma_min_radius))
        print('\t Soma mean radius : [%s] ' % str(self.soma_mean_radius))
        print('\t Soma maximum radius : [%s] ' % str(self.soma_max_radius))




