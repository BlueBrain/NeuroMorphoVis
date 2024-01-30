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
#pragma once

#include "Vertex.hpp"
#include "Triangle.hpp"
#include "Neighbour.hpp"
#include "NeighborPoint3.hpp"
#include "BMesh.hpp"
#include "EigenValue.hpp"
#include "EigenVector.hpp"
#include "Normal.hpp"

#ifdef PYBIND
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <pybind11/complex.h>
#endif

/**
 * @brief The OptimizationMesh class
 */
class OptimizationMesh
{
public:

    /**
     * @brief ~OptimizationMesh
     */
    ~OptimizationMesh();

    /**
     * @brief OptimizationMesh
     * @param nVertices
     * @param nFaces
     */
    OptimizationMesh(const size_t& nVertices, const size_t& nFaces);

    /**
     * @brief OptimizationMesh
     * @param vertices
     * @param triangles
     */
    OptimizationMesh(const BVertices& vertices, const BTriangles& triangles);

    /**
     * @brief smooth
     * @param maxMinAngle
     * @param minaMaxAngle
     * @param maximumIterations
     * @param preserveRidges
     * @param verbose
     * @return
     */
    bool smooth(const size_t& maxMinAngle,
                const size_t& minaMaxAngle,
                const size_t& maximumIterations,
                const bool& preserveRidges,
                const bool& verbose);

    /**
     * @brief smoothNormals
     * @param maxMinAngle
     * @param minMaxAngle
     * @param verbose
     */
    void smoothNormals(const float& maxMinAngle = 15,
                       const float& minMaxAngle = 150,
                       const bool& verbose = false);

    /**
     * @brief coarse
     * @param coarsenessRate
     * @param flatnessRate
     * @param densenessWeight
     * @param maxNormalAngle
     * @param verbose
     * @return
     */
    char coarse(float coarsenessRate,
                float flatnessRate, float densenessWeight,
                float maxNormalAngle,
                const bool &verbose);

    /**
     * @brief coarseDense
     * @param denseRate
     * @param iterations
     * @param verbose
     */
    void coarseDense(const float& denseRate, const size_t &iterations, const bool verbose);

    /**
     * @brief coarseFlat
     * @param flatnessRate
     * @param iterations
     * @param verbose
     */
    void coarseFlat(const float& flatnessRate, const size_t &iterations, const bool verbose);

    /**
     * @brief refine
     */
    void refine();

    /**
     * @brief getVertexPositionAlongSurface
     * @param x
     * @param y
     * @param z
     * @param a
     * @param b
     * @param c
     * @return
     */
    Vertex getVertexPositionAlongSurface(const float& x, const float& y, const float& z,
                                         const size_t& a, const size_t& b, const size_t& c);

    /**
     * @brief getAngleBetweenVertices
     * @param a
     * @param b
     * @param c
     * @return
     */
    float getAngleBetweenVertices(const size_t& a, const size_t& b, const size_t& c);

    /**
     * @brief getVertexNormal
     * @param n
     * @return
     */
    Normal getVertexNormal(const size_t& n);

    /**
     * @brief getEigenVector
     * @param vertexIndex
     * @param eigenValue
     * @param computedMaxAngle
     * @param verbose
     * @return
     */
    EigenVector getEigenVector(const size_t& vertexIndex, EigenValue* eigenValue,
                               float *computedMaxAngle, const bool &verbose = false);

    /**
     * @brief computeDotProduct
     * @param a
     * @param b
     * @param c
     * @return
     */
    float computeDotProduct(const size_t& a, const size_t& b, const size_t& c);

    /**
     * @brief computeCrossProduct
     * @param a
     * @param b
     * @param c
     * @return
     */
    Normal computeCrossProduct(const size_t& a, const size_t& b, const size_t& c);

    /**
     * @brief checkFlipAction
     * @param a
     * @param b
     * @param c
     * @param d
     * @param preserveRidges
     * @return
     */
    char checkFlipAction(const size_t& a, const size_t& b, const size_t& c, const size_t& d,
                         const bool& preserveRidges);

    /**
     * @brief getMinMaxAngles
     * @param computedMinangle
     * @param computedMaxangle
     * @param computedNumberSmallerAngles
     * @param computedNumberLargerAngles
     * @param maxMinAngle
     * @param minMaxAngle
     */
    void getMinMaxAngles(float *computedMinangle, float *computedMaxangle,
                         size_t *computedNumberSmallerAngles, size_t *computedNumberLargerAngles,
                         const float& maxMinAngle, const float& minMaxAngle);

    /**
     * @brief edgeFlipping
     * @param n
     * @param preserveRidges
     */
    void edgeFlipping(const size_t& n, const bool& preserveRidges);

    /**
     * @brief moveVerticesAlongSurface
     * @param n
     */
    void moveVerticesAlongSurface(const size_t& n);

    /**
     * @brief smoothNormal
     * @param n
     */
    void smoothNormal(const size_t& n);

    /**
     * @brief subdividePolygon
     * @param startNeighbour
     * @param faceAvailableList
     * @param faceAvailableIndex
     * @param faceMarker
     */
    void subdividePolygon(NPNT3 *startNeighbour, int *faceAvailableList,
                          int *faceAvailableIndex, int faceMarker);

    /**
     * @brief releaseOptimizationMeshData
     */
    void releaseOptimizationMeshData();

    /**
     * @brief destructOptimizationMesh
     */
    void destructOptimizationMesh();

    /**
     * @brief createNeighborlist
     */
    void createNeighborlist();

    /**
     * @brief destroyNeighborlist
     */
    void destroyNeighborlist();

    /**
     * @brief removeUnconnectedVertices
     */
    void removeUnconnectedVertices();

    /**
     * @brief deleteVertices
     */
    void deleteVertices();

    /**
     * @brief deleteFaces
     */
    void deleteFaces();

    /**
     * @brief translateMesh
     * @param dx
     * @param dy
     * @param dz
     */
    void translateMesh(const float& dx, const float& dy, const float& dz);

    /**
     * @brief scaleMesh
     * @param xScale
     * @param yScale
     * @param zScale
     */
    void scaleMesh(const float& xScale, const float& yScale, const float& zScale);

    /**
     * @brief scaleMeshUniformly
     * @param scaleFactor
     */
    void scaleMeshUniformly(const float& scaleFactor);

    /**
     * @brief optimizeUsingDefaultParameters
     */
    void optimizeUsingDefaultParameters();

    /**
     * @brief getVertices
     * @return
     */
    VertexPtr getVertices();



    /**
     * @brief getTriangles
     * @return
     */
    TrianglePtr getTriangles();

#ifdef PYBIND
    /**
     * @brief getVertexData
     * @return
     */
    pybind11::array_t< Vertex > getVertexData();

    /**
     * @brief getFaceData
     * @return
     */
    pybind11::array_t< Triangle > getFaceData();
#endif

public:

    /**
     * @brief numberVertices
     * Number of vertices
     */
    size_t numberVertices;

    /**
     * @brief numberFaces
     * Number of triangles
     */
    size_t numberFaces;

    /**
     * @brief averageLength
     * Average edge length
     */
    float averageLength;

    /**
     * @brief pMin
     * Minimal coordinate of nodes
     */
    Vertex pMin[3];

    /**
     * @brief pMax
     * Maximal coordinate of nodes
     */
    Vertex pMax[3];

    /**
     * @brief vertex
     * Pointer to the vertices
     */
    VertexPtr vertex;

    /**
     * @brief face
     * Pointer to the triangles
     */
    TrianglePtr face;

    /**
     * @brief neighbor
     * Pointer to the neighbors (triangles)
     */
    NeighbourPtr neighbor;

    /**
     * @brief neighborList
     * Pointer to the neighbor list
     */
    NeighborPoint3** neighborList;

    /**
     * @brief closed
     * A flag to indicate if the surface mesh is closed or not
     */
    bool closed;

    /**
     * @brief marker
     * A doman marker, to be used when tetrahedralizing
     */
    int marker;

    /**
     * @brief volumeConstraint
     * Volume constraint of the tetrahedralized domain
     */
    float volumeConstraint;

    /**
     * @brief useVolumeConstraint
     * A flag that determines if the volume constraint is used or not
     */
    bool useVolumeConstraint;

    /**
     * @brief asHole
     * A flag that determines if the mesh is a hole or not
     */
    bool asHole;
};

/**
 * @brief OptimizationMeshPtr
 */
typedef OptimizationMesh* OptimizationMeshPtr;

/**
 * @brief OptimizationMeshes
 */
typedef std::vector< OptimizationMesh > OptimizationMeshes;

/**
 * @brief OptimizationMeshesPtrs
 */
typedef std::vector< OptimizationMeshPtr > OptimizationMeshesPtrs;
