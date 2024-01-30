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

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "OptimizationMesh.hh"
#include "Timer.hpp"
#include <omp.h>

// For the version
#define STRINGIZE(x) #x
#define STRINGIZE_VALUE_OF(x) STRINGIZE(x)

namespace py = pybind11;

/**
 * @brief testOMP
 * Tests if  OpenMP is installed or not.
 * @param numberElements
 */
void testOMP(int numberElements)
{
    printf("Number of threads [%d] \n", omp_get_max_threads());
    size_t* a = new size_t[numberElements];
    size_t* b = new size_t[numberElements];
    size_t* c = new size_t[numberElements];

    TIMER_SET;
#pragma omp parallel for
    for (int i = 0; i < numberElements; ++i) { a[i] = i * 3 + 100; b[i] = 2 + i; c[i] = 0; }

#pragma omp parallel for
    for (int i = 0; i < numberElements; ++i) { c[i] = a[i] + b[i]; }

    printf("Example: @[0] element: %ld \n", c[0]);
    printf(LIB_STRING "STATS: W/ OpenMP Test [%f Seconds] \n", GET_TIME_SECONDS);

    TIMER_RESET;
    for (int i = 0; i < numberElements; ++i) { a[i] = i * 3 + 100; b[i] = 2 + i; c[i] = 0; }
    for (int i = 0; i < numberElements; ++i) { c[i] = a[i] + b[i]; }
    printf("Example: @[0] element: %ld \n", c[0]);
    printf(LIB_STRING "STATS: W/O OpenMP Test [%f Seconds] \n", GET_TIME_SECONDS);

    delete [] a; delete [] b; delete [] c;
}

/**
 * @brief exposeClasses
 * Helper functiont to expose C++ classes to Python.
 * @note In this function you would normally put this code directly in the PYBIND11_MODULE block,
 * but for larger libraries you will want to use functions in separate files to expose different
 * parts of your C++ library.
 * @param m
 */
void exposeClasses(py::module m)
{
    py::class_<Vertex>(m, "Vertex")
        .def(py::init<>(),
             R"mydelimiter(
                Constrcutor
             )mydelimiter")
        ;

    py::class_<Triangle>(m, "Triangle")
        .def(py::init<>(),
             R"mydelimiter(
                Constrcutor
             )mydelimiter")
        ;

    py::class_<OptimizationMesh>(m, "OptimizationMesh")
        .def(py::init<size_t, size_t>(),
             R"mydelimiter(
                Default constrcutor.
             )mydelimiter")
        .def(py::init<BVertices, BTriangles>(),
             R"mydelimiter(
                Constrcutor that takes, in order, list of vertices and triangles from
                a Blender mesh to create an OMesh.
             )mydelimiter")
        .def("scale_mesh_uniformly", &OptimizationMesh::scaleMeshUniformly,
             py::arg("scale_factor"),
             R"mydelimiter(
                Scales the mesh uniformly along the X, Y and Z coordinates according to the
                given scale_factor argument.
             )mydelimiter")
        .def("scale_mesh", &OptimizationMesh::scaleMesh,
             py::arg("x_scale_factor"),
             py::arg("y_scale_factor"),
             py::arg("z_scale_factor"),
             R"mydelimiter(
                Scales the mesh along the X, Y and Z coordinates with different
                scale factors applied to each dimension.
             )mydelimiter")
        .def("optimize_using_default_parameters", &OptimizationMesh::optimizeUsingDefaultParameters,
             R"mydelimiter(
                Optimizes the mesh using the default parameters.
             )mydelimiter")
        .def("get_vertex_data", &OptimizationMesh::getVertexData,
             R"mydelimiter(
                Returns a numpy structure of the vertices of the optimized mesh.
             )mydelimiter")
        .def("get_face_data", &OptimizationMesh::getFaceData,
             R"mydelimiter(
                Returns a numpy structure of the faces of the optimized mesh.
             )mydelimiter")
        .def("smooth", &OptimizationMesh::smooth,
             py::arg("largest_min_angle"),
             py::arg("smallest_max_angle"),
             py::arg("max_number_iterations"),
             py::arg("preserve_ridges"),
             py::arg("verbose"),
             R"mydelimiter(
                Smoothes the surface of the mesh.
             )mydelimiter")
        .def("smooth_normals", &OptimizationMesh::smoothNormals,
             py::arg("largest_min_angle"),
             py::arg("smallest_max_angle"),
             py::arg("verbose"),
             R"mydelimiter(
                Smoothes the normals of the surface of the mesh.
             )mydelimiter")
        .def("coarse", &OptimizationMesh::coarse,
             py::arg("coarseness_rate"),
             py::arg("flatness_rate"),
             py::arg("denseness_weight"),
             py::arg("largest_normal_angle"),
             py::arg("verbose"),
             R"mydelimiter(
                Coarses the surface of the mesh.
             )mydelimiter")
        .def("refine", &OptimizationMesh::refine,
             R"mydelimiter(
                Refines the surface of the mesh, when needed for the selected vertices.
             )mydelimiter")
        .def("coarse_dense", &OptimizationMesh::coarseDense,
             py::arg("dense_rate"),
             py::arg("iterations"),
             py::arg("verbose"),
             R"mydelimiter(
                Coarses the dense regions of the surface mesh.
             )mydelimiter")
        .def("coarse_flat", &OptimizationMesh::coarseFlat,
             py::arg("flatness_rate"),
             py::arg("iterations"),
             py::arg("verbose"),
             R"mydelimiter(
                Coarses the flat regions of the surface mesh.
             )mydelimiter")
        ;
}

/**
 * @brief exposeFunctions
 *  Helper functiont to expose C++ functions (without classes) to Python.
 * @param m
 */
void exposeFunctions(py::module m)
{
    m.def("test_omp", &testOMP,
          py::arg("number_elements"),
          R"mydelimiter(
            Tests the installation of OpenMP in the system. Just give this function a number
            of elements to perform a vector addition and check if all the CPU cores are running
            or not.
          )mydelimiter");
}

/**
 * @brief PYBIND11_MODULE
 * Compile the Python module.
 */
PYBIND11_MODULE(omesh, m)
{
    std::string doc = "Python bindings for the OMesh library, v." STRINGIZE_VALUE_OF(VERSION_INFO);
    m.doc() = doc.c_str();

    PYBIND11_NUMPY_DTYPE(Vertex, x, y, z);
    PYBIND11_NUMPY_DTYPE(Triangle, v1, v2, v3);

    exposeClasses(m);
    exposeFunctions(m);
}
