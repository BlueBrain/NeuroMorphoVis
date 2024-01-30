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

#include "OptimizationMesh.hh"
#include "BMesh.hpp"
#include "Timer.hpp"
#include "Common.hh"

OptimizationMesh::OptimizationMesh(const size_t& nVertices, const size_t& nFaces)
{
    printf(LIB_STRING "Creating an OMesh [%ld Vertices, %ld Triangles]\n", nVertices, nFaces);

    // Update the vertices
    numberVertices = nVertices;
    if (numberVertices > 0)
        vertex = new Vertex[numberVertices];
    else
        vertex = nullptr;

    // Update the triangular faces
    numberFaces = nFaces;
    if (numberFaces > 0)
        face = new Triangle[numberFaces];
    else
        face = nullptr;

    // Neighbours
    neighbor = nullptr;
    neighborList = nullptr;
    averageLength = 0.f;

    // Bounds
    pMin->x = 0.f; pMin->y = 0.f; pMin->z = 0.f;
    pMax->x = 0.f; pMax->y = 0.f; pMax->z = 0.f;

    // Initialize OptimizationMesh structures
    if (numberVertices > 0)
    {
#pragma omp parallel for
        for (size_t i = 0; i < numberVertices; ++i)
        {
            vertex[i].x = vertex[i].y = vertex[i].z = vertex[i].marker = 0;
            vertex[i].selected = true;
        }
    }

    if (numberFaces > 0)
    {
#pragma omp parallel for
        for (size_t i = 0; i < numberFaces; ++i)
        {
            face[i].v1 = face[i].v2 = face[i].v3 = face[i].marker = 0;
            face[i].selected = true;
        }
    }

    // Initialize domain data
    closed = true;
    marker = 1;
    volumeConstraint = 100;
    useVolumeConstraint = false;
    asHole = false;
}

OptimizationMesh::OptimizationMesh(const BVertices& vertices, const BTriangles& triangles)
{
    printf(LIB_STRING "Creating an OMesh [%ld Vertices, %ld Triangles]\n",
           vertices.size(),  triangles.size());

    TIMER_SET;

    // Update the vertices
    numberVertices = vertices.size();
    if (numberVertices > 0)
        vertex = new Vertex[numberVertices];
    else
        vertex = nullptr;

    // Update the triangular faces
    numberFaces = triangles.size();
    if (numberFaces > 0)
        face = new Triangle[numberFaces];
    else
        face = nullptr;

    // Neighbours
    neighbor = nullptr;
    neighborList = nullptr;
    averageLength = 0.f;

    // Bounds
    pMin->x = 0.f; pMin->y = 0.f; pMin->z = 0.f;
    pMax->x = 0.f; pMax->y = 0.f; pMax->z = 0.f;

    // Fill the vertices
    if (numberVertices > 0)
    {
#pragma omp parallel for
        for (size_t i = 0; i < vertices.size(); ++i)
        {
            vertex[i].x = vertices[i][0];
            vertex[i].y = vertices[i][1];
            vertex[i].z = vertices[i][2];
            vertex[i].selected = true;
        }
    }

    // Fill the faces
    if (numberFaces > 0)
    {
#pragma omp parallel for
    for (size_t i = 0; i < triangles.size(); ++i)
    {
        face[i].v1 =  triangles[i][0];
        face[i].v2 =  triangles[i][1];
        face[i].v3 =  triangles[i][2];
        face[i].selected = true;
    }
    }

    // Initialize domain data
    closed = true;
    marker = 1;
    volumeConstraint = 100;
    useVolumeConstraint = false;
    asHole = false;
    printf(LIB_STRING "STATS: OMesh Creation [%f Seconds] \n", GET_TIME_SECONDS);
}

OptimizationMesh::~OptimizationMesh()
{
    // Relase data memory
    releaseOptimizationMeshData();
}

void OptimizationMesh::releaseOptimizationMeshData()
{
    // Free allocated memory
    if (vertex)
    {
        delete [] vertex;
        printf(LIB_STRING "Releasing Vertices\n");
    }

    if (face)
    {
        delete [] face;
        printf(LIB_STRING "Releasing Faces\n");
    }

    // Destroy neighbourList
    destroyNeighborlist();

    printf(LIB_STRING "Data Released ... \n");
}

void OptimizationMesh::removeUnconnectedVertices()
{
    // Collect statistics
    size_t numberRemovedVertices = 0;

    std::vector< size_t > verticesToRemove(numberVertices);

#pragma omp parallel for
    for (size_t n = 0; n < numberVertices; ++n)
    {
        if (vertex[n].marker < 0)
        {
            numberRemovedVertices++;
        }

        verticesToRemove[n] = numberRemovedVertices;
    }

    printf(LIB_STRING "Removing [%ld] Vertices.\n", numberRemovedVertices);

    // Move vertices forward
#pragma omp parallel for
    for (size_t n = 0; n < numberVertices; ++n)
    {
        // If a vertex is to be removed
        if ((n == 0 && verticesToRemove[n] != 0) ||
                (n != 0 && verticesToRemove[n-1] != verticesToRemove[n]))
            continue;

        // Move vertices forward
        vertex[n - verticesToRemove[n]].x = vertex[n].x;
        vertex[n - verticesToRemove[n]].y = vertex[n].y;
        vertex[n - verticesToRemove[n]].z = vertex[n].z;
        vertex[n - verticesToRemove[n]].selected = vertex[n].selected;
        vertex[n - verticesToRemove[n]].marker = vertex[n].marker;
    }

    // Fix face offset
#pragma omp parallel for
    for (size_t n = 0; n < numberFaces; ++n)
    {
        face[n].v1 = face[n].v1 - verticesToRemove[face[n].v1];
        face[n].v2 = face[n].v2 - verticesToRemove[face[n].v2];
        face[n].v3 = face[n].v3 - verticesToRemove[face[n].v3];
    }

    // Adjust num_vertices
    numberVertices -= numberRemovedVertices;
}

// OptimizationMesh_createNeighborlist
void OptimizationMesh::createNeighborlist()
{
    // Destroy any exsisting neighborlist
    destroyNeighborlist();

    // Create an array of NeighborPoint3Ptr used to store
    // TODO: Use new
    NeighborPoint3Ptr* neighbourList = (NeighborPoint3Ptr*) malloc(
                sizeof(NeighborPoint3Ptr) * numberVertices);

    // Initialize the neighbor list
#pragma omp parallel for
    for (size_t n = 0; n < numberVertices; ++n)
    {
        neighbourList[n] = nullptr;

        // By default, mark all vertices for deletion
        vertex[n].marker = -1;
    }

    // Iterate over the faces and collect line segments (a, b) and its connection to a face (c).
    // Save the line segment so it forms a counter clockwise triangle with the origin vertex
    NPNT3 *firstNeighbour;
    NPNT3 *secondNeighbour;
    NPNT3 *auxiliaryNeighbour;
    // NPNT3 *lastNeighbour;

    size_t numberConnected = 0;
    for (size_t n = 0; n < numberFaces; ++n)
    {
        size_t a = face[n].v1;
        size_t b = face[n].v2;
        size_t c = face[n].v3;

        if (a == b || b == c || a == c)
        {
            printf("Face  %ld include vertices with same indices (%ld, %ld, %ld).\n", n, a, b, c);
        }

        firstNeighbour = (NPNT3*)malloc(sizeof(NPNT3));
        firstNeighbour->a = b;
        firstNeighbour->b = c;
        firstNeighbour->c = n;
        firstNeighbour->next = neighbourList[a];
        neighbourList[a] = firstNeighbour;

        // Mark vertex as connected
        if (vertex[a].marker < 0)
        {
            vertex[a].marker = 0;
            numberConnected += 1;
        }

        firstNeighbour = (NPNT3*) malloc(sizeof(NPNT3));
        firstNeighbour->a = c;
        firstNeighbour->b = a;
        firstNeighbour->c = n;
        firstNeighbour->next = neighbourList[b];
        neighbourList[b] = firstNeighbour;

        // Mark vertex as connected
        if (vertex[b].marker < 0)
        {
            vertex[b].marker = 0;
            numberConnected += 1;
        }

        firstNeighbour = (NPNT3*) malloc(sizeof(NPNT3));
        firstNeighbour->a = a;
        firstNeighbour->b = b;
        firstNeighbour->c = n;
        firstNeighbour->next = neighbourList[c];
        neighbourList[c] = firstNeighbour;

        // Mark vertex as connected
        if (vertex[c].marker < 0)
        {
            vertex[c].marker = 0;
            numberConnected += 1;
        }

    }

    // Check if there are vertices which are not connect to any face
    if (numberConnected < numberVertices)
    {
        // Attach the neighborlist to the surfaceMesh and destroy it
        neighborList = neighbourList;
        destroyNeighborlist();

        // Remove unconnected vertices
        removeUnconnectedVertices();

        // Re-create neighbors
        createNeighborlist();

        return;
    }

    // Order the neighbors so they are connected counter clockwise
    for (size_t n = 0; n < numberVertices; ++n)
    {
        int a0 = -1;
        int b0 = -1;

        firstNeighbour = neighbourList[n];

        int c = firstNeighbour->a;
        // int d = firstNeighbour->b;

        while (firstNeighbour != nullptr)
        {
            int a = firstNeighbour->a;
            int b = firstNeighbour->b;

            secondNeighbour = firstNeighbour->next;
            while (secondNeighbour != nullptr)
            {
                a0 = secondNeighbour->a;
                b0 = secondNeighbour->b;
                if (a0 == b && b0 != a)
                {
                    auxiliaryNeighbour = firstNeighbour;
                    while (auxiliaryNeighbour != nullptr)
                    {
                        if (auxiliaryNeighbour->next == secondNeighbour)
                        {
                            auxiliaryNeighbour->next = secondNeighbour->next;
                            break;
                        }
                        auxiliaryNeighbour = auxiliaryNeighbour->next;
                    }
                    auxiliaryNeighbour = firstNeighbour->next;
                    firstNeighbour->next = secondNeighbour;
                    secondNeighbour->next = auxiliaryNeighbour;
                    break;
                }

                secondNeighbour = secondNeighbour->next;

            }

            firstNeighbour = firstNeighbour->next;

        }

        // Check that the neighbor list is connected
        auxiliaryNeighbour = neighbourList[n];

        bool closed = true;
        while (auxiliaryNeighbour->next != nullptr)
        {
            // Check that we are connected
            if (auxiliaryNeighbour->b != auxiliaryNeighbour->next->a)
            {
                if (closed)
                {
                    printf("Polygons connected to vertex %ld are not closed (interupted):"
                           " (%.2f, %.2f, %.2f)\n", n, vertex[n].x, vertex[n].y, vertex[n].z);
                }

                // Do not bail, just register the vertex to not be done anything with
                vertex[n].selected = false;

                closed = false;
            }

            // Step one face forward
            auxiliaryNeighbour = auxiliaryNeighbour->next;
        }

        // Check if the list forms a closed ring
        if (closed && b0 != c)
        {
            printf("Polygons connected to vertex %ld are not closed (not closed):"
                   " (%.2f, %.2f, %.2f)\n", n, vertex[n].x, vertex[n].y, vertex[n].z);

            // Do not bail, just register the vertex to not be done anything with
            vertex[n].selected = false;

            closed = false;
        }

        if (!closed)
        {
            closed = false;
        }
    }

    // Attach the neighborlist to the surfaceMesh
    neighborList = neighbourList;
}

void OptimizationMesh::destroyNeighborlist()
{
    NeighborPoint3Ptr firstNeighbour = nullptr;
    NeighborPoint3Ptr auxiliaryNeighbour = nullptr;

    // The neighbor list must exist before deleting it
    if (neighborList != nullptr)
    {
        // Release the single neighbors
// #pragma omp parallel for
        for (size_t i = 0; i < numberVertices; ++i)
        {
            firstNeighbour = neighborList[i];
            while (firstNeighbour != nullptr)
            {
                auxiliaryNeighbour = firstNeighbour->next;
                free(firstNeighbour);
                firstNeighbour = auxiliaryNeighbour;
            }
        }

        // Free the array of pointers
        free(neighborList);
        neighborList = nullptr;
    }
}

void OptimizationMesh::deleteFaces()
{
    // Iterate over vertices and mark all for deletion
#pragma omp parallel for
    for (size_t n = 0; n < numberVertices; ++n)
    {
        vertex[n].marker = -1;
    }

    // Delete faces connected to vertices
    int numberRemovedFaces = 0;
    for (size_t n = 0; n < numberFaces; ++n)
    {
        // Check for removal of face
        if (face[n].marker < 0)
            numberRemovedFaces += 1;
        else
        {
            // If any previous face has been marked for deletion
            if (numberRemovedFaces > 0)
            {
                // Copy the face to a previous face
                face[n - numberRemovedFaces].v1 = face[n].v1;
                face[n - numberRemovedFaces].v2 = face[n].v2;
                face[n - numberRemovedFaces].v3 = face[n].v3;
                face[n - numberRemovedFaces].marker = face[n].marker;
                face[n - numberRemovedFaces].selected = face[n].selected;
            }

            // Un mark vertex for deletion
            vertex[face[n].v1].marker = 0;
            vertex[face[n].v2].marker = 0;
            vertex[face[n].v3].marker = 0;
        }
    }

    // Update the number of faces
    numberFaces -= numberRemovedFaces;
    removeUnconnectedVertices();
}

void OptimizationMesh::deleteVertices()
{
    // Mark faces connected to vertices for deletion
#pragma omp parallel for
    for (size_t n = 0; n < numberFaces; ++n)
    {
        if (vertex[face[n].v1].marker < 0 ||
            vertex[face[n].v2].marker < 0 ||
            vertex[face[n].v3].marker < 0 )
        {
            face[n].marker = -1;
        }
    }

    // Delete marked faces
    deleteFaces();
}


Vertex OptimizationMesh::getVertexPositionAlongSurface(const float& x, const float& y, const float& z,
                                                  const size_t& a, const size_t& b, const size_t& c)
{
    float ax = vertex[a].x;
    float ay = vertex[a].y;
    float az = vertex[a].z;

    float bx = vertex[b].x;
    float by = vertex[b].y;
    float bz = vertex[b].z;

    float cx = vertex[c].x;
    float cy = vertex[c].y;
    float cz = vertex[c].z;

    bx -= ax; by -= ay; bz -= az;
    float distance = std::sqrt(bx * bx + by * by + bz * bz);
    if (distance > 0) { bx /= distance; by /= distance; bz /= distance; }

    cx -= ax; cy -= ay; cz -= az;
    distance = std::sqrt(cx * cx +cy * cy + cz * cz);
    if (distance > 0) { cx /= distance; cy /= distance; cz /= distance; }

    float tx = 0.5 * (cx + bx);
    float ty = 0.5 * (cy + by);
    float tz = 0.5 * (cz + bz);
    distance = sqrt(tx * tx + ty * ty + tz * tz);
    if (distance > 0) { tx /= distance; ty /= distance; tz /= distance; }

    float xx = by * cz - bz * cy;
    float yy = bz * cx - bx * cz;
    float zz = bx * cy - by *cx;
    distance = sqrt(xx * xx + yy * yy + zz * zz);
    if (distance > 0) { xx /= distance; yy /= distance; zz /= distance; }

    bx = xx; by = yy; bz = zz;
    distance = tx * (x - ax) + ty * (y - ay) + tz * (z - az);

    xx = distance * tx + ax;
    yy = distance * ty + ay;
    zz = distance * tz + az;
    distance = bx * (x - xx) + by * (y - yy) + bz * (z - zz);

    // Return the new vertex
    Vertex newVertex;
    newVertex.x = distance * bx + xx;
    newVertex.y = distance * by + yy;
    newVertex.z = distance * bz + zz;
    return newVertex;
}

float OptimizationMesh::getAngleBetweenVertices(const size_t& a, const size_t& b, const size_t& c)
{
    float ax = vertex[a].x;
    float ay = vertex[a].y;
    float az = vertex[a].z;

    float bx = vertex[b].x;
    float by = vertex[b].y;
    float bz = vertex[b].z;

    float cx = vertex[c].x;
    float cy = vertex[c].y;
    float cz = vertex[c].z;

    float length1 = (ax - bx) * (ax - bx) + (ay - by) * (ay - by) + (az - bz) * (az - bz);
    float length2 = (ax - cx) * (ax - cx) + (ay - cy) * (ay - cy) + (az - cz) * (az - cz);
    float length3 = (bx - cx) * (bx - cx) + (by - cy) * (by - cy) + (bz - cz) * (bz - cz);

    float angle;
    if (length1 == 0 || length2 == 0) { angle = -999; }
    else
    {
        angle = 0.5 * (length1 + length2 - length3) / std::sqrt(length1 * length2);
        angle = std::acos(angle) * 180.0 / PIE;
    }

    return angle;
}

Normal OptimizationMesh::getVertexNormal(const size_t& n)
{
    float x = vertex[n].x;
    float y = vertex[n].y;
    float z = vertex[n].z;

    Normal normal; normal.x = 0; normal.y = 0; normal.z = 0;
    NPNT3 **neighbourList = neighborList;
    NPNT3 *firstNeighbour = neighbourList[n];
    int numberIterations = 0;
    while (firstNeighbour != nullptr)
    {
        int a = firstNeighbour->a;
        int b = firstNeighbour->b;

        float ax = vertex[a].x - x;
        float ay = vertex[a].y - y;
        float az = vertex[a].z - z;
        float length = std::sqrt(ax * ax + ay * ay + az * az);
        if (length > 0) { ax /= length; ay /= length; az /= length; }

        float bx = vertex[b].x - x;
        float by = vertex[b].y - y;
        float bz = vertex[b].z - z;
        length = std::sqrt(bx * bx + by * by + bz * bz);
        if (length > 0) { bx /= length; by /= length; bz /= length; }

        float gx = ay * bz - az * by;
        float gy = az * bx - ax * bz;
        float gz = ax * by - ay * bx;
        length = std::sqrt(gx * gx + gy * gy + gz * gz);
        if (length > 0) { gx /= length; gy /= length; gz /= length; }

        length = normal.x * gx + normal.y * gy + normal.z * gz;
        if (length < 0) { gx = -gx; gy = -gy; gz = -gz; }

        normal.x += gx;
        normal.y += gy;
        normal.z += gz;

        numberIterations++;
        firstNeighbour = firstNeighbour->next;
    }

    if (numberIterations > 0)
    {
        normal.x /= (float)numberIterations;
        normal.y /= (float)numberIterations;
        normal.z /= (float)numberIterations;

        float length = std::sqrt(normal.x * normal.x + normal.y * normal.y + normal.z * normal.z);
        if (length > 0) { normal.x /= length; normal.y /= length; normal.z /= length; }
    }
    else { normal.x = 0; normal.y = 0; normal.z = 0; }

    return normal;
}

EigenVector OptimizationMesh::getEigenVector(const size_t& vertexIndex, EigenValue* eigenValue,
                                        float *computedMaxAngle, const bool &verbose)
{
    Normal vertexNormal = getVertexNormal(vertexIndex);
    if (verbose)
    {
        printf(LIB_STRING "\tNormal@ [%ld]: (%.2f, %.2f, %.2f)\n",
               vertexIndex, vertexNormal.x, vertexNormal.y, vertexNormal.z);
    }

    double A[3][3];
    A[0][0] = vertexNormal.x * vertexNormal.x;
    A[0][1] = vertexNormal.x * vertexNormal.y;
    A[0][2] = vertexNormal.x * vertexNormal.z;
    A[1][1] = vertexNormal.y * vertexNormal.y;
    A[1][2] = vertexNormal.y * vertexNormal.z;
    A[2][2] = vertexNormal.z * vertexNormal.z;

    size_t startPointer = 0;
    size_t endPointer = 1;
    size_t indexArray[333];
    size_t distArray[333];
    indexArray[startPointer] = vertexIndex;
    distArray[startPointer] = 0;

    float maxAngle = 99999.0;

    Normal currentNormal;
    currentNormal.x = vertexNormal.x;
    currentNormal.y = vertexNormal.y;
    currentNormal.z = vertexNormal.z;

    NPNT3 **neighbourList = neighborList;
    NPNT3 *firstNeighbour;

    int visited;
    while (startPointer < endPointer)
    {
        size_t index = indexArray[startPointer];
        size_t dist = distArray[startPointer];
        startPointer ++;

        if (dist < ((DIM_SCALE > 2) ? (3):(2)))
        {
            firstNeighbour = neighbourList[index];
            while (firstNeighbour != nullptr)
            {
                size_t m = firstNeighbour->a;
                visited = 0;
                for (size_t n = 0; n < endPointer; ++n)
                {
                    if (indexArray[n] == m)
                    {
                        visited = 1;
                        break;
                    }
                }

                if (visited == 0)
                {
                    vertexNormal = getVertexNormal(m);

                    float angle = currentNormal.x * vertexNormal.x +
                                  currentNormal.y * vertexNormal.y +
                                  currentNormal.z * vertexNormal.z;

                    if (angle < 0)
                        angle = -angle;

                    if (angle < maxAngle)
                        maxAngle = angle;

                    A[0][0] += vertexNormal.x * vertexNormal.x;
                    A[0][1] += vertexNormal.x * vertexNormal.y;
                    A[0][2] += vertexNormal.x * vertexNormal.z;
                    A[1][1] += vertexNormal.y * vertexNormal.y;
                    A[1][2] += vertexNormal.y * vertexNormal.z;
                    A[2][2] += vertexNormal.z * vertexNormal.z;

                    indexArray[endPointer] = m;
                    distArray[endPointer] = dist + 1;
                    endPointer++;
                }

                firstNeighbour = firstNeighbour->next;
            }
        }
    }

    // Update the maximum angle
    *computedMaxAngle = maxAngle;

    A[1][0] = A[0][1];
    A[2][0] = A[0][2];
    A[2][1] = A[1][2];

    double c0 = A[0][0] * A[1][1] * A[2][2] +
            2 * A[0][1] * A[0][2 ]* A[1][2] -
                A[0][0] * A[1][2] * A[1][2] -
                A[1][1] * A[0][2] * A[0][2] -
                A[2][2] * A[0][1] * A[0][1];

    double c1 = A[0][0] * A[1][1] - A[0][1] * A[0][1] + A[0][0] * A[2][2]-
                A[0][2] * A[0][2] + A[1][1] * A[2][2] - A[1][2] * A[1][2];
    double c2 = A[0][0] + A[1][1] + A[2][2];

    double a = (3.0 * c1 - c2 * c2) / 3.0;
    double b = (-2.0 * c2 * c2 * c2 + 9.0 * c1 * c2-27.0 * c0) / 27.0;
    double q = b * b / 4.0 + a * a * a / 27.0;

    double theta = std::atan2(sqrt(-q), -0.5 * b);
    double p = std::sqrt(0.25 * b * b - q);

    double x1 = c2 / 3.0 + 2.0 *
            std::pow(p, 1.0 / 3.0) * std::cos(theta / 3.0);
    double x2 = c2 / 3.0 - std::pow(p, 1.0 / 3.0) *
            (std::cos(theta / 3.0) + std::sqrt(3.0) * std::sin(theta / 3.0));
    double x3 = c2 / 3.0 - std::pow(p, 1.0 / 3.0) *
            (std::cos(theta / 3.0) - std::sqrt(3.0) * std::sin(theta / 3.0));

    EigenVector auxiliaryEigenVector;

    // If we have a perfect flat area inline of one of the x, y, z axis
    if (std::isnan(x1) || std::isnan(x2) || std::isnan(x3))
    {
        // printf(LIB_STRING "@getEigenVector: nan@ [%ld]\n", vertexIndex);

        eigenValue->x = c2;
        eigenValue->y = 0;
        eigenValue->z = 0;

        auxiliaryEigenVector.x1 = 1;
        auxiliaryEigenVector.y1 = 0;
        auxiliaryEigenVector.z1 = 0;

        auxiliaryEigenVector.x2 = 0;
        auxiliaryEigenVector.y2 = 1;
        auxiliaryEigenVector.z2 = 0;

        auxiliaryEigenVector.x3 = 0;
        auxiliaryEigenVector.y3 = 0;
        auxiliaryEigenVector.z3 = 1;

        return auxiliaryEigenVector;
    }

    double tx = std::max(x1, std::max(x2, x3));
    double ty = 0, tz = 0;
    if (tx == x1)
    {
        if (x2 >= x3) { ty = x2; tz = x3; }
        else { ty = x3; tz = x2; }
    }
    else if (tx == x2)
    {
        if (x1 >= x3) { ty = x1; tz = x3; }
        else { ty = x3; tz = x1; }
    }
    else if (tx == x3)
    {
        if (x1 >= x2) { ty = x1; tz = x2; }
        else { ty = x2; tz = x1; }
    }

    x1 = tx; x2 = ty; x3 = tz;

    eigenValue->x = tx;
    eigenValue->y = ty;
    eigenValue->z = tz;

    if (x1 > 99999 || x1 < -99999 || x2 > 99999 || x2 < -99999 || x3 > 99999 || x3 < -99999)
    {
        printf(LIB_STRING "\tERROR @getEigenVector: [%f %f %f]\n", x1, x2, x3);
    }

    A[0][0] -= x1;
    A[1][1] -= x1;
    A[2][2] -= x1;

    double B[6];
    B[0] = A[1][1] * A[2][2] - A[1][2] * A[1][2];
    B[1] = A[0][2] * A[1][2] - A[0][1] * A[2][2];
    B[2] = A[0][0] * A[2][2] - A[0][2] * A[0][2];
    B[3] = A[0][1] * A[1][2] - A[0][2] * A[1][1];
    B[4] = A[0][1] * A[0][2] - A[1][2] * A[0][0];
    B[5] = A[0][0] * A[1][1] - A[0][1] * A[0][1];

    c0 = B[0] * B[0] + B[1] * B[1] + B[3] * B[3];
    c1 = B[1] * B[1] + B[2] * B[2] + B[4] * B[4];
    c2 = B[3] * B[3] + B[4] * B[4] + B[5] * B[5];

    if (c0 >= c1 && c0 >= c2)
    {
        tx = B[0]; ty = B[1]; tz = B[3];
    }
    else if (c1 >= c0 && c1 >= c2)
    {
        tx = B[1]; ty = B[2]; tz = B[4];
    }
    else if (c2 >= c0 && c2 >= c1)
    {
        tx = B[3]; ty = B[4]; tz = B[5];
    }

    p = std::sqrt(tx * tx + ty * ty + tz * tz);
    if (p > 0) { tx /= p; ty /= p; tz /= p; }

    auxiliaryEigenVector.x1 = tx;
    auxiliaryEigenVector.y1 = ty;
    auxiliaryEigenVector.z1 = tz;

    A[0][0] += x1;
    A[1][1] += x1;
    A[2][2] += x1;

    A[0][0] -= x2;
    A[1][1] -= x2;
    A[2][2] -= x2;

    B[0] = A[1][1] * A[2][2] - A[1][2] * A[1][2];
    B[1] = A[0][2] * A[1][2] - A[0][1] * A[2][2];
    B[2] = A[0][0] * A[2][2] - A[0][2] * A[0][2];
    B[3] = A[0][1] * A[1][2] - A[0][2] * A[1][1];
    B[4] = A[0][1] * A[0][2] - A[1][2] * A[0][0];
    B[5] = A[0][0] * A[1][1] - A[0][1] * A[0][1];

    c0 = B[0] * B[0]+ B[1] * B[1] + B[3] * B[3];
    c1 = B[1] * B[1]+ B[2] * B[2] + B[4] * B[4];
    c2 = B[3] * B[3]+ B[4] * B[4] + B[5] * B[5];
    if (c0 >= c1 && c0 >= c2)
    {
        tx = B[0]; ty = B[1]; tz = B[3];
    }
    else if (c1 >= c0 && c1 >= c2)
    {
        tx = B[1]; ty = B[2]; tz = B[4];
    }
    else if (c2 >= c0 && c2 >= c1)
    {
        tx = B[3]; ty = B[4]; tz = B[5];
    }
    p = std::sqrt(tx * tx + ty * ty + tz * tz);
    if (p > 0) { tx /= p; ty /= p; tz /= p; }

    auxiliaryEigenVector.x2 = tx;
    auxiliaryEigenVector.y2 = ty;
    auxiliaryEigenVector.z2 = tz;

    auxiliaryEigenVector.x3 = auxiliaryEigenVector.y1 * tz-auxiliaryEigenVector.z1 * ty;
    auxiliaryEigenVector.y3 = auxiliaryEigenVector.z1 * tx-auxiliaryEigenVector.x1 * tz;
    auxiliaryEigenVector.z3 = auxiliaryEigenVector.x1 * ty-auxiliaryEigenVector.y1 * tx;

    return auxiliaryEigenVector;
}

float OptimizationMesh::computeDotProduct(const size_t& a, const size_t& b, const size_t& c)
{
    float bx = vertex[b].x - vertex[a].x;
    float by = vertex[b].y - vertex[a].y;
    float bz = vertex[b].z - vertex[a].z;
    float length = std::sqrt(bx * bx + by * by + bz * bz);
    if (length > 0) { bx /= length; by /= length; bz /= length; }

    float cx = vertex[c].x - vertex[a].x;
    float cy = vertex[c].y - vertex[a].y;
    float cz = vertex[c].z - vertex[a].z;
    length = std::sqrt(cx * cx + cy * cy + cz * cz);
    if (length > 0) { cx /= length; cy /= length; cz /= length; }

    length = bx * cx + by * cy + bz * cz;
    return length;
}

Normal OptimizationMesh::computeCrossProduct(const size_t& a, const size_t& b, const size_t& c)
{
    float bx = vertex[b].x - vertex[a].x;
    float by = vertex[b].y - vertex[a].y;
    float bz = vertex[b].z - vertex[a].z;
    float length = sqrt(bx * bx + by * by + bz * bz);
    if (length > 0) { bx /= length; by /= length; bz /= length; }

    float cx = vertex[c].x - vertex[a].x;
    float cy = vertex[c].y - vertex[a].y;
    float cz = vertex[c].z - vertex[a].z;
    length = sqrt(cx * cx + cy * cy + cz * cz);
    if (length > 0) { cx /= length; cy /= length; cz /= length; }

    float gx = cy * bz - cz * by;
    float gy = cz * bx - cx * bz;
    float gz = cx * by - cy * bx;
    length = sqrt(gx * gx + gy * gy + gz * gz);
    if (length > 0) { gx /= length; gy /= length; gz /= length; }

    Normal value; value.x = gx; value.y = gy; value.z = gz;
    return value;
}

Normal rotate(const float& sx, const float& sy, const float& sz,
              const float& theta, const float& phi, const float& angle)
{
    float a[3][3], b[3][3];
    a[0][0] = (float)(std::cos(0.5 * PIE - phi) * std::cos(theta));
    a[0][1] = (float)(std::cos(0.5 * PIE - phi) * std::sin(theta));
    a[0][2] = (float)-std::sin(0.5 * PIE - phi);
    a[1][0] = (float)-std::sin(theta);
    a[1][1] = (float) std::cos(theta);
    a[1][2] = 0.f;
    a[2][0] = (float)(std::sin(0.5 * PIE - phi) * std::cos(theta));
    a[2][1] = (float)(std::sin(0.5 * PIE - phi) * std::sin(theta));
    a[2][2] = (float) std::cos(0.5 * PIE - phi);

    b[0][0] = (float)(std::cos(0.5 * PIE - phi) * std::cos(theta));
    b[0][1] = (float)-std::sin(theta);
    b[0][2] = (float)(std::sin(0.5 * PIE - phi) * std::cos(theta));
    b[1][0] = (float)(std::cos(0.5 * PIE - phi) * std::sin(theta));
    b[1][1] = (float)std::cos(theta);
    b[1][2] = (float)(std::sin(0.5 * PIE - phi) * std::sin(theta));
    b[2][0] = (float)-std::sin(0.5 * PIE - phi);
    b[2][1] = 0.f;
    b[2][2] = (float) std::cos(0.5 * PIE - phi);

    float x = a[0][0] * sx + a[0][1] * sy + a[0][2] * sz;
    float y = a[1][0] * sx + a[1][1] * sy + a[1][2] * sz;
    float z = a[2][0] * sx + a[2][1] * sy + a[2][2] * sz;

    float xx = (float)(std::cos(angle) * x - std::sin(angle) * y);
    float yy = (float)(std::sin(angle) * x + std::cos(angle) * y);
    float zz = z;

    Normal rotationVector;
    rotationVector.x = b[0][0] * xx + b[0][1] * yy + b[0][2] * zz;
    rotationVector.y = b[1][0] * xx + b[1][1] * yy + b[1][2] * zz;
    rotationVector.z = b[2][0] * xx + b[2][1] * yy + b[2][2] * zz;
    return rotationVector;
}

char OptimizationMesh::checkFlipAction(
        const size_t& a, const size_t& b, const size_t& c, const size_t& d,
        const bool& preserveRidges)
{
    // NPNT3 **neighbourList = neighborList;

    /// Smaller angle criterion
    float minAngle1 = -99999;
    float angle = computeDotProduct(a, b, c);
    if (angle > minAngle1)
        minAngle1 = angle;
    angle = computeDotProduct(a, b, d);
    if (angle > minAngle1)
        minAngle1 = angle;
    angle = computeDotProduct(b, a, c);
    if (angle > minAngle1)
        minAngle1 = angle;
    angle = computeDotProduct(b, a, d);
    if (angle > minAngle1)
        minAngle1 = angle;

    float minAngle2 = -99999;
    angle = computeDotProduct(c, a, d);
    if (angle > minAngle2)
        minAngle2 = angle;
    angle = computeDotProduct(c, b, d);
    if (angle > minAngle2)
        minAngle2 = angle;
    angle = computeDotProduct(d, a, c);
    if (angle > minAngle2)
        minAngle2 = angle;
    angle = computeDotProduct(d, b, c);
    if (angle > minAngle2)
        minAngle2 = angle;

    // Check which of the triangle combination has the smallest angle
    // minAngle1 is the minimal angle of the flipped configuration
    // minAngle2 is the minimal angle of the present configuration
    if (minAngle1 > minAngle2)
    {
        // Check if the angle between the normals of the two triangles are too small for a flip
        // action, for example if we are on a ridge
        Normal normal1 = computeCrossProduct(a, c, b);
        Normal normal2 = computeCrossProduct(a, b, d);

        // If we want to preserve the ridges the angle between the surface normals must be smaller
        // than cos(60deg) to flip the edges
        if (not preserveRidges ||
                normal1.x * normal2.x + normal1.y * normal2.y + normal1.z * normal2.z > 0.866)
            return 1;
    }

    return 0;
}

void OptimizationMesh::getMinMaxAngles(float *computedMinangle, float *computedMaxangle,
                     size_t *computedNumberSmallerAngles, size_t *computedNumberLargerAngles,
                     const float& maxMinAngle, const float& minMaxAngle)
{
    float minAngle = 99999.0;
    float maxAngle = -99999.0;

    size_t numberSmallerAngles = 0;
    size_t numberLargerAngles = 0;

    for (size_t n = 0; n < numberFaces; n++)
    {
        size_t a = face[n].v1;
        size_t b = face[n].v2;
        size_t c = face[n].v3;

        float angle = getAngleBetweenVertices(a, b, c);
        if (angle != -999)
        {
            if (angle < minAngle)
                minAngle = angle;

            if (angle > maxAngle)
                maxAngle = angle;

            if (angle < maxMinAngle)
                numberSmallerAngles++;

            if (angle > minMaxAngle)
                numberLargerAngles++;
        }

        angle = getAngleBetweenVertices(b, a, c);
        if (angle != -999)
        {
            if (angle < minAngle)
                minAngle = angle;

            if (angle > maxAngle)
                maxAngle = angle;

            if (angle < maxMinAngle)
                numberSmallerAngles++;

            if (angle > minMaxAngle)
                numberLargerAngles++;
        }

        angle = getAngleBetweenVertices(c, a, b);
        if (angle != -999)
        {
            if (angle < minAngle)
                minAngle = angle;

            if (angle > maxAngle)
                maxAngle = angle;

            if (angle < maxMinAngle)
                numberSmallerAngles++;

            if (angle > minMaxAngle)
                numberLargerAngles++;
        }
    }

    *computedMinangle = minAngle;
    *computedMaxangle = maxAngle;
    *computedNumberSmallerAngles = numberSmallerAngles;
    *computedNumberLargerAngles = numberLargerAngles;
}

void OptimizationMesh::edgeFlipping(const size_t& n, const bool& preserveRidges)
{
    int a, b, c;
    int f1, f2;
    char flipFlag, flipCheck;

    NPNT3 **neighbourList = neighborList;
    NPNT3 *firstNeighbour = neighbourList[n];
    NPNT3 *auxNeighbour1, *auxNeighbour2;
    NPNT3 *secondNeighbour;
    size_t numberIterations;
    while (firstNeighbour != nullptr)
    {
        numberIterations = 0;
        NPNT3* auxNeighbour = neighbourList[n];
        while (auxNeighbour != nullptr)
        {
            numberIterations++;
            auxNeighbour = auxNeighbour->next;
        }

        if (numberIterations <= 3)
        {
            if (numberIterations > 0)
            {
                float ax = 0;
                float ay = 0;
                float az = 0;

                auxNeighbour = neighbourList[n];

                while (auxNeighbour != nullptr)
                {
                    a = auxNeighbour->a;
                    ax += vertex[a].x;
                    ay += vertex[a].y;
                    az += vertex[a].z;
                    auxNeighbour = auxNeighbour->next;
                }

                vertex[n].x = ax / (float) numberIterations;
                vertex[n].y = ay / (float) numberIterations;
                vertex[n].z = az / (float) numberIterations;
            }
            return;
        }

        a = firstNeighbour->a;
        b = firstNeighbour->b;

        secondNeighbour = firstNeighbour->next;
        if (secondNeighbour == nullptr)
            secondNeighbour = neighbourList[n];

        c = secondNeighbour->b;

        flipFlag = 1;
        numberIterations = 0;
        auxNeighbour = neighbourList[b];
        while (auxNeighbour != nullptr)
        {
            numberIterations++;
            auxNeighbour = auxNeighbour->next;
        }

        if (numberIterations <= 3)
            flipFlag = 0;

        auxNeighbour = neighbourList[a];
        while (auxNeighbour != nullptr)
        {
            if (auxNeighbour->a == c)
                flipFlag = 0;
            auxNeighbour = auxNeighbour->next;
        }

        auxNeighbour = neighbourList[c];
        while (auxNeighbour != nullptr)
        {
            if (auxNeighbour->a == a)
                flipFlag = 0;
            auxNeighbour = auxNeighbour->next;
        }

        if (flipFlag)
        {
            flipCheck = checkFlipAction(n, b, a, c, preserveRidges);
            if (flipCheck)
            {
                f1 = firstNeighbour->c;
                f2 = secondNeighbour->c;

                // Update face info
                face[f1].v1 = n;
                face[f1].v2 = a;
                face[f1].v3 = c;
                face[f2].v1 = b;
                face[f2].v2 = c; // Switch a and c to make the face normal outwards
                face[f2].v3 = a; // Switch a and c to make the face normal outwards

                // Delete the entries in neighbor lists
                firstNeighbour->b = c;
                if (firstNeighbour->next == nullptr)
                    neighbourList[n] = neighbourList[n]->next;
                else
                    firstNeighbour->next = secondNeighbour->next;
                auxNeighbour1 = secondNeighbour;

                auxNeighbour = neighbourList[b];
                while (auxNeighbour != nullptr)
                {
                    if (auxNeighbour->b == static_cast< int >(n))
                        break;
                    auxNeighbour = auxNeighbour->next;
                }

                if (auxNeighbour == nullptr)
                {
                    printf(LIB_STRING "\tERROR @edgeFlipping @ [%ld]\n", n);
                }

                if (auxNeighbour->a == c)
                {
                    auxNeighbour->b = a;
                    auxNeighbour->c = f2;

                    if (auxNeighbour->next == nullptr)
                    {
                        secondNeighbour = neighbourList[b];
                        neighbourList[b] = secondNeighbour->next;
                    }
                    else
                    {
                        secondNeighbour = auxNeighbour->next;
                        auxNeighbour->next = secondNeighbour->next;
                    }
                    auxNeighbour2 = secondNeighbour;
                }
                else
                {
                    printf(LIB_STRING "\tERROR @edgeFlipping [%ld : %d %d %d]\n", n, a, b, c);
                    printf(LIB_STRING "[%f, %f, %f]\n", vertex[n].x, vertex[n].y, vertex[n].z);
                }

                // Add the entries in neighbor lists
                auxNeighbour = neighbourList[a];
                while (auxNeighbour != nullptr)
                {
                    const int nInt = static_cast< int >(n);
                    if ((auxNeighbour->a == nInt && auxNeighbour->b == b) ||
                        (auxNeighbour->a == b && auxNeighbour->b == nInt))
                        break;

                    auxNeighbour = auxNeighbour->next;
                }

                // Assume neigbors are stored counter clockwise
                if (auxNeighbour->a == b && auxNeighbour->b == static_cast< int >(n))
                {
                    auxNeighbour->b = c;
                    auxNeighbour->c = f2;
                    auxNeighbour1->a = c;
                    auxNeighbour1->b = n;
                    auxNeighbour1->c = f1;
                    auxNeighbour1->next = auxNeighbour->next;
                    auxNeighbour->next = auxNeighbour1;
                }
                else
                {
                    printf(LIB_STRING "\tERROR @edgeFlipping: auxNeighbour->a == b && auxNeighbour->b == n\n");
                }

                auxNeighbour = neighbourList[c];
                while (auxNeighbour != nullptr)
                {
                    const int nInt = static_cast< int >(n);
                    if ((auxNeighbour->a == nInt && auxNeighbour->b == b) ||
                            (auxNeighbour->a == b && auxNeighbour->b == nInt))
                        break;
                    auxNeighbour = auxNeighbour->next;
                }

                // Assume neigbors are stored counter clockwise
                const int nInt = static_cast< int >(n);
                if (auxNeighbour->a == nInt && auxNeighbour->b == b)
                {
                    auxNeighbour->b = a;
                    auxNeighbour->c = f1;
                    auxNeighbour2->a = a;
                    auxNeighbour2->b = b;
                    auxNeighbour2->c = f2;
                    auxNeighbour2->next = auxNeighbour->next;
                    auxNeighbour->next = auxNeighbour2;
                }
                else
                {
                    printf(LIB_STRING "\tERROR @edgeFlipping: auxNeighbour->a == n && auxNeighbour->b == b\n");
                }
            }
        }

        firstNeighbour = firstNeighbour->next;
    }
}

void OptimizationMesh::moveVerticesAlongSurface(const size_t& n)
{
    float x = vertex[n].x;
    float y = vertex[n].y;
    float z = vertex[n].z;

    float nx = 0;
    float ny = 0;
    float nz = 0;

    float weight = 0;
    NPNT3 **neighbourList = neighborList;
    NPNT3 *firstNeighbour = neighbourList[n];
    while (firstNeighbour != nullptr)
    {
        int a = firstNeighbour->a;
        int b = firstNeighbour->b;

        NPNT3* secondNeighbour = firstNeighbour->next;
        if (secondNeighbour == nullptr)
            secondNeighbour = neighbourList[n];

        int c = secondNeighbour->b;
        Vertex newVertexPosition = getVertexPositionAlongSurface(x, y, z, b, a, c);
        float angle = computeDotProduct(b, a, c);
        angle += 1.0;
        nx += angle * newVertexPosition.x;
        ny += angle * newVertexPosition.y;
        nz += angle * newVertexPosition.z;

        weight += angle;
        firstNeighbour = firstNeighbour->next;
    }

    if (weight > 0)
    {
        nx /= weight; ny /= weight; nz /= weight;

        EigenValue eigenValue;
        float maxAngle;
        EigenVector eigenVector = getEigenVector(n, &eigenValue, &maxAngle);

        if ((eigenVector.x1 == 0 && eigenVector.y1 == 0 && eigenVector.z1 == 0) ||
            (eigenVector.x2 == 0 && eigenVector.y2 == 0 && eigenVector.z2 == 0) ||
            (eigenVector.x3 == 0 && eigenVector.y3 == 0 && eigenVector.z3 == 0))
        {
            // printf(LIB_STRING "@moveVerticesAlongSurface: "
            //        "Old point [%0.2f, %0.2f, %0.2f] New point [%0.2f, %0.2f, %0.2f]\n",
            //        vertex[n].x, vertex[n].y, vertex[n].z,
            //        nx, ny, nz);

            vertex[n].x = nx;
            vertex[n].y = ny;
            vertex[n].z = nz;
        }
        else
        {
            nx -= x; ny -= y; nz -= z;

            float w1 = (nx * eigenVector.x1 + ny * eigenVector.y1 + nz * eigenVector.z1) /
                    ( 1.0 + eigenValue.x);
            float w2 = (nx * eigenVector.x2 + ny * eigenVector.y2 + nz * eigenVector.z2) /
                    ( 1.0 + eigenValue.y);
            float w3 = (nx * eigenVector.x3 + ny * eigenVector.y3 + nz * eigenVector.z3) /
                    ( 1.0 + eigenValue.z);

            nx = w1 * eigenVector.x1 + w2 * eigenVector.x2 + w3 * eigenVector.x3 + x;
            ny = w1 * eigenVector.y1 + w2 * eigenVector.y2 + w3 * eigenVector.y3 + y;
            nz = w1 * eigenVector.z1 + w2 * eigenVector.z2 + w3 * eigenVector.z3 + z;

            // printf(LIB_STRING "@moveVerticesAlongSurface: "
            //        "Old point [%0.2f, %0.2f, %0.2f] New point [%0.2f, %0.2f, %0.2f]\n",
            //        vertex[n].x, vertex[n].y, vertex[n].z,
            //        nx, ny, nz);

            vertex[n].x = nx;
            vertex[n].y = ny;
            vertex[n].z = nz;
        }
    }
}

void OptimizationMesh::smoothNormal(const size_t& n)
{
    TIMER_SET;

    int numberIterations = 0;
    float xPos = 0; float yPos = 0; float zPos = 0;
    NPNT3** neighbourList = neighborList;
    NPNT3* firstNeighbour = neighbourList[n];
    while (firstNeighbour != nullptr)
    {
        int a = firstNeighbour->a;
        int b = firstNeighbour->b;

        NPNT3* secondNeighbour = firstNeighbour->next;

        if (secondNeighbour == nullptr)
            secondNeighbour = neighbourList[n];

        int c = secondNeighbour->b;

        NPNT3* thirdNeighbour = secondNeighbour->next;
        if (thirdNeighbour == nullptr)
            thirdNeighbour = neighbourList[n];

        int d = thirdNeighbour->b;

        NPNT3* auxNeighbour = neighbourList[b];

        // If a vertex is neigbor with a non selected vertex continue
        if (!vertex[b].selected)
            return;

        while (auxNeighbour != nullptr)
        {
            const int nInt = static_cast< int >(n);

            if ((auxNeighbour->a == c && auxNeighbour->b != nInt) ||
                (auxNeighbour->b == c && auxNeighbour->a != nInt))
                break;
            auxNeighbour = auxNeighbour->next;
        }

        int e;
        if (auxNeighbour->a == c && auxNeighbour->b != static_cast< int >(n))
        {
            e = auxNeighbour->b;
        }
        else if (auxNeighbour->b == c && auxNeighbour->a != static_cast< int >(n))
        {
            e = auxNeighbour->a;
        }
        else
        {
            printf(LIB_STRING "\tERROR @smoothNormal: auxNeighbour\n");
        }

        Normal normal = computeCrossProduct(n, b, c);
        float gx = normal.x; float gy = normal.y; float gz = normal.z;
        float dx = 0; float dy = 0; float dz = 0;

        size_t num = 0;
        normal = computeCrossProduct(n, a, b);
        float length = normal.x * gx + normal.y * gy + normal.z * gz;
        if (length > 0)
        {
            num++;
            dx += length * normal.x;
            dy += length * normal.y;
            dz += length * normal.z;
        }
        normal = computeCrossProduct(n, c, d);
        length = normal.x * gx + normal.y * gy + normal.z * gz;
        if (length > 0)
        {
            num++;
            dx += length * normal.x;
            dy += length * normal.y;
            dz += length * normal.z;
        }
        normal = computeCrossProduct(b, e, c);
        length = normal.x * gx+normal.y * gy + normal.z * gz;
        if (length > 0)
        {
            num++;
            dx += length * normal.x;
            dy += length * normal.y;
            dz += length * normal.z;
        }

        length = std::sqrt(dx * dx + dy * dy + dz * dz);
        if (length > 0)
        {
            dx /= length; dy /= length; dz /= length;

            float fx = gy * dz - gz * dy;
            float fy = gz * dx - gx * dz;
            float fz = gx * dy - gy * dx;

            float cx = vertex[c].x;
            float cy = vertex[c].y;
            float cz = vertex[c].z;

            float bx = vertex[b].x;
            float by = vertex[b].y;
            float bz = vertex[b].z;

            length = fx * (bx - cx) + fy * (by - cy) + fz * (bz-cz);
            float theta, phi;
            if (length >= 0)
            {
                theta = (float) std::atan2(by - cy, bx - cx);
                phi = (float) std::atan2(bz - cz,
                                         std::sqrt((bx - cx) * (bx - cx) + (by - cy) * (by - cy)));
            }
            else
            {
                theta = (float) std::atan2(cy - by, cx - bx);
                phi = (float) std::atan2(cz - bz,
                                         std::sqrt((bx - cx) * (bx - cx) + (by - cy) * (by - cy)));
            }

            float alpha = std::acos(dx * gx + dy * gy + dz * gz) / (float)(4.0 - num);
            Normal rotatedNormal = rotate(vertex[n].x - cx,
                                          vertex[n].y - cy,
                                          vertex[n].z - cz, theta, phi, alpha);

            xPos += rotatedNormal.x + cx;
            yPos += rotatedNormal.y + cy;
            zPos += rotatedNormal.z + cz;

            numberIterations++;
        }

        firstNeighbour = firstNeighbour->next;
    }

    if (numberIterations > 0 && !std::isnan(xPos) && !std::isnan(yPos) && !std::isnan(zPos))
    {
        vertex[n].x = xPos / (float) numberIterations;
        vertex[n].y = yPos / (float) numberIterations;
        vertex[n].z = zPos / (float) numberIterations;
    }
}

void OptimizationMesh::subdividePolygon(NPNT3 *startNeighbour, int *faceAvailableList,
                      int *faceAvailableIndex, int faceMarker)
{
    int numberIterations = 1;
    NPNT3 **neighbourList = neighborList;
    NPNT3 *auxNeighbour = startNeighbour;
    while (auxNeighbour->next != startNeighbour)
    {
        numberIterations++;
        auxNeighbour = auxNeighbour->next;
    }

    if (numberIterations < 3)
    {
        printf(LIB_STRING "ERROR @subdividePolygon: Number of nodes less than 3!\n");
        return;
    }

    NPNT3 *firstNeighbour, *secondNeighbour;
    NPNT3 *firstCopyNeighbour, *secondCopyNeighbour;
    if (numberIterations == 3)
    {
        int a = startNeighbour->a;
        auxNeighbour = startNeighbour->next;
        free(startNeighbour);
        startNeighbour = auxNeighbour;

        int b = startNeighbour->a;
        auxNeighbour = startNeighbour->next;
        free(startNeighbour);
        startNeighbour = auxNeighbour;

        int c = startNeighbour->a;
        auxNeighbour = startNeighbour->next;
        free(startNeighbour);
        startNeighbour = auxNeighbour;

        int faceIndex = faceAvailableList[*faceAvailableIndex];
        face[faceIndex].v1 = a;
        face[faceIndex].v2 = b;
        face[faceIndex].v3 = c;
        face[faceIndex].marker = faceMarker;
        *faceAvailableIndex += 1;

        firstNeighbour = (NPNT3 *)malloc(sizeof(NPNT3));
        firstNeighbour->a = b;
        firstNeighbour->b = c;
        firstNeighbour->c = faceIndex;
        firstNeighbour->next = neighbourList[a];
        neighbourList[a] = firstNeighbour;

        firstNeighbour = (NPNT3 *)malloc(sizeof(NPNT3));
        firstNeighbour->a = c;
        firstNeighbour->b = a;
        firstNeighbour->c = faceIndex;
        firstNeighbour->next = neighbourList[b];
        neighbourList[b] = firstNeighbour;

        firstNeighbour = (NPNT3 *)malloc(sizeof(NPNT3));
        firstNeighbour->a = a;
        firstNeighbour->b = b;
        firstNeighbour->c = faceIndex;
        firstNeighbour->next = neighbourList[c];
        neighbourList[c] = firstNeighbour;
    }
    else
    {
        auxNeighbour = startNeighbour;
        int minNumber = auxNeighbour->b;
        firstNeighbour = auxNeighbour;
        auxNeighbour = auxNeighbour->next;
        while (auxNeighbour != startNeighbour)
        {
            int degree = auxNeighbour->b;
            if (degree < minNumber)
            {
                minNumber = degree;
                firstNeighbour = auxNeighbour;
            }
            auxNeighbour = auxNeighbour->next;
        }

        minNumber = 99999;
        auxNeighbour = startNeighbour;
        if (auxNeighbour != firstNeighbour &&
            auxNeighbour != firstNeighbour->next &&
            auxNeighbour->next != firstNeighbour)
        {
            minNumber = auxNeighbour->b;
            secondNeighbour = auxNeighbour;
        }

        auxNeighbour = auxNeighbour->next;
        while (auxNeighbour != startNeighbour)
        {
            int degree = auxNeighbour->b;
            if (auxNeighbour != firstNeighbour &&
                auxNeighbour != firstNeighbour->next &&
                auxNeighbour->next != firstNeighbour &&
                degree < minNumber)
            {
                minNumber = degree;
                secondNeighbour = auxNeighbour;
            }

            auxNeighbour = auxNeighbour->next;
        }

        firstNeighbour->b += 1;
        secondNeighbour->b += 1;

        firstCopyNeighbour = (NPNT3 *)malloc(sizeof(NPNT3));
        firstCopyNeighbour->a = firstNeighbour->a;
        firstCopyNeighbour->b = firstNeighbour->b;

        secondCopyNeighbour = (NPNT3 *)malloc(sizeof(NPNT3));
        secondCopyNeighbour->a = secondNeighbour->a;
        secondCopyNeighbour->b = secondNeighbour->b;
        auxNeighbour = firstNeighbour;

        while (auxNeighbour->next != firstNeighbour)
            auxNeighbour = auxNeighbour->next;

        auxNeighbour->next = firstCopyNeighbour;
        firstCopyNeighbour->next = secondCopyNeighbour;
        secondCopyNeighbour->next = secondNeighbour->next;
        secondNeighbour->next = firstNeighbour;

        subdividePolygon(firstNeighbour, faceAvailableList,
                         faceAvailableIndex, faceMarker);
        subdividePolygon(firstCopyNeighbour, faceAvailableList,
                         faceAvailableIndex, faceMarker);
    }
}

bool OptimizationMesh::smooth(const size_t& maxMinAngle, const size_t& minaMaxAngle,
                              const size_t& maximumIterations, const bool& preserveRidges,
                              const bool& verbose)
{
    TIMER_SET;

    // Check if neighbour list is created, otherwise create it
    if (!neighborList)
        createNeighborlist();

    // If it is still not created, then some polygons are not closed
    if (neighborList == nullptr)
    {
        printf(LIB_STRING "ERROR @smooth: Could not create neigbor list. "
               "Some polygons might not be closed. Operation not done!\n");
        return 0;
    }

    // Compute the distribution of the angles
    float minAngle, maxAngle;
    size_t numberSmallerAngles, numberLargerAngles;
    getMinMaxAngles(&minAngle, &maxAngle, &numberSmallerAngles, &numberLargerAngles,
                    maxMinAngle, minaMaxAngle);

    // Print the initial quality only when doing 1 or more iterations
    size_t i = 0;
    if (verbose && maximumIterations > 1)
    {
        printf(LIB_STRING "Angles:\n");
        printf(LIB_STRING "%3ld: Min θ, Max θ [%.5f, %.5f] "
               "θ < %ld, θ > %ld [%ld, %ld]\t\n",
               i, minAngle, maxAngle,
               maxMinAngle, minaMaxAngle,
               numberSmallerAngles, numberLargerAngles);
        fflush(stdout);
    }

    // Check if the mesh is smoothed or not
    bool smoothed = minAngle > maxMinAngle && maxAngle < minaMaxAngle;
    while (!smoothed && i < maximumIterations)
    {
        i++;

        // Smooth all vertices
        for (size_t n = 0; n < numberVertices; ++n)
        {
            // If we have a vertex wich is not selected we continue
            if (!vertex[n].selected)
                continue;

            // Move the vertex along the surface of the mesh
            moveVerticesAlongSurface(n);

            // Flip the edge
            edgeFlipping(n, preserveRidges);
        }

        // Calculate and print quality after surface smooth
        getMinMaxAngles(&minAngle, &maxAngle, &numberSmallerAngles,
                        &numberLargerAngles, maxMinAngle, minaMaxAngle);

        // Print the iteration number only when doing 1 or more iterations
        if (maximumIterations != 1 && verbose)
        {
            printf(LIB_STRING "%3ld: Min θ, Max θ [%.5f, %.5f] "
                   "θ < %ld, θ > %ld [%ld, %ld]\t\n",
                   i, minAngle, maxAngle,
                   maxMinAngle, minaMaxAngle,
                   numberSmallerAngles, numberLargerAngles);
            fflush(stdout);
        }
        else
        {
            if (verbose)
            {
                printf(LIB_STRING "%3ld: Min θ, Max θ [%.5f, %.5f] "
                       "θ < %ld, θ > %ld [%ld, %ld]\t\r",
                       i, minAngle, maxAngle,
                       maxMinAngle, minaMaxAngle,
                       numberSmallerAngles, numberLargerAngles);
                fflush(stdout);
            }
        }

        // Check if the mesh is smoothed or not
        smoothed = minAngle > maxMinAngle && maxAngle < minaMaxAngle;
    }
    printf(LIB_STRING "STATS: Surface Smoothing [%f Seconds] \n", GET_TIME_SECONDS);

    return smoothed;
}

void OptimizationMesh::smoothNormals(const float& maxMinAngle, const float& minMaxAngle,
                   const bool &verbose)
{
     TIMER_SET;

    // Check if neighbour list is created, otherwise create it
    if (!neighborList)
        createNeighborlist();

    // If it is still not created, then some polygons are not closed
    if (neighborList == nullptr)
    {
        printf("ERROR @smoothNormals: Could not create neigbor list. "
               "Some polygons might not be closed. Operation not done!\n");
        return;
    }

    // Normal smooth all vertices
    for (size_t n = 0; n < numberVertices; ++n)
    {
        // The vertex must be selected to smooth its normal
        if (!vertex[n].selected) { continue; }

        // Smooth the normal of the vertex
        smoothNormal(n);
    }

    // Compute the angles
    float minAngle, maxAngle;
    size_t numberSmallerAngles, numberGreaterAngles;
    getMinMaxAngles(&minAngle, &maxAngle, &numberSmallerAngles, &numberGreaterAngles,
                    maxMinAngle, minMaxAngle);

    if (verbose)
    {
        printf(LIB_STRING "Min θ, Max θ [%.5f, %.5f] "
               "θ < %f, θ > %f [%ld, %ld]\t\n",
               minAngle, maxAngle,
               maxMinAngle, minMaxAngle,
               numberSmallerAngles, numberGreaterAngles);
    }
    printf(LIB_STRING "STATS: Normal Smoothing [%f Seconds] \n", GET_TIME_SECONDS);
}

void OptimizationMesh::refine()
{
    TIMER_SET;

    size_t local_vertices[3], local_additional_vertices[3];

    NPNT3* ngr;
    float ax, ay, az;
    float nx, ny, nz;

    // Check if neighborlist is created, otherwise create it
    if (neighborList == nullptr)
        createNeighborlist();

    NPNT3** neighbourList = neighborList;

    // Store the number of vertices in the original mesh
    size_t initialNumberVertices = numberVertices;

    // Create an array with the number of edges associated with each vertex
    size_t* numberEdges = (size_t*) malloc(sizeof(size_t) * initialNumberVertices);

    // Create an array with the offsets into the vertex2edge array for each vertex
    size_t* offsets = (size_t*) malloc(sizeof(size_t) * initialNumberVertices);

    // Iterate over all vertices and collect edges
    size_t totalNumberEdges = 0;
    size_t localNumberEdges = 0;
    for (size_t n = 0; n < initialNumberVertices; ++n)
    {
        offsets[n] = totalNumberEdges;
        localNumberEdges = 0;

        ngr = neighbourList[n];
        while (ngr != nullptr)
        {
            // If n is smaller than ngr->a we have an edge
            if (int(n) < ngr->a)
            {
                totalNumberEdges++;
                localNumberEdges++;
            }
            ngr = ngr->next;
        }
        numberEdges[n] = localNumberEdges;
    }

    // Create memory for the refined mesh
    OptimizationMesh* refinedOptimizationMesh = new OptimizationMesh(initialNumberVertices + totalNumberEdges,
                                           numberFaces * 4);
    refinedOptimizationMesh->numberVertices = initialNumberVertices;
    refinedOptimizationMesh->numberFaces = numberFaces;

    // Copy the original mesh to the new mesh
    for (size_t n = 0; n < initialNumberVertices; ++n)
    {
        refinedOptimizationMesh->vertex[n].x = vertex[n].x;
        refinedOptimizationMesh->vertex[n].y = vertex[n].y;
        refinedOptimizationMesh->vertex[n].z = vertex[n].z;
    }

    for (size_t n = 0; n < numberFaces; ++n)
    {
        refinedOptimizationMesh->face[n].v1 = face[n].v1;
        refinedOptimizationMesh->face[n].v2 = face[n].v2;
        refinedOptimizationMesh->face[n].v3 = face[n].v3;
    }

    // Create the map from vertices to edges
    size_t* vertex2edge = (size_t*) malloc(sizeof(size_t) * totalNumberEdges);

    // Iterate over all vertices and split edges
    size_t edgeNumber = 0;
    for (size_t n = 0; n < initialNumberVertices; ++n)
    {
        // Get the coordinates of vertex n
        nx = refinedOptimizationMesh->vertex[n].x;
        ny = refinedOptimizationMesh->vertex[n].y;
        nz = refinedOptimizationMesh->vertex[n].z;

        ngr = neighbourList[n];
        while (ngr != nullptr)
        {
            // If n is smaller than ngr->a we have an edge
            if (int(n) < ngr->a)
            {
                // Add the value of the opposite vertex to the map
                vertex2edge[edgeNumber] = ngr->a;

                // Get the coordinates of vertex ngr->a
                ax = refinedOptimizationMesh->vertex[ngr->a].x;
                ay = refinedOptimizationMesh->vertex[ngr->a].y;
                az = refinedOptimizationMesh->vertex[ngr->a].z;

                // Add the new vertex coordinates of the splitted edge
                refinedOptimizationMesh->vertex[initialNumberVertices + edgeNumber].x = 0.5*(ax + nx);
                refinedOptimizationMesh->vertex[initialNumberVertices + edgeNumber].y = 0.5*(ay + ny);
                refinedOptimizationMesh->vertex[initialNumberVertices + edgeNumber].z = 0.5*(az + nz);

                // Increase the edge number
                edgeNumber++;
            }
            ngr = ngr->next;
        }
    }

    // A counter for adding new faces
    size_t faceNumber = refinedOptimizationMesh->numberFaces;

    // Iterate over faces and add information of the refined face
    for (size_t n = 0; n < refinedOptimizationMesh->numberFaces; ++n)
    {
        local_vertices[0] = refinedOptimizationMesh->face[n].v1;
        local_vertices[1] = refinedOptimizationMesh->face[n].v2;
        local_vertices[2] = refinedOptimizationMesh->face[n].v3;

        // Iterate over the vertices and find the edges
        for (size_t m = 0; m < 3; ++m)
        {
            size_t min_vertex_num = std::min(local_vertices[m], local_vertices[(m + 1) % 3]);
            size_t max_vertex_num = std::max(local_vertices[m], local_vertices[(m + 1) % 3]);

            // Find the edge number that fit the pair of vertices
            size_t k = 0;
            for (k = 0; k < numberEdges[min_vertex_num]; ++k)
                if (vertex2edge[offsets[min_vertex_num] + k] == max_vertex_num)
                    break;

            // The edge number represents the number of the added vertex plus the
            // number of original vertices
            local_additional_vertices[m] = initialNumberVertices + offsets[min_vertex_num] + k;

        }

        // Add information of the four new faces

        // First the mid face
        refinedOptimizationMesh->face[n].v1 = local_additional_vertices[0];
        refinedOptimizationMesh->face[n].v2 = local_additional_vertices[1];
        refinedOptimizationMesh->face[n].v3 = local_additional_vertices[2];

        // Then the three corner faces
        for (size_t m = 0; m < 3; m++)
        {
            refinedOptimizationMesh->face[faceNumber].v1 = local_vertices[m];
            refinedOptimizationMesh->face[faceNumber].v2 = local_additional_vertices[m];
            refinedOptimizationMesh->face[faceNumber].v3 = local_additional_vertices[(m + 2) % 3];
            faceNumber++;
        }
    }

    // Release memory
    free(numberEdges);
    free(offsets);
    free(vertex2edge);

    // Update number information
    refinedOptimizationMesh->numberVertices += totalNumberEdges;
    refinedOptimizationMesh->numberFaces *= 4;

    // Release old data
    releaseOptimizationMeshData();

    // Assign the refined mesh to the passed
    numberVertices = refinedOptimizationMesh->numberVertices;
    numberFaces = refinedOptimizationMesh->numberFaces;
    vertex = refinedOptimizationMesh->vertex;
    face = refinedOptimizationMesh->face;

    // Free memory of refined surface mesh struct
    delete refinedOptimizationMesh;

    // Recreate the neigborlist
    createNeighborlist();
    printf(LIB_STRING "STATS: Surface Refine [%f Seconds] \n", GET_TIME_SECONDS);
}

void OptimizationMesh::translateMesh(const float& dx, const float& dy, const float& dz)
{
#pragma omp parallel for
    for (size_t i = 0; i < numberVertices; ++i)
    {
        vertex[i].x += dx;
        vertex[i].y += dy;
        vertex[i].z += dz;
    }
}

void OptimizationMesh::scaleMesh(const float& xScale, const float& yScale, const float& zScale)
{
#pragma omp parallel for
    for (size_t i = 0; i < numberVertices; ++i)
    {
        vertex[i].x *= xScale;
        vertex[i].y *= yScale;
        vertex[i].z *= zScale;
    }
}

void OptimizationMesh::scaleMeshUniformly(const float& scaleFactor)
{
    scaleMesh(scaleFactor, scaleFactor, scaleFactor);
}

void OptimizationMesh::optimizeUsingDefaultParameters()
{
    coarseFlat(0.05, 5, true);
    smooth(15, 150, 15, false, true);
}

char OptimizationMesh::coarse(float coarsenessRate, float flatnessRate, float densenessWeight,
                              float maxNormalAngle, const bool &verbose)
{
    const size_t initialNumberVertices = numberVertices;

    // Check if neighbour list is created, otherwise create it
    if (!neighborList)
        createNeighborlist();

    // If it is still not created, then some polygons are not closed
    if (neighborList == nullptr)
    {
        printf(LIB_STRING "ERROR @coarse: Could not create neigbor list. "
               "Some polygons might not be closed. Operation not done!\n");
        return 0;
    }

    NPNT3** neighbourList = neighborList;

    size_t* vertexIndexArray = new size_t[numberVertices];
    size_t* faceIndexArray = new size_t[numberFaces];

    if (verbose)
    {
        printf(LIB_STRING "Mesh has [%ld] Vertices & [%ld] Faces.\n",
               numberVertices, numberFaces);
    }

    size_t inputNumberVertices = numberVertices;

    char stop = 0;

    // If using sparseness weight, calculate the average segment length of the mesh
    if (densenessWeight > 0.0)
    {
        float* averageLengths = new float[numberFaces];

#pragma omp parallel for
        for (size_t n = 0; n < numberFaces; n++)
        {
            int a = face[n].v1;
            int b = face[n].v2;
            int c = face[n].v3;

            float nx = std::sqrt((vertex[a].x - vertex[b].x) *
                                 (vertex[a].x - vertex[b].x) +
                                 (vertex[a].y - vertex[b].y) *
                                 (vertex[a].y - vertex[b].y) +
                                 (vertex[a].z - vertex[b].z) *
                                 (vertex[a].z - vertex[b].z));

            float ny = std::sqrt((vertex[a].x - vertex[c].x) *
                                 (vertex[a].x - vertex[c].x) +
                                 (vertex[a].y - vertex[c].y) *
                                 (vertex[a].y - vertex[c].y) +
                                 (vertex[a].z - vertex[c].z) *
                                 (vertex[a].z - vertex[c].z));

            float nz = std::sqrt((vertex[c].x - vertex[b].x) *
                                 (vertex[c].x - vertex[b].x) +
                                 (vertex[c].y - vertex[b].y) *
                                 (vertex[c].y - vertex[b].y) +
                                 (vertex[c].z - vertex[b].z) *
                                 (vertex[c].z - vertex[b].z));

            averageLengths[n] = (nx + ny + nz) / 3.0f;
            // averageLength += (nx + ny + nz) / 3.0f;
        }

        if (numberFaces == 0)
        {
            printf(LIB_STRING "ERROR @coarse: Zero degree on a vertex.\n");
            delete [] averageLengths;
            return 0;
        }
        else
        {
            float averageLength = 0.f;
            for (size_t n = 0; n < numberFaces; n++)
                averageLength += averageLengths[n];

            averageLength = averageLength / (float)(numberFaces);

            delete [] averageLengths;
        }
    }

    float ratio1 = 1.0, ratio2 = 1.0;
    int maxLength = 0;
    int faceAvailableList[64], faceAvailableIndex;
    int neighborAuxList[64];

    // The main loop over all vertices
    bool* deleteFlags = new bool[numberVertices];

#pragma omp parallel for
    for (size_t n = 0; n < numberVertices; n++)
    {
        // If the vertex have been flagged to not be removed
        if (!vertex[n].selected)
        {
            continue;
        }

        // Check if the vertex has enough neigborgs to be deleted
        char deleteFlag = 1;
        NPNT3* firstNeighbour = neighbourList[n];
        while (firstNeighbour != nullptr)
        {
            int a = firstNeighbour->a;
            int auxNumber1 = 0;
            int auxNumber2 = 0;

            NPNT3* secondNeighbour = neighbourList[a];
            while (secondNeighbour != nullptr)
            {
                fflush(stdout);
                int b = secondNeighbour->a;
                NPNT3* auxNeighbour1 = neighbourList[n];
                while (auxNeighbour1 != nullptr)
                {
                    if (auxNeighbour1->a == b)
                        auxNumber2++;
                    auxNeighbour1 = auxNeighbour1->next;
                }

                auxNumber1++;
                secondNeighbour = secondNeighbour->next;
            }

            if (auxNumber1 <= 3 || auxNumber2 > 2)
                deleteFlag = 0;

            firstNeighbour = firstNeighbour->next;
        }

        deleteFlags[n] = deleteFlag;
    }

    for (size_t n = 0; n < numberVertices; n++)
    {
        // Status report
        if (((n + 1) % 888) == 0 || (n + 1) == numberVertices)
        {
            const float percentage = 100.0 * (n + 1) / (float) numberVertices;
            printf(LIB_STRING "Progress: %2.2f \r", percentage);
            fflush(stdout);
        }
        fflush(stdout);

        if (deleteFlags[n])
        {
            float x = vertex[n].x;
            float y = vertex[n].y;
            float z = vertex[n].z;

            maxLength = -1;
            NPNT3* firstNeighbour = neighbourList[n];

            float averageLengthNN = -1;

            // If using sparseness as a criteria for coarsening calculate the maximal segment length
            if (densenessWeight > 0.0)
            {
                while (firstNeighbour != nullptr)
                {
                    int a = firstNeighbour->a;
                    int b = firstNeighbour->b;

                    float nx = std::sqrt((x - vertex[a].x) *
                                         (x - vertex[a].x) +
                                         (y - vertex[a].y) *
                                         (y - vertex[a].y) +
                                         (z - vertex[a].z) *
                                         (z - vertex[a].z));
                    float ny = std::sqrt((x - vertex[b].x) *
                                         (x - vertex[b].x) +
                                         (y - vertex[b].y) *
                                         (y - vertex[b].y) +
                                         (z - vertex[b].z) *
                                         (z - vertex[b].z));
                    float nn = std::sqrt((vertex[a].x - vertex[b].x) *
                                         (vertex[a].x - vertex[b].x) +
                                         (vertex[a].y - vertex[b].y) *
                                         (vertex[a].y - vertex[b].y) +
                                         (vertex[a].z - vertex[b].z) *
                                         (vertex[a].z - vertex[b].z));

                    if (nx > maxLength)
                        maxLength = nx;

                    if (ny > maxLength)
                        maxLength = ny;

                    if ((nx + ny + nn) / 3.0 > averageLengthNN)
                        averageLengthNN = (nx + ny + nn) / 3.0;

                    firstNeighbour = firstNeighbour->next;
                }

                // Max segment length over the average segment length of the mesh
                ratio2 = maxLength / averageLengthNN; // averageLength;
                ratio2 = std::pow(ratio2, densenessWeight);
            }

            // If using curvatory as a coarsening criteria calculate the local structure tensor
            float maxAngle;
            if (flatnessRate > 0.0)
            {
                EigenValue eigenValue;
                EigenVector eigenVector = getEigenVector(n, &eigenValue, &maxAngle);

                if (eigenValue.x == 0)
                {
                    printf(LIB_STRING "ERROR @coarse: Max EigenValue is zero!\n");
                    return 0;
                }
                else
                {
                    // printf(LIB_STRING "@coarse: EigenValues: [%ld], "
                    //  "(%.3f, %.3f, %.3f)\n", n, eigenValue.x, eigenValue.y, eigenValue.z);

                    ratio1 = fabs((eigenValue.y)/(eigenValue.x));
                    ratio1 = pow(ratio1, flatnessRate);
                    // ratio1 = (1.0 - maxAngle) * fabs((eigenValue.y) / (eigenValue.x));
                }
            }

            // Compare the two coarseness criterias against the given coarsenessRate
            bool deleteVertex = ratio1 * ratio2 < coarsenessRate;

            // Use maximal angle between vertex normal as a complementary coarse criteria
            if (maxNormalAngle > 0)
                deleteVertex = deleteVertex && (maxAngle > maxNormalAngle);

            // Deleting a vertex and retrianglulate the hole
            if (deleteVertex)
            {
                inputNumberVertices--;

                // delete vertex n
                vertex[n].x = -99999;
                vertex[n].y = -99999;
                vertex[n].z = -99999;

                int neighborNumber = 0;
                firstNeighbour = neighbourList[n];
                int face_marker;
                while (firstNeighbour != nullptr)
                {
                    int a = firstNeighbour->a;
                    int c = firstNeighbour->c;
                    faceAvailableList[neighborNumber] = c;
                    neighborAuxList[neighborNumber] = a;
                    neighborNumber++;

                    // Get face marker
                    face_marker = face[c].marker;

                    // Delete faces associated with vertex n
                    face[c].v1 = -1;
                    face[c].v2 = -1;
                    face[c].v3 = -1;
                    face[c].marker = -1;

                    // Delete neighbors associated with vertex n
                    NPNT3* secondNeighbour = neighbourList[a];
                    NPNT3* auxNeighbour1 = secondNeighbour;
                    while (secondNeighbour != nullptr)
                    {
                        if (secondNeighbour->a == int(n) || secondNeighbour->b == int(n))
                        {
                            if (secondNeighbour == neighbourList[a])
                            {
                                neighbourList[a] = secondNeighbour->next;
                                free(secondNeighbour);
                                secondNeighbour = neighbourList[a];
                                auxNeighbour1 = secondNeighbour;
                            }
                            else
                            {
                                auxNeighbour1->next = secondNeighbour->next;
                                free(secondNeighbour);
                                secondNeighbour = auxNeighbour1->next;
                            }
                        }
                        else
                        {
                            if (secondNeighbour == neighbourList[a])
                            {
                                secondNeighbour = secondNeighbour->next;
                            }
                            else
                            {
                                auxNeighbour1 = secondNeighbour;
                                secondNeighbour = secondNeighbour->next;
                            }
                        }
                    }

                    int auxNumber1 = 0;
                    secondNeighbour = neighbourList[a];
                    while (secondNeighbour != nullptr)
                    {
                        auxNumber1++;
                        secondNeighbour = secondNeighbour->next;
                    }
                    firstNeighbour->b = auxNumber1;
                    firstNeighbour = firstNeighbour->next;
                }

                firstNeighbour = neighbourList[n];
                while (firstNeighbour->next != nullptr)
                    firstNeighbour = firstNeighbour->next;
                firstNeighbour->next = neighbourList[n];

                faceAvailableIndex = 0;
                subdividePolygon(neighbourList[n], faceAvailableList,
                                 &faceAvailableIndex, face_marker);

                // Order the neighbors
                for (int m = 0; m < neighborNumber; ++m)
                {
                    firstNeighbour = neighbourList[neighborAuxList[m]];
                    int c = firstNeighbour->a;
                    while (firstNeighbour != nullptr)
                    {
                        int a = firstNeighbour->a;
                        int b = firstNeighbour->b;

                        NPNT3* secondNeighbour = firstNeighbour->next;
                        while (secondNeighbour != nullptr)
                        {
                            int a0 = secondNeighbour->a;
                            int b0 = secondNeighbour->b;

                            // Assume counter clockwise orientation
                            if (a0==b && b0!=a)
                            {
                                NPNT3* auxNeighbour1 = firstNeighbour;
                                while (auxNeighbour1 != nullptr)
                                {
                                    if (auxNeighbour1->next == secondNeighbour)
                                    {
                                        auxNeighbour1->next = secondNeighbour->next;
                                        break;
                                    }
                                    auxNeighbour1 = auxNeighbour1->next;
                                }
                                auxNeighbour1 = firstNeighbour->next;
                                firstNeighbour->next = secondNeighbour;
                                secondNeighbour->next = auxNeighbour1;
                                break;
                            }

                            secondNeighbour = secondNeighbour->next;
                        }

                        if (firstNeighbour->next == nullptr)
                        {
                            if (firstNeighbour->b != c)
                            {
                                printf(LIB_STRING
                                    "ERROR @coarse: Some polygons are not closed @[%ld] \n", n);
                            }
                        }

                        firstNeighbour = firstNeighbour->next;
                    }
                }

                // Smooth the neighbors
                int auxNumber2 = 0;
                for (int m = 0; m < neighborNumber; ++m)
                {
                    if (!vertex[auxNumber2].selected)
                        continue;

                    auxNumber2 = neighborAuxList[m];

                    x = vertex[auxNumber2].x;
                    y = vertex[auxNumber2].y;
                    z = vertex[auxNumber2].z;

                    float nx = 0;
                    float ny = 0;
                    float nz = 0;
                    float weight = 0;

                    firstNeighbour = neighbourList[auxNumber2];
                    while (firstNeighbour != nullptr)
                    {
                        int a = firstNeighbour->a;
                        int b = firstNeighbour->b;

                        NPNT3* secondNeighbour = firstNeighbour->next;
                        if (secondNeighbour == nullptr)
                            secondNeighbour = neighbourList[auxNumber2];

                        int c = secondNeighbour->b;

                        Vertex newPosition = getVertexPositionAlongSurface(x, y, z, b, a, c);
                        float angle = computeDotProduct(b, a, c);
                        angle += 1.0;
                        nx += angle * newPosition.x;
                        ny += angle * newPosition.y;
                        nz += angle * newPosition.z;

                        weight += angle;
                        firstNeighbour = firstNeighbour->next;
                    }

                    if (weight > 0)
                    {
                        nx /= weight;
                        ny /= weight;
                        nz /= weight;

                        EigenValue eigenValue;
                        EigenVector eigenVector = getEigenVector(auxNumber2,
                                                                 &eigenValue, &maxAngle, false);

                        if ((eigenVector.x1==0 && eigenVector.y1==0 && eigenVector.z1==0) ||
                            (eigenVector.x2==0 && eigenVector.y2==0 && eigenVector.z2==0) ||
                            (eigenVector.x3==0 && eigenVector.y3==0 && eigenVector.z3==0))
                        {
                            vertex[auxNumber2].x = nx;
                            vertex[auxNumber2].y = ny;
                            vertex[auxNumber2].z = nz;
                        }
                        else
                        {
                            nx -= x; ny -= y; nz -= z;

                            float w1 = (nx * eigenVector.x1 + ny * eigenVector.y1 + nz * eigenVector.z1) /
                                    (1.0 + eigenValue.x);
                            float w2 = (nx * eigenVector.x2 + ny * eigenVector.y2 + nz * eigenVector.z2) /
                                    (1.0 + eigenValue.y);
                            float w3 = (nx *eigenVector.x3 + ny * eigenVector.y3 + nz * eigenVector.z3) /
                                    (1.0 + eigenValue.z);

                            vertex[auxNumber2].x =
                                    w1 * eigenVector.x1 + w2 * eigenVector.x2 + w3 * eigenVector.x3 + x;
                            vertex[auxNumber2].y =
                                    w1 * eigenVector.y1 + w2 * eigenVector.y2 + w3 * eigenVector.y3 + y;
                            vertex[auxNumber2].z =
                                    w1 * eigenVector.z1 + w2 * eigenVector.z2 + w3 * eigenVector.z3 + z;
                        }
                    }
                }
            }
        }

        // if (inputNumberVertices < MeshSizeUpperLimit) { stop = 1; break; }
    }

    delete [] deleteFlags;

    // Clean the lists of nodes and faces
    int startIndex = 0;
    for (size_t n = 0; n < numberVertices; ++n)
    {
        if (vertex[n].x != -99999 && vertex[n].y != -99999 && vertex[n].z != -99999)
        {
            if (startIndex != int(n))
            {
                vertex[startIndex].x = vertex[n].x;
                vertex[startIndex].y = vertex[n].y;
                vertex[startIndex].z = vertex[n].z;
                vertex[startIndex].marker = vertex[n].marker;
                vertex[startIndex].selected = vertex[n].selected;
                neighbourList[startIndex] = neighbourList[n];
            }

            vertexIndexArray[n] = startIndex;
            startIndex++;
        }
        else
        {
            vertexIndexArray[n] = -1;
        }
    }

    numberVertices = startIndex;

    startIndex = 0;
    for (size_t n = 0; n < numberFaces; n++)
    {
        int a = face[n].v1;
        int b = face[n].v2;
        int c = face[n].v3;
        int face_marker = face[n].marker;

        if (a >= 0 && b >= 0 && c >= 0 &&
            vertexIndexArray[a] >= 0 && vertexIndexArray[b] >= 0 && vertexIndexArray[c] >= 0)
        {
            face[startIndex].v1 = vertexIndexArray[a];
            face[startIndex].v2 = vertexIndexArray[b];
            face[startIndex].v3 = vertexIndexArray[c];
            face[startIndex].marker = face_marker;
            faceIndexArray[n] = startIndex;
            startIndex++;
        }
        else
        {
            faceIndexArray[n] = -1;
        }
    }
    numberFaces = startIndex;

    for (size_t n = 0; n < numberVertices; n++)
    {
        NPNT3* firstNeighbour = neighbourList[n];
        while (firstNeighbour != nullptr)
        {
            int a = firstNeighbour->a;
            int b = firstNeighbour->b;
            int c = firstNeighbour->c;

            firstNeighbour->a = vertexIndexArray[a];
            firstNeighbour->b = vertexIndexArray[b];
            firstNeighbour->c = faceIndexArray[c];

            firstNeighbour = firstNeighbour->next;
        }
    }

    delete [] vertexIndexArray;
    delete [] faceIndexArray;
    printf("\n");

    if (verbose)
    {
        const float ratio = 100.0 * static_cast< float >(initialNumberVertices - numberVertices) /
                (initialNumberVertices);

        printf(LIB_STRING "Mesh has [%ld] Vertices & [%ld] Faces. Reduction Ratio [%f %%] \n",
               numberVertices, numberFaces, ratio);
    }

    return stop;
}

void OptimizationMesh::coarseDense(const float& denseRate,
                                   const size_t &iterations,
                                   const bool verbose)
{
    TIMER_SET;
    for (size_t i = 0; i < iterations; ++i)
        if (!coarse(denseRate, 0, 10, -1, verbose)) break;
    printf(LIB_STRING "STATS: Coarse Dense [%f Seconds] \n", GET_TIME_SECONDS);
}

void OptimizationMesh::coarseFlat(const float& flatnessRate,
                                  const size_t &iterations, const bool verbose)
{
    TIMER_SET;
    for (size_t i = 0; i < iterations; ++i)
        if (!coarse(flatnessRate, 1, 0, -1, verbose)) break;
    printf(LIB_STRING "STATS: Coarse Flat [%f Seconds] \n", GET_TIME_SECONDS);
}

#ifdef PYBIND
pybind11::array_t< Vertex > OptimizationMesh::getVertexData()
{
    //pybind11::capsule cleanup(vertex, [](void *f) {});
    return pybind11::array_t< Vertex >(
                { numberVertices },     // Shape
                { sizeof(Vertex) },     // Stride
                vertex                 // Pointer to data
               // cleanup                 // Garbage collection callback
                );
}

pybind11::array_t< Triangle > OptimizationMesh::getFaceData()
{
   // pybind11::capsule cleanup(face, [](void *f) {});
    return pybind11::array_t< Triangle >(
                { numberFaces },        // Shape
                { sizeof(Triangle) },   // Stride
                face                   // Pointer to data
                //cleanup                 // Garbage collection callback
                );
}
#endif

