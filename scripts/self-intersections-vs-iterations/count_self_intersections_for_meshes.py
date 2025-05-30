import sys
import argparse
import subprocess
import bpy
import bmesh
import mathutils

import nmv.mesh
import nmv.bmeshi
import nmv.scene

lib_path = '/projects/building/lib/python3.10/site-packages/omesh-1.0.0-py3.10-linux-x86_64.egg'
sys.path.append(lib_path)
import omesh


####################################################################################################
# @create_bmesh_copy_from_mesh_object
####################################################################################################
def create_bmesh_copy_from_mesh_object(mesh_object,
                                       transform=True,
                                       triangulate=False):
    # If the given object is not mesh, assert
    assert mesh_object.type == 'MESH'

    # Get access to the mesh data
    mesh_data = mesh_object.data

    # If the mesh is in the edit mode
    if mesh_object.mode == 'EDIT':
        bm_orig = bmesh.from_edit_mesh(mesh_data)
        bmesh_object = bm_orig.copy()
    else:
        bmesh_object = bmesh.new()
        bmesh_object.from_mesh(mesh_data)

    # If we need to consider the transformation
    if transform:
        matrix = mesh_object.matrix_world.copy()
        if not matrix.is_identity:
            bmesh_object.transform(matrix)

            # Update normals if the matrix has no rotation.
            matrix.translation.zero()
            if not matrix.is_identity:
                bmesh_object.normal_update()

    # If we need to triangulate the bmesh
    if triangulate:
        bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)

    # Return a reference to the bmesh object
    return bmesh_object


####################################################################################################
# @check_self_intersections_of_mesh_object
####################################################################################################
def check_self_intersections_of_mesh_object(mesh_object):
    # If the input object does not contain any polygons, return an empty list
    if not mesh_object.data.polygons:
        return []

    # Create the bmesh object
    bmesh_object = create_bmesh_copy_from_mesh_object(
        mesh_object=mesh_object, transform=False, triangulate=False)

    # Construct the BVHTree from the bmesh object
    tree = mathutils.bvhtree.BVHTree.FromBMesh(bmesh_object, epsilon=0.00001)

    # Check if any overlaps exist
    overlap = tree.overlap(tree)

    # Obtain a list of self-intersecting faces
    faces_error = {i for i_pair in overlap for i in i_pair}

    # Return a list of
    return faces_error


####################################################################################################
# @count_self_intersections
####################################################################################################
def count_self_intersections(mesh_object, n_iterations):
    vertices = list()
    for v in mesh_object.data.vertices:
        vertices.append([v.co[0], v.co[1], v.co[2]])

    faces = list()
    for f in mesh_object.data.polygons:
        v = f.vertices
        faces.append([v[0], v[1], v[2]])

    # Create an optimization mesh
    optimization_mesh = omesh.OptimizationMesh(vertices, faces)

    # Free the copies
    vertices.clear()
    faces.clear()

    # Optimize the mesh
    optimization_mesh.coarse_flat(0.05, 5, True)

    results = ''
    for i in range(n_iterations):
        if i > 0:
            optimization_mesh.smooth(15, 150, 1, False, True)

        # Get a copy to the vertex and face data
        vertices = optimization_mesh.get_vertex_data()
        faces = optimization_mesh.get_face_data()

        # Create a new mesh
        mesh_data = bpy.data.meshes.new("%s Data" % mesh_object.name)
        mesh_data.from_pydata(vertices, [], faces)
        mesh_data.update()

        # The optimized mesh
        created_mesh_object = bpy.data.objects.new("%s_optimized" % mesh_object.name, mesh_data)

        scene = bpy.context.scene
        scene.collection.objects.link(created_mesh_object)

        self_intersections = list(check_self_intersections_of_mesh_object(created_mesh_object))
        nmv.scene.delete_object_in_scene(created_mesh_object)

        results += '%d, SI[%d] \n' % (i, len(self_intersections))
        print(results)

        if len(self_intersections) == 0:
            break

    return results

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

    arg_help = 'Blender executable'
    parser.add_argument('--blender-executable',
                        action='store', dest='blender_executable', help=arg_help)

    arg_help = 'The input directory that contains the meshes'
    parser.add_argument('--input-directory', action='store', help=arg_help)

    arg_help = 'Output directory, where the final result stored'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    arg_help = 'Maximum number of smoothing iterations'
    parser.add_argument('--max-iterations',
                        action='store', default=1, type=int, help=arg_help)

    arg_help = 'Number of parallel cores'
    parser.add_argument('--num-cores',
                        action='store', default=1, type=int, help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @construct_per_mesh_command
####################################################################################################
def construct_per_mesh_command(args, input_mesh):

    command = ''
    command += ' %s ' % args.blender_executable
    command += ' -b --verbose 0 --python count_self_intersections.py -- '
    command += ' --input-directory %s ' % args.input_directory
    command += ' --input-mesh %s ' % input_mesh
    command += ' --output-directory %s ' % args.output_directory
    command += ' --max-iterations %s ' % int(args.max_iterations)
    return command


####################################################################################################
# @execute_command
####################################################################################################
def execute_command(command):

    print(command)
    subprocess.call(command, shell=True)


####################################################################################################
# @execute_commands_parallel
####################################################################################################
def execute_commands_parallel(shell_commands, num_cores):

    from joblib import Parallel, delayed
    Parallel(n_jobs=num_cores)(delayed(execute_command)(i) for i in shell_commands)


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Load all the OBJ meshes
    meshes_list = nmv.file.get_files_in_directory(args.input_directory, '.obj')
    commands = list()
    for input_mesh in meshes_list:
        commands.append(construct_per_mesh_command(args=args, input_mesh=input_mesh))

    execute_commands_parallel(commands, num_cores=args.num_cores)
