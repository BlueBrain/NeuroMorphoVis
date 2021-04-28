####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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


# Blender imports
import bpy
import bmesh
from mathutils import Vector

# Internal imports
import nmv.mesh


####################################################################################################
# @TetGenTetrahedralReader
####################################################################################################
class TetGenTetrahedralReader:
    """TetGen tetrahedral mesh reader.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 node_file,
                 ele_file):
        """Constructor

        :param node_file:
            Path to the node file.
        :param ele_file:
            Path to the element file.
        """

        # Node file
        self.node_file = node_file

        # Element file
        self.ele_file = ele_file

        # Nodes
        self.nodes = list()

        # Elements
        self.elements = list()

        # Number of nodes
        self.number_nodes = 0

        # Number of elements
        self.number_elements = 0

    ################################################################################################
    # @read_node_file
    ################################################################################################
    def read_node_file(self):
        """Reads a node file.
        """

        # Open the file
        file = open(self.node_file, 'r')

        # Read the file line by line into a structure
        for i, line in enumerate(file):

            # Read the number of nodes
            if i == 0:
                data = ' '.join(line.split())
                data = data.split(' ')
                self.number_nodes = data[0]

            # Actual nodes
            else:
                # Avoid comments
                if '#' in line:
                    continue

                data = ' '.join(line.split())
                data = data.split(' ')

                # Index
                index = int(data[0])

                # Coordinates
                x = float(data[1])
                y = float(data[2])
                z = float(data[3])

                # Add to the list
                vertex = Vector((x, y, z))
                self.nodes.append(vertex)

        # Close the file
        file.close()

    ################################################################################################
    # @read_ele_file
    ################################################################################################
    def read_ele_file(self):
        """Reads an element file.
        """

        # Open the file
        file = open(self.ele_file, 'r')

        # Read the file line by line into a structure
        for i, line in enumerate(file):

            # Read the number of elements
            if i == 0:
                data = line.split(' ')
                self.number_elements = data[0]

            # Actual elements
            else:
                # Avoid comments
                if '#' in line:
                    continue

                data = ' '.join(line.split())
                data = data.split(' ')

                # Index
                index = int(data[0])

                # Elements
                n0 = int(data[1])
                n1 = int(data[2])
                n2 = int(data[3])
                n3 = int(data[4])

                # Add to the list
                self.elements.append([n0, n1, n2, n3])

        # Close the file
        file.close()

    ################################################################################################
    # @construct_tetrahedral_mesh
    ################################################################################################
    def construct_tetrahedral_mesh(self):
        """Construct the tetrahedral mesh

        :return:
            A default mesh file containing the tetrahedral elements.
        """

        # Create a bmesh
        tetrahedral_bmesh = bmesh.new()

        # Vertices
        vertices = list()

        # Add the vertices and faces
        for i, element in enumerate(self.elements):
            # Get the vertices
            v1 = self.nodes[element[0] - 1]
            v2 = self.nodes[element[1] - 1]
            v3 = self.nodes[element[2] - 1]
            v4 = self.nodes[element[3] - 1]

            # Get the vertices from the list
            vertices.append(tetrahedral_bmesh.verts.new(v1))
            vertices.append(tetrahedral_bmesh.verts.new(v2))
            vertices.append(tetrahedral_bmesh.verts.new(v3))
            vertices.append(tetrahedral_bmesh.verts.new(v4))

        for i, vertex in enumerate(vertices):
            vertex.index = i

        # Process the elements
        for i, element in enumerate(self.elements):
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

        # Bmesh reconstructed
        tetrahedral_mesh = bpy.data.meshes.new('Tetrahedron')

        # Convert to a mesh
        tetrahedral_bmesh.to_mesh(tetrahedral_mesh)

        # New object
        tetrahedral_mesh_object = bpy.data.objects.new('Tetrahedron', tetrahedral_mesh)

        # Link it to the scene
        bpy.context.scene.collection.objects.link(tetrahedral_mesh_object)

        # Return the mesh object
        return tetrahedral_mesh_object

    ################################################################################################
    # @create_tetrahedral_mesh
    ################################################################################################
    def create_tetrahedral_mesh(self):
        """Creates a default tetrahedral mesh.

        :return:
            A reference to the created mesh.
        """

        # Read the node file
        self.read_node_file()

        # Read the elements file
        self.read_ele_file()

        # Construct the tetrahedral mesh and return a reference to it
        return self.construct_tetrahedral_mesh()

    ################################################################################################
    # @create_simplified_tetrahedral_mesh
    ################################################################################################
    def create_simplified_tetrahedral_mesh(self):
        """Creates a simplified tetrahedral mesh with no duplicate vertices. This will save a lot
        of memory during the rendering process.

        :return:
            A reference to the created mesh.
        """
        # Read the node file
        self.read_node_file()

        # Read the elements file
        self.read_ele_file()

        # Construct the tetrahedral mesh and return a reference to it
        tetrahedral_mesh = self.construct_tetrahedral_mesh()

        # Remove the duplicates
        nmv.mesh.remove_doubles(tetrahedral_mesh)

        # Return a reference to the mesh
        return tetrahedral_mesh

    ################################################################################################
    # @create_wire_frame_tetrahedral_mesh
    ################################################################################################
    def create_wire_frame_tetrahedral_mesh(self,
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
