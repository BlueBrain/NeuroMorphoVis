####################################################################################################
# Copyright (c) 2023 - 2024 Marwan Abdellah < abdellah.marwan@gmail.com >
#
# This file is part of OMesh, the OptimizationMesh library.
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

# This shell script installs omesh in place to be used directly by any python script. 
# Users need to use the correct version of Python. 

# Python executable
PYTHON_EXECUTABLE='python3.10'

###################################################################################
$PYTHON_EXECUTABLE setup.py build_ext install_lib install --prefix $PWD/../
###################################################################################