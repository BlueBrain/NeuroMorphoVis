####################################################################################################
# Copyright (c) 2020 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import os

# Blender imports
import bpy
import bmesh
from mathutils import Vector

# Internal imports
import nmv.mesh


####################################################################################################
# @QuarTetTetrahedralReader
####################################################################################################
class QuarTetTetrahedralReader:
    """QuarTet tetrahedral mesh reader.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 tet_file):
        """Constructor

        :param tet_file:
            Quartet .tet file.
        """

        # Node file
        self.tet_file = tet_file

        # Nodes
        self.nodes = list()

        # Elements
        self.elements = list()

        # Number of nodes
        self.number_nodes = 0

        # Number of elements
        self.number_elements = 0

    ################################################################################################
    # @Tetrahedron
    ################################################################################################
    class Tetrahedron:
        """Tetrahedron
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            """Constructor
            """

            # Tetrahedron index
            self.index = None

            # Tetrahedron face
            self.face = None

    ################################################################################################
    # @__init__
    ################################################################################################
    class TetrahedralMeshData:
        """TetrahedralMeshData
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            """Constructor
            """

            # Vertex list
            self.vertices = None

            # Tetrahedra list
            self.tetrahedrons = None

    ################################################################################################
    # @read_tet_file
    ################################################################################################
    def read_tet_file(self):
        """Read the .tet file.
        """

        data = list()

        # Open the file
        file = open(self.tet_file, 'r')

        # Read every line
        for line in file:

            # If line is a comment, ignore
            if '#' in line:
                continue

                # Get the number of vertices and tets
            if 'tet' in line:
                data_count = line
                continue

            data.append(line.strip('\n'))

        # Close the file
        file.close()

        # Get the number of vertices and faces from the data_count
        data_count = data_count.split(' ')

        number_vertices = int(data_count[1])
        faces = int(data_count[2])

        nmv.logger.log('The volumetric mesh has [%d] vertices and [%d] faces' % (number_vertices,
                                                                                 faces))

        # Get the vertices
        vertices = list()
        for i in range(number_vertices):
            vertex_data = data[i].split()
            vertex = Vector((float(vertex_data[0]), float(vertex_data[1]), float(vertex_data[2])))
            vertices.append(vertex)

        # Get the faces
        faces = list()
        for i in range(number_vertices, len(data)):
            face_data = data[i].split()
            face = [int(face_data[0]), int(face_data[1]), int(face_data[2]), int(face_data[3])]
            faces.append(face)

        # Create the tetrahedrons
        tetrahedrons = list()
        for i, face in enumerate(faces):
            tetrahedron = self.Tetrahedron()
            tetrahedron.index = i
            tetrahedron.face = face
            tetrahedrons.append(tetrahedron)

        # Create the tetrahedral mesh data structure
        tetrahedral_mesh_data = self.TetrahedralMeshData()
        tetrahedral_mesh_data.vertices = vertices
        tetrahedral_mesh_data.tetrahedrons = tetrahedrons

        # Return the mesh data
        return tetrahedral_mesh_data

    ################################################################################################
    # @create_tetrahedral_mesh
    ################################################################################################
    def create_tetrahedral_mesh(self):
        """Create a tetrahedral mesh and link it to the scene.
        """

        # Read the file
        tetrahedral_mesh_data = self.read_tet_file()

        # Create a bmesh
        tetrahedral_bmesh = bmesh.new()

        vertices = list()

        # Add the vertices and faces
        for i, tetrahedron in enumerate(tetrahedral_mesh_data.tetrahedrons):
            vertex_list = tetrahedral_mesh_data.vertices

            # Get the vertices from the list
            vertices.append(tetrahedral_bmesh.verts.new(vertex_list[tetrahedron.face[0]]))
            vertices.append(tetrahedral_bmesh.verts.new(vertex_list[tetrahedron.face[1]]))
            vertices.append(tetrahedral_bmesh.verts.new(vertex_list[tetrahedron.face[2]]))
            vertices.append(tetrahedral_bmesh.verts.new(vertex_list[tetrahedron.face[3]]))

        # tetrahedral_mesh.verts.ensure_lookup_table()
        for i, vertex in enumerate(vertices):
            vertex.index = i

        # Add the vertices and faces
        for i, tetrahedron in enumerate(tetrahedral_mesh_data.tetrahedrons):
            # Get the vertices to construct the faces
            v1 = vertices[4 * i + 0]
            v2 = vertices[4 * i + 1]
            v3 = vertices[4 * i + 2]
            v4 = vertices[4 * i + 3]

            # Add the faces to the mesh
            f1 = tetrahedral_bmesh.faces.new((v1, v2, v3))
            f2 = tetrahedral_bmesh.faces.new([v2, v3, v4])
            f3 = tetrahedral_bmesh.faces.new([v3, v4, v1])
            f4 = tetrahedral_bmesh.faces.new([v1, v4, v2])

        # Get mesh base name
        mesh_name = os.path.basename(self.tet_file).split('.')[0]

        tetrahedral_mesh = bpy.data.meshes.new(mesh_name)
        tetrahedral_bmesh.to_mesh(tetrahedral_mesh)

        tetrahedral_mesh_object = bpy.data.objects.new(mesh_name, tetrahedral_mesh)
        bpy.context.scene.collection.objects.link(tetrahedral_mesh_object)

        return tetrahedral_mesh_object

    ################################################################################################
    # @create_simplified_tetrahedral_mesh
    ################################################################################################
    def create_simplified_tetrahedral_mesh(self):
        """Creates a simplified tetrahedral mesh with no duplicate vertices. This will save a lot
        of memory during the rendering process.

        :return:
            A reference to the created mesh.
        """

        # Construct the tetrahedral mesh and return a reference to it
        tetrahedral_mesh = self.create_tetrahedral_mesh()

        # Remove the duplicates
        nmv.mesh.remove_doubles(tetrahedral_mesh)

        # Return a reference to the mesh
        return tetrahedral_mesh

    ################################################################################################
    # @create_wireframe_tetrahedral_mesh
    ################################################################################################
    def create_wireframe_tetrahedral_mesh(self,
                                          wireframe_thickness=0.01):
        """Creates a wireframe mesh.

        :param wireframe_thickness:
            The thickness of the wireframe.
        :return:
            A reference to the wireframe mesh.
        """

        # Create the simplified tetrahedral mesh
        simplified_tetrahedral_mesh = self.create_simplified_tetrahedral_mesh()

        # Apply the wireframe operator
        return nmv.mesh.create_wire_frame(
            mesh_object=simplified_tetrahedral_mesh, wireframe_thickness=wireframe_thickness)


####################################################################################################
# @import_quartet_mesh
####################################################################################################
def import_quartet_mesh(tet_file):
    """Imports a tetrahedral mesh and link it to the scene.

    :param tet_file:
        Quartet .tet file.
    :return:
        A reference to the imported mesh.
    """

    reader = nmv.file.QuarTetTetrahedralReader(tet_file=tet_file)
    return reader.create_tetrahedral_mesh()


####################################################################################################
# @import_quartet_mesh
####################################################################################################
def import_quartet_mesh_simplified(tet_file):
    """Imports a simplified tetrahedral mesh with no duplicate vertices. This will save a lot
    of memory during the rendering process.

    :param tet_file:
        Quartet .tet file.
    :return:
        A reference to the imported mesh.
    """

    reader = nmv.file.QuarTetTetrahedralReader(tet_file=tet_file)
    return reader.create_simplified_tetrahedral_mesh()


####################################################################################################
# @import_quartet_mesh
####################################################################################################
def import_quartet_mesh_wireframe(tet_file,
                                  wireframe_thickness):
    """Imports a quartet mesh into a wireframe.

    :param tet_file:
        Quartet .tet file.
    :param wireframe_thickness:
        The thickness of the wireframe.
    :return:
        A reference to the imported mesh.
    """

    reader = nmv.file.QuarTetTetrahedralReader(tet_file=tet_file)
    return reader.create_wireframe_tetrahedral_mesh(wireframe_thickness=wireframe_thickness)
