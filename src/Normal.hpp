/***************************************************************************************************
 * Copyright (c) 2023 - 2024 Marwan Abdellah < abdellah.marwan@gmail.com >
 * Copyright (C) 1994 - Michael Holst and Zeyun Yu
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

#pragma once

/**
 * @brief The Normal class
 */
class Normal
{
public:
    /**
     * @brief x
     */
    float x;

    /**
     * @brief y
     */
    float y;

    /**
     * @brief z
     */
    float z;
};

/**
 * @brief NormalPtr
 */
typedef Normal* NormalPtr;
