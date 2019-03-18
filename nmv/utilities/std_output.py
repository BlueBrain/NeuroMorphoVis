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
import sys

std_hook = None


####################################################################################################
# @disable_std_output
####################################################################################################
def disable_std_output():
    """Ignore the output from Blender verbose functions to make the output more clear to read.
    """

    # Hooks the stdout until further notice
    global hook
    hook = sys.stdout
    sys.stdout = open('trash.output', 'w')


####################################################################################################
# @enable_std_output
####################################################################################################
def enable_std_output():
    """Re-enable stdout again.
    """

    global hook
    if hook is None:
        return
    else:
        sys.stdout = hook
