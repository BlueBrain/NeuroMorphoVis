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
import time
import sys

# Internal imports
import nmv.bmeshi
import nmv.consts
import nmv.mesh
import nmv.scene


####################################################################################################
# @is_omesh_available
####################################################################################################
def is_omesh_available():

    # Get the version of the Blender software that is running the code
    python_version = '%s.%s' % (str(sys.version_info.major), str(sys.version_info.minor))

    # Append the path to the libraries to the system path
    libs_path = '%s/python%s/site-packages' % (nmv.consts.Paths.LIBS_PATH, python_version)
    sys.path.append(libs_path)

    # Try to import the library to see if it is available or not
    try:
        import omesh

    # The library is not available
    except ImportError:
        return False

    # The library is available
    return True


####################################################################################################
# @create_optimization_mesh
####################################################################################################
def create_optimization_mesh(mesh_object):
    """Creates an optimization mesh from a given mesh object.

    @param mesh_object:
        A given mesh object to create an OMesh (optimization mesh) object.
    @return:
        A reference to the created OMesh (optimization mesh).
    """

    if not is_omesh_available():
        return None

    # Create a list of vertices
    vertices = list()
    for v in mesh_object.data.vertices:
        vertices.append([v.co[0], v.co[1], v.co[2]])

    # Create a list of faces
    faces = list()
    for face in mesh_object.data.polygons:
        v = face.vertices
        faces.append([v[0], v[1], v[2]])

    # Create an optimization mesh and return a reference to it
    import omesh
    optimization_mesh = omesh.OptimizationMesh(vertices, faces)

    # Free the copies
    vertices.clear()
    faces.clear()

    # Return a reference to the optimization mesh
    return optimization_mesh


####################################################################################################
# @optimize_mesh
####################################################################################################
def optimize_mesh(mesh_object,
                  delete_input_mesh=False):
    """Optimizes the given mesh object and create a watertight output.

    @param mesh_object:
        A given mesh object to get optimized.
    @param delete_input_mesh:
        Deletes the input mesh from the scene to save memory.
    @return:
        A reference to the created mesh object.
    """

    if not is_omesh_available():
        return mesh_object

    start = time.time()

    # If the given object is not mesh, assert
    assert mesh_object.type == 'MESH'

    # Ensure that the mesh is triangulated
    nmv.mesh.triangulate_mesh(mesh_object)

    # Create an optimization mesh
    optimization_mesh = create_optimization_mesh(mesh_object)

    # Optimize the mesh and reduce the number of faces
    optimization_mesh.coarse_flat(0.05, 5, True)

    # Smooth normals
    optimization_mesh.smooth_normals(15, 150, True)

    # Initially smooth by 15 iterations
    optimization_mesh.smooth(15, 150, 25, False, True)

    # Smooth normals
    optimization_mesh.smooth_normals(15, 150, True)

    # Get a copy to the vertex and face data
    vertices = optimization_mesh.get_vertex_data()
    faces = optimization_mesh.get_face_data()

    # Create an optimized bmesh
    optimized_bmesh_object = nmv.bmeshi.create_bmesh_copy_from_vertices_and_faces(vertices, faces)

    # Verify if the mesh is watertight or not
    watertightness_check = nmv.bmeshi.is_bmesh_object_watertight(optimized_bmesh_object)

    # If it is watertight, then create the mesh object
    if watertightness_check.is_watertight():
        print('WATERTIGHNTESS\t OK!')

        end = time.time()
        print('OPTIMIZATION TIME: %f' % (end - start))

        # Free the optimized mesh
        optimized_bmesh_object.free()

        # Create a new mesh
        import bpy
        mesh_data = bpy.data.meshes.new("%s Data" % mesh_object.name)
        mesh_data.from_pydata(vertices, [], faces)
        mesh_data.update()

        # Create a new watertight mesh object
        watertight_mesh_object = bpy.data.objects.new("%s_watertight" % mesh_object.name, mesh_data)

        # Link it to the scene
        scene = bpy.context.scene
        scene.collection.objects.link(watertight_mesh_object)

        # Delete the input mesh if required
        if delete_input_mesh:
            nmv.scene.delete_object_in_scene(scene_object=mesh_object)

        # Return the watertight mesh
        return watertight_mesh_object

    else:
        # Print the watertightness check
        watertightness_check.print_status()

        # Try to make a watertight bmesh object
        nmv.bmeshi.try_to_make_bmesh_object_watertight(optimized_bmesh_object)

        end = time.time()
        print('OPTIMIZATION TIME: %f' % (end - start))

        # Create the corresponding watertight mesh object
        watertight_mesh_object = nmv.bmeshi.convert_bmesh_to_mesh(
            optimized_bmesh_object, '%s_watertight' % mesh_object.name)

        # Free the optimized mesh
        optimized_bmesh_object.free()

        # Delete the input mesh if required
        if delete_input_mesh:
            nmv.scene.delete_object_in_scene(scene_object=mesh_object)

        # Return the watertight mesh
        return watertight_mesh_object
