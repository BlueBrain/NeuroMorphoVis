####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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

# System imports
import sys
import tempfile

stdout_hook = None
stderr_hook = None


####################################################################################################
# @disable_std_output
####################################################################################################
def disable_std_output():
    """Ignore the output from Blender verbose functions to make the output more clear to read."""

    # Hooks the stdout until further notice
    global stdout_hook
    global stderr_hook

    stdout_hook = sys.stdout
    stderr_hook = sys.stderr

    temporary_directory = tempfile.gettempdir()

    sys.stdout = open('%s/nmv-stdout.output' % temporary_directory, 'w')
    sys.stderr = open('%s/nmv-stderr.output' % temporary_directory, 'w')


####################################################################################################
# @enable_std_output
####################################################################################################
def enable_std_output():
    """Re-enable stdout again."""

    global stdout_hook
    global stderr_hook

    if stdout_hook is None:
        return
    else:
        sys.stdout = stdout_hook
        sys.stderr = stderr_hook
