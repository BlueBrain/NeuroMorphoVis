####################################################################################################
# Copyright (c) 2024, EPFL / Blue Brain Project
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

import sys
import argparse
import bpy

import nmv.mesh
import nmv.bmeshi
import nmv.scene

lib_path = '/projects/building/lib/python3.10/site-packages/omesh-1.0.0-py3.10-linux-x86_64.egg'
sys.path.append(lib_path)
import omesh

####################################################################################################
# @create_optimization_mesh
####################################################################################################
def create_optimization_mesh(mesh_object):
    """Creates an optimization mesh from a given mesh object.

    @param mesh_object:
    @return:
    """
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

    import time

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

    opt_file = '/hdd1/biovis-24-zenodo/optimization-time/%s' % mesh_object.name

    # If it is watertight, then create the mesh object
    if watertightness_check.is_watertight():
        print('WATERTIGHNTESS\t OK!')

        end = time.time()
        print('OPTIMIZATION TIME: %f' % (end - start))
        f = open(opt_file, 'w')
        f.write(str(end - start))
        f.close()

        # Free the optimized mesh
        optimized_bmesh_object.free()

        # Create a new mesh
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
        f = open(opt_file, 'w')
        f.write(str(end - start))
        f.close()

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


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):
    """Parses the input arguments.

    :param arguments:
        Command line arguments.
    :return:
        Arguments list.
    """

    # add all the options
    description = 'Verify the number of self-intersections w.r.t optimization iterations'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'The input directory that contains the meshes'
    parser.add_argument('--input-directory', action='store', help=arg_help)

    arg_help = 'The input mesh file name'
    parser.add_argument('--input-mesh', action='store', help=arg_help)

    arg_help = 'Output directory, where the final result stored'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    # Parse the arguments
    return parser.parse_args()

####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Clear the scene
    nmv.scene.clear_scene()

    # Load the mesh object
    if '.obj' in args.input_mesh:
        mesh = nmv.file.import_obj_file(args.input_directory, args.input_mesh)

    elif '.stl' in args.input_mesh:
        mesh = nmv.file.import_stl_file(args.input_directory, args.input_mesh)
    else:
        print('Cannot read the given extension. Use .stl ot .obj!')
        exit(0)

    # Triangulate the mesh
    nmv.mesh.triangulate_mesh(mesh)

    # Count the self-intersections and return the results string
    watertight_mesh = optimize_mesh(mesh)

    # Write the result
    nmv.file.export_object_to_stl_file(watertight_mesh, args.output_directory, watertight_mesh.name)

    # Delete the input mesh object
    nmv.scene.delete_object_in_scene(mesh)
    nmv.scene.delete_object_in_scene(watertight_mesh)