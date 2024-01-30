/***************************************************************************************************
 * Copyright (c) 2023-2024 - Marwan Abdellah < abdellah.marwan@gmail.com >
 * Copyright (c) 1994 - Michael Holst and Zeyun Yu
 *
 * This file is part of OMesh, the OptimizationMesh library.
 *
 * This library is free software; you can redistribute it and/or modify it under the terms of the
 * GNU General Public License version 3.0 as published by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * You should have received a copy of the GNU General Public License along with this library;
 * if not, write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
 * MA 02111-1307, USA.
 * You can also find it on the GNU web site < https://www.gnu.org/licenses/gpl-3.0.en.html >
 *
 * OMesh is based on the GAMer (Geometry-preserving Adaptive MeshER) library, which is
 * redistributable and is modifiable under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation as published by the Free Software
 * Foundation; either version 2.1 of the License, or any later version.
 **************************************************************************************************/
#include <vector>

#pragma once

/**
 * @brief The EigenVector class
 */
class EigenVector
{
public:
    /**
     * @brief x1
     * The x-coordinate of first eigenvector
     */
    float x1;
    /**
     * @brief y1
     * The y-coordinate of first eigenvector
     */
    float y1;

    /**
     * @brief z1
     * The z-coordinate of first eigenvector
     */
    float z1;

    /**
     * @brief x2
     * The x-coordinate of second eigenvector
     */
    float x2;

    /**
     * @brief y2
     * The y-coordinate of second eigenvector
     */
    float y2;

    /**
     * @brief z2
     * The z-coordinate of second eigenvector
     */
    float z2;

    /**
     * @brief x3
     * The x-coordinate of third eigenvector
     */
    float x3;

    /**
     * @brief y3
     * The y-coordinate of third eigenvector
     */
    float y3;

    /**
     * @brief z3
     * The z-coordinate of third eigenvector
     */
    float z3;
};

/**
 * @brief EigenVectorPtr
 */
typedef EigenVector* EigenVectorPtr;

/**
 * @brief EigenVectors
 */
typedef std::vector< EigenVector > EigenVectors;
