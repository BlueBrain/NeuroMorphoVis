#!/usr/bin/python

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

import sys

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
    
args = sys.argv
args = args.split(',')

r = float(args[1])
g = float(args[2])
b = float(args[3])

if r > 255: r = 255
if r < 0: r = 0 
if r < 1.0 and r > 0.0: r = r * 256

if g > 255: g = 255
if g < 0: g = 0 
if g < 1.0 and g > 0.0: g = g * 256

if b > 255: b = 255
if b < 0: r = 0 
if b < 1.0 and b > 0.0: b = b * 256

r = int(r)
g = int(g)
b = int(b)

print(rgb_to_hex((r, g, b)))
