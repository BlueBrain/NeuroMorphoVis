####################################################################################################
# Copyright (c) 2023-2024 - Marwan Abdellah < abdellah.marwan@gmail.com >
# Copyright (c) 1994 - Michael Holst and Zeyun Yu
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
#
# OMesh is based on the GAMer (Geometry-preserving Adaptive MeshER) library, which is
# redistributable and is modifiable under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation as published by the Free Software
# Foundation; either version 2.1 of the License, or any later version.
####################################################################################################

# Minimum version is 3.1
cmake_minimum_required(VERSION 3.1...3.27)

# This is your project statement. You should always list languages;
# Listing the version is nice here since it sets lots of useful variables
project(omesh VERSION 0.1.0 LANGUAGES CXX)

# Release
set(CMAKE_BUILD_TYPE Release)

# Compilation flags
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} \
    -Wunused-variable \
    -Wsign-compare \
    -Wunused-but-set-variable \
    -Wunused-but-set-variable")

# Create the library from the source file
add_library(omesh
    src/Common.hh
    src/Vertex.hpp
    src/Triangle.hpp
    src/EigenVector.hpp
    src/Neighbour.hpp
    src/OptimizationMesh.cpp
    src/OptimizationMesh.hh
)
