####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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


####################################################################################################
# @PolyLine
####################################################################################################
class PolyLine:
    """Poly-line object that consists of multiple points and a material
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 name='poly-line',
                 samples=None,
                 material_index=0):
        """Constructor.
        :param name:
            Poly-line name.
        :param samples:
            A given list of samples, by default empty or None.
        :param material_index:
            The index of the material linked to this poly-line if multiple materials are used in
            a multi-poly-line object.
        """

        # Name
        self.name = name

        # Samples
        self.samples = samples

        # Material index
        self.material_index = material_index
