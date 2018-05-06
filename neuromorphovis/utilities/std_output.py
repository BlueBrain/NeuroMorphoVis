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

# System imports
import sys


####################################################################################################
# @disable_std_output
####################################################################################################
def disable_std_output():
    """Ignore the output from Blender verbose functions to make the output more clear to read.

    :return:
        A hook for stdout.
    """

    # Hooks the stdout until further notice
    hook = sys.stdout
    trash = open('trash.output', 'w')
    sys.stdout = trash
    return hook


####################################################################################################
# @enable_std_output
####################################################################################################
def enable_std_output(hook=None):
    """Re-enable stdout again.

    :param hook:
        A hook for std.
    """

    if hook is None:
        return
    else:
        sys.stdout = hook
